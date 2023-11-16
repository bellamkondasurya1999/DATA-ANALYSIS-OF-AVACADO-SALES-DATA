import pandas as pd
import numpy as np

# Load your dataset
csv_file_path = 'Augmented_avocado.csv'  # Replace with your file path
data = pd.read_csv(csv_file_path)

# Fill any null values
data = data.fillna(method='ffill')

# Delete duplicates
data = data.drop_duplicates()

# Convert date to numeric
data['Date'] = pd.to_datetime(data['Date'])
data['Date'] = data['Date'].map(pd.Timestamp.timestamp)

# Handling outliers using Tukey IQR method
def find_outliers_tukey(x):
    q1 = np.percentile(x, 25)
    q3 = np.percentile(x, 75)
    iqr = q3 - q1
    floor = q1 - 1.5 * iqr
    ceiling = q3 + 1.5 * iqr
    outlier_indices = list(x.index[(x < floor) | (x > ceiling)])
    outlier_values = list(x[outlier_indices])
    return outlier_indices, outlier_values

# Apply Tukey IQR method on numeric columns
numeric_columns = ['AveragePrice', 'Total Volume', '4046', '4225', '4770', 'Total Bags', 'Small Bags', 'Large Bags', 'XLarge Bags']
for col in numeric_columns:
    indices, _ = find_outliers_tukey(data[col])
    data = data.drop(index=indices)

# Save the cleaned data
cleaned_data_path = 'path_to_save_cleaned_avocado_dataset.csv'  # Replace with your desired file path
data.to_csv(cleaned_data_path, index=False)
