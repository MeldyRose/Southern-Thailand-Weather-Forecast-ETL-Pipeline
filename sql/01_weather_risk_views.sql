--Only for checking columns after load into PostgreSQL
/*SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'weather';*/

--Clean/derive weather indicators
CREATE OR REPLACE VIEW vw_weather_risks AS
SELECT
    province,
    name,
    region,
    geocode,
    latitude,
    longitude,
-- We still need forecast_time for the changing weather from the API calling in different times, but we can derive forecast_date for the daily aggregation
    forecast_time,
    forecast_time::date AS forecast_date,
    
    rain,
    relative_humidity,
    sea_level_pressure,
    cloud_high,
    cloud_low,
    cloud_medium,
    condition,
    temperature,
    wind_speed,

    CASE
        WHEN rain > 90 THEN 'Very Heavy'
        WHEN rain > 35 THEN 'Heavy'
        WHEN rain > 10 THEN 'Moderate'
        WHEN rain > 0 THEN 'Light'
        ELSE 'None'
    END AS rain_intensity

FROM weather;

--Add this after creating the view to ensure uniqueness of geocode and forecast_time in the weather tables
ALTER TABLE weather
ADD CONSTRAINT weather_unique_forecast
UNIQUE (geocode, forecast_time);