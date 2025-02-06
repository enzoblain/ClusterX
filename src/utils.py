import json
import os

def getFromEnv(key: str) -> str:
    value = os.getenv(key)

    if value is None:
        raise Exception(f"Missing environment variable: {key}")
    
    return value

def getFromConfigFile(*keys: str) -> str:
    if not keys:
        raise Exception("At least one key is required")

    filepath = 'config.json'
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(filepath, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            raise Exception("Invalid JSON file")

    for key in keys: # Loop through keys
        if key in data: # Check if key exists in the selected data
            data = data[key]
        else:
           raise Exception(f'Key "{key}" not found in file')

    return data