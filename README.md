# Southern Thailand Weather Forecast ETL Pipeline

Southern Thailand Weather Forecast ETL Pipeline is an individual project for learning data engineering and building an ETL pipeline to collect, transform, and analyze weather data from Southern Thailand.

## Project Overview

This project builds an ETL pipeline that:
- Extracts weather forecast data from the TMD API
- Stores the original API response as raw JSON
- Transforms and cleans the data using Python and Pandas
- Stores processed data for further analysis
- Loads structured data into PostgreSQL
- Provides data for weather and potential flood-risk analysis

## Tech Stack

- Python
- Pandas
- REST API
- PostgreSQL
- Docker
- Apache Airflow
- Power BI

## Prerequisites

- Python 3.12+
- PostgreSQL 16+
- Git
> I personally developed/tested on Python 3.14.6 and PostgreSQL 18.4

## Setup

### 1. Clone the repository

```bash
    git clone https://github.com/MeldyRose/Southern-Thailand-Weather-Forecast-ETL-Pipeline.git
    cd Southern-Thailand-Weather-Forecast-ETL-Pipeline
```

### 2. Create a virtual environment

```bash
    python -m venv .venv
```

Activate it:

**Windows**
```bash
    .venv\Scripts\activate
```

### 3. Install dependencies

```bash
    pip install -r requirements.txt
```    

### 4. Configure environment variables

Create a `.env` file:
```bash
    API_KEY=your_api_key
    DATABASE_URL=your_database_url
```  
> Never commit your `.env` file or API key to Git.

### 5. Run the pipeline

The pipeline can be run in two ways:

1. **Airflow + Docker** — recommended for scheduled orchestration
2. **Python `main.py`** — fallback option for running the ETL manually

#### 5.1 Set Up Airflow and Docker

##### 5.1.1 Download Airflow and Docker

Before running the pipeline with Airflow, install Docker Desktop and download the official Airflow Docker Compose setup.

- **Docker Desktop:** https://www.docker.com/products/docker-desktop/
- **Apache Airflow:** https://airflow.apache.org/docs/apache-airflow/stable/start.html
- **Apache Airflow Docker Setup:** https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

Make sure Docker Desktop is running before continuing.

Create a separate folder for the Airflow environment:

```bash
mkdir airflow-docker
cd airflow-docker
```

Download the official `docker-compose.yaml` file from the Airflow documentation and place it inside this folder.

##### 5.1.2 Set Up Airflow in Docker

Create the required Airflow directories and place the project's DAG inside the `dags` folder:
> or use already have the directory.

```text
airflow-docker/
├── docker-compose.yaml
├── dags/
│   └── pipeline.py
├── logs/
├── config/
└── plugins/
```

The `pipeline.py` DAG orchestrates the Weather ETL workflow:

```text
Extract → Transform → Load
```

Update the `volumes` section in `docker-compose.yaml` so the Airflow container can access the project's `src/` and `data/` directories:

```bash
volumes:
  - ${AIRFLOW_PROJ_DIR:-.}/dags:/opt/airflow/dags
  - <PROJECT_PATH>/src:/opt/airflow/src
  - <PROJECT_PATH>/data:/opt/airflow/data
```

Replace `<PROJECT_PATH>` with the local path to the cloned Weather ETL project.

Initialize Airflow:

```bash
docker compose up airflow-init
```

After initialization is complete, start Airflow:

```bash
docker compose up -d
```

Check that the Airflow containers are running:

```bash
docker compose ps
```

Open the Airflow web interface:

```text
http://localhost:8080
```

#### 5.2 Important Configuration

Before running the DAG, make sure the following configuration is correct in `docker-compose.yaml`.

##### 5.2.1 Airflow Username and Password

Check the Airflow username and password configured in the Docker Compose file.

Use these credentials to log in to:

```text
http://localhost:8080
```

Do not commit personal or sensitive passwords to GitHub.

##### 5.2.2 PostgreSQL Database URL

The Airflow container needs to connect to the PostgreSQL database used by the Weather ETL project.

Update the database URL in `docker-compose.yaml`:

```yaml
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://<POSTGRES_USER>:<POSTGRES_PASSWORD>@host.docker.internal:5432/<POSTGRES_DATABASE>
```

Replace:

```text
<POSTGRES_USER>      → PostgreSQL username
<POSTGRES_PASSWORD>  → PostgreSQL password
<POSTGRES_DATABASE>  → PostgreSQL database name
```

Use `host.docker.internal` as the host when PostgreSQL is running on the local machine outside Docker.

> **Important:** The database name is the PostgreSQL database name, not a table name or view name.

