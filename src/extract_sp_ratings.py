import pandas as pd

def extract_sp_ratings():
    """Extract only S&P ratings data from the processed ratings panel"""
    
    # Read the processed ratings data
    print("Reading ratings data...")
    df = pd.read_csv('data/processed/ratings_monthly_panel.csv')
    
    # Select only Date, Country, and S&P rating columns
    sp_columns = ['Date', 'Country', 'Rating_S&P']
    df_sp = df[sp_columns].copy()
    
    # Rename the S&P rating column to just 'Rating' for simplicity
    df_sp = df_sp.rename(columns={'Rating_S&P': 'Rating'})
    
    # Remove rows where S&P rating is missing (NaN)
    df_sp_clean = df_sp.dropna(subset=['Rating'])
    
    # Sort by Date and Country for better organization
    df_sp_clean = df_sp_clean.sort_values(['Date', 'Country'])
    
    # Save to new CSV file
    output_file = 'data/processed/sp_ratings_only.csv'
    df_sp_clean.to_csv(output_file, index=False)
    
    # Print summary statistics
    print(f"\nS&P Ratings Data Summary:")
    print(f"=" * 40)
    print(f"Total observations: {len(df_sp_clean):,}")
    print(f"Countries with S&P ratings: {df_sp_clean['Country'].nunique()}")
    print(f"Date range: {df_sp_clean['Date'].min()} to {df_sp_clean['Date'].max()}")
    print(f"Unique rating values: {df_sp_clean['Rating'].nunique()}")
    print(f"Output file: {output_file}")
    
    # Show sample of the data
    print(f"\nSample of S&P ratings data:")
    print(df_sp_clean.head(10))
    
    # Show rating distribution
    print(f"\nS&P Rating Distribution (Top 10):")
    rating_counts = df_sp_clean['Rating'].value_counts().head(10)
    for rating, count in rating_counts.items():
        print(f"  {rating}: {count:,}")
    
    return df_sp_clean

if __name__ == "__main__":
    extract_sp_ratings() 