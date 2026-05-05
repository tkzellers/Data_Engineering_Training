import os
from dotenv import load_dotenv

url = {}

load_dotenv()
# Read .env file
url['api_key'] = os.getenv('AMP_API_KEY')
url['secret_key'] = os.getenv('AMP_SECRET_KEY')
data_region = os.getenv('AMP_DATA_REGION')

api_key = os.getenv('AWS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_KEY')
bucket = os.getenv('AWS_BUCKET_NAME')

logger.info(f"Loaded API keys from .env")

url['base_url'] = "https://analytics.eu.amplitude.com/api/2/export"

