import re
import os
from ipwhois import IPWhois
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

def get_ip_info(ip):
        '''
        Takes an IP address and returns a dict of name, address, and network name 
        associated with that IP address - using the "ipwhois" library.
        This function will be used as a .map() function.

        arguments: ip = string, an IP address. 
        '''
        try:
            obj = IPWhois(ip) #prepare an 'obj' to lookup using ipwhois
            result = obj.lookup_rdap() #lookup the IP address using the rdap/whois servers, return a python dictionary
            try:
                netwk_name = result['network']['name']
            except: 
                netwk_name = None
            objects = result.get('objects', {})
            for key in objects:   
                contact = objects[key].get('contact', {})
                name = contact.get('name')
                contact_address = contact.get('address', {})
                try:
                    contact_address = contact_address[0].get('value', 0)
                except:
                    contact_address = None
                
                return {'name':name, 'contact_address':contact_address, 'netwk_name': netwk_name}}
        except:
            return {'name':None, 'contact_address': None, 'netwk_name': None}
        

def load_ips(s3_client):
    ips = []
    folder_path = os.path.join('amplitude_export_data')
    logger.info(f"Retrieving data from local storage at '{folder_path}'")
    print(folder_path)

    for root,_,files in os.walk(folder_path):
        for filename in files:
            #print(filename)
            file_path = os.path.join(root, filename)
            
            #print(file_path)
            
            with open(file_path, 'r') as file:
                for line in file:
                    address = re.findall(r'"ip_address":"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"', line)
                    ips.append(address)
    iplist = [item for sublist in ips for item in sublist] #make the list of lists into just a list (lol)
    iplist = list(set(iplist)) #dedupe the list
    print((f'{len(iplist)} ip addresses to process'))
    df = pd.DataFrame(iplist)
    df.columns = ['IP']
    # print(df.head())
    bucket = os.getenv('AWS_BUCKET_NAME')
    df['ipinfo_raw'] = df.map(get_ip_info)
    #print(df)
    j = df.to_json(orient='records')
    #print(j)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H')
    #print(str(timestamp))
    aws_destination = 'ipaddress_export/' + str(timestamp)
    #print(aws_destination)

    # for j in json_list:
    #     print(j)
    try:
        s3_client.put_object(
            Bucket = bucket, 
            Key = aws_destination, 
            Body = j,
            ContentType = 'application/json')
                            
        #print(f"{j} was uploaded to S3")    
        s3_client.head_object(Bucket = bucket, Key = aws_destination) #checks if the file exists in s3, would error if it doesn't
        #filecount_end -= 1
    except Exception as e:
            print(e)









#df[['netwk_desc', 'netwk_name', 'name', 'contact_address']] = df['ipinfo_raw'].str.split(',', expand=True)




        # print('-------new-------')
        # print(f'network_description: {netwk_desc}')
        # print(f'network_name: {netwk_name}')
        # print(f'objects: {name}, {contact_address}')





    #     for line in filename:
    #         address = re.findall(r'"ip_address":.*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
    #         ips.append(address)
    # flist = [item for sublist in ips for item in sublist]
    # print(flist)
#after this, need to run it through ipwhois script and turn it into a table or json or something to load into s3?