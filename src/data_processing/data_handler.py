import pandas as pd
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from src.utils.utils import getFromApi, getValueFromConfigFile
from src.utils.log import displayError
from src.utils.utils import setIndex

def getDataFromTwelveDataAPI(api_key: str = None, symbol: str = None, startDate: str = None, endDate: str = None, interval: str = None) -> pd.DataFrame:
    if api_key is None or symbol is None or interval is None:
        displayError("API key, symbol and interval must be provided")

    url = getValueFromConfigFile('config.json', 'API', 'API url')
    
    params = {
        'symbol': symbol,
        'interval': interval,
        'apikey': api_key
    }

    if startDate:
        params['start_date'] = startDate
    if endDate:
        params['end_date'] = endDate
    else:
        params['end_date'] = datetime.now(ZoneInfo('Australia/Sydney')).strftime('%Y-%m-%d %H:%M:%S')
    
    data = getFromApi(url, params)

    if 'values' not in data:
        displayError(f"Invalid data from TwelveData API ({data['message']})")
    
    data = pd.DataFrame(data['values'])

    data = setIndex(data, 'datetime')
    
    data = data[~data.index.duplicated(keep='first')]
    data = data.reindex(index=data.index[::-1]) # Old data first
    data = data[['open', 'high', 'low', 'close']]

    return data

def getDataFrameFromCsv(filepath: str = None, index: str = None) -> pd.DataFrame:
    if filepath is None:
        displayError("File path must be provided")
    
    if not os.path.exists(filepath):
        displayError(f"File {filepath} not found")
    
    data = pd.read_csv(filepath)

    if index:
        return data.set_index(index)
    
    return data