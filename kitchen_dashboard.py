import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Kitchen Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Corrected filename to match the file on disk
DATA_FILE = "Kittchen PNL Data.xlsx"
SHEET_NAME = "Sheet 1 - stores"

VARIANCE_BUCKETS = [
    ("< 15,000", 0, 14999.99),
    ("15,000 – 20,000", 15000, 19999.99),
    ("20,000 – 25,000", 20000, 24999.99),
    ("25,000 – 30,000", 25000, 29999.99),
    ("> 30,000", 30000, float("inf")),
]

REVENUE_RANGES = [
    ("< 20 lacs", 0, 1999999.99),
    ("20 – 30 lacs", 2000000, 2999999.99),
    ("30 – 40 lacs", 3000000, 3999999.99),
    ("> 40 lacs", 4000000, float("inf")),
]

MONTH_ORDER = [
    "Jan-2023","Feb-2023","Mar-2023","Apr-2023","May-2023","Jun-2023",
    "Jul-2023","Aug-2023","Sep-2023","Oct-2023","Nov-2023","Dec-2023",
    "Jan-2024","Feb-2024","Mar-2024","Apr-2024","May-2024","Jun-2024",
    "Jul-2024","Aug-2024","Sep-2024","Oct-2024","Nov-2024","Dec-2024",
]

def assign_variance_bucket(value):
    for label, lo, hi in VARIANCE_BUCKETS:
        if lo <= value <= hi:
            return label
    return "Unknown"

def assign_revenue_range(value):
    for label, lo, hi in REVENUE_RANGES:
        if lo <= value <= hi:
            return label
    return "Unknown"

@st.cache_data
def load_data(filepath):
    df = pd.read_excel(filepath, sheet_name=SHEET_NAME, header=1)

    df.columns = df.columns.str.strip()

    df["GM%"] = (
        df["GROSS MARGIN"] /
        df["NET REVENUE"].replace(0, pd.NA)
    ) * 100

    df["CM"] = df["GROSS MARGIN"] - df["IDEAL FOOD COST"]

    df["CM%"] = (
        df["CM"] /
        df["NET REVENUE"].replace(0, pd.NA)
    ) * 100

    df["EBITDA"] = df["KITCHEN EBITDA"]

    df["VARIANCE BUCKET"] = df["VARIANCE"].apply(assign_variance_bucket)

    df["REVENUE RANGE"] = df["NET REVENUE"].apply(assign_revenue_range)

    present_months = [
        m for m in MONTH_ORDER
        if m in df["MONTH"].unique()
    ]

    df["MONTH"] = pd.Categorical(
        df["MONTH"],
        categories=present_months,
        ordered=True
    )

    return df

def multiselect_all(label, options, key):
    selected = st.sidebar.multiselect(
        label,
        options=options,
        key=key
    )

    return selected if selected else options

def build_sidebar(df):
    st.sidebar.header("Global Filters")

    cities = sorted(df["CITY"].dropna().unique().tolist())
    zones = sorted(df["ZONE MAPPING"].dropna().unique().tolist())
    months = df["MONTH"].cat.categories.tolist()

    sel_city = multiselect_all("City", cities, "city")
    sel_zone = multiselect_all("Zone", zones, "zone")
    sel_month = multiselect_all("Month", months, "month")

    return sel_city, sel_zone, sel_month

def apply_global_filter(df, sel_city, sel_zone, sel_month):
    mask = (
        df["CITY"].isin(sel_city) &
        df["ZONE MAPPING"].isin(sel_zone) &
        df["MONTH"].isin(sel_month)
    )

    return df[mask].copy()

