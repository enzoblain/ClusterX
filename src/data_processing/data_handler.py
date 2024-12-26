import pandas as pd
import os
from datetime import datetime
from src.utils.utils import getFromApi, getValueFromConfigFile
from src.utils.log import addLog
from src.utils.utils import setIndex

def getDataFromTwelveDataAPI(api_key: str = None, symbol: str = None, startDate: str = None, endDate: str = None, interval: str = None) -> pd.DataFrame:
    if api_key is None or symbol is None or interval is None:
        raise ValueError("API key, symbol and interval must be provided")

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
        params['end_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    data = getFromApi(url, params)

    try:
        data = pd.DataFrame(data['values'])
    except KeyError as e:
        addLog(f"Error: {e}")
        return None
    
    addLog(f"Data from TwelveData API: {data.shape[0]} rows")

    data = setIndex(data, 'datetime')
    
    data = data.reindex(index=data.index[::-1]) # Old data first
    data = data[['open', 'high', 'low', 'close']]

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