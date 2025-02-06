from src.utils import getFromConfigFile, getFromEnv

import requests
import pandas as pd

from datetime import datetime
from zoneinfo import ZoneInfo

def getFromApi(url: str = None, params: dict = None, headers: dict = None) -> dict:
    if url is None:
        raise Exception("No URL provided for the API request")

    response = requests.get(url, params=params, headers=headers) # Send the request

    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}")

    return response.json()

def getDataFromTwelveDataApi(symbol: str = None, interval: str = None, startDate: str = None, endDate: str = None) -> pd.DataFrame:
    if symbol is None or interval is None:
        raise Exception("Symbol and interval must be provided")
    
    # API informations
    api_key = getFromEnv("TWELVE_DATA_API_KEY")
    api_endpoint = getFromConfigFile("APIS", "Twelve Data Api", "Endpoint")

    # Set parameters for the request
    params = {
        'symbol': symbol,
        'interval': interval,
        'apikey': api_key
    }

    # All dates should be in Sydney time
    if startDate:
        params['start_date'] = startDate
    if endDate:
        params['end_date'] = endDate
    else:
        params['end_date'] = datetime.now(ZoneInfo('Australia/Sydney')).strftime('%Y-%m-%d %H:%M:%S') # If no end date, use current date
    
    data = getFromApi(api_endpoint, params)

    if 'values' not in data:
        raise Exception(f"Invalid data from TwelveData API ({data['message']})")
    
    data = pd.DataFrame(data['values'])
    data = data.reindex(index=data.index[::-1], ) # Old data first
    data = data.reset_index(drop=True)
    data = data[['datetime', 'open', 'high', 'low', 'close']]

    data['datetime'] = pd.to_datetime(data['datetime'])
    data.dropna(inplace=True) # Remove NaN values

    print(f"Received data from Twelve Data: {data.shape[0]} rows for symbol {symbol} and interval {interval}")

    return data