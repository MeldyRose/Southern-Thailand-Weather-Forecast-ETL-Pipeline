#Without Airflow, we canuse this main python file to run the ETL process. It will call the extraction, transformation, and load functions in order.

from .extraction import extraction
from .transformation import transformation

def main():
    raw_data = extraction()
    processed_data = transformation(raw_data)



    

if __name__ == "__main__":
    main()