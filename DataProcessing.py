import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure Visualizations directory exists
os.makedirs('Visualizations', exist_ok=True)

# Assumes df is already loaded and contains columns like:
# 'Reported Date', 'Suburb', 'Offence Count', 'Offence Level 1 Description', 'Offence Level 2 Description'

df1 = pd.read_csv('Crime Statistics/2022-23_data_sa_crime.csv')
df2 = pd.read_csv('Crime Statistics/2023-24_data_sa_crime.csv')
df3 = pd.read_csv('Crime Statistics/2024-25_data_sa_crime.csv')
df = pd.concat([df1, df2, df3], ignore_index=True)

df.rename(columns={
    'Offence Level 1 Description': 'Offence Level 1',
    'Offence Level 2 Description': 'Offence Level 2',
    'Offence Level 3 Description': 'Offence Level 3',
    'Offence count': 'Offence Count',
    'Suburb - Incident': 'Suburb',
}, inplace=True)

# Ensure correct datetime parsing
df['Reported Date'] = pd.to_datetime(df['Reported Date'], dayfirst=True, errors='coerce')
df['Month'] = df['Reported Date'].dt.to_period('M')

# --- 1. Monthly Crime Trend ---
monthly_crime = df.groupby('Month')['Offence Count'].sum().sort_index()
plt.figure(figsize=(12, 5))
monthly_crime.plot(marker='o')
plt.title('Monthly Crime Trend (2022-25)')
plt.xlabel('Month')
plt.ylabel('Total Offences')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig('Visualizations/monthly_crime_trend.png')
plt.show()

# --- 2. Top 10 Offence Types ---
top_offences = df.groupby('Offence Level 1')['Offence Count'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
top_offences.plot(kind='barh', color='salmon')
plt.xlabel('Offence Count')
plt.title('Top 10 Offence Types (2022-25)')
plt.gca().invert_yaxis()
plt.grid(axis='x')
plt.tight_layout()
plt.savefig('Visualizations/top_10_offence_types.png')
plt.show()

# --- 3. Top 10 Suburbs by Total Crime ---
top_suburbs = df.groupby('Suburb')['Offence Count'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
top_suburbs.plot(kind='bar', color='steelblue')
plt.ylabel('Offence Count')
plt.title('Top 10 Crime Suburbs (2022-25)')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('Visualizations/top_10_crime_suburbs.png')
plt.show()

# --- 4. Heatmap of Suburb vs Crime Type ---
top_suburbs = df.groupby('Suburb')['Offence Count'].sum().sort_values(ascending=False).head(25).index
filtered_df = df[df['Suburb'].isin(top_suburbs)]

pivot = filtered_df.pivot_table(index='Suburb', columns='Offence Level 1', values='Offence Count', aggfunc='sum')
plt.figure(figsize=(10, 8))
sns.heatmap(np.log1p(pivot.fillna(0)), cmap='Reds', linewidths=0.5, annot=True, fmt=".1f")
plt.title("Crime Type by Suburb (Top 25, Log Scale)")
plt.xlabel("Crime Type")
plt.ylabel("Suburb")
plt.tight_layout()
plt.savefig('Visualizations/suburb_crime_heatmap_filtered.png')
plt.show()

# --- 6. Pie Chart of Offence Level 1 ---
offence_level1_counts = df['Offence Level 1'].value_counts()
plt.figure(figsize=(6, 6))
offence_level1_counts.plot.pie(autopct='%1.1f%%', startangle=140)
plt.title('Offence Level 1 Category Distribution')
plt.ylabel('')
plt.tight_layout()
plt.savefig('Visualizations/offence_level1_pie.png')
plt.show()

# --- 7. Top 10 Offence Level 2 Types ---
top_offences_lvl2 = df.groupby('Offence Level 2')['Offence Count'].sum().sort_values(ascending=False).head(
    10)
plt.figure(figsize=(10, 6))
top_offences_lvl2.plot(kind='barh', color='darkorange')
plt.xlabel('Offence Count')
plt.title('Top 10 Offence Level 2 Types (2022-25)')
plt.gca().invert_yaxis()
plt.grid(axis='x')
plt.tight_layout()
plt.savefig('Visualizations/top_10_offence_level2.png')
plt.show()
