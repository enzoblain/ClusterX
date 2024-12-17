from src.data_processing.data_handler import getDataFrameFromCsv
from src.utils.log import addLog
from src.utils.utils import delNonAlphaChars
import os
import pandas as pd

def saveDataFrameToCsv(symbol: str = None, interval: str = None, dataframe: pd.DataFrame = None):
    if symbol is None or interval is None or dataframe is None:
        raise ValueError("symbol, interval, and dataframe must be provided")
    
    symbol = delNonAlphaChars(symbol)
    folder_path = f"data/{symbol}"
    filepath = f"data/{symbol}/{interval}.csv"

    if not os.path.exists(folder_path):
        addLog(f"Creating folder {folder_path}")
        os.makedirs(folder_path)

    if not os.path.exists(filepath):
        addLog(f"Creating file {filepath}")
        dataframe.to_csv(filepath, index=True)
    else: 
        addLog(f"File {filepath} already exists. Combining dataframes")
        
        csv_data = getDataFrameFromCsv(filepath)
        csv_data['datetime'] = pd.to_datetime(csv_data['datetime'])
        csv_data.set_index('datetime', inplace=True)

        combined_dataFrame = pd.concat([csv_data, dataframe])
        combined_dataFrame = combined_dataFrame[~combined_dataFrame.index.duplicated(keep='last')]

        os.remove(filepath)
        combined_dataFrame.to_csv(filepath, index=True)
    
    return 