import pandas as pd
import numpy as np  # Importing numpy
import matplotlib.pyplot as plt

# Load the Excel file from your specified location
file_path = r"C:\Users\shenh\Desktop\starship\tdr salt.xlsx"
Sap_flow_data = pd.read_excel(file_path)
df = pd.DataFrame(Sap_flow_data)

# Convert 'dt' column to datetime
df['dt'] = pd.to_datetime(df['dt'], errors='coerce')

# Create separate date and time columns
df['Date'] = df['dt'].dt.date
df['Time'] = df['dt'].dt.time

# Keep measurements only every four hours
df = df[df['Time'].astype(str).str.endswith("00:00") & (df['dt'].dt.hour % 4 == 0)]

# Round all numeric columns to 4 decimal places
df = df.round(4)

# Drop the original 'dt' column
df = df.drop(columns=['dt'])

# Reset index to start from 1
df = df.reset_index(drop=True)
df.index += 1

# Calculate averages for the new columns using regex patterns
df['D type irrigation avg'] = df.filter(regex=r"_D_").apply(pd.to_numeric, errors='coerce').mean(axis=1)
df['E type irrigation avg'] = df.filter(regex=r"_E_").apply(pd.to_numeric, errors='coerce').mean(axis=1)
df['100% water'] = df.filter(regex=r"_100_").apply(pd.to_numeric, errors='coerce').mean(axis=1)
df['50% water'] = df.filter(regex=r"_50_").apply(pd.to_numeric, errors='coerce').mean(axis=1)
df['40 cm depth'] = df.filter(regex=r"_40").apply(pd.to_numeric, errors='coerce').mean(axis=1)
df['80 cm depth'] = df.filter(regex=r"_80").apply(pd.to_numeric, errors='coerce').mean(axis=1)

print("Updated Data with New Columns:")
print(df[['D type irrigation avg', 'E type irrigation avg', '100% water', '50% water', '40 cm depth', '80 cm depth', 'Date', 'Time']].head())

# First graph - effect of irrigation type on sensor depths
depths = ['40 cm depth', '80 cm depth']
d_type_values = [df['D type irrigation avg'].mean(), df['80 cm depth'].mean()]
e_type_values = [df['E type irrigation avg'].mean(), df['80 cm depth'].mean()]

plt.figure(figsize=(10, 6))
plt.plot(depths, d_type_values, marker='o', label='D Type Irrigation')
plt.plot(depths, e_type_values, marker='o', label='E Type Irrigation')
plt.title('Effect of Irrigation Type on Sensor Depths (40 cm vs 80 cm)')
plt.xlabel('Sensor Depth')
plt.ylabel('Average Sensor Value')
plt.legend()
plt.grid()
plt.show()

# Second graph - comparison of D and E irrigation types at 50% water
d_type_50_percent = df.filter(regex=r"T\d+_D_50").apply(pd.to_numeric, errors='coerce').mean(axis=1).mean()
e_type_50_percent = df.filter(regex=r"T\d+_E_50").apply(pd.to_numeric, errors='coerce').mean(axis=1).mean()

# Check for NaN or Inf values and replace them with 0 or some default value
average_values = [d_type_50_percent, e_type_50_percent]
average_values = [0 if pd.isna(val) or np.isinf(val) else val for val in average_values]

irrigation_types = ['D Type', 'E Type']

plt.figure(figsize=(8, 5))
plt.bar(irrigation_types, average_values, color=['blue', 'green'])
plt.title('Comparison of D and E Irrigation Types at 50% Water')
plt.xlabel('Irrigation Type')
plt.ylabel('Average Sensor Value')
plt.ylim(0, max(average_values) * 1.1)
plt.grid(axis='y')
plt.show()

# Save the cleaned and upgraded DataFrame to a CSV file
output_path = r"C:\Users\shenh\Desktop\starship\cleaned_tdr_salt.csv"
df.to_csv(output_path, index=False)