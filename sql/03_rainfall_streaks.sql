--Find consequtive rainy days (rain > 10 mm) for each geocode and province
CREATE OR REPLACE VIEW vw_rainfall_streaks AS
SELECT
    geocode,
    province,
    forecast_date,
    rain,

    CASE
        WHEN rain > 10 THEN 1
        ELSE 0
    END AS is_rainy

FROM vw_weather_risks;

--Calculate the streak of consecutive rainy days for each geocode and province
WITH rain_groups AS (
    SELECT
        province,
        forecast_date,
        is_rainy,
        forecast_date - ROW_NUMBER() OVER (
            PARTITION BY province, is_rainy
            ORDER BY forecast_date
        )::int AS rain_group
    FROM vw_rainfall_streaks
)
SELECT
    province,
    forecast_date,
    is_rainy,
    CASE
        WHEN is_rainy = 1 THEN
            ROW_NUMBER() OVER (
                PARTITION BY province, is_rainy, rain_group
                ORDER BY forecast_date
            )
        ELSE 0
    END AS rain_streak
FROM rain_groups;