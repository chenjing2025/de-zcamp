# Module 1 Homework: Docker & SQL

## Question 1. Understanding docker first run

```shell
dataeng@DESKTOP-RKINDGJ:~$ docker run -it --entrypoint bash python:3.12.8
root@1c6d1016d55b:/# pip --version
pip 24.3.1 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)
root@1c6d1016d55b:/#
```

## Question 2. Understanding Docker networking and docker-compose (no code for this Question)


## Prepare Postgres

## Question 3. Trip Segmentation Count

## Question 4. Longest trip for each day

## Question 5. Three biggest pickup zones

## Question 6. Largest tip

```shell
taxi_data=# SELECT
    z.Zone AS dropoff_zone,
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
ERROR:  missing FROM-clause entry for table "z"
LINE 2:     z.Zone AS dropoff_zone,
            ^
taxi_data=# SELECT
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


## Question 7. Terraform Workflow ((no code for this Question))



