import streamlit as st
import pandas as pd
from universal_data_loader import load_csv_file

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FORESIGHT",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# PREMIUM FORESIGHT DASHBOARD DESIGN
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #102a56;
    --navy-dark: #081b3d;
    --blue: #2563eb;
    --text: #12233f;
    --muted: #64748b;
    --border: #dbe5f1;
    --surface: #ffffff;
}

.stApp {
    background: #f3f7fc;
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1550px;
    padding: 2rem 2.5rem 3rem 2.5rem;
}

h1, h2, h3, h4 {
    color: var(--text) !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
}

h1 { font-size: 42px !important; margin-bottom: 0 !important; }
h2 { font-size: 27px !important; margin-top: 1.5rem !important; }
h3 { font-size: 22px !important; margin-top: 1.25rem !important; }

p, label, .stMarkdown, .stCaption { color: #334155 !important; }

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #102a56 0%, #081b3d 100%) !important;
    min-width: 255px !important;
}
section[data-testid="stSidebar"] * { color: #eaf2ff !important; }
section[data-testid="stSidebar"] .stMarkdown p { color: #d7e6ff !important; }

/* HEADER */
.foresight-header {
    background: transparent;
    padding: 0 0 1.2rem 0;
}
.foresight-kicker {
    color: #64748b !important;
    font-size: 14px;
    margin-top: -8px;
    margin-bottom: 12px;
}
.status-pill {
    display: inline-block;
    padding: 9px 15px;
    border-radius: 999px;
    background: #dcfce7;
    color: #166534 !important;
    font-size: 13px;
    font-weight: 700;
    border: 1px solid #bbf7d0;
}

/* METRIC CARDS */
div[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    border-radius: 18px !important;
    padding: 22px 24px !important;
    min-height: 128px;
    box-shadow: 0 8px 24px rgba(16, 42, 86, 0.07) !important;
}
div[data-testid="stMetricLabel"] {
    color: #52637a !important;
    font-size: 14px !important;
    font-weight: 700 !important;
}
div[data-testid="stMetricValue"] {
    color: #102a56 !important;
    font-size: 30px !important;
    font-weight: 800 !important;
}

/* FILTER / INPUTS */
div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1px solid #cbd8e8 !important;
    border-radius: 11px !important;
    min-height: 44px;
}
div[data-baseweb="select"] * { color: #102a56 !important; }
.stDateInput input, .stTextInput input {
    background: #ffffff !important;
    color: #102a56 !important;
    border-radius: 11px !important;
}

/* BUTTONS */
/* LIGHT BLUE PROFESSIONAL BUTTONS */

.stButton > button,
.stDownloadButton > button {
    background: #dbeafe !important;
    color: #1e40af !important;
    border: 1px solid #93c5fd !important;
    border-radius: 11px !important;
    font-weight: 700 !important;
    min-height: 42px;
    padding: 10px 20px !important;
}

/* BUTTON HOVER */

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #bfdbfe !important;
    color: #1e3a8a !important;
    border: 1px solid #60a5fa !important;
}

/* DATA TABLES */
div[data-testid="stDataFrame"] {
    border: 1px solid #d7e2ef !important;
    border-radius: 15px !important;
    overflow: hidden !important;
    box-shadow: 0 5px 18px rgba(16, 42, 86, 0.05);
}

/* CHARTS */
div[data-testid="stVegaLiteChart"], div[data-testid="stArrowVegaLiteChart"] {
    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 12px !important;
    box-shadow: 0 6px 20px rgba(16, 42, 86, 0.05);
}

/* ALERTS */
div[data-testid="stAlert"] {
    border-radius: 13px !important;
    border: 1px solid #dbe5f1 !important;
}

hr { border-color: #dbe5f1 !important; }

/* SECTION SPACING */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
    gap: 0.7rem;
}


/* ============================================================
   RESPONSIVE DESIGN - DESKTOP, TABLET & MOBILE
   ============================================================ */

/* LARGE SCREENS */
@media (min-width: 1600px) {
    .block-container {
        max-width: 1700px;
        padding-left: 3rem;
        padding-right: 3rem;
    }
}

/* TABLETS AND SMALL LAPTOPS */
@media (max-width: 1100px) {
    .block-container {
        padding-left: 1.25rem;
        padding-right: 1.25rem;
    }

    h1 {
        font-size: 34px !important;
    }

    h2 {
        font-size: 24px !important;
    }

    h3 {
        font-size: 19px !important;
    }

    div[data-testid="stMetric"] {
        padding: 18px !important;
        min-height: 112px;
    }

    div[data-testid="stMetricValue"] {
        font-size: 25px !important;
    }
}

/* MOBILE DEVICES */
@media (max-width: 768px) {
    .block-container {
        padding: 1rem 0.75rem 2rem 0.75rem;
        width: 100% !important;
    }

    h1 {
        font-size: 28px !important;
        line-height: 1.2 !important;
    }

    h2 {
        font-size: 22px !important;
        line-height: 1.25 !important;
    }

    h3 {
        font-size: 18px !important;
        line-height: 1.3 !important;
    }

    p, label, .stMarkdown, .stCaption {
        font-size: 13px !important;
    }

    .foresight-header {
        padding-bottom: 0.75rem;
    }

    .foresight-kicker {
        font-size: 12px !important;
        line-height: 1.5 !important;
    }

    .status-pill {
        display: block;
        width: fit-content;
        max-width: 100%;
        font-size: 11px !important;
        padding: 7px 10px !important;
    }

    /* Stack Streamlit columns vertically on phones */
    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        gap: 0.65rem !important;
    }

    [data-testid="stHorizontalBlock"] > [data-testid="column"] {
        min-width: 100% !important;
        width: 100% !important;
        flex: 1 1 100% !important;
    }

    div[data-testid="stMetric"] {
        width: 100% !important;
        min-height: auto !important;
        padding: 16px !important;
        border-radius: 14px !important;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 12px !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 25px !important;
        overflow-wrap: anywhere !important;
    }

    div[data-baseweb="select"] > div {
        min-height: 42px !important;
    }

    .stButton > button,
    .stDownloadButton > button {
        width: 100% !important;
        min-height: 44px !important;
        font-size: 13px !important;
    }

    div[data-testid="stDataFrame"] {
        max-width: 100% !important;
        overflow-x: auto !important;
        border-radius: 10px !important;
    }

    div[data-testid="stVegaLiteChart"],
    div[data-testid="stArrowVegaLiteChart"] {
        padding: 4px !important;
        border-radius: 12px !important;
        overflow-x: auto !important;
    }

    .stPlotlyChart,
    [data-testid="stImage"] {
        max-width: 100% !important;
        overflow-x: auto !important;
    }

    section[data-testid="stSidebar"] {
        min-width: 0 !important;
    }
}

