#Extract Basics

#TFL Bike Points

#1. Read the Documentation
#2. Make a Repo, folder, .py file
#3. Start scripting
#4. Import packages
#5. Set Variables (URLs, parameters, etc)
#6. Check status code

import requests
import json
from datetime import datetime

# Getting the current date and time
current_time = datetime.now()

base_url = "https://api.tfl.gov.uk/BikePoint"
id = "BikePoints_1"
bikepoint_url = base_url + "/" + id

#call the api
response = requests.get(bikepoint_url)
response_code = response.status_code

#put the actual response json into a variable called data
data = response.json()

filename = (f"{id}.json_{current_time}")
 
if response_code == 200:
    #write the data into a file
    try:
        with open("bikepoint_1_data.json", "w") as file:
         json.dump(data, file)
    except:
       print("Error writing file")
    print(f'File {filename} was created - Success!')
 
else:
    print(f'Error creating {filename}:')
    print(data.get("message", "no message given"))

  





