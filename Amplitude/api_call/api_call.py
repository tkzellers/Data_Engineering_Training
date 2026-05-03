import os
import requests
from dotenv import load_dotenv
import json
from io import BytesIO
import zipfile
import gzip
from datetime import datetime, timedelta
import time

load_dotenv()

# Read .env file
api_key = os.getenv('AMP_API_KEY')
secret_key = os.getenv('AMP_SECRET_KEY')
data_region = os.getenv('AMP_DATA_REGION')

base_url = "https://analytics.eu.amplitude.com/api/2/export"


start_time = (datetime.now() - timedelta(hours=24)).strftime('%Y%m%dT%H')
end_time = datetime.now().strftime('%Y%m%dT%H')

print(f"Start time: {start_time}, End time: {end_time}")

# start_time = input("Enter the start date for the data export (format: YYYYMMDD) or press t for today")
# end_time = input("Enter the end date for the data export (format: YYYYMMDD) or press enter to use the same date as the start date")

params = {
    'start': start_time,
    'end': end_time
}


#first script gets the response, records time, records size of the response.
start_time = time.process_time()
response = requests.get(base_url, params=params, auth=(api_key, secret_key))
response_code = response.status_code
response_message = response.text
response_size = len(response.content)
end_time = time.process_time()
print(f"Response code: {response_code}, Response message: {response.text}, Response size: {response_size} bytes, Response time: {end_time - start_time} seconds")



def extract_first_zip(response):
        #takes the response from the API call, keeping the data in memory with the BytesIO function, so that I can then
        #extract the zip files from that "virtual" zip file, and write those into a new directory called amplitude_data
        zip_bytes = BytesIO(response.content)
        with zipfile.ZipFile(zip_bytes, 'r') as z:
            z.extractall('amplitude_export_data') #One issue here is the 100011471 directory that gets created, where the .gz files are written. I hardcode this later. 

def filename_as_datetime(filename):
        #removes .gz from filename
        json_filename = filename[:-3]

def extract_second_gzip(filename):
            #uses gzip library to open and then read the .gz files, and converts the resulting arrangement of json lines into an
            #actual json array, which is then written into a new file, but with a proper .json file extension, and a name that is just the datetime
            #value from the original filename from amplitude.
            with gzip.open("amplitude_export_data/100011471/" + filename, 'rb') as gzfile:
                data = gzfile.read()
            json_string = data.decode('utf-8')
            json_lines = json_string.splitlines()
            json_data = []

            for line in json_lines:
                object = json.loads(line)
                json_data.append(object)
            
            #separate function to parse the filename into a datetime that might be easier to work with Snowflake?
            json_filename = filename_as_datetime(filename)

            with open(f'amplitude_export_data/{json_filename}', 'w') as json_file:
                #json_file.write(json_data)
                json.dump(json_data, json_file)

            print("Wrote jsonfname: " + json_filename)
            

#Running the functions
if response_code == 200:
    print(f"Connection Success - {response_code}")

    extract_first_zip(response)

    #100011471 is a hardcoded directory path, would like to make dynamic in the future.
    for filename in os.listdir("amplitude_export_data/100011471"):
        if filename.endswith('.gz'):
             extract_second_gzip(filename)
        else:
            print(f"{filename} is no a .gz file, skipped")

else: 
    print(f"Connection issue - {response_code}: {response.text}")
