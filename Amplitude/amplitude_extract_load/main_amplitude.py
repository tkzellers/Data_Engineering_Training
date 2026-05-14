import tempfile
import os
import time

from utils.api import make_api_call
from utils.api import construct_url
from utils.setup_logging import setup_logging
from utils.unzip_copy import extract_zip, extract_second_gzip
from load_amplitude import load_s3, aws_client
from extract_ipaddress import load_ips, get_ip_info

print("Imported tools and modules")
print("Starting Amplitude data extraction script")

#Running the functions#

#==========Intiate Logging==========#
logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs') #make a permanent path for the logs files
logger = setup_logging(logs_dir)
logger.info("Logger initiated")
print(logs_dir)
#==========#


#==========Setup Directories I need in Functions==========#
temp_dir = tempfile.mkdtemp() #make a temp directory to store the unzipped output
data_dir = "amplitude_export_data"
os.makedirs(data_dir, exist_ok=True) #make a new directory for outputting the data
#==========#
logger.info(f"Directories created, temporary: {temp_dir}, data: {data_dir}")

#==========Build URL==========#
url = construct_url()
#==========#
logger.info("URL Contrcuted")


attempt_counter = 1
while attempt_counter < 4:

    #==========Make the API Call and Get the outputs
    logger.info("Begin API Call")
    response_and_code = make_api_call(url['base_url'], url['params'], url['api_key'], url['secret_key'])
    response = response_and_code[0]
    response_code = response_and_code[1]
    #==========#
    logger.info("Finished API Call")

    if 200 <= response_code < 300:
        
        #==========Unzip and copy the downloaded files into the data directory==========#
        print("Begin Unzipping and Copying")
        logger.info("Begin Unzipping and Copying")
        extract_zip(response, temp_dir)
        extract_second_gzip(temp_dir, data_dir)
        #==========#
        logger.info("Finished Unzipping and Copying")


        #==========Load the files from data directory into s3 (and delete them from disk)==========#
        print("Begin Loading to S3")
        logger.info("Begin Loading to S3")
        s3_client = aws_client()
        
        
        load_ips(s3_client)


        load_s3(data_dir, s3_client)
        #==========#
        logger.info("Finished loading to S3")
        break
    
    #==========Conditionals for connection issues/errors==========#
    elif response_code >= 500:
        print(f"Server issue - {response_code}: {response.text}")
        logger.info(f"Server issue - Trying Server Again - Attempt number {attempt_counter}")
        time.sleep(30)
        attempt_counter += 1

        if attempt_counter >= 4:
            print(f"Too many attempts, connection failed, ending process")
            logger.error(f"Server failure - {response_code}: {response.text}")
            raise RuntimeError(f"Server failure - {response_code}: {response.text}")
            break

    else: 
        print(f"Connection issue - {response_code}: {response.text}")
        logger.error(f"Response is {response_code}: {response.text}")
        raise RuntimeError(f"Connection issue - {response_code}: {response.text}")
        break



