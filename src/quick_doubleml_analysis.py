#!/usr/bin/env python3
"""
Quick Double ML Analysis for 10-Day Timeline

This script performs the core Double ML analysis for the thesis
using the real bond yield and ND-GAIN data with World Bank controls.

Research Question: Does environmental vulnerability (ND-GAIN) causally 
affect 10-year sovereign bond yields?
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Double ML imports
from doubleml import DoubleMLData, DoubleMLPLR
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso
from sklearn.model_selection import cross_val_score

def load_and_prepare_data():
    """Load and prepare data for Double ML analysis"""
    print("📊 Loading merged panel data...")
    
    # Load the merged dataset
    data = pd.read_csv('data/merged_panel.csv')
    data['date'] = pd.to_datetime(data['date'])
    
    print(f"Original data shape: {data.shape}")
    print(f"Countries: {data['iso3c'].nunique()}")
    print(f"Date range: {data['date'].min()} to {data['date'].max()}")
    
    # Define variables for Double ML
    y_col = 'bond_yield'          # Outcome: 10-year sovereign bond yield
    d_col = 'nd_gain'             # Treatment: ND-GAIN vulnerability score
    
    # Control variables (only use available real data)
    available_controls = []
    potential_controls = ['gdp_growth', 'inflation', 'unemployment', 'public_debt']
    
    for col in potential_controls:
        if col in data.columns:
            available_controls.append(col)
    
    print(f"Available control variables: {available_controls}")
    
    # Remove rows with missing key variables
    key_vars = [y_col, d_col] + available_controls
    data_clean = data.dropna(subset=key_vars)
    
    print(f"After removing missing values: {data_clean.shape}")
    print(f"Data loss: {((len(data) - len(data_clean)) / len(data) * 100):.1f}%")
    
    return data_clean, y_col, d_col, available_controls

def run_doubleml_analysis(data, y_col, d_col, x_cols):
    """Run the main Double ML analysis"""
    print("\n🔬 Running Double ML Analysis...")
    
    # Create DoubleMLData object
    print("Creating DoubleMLData object...")
    dml_data = DoubleMLData(data, y_col=y_col, d_cols=d_col, x_cols=x_cols)
    
    print(f"DML Data summary:")
    print(f"  Outcome (Y): {y_col}")
    print(f"  Treatment (D): {d_col}")
    print(f"  Controls (X): {x_cols}")
    print(f"  Observations: {dml_data.n_obs}")
    
    # Specify machine learning models for nuisance parameters
    print("\nSpecifying ML models...")
    
    # Random Forest for both outcome and treatment models
    ml_g = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
    ml_m = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
    
    # Initialize Double ML PLR (Partially Linear Regression) model
    print("Initializing Double ML PLR model...")
    dml_plr = DoubleMLPLR(dml_data, ml_g=ml_g, ml_m=ml_m, n_folds=5, score='partialling out')
    
    # Fit the model
    print("Fitting Double ML model...")
    dml_plr.fit()
    
    # Display results
    print("\n" + "="*60)
    print("🎯 DOUBLE ML RESULTS")
    print("="*60)
    
    print("\nTreatment Effect Estimates:")
    print(dml_plr.summary)
    
    # Extract key results
    coef = dml_plr.coef[0]
    se = dml_plr.se[0]
    pval = dml_plr.pval[0]
    ci_lower = dml_plr.confint().iloc[0, 0]
    ci_upper = dml_plr.confint().iloc[0, 1]
    
    print(f"\n📈 KEY FINDINGS:")
    print(f"  Average Treatment Effect: {coef:.4f}")
    print(f"  Standard Error: {se:.4f}")
    print(f"  P-value: {pval:.4f}")
    print(f"  95% Confidence Interval: [{ci_lower:.4f}, {ci_upper:.4f}]")
    
    # Interpretation
    if pval < 0.05:
        significance = "statistically significant"
    else:
        significance = "not statistically significant"
    
    print(f"\n💡 INTERPRETATION:")
    print(f"  A 1-unit increase in ND-GAIN vulnerability score is associated with")
    print(f"  a {coef:.4f} percentage point change in bond yields.")
    print(f"  This effect is {significance} at the 5% level.")
    
    return dml_plr, coef, se, pval, ci_lower, ci_upper

def create_visualizations(data, results, y_col, d_col):
    """Create key visualizations"""
    print("\n📊 Creating visualizations...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Double ML Analysis Results', fontsize=16, fontweight='bold')
    
    # Plot 1: Treatment vs Outcome scatter
    axes[0, 0].scatter(data[d_col], data[y_col], alpha=0.5, s=1)
    axes[0, 0].set_xlabel('ND-GAIN Vulnerability Score')
    axes[0, 0].set_ylabel('Bond Yield (%)')
    axes[0, 0].set_title('Bond Yield vs ND-GAIN Score')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Add trend line
    z = np.polyfit(data[d_col].dropna(), data[y_col].dropna(), 1)
    p = np.poly1d(z)
    axes[0, 0].plot(data[d_col], p(data[d_col]), "r--", alpha=0.8, linewidth=2)
    
    # Plot 2: Treatment effect with confidence interval
    coef, se, _, ci_lower, ci_upper = results[1:6]
    axes[0, 1].bar(['Treatment Effect'], [coef], yerr=[se], capsize=10, 
                   color='skyblue', edgecolor='navy', alpha=0.7)
    axes[0, 1].errorbar(['Treatment Effect'], [coef], yerr=[[coef-ci_lower], [ci_upper-coef]], 
                       fmt='none', capsize=15, color='red', linewidth=2)
    axes[0, 1].set_ylabel('Effect Size')
    axes[0, 1].set_title('Treatment Effect Estimate')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Residuals analysis
    dml_plr = results[0]
    residuals = data[y_col] - dml_plr.predictions['ml_g'].flatten()
    axes[1, 0].scatter(dml_plr.predictions['ml_g'], residuals, alpha=0.5, s=1)
    axes[1, 0].axhline(y=0, color='red', linestyle='--')
    axes[1, 0].set_xlabel('Predicted Values')
    axes[1, 0].set_ylabel('Residuals')
    axes[1, 0].set_title('Residuals vs Fitted')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 4: Distribution of treatment variable
    axes[1, 1].hist(data[d_col], bins=50, alpha=0.7, edgecolor='black')
    axes[1, 1].axvline(data[d_col].mean(), color='red', linestyle='--', 
                      label=f'Mean: {data[d_col].mean():.3f}')
    axes[1, 1].set_xlabel('ND-GAIN Score')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].set_title('Distribution of ND-GAIN Scores')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('outputs/figures/doubleml_results.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Visualizations saved to outputs/figures/doubleml_results.png")

def save_results(results, data, y_col, d_col, x_cols):
    """Save results to files"""
    print("\n💾 Saving results...")
    
    dml_plr, coef, se, pval, ci_lower, ci_upper = results
    
    # Create results summary
    results_summary = {
        'Analysis': 'Double Machine Learning (PLR)',
        'Outcome_Variable': y_col,
        'Treatment_Variable': d_col,
        'Control_Variables': ', '.join(x_cols),
        'Sample_Size': len(data),
        'Treatment_Effect': coef,
        'Standard_Error': se,
        'P_Value': pval,
        'CI_Lower': ci_lower,
        'CI_Upper': ci_upper,
        'Significant_5pct': pval < 0.05,
        'Significant_1pct': pval < 0.01
    }
    
    # Save to CSV
    results_df = pd.DataFrame([results_summary])
    results_df.to_csv('outputs/tables/doubleml_results.csv', index=False)
    
    # Save detailed summary
    with open('outputs/results/doubleml_analysis_report.txt', 'w') as f:
        f.write("DOUBLE MACHINE LEARNING ANALYSIS REPORT\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("RESEARCH QUESTION:\n")
        f.write("Does environmental vulnerability (ND-GAIN) causally affect 10-year sovereign bond yields?\n\n")
        
        f.write("METHODOLOGY:\n")
        f.write("- Double Machine Learning (Partially Linear Regression)\n")
        f.write("- Random Forest for nuisance parameter estimation\n")
        f.write("- 5-fold cross-validation\n\n")
        
        f.write("DATA:\n")
        f.write(f"- Sample size: {len(data):,} observations\n")
        f.write(f"- Countries: {data['iso3c'].nunique()}\n")
        f.write(f"- Time period: {data['date'].min()} to {data['date'].max()}\n\n")
        
        f.write("VARIABLES:\n")
        f.write(f"- Outcome (Y): {y_col}\n")
        f.write(f"- Treatment (D): {d_col}\n")
        f.write(f"- Controls (X): {', '.join(x_cols)}\n\n")
        
        f.write("RESULTS:\n")
        f.write(f"- Average Treatment Effect: {coef:.4f}\n")
        f.write(f"- Standard Error: {se:.4f}\n")
        f.write(f"- P-value: {pval:.4f}\n")
        f.write(f"- 95% Confidence Interval: [{ci_lower:.4f}, {ci_upper:.4f}]\n\n")
        
        f.write("INTERPRETATION:\n")
        f.write(f"A 1-unit increase in ND-GAIN vulnerability score is associated with\n")
        f.write(f"a {coef:.4f} percentage point change in bond yields.\n")
        if pval < 0.05:
            f.write("This effect is statistically significant at the 5% level.\n")
        else:
            f.write("This effect is not statistically significant at the 5% level.\n")
    
    print("✅ Results saved:")
    print("  - outputs/tables/doubleml_results.csv")
    print("  - outputs/results/doubleml_analysis_report.txt")

def main():
    """Main analysis function"""
    print("🚀 Starting Quick Double ML Analysis for Thesis")
    print("=" * 60)
    
    # Step 1: Load and prepare data
    data, y_col, d_col, x_cols = load_and_prepare_data()
    
    # Step 2: Run Double ML analysis
    results = run_doubleml_analysis(data, y_col, d_col, x_cols)
    
    # Step 3: Create visualizations
    create_visualizations(data, results, y_col, d_col)
    
    # Step 4: Save results
    save_results(results, data, y_col, d_col, x_cols)
    
    print("\n" + "="*60)
    print("✅ QUICK DOUBLE ML ANALYSIS COMPLETED!")
    print("="*60)
    
    print("\n📁 Generated outputs:")
    print("  - outputs/figures/doubleml_results.png")
    print("  - outputs/tables/doubleml_results.csv")
    print("  - outputs/results/doubleml_analysis_report.txt")
    
    print("\n📈 Next steps for 10-day timeline:")
    print("  1. Review results and interpretation")
    print("  2. Run robustness checks with alternative models")
    print("  3. Perform regional/subgroup analysis")
    print("  4. Write thesis sections with findings")

if __name__ == "__main__":
    main()