/* VERY SMALL PHONES */
@media (max-width: 420px) {
    .block-container {
        padding-left: 0.55rem;
        padding-right: 0.55rem;
    }

    h1 {
        font-size: 24px !important;
    }

    h2 {
        font-size: 20px !important;
    }

    div[data-testid="stMetricValue"] {
        font-size: 22px !important;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="foresight-header">
    <h1>📊 FORESIGHT</h1>
    <h3>Demand Forecasting &amp; Inventory Risk Intelligence</h3>
    <div class="foresight-kicker">Live operational view • Forecast monitoring • Inventory risk prioritisation</div>
    <span class="status-pill">● System Online · Forecast data loaded</span>
</div>
""", unsafe_allow_html=True)

# ==============================
# UNIVERSAL CSV UPLOAD SYSTEM
# ==============================

st.sidebar.header("📂 Upload Business Data")

uploaded_files = st.sidebar.file_uploader(
    "Upload one or multiple CSV files",
    type=["csv"],
    accept_multiple_files=True
)

uploaded_dataframes = []

if uploaded_files:

    try:
        for file in uploaded_files:

            df, metadata = load_csv_file(file)

            df["source_file"] = file.name

            uploaded_dataframes.append(df)

        st.success(
            f"✅ {len(uploaded_dataframes)} CSV file(s) uploaded successfully!"
        )

        st.subheader("📊 Uploaded Data Preview")

        for df in uploaded_dataframes:

            st.write(
                f"**File:** {df['source_file'].iloc[0]}"
            )

            st.write(
                f"Rows: {df.shape[0]} | Columns: {df.shape[1]}"
            )

            st.dataframe(
                df.head(10),
                width="stretch"
            )

        uploaded_df = pd.concat(
            uploaded_dataframes,
            ignore_index=True,
            sort=False
        )


        if uploaded_files:
            st.subheader("🔍 Standardized Uploaded Columns")

            st.write(
                sorted(uploaded_df.columns.tolist())
        )


        st.subheader("📦 Combined Uploaded Data")

        st.write(f"Total Rows: {uploaded_df.shape[0]}")
        st.write(f"Total Columns: {uploaded_df.shape[1]}")

        # SKU mapping diagnostics: identify duplicate or inconsistent SKU identities
        if "sku_id" in uploaded_df.columns and "source_file" in uploaded_df.columns:
            sku_source_check = (
                uploaded_df.groupby("source_file")["sku_id"]
                .nunique()
                .reset_index(name="unique_skus")
            )
            st.caption("SKU mapping check")
            st.dataframe(sku_source_check, use_container_width=True, hide_index=True)

        st.dataframe(
            uploaded_df.head(10),
            width="stretch"
        )

    except Exception as error:

        st.error(
            f"❌ Upload Error: {error}"
        )

# ============================================================
# LOAD DATA
# ============================================================

# Load SKU-level inventory risk results
risk_data = pd.read_csv(
    "data/processed/sku_risk_results.csv"
)

# Load weekly forecast results
forecast_data = pd.read_csv(
    "data/processed/forecast_results.csv"
)

# Convert forecast date to datetime
forecast_data["week_start"] = pd.to_datetime(
    forecast_data["week_start"]
)

# ============================================================
# BUILD RISK DATA FROM UPLOADED BUSINESS CSVs
# ============================================================
# When CSVs are uploaded, calculate SKU-level operational metrics
# from the uploaded inventory and sales data instead of relying only
# on the pre-generated risk result file.
if uploaded_files and "sku_id" in uploaded_df.columns:
    uploaded_work = uploaded_df.copy()

    # ========================================================
    # USE THE COMPLETE SKU UNIVERSE
    # ========================================================
    # Do not restrict the dashboard to sku_master only.
    # The uploaded inventory file contains the complete 200-SKU
    # universe, while the sales/master files may contain fewer SKUs.

    uploaded_work["sku_id"] = (
        uploaded_work["sku_id"]
        .astype("string")
        .str.strip()
    )

    uploaded_work = uploaded_work[
        uploaded_work["sku_id"].notna()
        & uploaded_work["sku_id"].ne("")
        & uploaded_work["sku_id"].ne("<NA>")
    ].copy()

    # Convert numeric columns safely.
    for numeric_column in [
        "units_sold",
        "Current_Stock",
        "Inventory_Value",
    ]:
        if numeric_column in uploaded_work.columns:
            uploaded_work[numeric_column] = pd.to_numeric(
                uploaded_work[numeric_column],
                errors="coerce"
            ).fillna(0)

    # Keep every unique SKU from all uploaded business files.
    # This ensures inventory-only SKUs are also displayed.
    all_uploaded_skus = (
        uploaded_work["sku_id"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
    )

    st.sidebar.success(
        f"Complete SKU universe detected: {len(all_uploaded_skus)} SKUs"
    )

    # Demand is calculated only from rows that contain sales data.
    if "units_sold" in uploaded_work.columns:
        sales_by_sku = (
            uploaded_work.groupby("sku_id", as_index=False)["units_sold"]
            .sum()
            .rename(columns={"units_sold": "forecast_demand"})
        )
    else:
        sales_by_sku = pd.DataFrame({
            "sku_id": all_uploaded_skus,
            "forecast_demand": 0
        })

    # Inventory is calculated only from available inventory fields.
    inventory_columns = ["sku_id"]

    if "Current_Stock" in uploaded_work.columns:
        inventory_columns.append("Current_Stock")

    if "Inventory_Value" in uploaded_work.columns:
        inventory_columns.append("Inventory_Value")

    inventory_by_sku = (
        uploaded_work[inventory_columns]
        .groupby("sku_id", as_index=False)
        .max()
    )

    # Start with all SKUs, then merge demand and inventory metrics.
    sku_universe = pd.DataFrame({"sku_id": all_uploaded_skus})

    risk_data = (
        sku_universe
        .merge(sales_by_sku, on="sku_id", how="left")
        .merge(inventory_by_sku, on="sku_id", how="left")
        .fillna(0)
    )

    risk_data = risk_data.rename(
        columns={
            "Current_Stock": "available_inventory",
            "Inventory_Value": "rupee_value_at_risk"
        }
    )

    if "forecast_demand" not in risk_data.columns:
        risk_data["forecast_demand"] = 0

    if "available_inventory" not in risk_data.columns:
        risk_data["available_inventory"] = 0

    if "rupee_value_at_risk" not in risk_data.columns:
        risk_data["rupee_value_at_risk"] = 0

    # Ensure all KPI columns are numeric.
    for metric_column in [
        "forecast_demand",
        "available_inventory",
        "rupee_value_at_risk",
    ]:
        risk_data[metric_column] = pd.to_numeric(
            risk_data[metric_column],
            errors="coerce"
        ).fillna(0)

    risk_data["inventory_coverage"] = (
        risk_data["available_inventory"]
        / risk_data["forecast_demand"].replace(0, 1)
    )

    # Ensure every SKU receives a valid risk classification.
    risk_data["inventory_coverage"] = pd.to_numeric(
        risk_data["inventory_coverage"],
        errors="coerce"
    ).fillna(0)

    risk_data["risk_level"] = "Healthy"

    risk_data.loc[
        risk_data["inventory_coverage"] < 0.25,
        "risk_level"
    ] = "Reorder Now"

    risk_data.loc[
        (risk_data["inventory_coverage"] >= 0.25)
        & (risk_data["inventory_coverage"] < 0.75),
        "risk_level"
    ] = "Watch / Volatile"

    risk_data.loc[
        (risk_data["inventory_coverage"] >= 0.75)
        & (risk_data["inventory_coverage"] < 1.0),
        "risk_level"
    ] = "Markdown/Clear"


    # Add downstream risk metrics used by tables and decision grid
    risk_data["stockout_shortfall_units"] = (
        risk_data["forecast_demand"] - risk_data["available_inventory"]
    ).clip(lower=0)

    risk_data["overstock_excess_units"] = (
        risk_data["available_inventory"] - risk_data["forecast_demand"]
    ).clip(lower=0)

    # Normalize risk labels so summary cards and filters use the same values
    risk_data["risk_level"] = risk_data["risk_level"].replace({
        "Watch/Volatile": "Watch / Volatile",
        "Markdown / Clear": "Markdown/Clear",
    }).fillna("Healthy")

    risk_data["recommended_action"] = risk_data["risk_level"].map({
        "Reorder Now": "Reorder inventory",
        "Watch / Volatile": "Monitor demand and stock",
        "Markdown/Clear": "Consider markdown",
        "Healthy": "No immediate action"
    }).fillna("Review inventory")


if forecast_data["week_start"].isna().any():
    st.warning("Some forecast dates could not be read.")

# Load original dataset for category filtering
if uploaded_files:
    raw_data = uploaded_df.copy()
else:
    raw_data = pd.read_csv(
        "data/raw/retail_store_inventory.csv"
    )

if risk_data.empty:
    st.warning("No risk data available.")
    st.stop()

if forecast_data.empty:
    st.warning("No forecast data available.")
    st.stop()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.markdown("""
<div style="padding: 12px 4px 28px 4px;">
    <div style="font-size: 28px; font-weight: 800; color: white;">📊 FORESIGHT</div>
    <div style="font-size: 12px; color: #b9d2f5; margin-top: 6px;">Smarter Forecasts<br>Stronger Supply Chains</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.header("⚙️ Filters")


# -------------------- SKU FILTER --------------------

# Create SKU selection options
sku_options = ["All"] + sorted(
    risk_data["sku_id"].unique().tolist()
)

selected_sku = st.sidebar.selectbox(
    "Select SKU",
    sku_options
)


# -------------------- RISK FILTER --------------------

# Create risk level options
risk_options = ["All"] + sorted(
    risk_data["risk_level"].unique().tolist()
)

selected_risk = st.sidebar.selectbox(
    "Risk Level",
    risk_options
)


# -------------------- CATEGORY FILTER --------------------

# Create category options from uploaded data
if "category" in raw_data.columns:

    category_options = ["All"] + sorted(
        raw_data["category"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

else:

    category_options = ["All"]


selected_category = st.sidebar.selectbox(
    "Category",
    category_options
)



# APPLY CATEGORY FILTER

display_data = risk_data.copy()


# -------------------- APPLY SKU FILTER --------------------

if selected_sku != "All":
    display_data = display_data[
        display_data["sku_id"] == selected_sku
    ].copy()


# -------------------- APPLY RISK FILTER --------------------

if selected_risk != "All":
    display_data = display_data[
        display_data["risk_level"] == selected_risk
    ].copy()



if selected_category != "All":
    category_skus = raw_data.copy()

    if "category" in category_skus.columns and "sku_id" in category_skus.columns:
        category_skus["sku_id"] = category_skus["sku_id"].astype(str)
    elif (
        "category" in category_skus.columns
        and "store_id" in category_skus.columns
        and "product_id" in category_skus.columns
    ):
        category_skus["sku_id"] = (
            category_skus["store_id"].astype(str) + "_" +
            category_skus["product_id"].astype(str)
        )
    else:
        category_skus = pd.DataFrame()

    if not category_skus.empty:
        sku_category = (
            category_skus[category_skus["category"].notna()]
            .assign(category=lambda df: df["category"].astype(str).str.strip())
            .groupby("sku_id")["category"]
            .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else "Unknown")
            .reset_index()
        )
        selected_category_skus = sku_category.loc[
            sku_category["category"] == selected_category, "sku_id"
        ]
        display_data = display_data[
            display_data["sku_id"].astype(str).isin(selected_category_skus.astype(str))
        ].copy()
    else:
        st.warning("Category filtering is unavailable for this dataset.")

if display_data.empty:
    st.warning("No SKUs match the selected filters.")
    st.stop()

# ============================================================
# KPI METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

high_risk_count = int((display_data["risk_level"] == "Reorder Now").sum())

with col1:
    st.metric("Total SKUs", display_data["sku_id"].nunique())

with col2:
    st.metric("Forecast Demand", f"{display_data['forecast_demand'].sum():,.0f}")

with col3:
    st.metric("Value at Risk", f"₹{display_data['rupee_value_at_risk'].sum():,.0f}")

with col4:
    st.metric("At High Risk", high_risk_count)


# ============================================================
# RISK OVERVIEW
# ============================================================

st.subheader("Risk Overview")


# Count SKUs in each risk category
risk_summary = (
    display_data["risk_level"]
    .value_counts()
    .reset_index()
)

risk_summary.columns = [
    "risk_level",
    "sku_count"
]


# Display risk summary table
st.dataframe(
    risk_summary,
    width="stretch",
    hide_index=True
)


# Display risk summary chart
st.bar_chart(
    risk_summary.set_index("risk_level")["sku_count"]
)


# ============================================================
# RISK SUMMARY CARDS
# ============================================================

st.subheader("Risk Summary")


# Count each risk level
risk_counts = display_data["risk_level"].value_counts()


col1, col2, col3, col4 = st.columns(4)


with col1:

    # SKUs requiring immediate reorder
    st.metric(
        "Reorder Now",
        risk_counts.get("Reorder Now", 0)
    )


with col2:

    # SKUs with overstock risk
    st.metric(
        "Markdown / Clear",
        risk_counts.get("Markdown/Clear", 0)
    )


with col3:

    # SKUs with both risk conditions
    st.metric(
        "Watch / Volatile",
        risk_counts.get("Watch / Volatile", 0)
    )


with col4:

    # SKUs with no immediate risk
    st.metric(
        "Healthy",
        risk_counts.get("Healthy", 0)
    )


# ============================================================
# FORECAST VS ACTUAL
# ============================================================

st.subheader("Forecast Date Filter")

min_date = forecast_data["week_start"].min().date()
max_date = forecast_data["week_start"].max().date()

selected_dates = st.date_input(
    "Select Forecast Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = selected_dates

    forecast_data = forecast_data[
        (forecast_data["week_start"].dt.date >= start_date)
        & (forecast_data["week_start"].dt.date <= end_date)
    ].copy()

st.caption(
    f"Forecast Horizon: {forecast_data['week_start'].min().date()} "
    f"to {forecast_data['week_start'].max().date()}"
)

st.subheader("Forecast vs Actual")


if selected_sku == "All":

    # Aggregate actual and forecast demand across SKUs
    chart_data = (
        forecast_data
        .groupby("week_start")[
            ["units_sold", "gb_prediction"]
        ]
        .sum()
        .reset_index()
    )

else:

    # Show forecast and actual for selected SKU
    chart_data = forecast_data[
        forecast_data["sku_id"] == selected_sku
    ][
        [
            "week_start",
            "units_sold",
            "gb_prediction"
        ]
    ].copy()


# Clean and rename chart series for readable labels
if not chart_data.empty:
    for col in ["units_sold", "gb_prediction"]:
        if col in chart_data.columns:
            chart_data[col] = pd.to_numeric(chart_data[col], errors="coerce").fillna(0)
    chart_data = chart_data.rename(columns={
        "units_sold": "Actual Demand",
        "gb_prediction": "Forecast Demand"
    })

# Set week as chart index
chart_data = chart_data.set_index("week_start")


# Display actual and forecast demand
if chart_data.empty:
    st.info("No forecast-versus-actual data is available for the selected filters and date range.")
else:
    st.line_chart(
        chart_data,
        y=[
            "Actual Demand",
            "Forecast Demand"
        ]
    )


# ============================================================
# FORECAST UNCERTAINTY
# ============================================================

st.subheader("Forecast Uncertainty")


if selected_sku == "All":

    # Aggregate uncertainty across all SKUs
    uncertainty_data = (
        forecast_data
        .groupby("week_start")[
            [
                "gb_prediction",
                "forecast_lower_80",
                "forecast_upper_80"
            ]
        ]
        .mean()
        .reset_index()
    )

else:

    # Show uncertainty for selected SKU
    uncertainty_data = forecast_data[
        forecast_data["sku_id"] == selected_sku
    ][
        [
            "week_start",
            "gb_prediction",
            "forecast_lower_80",
            "forecast_upper_80"
        ]
    ].copy()


# Set week as chart index
uncertainty_data = uncertainty_data.set_index(
    "week_start"
)


# Display forecast uncertainty
if uncertainty_data.empty:
    st.info("No forecast uncertainty data is available for the selected filters and date range.")
else:
    st.line_chart(
        uncertainty_data,
        y=[
            "gb_prediction",
            "forecast_lower_80",
            "forecast_upper_80"
        ]
    )


# ============================================================
# INVENTORY COVERAGE
# ============================================================

st.subheader("Inventory Coverage")


# Calculate total forecast demand
total_forecast = display_data[
    "forecast_demand"
].sum()


# Calculate total available inventory
total_inventory = display_data[
    "available_inventory"
].sum()


# Calculate inventory coverage ratio
if total_forecast > 0:

    coverage_ratio = (
        total_inventory / total_forecast
    )

else:

    coverage_ratio = 0


col1, col2, col3 = st.columns(3)


with col1:

    # Show forecast demand
    st.metric(
        "12-Week Forecast Demand",
        f"{total_forecast:,.0f}"
    )


with col2:

    # Show available inventory
    st.metric(
        "Available Inventory",
        f"{total_inventory:,.0f}"
    )


with col3:

    # Show inventory coverage
    st.metric(
        "Inventory Coverage",
        f"{coverage_ratio:.2f}x"
    )


# ============================================================
# INVENTORY COMPARISON
# ============================================================

st.subheader("Forecast Demand vs Available Inventory")


# Prepare inventory comparison data
inventory_chart = pd.DataFrame({
    "Metric": [
        "Forecast Demand",
        "Available Inventory"
    ],
    "Units": [
        total_forecast,
        total_inventory
    ]
})


# Display inventory comparison
st.bar_chart(
    inventory_chart.set_index("Metric")
)


# ============================================================
# PRIORITIZED REORDER LIST
# ============================================================

st.subheader("Prioritized Reorder List")


# Keep only SKUs requiring reorder
reorder_data = display_data[
    display_data["risk_level"] == "Reorder Now"
].copy()


# Sort by financial risk
reorder_data = reorder_data.sort_values(
    "rupee_value_at_risk",
    ascending=False
)


# Display reorder information
st.dataframe(
    reorder_data[
        [
            "sku_id",
            "forecast_demand",
            "available_inventory",
            "stockout_shortfall_units",
            "rupee_value_at_risk",
            "recommended_action"
        ]
    ],
    width="stretch",
    hide_index=True
)


# ============================================================
# MARKDOWN / CLEAR LIST
# ============================================================

st.subheader("Markdown / Clear List")


# Keep only SKUs with overstock risk
markdown_data = display_data[
    display_data["risk_level"] == "Markdown/Clear"
].copy()


# Sort by excess inventory
markdown_data = markdown_data.sort_values(
    "overstock_excess_units",
    ascending=False
)


# Display markdown information
st.dataframe(
    markdown_data[
        [
            "sku_id",
            "forecast_demand",
            "available_inventory",
            "overstock_excess_units",
            "rupee_value_at_risk",
            "recommended_action"
        ]
    ],
    width="stretch",
    hide_index=True
)


# ============================================================
# DECISION GRID
# ============================================================

st.subheader("Inventory Risk Decision Grid")


# Prepare decision information
decision_grid = display_data[
    [
        "sku_id",
        "risk_level",
        "recommended_action",
        "stockout_shortfall_units",
        "overstock_excess_units",
        "rupee_value_at_risk"
    ]
].sort_values(
    "rupee_value_at_risk",
    ascending=False
)


# Display decision grid
st.dataframe(
    decision_grid,
    width="stretch",
    hide_index=True
)


# ============================================================
# VALUE AT RISK BY SKU
# ============================================================

st.subheader("Value at Risk by SKU")


# Select top 10 SKUs by financial risk
risk_value_chart = (
    display_data[
        [
            "sku_id",
            "rupee_value_at_risk"
        ]
    ]
    .sort_values(
        "rupee_value_at_risk",
        ascending=False
    )
    .head(10)
)


# Set SKU as chart index
risk_value_chart = risk_value_chart.set_index(
    "sku_id"
)


# Display financial risk chart
st.bar_chart(
    risk_value_chart[
        "rupee_value_at_risk"
    ]
)


# ============================================================
# SELECTED SKU DETAILS
# ============================================================

st.subheader("SKU Details")


if selected_sku != "All":

    # Get selected SKU details
    sku_detail = display_data[
        display_data["sku_id"] == selected_sku
    ].iloc[0]


    col1, col2, col3 = st.columns(3)


    with col1:

        # Selected SKU forecast demand
        st.metric(
            "Forecast Demand",
            f"{sku_detail['forecast_demand']:,.0f}"
        )


    with col2:

        # Selected SKU available inventory
        st.metric(
            "Available Inventory",
            f"{sku_detail['available_inventory']:,.0f}"
        )


    with col3:

        # Selected SKU financial risk
        st.metric(
            "12-Week Value at Risk",
            f"₹{sku_detail['rupee_value_at_risk']:,.0f}"
        )


    # Show selected SKU risk level
    st.write(
        "Risk Level:",
        sku_detail["risk_level"]
    )


    # Show recommended business action
    st.write(
        "Recommended Action:",
        sku_detail["recommended_action"]
    )

else:

    # Ask user to select a SKU
    st.info(
        "Select a specific SKU to view its detailed information."
    )


# ============================================================
# SELECTED SKU FORECAST TREND
# ============================================================

if selected_sku != "All":

    st.subheader("Selected SKU Forecast Trend")


    # Filter forecast data for selected SKU
    sku_forecast = forecast_data[
        forecast_data["sku_id"] == selected_sku
    ].copy()


    # Select actual and forecast columns
    sku_forecast = sku_forecast[
        [
            "week_start",
            "units_sold",
            "gb_prediction"
        ]
    ]


    # Set week as chart index
    sku_forecast = sku_forecast.set_index(
        "week_start"
    )


    # Display selected SKU trend
    st.line_chart(
        sku_forecast[
            [
                "units_sold",
                "gb_prediction"
            ]
        ]
    )

else:

    # Show message when all SKUs are selected
    st.info(
        "Select a specific SKU to view its detailed forecast trend."
    )


# ============================================================
# MODEL PERFORMANCE
# ============================================================

st.subheader("Model Performance")


# Final Gradient Boosting model WAPE
final_wape = 23.75


# Seasonal-naive baseline WAPE
baseline_wape = 33.71


col1, col2 = st.columns(2)


with col1:

    # Show final model WAPE
    st.metric(
        "Final Model WAPE",
        f"{final_wape:.2f}%"
    )


with col2:

    # Show baseline WAPE
    st.metric(
        "Seasonal Naive WAPE",
        f"{baseline_wape:.2f}%"
    )


# Explain WAPE
st.caption(
    "Lower WAPE indicates lower forecast error."
)

st.info(
    "Note: Risk KPIs and inventory coverage use the fixed "
    "12-week operational risk horizon. The date filter applies "
    "to forecast and uncertainty charts."
)


# ============================================================
# MODEL COMPARISON
# ============================================================

st.subheader("Model Comparison")


# Model performance results
model_comparison = pd.DataFrame({
    "Model": [
        "Seasonal Naive",
        "Random Forest",
        "Gradient Boosting"
    ],
    "WAPE": [
        33.71,
        25.28,
        24.14
    ]
})


# Display model comparison
st.bar_chart(
    model_comparison.set_index("Model")
)


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

st.subheader("Executive Summary")


# Calculate business indicators
total_skus = display_data[
    "sku_id"
].nunique()


reorder_count = (
    display_data["risk_level"]
    == "Reorder Now"
).sum()


total_risk_value = display_data[
    "rupee_value_at_risk"
].sum()


# Display executive summary
st.write(
    f"**SKUs analysed:** {total_skus}"
)


st.write(
    f"**SKUs requiring reorder:** {reorder_count}"
)


st.write(
    f"**Total value at risk:** ₹{total_risk_value:,.0f}"
)


st.write(
    "**Recommended focus:** Prioritize SKUs with the highest "
    "value at risk for inventory action."
)


# ============================================================
# DATA QUALITY & LIMITATIONS
# ============================================================

st.subheader("Download Filtered Risk Data")

download_data = display_data.copy()

csv_data = download_data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Risk Data as CSV",
    data=csv_data,
    file_name="foresight_risk_results.csv",
    mime="text/csv"
)

st.subheader("Data Quality & Limitations")


# Display important project limitations
st.info(
    """
    **Data notes**

    • Source data contains no missing values or duplicate SKU-date records.

    • Product categories are inconsistent across the source data, so
      category was not assigned to the SKU master table.

    • Lead time and reorder point were not available in the source data,
      so they were not fabricated.

    • Risk scoring uses available inventory and forecast demand over the
      selected forecast horizon.
    """
)

st.divider()

st.markdown("""
<div style="background: #eaf3ff; border: 1px solid #cfe2fb; border-radius: 12px; padding: 12px 16px; color: #23446f; font-size: 13px;">
    <b>ℹ️ Tip:</b> Use the sidebar filters to explore specific SKUs, risk levels, and product categories.
</div>
""", unsafe_allow_html=True)

st.caption("FORESIGHT | Demand Forecasting & Inventory Risk Dashboard")
st.caption("Built for inventory planning, forecast monitoring, and risk-based decision support.")