import pandas as pd

# Load the provided dataset
file_path = r"C:\Users\shenh\Desktop\starship\cleaned_stem_dendometer.csv"
df = pd.read_csv(file_path)

# Ensure 'Date' is in datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Create a new DataFrame to store weekly delta values
weekly_delta_df = pd.DataFrame()

# Iterate over each numeric column to calculate weekly delta
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns

for column in numeric_columns:
    # Group data by week and calculate max and min for each week
    weekly_max = df.groupby(df['Date'].dt.to_period('W'))[column].max()
    weekly_min = df.groupby(df['Date'].dt.to_period('W'))[column].min()

    # Calculate the weekly delta (max - min)
    weekly_delta = weekly_max - weekly_min

    # Add the weekly delta to the new DataFrame
    weekly_delta_df[column + '_delta'] = weekly_delta

# Add the 'Week' column to the new DataFrame
weekly_delta_df['Week'] = weekly_max.index.astype(str)

# Reorder columns to have 'Week' first
weekly_delta_df = weekly_delta_df[['Week'] + [col for col in weekly_delta_df.columns if col != 'Week']]

# Display the new DataFrame with weekly deltas
print("Weekly Delta Data:")
print(weekly_delta_df.head())

# Save the new DataFrame to a CSV file
output_path = r"C:\Users\shenh\Desktop\starship\weekly_delta_stem_dendrometer.csv"
weekly_delta_df.to_csv(output_path, index=False)

print(f"Weekly delta values saved successfully to {output_path}!")