##### 5.2.3 Run the Weather ETL DAG

After Airflow is running, open:

```text
http://localhost:8080
```

Find the DAG:

```text
southern_thailand_weather_forecast_etl_pipeline
```

Enable/unpause the DAG and trigger a run.

The tasks will run in the following order:

```text
Extract → Transform → Load
```

After a successful run, the weather data will be loaded into PostgreSQL.

#### 5.2.4 Stop Airflow

When finished, stop the Airflow containers:

```bash
docker compose down
```

To start Airflow again:

```bash
docker compose up -d
```

#### 5.3 Run the Pipeline Without Airflow

If Airflow or Docker is unavailable, the ETL pipeline can still be run directly with Python.

From the project root:

```bash
python -m src.main
```

This runs the core ETL workflow:

```text
Extract → Transform → Load
```

This option is mainly intended for development, testing, and debugging.

## ETL Pipeline

![Architecture for ETL Pipeline](ETL_Architecture.png)

## Project Structure
```
Southern-Thailand-Weather-Forecast-ETL-Pipeline/
│
├── config/
│   └── airflow.cfg
│
├── dags/
│   └── pipeline.py
│
├── data/
│   ├── raw/
│   └── processed/    
│
├── notebook/
│   └── weather_eda.ipynb
│
├── plugins/
│
├── powerbi/
│   ├── README.md
│   └── Weather_Forecast_Analysis_20260902.png
│
├── sql/
│   ├── 01_weather_risk_views.sql
│   ├── 02_rainfall_accumulation.sql
│   ├── 03_rainfall_streaks.sql
│   └── 04_rainfall_saved_streaks.sql
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── extraction.py
│   ├── load.py
│   ├── main.py
│   └── transformation.py
│
├── tests/
│   ├── test_extraction.py
│   └── test_main.py
│
├── .env.example
├── .gitignore
├── docker-compose.yaml
├── ETL_Architecture.png
├── LICENSE
├── README.md
└── requirements.txt
```

## Data Source

- Thai Meteorological Department(TMD) API

## Data Dictionary

The processed weather data will be used to explore:

- tc = temperature in Celsius
- tc_max = maximum temperature in Celsius
- tc_min = minimum temperature in Celsius
- rain = rainfall in millimeters
- rh = relative humidity in percentage
- slp = sea level pressure in hPa
- ws10m = wind speed at 10 meters in meters per second
- wd10m = wind direction at 10 meters in degrees
- cloudlow = low cloud cover in percentage
- cloudmed = medium cloud cover in percentage
- cloudhigh = high cloud cover in percentage
- cond = weather condition
    - 1 = ท้องฟ้าแจ่มใส (Clear)
    - 2 = มีเมฆบางส่วน (Partly cloudy)
    - 3 = เมฆเป็นส่วนมาก (Cloudy)
    - 4 = มีเมฆมาก (Overcast)
    - 5 = ฝนตกเล็กน้อย (Light rain)
    - 6 = ฝนปานกลาง (Moderate rain)
    - 7 = ฝนตกหนัก (Heavy rain)
    - 8 = ฝนฟ้าคะนอง (Thunderstorm)
    - 9 = อากาศหนาวจัด (Very cold)
    - 10 = อากาศหนาว (Cold)
    - 11 = อากาศเย็น (Cool)
    - 12 = อากาศร้อนจัด (Very hot)
     
## Analysis

The data produced by the ETL pipeline is structured and stored in PostgreSQL so that it can be used for different types of analysis and downstream applications.

For this project, the processed weather data is used to analyze **forecast rainfall and potential flood-risk indicators in Southern Thailand**. SQL views are created to transform the structured weather data into analytical datasets for the current use case.

Although the analysis focuses on rainfall and flood-risk indicators, the ETL pipeline is designed to produce reusable weather data that can support other analytical tasks in the future.

### Current Analysis

The current analysis focuses on the following areas:

#### 1. Rainfall Risk Classification

Rainfall values are classified into different intensity or risk levels to identify locations with higher forecast rainfall.

This allows rainfall conditions to be compared across different locations and provinces.

#### 2. Rainfall Accumulation

Rainfall accumulation is calculated across multiple forecast periods to identify areas that may experience sustained rainfall.

The analysis includes:

- 1-day rainfall accumulation
- 3-day rainfall accumulation
- 7-day rainfall accumulation

This provides more context than analyzing rainfall from a single forecast day.

#### 3. Consecutive Rainfall Streaks

The pipeline identifies consecutive rainy days for each forecast location.

A rainy day is currently defined as:

```
rain > 10 mm
```

## Future Improvements

- Containerize the pipeline with Docker
- Add data quality tests

