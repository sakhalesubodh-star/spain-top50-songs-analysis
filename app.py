
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Spain Top 50 | Music Analytics",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# DATA LOADING
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent


def find_csv(filename):
    """Find a CSV in the repository root or common data folders."""
    possible_paths = [
        PROJECT_DIR / filename,
        PROJECT_DIR / "Data" / "processed" / filename,
        PROJECT_DIR / "data" / "processed" / filename,
        PROJECT_DIR / "Spain_Top50_Analysis" / "Data" / "processed" / filename,
    ]

    for path in possible_paths:
        if path.is_file():
            return path

    return possible_paths[0]


LIFECYCLE_FILE = find_csv("song_lifecycle_with_stages.csv")
CHURN_FILE = find_csv("daily_churn.csv")


@st.cache_data
def load_lifecycle_data(file_path):
    data = pd.read_csv(file_path)

    for column in ["entry_date", "exit_date", "peak_date"]:
        if column in data.columns:
            data[column] = pd.to_datetime(
                data[column], errors="coerce"
            )

    for column in [
        "observations",
        "calendar_span_days",
        "peak_position",
        "time_to_peak_days",
    ]:
        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column], errors="coerce"
            )

    return data


@st.cache_data
def load_churn_data(file_path):
    data = pd.read_csv(file_path)

    if "date" in data.columns:
        data["date"] = pd.to_datetime(
            data["date"], errors="coerce"
        )

    for column in [
        "days_between_snapshots",
        "new_entries",
        "disappearances",
        "tracks_retained",
        "retention_rate_pct",
        "exit_rate_pct",
    ]:
        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column], errors="coerce"
            )

    return data


if not LIFECYCLE_FILE.is_file():
    st.error("Lifecycle dataset not found.")
    st.write("Expected file:", str(LIFECYCLE_FILE))
    st.info(
        "Upload song_lifecycle_with_stages.csv to the same "
        "GitHub directory as app.py, or place it inside "
        "Data/processed or data/processed."
    )
    st.stop()

songs = load_lifecycle_data(str(LIFECYCLE_FILE))

required_columns = {
    "song",
    "entry_date",
    "exit_date",
    "observations",
    "peak_position",
}

missing_columns = required_columns - set(songs.columns)

if missing_columns:
    st.error(
        f"Missing required columns: {sorted(missing_columns)}"
    )
    st.stop()

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #0b0f19;
    color: #f1f5f9;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

.main-title {
    font-size: 36px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 5px;
}

.subtitle {
    color: #94a3b8;
    font-size: 15px;
    margin-bottom: 25px;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #171e2e, #111827);
    border: 1px solid #293449;
    padding: 18px;
    border-radius: 14px;
}

[data-testid="stMetricLabel"] {
    color: #94a3b8;
    font-size: 0.9rem;
}

[data-testid="stMetricValue"] {
    color: #ffffff;
    font-weight: 700;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #293449;
    padding-top: 20px;
}

h1 {
    font-size: 2.3rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
}

h2 {
    font-size: 1.6rem !important;
    font-weight: 700 !important;
}

h3 {
    font-size: 1.15rem !important;
    font-weight: 600 !important;
}

hr {
    border-color: #293449;
    margin-top: 28px;
    margin-bottom: 28px;
    opacity: 0.4;
}

.stButton > button,
.stDownloadButton > button {
    border-radius: 8px;
    font-weight: 600;
    padding: 8px 16px;
}

[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
}

.footer {
    color: #64748b;
    text-align: center;
    padding: 20px;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="main-title">🎵 Spain Top 50 Analytics</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'Song lifecycle intelligence | Playlist performance | Content analytics'
    '</div>',
    unsafe_allow_html=True,
)

st.divider()

st.success(f"Lifecycle dataset loaded: {len(songs):,} records")

# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.title("🎛️ Dashboard Controls")
st.sidebar.markdown("### Analysis Filters")

filtered = songs.copy()

