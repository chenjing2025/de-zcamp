from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, TableEnvironment
from pyflink.common.time import Duration
from pyflink.common.watermark_strategy import WatermarkStrategy

# Function to create the aggregated sink table in PostgreSQL
def create_trips_aggregated_sink(t_env):
    table_name = 'processed_events_aggregated'
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            event_hour TIMESTAMP(3),
            PULocationID INT,
            DOLocationID INT,
            num_trips BIGINT,
            PRIMARY KEY (event_hour, PULocationID, DOLocationID) NOT ENFORCED
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = '{table_name}',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        );
    """
    t_env.execute_sql(sink_ddl)
    return table_name

# Function to create the Kafka source table for the trips data
def create_trips_source_kafka(t_env):
    table_name = "trips"
    source_ddl = f"""
        CREATE TABLE {table_name} (
            lpep_pickup_datetime TIMESTAMP(3),
            lpep_dropoff_datetime TIMESTAMP(3),
            PULocationID INT,
            DOLocationID INT,
            passenger_count INT,
            trip_distance DOUBLE,
            tip_amount DOUBLE,
            event_time AS lpep_dropoff_datetime,
            WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'properties.bootstrap.servers' = 'redpanda-1:29092',
            'topic' = 'green-trips',
            'scan.startup.mode' = 'earliest-offset',
            'properties.auto.offset.reset' = 'earliest',
            'format' = 'json'
        );
    """
    t_env.execute_sql(source_ddl)
    return table_name

# Main function to set up the environment and execute the job
def process_trips():
    # Set up the execution environment for streaming jobs
    env = StreamExecutionEnvironment.get_execution_environment()
    env.enable_checkpointing(10 * 1000)  # Checkpointing every 10 seconds
    env.set_parallelism(3)  # Set parallelism for the job

    # Set up the table environment for stream processing
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = TableEnvironment.create(env)  # Updated to pass only the environment here

    # Ensure the Kafka connector JAR is loaded
    t_env.get_config().get_configuration().set_string(
        "pipeline.jars", "file:///opt/flink-1.16.1/lib/flink-connector-kafka-1.16.1.jar"
    )

    try:
        # Create Kafka source table and the PostgreSQL sink table
        source_table = create_trips_source_kafka(t_env)
        aggregated_table = create_trips_aggregated_sink(t_env)

        # SQL query to insert aggregated data into the sink table using session window
        t_env.execute_sql(f"""
        INSERT INTO {aggregated_table}
        SELECT
            window_start AS event_hour,
            PULocationID,
            DOLocationID,
            COUNT(*) AS num_trips
        FROM TABLE(
            SESSION(TABLE {source_table}, DESCRIPTOR(event_time), INTERVAL '5' MINUTES)
        )
        GROUP BY window_start, PULocationID, DOLocationID;
        """).wait()  # Wait for the job to complete

    except Exception as e:
        # Handle errors during the job execution
        print("Writing records from Kafka to JDBC failed:", str(e))

# Execute the job when the script is run
if __name__ == '__main__':
    process_trips()
