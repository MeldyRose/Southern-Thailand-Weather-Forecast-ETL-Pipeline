import os
import json
import pandas as pd
from datetime import datetime
from .config import Config


def normalize_json(data):
    #The process of normalization can vary, it depends on your data
    df = pd.json_normalize(data['WeatherForecasts']) #Normalize the first level of JSON data into a flat table
    df = df.explode('forecasts',ignore_index=True) #Explode the 'Forecasts' column to create separate rows for each forecast

    forecast_df = pd.json_normalize(df['forecasts']) #Normalize the 'Forecasts' column into a flat table

    df = pd.concat([df.drop(columns=['forecasts']), forecast_df], axis=1) #Concatenate the original DataFrame with the normalized forecasts DataFrame
    return df

def col_rename(df):
    #1. Rename columns after normalize and explode automatically after . (Only if there is no duplicate column names)
    df.columns = df.columns.str.split('.').str[-1]
    #2. Rename columns for easier understanding and better readiness for PostgreSQL
    df = df.rename(columns={
        "areatype": "area_type",
        "lat": "latitude",
        "lon": "longitude",
        "time": "forecast_time",
        "cloudhigh": "cloud_high",
        "cloudmed": "cloud_medium",
        "cloudlow": "cloud_low",
        "cond": "condition",
        "rh": "relative_humidity",
        "slp": "sea_level_pressure",
        "tc": "temperature",
        "tc_max": "temperature_max",
        "tc_min": "temperature_min",
        "wd10m": "wind_direction",
        "ws10m": "wind_speed"
    })
    print(df.columns)
    return df

def clean_data(df):
    #There is no negative, duplicate,or any outliers.
    #Because the dataset is already cleaned and it only needs standardization of time column, dropping the missing value since it is intended to be missing and it is not an important part, so our transformation part is small. 
    df['forecast_time'] = pd.to_datetime(df['forecast_time'])
    #Drop the missing columns
    df = df.drop(columns=['tambon', 'amphoe'], errors='ignore')
    
    return df

def save_processed_data(df):
    #Save processed data after transformation before sending to the PostgreSQL
    if df is None or df.empty:
        print("No data to save.")
        return None

    #Ensure output directory exists
    os.makedirs(Config.processed_data_path, exist_ok=True)
    filename = f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    file_path = os.path.join(Config.processed_data_path, filename)
    try:
        df.to_csv(f"{file_path}", index =False)
        print(f"Processed data saved to {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to save processed data as csv file: {e}")
    return None

def transformation(raw_file_path):
    with open(raw_file_path, "r", encoding="utf-8")as file:
        data = json.load(file)

    df = normalize_json(data)
    df = col_rename(df)
    df = clean_data(df)
    saved_path = save_processed_data(df)
    return df

                