import os
import requests
from dotenv import load_dotenv
import json
from io import BytesIO
import zipfile
import gzip
from datetime import datetime, timedelta
import time
import shutil
import tempfile


# Define Logging
import logging
from datetime import datetime

os.makedirs("logs", exist_ok=True)

# Set Log filepath location
log_filename = f"logs/amplitude_extract_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Configure logs to retrieve INFO messages and higher
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_filename
)

logger = logging.getLogger(__name__) #this takes the name of the current module (file) as the logger name, which is a common practice in Python logging

def make_api_call(base_url, params, api_key, secret_key):
    #first function gets the response, records time, records size of the response.
    start_time = time.process_time()
    response = requests.get(base_url, params=params, auth=(api_key, secret_key))
    #response info
    response_code = response.status_code
    response_size = len(response.content)
    end_time = time.process_time()
    #print response info
    print(f"Response code: {response_code}, Response size: {response_size} bytes, Response time: {end_time - start_time} seconds")
    logger.info(f"API call made to {base_url} with params {params}. Response code: {response_code}, Response size: {response_size} bytes, Response time: {end_time - start_time} seconds")

    return response, response_code

def extract_first_zip(response):
        #takes the response from the API call, keeping the data in memory with the BytesIO function, so that I can then
        #extract the zip files from that "virtual" zip file, and write those into a newly made temp directory 
        
        temp_dir = tempfile.mkdtemp() #make a temp directory to store the unzipped output 
        try:
            zip_bytes = BytesIO(response.content) #data is read into memory as a zip file, without writing it to disk first
        except:
            print("Error reading zip file from response")
            logger.error("Error reading zip file from response")
            return None
        start_extract = time.process_time()
        with zipfile.ZipFile(zip_bytes, 'r') as z:
            z.extractall(temp_dir) #extract the zip file into the temp directory 
        end_extract = time.process_time()
        logger.info(f"Extracted zip folder successfully. Extract time: {end_extract - start_extract} seconds")
        return temp_dir #return the temp directory so that we can use it in the next function to find the gz files to extract

def extract_second_gzip(directory):
    '''directory is always the temp_dir we created in the first extraction function '''

    data_dir = "amplitude_export_data"
    os.makedirs(data_dir, exist_ok=True) #make a new directory for outputting the data
    logger.info(f"Amplitude_export_data directory created")
    
    unzipped_folder = next(f for f in os.listdir(directory) if f.isdigit()) #take the first folder that is named as a digit, which we know is always the one we want (the only one)
    folder_path = os.path.join(directory, unzipped_folder) #make a path to the unzipped folder 
    
    for root,_,files in os.walk(folder_path): #get into the unzipped folder, call out the files from the touple created by os.walk()
        print(f"Reading {len(files)} files") 
        for filename in files:
            if filename.endswith('.gz'):
                gz_path = os.path.join(root, filename)
                json_filename = filename[:-3] 
                output_path = os.path.join(data_dir, json_filename)
                with gzip.open(gz_path, 'rb') as gz_file, open(output_path, 'wb') as out_file:
                    shutil.copyfileobj(gz_file, out_file) #copyfileobj is a function that copies the data from the gz file to the json file, without having to read the entire file into memory at once
                print("Wrote jsonfname: " + json_filename)
            else:
                print(f"{filename} is not a .gz file, skipped")
    logger.info(f"Processed all files and copied into {data_dir}")
    shutil.rmtree(temp_dir)
    logger.info(f"Removed temporary directory")


load_dotenv()
# Read .env file
api_key = os.getenv('AMP_API_KEY')
secret_key = os.getenv('AMP_SECRET_KEY')
data_region = os.getenv('AMP_DATA_REGION')
logger.info(f"Loaded API keys from .env")

base_url = "https://analytics.eu.amplitude.com/api/2/export"

start_time = (datetime.now() - timedelta(hours=24)).strftime('%Y%m%dT%H')
end_time = datetime.now().strftime('%Y%m%dT%H')

print(f"Start time: {start_time}, End time: {end_time}")
logger.info(f"Recognized start time: {start_time} and end time: {end_time}")

# start_time = input("Enter the start date for the data export (format: YYYYMMDD) or press t for today")
# end_time = input("Enter the end date for the data export (format: YYYYMMDD) or press enter to use the same date as the start date")

params = {
    'start': start_time,
    'end': end_time
}
            
#Running the functions
response_and_code = make_api_call(base_url, params, api_key, secret_key)

response = response_and_code[0]
response_code = response_and_code[1]    

if response_code == 200:
    
    temp_dir = extract_first_zip(response)
    
    extract_second_gzip(temp_dir)

else: 
    print(f"Connection issue - {response_code}: {response.text}")
