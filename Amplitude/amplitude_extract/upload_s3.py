import boto3
import os
from dotenv import load_dotenv

##### AWS Keys
load_dotenv()
api_key = os.getenv('AWS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_KEY')
bucket = os.getenv('AWS_BUCKET_NAME')
#logger.info("Retrieved AWS keys")
##### AWS Keys

##### AWS Client
s3_client = boto3.client(
    's3',
    aws_access_key_id = api_key,
    aws_secret_access_key = secret_key,
)
##### AWS Client

#where am I looking
folder_path = os.path.join('amplitude_export_data') #change this to be data_dir later?

processed = 0

for root,_,files in os.walk(folder_path):
    print(f"{len(files)} files to upload")
    for filename in files:
        if filename.endswith('.json'):
            source_path = os.path.join(root, filename)
            try:
                s3_client.upload_file(source_path, bucket, filename)
                print(f"{filename} was uploaded to S3")    
                s3_client.head_object(Bucket = bucket, Key = filename) #checks if the file exists in s3, would error if it doesn't, so we're 
                os.remove(source_path) #Will remove files after successful upload
                processed += 1
            except Exception as e:
                print(e)
                #logging.error(e)

print(f"Processed {processed} files")