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


response = requests.get(base_url)


data = response.json()


print(response.json())

