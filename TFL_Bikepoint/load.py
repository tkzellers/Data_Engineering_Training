import requests
import json
from datetime import datetime
import os   
import time
import logging
import os
from dotenv import load_dotenv
import boto3

current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

log_filename = (f"{log_dir}/{__name__}_{current_time}.log")

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_filename
    )

logger = logging.getLogger() 
logger.info("Logger initiated")

##### AWS Keys
load_dotenv()
api_key = os.getenv('AWS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_KEY')
bucket = os.getenv('AWS_BUCKET_NAME')
logger.info("Retrieved AWS keys")
##### AWS Keys


##### AWS Client
s3_client = boto3.client(
    's3',
    aws_access_key_id = api_key,
    aws_secret_access_key = secret_key,
)
##### AWS Client


folder_path = os.path.join('data')



for root,_,files in os.walk(folder_path):
    processed = 0
    for filename in files:
        if filename.endswith('.json'):
            source_path = os.path.join(root, filename)
            try:
                s3_client.upload_file(source_path, bucket, filename)
                print(f"{filename} was uploaded to S3")    
                s3_client.head_object(Bucket = bucket, Key = filename) #checks if the file exists in s3, would error if it doesn't
                os.remove(source_path)
                processed += 1
            except Exception as e:
                logging.error(e)
            
            print(f"Processed {processed} files")
