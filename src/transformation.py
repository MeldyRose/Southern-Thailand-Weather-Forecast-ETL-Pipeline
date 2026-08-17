import os
import json
import pandas as pd
from .config import Config


def normalize_json(data):
    #The process of normalization can vary, it depends on your data
    df = pd.json_normalize(data['WeatherForecasts']) #Normalize the first level of JSON data into a flat table
    df = df.explode('forecasts',ignore_index=True) #Explode the 'Forecasts' column to create separate rows for each forecast

    forecast_df = pd.json_normalize(df['forecasts']) #Normalize the 'Forecasts' column into a flat table

    df = pd.concat([df.drop(columns=['forecasts']), forecast_df], axis=1) #Concatenate the original DataFrame with the normalized forecasts DataFrame
    return df

def clean_data(df):
    #Because the dataset is already cleaned and it only needs standardization of time column, our transformation part is small.
    df['time'] = pd.to_datetime(df['time'])
    return df

def transformation(raw_file_path):
    with open(raw_file_path, "r", encoding="utf-8")as file:
        data = json.load(file)

    df = normalize_json(data)
    df = clean_data(df)
    return df

                