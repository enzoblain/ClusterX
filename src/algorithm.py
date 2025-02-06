from src.api import getDataFromTwelveDataApi

def algorithm():
    intervals = ["1min", "5min", "15min", "30min", "1hour", "1day"]
    candles = {} # Store candles for each interval

    # Get data for each interval
    for interval in intervals: 
        candles[interval] = getDataFromTwelveDataApi(symbol="EUR/USD", interval=interval)
        print(candles[interval].head())