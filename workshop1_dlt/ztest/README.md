# 🚴‍♂️ End-to-End Data Pipeline for Santander Bike Rentals

## 📑 Table of Contents

* [Objectives](#objectives)
* [Dataset](#dataset)
* [Tech Stack](#tech-stack)
* [Pipeline Architecture](#pipeline-architecture)
* [Dashboard Features](#dashboard-features)
* [Repository Structure](#repository-structure)
* [Deployment Guide](#deployment-guide)
* [Future Enhancements](#future-enhancements)
* [Contributors](#contributors)

## 📌 Overview
This project builds an end-to-end data pipeline to process and visualize Santander bicycle rental data in London. It integrates cloud-based storage, data transformation, and dashboard visualization.

## 🎯 Objectives
Ingest & Store 🚀 - Fetch and store raw data in a data lake (Google Cloud Storage).

Process & Transform 🔄 - Move data to BigQuery and clean it for analysis.

Visualize & Analyze 📊 - Build a Looker Studio dashboard with key insights.

## 📂 Dataset
Source: TfL Cycling Open Data

Content: Time-series data on Santander bicycle rentals across London.

## ⚙️ Tech Stack
Cloud Platform: Google Cloud Platform (GCP) ☁️

Orchestration: Apache Airflow (Dockerized) 🔄

Data Warehouse: BigQuery 🏛️

Infrastructure: Terraform 🏗️

Visualization: Looker Studio 📊

## 🛠️ Pipeline Architecture

[Data Source] → [GCS] → [Airflow DAGs] → [BigQuery] → [Looker Studio]
Ingestion: Collects raw data and stores it in GCS.

Processing: Moves data from GCS to BigQuery.

Transformation: Cleans and structures data for analytics.

Visualization: Displays insights via Looker Studio.

## 📊 Dashboard Features
Categorical Data Distribution 📌 - Breakdown of key categorical variables.

Temporal Trends ⏳ - Analysis of rental trends over time.

## 🏗️ Repository Structure
```
📂 airflow/
 ├── 📂 dags/               # Airflow DAGs
 │    ├── dag1.py
 │    ├── dag2.py
 │    ├── dag3.py
 ├── 📂 sql/                # SQL transformation scripts
 │    ├── query1.sql
 │    ├── query2.sql
 ├── 📝 Dockerfile           # Airflow containerization
 ├── 📝 docker-compose.yml   # Docker setup
 ├── 📝 README.md            # Project documentation
```

## 🚀 Deployment Guide
Set up GCP resources using Terraform to provision the necessary infrastructure.

Deploy Airflow DAGs to automate the data ingestion, storage in Google Cloud Storage (GCS), and processing into BigQuery.

Run data transformations in BigQuery, optionally using dbt.

Create a Looker Studio Dashboard using the processed data for visualization.

## 🔮 Future Enhancements
Automate transformations using dbt.

Add real-time data processing.

Expand dashboard insights.

👥 Contributors
Your Name
