# Matplotlib Import and Plotting Examples Summary

## Overview
Successfully added matplotlib imports and comprehensive plotting examples to the `01_data_cleaning.ipynb` notebook.

## What Was Added

### 1. Import Statements
Added to both import sections in the notebook:
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Set plotting style
plt.style.use("default")
sns.set_palette("husl")
plt.rcParams["figure.figsize"] = (12, 8)
plt.rcParams["font.size"] = 12
```

### 2. Plotting Configuration
- **Default style**: Clean, professional appearance
- **Color palette**: Husl palette for better color distinction
- **Figure size**: Default 12x8 inches for good readability
- **Font size**: 12pt for clear labels and titles

### 3. Example Plotting Code

#### **Example 1: Time Series Plot**
- **Purpose**: Visualize sovereign spreads over time for multiple countries
- **Countries**: USA, Germany, France, Italy, Spain
- **Features**: 
  - Multiple country lines with different colors
  - Clear labels and legend
  - Grid for better readability
  - Professional formatting

#### **Example 2: Distribution Analysis**
- **Left plot**: Histogram of sovereign spreads
- **Right plot**: Box plot of sovereign spreads
- **Purpose**: Understand the distribution and identify outliers
- **Features**: Side-by-side comparison, grid lines, clear titles

#### **Example 3: Missing Data Heatmap**
- **Purpose**: Visualize missing data patterns across key variables
- **Variables**: sovereign_spread, cpi_yoy, gdp_annual_growth_rate, debt_to_gdp, vulnerability
- **Features**: 
  - Color-coded missing data visualization
  - Viridis colormap for accessibility
  - Clear variable labels

## Key Variables for Plotting

### **Core Variables Available:**
1. **`sovereign_spread`** - Main dependent variable
2. **`cpi_yoy`** - Consumer Price Index (year-over-year)
3. **`gdp_annual_growth_rate`** - GDP growth rate
4. **`debt_to_gdp`** - Government debt to GDP ratio
5. **`vulnerability`** - Climate vulnerability index
6. **`date`** - Time dimension
7. **`iso3c`** - Country identifiers

### **Fixed Effects Available:**
- **Country dummies**: 80 variables (e.g., `country_USA`, `country_DEU`)
- **Time dummies**: 552 variables (e.g., `time_2020-01`, `time_2020-02`)

### **Lagged Variables Available:**
- **`sovereign_spread_lag1`** - One-period lag
- **`sovereign_spread_lag2`** - Two-period lag

## Usage Examples

### **Basic Time Series Plot**
```python
# Plot sovereign spreads for a specific country
country_data = df_data[df_data['iso3c'] == 'USA']
plt.figure(figsize=(12, 6))
plt.plot(country_data['date'], country_data['sovereign_spread'], linewidth=2)
plt.title('Sovereign Spreads - USA', fontsize=14, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Sovereign Spread (%)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### **Comparative Analysis**
```python
# Compare multiple countries
countries = ['USA', 'DEU', 'FRA']
plt.figure(figsize=(15, 8))

for country in countries:
    country_data = df_data[df_data['iso3c'] == country]
    if not country_data.empty:
        plt.plot(country_data['date'], country_data['sovereign_spread'], 
                label=country, linewidth=2, alpha=0.8)

plt.title('Sovereign Spreads Comparison', fontsize=16, fontweight='bold')
plt.xlabel('Date', fontsize=14)
plt.ylabel('Sovereign Spread (%)', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### **Missing Data Analysis**
```python
# Analyze missing data patterns
missing_summary = df_data.isnull().sum()
missing_pct = (missing_summary / len(df_data)) * 100

plt.figure(figsize=(12, 6))
missing_pct.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Missing Data Percentage by Variable', fontsize=14, fontweight='bold')
plt.xlabel('Variables', fontsize=12)
plt.ylabel('Missing Percentage (%)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

## Benefits

### **1. Data Visualization**
- **Time series analysis**: Track sovereign spreads over time
- **Distribution analysis**: Understand variable characteristics
- **Missing data patterns**: Identify data quality issues
- **Comparative analysis**: Compare countries and variables

### **2. Quality Control**
- **Outlier detection**: Identify unusual values
- **Data completeness**: Visualize missing data patterns
- **Temporal patterns**: Understand time-varying effects
- **Cross-sectional patterns**: Compare country characteristics

### **3. Presentation Ready**
- **Professional appearance**: Clean, publication-quality plots
- **Consistent styling**: Uniform appearance across all plots
- **Accessibility**: Good color schemes and readable fonts
- **Export ready**: High-resolution plots for reports

## Next Steps

1. **Run the examples**: Execute the plotting code to verify functionality
2. **Customize plots**: Modify colors, sizes, and styles as needed
3. **Add more visualizations**: Create additional plots for specific analysis needs
4. **Export plots**: Save plots for use in reports and presentations
5. **Interactive plots**: Consider adding plotly for interactive visualizations

## Notes

- **Memory usage**: Large datasets may require efficient plotting methods
- **Performance**: Consider downsampling for very long time series
- **Export formats**: Plots can be saved as PNG, PDF, or SVG
- **Customization**: All plot parameters can be adjusted for specific needs



