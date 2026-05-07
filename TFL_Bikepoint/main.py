#Extract Basics
#TFL Bike Points
#1. Read the Documentation
#2. Make a Repo, folder, .py file
#3. Start scripting
#4. Import packages

from datetime import datetime
import os   
from dotenv import load_dotenv
from pathlib import Path

from modules.setup_logging import setup_logging
from modules.extract import extract_api
from modules.load import load_data

# Getting the current date and time
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

######Log Setup
logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
logger = setup_logging(logs_dir)
logger.info("Logger initiated")
#######Log Setup

#######Set Variables
base_url = "https://api.tfl.gov.uk/BikePoint"


if extract_api(base_url, 4, 'data') == True:
    data_dir = Path('data')
    load_data(data_dir)





#=== old stuff ===#

# log_dir = "logs"
# os.makedirs(log_dir, exist_ok=True)

# log_filename = (f"{log_dir}/{current_time}.log")

# logging.basicConfig(
#     level=logging.INFO, 
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     filename=log_filename
#     )


# response = requests.get(base_url)
# response_code = response.status_code
# data_dir = "data"
# os.makedirs(data_dir, exist_ok=True)
# attempt_counter = 0
# max_attempts = 4
# while attempt_counter < max_attempts:
    
#     if 200 <= response_code < 300:
#         data = response.json()
#         num_bikepoints = len(data)
#         filename = (f"{data_dir}/{current_time}.json")
        
        
#         with open(filename, "w") as file:
#                 json.dump(data, file)

#         print(f'File {filename} was created - Success!')
#         logger.info(f'File {filename} was created - Success!')
#         break
    
#     elif response_code >= 500:
#         #do a retry
#         time.sleep(30) #wait for 5 seconds before retrying
#         attempt_counter += 1
#         print(f"Attempt {attempt_counter}: Server error, retrying...")
#         logger.info(f"Attempt {attempt_counter}: Server error, retrying...")
        
#         if attempt_counter >= 4:
#              print(f"Too many attempts, connection failed, ending process")
#              logger.error("Server connection issue")
    
#     else :
#         print(f"Error making API call, response code: {response_code}")
#         logger.info(f"Error making API call, response code: {response_code}")
#         break




    # for num in range(10): #range(num_bikepoints):
    #     id = data[num]['id']
    #     blob = data[num]
    #     with open((f"data/bikepoint_{id}_data.json"), "w") as file:
    #         json.dump(blob, file)


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









