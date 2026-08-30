import pandas as pd
from sqlalchemy import create_engine
from .config import Config


def load_data(processed_data):
    #df = pd.read_csv(Config.processed_data_path)
    df = processed_data
    engine = create_engine(Config.DATABASE_URL)

    df.to_sql(
        #replace is only convenient for testing. 
        "weather",
        engine,
        if_exists="replace",
        index=False
    )

    print("Weather data loaded successfully.")
    return True