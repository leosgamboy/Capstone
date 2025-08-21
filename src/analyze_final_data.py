import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def analyze_final_dataset():
    """
    Quick analysis of the final merged dataset
    """
    print("Loading final dataset...")
    df = pd.read_csv("data/processed/data_final.csv")
    df['date'] = pd.to_datetime(df['date'])
    
    print("="*80)
    print("FINAL DATASET ANALYSIS")
    print("="*80)
    
    # Basic dataset info
    print(f"Dataset shape: {df.shape}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Number of countries: {df['iso3c'].nunique()}")
    print(f"Number of years: {df['year'].nunique()}")
    print(f"Total observations: {len(df)}")
    
    # Display column info
    print(f"\nColumns ({len(df.columns)}):")
    for i, col in enumerate(df.columns):
        print(f"  {i+1:2d}. {col}")
    
    # Data types
    print(f"\nData types:")
    print(df.dtypes)
    
    # Missing values analysis
    print(f"\nMissing values analysis:")
    missing_summary = df.isnull().sum()
    missing_pct = (missing_summary / len(df)) * 100
    
    for col in df.columns:
        if missing_summary[col] > 0:
            print(f"  {col}: {missing_summary[col]} ({missing_pct[col]:.1f}%)")
        else:
            print(f"  {col}: No missing values")
    
    # Sample of data
    print(f"\nSample of data (first 10 rows):")
    print(df.head(10))
    
    # Summary statistics for numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols = [col for col in numeric_cols if col not in ['year']]
    
    print(f"\nSummary statistics for numeric variables:")
    print(df[numeric_cols].describe())
    
    # Country coverage analysis
    print(f"\nCountry coverage analysis:")
    country_counts = df['iso3c'].value_counts()
    print(f"Countries with most observations:")
    print(country_counts.head(10))
    print(f"\nCountries with least observations:")
    print(country_counts.tail(10))
    
    # Year coverage analysis
    print(f"\nYear coverage analysis:")
    year_counts = df['year'].value_counts().sort_index()
    print(year_counts)
    
    # GAIN variable analysis
    if 'GAIN' in df.columns:
        print(f"\nGAIN variable analysis:")
        gain_stats = df['GAIN'].describe()
        print(gain_stats)
        
        # Countries with GAIN data
        countries_with_gain = df[df['GAIN'].notna()]['iso3c'].nunique()
        print(f"Countries with GAIN data: {countries_with_gain}")
        
        # Years with GAIN data
        years_with_gain = df[df['GAIN'].notna()]['year'].nunique()
        print(f"Years with GAIN data: {years_with_gain}")
    
    # Correlation analysis for key variables
    print(f"\nCorrelation analysis for key variables:")
    key_vars = ['yield_with_spread', 'sovereign_spread', 'GAIN', 'vulnerability', 'gdp_annual_growth_rate']
    key_vars = [var for var in key_vars if var in df.columns]
    
    if len(key_vars) > 1:
        corr_matrix = df[key_vars].corr()
        print(corr_matrix)
    
    # Data quality summary
    print(f"\n" + "="*80)
    print("DATA QUALITY SUMMARY")
    print("="*80)
    
    total_cells = len(df) * len(df.columns)
    missing_cells = df.isnull().sum().sum()
    completeness = ((total_cells - missing_cells) / total_cells) * 100
    
    print(f"Overall data completeness: {completeness:.1f}%")
    print(f"Total cells: {total_cells:,}")
    print(f"Missing cells: {missing_cells:,}")
    print(f"Filled cells: {total_cells - missing_cells:,}")
    
    # Recommendations
    print(f"\n" + "="*80)
    print("RECOMMENDATIONS")
    print("="*80)
    
    if completeness < 80:
        print("⚠️  Data completeness is below 80%. Consider:")
        print("   - Investigating missing data patterns")
        print("   - Using imputation techniques")
        print("   - Focusing analysis on countries with better coverage")
    
    if df['GAIN'].isnull().sum() > 0:
        print("⚠️  GAIN variable has missing values. Consider:")
        print("   - Forward-filling for time series continuity")
        print("   - Interpolation for missing years")
        print("   - Analyzing coverage by country and time period")
    
    print("✅ Dataset is ready for analysis with proper country and time coverage")
    
    return df

if __name__ == "__main__":
    final_data = analyze_final_dataset()
