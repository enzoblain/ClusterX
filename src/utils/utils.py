import json
import os
from dotenv import load_dotenv

def getValueFromConfigFile(filePath: str = None, *keys: str) -> str:
    if filePath is None or keys is None:
        raise ValueError("Both file path and key are required")
    
    filePath = 'config/' + filePath
    
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