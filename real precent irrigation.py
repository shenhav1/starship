import pandas as pd

# Load the provided Excel file and select the first sheet
file_path = r"C:\Users\shenh\Desktop\starship\Irrigation over ETo 1 (3).xlsx"
df = pd.read_excel(file_path, sheet_name=0)

# Remove the first column if it's an index column or not needed
if df.columns[0].lower() in ['index', 'unnamed']:
    df = df.iloc[:, 1:]

# Extract the 'date', '50% (L)', and '100% (L)' columns
columns_to_copy = df[['date', '50% (L)', '100% (L)']].copy()

# Convert the 'date' column to datetime
columns_to_copy['date'] = pd.to_datetime(columns_to_copy['date'], errors='coerce')

# Drop rows where the date could not be parsed (i.e., NaT values)
columns_to_copy = columns_to_copy.dropna(subset=['date'])

# Set the 'date' column as the index and ensure it's a DatetimeIndex
columns_to_copy.set_index('date', inplace=True)

# Resample the data to get weekly sums
weekly_data = columns_to_copy.resample('W').sum()

# Calculate the true percentage of the 50% irrigation compared to 100% irrigation
weekly_data['True Percentage'] = (weekly_data['50% (L)'] / weekly_data['100% (L)']) * 100

# Replace NaN or infinite values with 0
weekly_data['True Percentage'] = weekly_data['True Percentage'].fillna(0).replace([float('inf'), -float('inf')], 0)

# Format the 'True Percentage' to two decimal places and add the '%' sign
weekly_data['True Percentage'] = weekly_data['True Percentage'].apply(lambda x: f"{x:.2f}%")

# Reset the index to have 'Date' as a column again
weekly_data.reset_index(inplace=True)

# Save the new DataFrame to a CSV file
output_path = r"C:\Users\shenh\Desktop\starship\weekly_total_irrigation_with_percentage.csv"
weekly_data.to_csv(output_path, index=False)

# Print part of the table to check the results
print("Weekly Total Irrigation with Percentage (Sample):")
print(weekly_data.head())

print(f"Weekly percentage saved successfully to {output_path}!")
