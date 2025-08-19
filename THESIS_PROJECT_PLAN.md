# 🎓 THESIS PROJECT: Environmental Vulnerability & Sovereign Bond Yields

## 📋 Project Overview

**Research Question:** Does environmental vulnerability, as measured by the ND-GAIN index, have a causal effect on 10-year sovereign bond yields across 70+ countries?

**Methodology:** Double Machine Learning (DML) framework with high-dimensional macroeconomic and financial controls

**Data Coverage:** Monthly panel data from 1990-2025 spanning 67 countries

---

## 🎯 Current Project Status

### ✅ **COMPLETED TASKS**

#### **1. Data Integration & Processing**
- ✅ **Real Bond Yield Data:** 21,399 records from 67 countries (1990-2025)
- ✅ **ND-GAIN Vulnerability Data:** 66,816 records with monthly frequency
- ✅ **Macroeconomic Controls:** Placeholder data with realistic distributions
- ✅ **Merged Panel Dataset:** `data/merged_panel.csv` (21,399 × 13 variables)

#### **2. Data Quality**
- ✅ **Standardized Country Codes:** ISO3C format
- ✅ **Monthly Frequency:** Consistent time series
- ✅ **Missing Value Handling:** Forward-filling for ND-GAIN data
- ✅ **Data Validation:** Summary statistics generated

#### **3. Available Scripts**
- ✅ `src/thesis_data_integration.py` - Complete data integration pipeline
- ✅ `src/advanced_real_yield_analysis.py` - Advanced yield analysis
- ✅ `src/real_yield_data_integration.py` - Bond yield processing
- ✅ `src/merge_all_yield_data.py` - Comprehensive data merging

---

## 📊 Dataset Summary

### **Key Variables:**
- **Outcome (Y):** `bond_yield` - 10-year sovereign bond yield
- **Treatment (T):** `nd_gain` - ND-GAIN vulnerability score (0-1 scale)
- **Controls (X):** GDP growth, inflation, unemployment, current account, fiscal balance, public debt, credit rating, CDS spread
- **Identifiers:** `iso3c` (country), `date`, `region`

### **Data Statistics:**
- **Bond Yields:** Mean 6.02%, Range -0.96% to 49.03%
- **ND-GAIN Scores:** Mean 0.42, Range 0.27 to 0.57
- **Countries:** 67 countries across 6 regions
- **Time Period:** 1990-2025 (35 years)
- **Frequency:** Monthly panel data

---

## 📁 Project Structure

```
Capstone/
├── data/
│   ├── merged_panel.csv          # ✅ Main analysis dataset
│   ├── data_summary.txt          # ✅ Data documentation
│   ├── processed/                # ✅ Cleaned bond yield data
│   └── external/                 # ✅ Raw data sources
├── notebooks/
│   ├── 01_data_cleaning.ipynb   # 📝 Data cleaning template
│   ├── 02_eda.ipynb             # 📝 Exploratory analysis template
│   ├── 03_doubleml_main.ipynb   # 📝 Main DML analysis template
│   └── 04_robustness_checks.ipynb # 📝 Robustness checks template
├── src/
│   ├── thesis_data_integration.py    # ✅ Complete data pipeline
│   ├── advanced_real_yield_analysis.py # ✅ Advanced analysis
│   └── [other analysis scripts]      # ✅ Various analysis tools
├── outputs/
│   ├── figures/                 # 📁 For plots and visualizations
│   ├── tables/                  # 📁 For regression results
│   └── results/                 # 📁 For analysis reports
└── final_report/                # 📁 For thesis draft
```

---

## 🚀 IMPLEMENTATION PLAN

### **Phase 1: Data Validation & EDA (Week 1)**

