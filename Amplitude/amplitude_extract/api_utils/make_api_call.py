#Function to call any API and get the response data (in bytes) and response code
#Also includes logging data


import time
import requests
import logging

logger = logging.getLogger(__name__)

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