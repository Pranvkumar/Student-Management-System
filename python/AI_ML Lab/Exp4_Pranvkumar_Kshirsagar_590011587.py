import pandas as pd
import sys
import io

try:
    df = pd.read_csv("car_data.csv")
except FileNotFoundError:
    print("Error: 'car_data.csv' not found. Please ensure the file is in the correct directory.", file=sys.stderr)
    sys.exit(1)

output = io.StringIO()

print("First 5 rows of the dataset:", file=output)
print(df.head(), file=output)

print("\nStatistical summary of the dataset:", file=output)
print(df.describe(), file=output)

print("\nNumber of missing values in each column:", file=output)
number_of_missing = df.isnull().sum()
print(number_of_missing, file=output)

print("\nConcise summary of the DataFrame:", file=output)
df.info(buf=output)

print("\nNumber of unique values in each column:", file=output)
print(df.nunique(), file=output)

# Show output in console
print(output.getvalue())

# Export output to file
with open('car_data.txt', 'w') as f:
    f.write(output.getvalue())

print("Analysis has been written to car_data.txt")