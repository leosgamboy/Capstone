import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_rating_agencies():
    """Analyze the coverage and comprehensiveness of each rating agency"""
    
    # Read the processed ratings data
    df = pd.read_csv('data/processed/ratings_monthly_panel.csv')
    
    print("RATING AGENCIES ANALYSIS")
    print("=" * 50)
    
    # 1. Overall coverage by agency
    agencies = ['Fitch', 'S&P', 'DBRS', 'Moody\'s']
    coverage_stats = {}
    
    for agency in agencies:
        rating_col = f'Rating_{agency}'
        outlook_col = f'Outlook_{agency}'
        
        # Count non-null ratings
        total_ratings = df[rating_col].notna().sum()
        total_observations = len(df)
        coverage_pct = (total_ratings / total_observations) * 100
        
        # Count unique countries with ratings
        countries_with_ratings = df[df[rating_col].notna()]['Country'].nunique()
        total_countries = df['Country'].nunique()
        
        # Count unique rating values
        unique_ratings = df[rating_col].dropna().nunique()
        
        coverage_stats[agency] = {
            'total_ratings': total_ratings,
            'coverage_pct': coverage_pct,
            'countries_with_ratings': countries_with_ratings,
            'total_countries': total_countries,
            'unique_ratings': unique_ratings
        }
        
        print(f"\n{agency}:")
        print(f"  - Total ratings: {total_ratings:,}")
        print(f"  - Coverage: {coverage_pct:.1f}%")
        print(f"  - Countries covered: {countries_with_ratings}/{total_countries}")
        print(f"  - Unique rating values: {unique_ratings}")
    
    # 2. Temporal coverage analysis
    print(f"\n\nTEMPORAL COVERAGE ANALYSIS")
    print("=" * 50)
    
    # Convert Date to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    for agency in agencies:
        rating_col = f'Rating_{agency}'
        
        # Find first and last rating dates
        agency_data = df[df[rating_col].notna()]
        if not agency_data.empty:
            first_rating = agency_data['Date'].min()
            last_rating = agency_data['Date'].max()
            date_range = (last_rating - first_rating).days / 365.25
            
            print(f"\n{agency}:")
            print(f"  - First rating: {first_rating.strftime('%Y-%m')}")
            print(f"  - Last rating: {last_rating.strftime('%Y-%m')}")
            print(f"  - Date range: {date_range:.1f} years")
    
    # 3. Geographic coverage analysis
    print(f"\n\nGEOGRAPHIC COVERAGE ANALYSIS")
    print("=" * 50)
    
    for agency in agencies:
        rating_col = f'Rating_{agency}'
        
        # Get countries with ratings
        countries_with_ratings = df[df[rating_col].notna()]['Country'].unique()
        
        print(f"\n{agency} - Countries with ratings ({len(countries_with_ratings)}):")
        print(f"  {', '.join(sorted(countries_with_ratings))}")
    
    # 4. Rating distribution analysis
    print(f"\n\nRATING DISTRIBUTION ANALYSIS")
    print("=" * 50)
    
    for agency in agencies:
        rating_col = f'Rating_{agency}'
        
        # Get rating distribution
        rating_counts = df[rating_col].value_counts().head(10)
        
        print(f"\n{agency} - Top 10 ratings:")
        for rating, count in rating_counts.items():
            print(f"  {rating}: {count:,}")
    
    # 5. Academic research recommendations
    print(f"\n\nACADEMIC RESEARCH RECOMMENDATIONS")
    print("=" * 50)
    
    # Calculate comprehensive scores
    scores = {}
    for agency in agencies:
        stats = coverage_stats[agency]
        
        # Scoring criteria:
        # - Coverage percentage (40% weight)
        # - Number of countries covered (30% weight)
        # - Number of unique ratings (20% weight)
        # - Total number of ratings (10% weight)
        
        coverage_score = stats['coverage_pct'] / 100 * 40
        country_score = (stats['countries_with_ratings'] / stats['total_countries']) * 30
        unique_score = min(stats['unique_ratings'] / 20, 1) * 20  # Normalize to max 20
        total_score = min(stats['total_ratings'] / 10000, 1) * 10  # Normalize to max 10
        
        total_score = coverage_score + country_score + unique_score + total_score
        scores[agency] = total_score
    
    print("\nComprehensive Analysis Scores (higher is better):")
    for agency, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        print(f"  {agency}: {score:.1f}")
    
    # Recommendations
    best_agency = max(scores, key=scores.get)
    print(f"\nRECOMMENDATION: {best_agency} is the most comprehensive for academic research")
    
    # Detailed recommendation
    print(f"\nDetailed Analysis:")
    print(f"1. {best_agency} provides the most comprehensive coverage")
    print(f"2. Consider using {best_agency} as your primary source")
    print(f"3. You may want to supplement with other agencies for robustness checks")
    print(f"4. For cross-validation, consider using multiple agencies in your analysis")
    
    return df, coverage_stats, scores

if __name__ == "__main__":
    analyze_rating_agencies() 