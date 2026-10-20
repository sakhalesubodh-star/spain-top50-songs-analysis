# Content Maturity, Release Lifecycle & Playlist Rotation Analysis of Spain Top 50 Songs

## Abstract

Music streaming playlists provide a useful source of information for studying
song visibility, chart performance, and changes in playlist composition.
This project examines observations from the Spain Top 50 playlist to explore
song lifecycle patterns and playlist rotation.

The analysis uses Python-based data preparation, exploratory data analysis,
lifecycle metrics, and comparisons between consecutive playlist snapshots.
An interactive dashboard developed with Streamlit presents the results
through summary metrics, visualizations, filters, and downloadable data.

The project demonstrates a reproducible approach to analyzing observed
playlist behavior. Its findings are limited to the available observations
and do not independently establish the causes of song popularity or
playlist inclusion.

**Keywords:** Music Analytics, Data Analytics, Playlist Rotation, Song
Lifecycle, Python, Streamlit, Data Visualization.

## 1. Introduction

Digital music platforms make it possible to examine patterns in music
visibility and playlist composition over time.

A popular playlist may contain songs with different performance patterns.
Some songs appear across many observations, while others are visible for
shorter periods. The playlist itself may also experience changes as new
songs appear and previously observed songs disappear.

Analyzing these patterns can help describe playlist stability, song
longevity, and recorded chart performance.

This project focuses on observations from the Spain Top 50 playlist and
uses data analytics techniques to investigate these characteristics.

## 2. Research Problem

The project addresses the challenge of converting raw playlist observations
into interpretable measures of song lifecycle and playlist rotation.

The main research questions are:

1. How long do songs remain present in the observed playlist data?
2. How many times is each song observed?
3. What is the best recorded chart position for each song?
4. How quickly does a song reach its best recorded position?
5. How does playlist composition change between consecutive snapshots?
6. What proportion of previously observed songs remains in the next snapshot?

## 3. Research Objectives

The objectives of this project are:

- To inspect, validate, and prepare the playlist dataset.
- To conduct exploratory data analysis.
- To calculate song lifecycle metrics.
- To classify songs into lifecycle stages using defined thresholds.
- To measure new entries, disappearances, and track retention.
- To create an interactive dashboard for exploring the results.
- To communicate findings and limitations clearly.

## 4. Data and Methodology

### 4.1 Data Source

The study uses a dataset containing observations associated with the
Spain Top 50 playlist.

The dataset's exact collection period, number of records, source URL,
and collection method should be documented using the original dataset
and its metadata.

The analysis should not assume that the observations represent every
playlist update.

### 4.2 Data Preparation

The preparation process includes inspecting columns and data types,
checking missing values and duplicate records, validating relevant fields,
and converting date columns to datetime format.

The cleaned data is then used for exploratory analysis and lifecycle
calculations.

All cleaning decisions should be documented so that the analysis can
be reproduced.

### 4.3 Song Lifecycle Metrics

The analysis calculates the following metrics where the required data
is available:

- **First observed date:** The earliest recorded observation for a song.
- **Last observed date:** The latest recorded observation for a song.
- **Observed appearances:** The number of recorded observations containing
  that song.
- **Best recorded position:** The smallest numerical chart position
  recorded for that song.
- **Calendar span:** The difference between the first and last observed
  dates.
- **Time to peak:** The time between first observation and the date of
  the best recorded chart position.

The calendar span is not necessarily the song's continuous playlist
duration. Gaps in observations and intermittent appearances can affect
its interpretation.

### 4.4 Lifecycle Classification

Songs are grouped into lifecycle stages based on their observed appearance
counts using the thresholds implemented in the analysis notebook.

The thresholds should be stated explicitly in the final report.

These categories are analytical classifications created for this project.
They should not be treated as official Spotify classifications.

### 4.5 Playlist Churn Analysis

Consecutive observed playlist snapshots are compared to calculate:

- New entries
- Disappearances
- Tracks retained
- Retention rate
- Exit rate

Retention rate is calculated as:

Retained tracks / Tracks in the previous snapshot × 100

Exit rate is calculated as:

Disappearing tracks / Tracks in the previous snapshot × 100

These rates require a valid previous snapshot and a nonzero number of
tracks in that snapshot.

When observation dates are separated by different time intervals, the
results represent changes between the available snapshots rather than
daily changes.

### 4.6 Visualization and Dashboard

Python, Pandas, NumPy, Plotly, and Streamlit are used in the analytical
workflow.

The dashboard presents summary metrics, lifecycle charts, searchable
song details, available filters, churn visualizations, and downloadable
CSV files.

## 5. Results

This section must be completed using the actual outputs from the analysis.

Report the following results:

1. Total number of unique songs analyzed.
2. Number of songs in each lifecycle stage.
3. Average observed appearances.
4. Average best recorded chart position.
5. Songs with the longest observed calendar spans.
6. Average time to peak, where meaningful.
7. New entries and disappearances across snapshots.
8. Retention and exit rates across snapshots.

For each result, explain what it means and identify any important limitations.

Do not insert estimates or fabricated values.

## 6. Discussion

The results can be used to describe differences in observed song longevity
and playlist turnover.

Songs with many recorded appearances have a sustained presence in the
available observations, but this does not automatically demonstrate
greater popularity across all listening platforms.

Similarly, a strong recorded chart position does not establish why a song
reached that position.

Playlist churn measures describe changes between snapshots. They do not
identify the reasons behind those changes.

The discussion should connect each conclusion to a verified result and
consider alternative explanations and data limitations.

## 7. Limitations

The study has several limitations:

- The analysis depends on the completeness and quality of the available data.
- The observation schedule may not capture every playlist update.
- First and last observed dates may differ from actual entry and removal dates.
- Lifecycle stages depend on the chosen thresholds.
- Missing data and irregular snapshot intervals may affect comparisons.
- The analysis alone cannot establish causal relationships.
- Results may not generalize to other countries, playlists, or time periods.

## 8. Conclusion

This project demonstrates how playlist observations can be analyzed using
data cleaning, exploratory analysis, lifecycle metrics, churn calculations,
and interactive visualization.

The workflow provides a structured way to investigate observed song
presence, recorded chart positions, and changes in playlist composition.

The final conclusions should be based on verified numerical results and
should acknowledge the limitations of the available observations.

## 9. Future Scope

Potential extensions include:

- Comparing songs by artist.
- Investigating release dates and release age, if available.
- Examining changes across longer periods.
- Comparing playlists from different countries.
- Incorporating additional metadata where its source and quality can be verified.
- Deploying the dashboard for wider access.
- Automating data validation and report generation.

## 10. References

List the actual dataset source, relevant documentation, and research
articles consulted during the project.

Include complete titles, authors or organizations, publication dates,
and working links where available.

Do not list sources that were not actually consulted.