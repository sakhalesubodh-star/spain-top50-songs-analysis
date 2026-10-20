import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# ==========================================
# DATA LOADING
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR /"Spain_Top50_Analysis"/ "Data" / "processed"

LIFECYCLE_FILE = (
    DATA_DIR / "song_lifecycle_with_stages.csv"
)

@st.cache_data
def load_lifecycle_data(file_path):
    data = pd.read_csv(file_path)

    # Convert date columns to datetime
    for column in [
        "entry_date",
        "exit_date",
        "peak_date"
    ]:
        if column in data.columns:
            data[column] = pd.to_datetime(
                data[column],
                errors="coerce"
            )

    # Convert numerical columns safely
    for column in [
        "observations",
        "calendar_span_days",
        "peak_position",
        "time_to_peak_days"
    ]:
        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column],
                errors="coerce"
            )

    return data


if not LIFECYCLE_FILE.exists():
    st.error(
        f"Dataset not found: {LIFECYCLE_FILE}"
    )

    st.info(
        "Check that song_lifecycle_with_stages.csv "
        "exists inside data/processed."
    )

    st.stop()

songs = load_lifecycle_data(str(LIFECYCLE_FILE))

# Validate essential columns
required_columns = {
    "song",
    "entry_date",
    "exit_date",
    "observations",
    "peak_position"
}

missing_columns = required_columns - set(songs.columns)

if missing_columns:
    st.error(
        f"Missing required columns: {sorted(missing_columns)}"
    )
    st.stop()

st.success(
    f"Dataset loaded successfully: {len(songs):,} records"
)

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
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

/* Main application background */
.stApp {
    background-color: #0b0f19;
    color: #f1f5f9;
}

/* Main content area */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

/* Main heading */
.main-title {
    font-size: 36px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 5px;
}

/* Subtitle */
.subtitle {
    color: #94a3b8;
    font-size: 15px;
    margin-bottom: 25px;
}

/* KPI cards */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #171e2e, #111827);
    border: 1px solid #293449;
    padding: 20px;
    border-radius: 14px;
}

/* KPI labels */
div[data-testid="stMetricLabel"] {
    color: #94a3b8;
}

/* KPI values */
div[data-testid="stMetricValue"] {
    color: #ffffff;
    font-weight: 700;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #293449;
}

/* Section headings */
h2, h3 {
    color: #ffffff;
}

/* Divider */
hr {
    border-color: #293449;
}

/* Small footer */
.footer {
    color: #64748b;
    text-align: center;
    padding: 20px;
    font-size: 12px;
}
/* Main dashboard title */
h1 {
    font-size: 2.3rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
    padding-bottom: 10px;
}

/* Section headings */
h2 {
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    margin-top: 20px;
}

h3 {
    font-size: 1.15rem !important;
    font-weight: 600 !important;
}

/* KPI cards */
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.10);
    padding: 18px;
    border-radius: 12px;
}

/* KPI labels */
[data-testid="stMetricLabel"] {
    font-size: 0.9rem;
}

/* Rounded buttons */
.stButton > button,
.stDownloadButton > button {
    border-radius: 8px;
    font-weight: 600;
    padding: 8px 16px;
}

/* Sidebar spacing */
section[data-testid="stSidebar"] {
    padding-top: 20px;
}

/* Data tables */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
}

/* Improve divider appearance */
hr {
    margin-top: 28px;
    margin-bottom: 28px;
    opacity: 0.3;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="main-title">🎵 Spain Top 50 Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Song lifecycle intelligence | Playlist performance | Content analytics'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# ==========================================
# INTERACTIVE SIDEBAR FILTERS
# ==========================================

st.sidebar.title("🎛️ Dashboard Controls")
st.sidebar.markdown("### Analysis Filters")

filtered = songs.copy()

# Song search
search_text = st.sidebar.text_input(
    "🔎 Search song",
    placeholder="Enter song name..."
)

if search_text:
    filtered = filtered[
        filtered["song"].astype(str).str.contains(
            search_text,
            case=False,
            na=False
        )
    ]

# Date filter
valid_dates = songs["entry_date"].dropna()

if not valid_dates.empty:

    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()

    selected_dates = st.sidebar.date_input(
        "📅 Entry date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if (
        isinstance(selected_dates, (tuple, list))
        and len(selected_dates) == 2
    ):
        start_date, end_date = selected_dates

        filtered = filtered[
            filtered["entry_date"].dt.date.between(
                start_date,
                end_date
            )
        ]

# Lifecycle stage filter
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
        default=available_stages
    )

    filtered = filtered[
        filtered["lifecycle_stage"].isin(
            selected_stages
        )
    ]

st.sidebar.divider()

st.sidebar.caption(
    "All metrics and charts reflect the selected songs."
)

# ==========================================
# DYNAMIC KPI SECTION
# ==========================================

st.subheader("📊 Executive Overview")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

unique_songs = filtered["song"].nunique()

