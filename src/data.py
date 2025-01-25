# Local imports
from src.log import addLog, displayError
from src.utils import delNonAlphaChars, getFromApi, getValueFromConfigFile

# External imports
import os
import pandas as pd

from datetime import datetime
from zoneinfo import ZoneInfo

def saveDataFrameToCsv(symbol: str = None, interval: str = None, filename: str = None, dataframe: pd.DataFrame = None, index: str = None) -> str:
    if symbol is None or interval is None or filename is None or dataframe.empty or index is None:
        displayError("symbol, interval, dataframe and index must be provided")
    
    symbol = delNonAlphaChars(symbol)
    folder_path = f"data/{symbol}"
    filepath = f"data/{symbol}/{interval}/{filename}.csv"

    if not os.path.exists(folder_path):
        addLog(f"Creating folder {folder_path}")
        os.makedirs(folder_path)

    if not os.path.exists(f"data/{symbol}/{interval}"):
        addLog(f"Creating folder {folder_path}/{interval}")
        os.makedirs(f"data/{symbol}/{interval}")

    if not os.path.exists(filepath):
        addLog(f"Creating file {filepath}")
        dataframe.to_csv(filepath, index=True)

    else: 
        addLog(f"File {filepath} already exists. Combining dataframes")

        try:   
            csv_data = getDataFrameFromCsv(filepath)

            combined_dataFrame = pd.concat([csv_data, dataframe])
            combined_dataFrame = combined_dataFrame[~combined_dataFrame[index].duplicated(keep='last')]
            combined_dataFrame = combined_dataFrame.reset_index(drop=True)

            os.remove(filepath)
            combined_dataFrame.to_csv(filepath, index=True)

        except Exception as e:
            displayError(e)
    
    return filepath

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
    
    try:
        data = pd.DataFrame(data['values'])
        data = data.reindex(index=data.index[::-1], ) # Old data first
        data = data.reset_index(drop=True)
        data = data[['datetime', 'open', 'high', 'low', 'close', 'volume']]
    
    except Exception as e:
        displayError(e)

    return data

def getDataFrameFromCsv(filepath: str = None, returnNone: bool = False) -> pd.DataFrame:
    if filepath is None:   
        displayError("File path must be provided")

    
    if not os.path.exists(filepath):
        if returnNone:
            return pd.DataFrame()
        
        displayError(f"File {filepath} not found")

    try:
        data = pd.read_csv(filepath, index_col=0)

        if 'datetime' in data.columns:
            data['datetime'] = pd.to_datetime(data['datetime'])

    except Exception as e:
        displayError(e)
    
    return data