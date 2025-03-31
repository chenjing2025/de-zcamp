# 🚴‍♂️ End-to-End Data Pipeline for Santander Bike Rentals

## 📑Table of Contents
* [Overview](#overview)
* [Problem Statement](#problem-statement)
* [Cloud Setup](#cloud-setup)
  * [Provision GCP Resources with Terraform](#provision-gcp-resources-with-terraform)
  * [Set Up Airflow with Docker](#set-up-airflow-with-docker)
* [Data Pipeline Setup](#data-pipeline-setup)
  * [Data Ingestion (Airflow DAG)](#data-ingestion-airflow-dag)
  * [Data Transformation (BigQuery SQL)](#data-transformation-bigquery-sql)
* [Dashboard Setup](#dashboard-setup)
* [Running the Pipeline](#running-the-pipeline)

## Overview
This guide will walk you through setting up an end-to-end data pipeline using Apache Airflow, Google Cloud Storage (GCS), BigQuery, and Looker Studio. By the end of this workshop, you'll have a working dashboard visualizing London Santander bike rental data.

## Problem Statement
The goal of this project is to:

✅ Automate data ingestion from TfL (Transport for London) open data.

✅ Store raw data in Google Cloud Storage (GCS) as a data lake.

✅ Load and transform data into Google BigQuery for analytics.

✅ Build a dashboard in Looker Studio to visualize bike rental trends.

## Cloud Setup
### Provision GCP Resources with Terraform
First, we need to create a Google Cloud Storage bucket and a BigQuery dataset.

🛠 Step 1: Install Terraform

+ Install Terraform on your system by following this guide:[Terraform Installation Guide](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/1_terraform_gcp/windows.md).

+ Once installed, verify the installation with:

```
terraform -v  # Check Terraform version
```

🛠 Step 2: Google Cloud SDK and Credentials Setup

+ Set up the Google Cloud SDK on your system and authenticate with your Google Cloud project.

+ Follow the setup instructions here:
[Google Cloud SDK Setup Guide](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/1_terraform_gcp/2_gcp_overview.md#initial-setup)


🛠 Step 3: Create a Terraform Script 

+ Create a file called main.tf in a designated folder for your Terraform projects. For example, create a folder like C:\Users\user\terraform-projects.

+ You can refer to your main.tf file [here](https://github.com/chenjing2025/de-zcamp/blob/main/terraform_basic/main.tf).


🛠 Step 4: Deploy Terraform 

+ Open your terminal or command prompt and run the following commands:

```
C:\Users\user>cd C:\Users\user\terraform-projects
C:\Users\user\terraform-projects>terraform init
C:\Users\user\terraform-projects>terraform plan
C:\Users\user\terraform-projects>terraform apply
```

+ These [commands](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/1_terraform_gcp/1_terraform_overview.md#execution-steps)
will:

1. Initialize Terraform (terraform init).

2. Preview the changes Terraform will make (terraform plan).

3. Apply the changes to your Google Cloud project (terraform apply).


### Set Up Airflow with Docker
🛠 Step 1: Install Docker and Docker Compose

Ensure Docker is installed:
```
docker -v  # Check Docker version
docker-compose -v  # Check Docker Compose version
```

🛠 Step 2: Create docker-compose.yml

This will set up Apache Airflow with a Postgres backend.

```
version: '3'
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
    ports:
      - "5432:5432"

  webserver:
    image: apache/airflow:2.3.0
    environment:
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
    ports:
      - "8080:8080"
    volumes:
      - ./dags:/opt/airflow/dags
```
🛠 Step 3: Start Airflow

Run the following command to start Airflow:

```
docker-compose up -d
```

## Data Pipeline Setup
### Data Ingestion (Airflow DAG)

🛠 Step 1: Create an Airflow DAG

Create a Python file dags/bike_rentals_dag.py:

```
from airflow import DAG
from airflow.providers.google.cloud.operators.storage import GCSCreateObjectOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
}

with DAG('santander_bike_rentals_dag', default_args=default_args, schedule_interval='@daily') as dag:
    
    upload_to_gcs = GCSCreateObjectOperator(
        task_id='upload_data_to_gcs',
        bucket_name='santander-bike-rentals-data-lake',
        object_name='bike_rentals.csv',
        source_objects=['/path/to/local/file/bike_rentals.csv']
    )

    load_to_bigquery = GCSToBigQueryOperator(
        task_id='load_data_to_bigquery',
        bucket_name='santander-bike-rentals-data-lake',
        source_objects=['bike_rentals.csv'],
        destination_project_dataset_table='bike_rentals.dataset.table',
        write_disposition='WRITE_APPEND'
    )

    upload_to_gcs >> load_to_bigquery
```

🛠 Step 2: Deploy the DAG to Airflow

Move the DAG file into the dags/ folder in your Airflow container:

```
mv bike_rentals_dag.py dags/
```
Restart Airflow:

```
docker-compose restart
```
### Data Transformation (BigQuery SQL)
🛠 Step 1: Create a SQL Query for Data Cleaning

Create a SQL file sql/transform_bike_rentals.sql:

```sql
-- Clean and filter data
CREATE OR REPLACE TABLE `bike_rentals.dataset.cleaned_table` AS
SELECT * 
FROM `bike_rentals.dataset.raw_table`
WHERE rental_count > 0;
```
🛠 Step 2: Run SQL in BigQuery

Run the query in BigQuery Console or use:

```
bq query --use_legacy_sql=false < sql/transform_bike_rentals.sql
```
## Dashboard Setup
1️⃣ Open Looker Studio → Click Create Report

2️⃣ Select BigQuery as your data source

3️⃣ Choose the bike_rentals.dataset.cleaned_table

4️⃣ Create visualizations:

Bar Chart → Categorical data distribution

Line Chart → Bike rentals over time

## Running the Pipeline
To run the entire pipeline:

1️⃣ Start Terraform:

```
terraform apply
```

2️⃣ Start Airflow:

```
docker-compose up -d
```

3️⃣ Trigger DAG in Airflow UI:

Open http://localhost:8080

Run santander_bike_rentals_dag

4️⃣ Check BigQuery for transformed data

5️⃣ Open Looker Studio and refresh the dashboard

