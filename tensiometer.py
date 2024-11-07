import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Set the display option to show all columns
pd.set_option('display.max_columns', None)

# Reading the Excel file of Tensiometer data
tensiometer_file_path = r"C:\Users\shenh\Downloads\tensiometer data1.xlsx"
tensiometer_df = pd.read_excel(tensiometer_file_path)

# Saving the file as CSV on the Desktop
csv_file_path = r"C:\Users\shenh\Desktop\starship\tensiometer data1.csv"
tensiometer_df.to_csv(csv_file_path, index=False)

print("Tensiometer data file has been successfully converted to CSV!")

# Removing all rows with missing values
tensiometer_df_cleaned = tensiometer_df.dropna()

# Normalizing the data to a 0-1 range
scaler = MinMaxScaler()

# Selecting only numeric columns
numeric_columns = tensiometer_df_cleaned.select_dtypes(include=['float64', 'int64']).columns
tensiometer_df_cleaned[numeric_columns] = scaler.fit_transform(tensiometer_df_cleaned[numeric_columns])

# Displaying the result after normalization
print("Data after normalization:")
print(tensiometer_df_cleaned.head())

# Saving the normalized file as a new CSV on the Desktop
normalized_csv_file_path = r"C:\Users\shenh\Desktop\starship\tensiometer data1 normalized.csv"
tensiometer_df_cleaned.to_csv(normalized_csv_file_path, index=True)

print(f"Cleaned and normalized data saved successfully to {normalized_csv_file_path}!")

# Reading the saved file
tensiometer_df_path = r"C:\Users\shenh\Desktop\starship\tensiometer data1 normalized.csv"
tensiometer_df_cleaned = pd.read_csv(tensiometer_df_path)

# Converting 'dt' column to datetime format
tensiometer_df_cleaned['dt'] = pd.to_datetime(tensiometer_df_cleaned['dt'])

# Creating separate columns for Date and Time
tensiometer_df_cleaned['Date'] = tensiometer_df_cleaned['dt'].dt.date
tensiometer_df_cleaned['Time'] = tensiometer_df_cleaned['dt'].dt.time

# Filtering the data to include only rows where the time is every 4 hours
tensiometer_df_cleaned = tensiometer_df_cleaned[tensiometer_df_cleaned['dt'].dt.minute == 0]
tensiometer_df_cleaned = tensiometer_df_cleaned[tensiometer_df_cleaned['dt'].dt.hour % 4 == 0]

# Removing the original 'dt' column if no longer needed
tensiometer_df_cleaned = tensiometer_df_cleaned.drop(columns=['dt'])

# Displaying the table after splitting Date and Time
print(tensiometer_df_cleaned.head())

# Saving the table with the new columns on the Desktop
split_csv_file_path = r"C:\Users\shenh\Desktop\starship\tensiometer data1 split.csv"
tensiometer_df_cleaned.to_csv(split_csv_file_path, index=False)

print(f"Data has been successfully saved to {split_csv_file_path}!")

# Reading the saved file with the "Unnamed" column
tensiometer_df_path = r"C:\Users\shenh\Desktop\starship\tensiometer data1 split.csv"
tensiometer_df_cleaned = pd.read_csv(tensiometer_df_path)

# Removing the unnamed column "Unnamed: 0"
if 'Unnamed: 0' in tensiometer_df_cleaned.columns:
    tensiometer_df_cleaned = tensiometer_df_cleaned.drop(columns=['Unnamed: 0'])

# Displaying the table after removing the column
print(tensiometer_df_cleaned.head())

# Saving the file without the unnamed column on the Desktop
final_csv_file_path = r"C:\Users\shenh\Desktop\starship\tensiometer data1 final.csv"
tensiometer_df_cleaned.to_csv(final_csv_file_path, index=False)

print(f"File has been successfully saved without the unnamed column to {final_csv_file_path}!")

# Reading the updated file
file_path = r"C:\Users\shenh\Desktop\starship\tensiometer data1 final.csv"
df = pd.read_csv(file_path)

# Adding the code from your friend to create new average columns
df['D type irrigation avg'] = df.filter(regex=r"D").apply(pd.to_numeric, errors='coerce').mean(axis=1)
df['E type irrigation avg'] = df.filter(regex=r"E").apply(pd.to_numeric, errors='coerce').mean(axis=1)
df['100% water'] = df.filter(regex=r"_100$").apply(pd.to_numeric, errors='coerce').mean(axis=1)
df['50% water'] = df.filter(regex=r"_50$").apply(pd.to_numeric, errors='coerce').mean(axis=1)
df['40 cm depth'] = df.filter(regex=r"_40").apply(pd.to_numeric, errors='coerce').mean(axis=1)
df['80 cm depth'] = df.filter(regex=r"_80").apply(pd.to_numeric, errors='coerce').mean(axis=1)

# Filling NaN values with 0
df = df.fillna(0)

# Displaying the result with Date and Time columns
print("Updated Data with New Columns (NaN values replaced with 0):")
print(df[['Date', 'Time', 'D type irrigation avg', 'E type irrigation avg', '100% water', '50% water', '40 cm depth', '80 cm depth']].head())

# Saving the table with the new average columns
output_file_path = r"C:\Users\shenh\Desktop\starship\tensiometer data1 averages.csv"
df.to_csv(output_file_path, index=False)

print(f"File with average columns has been saved successfully to {output_file_path}!")
