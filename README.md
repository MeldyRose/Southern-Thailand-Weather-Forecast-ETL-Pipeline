# Southern Thailand Weather Forecast ETL Pipeline

Southern Thailand Weather Forecast ETL Pipeline is an individual project for learning data engineering and building ETL pipeline to collect, transform, and analyze weather data from Southern Thailand.

## Project Overview

This project builds an ETL pipeline that:
- Extracts weather forecast data from the TMD API
- Stores the original API response as raw JSON
- Transforms and cleans the data using Python and Pandas
- Stores processed data for further analysis
- Loads structured data into PostgreSQL
- Provide data for weather and potential flood-risk analysis

## Tech Stack

- Python
- Pandas
- REST API
- PostgreSQL
- Docker
- Apache Airflow
- Power BI

## Prerequisites

- Python
- PostgreSQL
- Git

## Setup

### 1. Clone the repository

```
    git clone https://github.com/MeldyRose/Southern-Thailand-Weather-Forecast-ETL-Pipeline.git
    cd Southern-Thailand-Weather-Forecast-ETL-Pipeline
```

### 2. Create a virtual environment

```
    python -m venv .venv
```

Activate it:

**Windows**
```
    .venv\Scripts\activate
```

### 3. Install dependencies

```
    pip install -r requirements.txt
```    

### 4. Configure environment variables

Create a `.env` file:
```
    API_KEY = your_api_key
```  

### 5. Run the pipeline

Currently, it uses main.py as orchestration but soon later it will use Airflow.
```
    python -m src.main
```  

## ETL Pipeline

> In progress

## Project Structure

> In progress

## Data Source

- Thai Meteorological Department(TMD) API

## Analysis

The processed weather data will be used to explore:
- 

## Future Improvements

- Add automated orchestration with Apache Airflow
- Containerize the pipeline with Docker
- Add data quality tests
- Build a Power BI dashboard

