#Extract Basics
#TFL Bike Points
#1. Read the Documentation
#2. Make a Repo, folder, .py file
#3. Start scripting
#4. Import packages



import requests
import json
from datetime import datetime

# Getting the current date and time
current_time = datetime.now()

#Set Variables (URLs, parameters, etc)
base_url = "https://api.tfl.gov.uk/BikePoint"

full_response = requests.get(base_url)
num_bikepoints = len(full_response.json())

response = requests.get(base_url)
response_code = response.status_code
data = response.json()

for num in range(num_bikepoints):
    id = data[num]['id']
    blob = data[num]
    with open((f"bikepoint_{id}_data.json"), "w") as file:
        json.dump(blob, file)






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









