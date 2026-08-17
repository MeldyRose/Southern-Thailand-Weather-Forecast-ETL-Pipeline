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
        responses = requests.request("GET", url, headers=headers, params= querystring, timeout= 10)
        responses.raise_for_status() #Raises HTTPError for 4xx/5xx responses
        data = responses.json()
        return data
    except (requests.exceptions.RequestException, json.JSONDecodeError, ValueError) as e:
        #Check if Network/ HTTP problem, Malformed response text, Invalid/ empty data payload happens
        print(f"Error fetching weather data: {e}")
        return None 

def save_data_to_json(data):
    if not data:
        print("No data to save.")
        return

    #Ensure output directory exists
    os.makedirs(Config.raw_data_path, exist_ok=True)
    filename = f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    file_path = os.path.join(Config.raw_data_path, filename)

    with open(file_path, 'w', encoding= "utf-8") as f:
        json.dump(data, f, ensure_ascii= False, indent= 12)
    print(f"Data saved to {file_path}")
