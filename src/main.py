#Without Airflow, we canuse this main python file to run the ETL process. It will call the extraction, transformation, and load functions in order.

from .extraction import fetch_weather_data, save_data_to_json

def main():
    data = fetch_weather_data()
    if data: 
        save_data_to_json(data)
    else :
        print("No data fetched. Existing.")
    

if __name__ == "__main__":
    main()