def dashboard_kitchen_pnl(df):
    st.header("Dashboard 1 — Kitchen Performance")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        rev_cohorts = ["All"] + sorted(
            df["REVENUE COHORT"].dropna().unique().tolist()
        )

        sel_rev_cohort = st.selectbox(
            "Revenue Cohort",
            rev_cohorts,
            key="d1_rev_cohort"
        )

    with col2:
        cm_cohorts = ["All"] + sorted(
            df["CM COHORT"].dropna().unique().tolist()
        )

        sel_cm_cohort = st.selectbox(
            "CM Cohort",
            cm_cohorts,
            key="d1_cm_cohort"
        )

    with col3:
        ebitda_cats = ["All"] + sorted(
            df["EBITDA CATEGORY"].dropna().unique().tolist()
        )

        sel_ebitda_cat = st.selectbox(
            "EBITDA Category",
            ebitda_cats,
            key="d1_ebitda_cat"
        )

    with col4:
        ebitda_cohorts = ["All"] + sorted(
            df["EBITDA COHORT"].dropna().unique().tolist()
        )

        sel_ebitda_cohort = st.selectbox(
            "EBITDA Cohort",
            ebitda_cohorts,
            key="d1_ebitda_cohort"
        )

    st.markdown("### Range Filters")

    rc1, rc2, rc3 = st.columns(3)

    with rc1:
        rev_min = float(df["NET REVENUE"].min())
        rev_max = float(df["NET REVENUE"].max())

        rev_range = st.slider(
            "Net Revenue (INR)",
            min_value=rev_min,
            max_value=rev_max,
            value=(rev_min, rev_max),
            step=10000.0,
            format="₹%.0f",
            key="d1_rev_range"
        )

    with rc2:
        ebitda_min = float(df["EBITDA"].min())
        ebitda_max = float(df["EBITDA"].max())

        ebitda_range = st.slider(
            "EBITDA (INR)",
            min_value=ebitda_min,
            max_value=ebitda_max,
            value=(ebitda_min, ebitda_max),
            step=10000.0,
            format="₹%.0f",
            key="d1_ebitda_range"
        )

    with rc3:
        cm_min = float(df["CM"].min())
        cm_max = float(df["CM"].max())

        cm_range = st.slider(
            "Contribution Margin (INR)",
            min_value=cm_min,
            max_value=cm_max,
            value=(cm_min, cm_max),
            step=10000.0,
            format="₹%.0f",
            key="d1_cm_range"
        )

    fdf = df.copy()

    if sel_rev_cohort != "All":
        fdf = fdf[fdf["REVENUE COHORT"] == sel_rev_cohort]

    if sel_cm_cohort != "All":
        fdf = fdf[fdf["CM COHORT"] == sel_cm_cohort]

    if sel_ebitda_cat != "All":
        fdf = fdf[fdf["EBITDA CATEGORY"] == sel_ebitda_cat]

    if sel_ebitda_cohort != "All":
        fdf = fdf[fdf["EBITDA COHORT"] == sel_ebitda_cohort]

    fdf = fdf[
        fdf["NET REVENUE"].between(*rev_range) &
        fdf["EBITDA"].between(*ebitda_range) &
        fdf["CM"].between(*cm_range)
    ]

    stores = sorted(fdf["STORE"].dropna().unique().tolist())

    sel_stores = st.multiselect(
        "Store",
        options=stores,
        key="d1_store"
    )

    if sel_stores:
        fdf = fdf[fdf["STORE"].isin(sel_stores)]

    st.caption(
        f"Showing {len(fdf):,} records across "
        f"{fdf['STORE'].nunique()} stores"
    )

    if fdf.empty:
        st.warning("No records found.")
        return

    k1, k2, k3, k4, k5 = st.columns(5)

    k1.metric(
        "Total Net Revenue",
        f"₹{fdf['NET REVENUE'].sum():,.0f}"
    )

    k2.metric(
        "Total Gross Margin",
        f"₹{fdf['GROSS MARGIN'].sum():,.0f}"
    )

    k3.metric(
        "Average GM%",
        f"{fdf['GM%'].mean():.1f}%"
    )

    k4.metric(
        "Total EBITDA",
        f"₹{fdf['EBITDA'].sum():,.0f}"
    )

    k5.metric(
        "Average CM%",
        f"{fdf['CM%'].mean():.1f}%"
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "Monthly Trend",
        "Store Comparison",
        "EBITDA Distribution",
        "Raw Data"
    ])

    with tab1:
        monthly = (
            fdf.groupby("MONTH", observed=True)
            .agg(
                NET_REVENUE=("NET REVENUE", "sum"),
                GROSS_MARGIN=("GROSS MARGIN", "sum"),
                EBITDA=("EBITDA", "sum"),
            )
            .reset_index()
        )

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=monthly["MONTH"].astype(str),
            y=monthly["NET_REVENUE"],
            name="Net Revenue"
        ))

        fig.add_trace(go.Scatter(
            x=monthly["MONTH"].astype(str),
            y=monthly["GROSS_MARGIN"],
            name="Gross Margin",
            mode="lines+markers"
        ))

        fig.add_trace(go.Scatter(
            x=monthly["MONTH"].astype(str),
            y=monthly["EBITDA"],
            name="EBITDA",
            mode="lines+markers"
        ))

        fig.update_layout(
            title="Monthly Revenue, Gross Margin & EBITDA",
            xaxis_title="Month",
            yaxis_title="INR",
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        store_agg = (
            fdf.groupby("STORE")
            .agg(
                NET_REVENUE=("NET REVENUE", "sum"),
                EBITDA=("EBITDA", "sum"),
                GM_PCT=("GM%", "mean"),
                CM_PCT=("CM%", "mean"),
            )
            .reset_index()
            .sort_values("NET_REVENUE", ascending=False)
            .head(20)
        )

        fig2 = px.bar(
            store_agg,
            x="STORE",
            y="NET_REVENUE",
            color="EBITDA",
            title="Top 20 Stores — Net Revenue"
        )

        fig2.update_xaxes(tickangle=45)

        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        fig4 = px.histogram(
            fdf,
            x="EBITDA",
            nbins=30,
            color="EBITDA CATEGORY",
            title="EBITDA Distribution"
        )

        st.plotly_chart(fig4, use_container_width=True)

    with tab4:
        display_cols = [
            "MONTH",
            "CITY",
            "STORE",
            "STATUS",
            "ZONE MAPPING",
            "NET REVENUE",
            "GROSS MARGIN",
            "GM%",
            "CM",
            "CM%",
            "EBITDA",
        ]

        st.dataframe(
            fdf[display_cols]
            .sort_values(["MONTH", "STORE"])
            .reset_index(drop=True)
            .style.format({
                "NET REVENUE": "₹{:,.0f}",
                "GROSS MARGIN": "₹{:,.0f}",
                "CM": "₹{:,.0f}",
                "EBITDA": "₹{:,.0f}",
                "GM%": "{:.1f}%",
                "CM%": "{:.1f}%",
            }),
            use_container_width=True,
            height=450,
        )

def dashboard_variance_pnl(df):
    st.header("Dashboard 2 — Variance Analysis")

    bucket_labels = [b[0] for b in VARIANCE_BUCKETS]

    sel_buckets = st.multiselect(
        "Variance Bucket Filter",
        options=bucket_labels,
        key="d2_var_bucket",
    )

    if sel_buckets:
        fdf = df[df["VARIANCE BUCKET"].isin(sel_buckets)].copy()
    else:
        fdf = df.copy()

    if fdf.empty:
        st.warning("No records found.")
        return

    fdf["VARIANCE %"] = (
        fdf["VARIANCE"] /
        fdf["NET REVENUE"].replace(0, pd.NA)
    ) * 100

    sd1 = (
        fdf.groupby("REVENUE COHORT")
        .agg(
            AVG_VARIANCE_PCT=("VARIANCE %", "mean"),
            STORES=("STORE", "nunique"),
        )
        .reset_index()
    )

    fig_sd1 = px.bar(
        sd1,
        x="REVENUE COHORT",
        y="AVG_VARIANCE_PCT",
        color="AVG_VARIANCE_PCT",
        text=sd1["AVG_VARIANCE_PCT"].map("{:.2f}%".format),
        title="Average Variance %"
    )

    fig_sd1.update_traces(textposition="outside")

    st.plotly_chart(fig_sd1, use_container_width=True)

    pivot = (
        fdf.groupby(
            ["REVENUE RANGE", "MONTH"],
            observed=True
        )["STORE"]
        .count()
        .reset_index()
        .rename(columns={"STORE": "STORE COUNT"})
    )

    pivot_table = pivot.pivot(
        index="REVENUE RANGE",
        columns="MONTH",
        values="STORE COUNT",
    ).fillna(0).astype(int)

    fig_heatmap = go.Figure(
        data=go.Heatmap(
            z=pivot_table.values,
            x=[str(c) for c in pivot_table.columns],
            y=pivot_table.index.tolist(),
            text=pivot_table.values,
            texttemplate="%{text}"
        )
    )

    fig_heatmap.update_layout(
        title="Store Count Heatmap",
        xaxis_title="Month",
        yaxis_title="Revenue Range"
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)

def main():
    st.title("Kitchen Performance Dashboard")

    try:
        df = load_data(DATA_FILE)

    except FileNotFoundError:
        st.error(
            f"Data file '{DATA_FILE}' not found."
        )

        st.stop()

    sel_city, sel_zone, sel_month = build_sidebar(df)

    df_filtered = apply_global_filter(
        df,
        sel_city,
        sel_zone,
        sel_month
    )

    st.sidebar.metric(
        "Filtered Records",
        f"{len(df_filtered):,}"
    )

    st.sidebar.metric(
        "Unique Stores",
        f"{df_filtered['STORE'].nunique()}"
    )

    tab_pnl, tab_var = st.tabs([
        "Kitchen Performance",
        "Variance Analysis",
    ])

    with tab_pnl:
        dashboard_kitchen_pnl(df_filtered)

    with tab_var:
        dashboard_variance_pnl(df_filtered)

if __name__ == "__main__":
    main()
