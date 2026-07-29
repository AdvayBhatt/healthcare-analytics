# Analysis Challenges

## Q1: Geographic Variation in Medicare Payments

- Challenge: Determining the appropriate payment metric required distinguishing between aggregate payment ratios and provider-level payment behavior.
- Resolution: Compared provider-level ratios because averaging ratios answers a different question than calculating total payments divided by total charges.

- Challenge: Large differences between states could be driven by a small number of extreme observations.
- Resolution: Investigated outlier states and performed sensitivity analysis after excluding problematic categories.

- Challenge: Statistical significance alone did not indicate whether differences were meaningful.
- Resolution: Added effect-size analysis using η² and pairwise comparisons.

## Q2: Drivers of Medicare Payment Variation

- Challenge: Healthcare payment data contained extreme skew and large variation across providers.
- Resolution: Applied log transformation to Medicare payments to improve model stability and make coefficients easier to interpret.

- Challenge: High-cardinality categorical variables created many regression coefficients.
- Resolution: Grouped smaller categories and evaluated whether categories contained enough observations.

- Challenge: Large sample size caused many predictors to become statistically significant.
- Resolution: Focused interpretation on coefficient magnitude and practical impact rather than p-values alone.

- Challenge: Initial model diagnostics indicated potential scaling/multicollinearity concerns.
- Resolution: Investigated predictors and confirmed whether issues were caused by variable scale or actual correlation problems.

## Q3: Facility vs Non-Facility Payment Differences

- Challenge: Testing hundreds of HCPCS codes increased the probability of false discoveries.
- Resolution: Applied Benjamini-Hochberg FDR correction before identifying significant procedures.

- Challenge: Several procedures were statistically significant but had very small payment differences.
- Resolution: Converted log differences into percentage differences and introduced a practical significance threshold.

- Challenge: Large differences required determining whether they represented meaningful patterns or data issues.
- Resolution: Investigated high-impact codes and identified cataract procedures (66984 and 66982) as notable examples requiring interpretation.
