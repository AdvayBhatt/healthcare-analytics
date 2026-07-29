# Analysis Challenges

## Q1: Geographic Variation in Medicare Payment Ratios

### Defining the Correct Metric
- Challenge:
  Determining whether to calculate payment ratio using aggregated state totals or average provider-level ratios.

- Resolution:
  Used the average of row-level payment ratios because the research question focused on differences between typical provider-service observations.

### Statistical vs Practical Significance
- Challenge:
  Millions of observations caused even small state differences to become statistically significant.

- Resolution:
  Added η² effect size analysis and practical thresholds for pairwise differences.

### Outlier States
- Challenge:
  Alaska and Wisconsin produced disproportionate Tukey HSD differences.

- Resolution:
  Performed sensitivity analysis excluding these states and compared the resulting ANOVA effect size.

## Q2: Drivers of Medicare Payment Variation

### Highly Skewed Payment Distribution
- Challenge:
  Medicare payment amounts contained extreme right skew.

- Resolution:
  Applied log transformation to stabilize variance and improve interpretability.

### High Cardinality Categories
- Challenge:
  Provider specialties and HCPCS codes contained many categories, including rare groups.

- Resolution:
  Grouped low-frequency categories into "Other" categories to improve model stability.

### CPT Categorization
- Challenge:
  HCPCS codes included both numeric CPT-style codes and alphabetic HCPCS codes.

- Resolution:
  Created separate classification logic:
  - Numeric CPT ranges
  - Alphabetic HCPCS prefixes

### Model Diagnostics
- Challenge:
  The regression condition number suggested possible numerical instability.

- Resolution:
  Standardized beneficiary volume variables and confirmed that scaling, rather than severe multicollinearity, was driving the issue.

## Q3: Facility vs Non-Facility Payment Differences

### Paired Comparison Design
- Challenge:
  Comparing facility and office payments directly could confound differences between providers.

- Resolution:
  Matched comparisons by provider NPI and HCPCS procedure so each comparison represented the same provider performing the same service in different settings.

### Multiple Comparisons
- Challenge:
  Testing hundreds of HCPCS codes increased the chance of false positives.

- Resolution:
  Applied Benjamini-Hochberg FDR correction.

### Statistical Significance vs Business Relevance
- Challenge:
  Large sample sizes caused some small payment differences to become statistically significant.

- Resolution:
  Added a practical significance threshold of 5% payment difference after converting log differences back into percentage changes.

### Interpreting Large Differences
- Challenge:
  Some procedures showed extremely large facility-office differences.

- Resolution:
  Investigated the largest differences and identified cataract procedures (66984 and 66982) as major outliers requiring contextual interpretation.
