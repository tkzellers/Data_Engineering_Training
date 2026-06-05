
from ipwhois import IPWhois

iplist = [
    "2.23.63.230", "3.117.209.254", "4.209.209.138", "5.148.67.114", "6.33.127.132",
    "7.115.107.176", "12.235.16.3", "14.2.39.182", "14.160.178.153", "18.132.218.41",
    "20.72.134.182", "24.206.70.41", "24.239.177.13", "27.67.214.254", "34.34.225.239",
    "37.130.253.2", "37.212.86.188", "42.112.41.244", "43.173.177.149", "43.173.182.137",
    "44.236.4.249", "45.91.112.114", "47.18.207.218", "47.128.49.5", "47.128.49.6",
    "47.128.49.7", "47.128.49.224", "47.128.49.225", "49.34.195.39", "49.43.32.179",
    "49.43.119.72", "49.43.224.180", "49.206.9.205", "52.23.63.230", "58.187.6.148",
    "62.7.230.4", "65.49.101.219", "66.78.213.134", "66.78.213.136", "66.78.213.139",
    "66.78.213.140", "66.108.235.190", "69.241.43.220", "70.160.198.146", "72.136.106.182",
    "76.33.127.132", "76.46.19.3", "79.117.198.87", "79.181.133.7", "81.17.55.33",
    "81.96.125.44", "81.152.248.223", "81.158.130.101", "82.15.191.251", "82.129.10.241",
    "82.197.46.185", "83.48.120.123", "85.115.43.2", "86.190.67.139", "87.115.107.176",
    "89.40.212.226", "90.219.89.226", "90.221.168.6", "90.243.182.2", "91.73.26.127"
]
#['147.197.52.59','192.193.13.16','213.86.87.74']



# for i in iplist:
#     obj = IPWhois(i)
#     result = obj.lookup_rdap()

import json

with open('blah.json', 'r', encoding='utf-8') as file:
    result = json.load(file)

name = contact.get('name')
netwk_name = result['network']['name']

try:
    netwk_desc = result['network']['remarks'][0]['description']
except:
    netwk_desc = None

objects_list = []
objects = result.get('objects', {})
for key in objects:
    contact = objects[key].get('contact', {})
    contact_address = contact.get('address', {})
    try:
        # contact_address = contact_address[0]
        contact_address = contact_address[0].get('value', 0)
        # contact_address = contact_address.split('\n')[0:]
        # contact_address = ", ".join(contact_address)
    except:
        contact_address = None
    name = contact.get('name')

##---SOMETHING TO TRY
# def format_contact_address(contact):
#     address = contact.get("address")
#     if not isinstance(address, list) or not address:
#         return None

#     value = address[0].get("value", "")
#     if not isinstance(value, str):
#         return None

#     return ", ".join(value.splitlines())

# objects_list = []
# for obj in result.get("objects", {}).values():
#     contact = obj.get("contact", {})
#     contact_address = format_contact_address(contact)
#     objects_list.append(contact_address)




#Create a table
#insert into that table from this script


print('-------new-------')
print(f'network_description: {netwk_desc}')
print(f'network_name: {netwk_name}')
print(f'name: {name}')
print(f'address: {contact_address}')

#two different regex queries
#one for "name"
#one for "address", with "value"

# print(re.findall("'name':( .*?),", str(result)))
# print(re.findall("'value':( .*?)\n", str(result)))

#print(str(result))

#result = json.dumps(result)