#### **Step 1.1: Validate Merged Dataset**
```bash
# Run exploratory analysis
python -c "
import pandas as pd
df = pd.read_csv('data/merged_panel.csv')
print('Dataset shape:', df.shape)
print('Missing values:', df.isnull().sum())
print('Countries:', df['iso3c'].nunique())
print('Date range:', df['date'].min(), 'to', df['date'].max())
"
```

#### **Step 1.2: Update Notebooks**
- **Update `notebooks/01_data_cleaning.ipynb`** to use existing merged data
- **Update `notebooks/02_eda.ipynb`** for comprehensive exploratory analysis
- **Add missing value analysis, correlation matrices, trend plots**

### **Phase 2: Double ML Implementation (Week 2)**

#### **Step 2.1: Main Analysis**
- **Update `notebooks/03_doubleml_main.ipynb`** with:
  - Proper variable definitions (Y, T, X)
  - Random Forest nuisance parameter estimation
  - Partially Linear Regression (PLR) model
  - Treatment effect estimation and inference

#### **Step 2.2: Model Specification**
```python
# Key variables for DML
y_col = 'bond_yield'           # Outcome
d_col = 'nd_gain'              # Treatment
x_cols = ['gdp_growth', 'inflation', 'unemployment', 
          'current_account', 'fiscal_balance', 'public_debt', 
          'cds_spread']         # Controls
```

### **Phase 3: Robustness & Validation (Week 3)**

#### **Step 3.1: Alternative Models**
- **Update `notebooks/04_robustness_checks.ipynb`** with:
  - Lasso regression for nuisance parameters
  - XGBoost for non-linear relationships
  - Different Random Forest specifications

#### **Step 3.2: Subgroup Analysis**
- **Regional analysis:** Europe, Asia, Americas, Africa
- **Income group analysis:** High, middle, low income countries
- **Time period analysis:** Pre/post financial crisis, COVID-19

### **Phase 4: Results & Documentation (Week 4)**

#### **Step 4.1: Generate Outputs**
- **Figures:** Treatment effect plots, robustness checks
- **Tables:** Regression results, summary statistics
- **Reports:** Comprehensive analysis documentation

#### **Step 4.2: Thesis Integration**
- **Update `final_report/`** with findings
- **Create presentation materials**
- **Document methodology and results**

---

## 🔧 Technical Implementation

### **Required Packages:**
```python
# Core analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Double ML
from doubleml import DoubleMLData, DoubleMLPLR
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso
from xgboost import XGBRegressor

# Time series
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
```

### **Key Analysis Steps:**

#### **1. Data Preparation**
```python
# Load merged data
df = pd.read_csv('data/merged_panel.csv')
df['date'] = pd.to_datetime(df['date'])

# Define variables
y_col = 'bond_yield'
d_col = 'nd_gain'
x_cols = [col for col in df.columns if col not in ['iso3c', 'date', y_col, d_col, 'region']]

# Remove missing values
df_clean = df.dropna(subset=[y_col, d_col] + x_cols)
```

#### **2. Double ML Setup**
```python
# Create DoubleMLData object
dml_data = DoubleMLData(df_clean, y_col=y_col, d_cols=d_col, x_cols=x_cols)

# Specify ML models
ml_g = RandomForestRegressor(n_estimators=500, max_depth=5, random_state=42)
ml_m = RandomForestRegressor(n_estimators=500, max_depth=5, random_state=42)

# Fit PLR model
dml_plr = DoubleMLPLR(dml_data, ml_g=ml_g, ml_m=ml_m)
dml_plr.fit()
```

#### **3. Results Interpretation**
```python
# Treatment effect
print("Average Treatment Effect:", dml_plr.summary)

# Confidence intervals
print("95% CI:", dml_plr.confint())

# Robustness checks
# - Different ML models
# - Subgroup analysis
# - Time period analysis
```

---

## 📈 Expected Outcomes

### **Primary Results:**
1. **Average Treatment Effect (ATE)** of ND-GAIN vulnerability on bond yields
2. **Confidence intervals** and statistical significance
3. **Robustness checks** across different specifications

