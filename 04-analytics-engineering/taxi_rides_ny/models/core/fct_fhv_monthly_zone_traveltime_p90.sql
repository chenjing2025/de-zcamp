WITH trip_duration_data AS (
    SELECT
        fhv.PUlocationID AS pickup_location_id,      -- Pickup Location ID
        fhv.DOLocationID AS dropoff_location_id,     -- Dropoff Location ID
        fhv.pickup_zone_name,                        -- Pickup Zone Name from dim_fhv_trips
        fhv.dropoff_zone_name,                       -- Dropoff Zone Name from dim_fhv_trips
        fhv.year,                                    -- Year from dim_fhv_trips
        fhv.month,                                   -- Month from dim_fhv_trips
        TIMESTAMP_DIFF(TIMESTAMP(fhv.dropOff_datetime), TIMESTAMP(fhv.pickup_datetime), SECOND) AS trip_duration -- Calculate trip duration in seconds
    FROM {{ ref('dim_fhv_trips') }} fhv
    WHERE fhv.PUlocationID IS NOT NULL
      AND fhv.DOLocationID IS NOT NULL
)

SELECT
    pickup_location_id,
    dropoff_location_id,
    pickup_zone_name,                             -- Include Pickup Zone Name
    dropoff_zone_name,                            -- Include Dropoff Zone Name
    year,
    month,
    PERCENTILE_CONT(trip_duration, 0.90) OVER (PARTITION BY year, month, pickup_location_id, dropoff_location_id) AS p90_trip_duration -- Compute the P90 for each partition
FROM trip_duration_data
ORDER BY year, month, pickup_location_id, dropoff_location_id
