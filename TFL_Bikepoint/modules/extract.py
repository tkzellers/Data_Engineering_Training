import logging
import os
from datetime import datetime
import time
import requests
import json


logger = logging.getLogger(__name__)

def extract_api(base_url, max_attempts, dir):
    """Calls API with base_url, and extracts data into a directory (dir). If 500 error, will try (max_attempts) number of times

    Args:
        base_url (str): url for API
        max_attempts (int): number of times to retry if server is non responsive
        dir (str): directory name for extracted data
    """    

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    response = requests.get(base_url)
    response_code = response.status_code

    data_dir = dir
    os.makedirs(data_dir, exist_ok=True)

    attempt_counter = 0
    while attempt_counter < max_attempts:
        
        if 200 <= response_code < 300:
            data = response.json()
            num_bikepoints = len(data)
            filename = (f"{data_dir}/{current_time}.json")
            
            
            with open(filename, "w") as file:
                    json.dump(data, file)

            print(f'File {filename} was created - Success!')
            logger.info(f'File {filename} was created - Success!')
            return True
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
    
