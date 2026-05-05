#Extract Basics
#TFL Bike Points
#1. Read the Documentation
#2. Make a Repo, folder, .py file
#3. Start scripting
#4. Import packages

import requests
import json
from datetime import datetime
import os   
import time
import logging
import os
from dotenv import load_dotenv
import boto3

# Getting the current date and time
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

######Log Setup
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

log_filename = (f"{log_dir}/{current_time}.log")

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_filename
    )

logger = logging.getLogger() 
logger.info("Logger initiated")
#######Log Setup


# #######Get Keys
# load_dotenv()
# api_key = os.getenv('AWS_KEY_ID')
# secret_key = os.getenv('AWS_SECRET_KEY')
# bucket = os.getenv('AWS_BUCKET_NAME')
# logger.info("Retrieved AWS keys")

# s3_client = boto3.client(
#     's3',
#     aws_access_key_id = api_key,
#     aws_secret_access_key = secret_key,
# )
# ########Get Keys



#Set Variables (URLs, parameters, etc)
base_url = "https://api.tfl.gov.uk/BikePoint"

response = requests.get(base_url)
response_code = response.status_code

data_dir = "data"
os.makedirs(data_dir, exist_ok=True)

attempt_counter = 0
while attempt_counter < 4:
    
    if 200 <= response_code < 300:
        data = response.json()
        num_bikepoints = len(data)
        filename = (f"{data_dir}/{current_time}.json")
        
        
        with open(filename, "w") as file:
                json.dump(data, file)

        # #aws boto3 file upload, replaces the above open()
        # s3_client.upload_file(data, bucket, filename)
        # logger.info(f"Uploaded {filename} to S3")

        print(f'File {filename} was created - Success!')
        logger.info(f'File {filename} was created - Success!')
        break
    
    elif response_code >= 500:
        #do a retry
        time.sleep(30) #wait for 5 seconds before retrying
        attempt_counter += 1
        print(f"Attempt {attempt_counter}: Server error, retrying...")
        logger.info(f"Attempt {attempt_counter}: Server error, retrying...")
        
        if attempt_counter >= 4:
             print(f"Too many attempts, connection failed, ending process")
             logger.error("Server connection issue")
    
    else :
        print(f"Error making API call, response code: {response_code}")
        logger.info(f"Error making API call, response code: {response_code}")
        break




    # for num in range(10): #range(num_bikepoints):
    #     id = data[num]['id']
    #     blob = data[num]
    #     with open((f"data/bikepoint_{id}_data.json"), "w") as file:
    #         json.dump(blob, file)


# for num in range(num_bikepoints):
#    id = data[0]['id']
#    bikepoint_url = base_url + "/" + id
#    filename = (f"{id}.json_{current_time}")
#    if response_code == 200:
# #write the data into a file
#     try:
#         with open(f"bikepoint_{num}_data.json", "w") as file:
#             json.dump(data, file)
#     except:
#         print("Error writing file")
#         print(f'File {filename} was created - Success!')
#     else:
#         print(f'Error creating {filename}:')
#         print(data.get("message", "no message given"))









