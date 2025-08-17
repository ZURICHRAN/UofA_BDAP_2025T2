import pandas as pd
import matplotlib.pyplot as plt
import os

# Set file path relative to project directory
file_path = 'Total Value of Dwellings/643201.xlsx'

# Step 1: Load with correct header row (first line as column names)
df = pd.read_excel(file_path, sheet_name='Data1', header=0)

# Step 2: Skip down to where data begins (after metadata rows)
df = df.iloc[9:].reset_index(drop=True)

# Save cleaned dataframe for inspection (after initial load/cleanup)
df.to_csv('Total Value of Dwellings/643201_cleaned_data.csv', index=False)
print('Saved cleaned data to Total Value of Dwellings/643201_cleaned_data.csv')

# Step 3: Rename date column and convert
df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
df['Date'] = pd.to_datetime(df['Date'], format='%m-%Y', errors='coerce')

print(df.columns.tolist())
# Select and rename relevant columns for South Australia
df_sa = df[['Date',
            'Value of dwelling stock; Owned by Households ;  South Australia ;',
            'Number of residential dwellings ;  South Australia ;']]
df_sa.columns = ['Date', 'Dwelling Value (SA)', 'Dwelling Count (SA)']

# Compute average dwelling price
df_sa['Average Price (SA)'] = df_sa['Dwelling Value (SA)'] * 1e6 / (df_sa['Dwelling Count (SA)'] * 1e3)

# Plot dwelling value and average price
os.makedirs('Visualizations', exist_ok=True)

plt.figure(figsize=(12, 6))
plt.plot(df_sa['Date'], df_sa['Dwelling Value (SA)'], label='Dwelling Value (Millions)')
plt.title('South Australia Total Dwelling Stock Value Over Time')
plt.xlabel('Date')
plt.ylabel('Value ($ Millions)')
plt.grid(True)
plt.tight_layout()
plt.legend()
plt.savefig('Visualizations/sa_dwelling_value_trend.png')
plt.show()



plt.figure(figsize=(12, 6))
plt.plot(df_sa['Date'], df_sa['Average Price (SA)'], color='orange', label='Average Dwelling Price')
plt.title('South Australia Average Dwelling Price Over Time')
plt.xlabel('Date')
plt.ylabel('Price ($)')
plt.grid(True)
plt.tight_layout()
plt.legend()
plt.savefig('Visualizations/sa_average_dwelling_price_trend.png')
plt.show()

# 1. Year-on-Year Growth of Average Price
df_sa['YoY Avg Price Growth (%)'] = df_sa['Average Price (SA)'].pct_change(periods=4) * 100
plt.figure(figsize=(12, 6))
plt.plot(df_sa['Date'], df_sa['YoY Avg Price Growth (%)'], marker='o', color='green')
plt.title('South Australia YoY Growth in Average Dwelling Price')
plt.xlabel('Date')
plt.ylabel('Growth Rate (%)')
plt.grid(True)
plt.tight_layout()
plt.savefig('Visualizations/sa_yoy_avg_price_growth.png')
plt.show()

# 2. Dwelling Count vs Avg Price Scatter
plt.figure(figsize=(8, 6))
plt.scatter(df_sa['Dwelling Count (SA)'], df_sa['Average Price (SA)'], alpha=0.7)
plt.title('SA Dwelling Count vs Average Price')
plt.xlabel('Dwelling Count (000s)')
plt.ylabel('Average Price (AUD)')
plt.grid(True)
plt.tight_layout()
plt.savefig('Visualizations/sa_dwelling_count_vs_price.png')
plt.show()

# 3. SA Dwelling Value by Ownership Type
df['Date'] = pd.to_datetime(df['Date'], format='%m-%Y', errors='coerce')
value_cols = [
    'Value of dwelling stock; Owned by Households ;  South Australia ;',
    'Value of dwelling stock; Owned by Non-Households ;  South Australia ;',
    'Value of dwelling stock; Owned by All Sectors ;  South Australia ;'
]
labels = ['Households', 'Non-Households', 'All Sectors']
plt.figure(figsize=(12, 6))
for col, label in zip(value_cols, labels):
    plt.plot(df['Date'], df[col], label=label)
plt.title('SA Dwelling Stock Value by Ownership Type')
plt.xlabel('Date')
plt.ylabel('Value (Million AUD)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('Visualizations/sa_value_by_owner_type.png')
plt.show()
