from datetime import datetime
import json
import os
import pandas as pd

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

def delNonAlphaChars(string: str) -> str:
    return ''.join(e for e in string if e.isalnum()) # Keep only alphanumeric characters

def isInTimeRange(time: pd.Timestamp, start: str, end: str) -> bool:
    try:
        current_time = time.time()
        start_time = datetime.strptime(start, "%H:%M").time()
        end_time = datetime.strptime(end, "%H:%M").time()

        if end_time < start_time: # if the range crosses midnight
            return current_time >= start_time or current_time <= end_time

        return start_time <= current_time <= end_time # standard case
    
    except ValueError:
        print("Invalid time format")