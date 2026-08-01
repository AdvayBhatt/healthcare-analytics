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

  ### HCPCS Code Formatting

- Challenge:
  HCPCS codes contain both numeric and alphanumeric identifiers, and numeric-only codes with leading zeros can lose formatting during CSV export/import.

- Resolution:
  Preserved HCPCS codes as strings throughout dashboard ingestion to maintain identifier formatting.


  ## Q4: Rural vs Urban Utilization Differences

### Measuring Utilization Differences
- Challenge:
  Comparing raw service counts would mostly reflect differences in provider volume and population size rather than utilization behavior.

- Resolution:
  Normalized service counts by beneficiary volume using services-per-beneficiary rates.

### Small Overall Effect vs Procedure-Level Differences
- Challenge:
  Aggregate rural-urban differences were relatively small, which could hide important differences in specific healthcare services.

- Resolution:
  Performed procedure-level HCPCS analysis to identify where larger utilization gaps were concentrated.

### Multiple Procedure Testing
- Challenge:
  Testing 1,497 HCPCS procedures created a high risk of false positives.

- Resolution:
  Applied Benjamini-Hochberg FDR correction before identifying statistically significant procedures.

### Interpreting Specialized Care Differences
- Challenge:
  Oncology, radiation, and infusion-related procedures showed some of the largest rural-urban gaps, but claims data alone cannot determine whether these reflect access barriers, provider availability, referral patterns, or differences in patient need.

- Resolution:
  Framed findings as differences in observed utilization patterns rather than causal evidence of healthcare access limitations.
