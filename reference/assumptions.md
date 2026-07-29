# Analysis Assumptions

## Q1: Geographic Variation in Medicare Payments

- Used payment ratio metrics to compare Medicare payments relative to submitted charges across states.
- Calculated state-level comparisons using grouped statistics rather than averaging aggregate totals, because the research question focused on differences in provider-level payment behavior.
- Used ANOVA to test whether mean payment ratios differed across states.
- Applied Tukey HSD post-hoc testing after ANOVA to identify which state pairs had statistically significant differences.
- Considered effect size (η²) alongside statistical significance because large sample sizes can make small differences statistically significant.
- Excluded states/categories with insufficient observations when necessary to avoid unstable estimates.
- Investigated extreme outlier states separately rather than allowing a small number of observations to dominate conclusions.

## Q2: Drivers of Medicare Payment Variation

- Used log-transformed Medicare payment as the dependent variable because healthcare payment data is highly right-skewed and contains extreme values.
- Interpreted regression coefficients in log terms as approximate percentage differences in payment.
- Included provider, geographic, and service-related characteristics as predictors to identify factors associated with payment variation.
- Treated categorical variables (such as state, provider type, and place of service) as fixed effects.
- Used a large sample size model while recognizing that statistical significance does not necessarily imply practical importance.
- Evaluated model performance using adjusted R² rather than relying only on individual coefficient significance.
- Grouped rare categories where necessary to avoid unstable estimates from very small sample sizes.

## Q3: Facility vs Non-Facility Payment Differences

- Compared facility and non-facility payments using median differences in log-transformed payments.
- Used median differences rather than means to reduce sensitivity to extreme payment outliers.
- Tested HCPCS-level differences independently and applied Benjamini-Hochberg false discovery rate correction to account for multiple comparisons.
- Converted log differences back into percentage differences using:
  
  exp(median_diff) - 1

- Defined practical significance as a payment difference of at least 5%.
- Selected the 5% threshold based on observed effect-size distribution rather than a purely statistical cutoff.
- Retained large outliers (such as cataract procedures) because they represented meaningful payment patterns rather than data errors.
