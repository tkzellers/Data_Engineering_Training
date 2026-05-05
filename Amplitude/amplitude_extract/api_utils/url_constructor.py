import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


def construct_url():
    url = {}

    load_dotenv()
    # Read .env file
    url['api_key'] = os.getenv('AMP_API_KEY')
    url['secret_key'] = os.getenv('AMP_SECRET_KEY')
    data_region = os.getenv('AMP_DATA_REGION')
    logger.info(f"Loaded API keys from .env")

    url['base_url'] = "https://analytics.eu.amplitude.com/api/2/export"

    start_time = (datetime.now() - timedelta(hours=24)).strftime('%Y%m%dT%H')
    end_time = datetime.now().strftime('%Y%m%dT%H')

    print(f"Start time: {start_time}, End time: {end_time}")
    logger.info(f"Recognized start time: {start_time} and end time: {end_time}")

    # start_time = input("Enter the start date for the data export (format: YYYYMMDD) or press t for today")
    # end_time = input("Enter the end date for the data export (format: YYYYMMDD) or press enter to use the same date as the start date")

    url['params'] = {
        'start': start_time,
        'end': end_time
    }

    return url