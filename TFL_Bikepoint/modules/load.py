import requests
import json
from datetime import datetime
import os   
import time
import logging
import os
from dotenv import load_dotenv
import boto3

logger = logging.getLogger(__name__)

def load_data(data_dir):
    """_summary_

    Args:
        data_dir (str): directory for data to be loaded
    """    

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

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

    folder_path = os.path.join(data_dir)

    for root,_,files in os.walk(folder_path):
        processed = 0
        logger.info(f"{len(files)} files to be processed")
        print(f"{len(files)} files to be processed")
        for filename in files:
            if filename.endswith('.json'):
                source_path = os.path.join(root, filename)
                try:
                    s3_client.upload_file(source_path, bucket, filename)
                    #print(f"{filename} was uploaded to S3")    
                    s3_client.head_object(Bucket = bucket, Key = filename) #checks if the file exists in s3, would error if it doesn't, so we're 
                    os.remove(source_path)
                    processed += 1
                except Exception as e:
                    logging.error(e)
                    print(e)
                
                print(f"Processed {processed} files")
                logger.info(f"Processed {processed} files")
                
                #return True 
    
