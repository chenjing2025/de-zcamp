import io
import os
import requests
import pandas as pd
from google.cloud import storage
import time
from google.api_core.exceptions import RetryError

"""
Pre-reqs: 
1. `pip install pandas pyarrow google-cloud-storage`
2. Set GOOGLE_APPLICATION_CREDENTIALS to your project/service-account key
3. Set GCP_GCS_BUCKET as your bucket or change default value of BUCKET
"""

# services = ['fhv','green','yellow']
init_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/'
# switch out the bucketname
BUCKET = os.environ.get("GCP_GCS_BUCKET", "my-kestra-data-bucket")


def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    """
    # # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # # (Ref: https://github.com/googleapis/python-storage/issues/74)
    # storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    # storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

    # client = storage.Client()
    # bucket = client.bucket(bucket)
    # blob = bucket.blob(object_name)
    # blob.upload_from_filename(local_file)
    retries = 5
    for i in range(retries):
        try:
            client = storage.Client()
            bucket = client.bucket(bucket)
            blob = bucket.blob(object_name)
            blob.upload_from_filename(local_file, timeout=600)  # Increase timeout
            print(f"Uploaded: {object_name}")
            break  # Break the loop if upload is successful
        except RetryError as e:
            if i == retries - 1:
                print(f"Failed to upload after {retries} attempts: {e}")
            else:
                wait_time = 2 ** i  # Exponential backoff
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)


def web_to_gcs(year, service):
    for i in range(12):
        
        # sets the month part of the file_name string
        month = '0'+str(i+1)
        month = month[-2:]

        # csv file_name
        file_name = f"{service}_tripdata_{year}-{month}.csv.gz"

        # download it using requests via a pandas df
        request_url = f"{init_url}{service}/{file_name}"
        # r = requests.get(request_url)
        r = requests.get(request_url, timeout=120)  # Set a timeout for the download
        open(file_name, 'wb').write(r.content)
        print(f"Local: {file_name}")

        # read it back into a parquet file
        df = pd.read_csv(file_name, compression='gzip')
        file_name = file_name.replace('.csv.gz', '.parquet')
        df.to_parquet(file_name, engine='pyarrow')
        print(f"Parquet: {file_name}")

        # upload it to gcs 
        upload_to_gcs(BUCKET, f"{service}/{file_name}", file_name)
        print(f"GCS: {service}/{file_name}")


# web_to_gcs('2019', 'green')
# web_to_gcs('2020', 'green')
# web_to_gcs('2019', 'yellow')
web_to_gcs('2020', 'yellow')
# web_to_gcs('2019', 'fhv')

# import numpy
# print(numpy.__version__)
