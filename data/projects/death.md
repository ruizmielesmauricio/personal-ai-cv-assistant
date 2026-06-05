# Death Discography Dashboard

## Project Overview

The Death Discography Dashboard is an interactive analytics application built using Streamlit that explores the complete studio discography of the influential death metal band Death.

The project combines music metadata from multiple APIs and transforms it into a user-friendly dashboard for exploring albums, songs, tempo characteristics, popularity metrics, and listening trends.

This project was designed to demonstrate end-to-end data analytics skills including data collection, API integration, data cleaning, feature engineering, dashboard development, and deployment.

---

## Business Objective

The goal of the project was to create a fully interactive dashboard that allows users to:

- Explore Death's studio albums
- Analyze song tempo (BPM)
- Compare albums
- Identify the most popular tracks
- Investigate listener behaviour and streaming popularity

The project simulates a real-world analytics workflow where data from multiple sources must be combined and transformed into meaningful insights.

---

## Data Sources

The dashboard integrates data from multiple public APIs:

### Spotify API
Used to collect:

- Album information
- Track metadata
- Track duration
- Popularity scores

### Last.fm API
Used to collect:

- Listener counts
- Play counts
- Audience engagement metrics

### MusicBrainz / AcousticBrainz
Used to enrich songs with:

- BPM information
- Audio characteristics

---

## Methodology

### Data Collection

Data was extracted using Python API calls and merged into a unified dataset.

The workflow included:

1. Retrieve all official studio albums.
2. Retrieve every track from each album.
3. Collect popularity metrics.
4. Collect BPM data.
5. Merge datasets.
6. Validate and clean records.

---

### Data Cleaning

Several preprocessing steps were performed:

- Duplicate removal
- Missing value handling
- Type conversion
- Standardisation of album and track names
- BPM validation

---

### Feature Engineering

Additional metrics were created including:

- Track length in minutes
- Album release chronology
- Average BPM per album
- Most listened tracks
- Most popular tracks
- Fastest songs
- Slowest songs

---

## Dashboard Features

### Band Overview

Displays:

- Number of albums
- Number of tracks
- Average BPM
- Most popular track
- Fastest song
- Slowest song

---

### Album Timeline

Interactive visualization showing:

- Album release sequence
- Discography progression

---

### BPM Analysis

Users can:

- Explore BPM distributions
- Compare album tempo profiles
- Identify the fastest and slowest compositions

---

### Top Tracks Analysis

Displays:

- Most played tracks
- Most listened songs
- Popularity rankings

---

### Album Comparison Tool

Allows users to compare:

- Average BPM
- Track counts
- Popularity metrics
- Listener engagement

---

### Interactive Filtering

Users can dynamically filter data by:

- Album
- Song
- BPM ranges

---

## Technologies Used

- Python
- Pandas
- Streamlit
- Plotly
- Spotify API
- Last.fm API
- MusicBrainz API
- AcousticBrainz API

---

## Deployment

The dashboard was deployed using Streamlit Community Cloud, making it publicly accessible through a web browser without requiring local installation.

---

## Skills Demonstrated

This project demonstrates:

- Data Collection
- API Integration
- Data Cleaning
- Feature Engineering
- Data Visualisation
- Dashboard Development
- Streamlit Deployment
- Analytical Storytelling
- User Experience Design

---

## Outcome

The final solution transformed raw music metadata into an interactive analytics platform that allows users to explore over three decades of Death's discography through data-driven insights and visualisations.
