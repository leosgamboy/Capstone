import pandas as pd
import numpy as np

# Read the original CSV file
df = pd.read_csv('data/external/Data/nd_gain_countryindex_2025/resources/gain/gain.csv')

# Rename ISO3 column to ISO3C
df = df.rename(columns={'ISO3': 'iso3c'})

# Melt the dataframe to convert from wide to long format
# Keep only iso3c as id variable, melt all other columns except Name
id_vars = ['iso3c']
value_vars = [col for col in df.columns if col not in ['iso3c', 'Name']]

# Melt the dataframe
df_long = df.melt(
    id_vars=id_vars,
    value_vars=value_vars,
    var_name='date',
    value_name='gain'
)

# Convert date column to integer (year)
df_long['date'] = df_long['date'].astype(int)

# Sort by iso3c and date
df_long = df_long.sort_values(['iso3c', 'date'])

# Reset index
df_long = df_long.reset_index(drop=True)

# Save the transformed data
output_path = 'data/external/Data/nd_gain_countryindex_2025/resources/gain/gain_long.csv'
df_long.to_csv(output_path, index=False)

print(f"Transformation complete! Output saved to: {output_path}")
print(f"Original shape: {df.shape}")
print(f"New shape: {df_long.shape}")
print("\nFirst few rows of transformed data:")
print(df_long.head(10))
print("\nColumn names:")
print(df_long.columns.tolist())
