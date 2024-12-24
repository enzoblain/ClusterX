import pandas as pd
import os

def setDatetimeIndex(data: pd.DataFrame) -> None:
    data['datetime'] = pd.to_datetime(data['datetime'])
    data.set_index('datetime', inplace=True)

    return data

def getDataFrameFromCsv(filepath: str = None, index: str = None) -> pd.DataFrame:
    if filepath is None:
        raise ValueError("File path must be provided")
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File {filepath} not found")
    
    data = pd.read_csv(filepath)

    if index:
        return data.set_index(index)
    
    return data