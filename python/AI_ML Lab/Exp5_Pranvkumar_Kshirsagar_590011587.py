# # Data visualization graphs in Python

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("car_data.csv")

# -------------------- BOX PLOTS --------------------
# Set a refined style and a blue color palette
sns.set_style("whitegrid")
sns.set_palette("Blues_r")

# Create a 2x3 subplot grid
fig, axes = plt.subplots(2, 3, figsize=(20, 12))
fig.suptitle('Distribution Analysis using Box Plots', fontsize=20, fontweight='bold')
axes = axes.flatten()

# 1. Box Plot - Selling Price by Year
# BOX PLOT
sns.boxplot(x="Year", y="Selling_Price", data=df, ax=axes[0])
axes[0].set_title("Selling Price Distribution by Year", fontsize=12)
years = sorted(df['Year'].unique())
axes[0].set_xticks(range(0, len(years), 2))
axes[0].set_xticklabels(years[::2])
axes[0].set_xlabel("Year", fontsize=10)
axes[0].set_ylabel("Selling Price", fontsize=10)

# 2. Box Plot - Selling Price by Fuel Type
# BOX PLOT
sns.boxplot(x="Fuel_Type", y="Selling_Price", data=df, ax=axes[1])
axes[1].set_title("Selling Price Distribution by Fuel Type", fontsize=12)
axes[1].set_xlabel("Fuel Type", fontsize=10)
axes[1].set_ylabel("Selling Price", fontsize=10)

# 3. Box Plot - Selling Price by Seller Type
# BOX PLOT
sns.boxplot(x="Seller_Type", y="Selling_Price", data=df, ax=axes[2])
axes[2].set_title("Selling Price Distribution by Seller Type", fontsize=12)
axes[2].set_xlabel("Seller Type", fontsize=10)
axes[2].set_ylabel("Selling Price", fontsize=10)

# 4. Box Plot - Selling Price by Transmission
# BOX PLOT
sns.boxplot(x="Transmission", y="Selling_Price", data=df, ax=axes[3])
axes[3].set_title("Selling Price Distribution by Transmission", fontsize=12)
axes[3].set_xlabel("Transmission", fontsize=10)
axes[3].set_ylabel("Selling Price", fontsize=10)

# 5. Box Plot - Present Price by Fuel Type
# BOX PLOT
sns.boxplot(x="Fuel_Type", y="Present_Price", data=df, ax=axes[4])
axes[4].set_title("Present Price Distribution by Fuel Type", fontsize=12)
axes[4].set_xlabel("Fuel Type", fontsize=10)
axes[4].set_ylabel("Present Price", fontsize=10)

# 6. Box Plot - Kms Driven by Fuel Type
# BOX PLOT
sns.boxplot(x="Fuel_Type", y="Kms_Driven", data=df, ax=axes[5])
axes[5].set_title("Kms Driven Distribution by Fuel Type", fontsize=12)
axes[5].set_xlabel("Fuel Type", fontsize=10)
axes[5].set_ylabel("Kms Driven", fontsize=10)

# Remove top and right spines for a cleaner look
for ax in axes:
    sns.despine(ax=ax)

# Adjust layout and display the plots
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

# -------------------- LINE PLOTS --------------------
# Set a refined style
sns.set_style("whitegrid")
sns.set_palette("Greens_r") # Use a reversed green palette

# Create a 2x3 subplot grid
fig, axes = plt.subplots(2, 3, figsize=(20, 12))
fig.suptitle('Trend Analysis of Car Data', fontsize=20, fontweight='bold')
axes = axes.flatten()

# 1. Line Plot - Selling Price by Year
# LINE PLOT
sns.lineplot(x="Year", y="Selling_Price", data=df, ax=axes[0], marker='o', color='darkgreen')
axes[0].set_title("Average Selling Price Trend by Year", fontsize=12)
years = sorted(df['Year'].unique())
axes[0].set_xticks(years[::2])
axes[0].set_xticklabels(years[::2])
axes[0].set_xlabel("Year", fontsize=10)
axes[0].set_ylabel("Selling Price", fontsize=10)

# 2. Line Plot - Selling Price by Fuel Type
# LINE PLOT
sns.lineplot(x="Fuel_Type", y="Selling_Price", data=df, ax=axes[1], marker='o', color='seagreen')
axes[1].set_title("Average Selling Price by Fuel Type", fontsize=12)
axes[1].set_xlabel("Fuel Type", fontsize=10)
axes[1].set_ylabel("Selling Price", fontsize=10)

