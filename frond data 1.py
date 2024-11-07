import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import matplotlib.dates as mdates
pd.set_option('display.max_columns', None)


# Reading the Excel file
excel_file_path = r"C:\Users\shenh\Downloads\Frond data 1.xlsx"
df = pd.read_excel(excel_file_path)

# Saving the file as CSV on the Desktop
csv_file_path = r"C:\Users\shenh\Desktop\Frond data 1.csv"
df.to_csv(csv_file_path, index=False)

print("File has been successfully converted to CSV!")
df_cleaned = df.dropna()  # Removing all rows with missing values

# Normalizing the data to a 0-1 range
scaler = MinMaxScaler()

# Selecting only numeric columns (excluding the time column)
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns  # Normalizing only the numeric columns
df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

# Displaying the data after normalization
print("Data after normalization:")
print(df.head())

df['Date & time'] = pd.to_datetime(df['Date & time'])

df['Date'] = df['Date & time'].dt.date
df['Time'] = df['Date & time'].dt.time
df = df.drop(columns=['Date & time'])
df = df[df['Time'].astype(str).str.endswith("00:00")]

df = df.round(4)
df = df.reset_index(drop=True)
df.index += 1
print("Data after all modifications:")
print(df.head())

# Saving the final cleaned and updated data on the Desktop
final_csv_file_path = r"C:\Users\shenh\Desktop\Frond data final.csv"
df.to_csv(final_csv_file_path, index=True)

print(f"Cleaned and updated data saved successfully to {final_csv_file_path}!")

# Calculating averages for columns starting with D, E, 100%, 50%
# Selecting only numeric columns for the averages calculation
df['D type irrigation avg'] = df.filter(regex=r"D").select_dtypes(include=['float64', 'int64']).mean(axis=1)
df['E type irrigation avg'] = df.filter(regex=r"E").select_dtypes(include=['float64', 'int64']).mean(axis=1)
df['100% water'] = df.filter(regex=r"_100$").select_dtypes(include=['float64', 'int64']).mean(axis=1)
df['50% water'] = df.filter(regex=r"_50$").select_dtypes(include=['float64', 'int64']).mean(axis=1)

# Displaying the result with the new columns
print("Data after calculating averages:")
print(df[['D type irrigation avg', 'E type irrigation avg', '100% water', '50% water']].head())

# Calculating growth rate for each column
df['D_type_growth_rate'] = df['D type irrigation avg'].diff()
df['E_type_growth_rate'] = df['E type irrigation avg'].diff()
df['100_growth_rate'] = df['100% water'].diff()
df['50_growth_rate'] = df['50% water'].diff()

# Removing rows with missing values after calculating growth rate
df = df.dropna(subset=['D_type_growth_rate', 'E_type_growth_rate', '100_growth_rate', '50_growth_rate'])

# Removing negative values representing frond cutting
df = df[(df['D_type_growth_rate'] >= 0) & (df['E_type_growth_rate'] >= 0) &
        (df['100_growth_rate'] >= 0) & (df['50_growth_rate'] >= 0)]

# Displaying growth rate after cleaning
print("Growth rate after cleaning:")
print(df[['Date', 'D_type_growth_rate', 'E_type_growth_rate', '100_growth_rate', '50_growth_rate']])

# First plot - Comparing growth rate between D and E types
plt.figure(figsize=(12, 6))

# Plot for D type irrigation avg growth rate
plt.plot(df['Date'], df['D_type_growth_rate'], label='D Type Growth Rate', color='blue', marker='o')

# Plot for E type irrigation avg growth rate
plt.plot(df['Date'], df['E_type_growth_rate'], label='E Type Growth Rate', color='orange', marker='x')

# Adding labels to axes
plt.xlabel('Date')
plt.ylabel('Growth Rate')

# Adding title to the plot
plt.title('Growth Rate Comparison: D Type vs E Type Irrigation')

# Rotating the x-axis labels to avoid overlapping
plt.xticks(rotation=45)

# Adding legend to the plot
plt.legend()

# Adjusting layout to prevent clipping
plt.tight_layout()

# Displaying the plot
plt.show()

# Second plot - Comparing growth rate between 100% and 50% irrigation
plt.figure(figsize=(12, 6))

# Plot for 100% water growth rate
plt.plot(df['Date'], df['100_growth_rate'], label='100% Water Growth Rate', color='green', marker='s')

# Plot for 50% water growth rate
plt.plot(df['Date'], df['50_growth_rate'], label='50% Water Growth Rate', color='red', marker='d')

# Adding labels to axes
plt.xlabel('Date')
plt.ylabel('Growth Rate')

# Adding title to the plot
plt.title('Growth Rate Comparison: 100% Water vs 50% Water')

# Rotating the x-axis labels to avoid overlapping
plt.xticks(rotation=45)

# Adding legend to the plot
plt.legend()

# Adjusting layout to prevent clipping
plt.tight_layout()

# Displaying the plot
plt.show()

# First plot - Comparison between 100% and 50% water amounts
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['100% water'], label='100% water')
plt.plot(df['Date'], df['50% water'], label='50% water')
plt.xlabel('Date')
plt.ylabel('Values')
plt.title('The effect of the amount of water on the growth of the frond')
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30))
plt.gca().xaxis.set_minor_locator(mdates.HourLocator(interval=90))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

# Second plot - Comparison between irrigation methods (D and E)
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['D type irrigation avg'], label='D type irrigation avg')
plt.plot(df['Date'], df['E type irrigation avg'], label='E type irrigation avg')
plt.xlabel('Date')
plt.ylabel('Values')
plt.title('The effect of the irrigation method on the growth of the frond')
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30))
plt.gca().xaxis.set_minor_locator(mdates.HourLocator(interval=90))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