search_text = st.sidebar.text_input(
    "🔎 Search song",
    placeholder="Enter song name...",
)

if search_text:
    filtered = filtered[
        filtered["song"].astype(str).str.contains(
            search_text, case=False, na=False
        )
    ]

valid_dates = songs["entry_date"].dropna()

if not valid_dates.empty:
    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()

    selected_dates = st.sidebar.date_input(
        "📅 Entry date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
        start_date, end_date = selected_dates

        filtered = filtered[
            filtered["entry_date"].dt.date.between(
                start_date, end_date
            )
        ]

if "lifecycle_stage" in songs.columns:
    available_stages = sorted(
        songs["lifecycle_stage"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_stages = st.sidebar.multiselect(
        "🎵 Lifecycle Stage",
        options=available_stages,
        default=available_stages,
    )

    filtered = filtered[
        filtered["lifecycle_stage"].isin(selected_stages)
    ]

st.sidebar.divider()
st.sidebar.caption(
    "All metrics and charts reflect the selected songs."
)

# ==========================================
# EXECUTIVE OVERVIEW
# ==========================================

st.subheader("📊 Executive Overview")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

unique_songs = filtered["song"].nunique()
avg_observations = filtered["observations"].mean()
avg_best_rank = filtered["peak_position"].mean()

lifecycle_categories = (
    filtered["lifecycle_stage"].nunique()
    if "lifecycle_stage" in filtered.columns
    else 0
)

kpi1.metric("Unique Songs", f"{unique_songs:,}")

kpi2.metric(
    "Avg. Playlist Appearances",
    f"{avg_observations:.1f}"
    if pd.notna(avg_observations)
    else "N/A",
)

kpi3.metric(
    "Average Best Rank",
    f"{avg_best_rank:.1f}"
    if pd.notna(avg_best_rank)
    else "N/A",
)

kpi4.metric("Lifecycle Categories", f"{lifecycle_categories}")

st.caption(
    f"Showing {len(filtered):,} song records after applying filters."
)

# ==========================================
# PERFORMANCE & LIFECYCLE CHARTS
# ==========================================

st.subheader("📈 Song Performance & Lifecycle")

left_chart, right_chart = st.columns(2)

with left_chart:
    st.markdown("#### Lifecycle Stage Distribution")

    if "lifecycle_stage" in filtered.columns and not filtered.empty:
        stage_counts = (
            filtered["lifecycle_stage"]
            .value_counts()
            .rename_axis("Lifecycle Stage")
            .reset_index(name="Songs")
        )

        fig_stage = px.pie(
            stage_counts,
            names="Lifecycle Stage",
            values="Songs",
            hole=0.55,
            title="Distribution of Song Lifecycle Stages",
        )

        fig_stage.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )

        st.plotly_chart(fig_stage, use_container_width=True)
    else:
        st.info("No lifecycle stage data matches the selected filters.")

with right_chart:
    st.markdown("#### Top 10 Songs")

    top_songs = filtered.dropna(
        subset=["observations"]
    ).nlargest(10, "observations")

    if not top_songs.empty:
        hover_columns = [
            col for col in [
                "peak_position",
                "calendar_span_days",
                "lifecycle_stage",
            ]
            if col in top_songs.columns
        ]

        fig_top = px.bar(
            top_songs.sort_values("observations"),
            x="observations",
            y="song",
            orientation="h",
            hover_data=hover_columns,
            title="Top Songs by Playlist Appearances",
        )

        fig_top.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )

        st.plotly_chart(fig_top, use_container_width=True)
    else:
        st.info("No songs match the current filters.")

# ==========================================
# SONG LIFECYCLE DETAILS
# ==========================================

st.markdown("---")
st.header("🎵 Song Lifecycle Details")

st.write(
    "Explore individual songs and understand their playlist duration, "
    "peak position, and lifecycle stage."
)

preferred_columns = [
    "song",
    "artist",
    "entry_date",
    "exit_date",
    "observations",
    "peak_position",
    "calendar_span_days",
    "time_to_peak_days",
    "lifecycle_stage",
]

display_columns = [
    column for column in preferred_columns
    if column in filtered.columns
]

if filtered.empty:
    st.info("No song records match the current filters.")
else:
    st.dataframe(
        filtered[display_columns],
        use_container_width=True,
        hide_index=True,
    )

st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=filtered[display_columns].to_csv(index=False).encode("utf-8"),
    file_name="filtered_song_lifecycle.csv",
    mime="text/csv",
    key="download_lifecycle",
)

