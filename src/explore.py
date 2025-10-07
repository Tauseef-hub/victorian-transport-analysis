import pandas as pd

# Load the data
print("Loading data...")
df = pd.read_csv('data/annual_metropolitan_train_station_entries_fy_2024_2025.csv')

# See what we have
print("\n--- BASIC INFO ---")
print(f"Number of stations: {len(df)}")
print(f"Number of columns: {len(df.columns)}")

print("\n--- COLUMN NAMES ---")
for i, col in enumerate(df.columns, 1):
    print(f"{i}. {col}")

print("\n--- FIRST 3 STATIONS ---")
print(df.head(3))

print("\n--- DONE! ---")