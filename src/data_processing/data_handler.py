import pandas as pd
from datetime import datetime
from src.utils.utils import getFromApi, getValueFromConfigFile
from src.utils.log import addLog
from src.utils.utils import setDatetimeIndex

def getDataFromTwelveDataAPI(api_key: str = None, symbol: str = None, startDate: str = None, endDate: str = None) -> pd.DataFrame:
    if api_key is None or symbol is None:
        raise ValueError("api_key and symbol must be provided")

    url = getValueFromConfigFile('config.json', 'API', 'API url')
    
    params = {
        'symbol': symbol,
        'interval': '1min',
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

    data = setDatetimeIndex(data)
    
    data = data.reindex(index=data.index[::-1]) # Old data first
    data = data[['open', 'high', 'low', 'close']]

    return data