import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.express as px
import numpy as np



st.set_page_config(
    page_title="Medicare Payment Analytics",
    layout="wide"
)


#Imports

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "tables"

q1_df = pd.read_csv(OUTPUT_DIR / "q1_state_summary.csv")
q2_df = pd.read_csv(OUTPUT_DIR / "q2_regression_results.csv")
q3_df = pd.read_csv(
    OUTPUT_DIR / "q3_facility_differences.csv",
    dtype={"HCPCS_Cd": str}
)

q3_all_df = pd.read_csv(
    OUTPUT_DIR / "q3_all_tested_procedures.csv",
    dtype={"HCPCS_Cd": str}
)

#UI Work

st.title("Medicare Payment Analytics Dashboard")

st.markdown(
    """
    Analysis of CMS Medicare Physician & Other Practitioners claims data.

    This dashboard explores:
    - Geographic variation in payment efficiency
    - Drivers of Medicare payment amounts
    - Facility vs office payment differences
    """
)


tab1, tab2, tab3 = st.tabs(
    [
        "Geographic Variation",
        "Payment Drivers",
        "Facility vs Office"
    ]
)
q1_display = q1_df.rename(columns={
    "Rndrng_Prvdr_State_Abrvtn": "State",
    "mean": "Mean Payment Ratio",
    "std": "Standard Deviation",
    "count": "Claims"
})

q3_display = q3_df.copy()

q3_display["Percent Difference"] = (
        np.exp(q3_display["median_diff"]) - 1
) * 100

