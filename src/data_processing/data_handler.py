import pandas as pd
from datetime import datetime

from src.utils.utils import getFromApi, getValueFromConfigFile

def getDataFromTwelveDataAPI(api_key: str = None, symbol: str = None) -> pd.DataFrame:
    url = getValueFromConfigFile('config.json', 'API', 'API url')
    params = {
        'symbol': symbol,
        'interval': '1min',
        'apikey': api_key,
        'end_date': datetime.now().strftime('%Y-%m-%d'),
    }
    
    data = getFromApi(url, params)

    data = pd.DataFrame(data['values'])
    data.set_index("datetime", inplace=True)
    data = data.reindex(index=data.index[::-1]) # Old data first
    data = data[['open', 'high', 'low', 'close']]

    return data