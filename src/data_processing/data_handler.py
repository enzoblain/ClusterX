import pandas as pd
from datetime import datetime
import os
from src.utils.utils import getFromApi, getValueFromConfigFile
from src.utils.log import addLog

def getDataFromTwelveDataAPI(api_key: str = None, symbol: str = None, endDate: None = str) -> pd.DataFrame:
    if api_key is None or symbol is None:
        raise ValueError("api_key and symbol must be provided")

    url = getValueFromConfigFile('config.json', 'API', 'API url')
    params = {
        'symbol': symbol,
        'interval': '1min',
        'apikey': api_key,
        'end_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    data = getFromApi(url, params)

    try:
        data = pd.DataFrame(data['values'])
    except KeyError as e:
        addLog(f"Error: {e}")
        return None
    
    addLog(f"Data from TwelveData API: {data.shape[0]} rows")
    
    data['datetime'] = pd.to_datetime(data['datetime'])
    data.set_index("datetime", inplace=True)
    data = data.reindex(index=data.index[::-1]) # Old data first
    data = data[['open', 'high', 'low', 'close']]

    return data

def getDataFrameFromCsv(filepath: str = None) -> pd.DataFrame:
    if filepath is None:
        raise ValueError("File path must be provided")
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File {filepath} not found")
    
    return pd.read_csv(filepath)