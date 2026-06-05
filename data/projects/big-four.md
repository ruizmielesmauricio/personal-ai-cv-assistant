# Big Four Thrash Metal Analytics Dashboard

## Project Overview

The Big Four Thrash Dashboard is an interactive business intelligence application that analyzes the discographies of the four most influential thrash metal bands:

- Metallica
- Megadeth
- Slayer
- Anthrax

The dashboard combines music metadata, listener statistics, popularity metrics, and BPM analysis to compare the evolution and characteristics of each band's catalogue.

The project was developed to showcase advanced data analytics, API integration, dashboard design, and deployment skills.

---

## Business Objective

The objective was to build a comparative analytics platform capable of answering questions such as:

- Which band has the fastest average songs?
- Which albums have the highest listener engagement?
- Which songs are the most popular?
- How do BPM profiles differ between bands?
- Which albums contain the fastest and slowest tracks?

The project demonstrates how multiple data sources can be combined to generate actionable insights and interactive visualisations.

---

## Data Sources

### Spotify API

Used to retrieve:

- Albums
- Tracks
- Track duration
- Popularity scores

### Last.fm API

Used to collect:

- Listener counts
- Play counts
- Community engagement metrics

### AcousticBrainz

Used to obtain:

- BPM measurements
- Audio analysis features

---

## Methodology

### Data Collection

A Python ETL workflow was created to:

1. Retrieve albums for all four bands.
2. Retrieve track information.
3. Collect popularity metrics.
4. Collect listener statistics.
5. Collect BPM information.
6. Merge all datasets.

---

### Data Cleaning

Data preparation included:

- Duplicate removal
- Missing value treatment
- Data type validation
- Album normalization
- BPM verification

---

### Feature Engineering

Several derived metrics were created:

- Track length (minutes)
- Average album BPM
- Average band BPM
- Most popular tracks
- Most listened tracks
- Fastest tracks
- Slowest tracks
- Album-level performance metrics

---

## Dashboard Features

### Band Overview

Displays key KPIs including:

- Total albums
- Total tracks
- Average BPM
- Most popular track
- Fastest track
- Slowest track

---

### Discography Analysis

Provides insights into:

- Album evolution
- Release timelines
- Catalogue growth

---

### BPM Analytics

Users can:

- Compare BPM distributions
- Explore tempo characteristics
- Identify musical trends

---

### Listener Analysis

Analyzes:

- Play counts
- Listener counts
- Audience engagement

---

### Album Comparison Tool

Allows side-by-side comparison of albums across:

- BPM
- Popularity
- Listener metrics
- Track counts

---

### Interactive Exploration

Users can dynamically filter:

- Bands
- Albums
- Tracks
- BPM ranges

---

## Technologies Used

- Python
- Pandas
- Streamlit
- Plotly
- Spotify API
- Last.fm API
- AcousticBrainz API

---

## Deployment

The dashboard was deployed using Streamlit Community Cloud and made publicly accessible through a web application.

---

## Skills Demonstrated

This project demonstrates:

- API Integration
- ETL Development
- Data Cleaning
- Feature Engineering
- Dashboard Design
- Interactive Data Visualisation
- Streamlit Development
- Deployment
- Data Storytelling

---

## Outcome

The project successfully transformed data from multiple music platforms into a unified analytics dashboard that enables detailed comparisons between the Big Four thrash metal bands. The dashboard provides users with interactive insights into musical characteristics, popularity trends, listener engagement, and discography evolution.