avg_observations = filtered[
    "observations"
].mean()

avg_best_rank = filtered[
    "peak_position"
].mean()

if "lifecycle_stage" in filtered.columns:
    lifecycle_categories = filtered[
        "lifecycle_stage"
    ].nunique()
else:
    lifecycle_categories = 0

kpi1.metric(
    "Unique Songs",
    f"{unique_songs:,}"
)

kpi2.metric(
    "Avg. Playlist Appearances",
    (
        f"{avg_observations:.1f}"
        if pd.notna(avg_observations)
        else "N/A"
    )
)

kpi3.metric(
    "Average Best Rank",
    (
        f"{avg_best_rank:.1f}"
        if pd.notna(avg_best_rank)
        else "N/A"
    )
)

kpi4.metric(
    "Lifecycle Categories",
    f"{lifecycle_categories}"
)

st.caption(
    f"Showing {len(filtered):,} song records "
    f"after applying the selected filters."
)

# ==========================================
# INTERACTIVE CHARTS
# ==========================================

import plotly.express as px

st.subheader("📈 Song Performance & Lifecycle")

left_chart, right_chart = st.columns(2)

with left_chart:

    st.markdown("#### Lifecycle Stage Distribution")

    if "lifecycle_stage" in filtered.columns:

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
            title="Distribution of Song Lifecycle Stages"
        )

        fig_stage.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig_stage,
            use_container_width=True
        )

    else:
        st.warning(
            "Lifecycle stage data is unavailable."
        )

with right_chart:

    st.markdown("#### Top 10 Songs")

    top_songs = filtered.nlargest(
        10,
        "observations"
    )

    if not top_songs.empty:

        fig_top = px.bar(
            top_songs.sort_values("observations"),
            x="observations",
            y="song",
            orientation="h",
            hover_data=[
                "peak_position",
                "calendar_span_days"
            ] if "calendar_span_days" in top_songs.columns
            else ["peak_position"],
            title="Top Songs by Playlist Appearances"
        )

        fig_top.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig_top,
            use_container_width=True
        )

    else:
        st.info(
            "No songs match the current filters."
        )
# -----------------------------------------
# SONG LIFECYCLE DETAILS
# -----------------------------------------

st.markdown("---")
st.header("🎵 Song Lifecycle Details")

st.write(
    "Explore individual songs and understand their "
    "playlist duration, peak position, and lifecycle stage."
)

# Select available columns
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
    col for col in preferred_columns
    if col in filtered.columns
]

# -----------------------------------------
# PLAYLIST CHURN ANALYSIS
# -----------------------------------------

st.markdown("---")
st.header("🔄 Playlist Churn Analysis")

st.write(
    "Analyze how songs enter, leave, and remain in the "
    "Spain Top 50 playlist across observed snapshots."
)

from pathlib import Path

CHURN_FILE = (
    Path(__file__).resolve().parent.parent
    /"Spain_Top50_Analysis"
    / "data"
    / "processed"
    / "daily_churn.csv"
)

if CHURN_FILE.exists():

    churn = pd.read_csv(CHURN_FILE)

    # Convert the date column
    if "date" in churn.columns:
        churn["date"] = pd.to_datetime(
            churn["date"], errors="coerce"
        )

    # Display available metrics
    metric_columns = [
        col for col in [
            "new_entries",
            "disappearances",
            "tracks_retained",
            "retention_rate_pct",
            "exit_rate_pct",
        ]
        if col in churn.columns
    ]

    if metric_columns:

        st.subheader("Playlist Changes Over Time")

        selected_metrics = st.multiselect(
            "Select metrics to display",
            options=metric_columns,
            default=[
                col for col in [
                    "new_entries",
                    "disappearances",
                ]
                if col in metric_columns
            ],
        )

        if selected_metrics:

            chart_data = churn.copy()

            if "date" in chart_data.columns:
                chart_data = chart_data.sort_values("date")

            st.line_chart(
                chart_data.set_index("date")[selected_metrics]
                if "date" in chart_data.columns
                else chart_data[selected_metrics]
            )

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
        )

    else:
        st.warning(
            "The churn file exists, but the expected metric "
            "columns were not found. Check its column names."
        )

else:
    st.warning(
        "daily_churn.csv was not found. Check that it exists "
        "inside data/processed."
    )

# Display the filtered lifecycle data
st.dataframe(
    filtered[display_columns],
    use_container_width=True,
    hide_index=True
)

# -----------------------------------------
# DOWNLOAD FILTERED DATA
# -----------------------------------------

st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=filtered[display_columns].to_csv(index=False).encode("utf-8"),
    file_name="filtered_song_lifecycle.csv",
    mime="text/csv",
)



# ==========================================
# FOOTER
# ==========================================

st.markdown(
    '<div class="footer">'
    'Spain Top 50 Song Lifecycle Analytics | '
    'Python • Streamlit • Plotly • Pandas'
    '</div>',
    unsafe_allow_html=True
)