
# Death Discography Dashboard

<img width="2852" height="1734" alt="image" src="https://github.com/user-attachments/assets/25eb75ba-275a-4159-a942-f9ab3dc74d12" />


## [Dashboard](https://deathdiscography-h9p46woir6f86utjcw2ikh.streamlit.app)

An interactive Streamlit dashboard analyzing the discography of the band Death.

## Features

- Official studio album exploration
- Track-level analytics
- BPM analysis
- Listener and playcount metrics from Last.fm
- Album comparison tool
- Interactive filtering
- Album artwork visualization

## Dashboard Sections
- Band overview
- Album timeline
- BPM distribution
- Top tracks
- Album comparison
- Track explorer


## Data Sources

- Spotify API
- Last.fm API
- MusicBrainz / AcousticBrainz

## Tech Stack

- Python
- Pandas
- Streamlit
- Plotly
# Death Discography Dashboard

## Project Summary

Built an interactive analytics dashboard exploring the complete studio discography of the band Death. The project combines music metadata, popularity metrics, and musical characteristics to allow fans to explore albums and tracks through an interactive web application.

## Business Problem

Music data is distributed across multiple platforms and difficult to analyse collectively. The objective was to consolidate multiple music datasets into a single analytical platform that allows users to compare albums, tracks, popularity, and musical characteristics.

## Data Sources

- Spotify API
- Last.fm API
- MusicBrainz
- AcousticBrainz

## Data Engineering

### Extraction

Collected album and track information from MusicBrainz and enriched records using Last.fm and Spotify-based sources.

### Transformation

- Removed duplicate tracks
- Filtered non-studio releases
- Standardised popularity metrics
- Joined datasets from multiple APIs

### Loading

Created a consolidated dataset used by Streamlit and Plotly visualisations.

## Technologies

- Python
- Pandas
- Streamlit
- Plotly

## Dashboard Features

- Album exploration
- Track-level analysis
- BPM analysis
- Listener trends
- Popularity comparison

## Key Challenges

- Matching tracks across APIs
- Inconsistent naming conventions
- Missing BPM information

## Results

- Interactive web application deployed publicly
- Unified music dataset
- Track-level and album-level analytics

## Skills Demonstrated

- API Integration
- Data Cleaning
- ETL Pipelines
- Dashboard Development
- Data Visualisation
- Python Development

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
## Author
**_Mauricio Ruiz_**


