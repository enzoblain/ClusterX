import pandas as pd
from src.utils.utils import isInTimeRange
from src.utils.log import addLog

def getSessions(candles: pd.DataFrame, sessions: list = None, interval: str = None) -> list:
    addLog(f"Searching for sessions and their caracteristics in market data for {interval} interval")
    sessions_time = [
        {
            "name": "Tokyo",
            "start": "00:00",
            "end": "06:00"
        },
        {
            "name": "London",
            "start": "07:00",
            "end": "13:00"
        },
        {
            "name": "New York",
            "start": "14:00",
            "end": "20:00"
        }
    ]

    if not sessions:
        sessions = []

    for i in range (len(candles)):
        for session in sessions_time:
            if isInTimeRange(candles.iloc[i].name, session["start"], session["end"]):
                if not sessions or sessions[-1]["name"] != session["name"]:
                    sessions.append({
                        "name": session["name"],
                        "start": candles.iloc[i].name,
                        "end": candles.iloc[i].name,
                        "high": candles.iloc[i]["high"],
                        "low": candles.iloc[i]["low"]
                    })
                else:
                    sessions[-1]["end"] = candles.iloc[i].name
                    sessions[-1]["high"] = max(sessions[-1]["high"], candles.iloc[i]["high"])
                    sessions[-1]["low"] = min(sessions[-1]["low"], candles.iloc[i]["low"])
                break

    return sessions