# 3. Line Plot - Selling Price by Seller Type
# LINE PLOT
sns.lineplot(x="Seller_Type", y="Selling_Price", data=df, ax=axes[2], marker='o', color='mediumseagreen')
axes[2].set_title("Average Selling Price by Seller Type", fontsize=12)
axes[2].set_xlabel("Seller Type", fontsize=10)
axes[2].set_ylabel("Selling Price", fontsize=10)

# 4. Line Plot - Selling Price by Transmission
# LINE PLOT
sns.lineplot(x="Transmission", y="Selling_Price", data=df, ax=axes[3], marker='o', color='darkolivegreen')
axes[3].set_title("Average Selling Price by Transmission", fontsize=12)
axes[3].set_xlabel("Transmission", fontsize=10)
axes[3].set_ylabel("Selling Price", fontsize=10)

# 5. Line Plot - Present Price by Fuel Type
# LINE PLOT
sns.lineplot(x="Fuel_Type", y="Present_Price", data=df, ax=axes[4], marker='o', color='forestgreen')
axes[4].set_title("Average Present Price by Fuel Type", fontsize=12)
axes[4].set_xlabel("Fuel Type", fontsize=10)
axes[4].set_ylabel("Present Price", fontsize=10)

# 6. Line Plot - Kms Driven by Fuel Type
# LINE PLOT
sns.lineplot(x="Fuel_Type", y="Kms_Driven", data=df, ax=axes[5], marker='o', color='limegreen')
axes[5].set_title("Average Kms Driven by Fuel Type", fontsize=12)
axes[5].set_xlabel("Fuel Type", fontsize=10)
axes[5].set_ylabel("Kms Driven", fontsize=10)

# Remove top and right spines for a cleaner look
for ax in axes:
    sns.despine(ax=ax)

# Adjust layout and display the plots
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

# -------------------- BAR PLOTS --------------------
# Set style
sns.set(style="whitegrid")

# Create a 2x3 subplot grid
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.flatten()

# 1. Bar Plot - Selling Price by Year
# BAR PLOT
sns.barplot(x="Year", y="Selling_Price", data=df, ax=axes[0], errorbar=None, palette="hot")
axes[0].set_title("Selling Price by Year")
# Rotate x-axis labels for better readability
axes[0].tick_params(axis='x', rotation=45)

# 2. Bar Plot - Selling Price by Fuel Type
# BAR PLOT
sns.barplot(x="Fuel_Type", y="Selling_Price", data=df, ax=axes[1], errorbar=None, palette="hot")
axes[1].set_title("Selling Price by Fuel Type")

# 3. Bar Plot - Selling Price by Seller Type
# BAR PLOT
sns.barplot(x="Seller_Type", y="Selling_Price", data=df, ax=axes[2], errorbar=None, palette="hot")
axes[2].set_title("Selling Price by Seller Type")

# 4. Bar Plot - Selling Price by Transmission
# BAR PLOT
sns.barplot(x="Transmission", y="Selling_Price", data=df, ax=axes[3], errorbar=None, palette="hot")
axes[3].set_title("Selling Price by Transmission")

# 5. Bar Plot - Present Price by Fuel Type
# BAR PLOT
sns.barplot(x="Fuel_Type", y="Present_Price", data=df, ax=axes[4], errorbar=None, palette="hot")
axes[4].set_title("Present Price by Fuel Type")

# 6. Bar Plot - Kms Driven by Fuel Type
# BAR PLOT
sns.barplot(x="Fuel_Type", y="Kms_Driven", data=df, ax=axes[5], errorbar=None, palette="hot")
axes[5].set_title("Kms Driven by Fuel Type")

# Adjust layout
plt.tight_layout()
plt.show()

# -------------------- PIE CHARTS --------------------
# Set a refined style for pie charts
sns.set_palette("viridis")
plt.style.use('seaborn-v0_8-whitegrid')

# Create a 2x2 subplot grid for better visualization of pie charts
fig, axes = plt.subplots(2, 2, figsize=(14, 14))
fig.suptitle('Distribution Analysis of Car Features', fontsize=20, fontweight='bold')
axes = axes.flatten()

