"""Streamlit dashboard for the 10 Academy Solar Challenge."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from utils import COUNTRY_FILES, load_available_countries, summarize_sites  # noqa: E402

st.set_page_config(
    page_title="Solar Data Discovery | 10 Academy",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("☀️ Solar Data Discovery")
st.caption("Interactive comparison of solar irradiance and environmental measurements in Benin, Sierra Leone, and Togo.")

@st.cache_data(show_spinner="Loading local solar datasets…")
def get_data(countries: tuple[str, ...], refresh_token: int = 0):
    # refresh_token makes it possible to invalidate cached data using the Refresh button.
    del refresh_token
    return load_available_countries(countries)

with st.sidebar:
    st.header("Dashboard controls")
    chosen = st.multiselect(
        "Select countries",
        options=list(COUNTRY_FILES),
        default=list(COUNTRY_FILES),
        help="Choose one or more country datasets to include in the charts and site summary.",
    )
    metric_options = ["GHI", "DNI", "DHI"]
    metric = st.selectbox("Irradiance metric", metric_options, index=0)
    st.caption("Irradiance is measured in W/m². Environmental fields use their dataset units.")
    if st.button("Refresh data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

if not chosen:
    st.info("Select at least one country in the sidebar to view the dashboard.")
    st.stop()

with st.spinner("Preparing data for the selected countries…"):
    data, source_paths, load_errors = get_data(tuple(chosen))

if load_errors:
    st.warning("Some selected datasets could not be loaded. Check the file locations shown below.")
    for message in load_errors:
        st.code(message)

if data.empty:
    st.error("No datasets were loaded. Add the CSV files to data/raw/ or cleaned files to data/processed/, then refresh.")
    st.markdown("**Expected raw files**")
    for country in chosen:
        st.code(f"data/raw/{COUNTRY_FILES[country]}")
    st.stop()

# Date filter is available when Timestamp exists.
if "Timestamp" in data.columns and data["Timestamp"].notna().any():
    valid_dates = data["Timestamp"].dropna()
    min_date, max_date = valid_dates.min().date(), valid_dates.max().date()
    with st.sidebar:
        selected_dates = st.date_input(
            "Date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            help="Filter the charts and summary to the selected date range.",
        )
    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
        data = data[data["Timestamp"].dt.date.between(start_date, end_date)]

if data.empty:
    st.warning("No records fall within the selected date range. Choose a wider date range.")
    st.stop()

# Metric cards
metric_series = pd.to_numeric(data.get(metric, pd.Series(dtype=float)), errors="coerce")
valid_metric = metric_series.dropna()
mean_metric = float(valid_metric.mean()) if not valid_metric.empty else float("nan")
median_metric = float(valid_metric.median()) if not valid_metric.empty else float("nan")
country_count = data["Country"].nunique()
record_count = len(data)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Countries selected", f"{country_count}")
k2.metric(f"Mean {metric}", f"{mean_metric:,.2f} W/m²" if pd.notna(mean_metric) else "N/A")
k3.metric(f"Median {metric}", f"{median_metric:,.2f} W/m²" if pd.notna(median_metric) else "N/A")
k4.metric("Records in filter", f"{record_count:,}")

st.divider()
left, right = st.columns((1.2, 1))

with left:
    st.subheader(f"{metric} distribution by country")
    if metric not in data.columns:
        st.warning(f"The selected metric '{metric}' is not available in the loaded files.")
    else:
        plot_data = data[["Country", metric]].copy()
        plot_data[metric] = pd.to_numeric(plot_data[metric], errors="coerce")
        plot_data = plot_data.dropna()
        # Boxplots remain responsive by limiting each country to a reproducible sample.
        if not plot_data.empty:
            samples = []
            for _, group in plot_data.groupby("Country", sort=False):
                samples.append(group.sample(n=min(len(group), 12000), random_state=42))
            plot_data = pd.concat(samples, ignore_index=True) if samples else plot_data
        if plot_data.empty:
            st.info("No numeric values are available for this metric in the selected date range.")
        else:
            fig = px.box(
                plot_data,
                x="Country",
                y=metric,
                color="Country",
                points=False,
                title=f"Distribution of {metric} (sampled for display)",
                labels={metric: f"{metric} (W/m²)", "Country": "Country"},
            )
            fig.update_layout(showlegend=False, margin=dict(l=10, r=10, t=55, b=10))
            st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader(f"Average {metric} by country")
    if metric in data.columns:
        mean_by_country = data.groupby("Country")[metric].mean(numeric_only=True).reset_index()
        mean_by_country = mean_by_country.sort_values(metric, ascending=False)
        fig = px.bar(
            mean_by_country,
            x="Country",
            y=metric,
            color="Country",
            text_auto=".2f",
            title=f"Mean {metric} (W/m²)",
            labels={metric: f"Mean {metric} (W/m²)"},
        )
        fig.update_layout(showlegend=False, margin=dict(l=10, r=10, t=55, b=10))
        st.plotly_chart(fig, use_container_width=True)

st.subheader("Solar irradiance over time")
if "Timestamp" in data.columns and metric in data.columns:
    time_data = data[["Timestamp", "Country", metric]].copy()
    time_data[metric] = pd.to_numeric(time_data[metric], errors="coerce")
    time_data = time_data.dropna(subset=["Timestamp", metric])
    if not time_data.empty:
        # Aggregate minute-level records to daily averages to keep the interactive chart lightweight.
        time_data["Date"] = time_data["Timestamp"].dt.floor("D")
        daily = time_data.groupby(["Country", "Date"], as_index=False)[metric].mean()
        trend = px.line(
            daily,
            x="Date",
            y=metric,
            color="Country",
            title=f"Daily mean {metric}",
            labels={metric: f"Daily mean {metric} (W/m²)", "Date": "Date"},
        )
        trend.update_layout(hovermode="x unified", margin=dict(l=10, r=10, t=55, b=10))
        st.plotly_chart(trend, use_container_width=True)
    else:
        st.info("Timestamp or numeric irradiance values are unavailable for the trend chart.")
else:
    st.info("A Timestamp column and numeric irradiance field are needed for the time-series chart.")

st.subheader("Top-performing country / measurement sites")
st.caption(
    "The supplied files contain one named measurement station per country, not multiple regions within each country. "
    "This table therefore ranks the available country-level stations; it cannot identify top regions inside a country. "
    "Values reflect the current country and date filters."
)
site_summary = summarize_sites(data)
if not site_summary.empty:
    pretty = site_summary.copy()
    for col in ["GHI", "DNI", "DHI", "Tamb", "RH", "WS", "WSgust"]:
        if col in pretty.columns:
            pretty[col] = pretty[col].round(2)
    st.dataframe(pretty, use_container_width=True, hide_index=True)
else:
    st.info("No summary fields are available for the selected data.")

with st.expander("Data sources and quality notes"):
    st.markdown("**Loaded files**")
    for country, path in source_paths.items():
        st.write(f"- **{country}:** `{path}`")
    st.markdown(
        "- The app reads local CSV files and does not include the datasets in the source package.\n"
        "- It prefers `data/processed/<country>_clean.csv` when present; otherwise it reads the matching source CSV in `data/raw/`.\n"
        "- The supplied datasets have a `Comments` column that is entirely missing in the reported profiling.\n"
        "- Mean irradiance includes night-time observations unless you narrow the date range; interpret country comparisons alongside the EDA findings."
    )

st.caption("10 Academy · Solar Challenge · Interactive dashboard")
