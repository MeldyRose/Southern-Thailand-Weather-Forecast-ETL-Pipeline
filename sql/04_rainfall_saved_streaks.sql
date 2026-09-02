--Save the calculated streaks into a new view
CREATE OR REPLACE VIEW vw_rainfall_streak_calculated AS

WITH rain_groups AS (
    SELECT
        geocode,
        province,
        forecast_date,
        is_rainy,

        forecast_date - ROW_NUMBER() OVER (
            PARTITION BY geocode, is_rainy
            ORDER BY forecast_date
        )::int AS rain_group

    FROM vw_rainfall_streaks
)

SELECT
    geocode,
    province,
    forecast_date,
    is_rainy,

    CASE
        WHEN is_rainy = 1 THEN
            ROW_NUMBER() OVER (
                PARTITION BY geocode, is_rainy, rain_group
                ORDER BY forecast_date
            )
        ELSE 0
    END AS rain_streak

FROM rain_groups;