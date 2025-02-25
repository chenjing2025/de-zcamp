{{ config(materialized='view') }}

SELECT
    dispatching_base_num,
    CAST(pickup_datetime AS TIMESTAMP) AS pickup_datetime,
    CAST(dropOff_datetime AS TIMESTAMP) AS dropoff_datetime,
    CAST(PUlocationID AS INT64) AS PUlocationID,  -- Ensure it joins with dim_zones
    CAST(DOLocationID AS INT64) AS DOLocationID,
    SR_Flag,
    Affiliated_base_number
FROM {{ source('staging', 'fhv_tripdata') }}
WHERE dispatching_base_num IS NOT NULL   -- Filter out rows where dispatching_base_num is NULL
