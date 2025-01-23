# Local imports
from src.log import displayError

# External imports
from datetime import datetime
from dotenv import load_dotenv

import json
import os
import requests

import pandas as pd

def getValueFromConfigFile(filePath: str = None, *keys: str) -> str:
    if filePath is None or keys is None:
        displayError("Both file path and key are required")
    
    if not os.path.exists(filePath):
        displayError("File not found")
    
    with open(filePath, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            displayError("Invalid JSON file")

    if not keys:
        displayError("At least one key is required")

    for key in keys:
        if key in data:
            data = data[key]
        else:
            displayError(f'Key "{key}" not found in file')

    return data

def getFromEnv(key: str) -> str:
    load_dotenv()

    value = os.getenv(key)

    if value is None:
        displayError(f'Key "{key}" not found in environment variables')
    
    return value

def getFromApi(url: str = None, params: dict = None, headers: dict = None) -> dict:
    if url is None:
        displayError("URL is required")

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        displayError(f"API request failed with status code {response.status_code}")

    return response.json()

def delNonAlphaChars(string: str) -> str:
    return ''.join(e for e in string if e.isalnum())

def isInTimeRange(time: pd.Timestamp, start: str, end: str) -> bool:
    try:
        current_time = time.time()
        start_time = datetime.strptime(start, "%H:%M").time()
        end_time = datetime.strptime(end, "%H:%M").time()

        if end_time < start_time: # if the range crosses midnight
            return current_time >= start_time or current_time <= end_time

        return start_time <= current_time <= end_time # standard case
    
    except ValueError:
        displayError("Invalid time format")