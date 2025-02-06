from src.api import getDataFromTwelveDataApi
from src.utils import getFromConfigFile

def algorithm():
    intervals = ["1min", "5min", "15min", "30min", "1h", "4h", "1day"] # List of intervals
    candles = {} # Store candles for each interval

    symbol = getFromConfigFile("Symbol")

    # Get data for each interval
    for interval in intervals: 
        candles[interval] = getDataFromTwelveDataApi(symbol=symbol, interval=interval)