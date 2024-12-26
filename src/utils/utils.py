import json
import os
import requests
from dotenv import load_dotenv
import pandas as pd
from src.utils.log import displayError

def getValueFromConfigFile(filePath: str = None, *keys: str) -> str:
    if filePath is None or keys is None:
        displayError("Both file path and key are required")
    
    filePath = 'src/' + filePath
    
    if not os.path.exists(filePath):
        displayError("File not found")
    
    with open(filePath, 'r') as file:
        data = json.load(file)

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

def setIndex(data: pd.DataFrame, index: str = None) -> None:
    if index is None:
        displayError("Index must be provided")
    
    if index not in data.columns:
        displayError(f"Index {index} not found in data")
    
    if index  == 'datetime':
        data['datetime'] = pd.to_datetime(data['datetime'])
    
    data.set_index('datetime', inplace=True)

    return data