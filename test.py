import pandas as pd

# Reading the updated file
file_path = r"C:\Users\shenh\Desktop\tensiometer data1 final.csv"
df = pd.read_csv(file_path)

# Printing the column names to check
print("Column names in the DataFrame:")
print(df.columns)
