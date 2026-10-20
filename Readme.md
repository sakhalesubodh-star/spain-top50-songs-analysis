# Spain Top 50 Songs: Content Maturity, Release Lifecycle & Playlist Rotation Analysis

## Project Overview

This project analyzes songs appearing in the Spain Top 50 playlist to understand
their playlist lifecycle, content maturity, chart performance, and playlist
rotation patterns.

The analysis combines data cleaning, exploratory data analysis, lifecycle
metrics, playlist churn analysis, and an interactive Streamlit dashboard.

The goal is to turn raw playlist observations into actionable insights about
song longevity, peak chart positions, and changes in playlist composition.

## Business Problem

Music analysts and playlist managers need to understand how songs perform
after entering a popular playlist.

This project investigates questions such as:

- How long do songs remain visible in the observed playlist data?
- How quickly do songs reach their best recorded chart position?
- Which songs have the longest observed lifecycles?
- How frequently does the playlist composition change?
- What proportion of previously observed songs remain in subsequent snapshots?
- How can playlist lifecycle and rotation patterns be communicated through
  an interactive dashboard?

## Project Objectives

1. Clean and validate the playlist dataset.
2. Explore song performance and playlist trends.
3. Calculate song lifecycle metrics.
4. Categorize songs by lifecycle stage.
5. Measure playlist entries, disappearances, and retention.
6. Build an interactive dashboard for exploring the results.
7. Communicate findings through visualizations and business recommendations.

## Tools and Technologies

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- Jupyter Notebook
- Visual Studio Code
- Git and GitHub

## Methodology

### 1. Data Preparation

- Inspected the available dataset and its structure.
- Checked missing values and duplicate records.
- Validated relevant columns and data types.
- Converted date columns to appropriate datetime formats.
- Prepared the data for lifecycle and trend analysis.

### 2. Exploratory Data Analysis

Explored the available playlist observations to understand song performance,
playlist activity, and the distribution of lifecycle metrics.

### 3. Song Lifecycle Analysis

Calculated lifecycle metrics such as:

- First observed playlist date
- Last observed playlist date
- Number of observed appearances
- Best recorded chart position
- Calendar span between first and last appearances
- Time taken to reach the best recorded position

### 4. Lifecycle Classification

Songs were grouped into lifecycle stages using their observed appearance
counts. The classification thresholds should be interpreted according to the
rules implemented in the analysis notebook.

### 5. Playlist Churn Analysis

Compared consecutive observed playlist snapshots to calculate:

- New entries
- Disappearances
- Tracks retained
- Retention rate
- Exit rate

The results represent changes between available observations. They do not
necessarily identify the exact date a song entered or left the playlist.

### 6. Interactive Dashboard

Developed a Streamlit dashboard with:

- Key performance indicators
- Song search and available filters
- Lifecycle charts
- Song lifecycle details
- Playlist churn visualizations
- CSV download options

## Key Performance Indicators

The dashboard includes metrics such as:

- Number of unique songs in the filtered dataset
- Average observed appearances
- Average best recorded chart position
- Number of lifecycle stages represented
- Playlist entries and disappearances
- Playlist retention and exit rates, where available

Metric values depend on the dataset and filters selected.

## Business Value

The analysis can help music analysts and playlist managers:

- Understand observed song longevity.
- Identify songs with strong or sustained playlist presence.
- Examine playlist turnover and stability.
- Compare lifecycle patterns across songs.
- Explore performance patterns through interactive visualizations.

These findings describe patterns in the available data and should not be
interpreted as proof of why a song became popular or disappeared.

## Project Structure

```text
Spain_Top50_Analysis/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── dashboard/
│   └── app.py
├── README.md
└── requirements.txt
```

Adjust this structure to match the files actually included in your repository.

## How to Run the Dashboard

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Replace the placeholder with your actual repository URL.

### 2. Open the Project

```bash
cd Spain_Top50_Analysis
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the Dashboard

```bash
streamlit run dashboard/app.py
```

Ensure that the processed lifecycle and churn CSV files exist in the expected
data directory before launching the dashboard.

## Limitations

- Results depend on the available playlist snapshots.
- Missing observation dates can affect lifecycle and churn interpretation.
- Observed playlist duration is not necessarily the same as a song's complete
  lifespan on Spotify.
- Lifecycle categories depend on the selected classification thresholds.
- Correlation or observed patterns do not establish causation.

## Future Improvements

- Add artist-level comparisons.
- Analyze release age alongside playlist lifecycle.
- Add more detailed temporal trend analysis.
- Compare lifecycle patterns across artists and release types when the required
  fields are available.
- Deploy the dashboard online.
- Add automated data validation and reproducible analysis workflows.

## Author

Subodh Sakhale

Data Analytics Project