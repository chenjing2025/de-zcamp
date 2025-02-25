SELECT *
FROM {{ ref('fact_trips') }}
WHERE pickup_datetime >= CAST(DATE '2019-01-15' AS TIMESTAMP) - INTERVAL '{{ var("days_back", env_var("DBT_DAYS_BACK", "30")) }}' DAY
