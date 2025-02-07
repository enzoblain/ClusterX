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
        raise Exception("File does not exist")

    dataFrame = pd.read_csv(filepath, index_col=0)

    if 'datetime' in dataFrame.columns:
        dataFrame['datetime'] = pd.to_datetime(dataFrame['datetime'])
    
    return dataFrame