import os
import requests
from dotenv import load_dotenv
import json
from io import BytesIO
import zipfile
import gzip

load_dotenv()

# Read .env file
api_key = os.getenv('AMP_API_KEY')
secret_key = os.getenv('AMP_SECRET_KEY')
data_region = os.getenv('AMP_DATA_REGION')

base_url = "https://analytics.eu.amplitude.com/api/2/export"

#YYYYMMDDTHH (note the T in there is hard required)
start_time = '20260429T01'
end_time = '20260429T23'

params = {
    'start': start_time,
    'end': end_time
}

response = requests.get(base_url, params=params, auth=(api_key, secret_key))
response_code = response.status_code

print(f"Response Code: {response_code}")

zip_bytes = BytesIO(response.content)
with zipfile.ZipFile(zip_bytes, 'r') as z:
    z.extractall('amplitude_data')

print(os.listdir('amplitude_data'))

for filename in os.listdir("amplitude_data/100011471"):
    print(filename)
    if filename.endswith('.gz'):
        with gzip.open("amplitude_data/100011471/" + filename, 'rb') as gzfile:
            data = gzfile.read()
        
        json_string = data.decode('utf-8')
        json_lines = json_string.splitlines()
        json_data = []

        for line in json_lines:
            object = json.loads(line)
            json_data.append(object)

        #json_data = json.loads(json_string)

        json_filename = filename[:-3]
        print("jsonfname: " + json_filename)

        with open(f'amplitude_data/{json_filename}', 'w') as json_file:
            #json_file.write(json_data)
            json.dump(json_data, json_file)
    else:
        print(f"{filename} is no a .gz file, skipped")
        




# if response_code == 200:
#     with open('amplitude_data.json', 'w') as file:
#         json.dump(response.json(), file)
#     print("Data successfully downloaded and saved as amplitude_data.zip")
# else:
#     print(f"Failed to retrieve data. Status code: {response_code}, Response: {response.text}")  

# print(response.json())