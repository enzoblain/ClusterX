import json
import os
import requests
from dotenv import load_dotenv
import pandas as pd

def getValueFromConfigFile(filePath: str = None, *keys: str) -> str:
    if filePath is None or keys is None:
        raise ValueError("Both file path and key are required")
    
    filePath = 'src/' + filePath
    
    if not os.path.exists(filePath):
        raise FileNotFoundError("File not found")
    
    with open(filePath, 'r') as file:
        data = json.load(file)

    for key in keys:
        if key in data:
            data = data[key]
        else:
            raise KeyError(f'Key "{key}" not found in file')

    return data

def getFromEnv(key: str) -> str:
    load_dotenv()

    value = os.getenv(key)

    if value is None:
        raise KeyError(f'Key "{key}" not found in environment variables')
    
    return value

def getFromApi(url: str = None, params: dict = None, headers: dict = None) -> dict:
    if url is None:
        raise ValueError("URL is required")

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}")

    return response.json()

def delNonAlphaChars(string: str) -> str:
    return ''.join(e for e in string if e.isalnum())

def setDatetimeIndex(data: pd.DataFrame) -> None:
    data['datetime'] = pd.to_datetime(data['datetime'])
    data.set_index('datetime', inplace=True)

    return data

def getDataFrameFromCsv(filepath: str = None, index: str = None) -> pd.DataFrame:
    if filepath is None:
        raise ValueError("File path must be provided")
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File {filepath} not found")
    
    data = pd.read_csv(filepath)

    if index:
        return data.set_index(index)
    
    return data