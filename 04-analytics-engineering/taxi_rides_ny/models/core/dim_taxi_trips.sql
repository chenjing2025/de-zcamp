-- models/core/dim_taxi_trips.sql

WITH time_dimensions AS (
    SELECT
        pickup_datetime,
        EXTRACT(YEAR FROM pickup_datetime) AS year,
        EXTRACT(QUARTER FROM pickup_datetime) AS quarter,
        EXTRACT(MONTH FROM pickup_datetime) AS month,
        CONCAT(EXTRACT(YEAR FROM pickup_datetime), '/Q', EXTRACT(QUARTER FROM pickup_datetime)) AS year_quarter
    FROM {{ ref('fct_taxi_trips') }}
)

SELECT
    year,
    quarter,
    month,
    year_quarter
FROM time_dimensions
GROUP BY year, quarter, month, year_quarter
ORDER BY year, quarter

