# Healthcare Analytics: Medicare Claims Payment & Utilization Analysis

## Overview
A statistical analysis of CMS Medicare Physician & Other Practitioners claims data, examining payment efficiency, geographic variation in reimbursement, cost drivers, and utilization patterns across provider specialties and regions. This project is motivated by my experience in healthcare revenue cycle and risk adjustment analytics gained through two summers interning at Optum Insight.

## Motivation
Working inside a payer organization's revenue cycle quickly led me to ask where friction enters the path from a submitted claim to a paid claim, and how much of that friction is visible in public data. CMS's public data doesn't show when the claim processing actually occurs as a timestamp, so this project uses the closest available proxy in the relationship between what providers bill, what Medicare allows, and what Medicare actually pays to study payment efficiency, not processing time. That distinction is stated here throughout this repo (see `reference/assumptions.md`).

## Data Source
- **Dataset:** CMS Medicare Physician & Other Practitioners by Provider and Service
- **Source:** [data.cms.gov](https://data.cms.gov)
- **Granularity:** Provider x HCPCS procedure code x place of service

## Key Variables
| Variable | What It Enables |
|---|---|
| `Avg_Sbmtd_Chrg` | What providers billed |
| `Avg_Mdcr_Alowd_Amt` | What Medicare allowed |
| `Avg_Mdcr_Pymt_Amt` | What Medicare actually paid |
| `Avg_Mdcr_Stdzd_Amt` | Payment accounting for geographic variation |
| `Tot_Benes` | Patient volume |
| `Tot_Srvcs` | Service volume |
| `Place_Of_Srvc` | Facility v. office setting |
| `HCPCS_Cd` | Procedure code |
| `Rndrng_Prvdr_State_Abrvtn` | State (geographic analysis) |
| `Rndrng_Prvdr_RUCA` | Rural vs. urban classification |
| `Rndrng_Prvdr_Type` | Specialty |

**Derived metric: `payment_ratio`:**
```
payment_ratio = Avg_Mdcr_Pymt_Amt / Avg_Sbmtd_Chrg
```
The fraction of billed charges Medicare actually pays. Used throughout as the closest available metric for claim friction/payment efficiency in this dataset.

## Research Questions

**Q1: Payment efficiency by geography**
Does `payment_ratio` vary significantly by state after controlling for procedure type? ANOVA and post-hoc tests, visualized with a choropleth map for the US states.

**Q2: Cost drivers**
What predicts `Avg_Mdcr_Pymt_Amt`? Multiple regression using specialty, state, rural/urban classification, place of service, and volume as predictors, with inference like confidence intervals, F-test, residual diagnostics, and so on.

**Q3: Facility vs. non-facility payment differences**
Do providers in FACILITY settings receive systematically different payments than OFFICE settings for the SAME procedure? Two-sample tests are used like t-test / Wilcoxon with effect sizes.

**Q4: Utilization patterns by rural/urban status**
Do rural providers serve fewer beneficiaries per service type, and are certain procedures systematically underutilized in rural areas relative to urban ones?

Hypotheses

Q1: Payment efficiency by geography

H_0: `payment_ratio` does not vary significantly by state
H_1: `payment_ratio` varies significantly between at least two states


Q2: Cost drivers

Overall model (F-test): H_0: all regression coefficients = 0 (the model explains no variance in Avg_Mdcr_Pymt_Amt) vs. H₁: at least one coefficient ≠ 0
Per-predictor (t-tests): for each predictor, H_0: \beta = 0 (no effect, holding other predictors fixed) vs. H_1: \beta ≠ 0

Q3: Facility vs. non-facility payment differences

H_0: providers in facility settings do not receive systematically different payments than office settings for the same procedure
H_1: providers in facility settings receive systematically different payments than office settings for the same procedure


Q4a: Beneficiaries served, rural vs. urban

H_0: rural providers serve the same number of beneficiaries per service type as urban providers
H_1: rural providers serve fewer beneficiaries per service type than urban providers
One-sided, right-tailed test on (urban rate - rural rate)


Q4b: Procedure-level underutilization, rural vs. urban
Tested independently for each procedure code, using services-per-beneficiary rate ratios:

H_{0p}: the rural utilization rate for procedure p is not lower than the urban rate
H_{1p}: the rural utilization rate for procedure p is lower than the urban rate

Because this involves one hypothesis test per procedure code so dozens to hundreds of simultaneous tests, raw p-values are corrected for multiple comparisons using the Benjamini-Hochberg (FDR) procedure before any procedure is flagged as significantly underutilized. This controls the expected proportion of false positives among flagged procedures, rather than relying on an uncorrected 0.05 threshold that would produce misleading results at this scale.

## Methodology
Each question is answered with some statistical methods like EDA with distributional analysis, formally stated hypotheses, model fitting, assumption checking, and effect size interpretation alongside statistical significance.

## Findings

Q1: Payment efficiency by geography (DONE)

A one-way ANOVA found a statistically significant difference in mean payment_ratio across states (p < .001), but state explains only a small share of total variation (η² ≈ 1.3%) meaning that most of the spread in `payment_ratio` comes from claim-to-claim variation within states, not from which state a claim was filed in. Post-hoc Tukey HSD testing (filtered to pairs with a practically meaningful gap, |meandiff| > 0.10) showed that the large majority of those meaningful pairwise differences trace back to two extreme states in Alaska (highest) and Wisconsin (lowest) rather than being broadly distributed across all states. Re-running the ANOVA with AK and WI excluded dropped η² from ~1.3% to ~0.9%, confirming these two states account for a disproportionate but not dominant share of the already small state-level effect. Visualized as a state-level choropleth (outputs/figures/).

Q2: Cost drivers

Multiple regression on a log-transformed version of `Avg_Mdcr_Pymt_Amt` to address strong skewness towards the right, since OLS assumes ~normally distributed residuals. This was built up in stages to isolate what actually explains payment amount. A baseline model with state, top 40 specialties, place of service, rural/urban status, and patient volume explained only 14.5% of variance by adjusted R². Adding a procedure-type predictor in the CPT/HCPCS codes grouped into the categories Anesthesia, Surgery, Radiology, Pathology/Lab, Medicine, E/M, Drugs, etc., derived from official CPT numeric ranges and HCPCS Level II letter prefixes then raised adjusted R² to 43.6%, showing me that procedure type is by far the strongest driver of payment amount among the predictors considered. All predictors were statistically significant at p < .001 given the sample size of ~9.76M rows.

Holding procedure type, specialty, state, place of service, and volume constant, rural providers are associated with roughly a 5.4% lower average payment than urban providers which is interesting because the gap was around 10% before procedure mix was controlled for. That shows me part of the raw rural/urban payment gap reflects a difference in what procedures are performed rather than the rural/urban payment for the same procedure.

In addition, here are some diagnostics of note:
(1) a handful of procedure categories that were almost empty like DME, Orthotics/Prosthetics initially destabilized coefficient estimates and inflated the model's condition number roughly 20x. However, collapsing them into an "Other" bucket resolved this with no important loss in adjusted R². 

(2) the model's remaining moderate condition number turned out to be a pure scale artifact from `Tot_Benes` or patient volume, ranging into the thousands sitting alongside 0/1 dummy variables, not genuine multicollinearity between predictors. Then, standardizing Tot_Benes using z-scores dropped the condition number from ~1.95e+05 to 198 with no change to any other coefficient, R², or significance level, confirming the model was numerically stable all along.

## Limitations
This dataset reflects paid claims outcomes, not claims processing timelines. It cannot measure time-to-payment, denial-to-resubmission cycles, or true revenue cycle bottlenecks because understand those require proprietary claims processing timestamp data. `payment_ratio` and related metrics are proxies for payment efficiency and billing consistency, not direct measures of processing friction. This limitation is documented, again, in `reference/assumptions.md`

## Project Structure
```
healthcare-analytics/
├── data/
│   └── raw/              # downloaded CMS files
├── notebooks/
│   ├── 01_eda.ipynb      # exploratory analysis
│   ├── 02_cleaning.ipynb # data cleaning decisions
│   └── 03_modeling.ipynb # regression + inference
├── src/
│   ├── data_loader.py    # loading and preprocessing
│   └── model.py          # model fitting utilities
├── app/
│   └── dashboard.py      # Streamlit results dashboard
├── outputs/
│   ├── figures/          # saved charts
│   └── model_results/    # coefficient tables, diagnostics
├── reference/
│   └── assumptions.md    # explicit statement of data limitations
├── requirements.txt
└── README.md
```

## Tech Stack
Python, pandas, statsmodels, Plotly (choropleth mapping), Streamlit

## Status
In progress: EDA underway.
