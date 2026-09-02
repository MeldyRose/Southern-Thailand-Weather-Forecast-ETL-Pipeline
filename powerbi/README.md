# Power BI Dashboard — Southern Thailand Weather & Flood Risk

## Overview

This Power BI dashboard visualizes weather forecast data for Southern Thailand collected from the **Thai Meteorological Department (TMD)**.

The dashboard is designed to answer:

> **Where and when is Southern Thailand at higher flood risk based on forecast rainfall?**

It transforms the processed weather data from the ETL pipeline into an interactive dashboard for monitoring rainfall intensity, rainfall distribution, and prolonged rainy conditions across provinces and locations.

---

## Dashboard Objectives

The dashboard focuses on:

- Monitoring forecast rainfall across Southern Thailand
- Identifying provinces experiencing heavy rainfall
- Finding locations with the highest forecast rainfall
- Monitoring consecutive rainy days
- Comparing rainfall intensity across locations
- Observing rainfall trends over the forecast period
- Visualizing the geographical distribution of rainfall

---

## Dashboard Analysis

### 1. Date for Analysis

Allows users to select the forecast date being analyzed.

The dashboard visuals update based on the selected date to provide a focused view of rainfall conditions.

### 2. Total Rainfall

Shows the total forecast rainfall across the selected locations and date.

**Metric:** `SUM(rain)`

### 3. Provinces with Heavy Rainfall

Counts the number of provinces where forecast rainfall reaches the defined heavy-rainfall threshold.

This provides an overview of how widespread heavy rainfall conditions are.

### 4. Maximum Rainfall

Displays the highest forecast rainfall value within the selected analysis period.

**Metric:** `MAX(rain)`

This helps identify the most extreme rainfall location.

### 5. Maximum Rainfall Streak

Shows the longest consecutive period of rainy conditions.

A rainy day is classified based on the project's rainfall threshold.

This metric helps identify areas experiencing prolonged rainfall, which may increase flood-related concerns.

### 6. Top 5 Rainfall Locations by Province

Displays the locations with the highest forecast rainfall for each province.

This helps identify specific areas that may require closer attention rather than only looking at province-level averages.

### 7. Rainfall Intensity Distribution

Shows the number of locations belonging to each rainfall intensity category.

This provides an overview of how rainfall conditions are distributed across Southern Thailand.

### 8. Rainfall Trend

A line chart showing how total forecast rainfall changes over the selected forecast dates.

This helps identify increasing, decreasing, or persistent rainfall patterns.

### 9. Average Rainfall Map

Displays the geographical distribution of average forecast rainfall.

Locations are categorized by rainfall intensity to make areas with higher rainfall easier to identify geographically.

---

> Note: The dashboard displays forecast dates rather than the API extraction date. For example, if the API is called on 2 September 2026, the forecast data shown may begin on 3 September 2026 (but it is written as the current date for easy understanding), representing the weather forecast for the following day.