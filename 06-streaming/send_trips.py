import pandas as pd
import json
from time import time
from kafka import KafkaProducer

# Define the JSON serializer
def json_serializer(data):
    return json.dumps(data).encode('utf-8')

# Kafka configuration
server = 'localhost:9092'  # Kafka server
topic_name = 'green-trips'  # Topic name

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[server],
    value_serializer=json_serializer
)

# Path to your local CSV file in WSL
file_path = "/mnt/d/data-engineering-zoomcamp/green_tripdata_2019-10.csv.gz" 

# Read the data from the CSV file
df = pd.read_csv(file_path, compression='gzip', usecols=[
    'lpep_pickup_datetime', 'lpep_dropoff_datetime', 'PULocationID',
    'DOLocationID', 'passenger_count', 'trip_distance', 'tip_amount'
])

# Send data to Kafka topic
t0 = time()  # Start time

for _, row in df.iterrows():
    message = row.to_dict()  # Convert row to dictionary
    producer.send(topic_name, value=message)

producer.flush()  # Ensure all data is sent

t1 = time()  # End time
took = t1 - t0  # Calculate time taken

print(f"Time taken to send data: {took:.2f} seconds")
