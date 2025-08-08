import pandas as pd
import numpy as np
import os

# Load and combine data from all three years
df1 = pd.read_csv('Crime Statistics/2022-23_data_sa_crime.csv')
df2 = pd.read_csv('Crime Statistics/2023-24_data_sa_crime.csv')
df3 = pd.read_csv('Crime Statistics/2024-25_data_sa_crime.csv')
df = pd.concat([df1, df2, df3], ignore_index=True)

# Standardize column names
df.rename(columns={
    'Offence Level 1 Description': 'Offence Level 1',
    'Offence Level 2 Description': 'Offence Level 2',
    'Offence Level 3 Description': 'Offence Level 3',
    'Offence count': 'Offence Count',
    'Suburb - Incident': 'Suburb',
}, inplace=True)

# Parse reported date and extract month
df['Reported Date'] = pd.to_datetime(df['Reported Date'], dayfirst=True, errors='coerce')
df['Month'] = df['Reported Date'].dt.to_period('M').dt.to_timestamp()

# Optional: Ensure output directory exists
os.makedirs('Outputs', exist_ok=True)


# Step 1: Aggregate by Suburb × Offence Level 1 × Offence Level 2 × Month
model_df = df.groupby(['Suburb', 'Offence Level 1', 'Offence Level 2', 'Month'])['Offence Count'].sum().reset_index()
model_df = model_df.rename(columns={'Offence Count': 'offence_count'})
model_df = model_df.sort_values(by=['Suburb', 'Offence Level 1', 'Offence Level 2', 'Month'])

# Step 2: Create lag_1 to lag_12 features to capture historical offence counts
for lag in range(1, 13):
    model_df[f'lag_{lag}'] = model_df.groupby(['Suburb', 'Offence Level 1', 'Offence Level 2'])['offence_count'].shift(lag)

# Step 3: Drop rows with any missing lag values
lag_cols = [f'lag_{i}' for i in range(1, 13)]
model_df = model_df.dropna(subset=lag_cols)

# Step 4: Optional statistical features
model_df['avg_lag_3'] = model_df[[f'lag_{i}' for i in range(1, 4)]].mean(axis=1)
model_df['std_lag_3'] = model_df[[f'lag_{i}' for i in range(1, 4)]].std(axis=1)

# Step 5: Extract month number
model_df['month'] = model_df['Month'].dt.month

# Step 6: Save to CSV
model_df.to_csv('crime_model_data.csv', index=False)
print("✅ crime_model_data.csv exported successfully.")
