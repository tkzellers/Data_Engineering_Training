import os
from dotenv import load_dotenv
from io import BytesIO
import zipfile
import gzip
from datetime import datetime, timedelta
import time
import shutil
import tempfile
import logging

logger = logging.getLogger(__name__)


def extract_zip(response, temp_dir):
        #takes the response from the API call, keeping the data in memory with the BytesIO function, so that I can then
        #extract the zip files from that "virtual" zip file, and write those into a newly made temp directory 
        
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
        print(f"Extracted successfully into {temp_dir}. Extract time: {end_extract - start_extract} seconds")
        logger.info(f"Extracted successfully into {temp_dir}. Extract time: {end_extract - start_extract} seconds")
        return temp_dir #return the temp directory so that we can use it in the next function to find the gz files to extract


def extract_second_gzip(directory, data_dir):
    '''directory is always the temp_dir we created in the first extraction function '''

    # data_dir = "amplitude_export_data"
    # os.makedirs(data_dir, exist_ok=True) #make a new directory for outputting the data
    logger.info(f"Amplitude_export_data directory created")

##======= Find the unzipped folder named after TIL's Account number ======##
    try:
        unzipped_folder = next(f for f in os.listdir(directory) if f.isdigit()) #take the first folder that is named as a digit, which we know is always the one we want (the only one)
        folder_path = os.path.join(directory, unzipped_folder) #make a path to the unzipped folder 
    except:
        print("Error finding unzipped folder")
        logger.error("Error finding unzipped folder")

##========##

    for root,_,files in os.walk(folder_path): #get into the unzipped folder, call out the files from the touple created by os.walk()
        print(f"Extracting and Copying {len(files)} files") 
        for filename in files:
            if filename.endswith('.gz'):
                gz_path = os.path.join(root, filename)
                json_filename = filename[:-3] 
                output_path = os.path.join(data_dir, json_filename)
                with gzip.open(gz_path, 'rb') as gz_file, open(output_path, 'wb') as out_file:
                    shutil.copyfileobj(gz_file, out_file) #copyfileobj is a function that copies the data from the gz file to the json file, without having to read the entire file into memory at once
                #print("Wrote jsonfname: " + json_filename)
            else:
                print(f"{filename} is not a .gz file, skipped")
    logger.info(f"Processed all files and copied into {data_dir}")
    shutil.rmtree(directory)
    logger.info(f"Removed temporary directory")