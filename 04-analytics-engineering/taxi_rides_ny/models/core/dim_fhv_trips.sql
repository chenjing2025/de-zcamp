{{ config(materialized='table') }}

WITH fhv AS (
    SELECT *
    FROM {{ ref('stg_fhv_tripdata') }}
),
dim_zones as (
    select * from {{ ref('dim_zones') }}
    where borough != 'Unknown'
)

SELECT
    fhv.dispatching_base_num,
    fhv.pickup_datetime,
    fhv.dropOff_datetime,
    fhv.PUlocationID,
    fhv.DOLocationID,
    fhv.SR_Flag,
    fhv.Affiliated_base_number,
    EXTRACT(YEAR FROM fhv.pickup_datetime) AS year,
    EXTRACT(MONTH FROM fhv.pickup_datetime) AS month,
    pz.zone AS pickup_zone_name,  -- Zone information for Pickup
    dz.zone AS dropoff_zone_name -- Zone information for Dropoff
FROM fhv
INNER JOIN dim_zones pz
    ON fhv.PUlocationID = pz.locationid  -- Adjust field names as necessary
INNER JOIN dim_zones dz
    ON fhv.DOLocationID = dz.locationid  -- Adjust field names as necessary

