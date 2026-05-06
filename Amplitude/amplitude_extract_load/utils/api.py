#Function to call any API and get the response data (in bytes) and response code
#Also includes logging data


import time
import requests
import logging
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

api_logger = logging.getLogger("utils.setup_logging" + __name__)


def construct_url():
    url = {}

    load_dotenv()
    # Read .env file
    url['api_key'] = os.getenv('AMP_API_KEY')
    url['secret_key'] = os.getenv('AMP_SECRET_KEY')
    data_region = os.getenv('AMP_DATA_REGION')
    api_logger.info(f"Loaded API keys from .env")

    url['base_url'] = "https://analytics.eu.amplitude.com/api/2/export"

    start_time = (datetime.now() - timedelta(hours=24)).strftime('%Y%m%dT%H')
    end_time = datetime.now().strftime('%Y%m%dT%H')

    print(f"Start time: {start_time}, End time: {end_time}")
    api_logger.info(f"Recognized start time: {start_time} and end time: {end_time}")

    # start_time = input("Enter the start date for the data export (format: YYYYMMDD) or press t for today")
    # end_time = input("Enter the end date for the data export (format: YYYYMMDD) or press enter to use the same date as the start date")

    url['params'] = {
        'start': start_time,
        'end': end_time
    }

    return url



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
    api_logger.info(f"API call made to {base_url} with params {params}. Response code: {response_code}, Response size: {response_size} bytes, Response time: {end_time - start_time} seconds")

    return response, response_code


