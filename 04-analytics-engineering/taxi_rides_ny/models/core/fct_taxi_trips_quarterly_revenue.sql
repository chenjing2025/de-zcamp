-- models/core/fct_taxi_trips_quarterly_revenue.sql with YoY
WITH quarterly_revenue AS (
    SELECT
        CAST(EXTRACT(YEAR FROM pickup_datetime) AS INT64) AS year,  
        EXTRACT(QUARTER FROM pickup_datetime) AS quarter,
        CONCAT(CAST(EXTRACT(YEAR FROM pickup_datetime) AS STRING), '/Q', EXTRACT(QUARTER FROM pickup_datetime)) AS year_quarter,
        service_type,  
        SUM(total_amount) AS total_revenue
    FROM {{ ref('fct_taxi_trips') }}
    GROUP BY year, quarter, year_quarter, service_type
),
previous_year_revenue AS (
    SELECT
        CAST(year AS INT64) AS year,  
        quarter,
        service_type,
        total_revenue AS prev_year_revenue
    FROM quarterly_revenue
    WHERE year < (SELECT MAX(year) FROM quarterly_revenue)  -- Include all previous years
)
SELECT
    qr.year,
    qr.quarter,
    qr.year_quarter,
    qr.service_type,  
    qr.total_revenue,
    COALESCE(pyr.prev_year_revenue, 0) AS prev_year_revenue,
    CASE
        WHEN pyr.prev_year_revenue = 0 THEN NULL  
        ELSE (qr.total_revenue - pyr.prev_year_revenue) / pyr.prev_year_revenue * 100
    END AS yoy_growth
FROM quarterly_revenue qr
LEFT JOIN previous_year_revenue pyr
    ON qr.quarter = pyr.quarter 
    AND qr.year = pyr.year + 1  
    AND qr.service_type = pyr.service_type
ORDER BY qr.year, qr.quarter, qr.service_type


