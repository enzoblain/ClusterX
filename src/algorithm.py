from src.api import getDataFromTwelveDataApi
from src.data import saveDataframetoCSV
from src.utils import getFromConfigFile, delNonAlphaChars

def algorithm():
    env = getFromConfigFile("Environment")

    if env not in ["dev", "prod"]:
        raise Exception("Environment not supported")
    
    if env == "prod":
        intervals = ["1min", "5min", "15min", "30min", "1h", "4h", "1day"] # List of intervals
    else:
        intervals = ["1min"]

    candles = {} # Store candles for each interval

    symbol = getFromConfigFile("Symbol")

    # Get data for each interval
    for interval in intervals: 
        candles[interval] = getDataFromTwelveDataApi(symbol=symbol, interval=interval)

        # Define the path to save the data
        symbolpath = delNonAlphaChars(symbol) # Remove non-alphanumeric characters to make a valid filename
        filepath = f"data/{symbolpath}/{interval}/candles.csv"

        # Save the data to a CSV file
        saveDataframetoCSV(candles[interval], filepath, 'datetime')