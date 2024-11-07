import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Set the display option to show all columns
pd.set_option('display.max_columns', None)

# Reading the CSV file
file_path = r"C:\Users\shenh\Desktop\starship\Frond data final.csv"
df = pd.read_csv(file_path)

# Combining 'Date' and 'Time' columns into a single 'DateTime' column
df['DateTime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'], errors='coerce')

# Remove rows where 'DateTime' is NaT (if any exist)
df = df.dropna(subset=['DateTime'])

# Filtering the data to include only rows where the time is every 4 hours
df = df[df['DateTime'].dt.minute == 0]  # Only on the hour
df = df[df['DateTime'].dt.hour % 4 == 0]  # Every 4 hours

# Drop the 'DateTime' column
df = df.drop(columns=['DateTime'])

# Dropping the unnamed column (if it exists)
if 'Unnamed: 0' in df.columns:
    df = df.drop(columns=['Unnamed: 0'])

# Normalizing numeric columns to a 0-1 range
scaler = MinMaxScaler()
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

# Resetting the index
df = df.reset_index(drop=True)

# Displaying the cleaned and normalized data
print("Data after filtering and normalization:")
print(df.head())

# Saving the filtered and normalized data
output_file_path = r"C:\Users\shenh\Desktop\starship\Frond data final filtered.csv"
df.to_csv(output_file_path, index=False)

print(f"Filtered and normalized data saved successfully to {output_file_path}!")

# Reading the filtered and normalized data
file_path = r"C:\Users\shenh\Desktop\starship\Frond data final filtered.csv"
df = pd.read_csv(file_path)

# Calculating the growth rate for each numeric column
growth_rate_df = pd.DataFrame()
for column in df.select_dtypes(include=['float64', 'int64']).columns:
    growth_rate_df[f"{column}_growth_rate"] = df[column].diff()

# Removing the first row, as the growth rate calculation produces NaN for the first entry
growth_rate_df = growth_rate_df.dropna().reset_index(drop=True)

# Adding Date and Time columns back to the growth rate DataFrame
growth_rate_df['Date'] = df['Date'][1:].reset_index(drop=True)  # Skip the first date
growth_rate_df['Time'] = df['Time'][1:].reset_index(drop=True)  # Skip the first time

# Reordering columns to have Date and Time first
growth_rate_df = growth_rate_df[['Date', 'Time'] + [col for col in growth_rate_df.columns if col not in ['Date', 'Time']]]

# Displaying the growth rate data
print("Growth rate data for each tree:")
print(growth_rate_df.head())

# Saving the growth rate data to a new CSV file
output_file_path = r"C:\Users\shenh\Desktop\starship\Frond growth rates.csv"
growth_rate_df.to_csv(output_file_path, index=False)

print(f"Growth rate data saved successfully to {output_file_path}!")

import pandas as pd
import matplotlib.pyplot as plt

# Reading the files
frond_data_path = r"C:\Users\shenh\Desktop\starship\Frond data final filtered.csv"
tensiometer_data_path = r"C:\Users\shenh\Desktop\starship\tensiometer data1 final.csv"

# Loading the data into DataFrames
frond_df = pd.read_csv(frond_data_path)
tensiometer_df = pd.read_csv(tensiometer_data_path)

# Converting the 'Date' column to a date format
frond_df['Date'] = pd.to_datetime(frond_df['Date'], errors='coerce')
tensiometer_df['Date'] = pd.to_datetime(tensiometer_df['Date'], errors='coerce')

# Merging the data on the 'Date' column, keeping only rows with matching dates
merged_df = pd.merge(frond_df, tensiometer_df, on='Date', how='inner')

# Comparing data for each tree at the depths (40 cm and 80 cm)
tree_columns = [col for col in frond_df.columns if col not in ['Date', 'Time']]

for tree in tree_columns:
    # Creating column names for 40 cm and 80 cm depths from the Tensiometer table
    tensiometer_40_col = f"{tree}_40"
    tensiometer_80_col = f"{tree}_80"

    # Checking if the columns exist in the Tensiometer table
    if tensiometer_40_col in tensiometer_df.columns and tensiometer_80_col in tensiometer_df.columns:
        # Creating a plot for each tree
        plt.figure(figsize=(12, 6))

        # Plotting the growth rate of the tree
        plt.plot(merged_df['Date'], merged_df[tree], label=f'{tree} Growth Rate', color='green', marker='o')

        # Plotting the pressure at 40 cm depth
        plt.plot(merged_df['Date'], merged_df[tensiometer_40_col], label=f'{tree} Pressure at 40 cm', color='blue',
                 linestyle='--')

        # Plotting the pressure at 80 cm depth
        plt.plot(merged_df['Date'], merged_df[tensiometer_80_col], label=f'{tree} Pressure at 80 cm', color='red',
                 linestyle='--')

        # Title and axis labels
        plt.title(f'Comparison of {tree} Growth Rate and Root Pressure')
        plt.xlabel('Date')
        plt.ylabel('Values')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

# Calculating the correlation between each tree's growth rate and the pressure at 40 cm and 80 cm depths
for tree in tree_columns:
    tensiometer_40_col = f"{tree}_40"
    tensiometer_80_col = f"{tree}_80"

    if tensiometer_40_col in merged_df.columns and tensiometer_80_col in merged_df.columns:
        # Calculating the correlation
        correlation_40 = merged_df[tree].corr(merged_df[tensiometer_40_col])
        correlation_80 = merged_df[tree].corr(merged_df[tensiometer_80_col])

        print(f"Correlation between {tree} growth rate and pressure at 40 cm: {correlation_40:.2f}")
        print(f"Correlation between {tree} growth rate and pressure at 80 cm: {correlation_80:.2f}\n")
