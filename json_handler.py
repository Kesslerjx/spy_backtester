import requests
import json

API_CALL  = 'https://eodhistoricaldata.com/api/options/SPY.US?api_token=62fe673465ec30.58512842&from=2022-04-21'
FILE_PATH = './data/spy_options_data.json'

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



