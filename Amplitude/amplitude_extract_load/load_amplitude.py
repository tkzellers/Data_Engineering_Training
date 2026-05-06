import boto3
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

def load_s3(data_dir):
    ##### AWS Keys #######
    load_dotenv()
    api_key = os.getenv('AWS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_KEY')
    bucket = os.getenv('AWS_BUCKET_NAME')
    logger.info("Retrieved AWS keys")
    ##### AWS Keys #######

    ##### AWS Client #######
    s3_client = boto3.client(
        's3',
        aws_access_key_id = api_key,
        aws_secret_access_key = secret_key,
    )
    ##### AWS Client #######
    logger.info(f"Established connection with '{bucket}'")

    #Source folder from function input (which is data_dir initialized in the main function)
    folder_path = os.path.join(data_dir) 

    #Iterate through files in the data_dir, upload, and then delete them.
    for root,_,files in os.walk(folder_path):
        filecount_start = len(files)
        filecount_end = len(files)
        print(f"{filecount_start} files to upload")
        logger.info(f"{len(files)} files to upload from {data_dir}")
        for filename in files:
            if filename.endswith('.json'):
                source_path = os.path.join(root, filename)
                try:
                    s3_client.upload_file(source_path, bucket, filename)
                    #print(f"{filename} was uploaded to S3")    
                    s3_client.head_object(Bucket = bucket, Key = filename) #checks if the file exists in s3, would error if it doesn't
                    os.remove(source_path) #Will remove files after successful upload
                    filecount_end -= 1
                except Exception as e:
                    print(e)
                    logger.error(e)

    print(f"Uploaded {filecount_start - filecount_end} files to {bucket}")
    logger.info(f"Uploaded {filecount_start - filecount_end} files to {bucket}")