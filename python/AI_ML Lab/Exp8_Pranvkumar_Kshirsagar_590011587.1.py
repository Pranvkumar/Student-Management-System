import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

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

numerical_cols = ['Year', 'Present_Price', 'Kms_Driven', 'Owner']
encoded_cols = [col + '_encoded' for col in categorical_columns]
feature_cols = numerical_cols + encoded_cols

X = df_processed[feature_cols]
y = df_processed['Selling_Price']

print("=" * 60)
print("ORIGINAL DATA ANALYSIS")
print("=" * 60)

correlation_matrix = df_processed[feature_cols + ['Selling_Price']].corr()
display_correlation_matrix = correlation_matrix.copy()
display_correlation_matrix.columns = [col.replace('_encoded', '') for col in display_correlation_matrix.columns]
display_correlation_matrix.index = [idx.replace('_encoded', '') for idx in display_correlation_matrix.index]

plt.figure(figsize=(12, 10))
sns.heatmap(display_correlation_matrix, 
            annot=True, 
            cmap='coolwarm', 
            center=0,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": .8},
            fmt='.2f')
plt.title('Original Features Correlation Heatmap', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.show()

print("=" * 60)
print("PCA IMPLEMENTATION")
print("=" * 60)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA()
X_pca = pca.fit_transform(X_scaled)

explained_variance_ratio = pca.explained_variance_ratio_
cumulative_variance_ratio = np.cumsum(explained_variance_ratio)

print("Explained Variance Ratio for each component:")
for i, ratio in enumerate(explained_variance_ratio):
    print(f"PC{i+1}: {ratio:.4f} ({ratio*100:.2f}%)")

print(f"\nCumulative Explained Variance:")
for i, cum_ratio in enumerate(cumulative_variance_ratio):
    print(f"First {i+1} components: {cum_ratio:.4f} ({cum_ratio*100:.2f}%)")

fig, axes = plt.subplots(2, 2, figsize=(20, 16))

axes[0,0].plot(range(1, len(explained_variance_ratio) + 1), explained_variance_ratio, 'bo-')
axes[0,0].set_xlabel('Principal Component')
axes[0,0].set_ylabel('Explained Variance Ratio')
axes[0,0].set_title('Scree Plot - Individual Variance Explained')
axes[0,0].grid(True)

axes[0,1].plot(range(1, len(cumulative_variance_ratio) + 1), cumulative_variance_ratio, 'ro-')
axes[0,1].axhline(y=0.95, color='k', linestyle='--', alpha=0.7)
axes[0,1].axhline(y=0.90, color='g', linestyle='--', alpha=0.7)
axes[0,1].set_xlabel('Principal Component')
axes[0,1].set_ylabel('Cumulative Explained Variance Ratio')
axes[0,1].set_title('Cumulative Variance Explained')
axes[0,1].grid(True)
axes[0,1].legend(['Cumulative Variance', '95% Threshold', '90% Threshold'])

n_components_95 = np.argmax(cumulative_variance_ratio >= 0.95) + 1
n_components_90 = np.argmax(cumulative_variance_ratio >= 0.90) + 1
n_components_fixed = 3

print(f"\nComponents needed for 90% variance: {n_components_90}")
print(f"Components needed for 95% variance: {n_components_95}")
print(f"Using fixed 3 components: {cumulative_variance_ratio[n_components_fixed-1]*100:.2f}% variance retained")

pca_reduced = PCA(n_components=n_components_fixed)
X_pca_reduced = pca_reduced.fit_transform(X_scaled)

pca_df = pd.DataFrame(X_pca_reduced, columns=[f'PC{i+1}' for i in range(n_components_fixed)])
pca_df['Selling_Price'] = y

pca_correlation = pca_df.corr()
sns.heatmap(pca_correlation, 
            annot=True, 
            cmap='coolwarm', 
            center=0,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": .8},
            fmt='.2f',
            ax=axes[1,0])
axes[1,0].set_title(f'PCA Components Correlation', fontsize=14, fontweight='bold')

components_df = pd.DataFrame(pca_reduced.components_.T, 
                            columns=[f'PC{i+1}' for i in range(n_components_fixed)],
                            index=[col.replace('_encoded', '') for col in feature_cols])
sns.heatmap(components_df, 
            annot=True, 
            cmap='RdBu_r', 
            center=0,
            cbar_kws={"shrink": .8},
            fmt='.2f',
            ax=axes[1,1])
axes[1,1].set_title('Feature Contributions to Principal Components', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.show()

print("=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
X_train_pca, X_test_pca, _, _ = train_test_split(X_pca_reduced, y, test_size=0.2, random_state=42)

model_original = LinearRegression()
model_original.fit(X_train, y_train)
y_pred_original = model_original.predict(X_test)

model_pca = LinearRegression()
model_pca.fit(X_train_pca, y_train)
y_pred_pca = model_pca.predict(X_test_pca)

mse_original = mean_squared_error(y_test, y_pred_original)
r2_original = r2_score(y_test, y_pred_original)

mse_pca = mean_squared_error(y_test, y_pred_pca)
r2_pca = r2_score(y_test, y_pred_pca)

print("Original Features Model:")
print(f"Mean Squared Error: {mse_original:.4f}")
print(f"R² Score: {r2_original:.4f}")
print(f"Features used: {len(feature_cols)}")

print(f"\nPCA Model (3 components):")
print(f"Mean Squared Error: {mse_pca:.4f}")
print(f"R² Score: {r2_pca:.4f}")
print(f"Features used: 3")
print(f"Variance retained: {cumulative_variance_ratio[n_components_fixed-1]*100:.2f}%")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

axes[0].scatter(y_test, y_pred_original, alpha=0.7)
axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
axes[0].set_xlabel('Actual Selling Price')
axes[0].set_ylabel('Predicted Selling Price')
axes[0].set_title(f'Original Features Model\nR² = {r2_original:.4f}')
axes[0].grid(True, alpha=0.3)

axes[1].scatter(y_test, y_pred_pca, alpha=0.7, color='green')
axes[1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
axes[1].set_xlabel('Actual Selling Price')
axes[1].set_ylabel('Predicted Selling Price')
axes[1].set_title(f'PCA Model (3 components)\nR² = {r2_pca:.4f}')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\n" + "=" * 60)
print("FEATURE IMPORTANCE ANALYSIS")
print("=" * 60)

feature_importance = pd.DataFrame({
    'Feature': [col.replace('_encoded', '') for col in feature_cols],
    'Coefficient': model_original.coef_
})
feature_importance['Abs_Coefficient'] = abs(feature_importance['Coefficient'])
feature_importance = feature_importance.sort_values('Abs_Coefficient', ascending=False)

print("Feature Importance (Original Model):")
print(feature_importance)

plt.figure(figsize=(12, 8))
plt.barh(feature_importance['Feature'], feature_importance['Coefficient'])
plt.xlabel('Coefficient Value')
plt.title('Feature Importance in Original Model')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("\nPCA Component Loadings:")
for i in range(n_components_fixed):
    print(f"\nPC{i+1} (Explains {explained_variance_ratio[i]*100:.2f}% variance):")
    pc_loadings = pd.DataFrame({
        'Feature': [col.replace('_encoded', '') for col in feature_cols],
        'Loading': pca_reduced.components_[i]
    })
    pc_loadings['Abs_Loading'] = abs(pc_loadings['Loading'])
    pc_loadings = pc_loadings.sort_values('Abs_Loading', ascending=False)
    print(pc_loadings.head(3))