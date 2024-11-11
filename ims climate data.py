import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the Excel file from your specified location
file_path = r"C:\Users\shenh\Desktop\starship\ims climate data.xlsx"
# Make sure to use the correct function for an Excel file
Sap_flow_data = pd.read_excel(file_path)  # Use read_excel for Excel files
df = pd.DataFrame(Sap_flow_data)

# Set the display option to show all columns
pd.set_option('display.max_columns', None)

# Display original data structure
print("Original Data:")
print(df.head(2))

# Convert 'dt' column to datetime if it's not already in datetime format
df['dt'] = pd.to_datetime(df['dt'], errors='coerce')

# Plot Radiation over time
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.plot(df['dt'], df['Radiation (MJ/m2/hr)'], label='Radiation', color='orange')
plt.xlabel('Date and Time')
plt.ylabel('Radiation (MJ/m2/hr)')
plt.title('Radiation Over Time')
plt.xticks(rotation=45)
plt.grid(True)

# Plot Relative Humidity over time
plt.subplot(2, 2, 2)
plt.plot(df['dt'], df['relative humidity (%)'], label='Relative Humidity', color='blue')
plt.xlabel('Date and Time')
plt.ylabel('Relative Humidity (%)')
plt.title('Relative Humidity Over Time')
plt.xticks(rotation=45)
plt.grid(True)

# Plot Temperature over time
plt.subplot(2, 2, 3)
plt.plot(df['dt'], df['Temperature (oC)'], label='Temperature', color='red')
plt.xlabel('Date and Time')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Over Time')
plt.xticks(rotation=45)
plt.grid(True)

# Plot Wind Speed over time
plt.subplot(2, 2, 4)
plt.plot(df['dt'], df['wind speed at 2m (m/s)'], label='Wind Speed', color='green')
plt.xlabel('Date and Time')
plt.ylabel('Wind Speed (m/s)')
plt.title('Wind Speed Over Time')
plt.xticks(rotation=45)
plt.grid(True)

# Adjust layout and show plot
plt.tight_layout()
plt.show()

# Save the cleaned and upgraded DataFrame to a CSV file
output_path = r"C:\Users\shenh\Desktop\starship\cleaned_ims_climate_data.csv"
df.to_csv(output_path, index=False)
