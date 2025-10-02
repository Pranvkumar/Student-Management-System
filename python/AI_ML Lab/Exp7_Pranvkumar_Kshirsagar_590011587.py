import pandas as pd
from sklearn.preprocessing import OneHotEncoder

df = pd.read_csv("used_cars_data.csv")
print(df.describe())

print("\nNumber of unique values in each column:")
print(df.nunique())

df['Name_Brand'] = df['Name'].str.split().str[0]
Name_Brand = df['Name_Brand'].value_counts()
print("\n" + "="*50 + "\n")
print("Car brands grouped by name:")
print(Name_Brand)

df.to_csv("used_cars_with_brand.csv", index=False)
print("\n" + "="*50 + "\n")
print("A new column 'Brand' has been created and the data has been saved to 'used_cars_with_brand.csv'.")
print("First 5 rows of the new DataFrame:")
print(df.head())

dataframe = pd.read_csv("used_cars_with_brand.csv")
print("\nNumber of unique values in each column:")
print(dataframe.nunique())

Name_Brand = dataframe['Name_Brand'].value_counts()
print("\n" + "="*50 + "\n")
print("Car brands grouped by name:")
print(Name_Brand)


unique_Brands = sorted(dataframe['Name_Brand'].unique())
Brand_to_index = {Name_Brand: idx for idx, Name_Brand in enumerate(unique_Brands)}
dataframe['Name_Brand_encoded'] = dataframe['Name_Brand'].map(Brand_to_index)

print("Name_Brand encoding mapping:")
for Name_Brand, idx in Brand_to_index.items():
    print(f"{idx}: {Name_Brand}")

dataframe.to_csv("used_cars_with_brand_and_encoded.csv", index=False)

print("\n" + "="*50 + "\n")
print("A new CSV file 'used_cars_with_brand_and_encoded.csv' has been created with the 'Company_encoded' column.")
print("First 5 rows of the new DataFrame:")
print(dataframe.head())

unique_Brands = sorted(dataframe['Name_Brand'].unique())
Brand_to_index = {Name_Brand: idx for idx, Name_Brand in enumerate(unique_Brands)}
dataframe['Name_Brand_encoded'] = dataframe['Name_Brand'].map(Brand_to_index)

print("Name_Brand encoding mapping:")
for Name_Brand, idx in Brand_to_index.items():
    print(f"{idx}: {Name_Brand}")


# Use OneHotEncoder for the Name_Brand column and concatenate
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
encoded_brands_sklearn = encoder.fit_transform(dataframe[['Name_Brand']])
encoded_brands_sklearn_df = pd.DataFrame(encoded_brands_sklearn, columns=encoder.get_feature_names_out(['Name_Brand']))

print("\n" + "="*50 + "\n")
print("One-hot encoded 'Name_Brand' column (using sklearn) shape:")
print(encoded_brands_sklearn_df.shape)
print("\nFirst 5 rows of the one-hot encoded 'Name_Brand' DataFrame (sklearn):")
print(encoded_brands_sklearn_df.head())

# Combine the original dataframe with the one-hot encoded columns
final_dataframe = pd.concat([dataframe, encoded_brands_sklearn_df], axis=1)

# Save the final DataFrame to a new CSV file
final_dataframe.to_csv("used_cars_with_brand_and_encoded.csv", index=False)

print("\n" + "="*50 + "\n")
print("A new CSV file 'used_cars_with_brand_and_encoded.csv' has been created.")
print("It includes the original data plus the one-hot encoded columns.")
print("First 5 rows of the new DataFrame:")
print(final_dataframe.head())
