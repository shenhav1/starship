
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Load the provided Excel file
file_path = r"C:\Users\shenh\Desktop\starship\irrigation and dendrometer.xlsx"
df = pd.read_excel(file_path)

# Extract relevant columns for 50% and 100% comparisons
df_50 = df[['date', '50% water_delta', '50% (L) irrigation']].dropna()
df_100 = df[['date', '100% water_delta', '100% (L) irrigation']].dropna()

# Convert 'date' column to datetime
df_50['date'] = pd.to_datetime(df_50['date'], errors='coerce')
df_100['date'] = pd.to_datetime(df_100['date'], errors='coerce')

# Calculate correlation for 50% irrigation
corr_50, _ = pearsonr(df_50['50% (L) irrigation'], df_50['50% water_delta'])
print(f"Correlation between 50% irrigation and 50% dendrometer change: {corr_50:.2f}")

# Plot 50% irrigation vs. dendrometer change
plt.figure(figsize=(10, 5))
plt.scatter(df_50['50% (L) irrigation'], df_50['50% water_delta'], color='blue', label='50% Irrigation')
plt.title('50% Irrigation vs. Dendrometer Change')
plt.xlabel('50% (L) Irrigation')
plt.ylabel('50% Water Delta')
plt.legend()
plt.grid(True)
plt.show()

# Calculate correlation for 100% irrigation
corr_100, _ = pearsonr(df_100['100% (L) irrigation'], df_100['100% water_delta'])
print(f"Correlation between 100% irrigation and 100% dendrometer change: {corr_100:.2f}")

# Plot 100% irrigation vs. dendrometer change
plt.figure(figsize=(10, 5))
plt.scatter(df_100['100% (L) irrigation'], df_100['100% water_delta'], color='green', label='100% Irrigation')
plt.title('100% Irrigation vs. Dendrometer Change')
plt.xlabel('100% (L) Irrigation')
plt.ylabel('100% Water Delta')
plt.legend()
plt.grid(True)
plt.show()
