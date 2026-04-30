import os
from mailchimp_marketing import Client
from dotenv import load_dotenv
import json

load_dotenv()

# Read .env file
api_key = os.getenv('MC_API_KEY')
server_prefix = os.getenv('MC_SERVER_PREFIX')

mailchimp = Client()
mailchimp.set_config({
  "api_key": api_key,
  "server": server_prefix
})

response = mailchimp.ping.get()
print(response)

campaigns = mailchimp.campaigns.list()

with open('campaigns.json', 'w') as f:
    json.dump(campaigns, f, indent=4)