# ==========================================
# PLAYLIST CHURN ANALYSIS
# ==========================================

st.markdown("---")
st.header("🔄 Playlist Churn Analysis")

st.write(
    "Analyze how songs enter, leave, and remain in the "
    "Spain Top 50 playlist across observed snapshots."
)

if not CHURN_FILE.is_file():
    st.warning(
        f"Churn dataset not found: {CHURN_FILE}. "
        "Upload daily_churn.csv to the same directory as app.py "
        "or place it inside Data/processed or data/processed."
    )
else:
    churn = load_churn_data(str(CHURN_FILE))

    st.success(f"Churn dataset loaded: {len(churn):,} records")

    metric_columns = [
        column for column in [
            "new_entries",
            "disappearances",
            "tracks_retained",
            "retention_rate_pct",
            "exit_rate_pct",
        ]
        if column in churn.columns
    ]

    # Churn KPI cards
    churn_kpis = [
        ("Total New Entries", "new_entries", "sum"),
        ("Total Disappearances", "disappearances", "sum"),
        ("Average Retention Rate", "retention_rate_pct", "mean"),
        ("Average Exit Rate", "exit_rate_pct", "mean"),
    ]

    available_kpis = [
        item for item in churn_kpis
        if item[1] in churn.columns
    ]

    if available_kpis:
        churn_cols = st.columns(len(available_kpis))

        for col, (label, column, operation) in zip(
            churn_cols, available_kpis
        ):
            values = churn[column].dropna()

            if values.empty:
                display_value = "N/A"
            elif operation == "sum":
                display_value = f"{values.sum():,.0f}"
            else:
                display_value = f"{values.mean():.2f}%"

            col.metric(label, display_value)

    if metric_columns:
        st.subheader("Playlist Changes Over Time")

        default_metrics = [
            column for column in [
                "new_entries",
                "disappearances",
            ]
            if column in metric_columns
        ]

        selected_metrics = st.multiselect(
            "Select metrics to display",
            options=metric_columns,
            default=default_metrics,
            key="churn_metrics",
        )

        if selected_metrics:
            chart_data = churn.copy()

            if "date" in chart_data.columns:
                chart_data = chart_data.dropna(
                    subset=["date"]
                ).sort_values("date")

                if not chart_data.empty:
                    fig_churn = px.line(
                        chart_data,
                        x="date",
                        y=selected_metrics,
                        markers=True,
                        title="Playlist Churn Metrics Over Time",
                    )

                    fig_churn.update_layout(
                        template="plotly_dark",
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        legend_title_text="Metric",
                    )

                    st.plotly_chart(
                        fig_churn,
                        use_container_width=True,
                    )
                else:
                    st.info("No valid dates are available for the churn chart.")
            else:
                st.warning("The churn dataset does not contain a date column.")

    st.subheader("Snapshot-by-Snapshot Results")

    st.dataframe(
        churn,
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        label="📥 Download Playlist Churn Data",
        data=churn.to_csv(index=False).encode("utf-8"),
        file_name="playlist_churn_analysis.csv",
        mime="text/csv",
        key="download_churn",
    )

# ==========================================
# FOOTER
# ==========================================

st.markdown(
    '<div class="footer">'
    'Spain Top 50 Song Lifecycle Analytics | '
    'Python • Streamlit • Plotly • Pandas'
    '</div>',
    unsafe_allow_html=True,
)
