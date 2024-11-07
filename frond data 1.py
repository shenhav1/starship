import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import matplotlib.dates as mdates
pd.set_option('display.max_columns', None)

# Create the "starship" folder on the Desktop if it doesn't exist
desktop_path = r"C:\Users\shenh\Desktop"
starship_folder = os.path.join(desktop_path, "starship")
if not os.path.exists(starship_folder):
    os.makedirs(starship_folder)

# Reading the Excel file
excel_file_path = r"C:\Users\shenh\Downloads\Frond data 1.xlsx"
df = pd.read_excel(excel_file_path)

# Saving the file as CSV in the "starship" folder on the Desktop
csv_file_path = os.path.join(starship_folder, "Frond data 1.csv")
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

# Filtering to include only rows where the time is every 4 hours
df = df[df['Date & time'].dt.hour % 4 == 0]

# Dropping the original 'Date & time' column
df = df.drop(columns=['Date & time'])

df = df.round(4)
df = df.reset_index(drop=True)
df.index += 1
print("Data after all modifications:")
print(df.head())

# Saving the final cleaned and updated data on the Desktop
final_csv_file_path = os.path.join(starship_folder, "Frond data final.csv")
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

# Saving the table with Date, Time, and growth rates as a CSV file
growth_rate_csv_path = os.path.join(starship_folder, "Frond growth rates.csv")
df[['Date', 'Time', 'D_type_growth_rate', 'E_type_growth_rate', '100_growth_rate', '50_growth_rate']].to_csv(growth_rate_csv_path, index=False)

print(f"Growth rates with Date and Time have been successfully saved to {growth_rate_csv_path}!")

# The rest of the plotting code...
