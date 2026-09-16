from datetime import datetime
import sys

sys.path.insert(0, "/opt/airflow")
from airflow.sdk import DAG, task

from src.config import Config
from src.extraction import extraction
from src.transformation import transformation
from src.load import load_data

with DAG(
    dag_id="southern_thailand_weather_forecast_etl_pipeline",
    start_date=datetime(2026, 9, 14),
    schedule="@daily",
    catchup=False,
    tags=["weather","etl"],
):

    @task
    def extraction_task():
        return extraction()

    @task
    def transformation_task(raw_data):
        return transformation(raw_data)

    @task
    def load_task(transformed_data):
        return load_data(transformed_data)

    raw_data = extraction_task()
    transformed_data = transformation_task(raw_data)
    load_task(transformed_data)