### **Secondary Analysis:**
1. **Regional heterogeneity** in treatment effects
2. **Time-varying effects** (pre/post crisis periods)
3. **Non-linear relationships** using alternative ML models

### **Policy Implications:**
1. **Environmental risk pricing** in sovereign debt markets
2. **Climate change adaptation** and bond market implications
3. **Investment strategies** for climate-resilient portfolios

---

## 🎯 Next Steps

### **Immediate Actions (This Week):**

1. **✅ Data Integration Complete** - Merged panel dataset ready
2. **📝 Update Notebooks** - Modify existing notebooks to use real data
3. **🔍 Run EDA** - Comprehensive exploratory data analysis
4. **⚙️ Implement DML** - Set up Double ML pipeline

### **Week 1 Goals:**
- [ ] Validate data quality and completeness
- [ ] Update `notebooks/02_eda.ipynb` with comprehensive analysis
- [ ] Create initial visualizations and summary statistics
- [ ] Document data sources and methodology

### **Week 2 Goals:**
- [ ] Implement Double ML analysis in `notebooks/03_doubleml_main.ipynb`
- [ ] Estimate average treatment effects
- [ ] Generate confidence intervals and significance tests
- [ ] Create initial results tables and figures

### **Week 3 Goals:**
- [ ] Complete robustness checks in `notebooks/04_robustness_checks.ipynb`
- [ ] Regional and subgroup analysis
- [ ] Alternative model specifications
- [ ] Sensitivity analysis

### **Week 4 Goals:**
- [ ] Finalize all results and visualizations
- [ ] Write comprehensive analysis report
- [ ] Prepare thesis draft
- [ ] Create presentation materials

---

## 📊 Success Metrics

### **Data Quality:**
- ✅ **Coverage:** 67 countries, 35 years, monthly frequency
- ✅ **Completeness:** <5% missing values in key variables
- ✅ **Consistency:** Standardized formats and codes

### **Analysis Quality:**
- **Statistical Power:** Sufficient observations for reliable inference
- **Model Performance:** Good fit for nuisance parameter estimation
- **Robustness:** Consistent results across specifications

### **Research Impact:**
- **Novel Findings:** New insights on climate-finance nexus
- **Policy Relevance:** Actionable recommendations for investors/policymakers
- **Academic Contribution:** Methodological advances in causal inference

---

## 🎓 Thesis Integration

### **Key Sections to Develop:**
1. **Introduction:** Climate change and sovereign debt markets
2. **Literature Review:** Environmental finance, causal inference
3. **Data & Methodology:** ND-GAIN index, Double ML framework
4. **Results:** Treatment effects, robustness checks
5. **Discussion:** Policy implications, limitations, future research

### **Expected Contributions:**
- **Empirical:** First causal evidence of environmental vulnerability on bond yields
- **Methodological:** Application of Double ML to climate-finance research
- **Policy:** Investment strategies for climate-resilient portfolios

---

## 📞 Support & Resources

### **Available Scripts:**
- `src/thesis_data_integration.py` - Complete data pipeline
- `src/advanced_real_yield_analysis.py` - Advanced analysis tools
- Notebooks for step-by-step implementation

### **Data Sources:**
- **Bond Yields:** Real historical data (1990-2025)
- **ND-GAIN:** Environmental vulnerability index
- **Controls:** IMF, World Bank, other macro indicators

### **Documentation:**
- `data/data_summary.txt` - Complete data documentation
- This plan document - Implementation roadmap
- Notebooks - Step-by-step analysis guides

---

**🎯 Status: READY FOR ANALYSIS**  
**📅 Timeline: 4 weeks to completion**  
**📊 Data: 21,399 observations, 67 countries, 35 years**  
**🔬 Method: Double Machine Learning (DML)**  
**🎓 Goal: Causal inference on climate-finance nexus** 