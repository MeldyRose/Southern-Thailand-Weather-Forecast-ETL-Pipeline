from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import json
import requests

from .config import Config

load_dotenv()

def fetch_weather_data():
    print("Fetched")
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
        responses = requests.request("GET", url, headers=headers, params= querystring, timeout= 10)
        data = responses.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None 

def save_data_to_json(data):
    print("Save?")
    filename = f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    file_path = os.path.join(Config.raw_data_path, filename)

    with open(file_path, 'w', encoding= "utf-8") as f:
        json.dump(data, f, ensure_ascii= False, indent= 12)
    print(f"Data saved to {file_path}")
