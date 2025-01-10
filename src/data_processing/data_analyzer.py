from src.utils.log import addLog, displayError

import pandas as pd

def checkDataContinuity(data: pd.DataFrame, time_interval: str = '1min') -> list:
    addLog("Looking for discontinuity in data")
   
    holes = []

    if data.empty:
        displayError("Data is empty")
    
    if time_interval.endswith('s'):
        time_diff = pd.Timedelta(seconds=int(time_interval[:-1]))
    elif time_interval.endswith('min'):
        time_diff = pd.Timedelta(minutes=int(time_interval[:-3]))
    elif time_interval.endswith('h'):
        time_diff = pd.Timedelta(hours=int(time_interval[:-1]))
    elif time_interval.endswith('day'):
        time_diff = pd.Timedelta(days=int(time_interval[:-3]))
    elif time_interval.endswith('week'):
        time_diff = pd.Timedelta(weeks=int(time_interval[:-4]))
    else:
        displayError("Invalid time interval")

    if not isinstance(data.index, pd.DatetimeIndex):
        displayError("Data index must be a DatetimeIndex")

    for i in range(1, len(data)):
        previous_time = data.index[i-1]
        current_time = data.index[i]
        
        if (current_time - previous_time) != time_diff:
            holes.append((previous_time, current_time))

    return holes