# 1. Pie Chart - Fuel Type Distribution
# PIE CHART
fuel_counts = df["Fuel_Type"].value_counts()
axes[0].pie(fuel_counts, labels=fuel_counts.index, autopct="%1.1f%%", startangle=90, wedgeprops=dict(width=0.3))
axes[0].set_title("Fuel Type Distribution", fontsize=14)
axes[0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# 2. Pie Chart - Seller Type Distribution
# PIE CHART
seller_counts = df["Seller_Type"].value_counts()
axes[1].pie(seller_counts, labels=seller_counts.index, autopct="%1.1f%%", startangle=90, wedgeprops=dict(width=0.3))
axes[1].set_title("Seller Type Distribution", fontsize=14)
axes[1].axis('equal')

# 3. Pie Chart - Transmission Type Distribution
# PIE CHART
transmission_counts = df["Transmission"].value_counts()
axes[2].pie(transmission_counts, labels=transmission_counts.index, autopct="%1.1f%%", startangle=90, wedgeprops=dict(width=0.3))
axes[2].set_title("Transmission Type Distribution", fontsize=14)
axes[2].axis('equal')

# 4. Pie Chart - Total Selling Price by Fuel Type
# PIE CHART
price_by_fuel = df.groupby("Fuel_Type")["Selling_Price"].sum()
axes[3].pie(price_by_fuel, labels=price_by_fuel.index, autopct="%1.1f%%", startangle=90, wedgeprops=dict(width=0.3))
axes[3].set_title("Proportion of Total Selling Price by Fuel Type", fontsize=14)
axes[3].axis('equal')

# Adjust layout and display the plots
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()

# -------------------- SCATTER PLOTS --------------------
# Set a refined style and cold color palette for scatter plots
sns.set_style("whitegrid")
sns.set_palette("cool")

# Create a 2x3 subplot grid for scatter plots
fig, axes = plt.subplots(2, 3, figsize=(20, 12))
fig.suptitle('Scatter Plot Analysis (Cold Theme)', fontsize=20, fontweight='bold')
axes = axes.flatten()

# 1. Scatter Plot - Present Price vs Selling Price
# SCATTER PLOT
sns.scatterplot(x="Present_Price", y="Selling_Price", hue="Fuel_Type", data=df, ax=axes[0], s=70, palette="cool")
axes[0].set_title("Present Price vs Selling Price", fontsize=12)
axes[0].set_xlabel("Present Price", fontsize=10)
axes[0].set_ylabel("Selling Price", fontsize=10)

# 2. Scatter Plot - Kms Driven vs Selling Price
# SCATTER PLOT
sns.scatterplot(x="Kms_Driven", y="Selling_Price", hue="Fuel_Type", data=df, ax=axes[1], s=70, palette="cool")
axes[1].set_title("Kms Driven vs Selling Price", fontsize=12)
axes[1].set_xlabel("Kms Driven", fontsize=10)
axes[1].set_ylabel("Selling Price", fontsize=10)

# 3. Scatter Plot - Year vs Selling Price
# SCATTER PLOT
sns.scatterplot(x="Year", y="Selling_Price", hue="Fuel_Type", data=df, ax=axes[2], s=70, palette="cool")
axes[2].set_title("Year vs Selling Price", fontsize=12)
axes[2].set_xlabel("Year", fontsize=10)
axes[2].set_ylabel("Selling Price", fontsize=10)

# 4. Scatter Plot - Present Price vs Kms Driven
# SCATTER PLOT
sns.scatterplot(x="Present_Price", y="Kms_Driven", hue="Fuel_Type", data=df, ax=axes[3], s=70, palette="cool")
axes[3].set_title("Present Price vs Kms Driven", fontsize=12)
axes[3].set_xlabel("Present Price", fontsize=10)
axes[3].set_ylabel("Kms Driven", fontsize=10)

# 5. Scatter Plot - Selling Price vs Transmission
# SCATTER PLOT
sns.scatterplot(x="Transmission", y="Selling_Price", hue="Fuel_Type", data=df, ax=axes[4], s=70, palette="cool")
axes[4].set_title("Selling Price vs Transmission", fontsize=12)
axes[4].set_xlabel("Transmission", fontsize=10)
axes[4].set_ylabel("Selling Price", fontsize=10)

# 6. Scatter Plot - Selling Price vs Seller Type
# SCATTER PLOT
sns.scatterplot(x="Seller_Type", y="Selling_Price", hue="Fuel_Type", data=df, ax=axes[5], s=70, palette="cool")
axes[5].set_title("Selling Price vs Seller Type", fontsize=12)
axes[5].set_xlabel("Seller Type", fontsize=10)
axes[5].set_ylabel("Selling Price", fontsize=10)

# Remove top and right spines for a cleaner look
for ax in axes:
    sns.despine(ax=ax)

# Adjust layout and display the plots
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

# -------------------- HEATMAP --------------------
sns.set_style("whitegrid")
sns.set_palette("Purples_r")

# HEATMAP
plt.figure(figsize=(10, 8))
corr = df.corr(numeric_only=True)
sns.heatmap(corr, annot=True, cmap="Purples", fmt=".2f", linewidths=0.5, cbar_kws={"shrink": 0.8})
plt.title("Correlation Heatmap (Violet Palette)", fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()