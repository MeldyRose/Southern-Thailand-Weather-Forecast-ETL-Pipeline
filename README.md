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

* **Docker (Recommended)**: Dependencies listed in `requirements.txt` are automatically installed inside the container via the `Dockerfile` when you run `docker compose up --build`. No manual installation is needed!
* **Local Python Execution (Fallback)**: If running the ETL pipeline manually without Docker, install dependencies inside your virtual environment:

  ```bash
  pip install -r requirements.txt
  ```

### 4. Configure environment variables

Create a `.env` file by copying `.env.example`:

**Linux / macOS / Git Bash / PowerShell:**
```bash
cp .env.example .env
```

Or on **Windows Command Prompt (cmd)**:
```cmd
copy .env.example .env
```

Open `.env` and fill in your keys.

> **Security Note:** Never commit your `.env` file or API key to Git (`.env` is included in `.gitignore`).

### 5. Run the pipeline

The pipeline can be run in two ways:

1. **Airflow + Docker** — recommended for scheduled orchestration
2. **Python `main.py`** — fallback option for running the ETL manually

#### 5.1 Set Up Airflow and Docker

The repository includes a custom **`Dockerfile`** and a ready-to-use **`docker-compose.yaml`** in the root directory to orchestrate Apache Airflow and PostgreSQL.

##### 5.1.1 How the `Dockerfile` Works

The project uses a custom **`Dockerfile`** extending `apache/airflow:2.7.1-python3.11` to package the ETL environment:
- **System Dependencies**: Installs system packages (`gcc`, `libpq-dev`) for database driver support.
- **Python Requirements**: Automatically installs all project dependencies from `requirements.txt` into the Airflow environment layer.
- **Source Code Integration**: Copies `src/` into `/opt/airflow/src/` so Airflow tasks can directly import extraction, transformation, and loading functions.

When `docker compose up --build` is run, Docker automatically uses the `Dockerfile` (`build: .` in `docker-compose.yaml`) to build the custom container image for all Airflow services.

##### 5.1.2 Services Overview in Docker Compose

The `docker-compose.yaml` manages two PostgreSQL services to keep system metadata separated from your business data:

1. **`postgres` (Airflow Metadata DB)**: Internal database used exclusively by Apache Airflow to store DAG runs, execution logs, and scheduling metadata.
2. **`weather_db` (Project Data Warehouse)**: Dedicated PostgreSQL database for storing weather forecast data and analytical views.
   - **Automated SQL Setup**: Mounts `./sql` to `/docker-entrypoint-initdb.d`. All SQL scripts (`01_weather_risk_views.sql`, `02_rainfall_accumulation.sql`, etc.) execute automatically on startup to build database views and structures.
   - **External Access (Port `5433`)**: Exposes port `5433:5432` so external tools (**Power BI**, **DBeaver**, or local SQL clients) can connect directly to `localhost:5433`.

##### 5.1.3 Running Airflow with Docker Compose & Dockerfile

1. **Set up Environment Variables**:
   Copy `.env.example` to `.env` and fill in your TMD API key:
   ```bash
   cp .env.example .env
   ```

2. **Build Image & Initialize Airflow**:
   Build the custom Docker image using `Dockerfile` and initialize Airflow:
   ```bash
   docker compose up --build airflow-init
   ```

3. **Start All Services**:
   ```bash
   docker compose up -d
   ```
   *(If you make changes to `requirements.txt` or `src/`, rebuild the image anytime using `docker compose build`)*

4. **Verify Running Containers**:
   ```bash
   docker compose ps
   ```

5. **Access the Airflow Web UI**:
   Open http://localhost:8080 in your browser.
   - **Default Username:** `airflow`
   - **Default Password:** `airflow`

##### 5.1.4 Running the Weather ETL DAG

1. Open http://localhost:8080 and log in.
2. Locate the DAG named `southern_thailand_weather_forecast_etl_pipeline`.
3. Unpause/enable the DAG toggle and click **Trigger DAG**.
4. The pipeline will execute the tasks in order: `Extract → Transform → Load`.

##### 5.1.5 Stopping Airflow

To stop all running services:
```bash
docker compose down
```

#### 5.2 Run the Pipeline Without Airflow

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

- [ ] Add data quality tests (e.g. Great Expectations / Pytest)

