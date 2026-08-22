from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import json
import requests

from .config import Config

load_dotenv()

def fetch_weather_data():
    tmrw_date = (datetime.now()+timedelta(days=1)).strftime("%Y-%m-%d")
    url = Config.url
    querystring = {
        "region": Config.default_region,
        "fields": Config.default_fields,
        "date":tmrw_date, 
        "duration": Config.default_duration
    }
    headers = {
        'accept': "application/json",
        'authorization': f"Bearer {Config.API_KEY}",
    }

    try: 
        response = requests.request("GET", url, headers=headers, params= querystring, timeout= 10)
        response.raise_for_status() #Raises HTTPError for 4xx/5xx responses
        data = response.json()

        if not data or 'WeatherForecasts' not in data:
            print("Warning: API responded successfully but key data structure is missing.")

        return data
    
    except (requests.exceptions.RequestException, json.JSONDecodeError, ValueError) as e:
        #Check if Network/ HTTP problem, Malformed response text, Invalid/ empty data payload happens
        print(f"Error fetching weather data: {e}")
        return None 

def save_data_to_json(data):
    if not data:
        print("No data to save.")
        return None

    #Ensure output directory exists
    os.makedirs(Config.raw_data_path, exist_ok=True)
    filename = f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    file_path = os.path.join(Config.raw_data_path, filename)
    try:
        with open(file_path, 'w', encoding= "utf-8") as f:
            json.dump(data, f, ensure_ascii= False, indent= 12)
        print(f"Raw data saved to {file_path}")
        return file_path

    except Exception as e:
        print(f"Failed to write raw data to JSON file: {e}")
        return None

def extraction():
    data = fetch_weather_data()
    file_path = save_data_to_json(data)
    return file_path
