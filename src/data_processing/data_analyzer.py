from src.utils.log import addLog

import pandas as pd

def checkDataContinuity(data: pd.DataFrame, time_interval: str = '1min') -> list:
    addLog("Looking for discontinuity in data")
   
    holes = []

    if data.empty:
        raise ValueError("Data is empty")
    
    if time_interval == '1min':
        time_diff = pd.Timedelta(minutes=1)

    if not isinstance(data.index, pd.DatetimeIndex):
        raise ValueError("Data index must be a DatetimeIndex")

    for i in range(1, len(data)):
        previous_time = data.index[i-1]
        current_time = data.index[i]
        
        if (current_time - previous_time) != time_diff:
            holes.append((previous_time, current_time))

    return holes
