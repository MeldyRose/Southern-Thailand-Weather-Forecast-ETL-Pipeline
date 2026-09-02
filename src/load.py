from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.dialects.postgresql import insert

from .config import Config


def load_data(processed_data):
    df = processed_data
#Create a SQLAlchemy engine and metadata object to do UPSERT operation on the weather table. The UPSERT operation will insert new records and update existing records based on the unique constraint defined on the geocode and forecast_time columns.
    engine = create_engine(Config.DATABASE_URL)

    metadata = MetaData()
    weather_table = Table(
        "weather",
        metadata,
        autoload_with=engine
    )
#Retrieve the processed data as a list of dictionaries and perform an UPSERT operation on the weather table.
    records = df.to_dict(orient="records")

    stmt = insert(weather_table).values(records)
#Define the update_columns dictionary to specify which columns should be updated in case of a conflict. The excluded object is used to reference the values that would have been inserted if there was no conflict.
    update_columns = {
        column.name: stmt.excluded[column.name]
        for column in weather_table.columns
        if column.name not in ["geocode", "forecast_time"]
    }

    stmt = stmt.on_conflict_do_update(
        index_elements=["geocode", "forecast_time"],
        set_=update_columns
    )

    with engine.begin() as connection:
        connection.execute(stmt)

    print("Weather data loaded successfully.")
    return True