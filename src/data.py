import pandas as pd

import os

def saveDataframetoCSV(dataframe: pd.DataFrame, filepath: str, indexCol: str) -> None:
    if filepath is None:
        raise Exception("Filepath is required")
    
    if dataframe.empty:
        raise Exception("Dataframe is empty") 
    
    if indexCol is None:
        raise Exception("Index column is required")

    path = filepath.split(os.sep) # Split the filepath by the separator
    folder_path = os.path.join(*path[:-1]) # Join the folders to create the folder path

    if not os.path.exists(folder_path):
        os.makedirs(folder_path) # Create the folder if it doesn't exist

    old_data = getDataFrameFromCsv(filepath, returnNone=True) # Return the data or an empty DataFrame if the file does not exist 

    combined_data = pd.concat([dataframe, old_data]) # Concatenate the old and new data
    combined_data = combined_data[~combined_data[indexCol].duplicated(keep='last')] # Remove duplicates based on the selected column
    combined_data.reset_index(drop=True, inplace=True) # Reset the index

    combined_data.to_csv(filepath, index=True) # Save the new data to a CSV file

def getDataFrameFromCsv(filepath: str = None, returnNone: bool = False) -> pd.DataFrame:
    if filepath is None:   
        raise Exception("Filepath is required")
    
    if not os.path.exists(filepath):
        if returnNone:
            return pd.DataFrame()
        
        raise Exception("File does not exist")

    try:
        dataFrame = pd.read_csv(filepath, index_col=0)

        if 'datetime' in dataFrame.columns:
            dataFrame['datetime'] = pd.to_datetime(dataFrame['datetime'])

    except Exception as e:
        raise Exception("Error reading CSV file: ", e)
    
    return dataFrame