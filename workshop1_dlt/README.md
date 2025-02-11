## Workshop "Data Ingestion with dlt": Homework

Run https://github.com/chenjing2025/de-zcamp/blob/main/workshop1_dlt/README.md in Google Colab

```markdown
[Link to the Notebook](path/to/your/workshop1_dlt_homework.ipynb)

### Question 1: dlt Version

```python
!pip install dlt[duckdb]
!dlt --version
```

### Question 2: Define & Run the Pipeline (NYC Taxi API)

```python
import dlt
import requests

# Define the API endpoint
BASE_URL = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"

# Define a resource to extract all pages of data
@dlt.resource
def ny_taxi():
    page = 1  # Start from page 1

    while True:
        response = requests.get(BASE_URL, params={"page": page})
        data = response.json()

        # Stop when an empty page is returned
        if not data:
            break

        yield data  # Return data for this page
        page += 1  # Go to the next page

# Create a pipeline for DuckDB
pipeline = dlt.pipeline(
    pipeline_name="ny_taxi_pipeline",
    destination="duckdb",
    dataset_name="ny_taxi_data"
)

# Run the pipeline and load data into DuckDB
load_info = pipeline.run(ny_taxi)
print(load_info)
```

```python
import duckdb
from google.colab import data_table
data_table.enable_dataframe_formatter()

# A database '<pipeline_name>.duckdb' was created in working directory so just connect to it

# Connect to the DuckDB database
conn = duckdb.connect(f"{pipeline.pipeline_name}.duckdb")

# Set search path to the dataset
conn.sql(f"SET search_path = '{pipeline.dataset_name}'")

# Describe the dataset
conn.sql("DESCRIBE").df()
```

```python
# Show all tables in the dataset
tables = conn.sql("SHOW TABLES").df()
print(tables)
```

                  name
0           _dlt_loads
1  _dlt_pipeline_state
2         _dlt_version
3              ny_taxi

```python
print(len(tables))
```

4

### Question 3: Explore the loaded data

```python
df4 = pipeline.dataset(dataset_type="default").ny_taxi.df()
total_records = len(df4)
print(f"Total number of records extracted: {total_records}")
```

Total number of records extracted: 10000

### Question 4: Trip Duration Analysis

```python
with pipeline.sql_client() as client:
    res = client.execute_sql(
            """
            SELECT
            AVG(date_diff('minute', trip_pickup_date_time, trip_dropoff_date_time))
            FROM ny_taxi;
            """
        )
    # Prints column values of the first row
    print(res)
```

[(12.3049,)]
