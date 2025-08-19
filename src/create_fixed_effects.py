import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def create_fixed_effects_and_lags():
    """
    Load baseline dataset and create country/time fixed effects and lagged variables
    """
    print("Loading baseline dataset...")
    df_data = pd.read_csv("data/processed/data_baseline_cleaned.csv")
    
    # Convert date to datetime
    df_data['date'] = pd.to_datetime(df_data['date'])
    
    print(f"Dataset loaded: {df_data.shape}")
    print(f"Date range: {df_data['date'].min()} to {df_data['date'].max()}")
    print(f"Countries: {df_data['iso3c'].nunique()}")
    print(f"Variables: {len(df_data.columns)}")
    
    # Display first few rows
    print("\nFirst few rows:")
    print(df_data.head())
    
    # Create country fixed effects (dummy variables for each country)
    print("\nCreating country fixed effects...")
    country_dummies = pd.get_dummies(df_data['iso3c'], prefix='country')
    print(f"Created {len(country_dummies.columns)} country dummies")
    
    # Create time fixed effects (dummy variables for each year-month)
    print("Creating time fixed effects...")
    df_data['year_month'] = df_data['date'].dt.to_period('M')
    time_dummies = pd.get_dummies(df_data['year_month'], prefix='time')
    print(f"Created {len(time_dummies.columns)} time dummies")
    
    # Add fixed effects to the main dataset
    df_data = pd.concat([df_data, country_dummies, time_dummies], axis=1)
    
    print(f"Dataset shape after adding fixed effects: {df_data.shape}")
    print(f"Total variables now: {len(df_data.columns)}")
    
    # Display sample of fixed effects
    print("\nSample country dummies:")
    print(country_dummies.iloc[:5, :10].head())
    
    print("\nSample time dummies:")
    print(time_dummies.iloc[:5, :10].head())
    
    # Sort data by country and date for proper lagging
    print("\nCreating lagged sovereign spread variable...")
    df_data = df_data.sort_values(['iso3c', 'date'])
    
    # Create lagged sovereign spread (y(t-1))
    df_data['sovereign_spread_lag1'] = df_data.groupby('iso3c')['sovereign_spread'].shift(1)
    
    # Create additional lags if needed
    df_data['sovereign_spread_lag2'] = df_data.groupby('iso3c')['sovereign_spread'].shift(2)
    
    # Check lag creation
    print(f"Dataset shape after adding lags: {df_data.shape}")
    print(f"Variables including lags: {len(df_data.columns)}")
    
    # Display sample of lagged variables
    print("\nSample of lagged sovereign spread variables:")
    lag_sample = df_data[['date', 'iso3c', 'sovereign_spread', 'sovereign_spread_lag1', 'sovereign_spread_lag2']].head(10)
    print(lag_sample)
    
    # Check for missing values in lagged variables
    print(f"\nMissing values in sovereign_spread: {df_data['sovereign_spread'].isna().sum()}")
    print(f"Missing values in sovereign_spread_lag1: {df_data['sovereign_spread_lag1'].isna().sum()}")
    print(f"Missing values in sovereign_spread_lag2: {df_data['sovereign_spread_lag2'].isna().sum()}")
    
    # Summary of the final dataset
    print("\n" + "="*80)
    print("FINAL DATASET SUMMARY")
    print("="*80)
    print(f"Total observations: {len(df_data)}")
    print(f"Total countries: {df_data['iso3c'].nunique()}")
    print(f"Total variables: {len(df_data.columns)}")
    print(f"Date range: {df_data['date'].min()} to {df_data['date'].max()}")
    
    # List all variables
    print(f"\nAll variables in the dataset:")
    for i, col in enumerate(df_data.columns):
        print(f"{i+1:3d}. {col}")
    
    # Check data types
    print(f"\nData types:")
    print(df_data.dtypes.value_counts())
    
    # Check for any remaining missing values
    print(f"\nMissing values summary:")
    missing_summary = df_data.isnull().sum()
    missing_summary = missing_summary[missing_summary > 0].sort_values(ascending=False)
    if len(missing_summary) > 0:
        print(missing_summary)
    else:
        print("No missing values in the dataset")
    
    print("\nDataset ready for analysis!")
    
    return df_data

if __name__ == "__main__":
    df_data = create_fixed_effects_and_lags()



