from src.api import getDataFromTwelveDataApi
from src.data import saveDataframetoCSV, getDataFrameFromCsv, combineDataFrames
from src.utils import getFromConfigFile, delNonAlphaChars

def algorithm():
    env = getFromConfigFile("Environment")

    if env not in ["dev", "prod"]:
        raise Exception("Environment not supported")
    
    if env == "prod":
        intervals = ["1min", "5min", "15min", "30min", "1h", "4h", "1day"] # List of intervals
    else:
        intervals = ["1min"]

    data = {} # Store candles for each interval

    symbol = getFromConfigFile("Symbol")

    # Get data for each interval
    for interval in intervals: 
        data[interval] = {} # Prepare the data structure

        # Define the path to save the data
        symbolpath = delNonAlphaChars(symbol) # Remove non-alphanumeric characters to make a valid filename
        candles_path = f"data/{symbolpath}/{interval}/candles.csv"

        candles_old_data = getDataFrameFromCsv(candles_path)

        if env == "prod":
            new_data = getDataFromTwelveDataApi(symbol=symbol, interval=interval)

            candle_data = combineDataFrames([candles_old_data, new_data], 'datetime')

            # Save the data to a CSV file
            saveDataframetoCSV(candle_data, candles_path)

        else:
            candle_data = candles_old_data

        data[interval]["candles"] = candle_data

    print(data)