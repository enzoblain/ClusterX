from src.utils import isInTimeRange

import pandas as pd

def getSessions(last_session: str = None, candles: pd.DataFrame = pd.DataFrame()) -> pd.DataFrame:
    if candles.empty:
        raise Exception("Candles dataframe is empty")

    last_session = pd.to_datetime("2025-02-04 19:23:00")
    index = candles[candles['datetime'] == last_session].index

    if index.empty:
        raise Exception("Last session not found in candles dataframe")
    
    sessions_time = [ # all times are in Sydney time
        {
            "name": "Tokyo",
            "start": "10:00",
            "end": "18:30"
        },
        {
            "name": "London",
            "start": "18:30",
            "end": "23:00"
        },
        {
            "name": "New York AM",
            "start": "23:00",
            "end": "03:30"
        },
        {
            "name": "New York PM",
            "start": "03:30",
            "end": "08:00"
        }
    ]

    sessions = []

    for i in range (index, len(candles)):
        for session in sessions_time:
            if isInTimeRange(candles.iloc[i]['datetime'], session["start"], session["end"]):
                if not sessions or sessions[-1]["name"] != session["name"]:
                    sessions.append({
                        "name": session["name"],
                        "start": candles.iloc[i]['datetime'],
                        "end": candles.iloc[i]['datetime'],
                        "high": candles.iloc[i]["high"],
                        "low": candles.iloc[i]["low"]
                    })

                else:
                    sessions[-1]["end"] = candles.iloc[i]['datetime']
                    sessions[-1]["high"] = max(sessions[-1]["high"], candles.iloc[i]["high"])
                    sessions[-1]["low"] = min(sessions[-1]["low"], candles.iloc[i]["low"])

                break

    new_sessions = pd.DataFrame(sessions)
    new_sessions['start'] = pd.to_datetime(new_sessions['start'])
    new_sessions['end'] = pd.to_datetime(new_sessions['end'])

    return new_sessions