import pandas as pd
import numpy as np

def create_readable_missing_table():
    """
    Create a more readable missing data table by country
    """
    # Load the missing data by country
    missing_by_country = pd.read_csv("data/processed/missing_data_by_country.csv")
    
    # Get variable names (excluding metadata columns)
    metadata_cols = ['Country', 'Total_Observations', 'overall_completeness']
    variable_cols = [col for col in missing_by_country.columns if col not in metadata_cols]
    
    # Extract variable names (remove _missing_pct suffix)
    variables = [col.replace('_missing_pct', '') for col in variable_cols if col.endswith('_missing_pct')]
    
    # Create a clean table with just the missing percentages
    clean_table = missing_by_country[['Country', 'Total_Observations', 'overall_completeness']].copy()
    
    for var in variables:
        col_name = f'{var}_missing_pct'
        if col_name in missing_by_country.columns:
            clean_table[var] = missing_by_country[col_name]
    
    # Sort by overall completeness (descending)
    clean_table = clean_table.sort_values('overall_completeness', ascending=False)
    
    # Round all numeric columns to 1 decimal place
    numeric_cols = clean_table.select_dtypes(include=[np.number]).columns
    clean_table[numeric_cols] = clean_table[numeric_cols].round(1)
    
    # Save the clean table
    clean_table.to_csv("data/processed/missing_data_table_clean.csv", index=False)
    
    # Create a summary table showing top and bottom countries
    print("="*100)
    print("MISSING DATA ANALYSIS BY COUNTRY - CLEAN TABLE")
    print("="*100)
    print(f"Total countries: {len(clean_table)}")
    print(f"Total variables: {len(variables)}")
    print()
    
    print("TOP 15 COUNTRIES BY DATA COMPLETENESS:")
    print("-" * 100)
    top_15 = clean_table.head(15)
    print(top_15.to_string(index=False, float_format='%.1f'))
    print()
    
    print("BOTTOM 15 COUNTRIES BY DATA COMPLETENESS:")
    print("-" * 100)
    bottom_15 = clean_table.tail(15)
    print(bottom_15.to_string(index=False, float_format='%.1f'))
    print()
    
    # Create a summary by variable
    print("VARIABLE COMPLETENESS SUMMARY:")
    print("-" * 100)
    var_summary = []
    
    for var in variables:
        missing_pct = clean_table[var].mean()
        complete_pct = 100 - missing_pct
        var_summary.append({
            'Variable': var,
            'Avg_Missing_Pct': round(missing_pct, 1),
            'Avg_Complete_Pct': round(complete_pct, 1)
        })
    
    var_summary_df = pd.DataFrame(var_summary)
    var_summary_df = var_summary_df.sort_values('Avg_Complete_Pct', ascending=False)
    print(var_summary_df.to_string(index=False, float_format='%.1f'))
    
    # Save variable summary
    var_summary_df.to_csv("data/processed/variable_completeness_summary.csv", index=False)
    
    # Create a heatmap-style table for better visualization
    print("\n" + "="*100)
    print("MISSING DATA HEATMAP (Top 20 Countries)")
    print("="*100)
    
    # Select top 20 countries
    top_20 = clean_table.head(20)
    
    # Create a heatmap table
    heatmap_data = top_20[['Country'] + variables].copy()
    
    # Convert to percentage format for display
    for var in variables:
        heatmap_data[var] = heatmap_data[var].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
    
    print(heatmap_data.to_string(index=False))
    
    # Save heatmap data
    heatmap_data.to_csv("data/processed/missing_data_heatmap_top20.csv", index=False)
    
    print(f"\nFiles saved:")
    print(f"  - data/processed/missing_data_table_clean.csv")
    print(f"  - data/processed/variable_completeness_summary.csv")
    print(f"  - data/processed/missing_data_heatmap_top20.csv")
    
    return clean_table, var_summary_df

def analyze_country_coverage():
    """
    Analyze which countries have the best coverage for different variable combinations
    """
    print("\n" + "="*100)
    print("COUNTRY COVERAGE ANALYSIS FOR KEY VARIABLES")
    print("="*100)
    
    # Load the clean missing data table
    clean_table = pd.read_csv("data/processed/missing_data_table_clean.csv")
    
    # Define key variable groups
    key_variables = {
        'Macroeconomic': ['gdp_annual_growth_rate', 'cpi_yoy', 'debt_to_gdp'],
        'Financial': ['sovereign_yield', 'sovereign_spread', 'deficit_to_gdp'],
        'Governance': ['wgi_cc', 'wgi_ge', 'wgi_pv', 'wgi_rl', 'wgi_rq', 'wgi_va'],
        'External': ['current_account_balance', 'NEER', 'vulnerability']
    }
    
    for group_name, variables in key_variables.items():
        print(f"\n{group_name.upper()} VARIABLES:")
        print("-" * 50)
        
        # Calculate completeness for this group
        group_cols = [var for var in variables if var in clean_table.columns]
        if group_cols:
            clean_table[f'{group_name}_completeness'] = 100 - clean_table[group_cols].mean(axis=1)
            
            # Show top 10 countries for this group
            top_group = clean_table.nlargest(10, f'{group_name}_completeness')[['Country', f'{group_name}_completeness']]
            print(f"Top 10 countries by {group_name} completeness:")
            print(top_group.round(1).to_string(index=False))
        else:
            print("No variables found for this group")
    
    # Save the enhanced table
    clean_table.to_csv("data/processed/missing_data_table_enhanced.csv", index=False)
    print(f"\nEnhanced table saved to: data/processed/missing_data_table_enhanced.csv")

if __name__ == "__main__":
    # Create the clean missing data table
    clean_table, var_summary = create_readable_missing_table()
    
    # Analyze country coverage by variable groups
    analyze_country_coverage()
