import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

"" "" ""
# קריאת קובץ ה-Excel
excel_file_path = r"C:\Users\shenh\Downloads\Frond data 1.xlsx"
df = pd.read_excel(excel_file_path)

# שמירת הקובץ בפורמט CSV
csv_file_path = r"C:\Users\shenh\Downloads\Frond data 1.csv"
df.to_csv(csv_file_path, index=False)

print("הקובץ הומר בהצלחה ל-CSV!")
df_cleaned = df.dropna()  # מחיקה של כל השורות עם ערכים חסרים


# נרמול הנתונים בטווח של 0-1
scaler = MinMaxScaler()

# בחירת העמודות המספריות בלבד (מלבד עמודת הזמן)
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns  # נרמול של העמודות המספריות בלבד
df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

# הצגת התוצאה לאחר הנרמול
print("הנתונים לאחר הנרמול:")
print(df.head())

df['Date & time'] = pd.to_datetime(df['Date & time'])

df['Date'] = df['Date & time'].dt.date
df['Time'] = df['Date & time'].dt.time
df = df.drop(columns=['Date & time'])
df = df[df['Time'].astype(str).str.endswith("00:00")]

df = df.round(4)
df = df.reset_index(drop=True)
df.index += 1
print("הנתונים לאחר כל השינויים:")
print(df.head())
final_csv_file_path = r"C:\Users\shenh\Downloads\Frond data final.csv"
df.to_csv(final_csv_file_path, index=True)

print(f"הנתונים המסוננים והמעודכנים נשמרו בהצלחה ב-{final_csv_file_path}!")



# יצירת גרף לפי העמודות 'T2_D_50' ו-'T5_D_50'
plt.figure(figsize=(12, 6))

# ציור קווי המגמה של T2_D_50 ו-T5_D_50
plt.plot(df['Date'], df['T2_D_50'], label='T2_D_50', color='blue')
plt.plot(df['Date'], df['T7_E_100'], label='T7_E_100', color='orange')

# הוספת תוויות לצירים ולגרף
plt.xlabel('Date')
plt.ylabel('Values')
plt.title('Trend of T2_D_50 and T7_E_100 Over Time')

# סיבוב התוויות של ציר ה-X כדי למנוע חפיפה
plt.xticks(rotation=45)

# הצגת מקרא (legend) לנתונים
plt.legend()

# התאמה של מרווחים בגוף הגרף
plt.tight_layout()

# הצגת הגרף
plt.show()

"" "" ""

# חישוב קצב הצמיחה
df['T2_growth_rate'] = df['T2_D_50'].diff()
df['T9_growth_rate'] = df['T9_D_100'].diff()

# מחיקה של ערכים ריקים שנוצרו לאחר חישוב קצב הצמיחה
df = df.dropna(subset=['T2_growth_rate', 'T9_growth_rate'])

# מחיקה של ערכים שליליים שמייצגים קיצוץ לולב
df = df[(df['T2_growth_rate'] >= 0) & (df['T9_growth_rate'] >= 0)]

# הצגת קצב הצמיחה לאחר הניקוי
print("קצב הצמיחה לאחר הניקוי:")
print(df[['Date', 'T2_growth_rate', 'T9_growth_rate']])

# שמירת הקובץ הסופי לאחר הניקוי
final_csv_file_path = r"C:\Users\shenh\Downloads\Frond growth rate final.csv"
df.to_csv(final_csv_file_path, index=True)

print(f"הנתונים המסוננים נשמרו בהצלחה ב-{final_csv_file_path}!")


# יצירת גרף עבור קצב הצמיחה של שני העצים
plt.figure(figsize=(12, 6))

# גרף עבור קצב הצמיחה של T2_D_50
plt.plot(df['Date'], df['T2_growth_rate'], label='T2 Growth Rate', color='green', marker='o')

# גרף עבור קצב הצמיחה של T5_D_50
plt.plot(df['Date'], df['T9_growth_rate'], label='T9 Growth Rate', color='red', marker='x')

# הוספת תוויות לצירים
plt.xlabel('Date')
plt.ylabel('Growth Rate')

# הוספת כותרת לגרף
plt.title('Growth Rate of T2 and T9 Over Time')

# סיבוב התוויות של ציר ה-X כדי למנוע חפיפה
plt.xticks(rotation=45)

# הוספת מקרא (legend) לנתונים
plt.legend()

# התאמה של המרווחים בגוף הגרף
plt.tight_layout()

# הצגת הגרף
plt.show()