with tab1:
    st.header("Q1: Payment Efficiency by State")

    fig = px.choropleth(
        q1_display,
        locations="State",
        locationmode="USA-states",
        color="Mean Payment Ratio",
        hover_name="State",
        custom_data=["Mean Payment Ratio", "Standard Deviation", "Claims"],
        color_continuous_scale="Viridis",
        scope="usa",
        title="U.S. States by Medicare Payment Ratio"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=40, b=0)
    )

    fig.update_geos(
        bgcolor="rgba(0,0,0,0)"
    )

    fig.update_traces(
        hovertemplate=
            "<b>%{hovertext}</b><br><br>"
            "Mean Payment Ratio: %{customdata[0]:.3f}<br>"
            "Standard Deviation: %{customdata[1]:.3f}<br>"
            "Claims: %{customdata[2]:,.0f}"
            "<extra></extra>"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="States Analyzed",
            value=q1_display["State"].nunique()
        )

    with col2:
        st.metric(
            label="Effect Size (η²)",
            value="1.3%"
        )

    with col3:
        st.metric(
            label="Key Outliers",
            value="AK, WI"
        )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ### Key Finding

    Although payment ratios differed significantly across states (**p < 0.001**),
    state explained only about **1.3%** of the overall variation in payment ratios.
    Most variability occurred **within** states rather than **between** them.
    Alaska and Wisconsin accounted for many of the largest practically meaningful
    differences identified by the Tukey HSD analysis.
    """)

    st.subheader("State Summary")

    st.dataframe(
        q1_display.sort_values("Mean Payment Ratio", ascending=False).style.format({
            "Mean Payment Ratio": " {:.3f}",
            "Standard Deviation": " {:.3f}",
            "Claims": " {:,}"
        }),
        use_container_width=True,
        hide_index=True
    )

with tab2:
    st.header("Q2: Medicare Payment Drivers")

    st.caption(
        "Values represent estimated Medicare payment relative to the reference CPT category, "
        "holding state, specialty, place of service, rural/urban status, and beneficiary volume constant."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Adjusted R²",
            value="43.6%"
        )

    with col2:
        st.metric(
            label="Observations",
            value="9.76M"
        )

    with col3:
        st.metric(
            label="Strongest Driver",
            value="Procedure Type"
        )

    q2_cpt = q2_df[
        q2_df["feature"].str.contains("CPT_category")
    ].copy()

    q2_cpt["Category"] = (
        q2_cpt["feature"]
        .str.extract(r"\[T\.(.*)\]")
    )

    q2_cpt["Payment Multiplier"] = np.exp(q2_cpt["coefficient"])

    
    q2_cpt["Percent Impact"] = (
        q2_cpt["Payment Multiplier"] - 1
    ) * 100

    fig_cpt = px.bar(
        q2_cpt.sort_values("Payment Multiplier"),
        x="Payment Multiplier",
        y="Category",
        orientation="h",
        title="Procedure Category Impact on Medicare Payment",
        labels={
            "Payment Multiplier":
                "Payment Relative to Anesthesia (1.0 = Anesthesia)",
            "Category":"Procedure Category"
        }
    )

    fig_cpt.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    fig_cpt.add_vline(
        x=0,
        line_width=2
    )

    st.plotly_chart(fig_cpt, use_container_width=True)
    st.caption(
        "Bars show estimated Medicare payment relative to the reference procedure category "
        "(Anesthesia = 1.0), after controlling for state, provider specialty, place of service, "
        "rural/urban status, and beneficiary volume."
    )

    st.subheader("Procedure Category Effects")

    st.dataframe(
        q2_cpt[
            ["Category", "Percent Impact"]
        ]
        .sort_values(
            "Percent Impact",
            ascending=False
        )
        .style.format({
            "Percent Impact": "{:.1f}%"
        }),
        hide_index=True,
        use_container_width=True
    )

    st.subheader("Other Important Predictors")

    rural_effect = q2_df[
        q2_df["feature"] == "rural_urban"
    ].copy()

    rural_percent = (
        np.exp(rural_effect["coefficient"].iloc[0]) - 1
    ) * 100

    benes_effect = q2_df[
        q2_df["feature"] == "Tot_Benes_scaled"
    ].copy()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Rural Provider Payment Difference",
            value=f"{rural_percent:.1f}%"
        )

    with col2:
        st.metric(
            label="Beneficiary Volume Effect",
            value="Small Negative Association"
        )

    st.markdown("""
    ### Key Findings

    Procedure category was the strongest predictor of Medicare payment amounts.
    After controlling for provider specialty, geography, place of service, rural/urban
    classification, and beneficiary volume, procedure mix explained a substantial
    portion of payment variation.

    The model's adjusted R² increased from 14.5% to approximately 43.6% after adding
    CPT/HCPCS procedure categories, showing that the type of service performed is a
    major driver of Medicare payment amounts.

    Rural providers were associated with approximately 5.4% lower payments after
    controlling for procedure mix and other factors, suggesting that part of the
    raw rural/urban difference is explained by differences in service composition.
    """)


with tab3:
    st.header("Q3: Facility vs Office Payment Differences")

    st.caption(
        "Only procedures with a practically meaningful (≥5%) payment difference "
        "after Benjamini-Hochberg FDR correction are shown. Positive values indicate "
        "higher Medicare payments in facility settings than office settings."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Procedures Tested",
            len(q3_all_df)
        )

    with col2:
        st.metric(
            "Statistically Significant",
            int(q3_all_df["significant"].sum())
        )

    with col3:
        st.metric(
            "Practically Significant",
            len(q3_df)
        )


    fig_q3 = px.bar(
        q3_df.sort_values("percent_difference"),
        x="percent_difference",
        y="HCPCS_Cd",
        orientation="h",
        title="Facility vs Office Payment Differences by Procedure",
        labels={
            "percent_difference": "Facility Payment Difference (%)",
            "HCPCS_Cd": "HCPCS Procedure Code"
        },
        text="percent_difference"
    )

    fig_q3.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(
            type="category"
        )
    )

    fig_q3.update_traces(
        texttemplate="%{text:.1f}%"
    )
    

    st.plotly_chart(
        fig_q3,
        use_container_width=True
    )


    st.subheader("Significant Procedure Differences")

    st.dataframe(
        q3_df[
            [
                "HCPCS_Cd",
                "n_pairs",
                "p_value_fdr",
                "percent_difference"
            ]
        ]
        .sort_values(
            "percent_difference",
            ascending=False
        )
        .style.format({
            "p_value_fdr": "{:.2e}",
            "percent_difference": "{:.1f}%"
        }),
        hide_index=True,
        use_container_width=True
    )


    st.markdown("""
    ### Key Finding

    Facility and office payments differed significantly for several procedure codes
    after controlling for provider-level differences through paired comparisons.

    The largest differences were concentrated in specific procedures rather than
    occurring universally across all services. Statistical significance was adjusted
    using Benjamini-Hochberg false discovery rate correction to account for testing
    multiple HCPCS codes simultaneously.
    """)
    