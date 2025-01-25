# Module 1 Homework: Docker & SQL

## Question 1. Understanding docker first run

```shell
dataeng@DESKTOP-RKINDGJ:~$ docker run -it --entrypoint bash python:3.12.8
root@1c6d1016d55b:/# pip --version
pip 24.3.1 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)
root@1c6d1016d55b:/#
```

## Question 2. Understanding Docker networking and docker-compose (skip as no code for this Question)

## Prepare Postgres

## Question 3. Trip Segmentation Count

```shell
taxi_data=# SELECT
    COUNT(*) FILTER (WHERE trip_distance <= 1) AS "Up to 1 mile",
    COUNT(*) FILTER (WHERE trip_distance > 1 AND trip_distance <= 3) AS "1 to 3 miles",
    COUNT(*) FILTER (WHERE trip_distance > 3 AND trip_distance <= 7) AS "3 to 7 miles",
    COUNT(*) FILTER (WHERE trip_distance > 7 AND trip_distance <= 10) AS "7 to 10 miles",
    COUNT(*) FILTER (WHERE trip_distance > 10) AS "Over 10 miles"
FROM
    public.green_taxi_trips
WHERE
    lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01';
 Up to 1 mile | 1 to 3 miles | 3 to 7 miles | 7 to 10 miles | Over 10 miles
--------------+--------------+--------------+---------------+---------------
       104830 |       198995 |       109642 |         27686 |         35201
(1 row)
```

## Question 4. Longest trip for each day

```shell
taxi_data=# SELECT
    TO_CHAR(lpep_pickup_datetime, 'YYYY-MM-DD') AS pickup_date,
    MAX(trip_distance) AS longest_trip_distance
FROM
    public.green_taxi_trips
WHERE
    lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01'
GROUP BY
    pickup_date
ORDER BY
    longest_trip_distance DESC
LIMIT 1;
 pickup_date | longest_trip_distance
-------------+-----------------------
 2019-10-31  |                515.89
(1 row)
```

## Question 5. Three biggest pickup zones

```shell
taxi_data=# SELECT
    z.Zone AS pickup_zone,
    SUM(gtt.total_amount) AS total_amount
FROM
    public.green_taxi_trips gtt
JOIN
    public.taxi_zone_lookup z
    ON gtt.pulocationid = z.LocationID  -- Match pulocationid with LocationID
WHERE
    gtt.lpep_pickup_datetime::date = '2019-10-18'
GROUP BY
    pickup_zone
HAVING
    SUM(gtt.total_amount) > 13000
ORDER BY
    total_amount DESC;
     pickup_zone     | total_amount
---------------------+--------------
 East Harlem North   |     18686.68
 East Harlem South   |     16797.26
 Morningside Heights |     13029.79
(3 rows)
```

## Question 6. Largest tip

```shell
SELECT
    dropoff_zone.Zone AS dropoff_zone,
    MAX(gtt.tip_amount) AS largest_tip
FROM
    public.green_taxi_trips gtt
JOIN
    public.taxi_zone_lookup pickup_zone
    ON gtt.pulocationid = pickup_zone.LocationID
JOIN
    public.taxi_zone_lookup dropoff_zone
    ON gtt.dolocationid = dropoff_zone.LocationID
WHERE
    pickup_zone.Zone = 'East Harlem North'
    AND gtt.lpep_pickup_datetime::date BETWEEN '2019-10-01' AND '2019-10-31'
GROUP BY
    dropoff_zone.Zone
ORDER BY
    largest_tip DESC
LIMIT 1;
 dropoff_zone | largest_tip
--------------+-------------
 JFK Airport  |        87.3
(1 row)

```

## Terraform

In this section homework 1, I have done prepared the environment by creating resources in GCP with Terraform.

1. Install Terraform on Laptop. 

2. Copy the files from the course repo to the Laptop.

3. Modify the files (see main.tf under terraform_basic folder) and create a GCP Bucket and Big Query Dataset.

GCP Bucket

   <img src="images/gcp_bucket.png" alt="GCP Bucket" width="500">
   
   
Big Query Dataset

   <img src="images/big_query_dataset.png" alt="Big Query Dataset" width="500" height="300">

### Execution

```shell
# Refresh service-account's auth-token for this session
gcloud auth application-default login
```

```shell
# Initialize state file (.tfstate)
C:\Users\user>cd C:\Users\user\terraform-projects
C:\Users\user\terraform-projects>terraform init
```

 <img src="images/tf_init.png" width="500">

```shell
# Check changes to new infra plan
C:\Users\user\terraform-projects>terraform plan
```

 <img src="images/tf_plan.png" width="500">

```shell
# Create new infra
C:\Users\user\terraform-projects>terraform apply
```

 <img src="images/tf_apply.png" width="500">
 
```shell
# Delete infra after your work, to avoid costs on any running services
C:\Users\user\terraform-projects>terraform destroy
```

 <img src="images/tf_destroy.png" width="500">

After executing terraform destroy, both the GCP Bucket and Big Query Dataset I created before are removed.


## Question 7. Terraform Workflow (skip as no code for this Question)



