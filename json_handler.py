import requests
import json

API_KEY   = 'KEY'
API_CALL_CSV = 'https://eodhistoricaldata.com/api/eod/SPY.US?api_token=demo&period=d&from=2022-01-01'
API_CALL  = 'https://eodhistoricaldata.com/api/options/SPY.US?api_token='+API_KEY+'&from=2022-01-01'
FILE_PATH = './data/spy_options_since_2021.json'

def get_json(call):
    response   = requests.get(API_CALL)
    dictionary = response.json()  # Converts to dictionary
    print('Received JSON data')
    return json.dumps(dictionary) # Converts to JSON string

def save_json(jsonString, path):
    with open(path, 'w') as outfile:
        outfile.write(jsonString)
    print('Saved JSON data to file')

def get_dict(path):
    with open(path) as json_file:
        data = json.load(json_file)
    
    return data

# Update API_CALL
# Change FILE_PATH
# Remove comment below
# Run file
#save_json(get_json(API_CALL), FILE_PATH)


