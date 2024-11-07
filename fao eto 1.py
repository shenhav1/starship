import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Set the display option to show all columns
pd.set_option('display.max_columns', None)

# Reading the Excel file of FAO ETo and VPD
fao_eto_file_path = r"C:\Users\shenh\Downloads\fao eto1.xlsx"
fao_eto_df = pd.read_excel(fao_eto_file_path)

# Saving the file as CSV in the starship folder on the Desktop
csv_file_path = r"C:\Users\shenh\Desktop\starship\fao eto1.csv"
fao_eto_df.to_csv(csv_file_path, index=False)

print("File has been successfully converted to CSV!")

# Removing all rows with missing values
fao_eto_cleaned = fao_eto_df.dropna()

# Normalizing the data to a 0-1 range
scaler = MinMaxScaler()

# Selecting only numeric columns
numeric_columns = fao_eto_cleaned.select_dtypes(include=['float64', 'int64']).columns
fao_eto_cleaned[numeric_columns] = scaler.fit_transform(fao_eto_cleaned[numeric_columns])

# Displaying the result after normalization
print("Data after normalization:")
print(fao_eto_cleaned.head())

# Saving the normalized file as a new CSV in the starship folder on the Desktop
final_csv_file_path = r"C:\Users\shenh\Desktop\starship\fao eto final.csv"
fao_eto_cleaned.to_csv(final_csv_file_path, index=True)

print(f"Cleaned and updated data saved successfully to {final_csv_file_path}!")

# Reading the saved file
fao_eto_file_path = r"C:\Users\shenh\Desktop\starship\fao eto final.csv"
fao_eto_df = pd.read_csv(fao_eto_file_path)

# Converting 'dt' column to datetime format
fao_eto_df['dt'] = pd.to_datetime(fao_eto_df['dt'], errors='coerce')

# Creating separate columns for Date and Time
fao_eto_df['Date'] = fao_eto_df['dt'].dt.date
fao_eto_df['Time'] = fao_eto_df['dt'].dt.time

# Filtering to keep only rows where the time is every 4 hours (e.g., 00:00, 04:00, 08:00, etc.)
fao_eto_df = fao_eto_df[fao_eto_df['Time'].astype(str).str.endswith("00:00") & (fao_eto_df['dt'].dt.hour % 4 == 0)]

# Rounding all numeric columns to 4 decimal places
fao_eto_df = fao_eto_df.round(4)

# Optionally, drop the original 'dt' column
fao_eto_df = fao_eto_df.drop(columns=['dt'])

# Resetting the index to start from 1
fao_eto_df = fao_eto_df.reset_index(drop=True)
fao_eto_df.index += 1

# Displaying the modified DataFrame
print(fao_eto_df.head())

# Saving the table with the new columns in the starship folder on the Desktop
final_csv_file_path = r"C:\Users\shenh\Desktop\starship\fao eto split final.csv"
fao_eto_df.to_csv(final_csv_file_path, index=False)

print(f"Data has been successfully saved to {final_csv_file_path}!")

# Removing the unnamed column "Unnamed: 0" if it exists
if 'Unnamed: 0' in fao_eto_df.columns:
    fao_eto_df = fao_eto_df.drop(columns=['Unnamed: 0'])

# Displaying the final DataFrame
print(fao_eto_df.head())

# Saving the final file without the unnamed column in the starship folder on the Desktop
final_csv_file_path = r"C:\Users\shenh\Desktop\starship\fao eto final without unnamed.csv"
fao_eto_df.to_csv(final_csv_file_path, index=False)

print(f"File has been successfully saved without the unnamed column to {final_csv_file_path}!")
