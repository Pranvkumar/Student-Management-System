import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("used_cars_data.csv")
print(df.describe())
print("\n")
print(df.head())
print("\n")
print(df.info())
print("\n")
df.drop("New_Price",axis=1,inplace=True)    #To drop a column in dataset
missing_values = df.isnull().sum()
print(missing_values)
mean_value = df["Price"].mean()
print(mean_value)
df['Mileage'] = df['Mileage'].str.extract(r'([\d.]+)').astype(float)
df['Engine'] = df['Engine'].str.extract(r'([\d.]+)').astype(float)
df['Power'] = df['Power'].str.extract(r'([\d.]+)').astype(float)

df["Price"].fillna(df["Price"].mean(),inplace=True)
df["Seats"].fillna(df["Seats"].mean(),inplace=True)
df["Power"].fillna(df["Power"].mean(),inplace=True)
df["Engine"].fillna(df["Engine"].mean(),inplace=True)
df["Mileage"].fillna(df["Mileage"].mean(),inplace=True)     # repalce mean value with empty places 
missing_values = df.isnull().sum()
print(missing_values)
def remove_outliers_iqr(df):
    df = df.copy()
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 0.5 * IQR   
        upper_bound = Q3 + 0.25 * IQR  

        df.loc[df[col] < lower_bound, col] = None
        df.loc[(df[col] >= lower_bound) & (df[col] < Q1), col] = Q1
        df.loc[(df[col] > Q3) & (df[col] <= upper_bound), col] = Q3
        df.loc[df[col] > upper_bound, col] = None
    
    return df

df_clean = remove_outliers_iqr(df)
numeric_df = df.select_dtypes(include=['int64', 'float64'])
numeric_df = numeric_df.drop(columns=["S.No."], errors="ignore")
for col in numeric_df.columns:
    plt.figure(figsize=(6, 4))
    plt.boxplot(numeric_df[col].dropna())
    plt.title(f"Box Plot of {col}")
    plt.ylabel(col)
    plt.show()

numeric_df = df_clean.select_dtypes(include=['int64', 'float64'])
numeric_df = numeric_df.drop(columns=["S.No."], errors="ignore")
for col in numeric_df.columns:
    plt.figure(figsize=(6, 4))
    plt.boxplot(numeric_df[col].dropna())
    plt.title(f"Box Plot of {col} [Outliner_Removed]")
    plt.ylabel(col)
    plt.show()

