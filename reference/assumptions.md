# Analysis Assumptions

## Q1: Geographic Variation in Medicare Payment Ratios

### Payment Ratio Definition
- Defined payment ratio as:
  
  Avg_Mdcr_Pymt_Amt / Avg_Sbmtd_Chrg

- This metric measures the fraction of submitted charges reimbursed by Medicare for a given provider-service observation.
- Used the row-level payment ratio rather than calculating total payments divided by total charges because these answer different analytical questions.
- The row-level ratio captures differences in the typical claim/provider-service observation, which aligns with the hypothesis testing objective.

### Data Filtering
- Removed provider demographic fields that were not relevant for payment analysis:
  - Provider middle name
  - Provider first name
  - Address secondary information
  - Provider credentials

- Removed observations missing RUCA information because rural/urban analysis requires a valid geographic classification.

- Excluded zero-payment observations and payment ratios above 1 for modeling analyses:
  - Zero payments may represent denied, rejected, or non-reimbursed claims rather than actual reimbursement behavior.
  - Ratios above 1 may represent crossover claims or coordination of benefits where combined payments exceed submitted charges.

### Statistical Testing
- Used one-way ANOVA to test whether mean payment ratios differed across states.
- Used η² effect size to evaluate practical importance because the large sample size could produce statistically significant results even when state-level differences explained little variation.
- Used Tukey HSD for pairwise state comparisons after ANOVA.
- Applied a 0.10 absolute mean difference threshold when identifying practically meaningful state pair differences.

## Q2: Drivers of Medicare Payment Variation

### Target Variable
- Modeled Avg_Mdcr_Pymt_Amt rather than payment ratio because the goal was to understand factors associated with Medicare payment amounts.
- Applied log transformation:

  log(Avg_Mdcr_Pymt_Amt)

- Log transformation was used because payment amounts were highly right-skewed with large outliers.
- Coefficients in the log model are interpreted as multiplicative changes in payment.

### Predictors
Included:
- Beneficiary volume (Tot_Benes)
- Rural/urban classification
- State fixed effects
- Provider specialty/type
- Place of service
- CPT/HCPCS category

### Category Handling
- Grouped provider specialties by frequency:
  - Retained top 40 provider types.
  - Combined remaining specialties into "Other."

- Created CPT categories using HCPCS code ranges and alphabetic HCPCS prefixes.
- Collapsed rare CPT categories into broader groups to avoid unstable coefficient estimates.

### Model Interpretation
- Evaluated adjusted R² to measure explanatory power.
- Focused interpretation on coefficient magnitude rather than only statistical significance due to the very large dataset.
- Standardized Tot_Benes after observing condition number concerns to distinguish scaling issues from true multicollinearity.

## Q3: Facility vs Non-Facility Payment Differences

### Study Design
- Compared facility and office payments for the same provider-procedure combination.
- Created paired observations using:
  - Rendering provider NPI
  - HCPCS code

- Only compared providers who performed the same HCPCS procedure in both facility and office settings.

### Statistical Testing
- Used Wilcoxon signed-rank testing because:
  - Payment differences were not assumed to be normally distributed.
  - Comparisons were paired within provider-procedure combinations.

- Required HCPCS codes to have at least 20 facility observations before testing.

### Multiple Testing
- Tested multiple HCPCS procedures independently.
- Applied Benjamini-Hochberg false discovery rate correction before identifying significant procedures.

### Practical Significance
- Converted median log payment differences back into percentage differences:

  (exp(median_diff)-1) * 100

- Defined practical significance as a >=5% payment difference.
- Selected the threshold after observing the distribution of FDR-significant results, where differences below 5% represented small statistical effects while larger differences represented potentially meaningful reimbursement gaps.

# Dashboard and Reporting Assumptions

## Dashboard Architecture

- The Streamlit dashboard does not directly process raw CMS claims data.
- Analytical transformations and statistical tests are performed in the analysis notebook.
- The dashboard consumes processed summary tables exported from the analysis pipeline.

### Output Tables

The dashboard depends on the following generated files:

- q1_state_summary.csv
  - State-level payment ratio summaries used for geographic visualization.

- q2_regression_results.csv
  - Regression coefficients, confidence intervals, and p-values used for model interpretation.

- q3_all_tested_procedures.csv
  - Complete HCPCS testing results used to report the statistical testing funnel.

- q3_facility_differences.csv
  - Filtered procedures meeting practical significance thresholds used for visualization.

### Reproducibility

- Raw CMS data is not included due to file size limitations.
- The notebook contains the transformation and modeling workflow required to regenerate dashboard outputs.

## Q4: Rural vs Urban Utilization Differences

### Utilization Metric Definition
- Compared rural and urban utilization using services-per-beneficiary rates:

  Tot_Srvcs / Tot_Benes

- This metric was used to normalize service volume by beneficiary population because raw service counts would primarily reflect differences in provider volume and population size.

### Overall Rural-Urban Comparison (Q4a)
- Tested whether aggregate utilization rates differed between rural and urban providers.
- Used a one-sided Mann-Whitney U test because the hypothesis specifically tested whether rural utilization was lower than urban utilization.

### Procedure-Level Analysis (Q4b)
- Tested each HCPCS procedure code independently to identify services with potentially larger rural-urban utilization gaps.
- Required sufficient observations per procedure to reduce instability from extremely rare services.
- Applied Benjamini-Hochberg false discovery rate correction because hundreds of simultaneous procedure-level tests were performed.

### Practical Significance
- Statistical significance alone was not considered sufficient because large datasets can detect very small differences.
- Procedures were only classified as practically significant when rural utilization was at least 5% lower than urban utilization.

### Interpretation Limitations
- Lower rural utilization does not necessarily indicate lack of access or unmet medical need.
- This analysis measures observed paid service utilization, not disease prevalence, patient preferences, referral patterns, or availability of specialists.
- The findings should be interpreted as identifying areas where rural-urban utilization differences exist, not proving causal barriers to care.
