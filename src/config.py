from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

# Define the project root directory
ProjectRoot = Path(__file__).resolve().parent.parent

class Config:
    # Load the API key from environment variables
    API_KEY = os.getenv("API_KEY")
    if not API_KEY:
        raise ValueError("API_KEY is not set in the environment variables.")

    # Load the Database Url from environment variables
    DATABASE_URL = os.getenv("DATABASE_URL") 
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set")

    # Define paths for raw and processed data
    raw_data_path = ProjectRoot / "data" / "raw"
    processed_data_path = ProjectRoot / "data" / "processed"

    # Configuration for the weather API
    url = "https://data.tmd.go.th/nwpapi/v1/forecast/location/daily/region"
    default_region = "S"
    default_fields = "tc, tc_max, tc_min, rain, rh, slp, ws10m, wd10m, cloudlow, cloudmed, cloudhigh, cond"
    default_duration = "7"