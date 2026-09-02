--Analyze rainfall across the 7-day forecast

--A. Daily rainfall already exists in 01 so now we calculate for B and C

CREATE OR REPLACE VIEW vw_rainfall_accumulation AS
SELECT
    geocode,
    province,
    forecast_date,
    rain,
--B. 3-day cumulative rainfall
    SUM(rain) OVER (
        PARTITION BY geocode
        ORDER BY forecast_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS rain_3day_total,
--C. 7-day cumulative rainfall
    SUM(rain) OVER (
        PARTITION BY geocode
        ORDER BY forecast_
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS rain_7day_total

FROM vw_weather_risks;
