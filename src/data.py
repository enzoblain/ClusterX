from src.api import getDataFromTwelveDataApi
from src.structures import getCandlesDirection, getFVG, getSessions
from src.utils import delNonAlphaChars

import pandas as pd

import os

from typing import List

def saveDataframetoCSV(dataframe: pd.DataFrame, filepath: str) -> None:
    if filepath is None:
        raise Exception("Filepath is required")
    
    if dataframe.empty:
        raise Exception("Dataframe is empty") 

    path = filepath.split(os.sep) # Split the filepath by the separator
    folder_path = os.path.join(*path[:-1]) # Join the folders to create the folder path

    if not os.path.exists(folder_path):
        os.makedirs(folder_path) # Create the folder if it doesn't exist

    dataframe.to_csv(filepath) # Save the dataframe to a CSV file

def combineDataFrames(dataframes: List[pd.DataFrame], indexCol: str = None) -> pd.DataFrame:
    if not dataframes:
        raise Exception("Dataframes list is empty")
    
    if indexCol is None:
        raise Exception("Index column is required")

    combined_data = pd.concat(dataframes) # Concatenate the dataframes
    combined_data = combined_data[~combined_data[indexCol].duplicated(keep='last')] # Remove duplicates based on the selected column
    combined_data.reset_index(drop=True, inplace=True) # Reset the index

    return combined_data

def getDataFrameFromCsv(filepath: str = None) -> pd.DataFrame:
    if filepath is None:   
        raise Exception("Filepath is required")
    
    if not os.path.exists(filepath):
        return pd.DataFrame()

    dataFrame = pd.read_csv(filepath, index_col=0)

    if 'datetime' in dataFrame.columns:
        dataFrame['datetime'] = pd.to_datetime(dataFrame['datetime'])
    
    return dataFrame

def loadOldData(env: str, symbol: str = None) -> dict:
    if env not in ["dev", "prod"]:
        raise Exception("Environment not supported")
    
    if env == "prod":
        intervals = ["1min", "5min", "15min", "30min", "1h", "4h", "1day"] # List of intervals
    else:
        intervals = ["1min"]
    
    if not symbol:
        raise Exception("Symbol is required")
    
    symbol_path = delNonAlphaChars(symbol) # Remove non-alphanumeric characters to make a valid filename

    data = {} # Store candles for each interval

    ############################
    #        SESSIONS          #
    ############################

    sessions_path = f"data/{symbol_path}/sessions.csv"
    sessions = getDataFrameFromCsv(sessions_path)

    if not sessions.empty:
        sessions['start'] = pd.to_datetime(sessions['start'])
        sessions['end'] = pd.to_datetime(sessions['end'])

    data["sessions"] = sessions

    for interval in intervals:
        data[interval] = {} # Prepare the data structure

        ############################
        #          CANDLES         #
        ############################

        candles_path = f"data/{symbol_path}/{interval}/candles.csv"
        candles_data = getDataFrameFromCsv(candles_path)

        data[interval]["candles"] = candles_data

        ############################
        #           FVG            #
        ############################

        fvg_path = f"data/{symbol_path}/{interval}/fvg.csv"
        fvg_data = getDataFrameFromCsv(fvg_path)

        data[interval]["fvg"] = fvg_data

    return data

def updateData(data: dict, env: str, symbol: str = None):
    if env not in ["dev", "prod"]:
        raise Exception("Environment not supported")
    
    if not symbol:
        raise Exception("Symbol is required")
    
    symbol_path = delNonAlphaChars(symbol) # Remove non-alphanumeric characters to make a valid filename

    if env == "dev":
        return data
    
    intervals = ["1min", "5min", "15min", "30min", "1h", "4h", "1day"] # List of intervals

    for interval in intervals:
        ############################
        #          CANDLES         #
        ############################
        old_candles = data[interval]["candles"]

        new_candles = getDataFromTwelveDataApi(symbol=symbol, interval=interval)
        new_candles = getCandlesDirection(new_candles)

        if not old_candles.empty:
            new_candles = combineDataFrames([old_candles, new_candles], 'datetime')

        candles_path = f"data/{symbol_path}/{interval}/candles.csv"
        saveDataframetoCSV(new_candles, candles_path)

        data[interval]["candles"] = new_candles

        ############################
        #           FVG            #
        ############################
        old_fvg = data[interval]["fvg"]

        if not old_fvg.empty:
            last_fvg = old_fvg['datetime'].iloc[-1]
        else:
            last_fvg = None

        new_fvg = getFVG(last_fvg, new_candles)
        new_fvg = combineDataFrames([old_fvg, new_fvg], 'datetime')

        fvg_path = f"data/{symbol_path}/{interval}/fvg.csv"
        saveDataframetoCSV(new_fvg, fvg_path)

        data[interval]["fvg"] = new_fvg

    ############################
    #        SESSIONS          #
    ############################
    old_sessions = data["sessions"]

    if not old_sessions.empty:
        last_session = old_sessions['end'].iloc[-1]
    else:
        last_session = None

    candles = data["1min"]["candles"]

    new_sessions = getSessions(last_session, candles)
    new_sessions = combineDataFrames([old_sessions, new_sessions], 'start')

    sessions_path = f"data/{symbol_path}/sessions.csv"
    saveDataframetoCSV(new_sessions, sessions_path)

    data["sessions"] = new_sessions

    return data
