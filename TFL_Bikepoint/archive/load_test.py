import os
from dotenv import load_dotenv
import boto3
import logging

logger = logging.getLogger(__name__)

load_dotenv()

api_key = os.getenv('AWS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_KEY')
bucket = os.getenv('AWS_BUCKET_NAME')
logger.info("Retrieved AWS keys")

s3_client = boto3.client(
    's3',
    aws_access_key_id = api_key,
    aws_secret_access_key = secret_key,
)

data = "data/2026-05-05_04-49-03.json"
filename = "2026-05-05_04-49-03.json"

s3_client.upload_file(data, bucket, filename)
logger.info(f"Uploaded {filename} to S3")
