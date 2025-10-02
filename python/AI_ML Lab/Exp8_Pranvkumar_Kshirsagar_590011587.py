import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv('c:/Users/Prana/OneDrive/Desktop/coding/car_data.csv')

print("Dataset Info:")
print(df.info())
print("\nDataset Shape:", df.shape)
print("\nFirst few rows:")
print(df.head())

df_processed = df.copy()

le = LabelEncoder()
categorical_columns = ['Car_Name', 'Fuel_Type', 'Seller_Type', 'Transmission']

for col in categorical_columns:
    df_processed[col + '_encoded'] = le.fit_transform(df_processed[col])

numerical_cols = ['Year', 'Selling_Price', 'Present_Price', 'Kms_Driven', 'Owner']
encoded_cols = [col + '_encoded' for col in categorical_columns]
all_numerical_cols = numerical_cols + encoded_cols

correlation_matrix = df_processed[all_numerical_cols].corr()

display_correlation_matrix = correlation_matrix.copy()
display_correlation_matrix.columns = [col.replace('_encoded', '') for col in display_correlation_matrix.columns]
display_correlation_matrix.index = [idx.replace('_encoded', '') for idx in display_correlation_matrix.index]

print("=" * 60)
print("PHASE 1: CORRELATION ANALYSIS")
print("=" * 60)

fig, axes = plt.subplots(1, 2, figsize=(24, 10))

sns.heatmap(display_correlation_matrix, 
            annot=True, 
            cmap='coolwarm', 
            center=0,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": .8},
            fmt='.2f',
            ax=axes[0])
axes[0].set_title('Correlation Heatmap - All Variables', fontsize=16, fontweight='bold', pad=20)
axes[0].tick_params(axis='x', rotation=45, labelsize=10)
axes[0].tick_params(axis='y', rotation=0, labelsize=10)

price_cols = ['Selling_Price', 'Present_Price', 'Year', 'Kms_Driven', 'Owner']
price_corr = df_processed[price_cols].corr()
sns.heatmap(price_corr, 
            annot=True, 
            cmap='RdYlBu_r', 
            center=0,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": .8},
            fmt='.2f',
            ax=axes[1])
axes[1].set_title('Price-Related Variables Correlation', fontsize=16, fontweight='bold', pad=20)
axes[1].tick_params(axis='x', rotation=45, labelsize=12)
axes[1].tick_params(axis='y', rotation=0, labelsize=12)

plt.tight_layout()
plt.subplots_adjust(bottom=0.2)
plt.show()

print("\n" + "=" * 60)
print("PHASE 2: BUSINESS ANALYSIS")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(20, 16))

fuel_price_pivot = df.groupby('Fuel_Type')['Selling_Price'].mean().reset_index()
fuel_price_matrix = fuel_price_pivot.set_index('Fuel_Type').T
sns.heatmap(fuel_price_matrix, 
            annot=True, 
            cmap='viridis', 
            cbar_kws={"shrink": .8},
            fmt='.2f',
            ax=axes[0,0])
axes[0,0].set_title('Average Selling Price by Fuel Type', fontsize=14, fontweight='bold')

year_fuel_pivot = df.pivot_table(values='Selling_Price', 
                                 index='Year', 
                                 columns='Fuel_Type', 
                                 aggfunc='mean')
sns.heatmap(year_fuel_pivot, 
            annot=True, 
            cmap='plasma', 
            cbar_kws={"shrink": .8},
            fmt='.1f',
            ax=axes[0,1])
axes[0,1].set_title('Average Selling Price by Year and Fuel Type', fontsize=14, fontweight='bold')

trans_seller_pivot = df.pivot_table(values='Selling_Price',
                                    index='Transmission',
                                    columns='Seller_Type',
                                    aggfunc='mean')
sns.heatmap(trans_seller_pivot,
            annot=True,
            cmap='Blues',
            cbar_kws={"shrink": .8},
            fmt='.2f',
            ax=axes[1,0])
axes[1,0].set_title('Average Selling Price by Transmission and Seller Type', fontsize=14, fontweight='bold')

owner_fuel_pivot = df.pivot_table(values='Selling_Price',
                                  index='Owner',
                                  columns='Fuel_Type',
                                  aggfunc='mean')
sns.heatmap(owner_fuel_pivot,
            annot=True,
            cmap='Reds',
            cbar_kws={"shrink": .8},
            fmt='.2f',
            ax=axes[1,1])
axes[1,1].set_title('Average Selling Price by Owner Count and Fuel Type', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.show()

print("\n" + "=" * 60)
print("PHASE 3: DATA QUALITY ANALYSIS")
print("=" * 60)

plt.figure(figsize=(14, 8))
sns.heatmap(df.isnull(), 
            yticklabels=False, 
            cbar=True, 
            cmap='viridis')
plt.title('Missing Values Heatmap', fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Columns', fontsize=14)
plt.ylabel('Rows', fontsize=14)
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(18, 8))

brand_counts = df['Car_Name'].value_counts().head(10)
top_brands = brand_counts.index
brand_price_data = []
for brand in top_brands:
    brand_data = df[df['Car_Name'] == brand]['Selling_Price'].values
    brand_price_data.append(brand_data)

brand_price_matrix = pd.DataFrame({brand: pd.cut(df[df['Car_Name'] == brand]['Selling_Price'], 
                                                 bins=5, labels=['Low', 'Med-Low', 'Medium', 'Med-High', 'High']).value_counts()
                                  for brand in top_brands if not df[df['Car_Name'] == brand].empty}).fillna(0)

sns.heatmap(brand_price_matrix, 
            annot=True, 
            cmap='YlOrRd', 
            fmt='.0f',
            cbar_kws={"shrink": .8},
            ax=axes[0])
axes[0].set_title('Price Range Distribution by Top Car Brands', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Car Brands', fontsize=12)
axes[0].set_ylabel('Price Ranges', fontsize=12)

df['Car_Age'] = 2018 - df['Year']
age_price_pivot = pd.crosstab(pd.cut(df['Car_Age'], bins=5), 
                              pd.cut(df['Selling_Price'], bins=5))
sns.heatmap(age_price_pivot, 
            annot=True, 
            cmap='coolwarm', 
            fmt='.0f',
            cbar_kws={"shrink": .8},
            ax=axes[1])
axes[1].set_title('Car Age vs Selling Price Distribution', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Selling Price Ranges', fontsize=12)
axes[1].set_ylabel('Car Age Ranges', fontsize=12)

plt.tight_layout()
plt.show()

print("\nSummary Statistics:")
print(df.describe())

print("\nTop 5 Positive Correlations with Selling Price:")
selling_price_corr = correlation_matrix['Selling_Price'].sort_values(ascending=False)
print(selling_price_corr.head())

print("\nTop 5 Negative Correlations with Selling Price:")
print(selling_price_corr.tail())
