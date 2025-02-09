from src.utils import isInTimeRange

import pandas as pd

def getCandlesDirection(candles: pd.DataFrame) -> pd.DataFrame:
     # Create a new column 'direction' based on the close and open prices
    candles['direction'] = candles.apply(
        lambda row: 'bullish' if row['close'] > row['open'] else 'bearish', axis=1
    )

    
    return candles

def getSessions(last_session: int = None, candles: pd.DataFrame = pd.DataFrame()) -> pd.DataFrame:
    if candles.empty:
        raise Exception("Candles dataframe is empty")

    if last_session:
        index = candles[candles['datetime'] == last_session].index.tolist()

        if index == []:
            index = 0
        else:
            index = index[0] + 1 # Start from the next candle

    else:
        index = 0
    
    sessions = []
    
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
    if not new_sessions.empty:
        new_sessions['start'] = pd.to_datetime(new_sessions['start'])
        new_sessions['end'] = pd.to_datetime(new_sessions['end'])

    return new_sessions

def getFVG(last_fvg: int, candles) -> pd.DataFrame:
    if candles.empty:
        raise Exception("Candles dataframe is empty")

    if last_fvg:
        index = candles[candles['datetime'] == last_fvg].index.tolist()

        if index == []:
            index = 1
        else:
            index = index[0] + 1
    else:
        index = 1
    
    fvg = []
        
    for i in range(index, len(candles) - 1):
        if candles.iloc[i - 1]["low"] > candles.iloc[i + 1]["high"]: # bearish gap
            fvg.append({
                "datetime": candles.iloc[i]['datetime'],
                "type": "Fair Value Gap",
                "direction": "bearish",
                "high": candles.iloc[i -1]["low"],
                "low": candles.iloc[i + 1]["high"]
            })
        elif candles.iloc[i - 1]["high"] < candles.iloc[i + 1]["low"]: # bullish gap
            fvg.append({
                "datetime": candles.iloc[i]['datetime'],
                "type": "Fair Value Gap",
                "direction": "bullish",
                "high": candles.iloc[i + 1]["low"],
                "low": candles.iloc[i - 1]["high"]       
            })

    new_fvg = pd.DataFrame(fvg)

    if not new_fvg.empty:
        new_fvg['datetime'] = pd.to_datetime(new_fvg['datetime'])

    return new_fvg