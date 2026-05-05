import tempfile

from api_utils.make_api_call import make_api_call
from api_utils.url_constructor import construct_url
from logging_utils.setup_logging import setup_logging
from unzip_copy_utils.unzip_copy import extract_first_zip, extract_second_gzip

print("Imported tools")
print("Starting Amplitude data extraction script")





##===============================================================================##
#Running the functions

logger = setup_logging()

temp_dir = tempfile.mkdtemp() #make a temp directory to store the unzipped output 

url = construct_url()

response_and_code = make_api_call(url['base_url'], url['params'], url['api_key'], url['secret_key'])

response = response_and_code[0]
response_code = response_and_code[1]    

if response_code == 200:
    
    extract_first_zip(response, temp_dir)
    
    extract_second_gzip(temp_dir)

else: 
    print(f"Connection issue - {response_code}: {response.text}")
