# Local imports
from src.log import displayError
from src.utils import isInTimeRange

# External imports
import pandas as pd

from typing import Tuple

##############################################
#                 CANDLES                    #
##############################################

def getCandlesDirection(candles: pd.DataFrame) -> pd.DataFrame:
    try:
        candles['direction'] = candles.apply(
            lambda row: 'bullish' if row['close'] > row['open'] else 'bearish', axis=1
        )

    except Exception as e:
        displayError(e)
    
    return candles

##############################################
#           TRENDS & ORDER BLOCKS            #
##############################################

def getTrendsAndOrderBlocks(candles: pd.DataFrame, trends: list = None, order_blocks: list = None) -> Tuple[pd.DataFrame]:
    if candles.empty:
        displayError("Candles DataFrame is empty")

    if not order_blocks:
        order_blocks = []

    if trends:  # If old trends are provided
        last_trend_start = trends[-1]["start"]
        last_trend_start_index = candles.index.get_loc(last_trend_start)
        i = last_trend_start_index + 1  # Start from the next candle after the last trend start
        
    else:  # If no old trends are provided
        first_candle = candles.iloc[0]
        trends = [{
            "direction": first_candle['direction'],
            "start": first_candle.name,
            "low": first_candle['low'],
            "high": first_candle['high'],
            "end": None
        }]
        i = 1
        subtrend = None

    # Convert DataFrame columns to Series for faster access
    directions = candles["direction"]
    closes = candles["close"]
    lows = candles["low"]
    highs = candles["high"]

    try:
        while i < len(candles):
            current_direction = directions.iloc[i]
            current_close = closes.iloc[i]
            current_low = lows.iloc[i]
            current_high = highs.iloc[i]

            last_trend = trends[-1]

            if current_direction == last_trend["direction"]:  # Same direction as the trend
                if subtrend:
                    if subtrend["direction"] == "bullish":  # Bullish trend and subtrend 
                        if current_close < subtrend["low"]:
                            last_trend["high"] = subtrend["high"]  # Update trend high
                            subtrend = None
                        else:
                            subtrend["high"] = max(subtrend["high"], current_high)
                    else:  # Bearish trend and subtrend
                        if current_close > subtrend["high"]:
                            last_trend["low"] = subtrend["low"]  # Update trend low
                            subtrend = None
                        else:
                            subtrend["low"] = min(subtrend["low"], current_low)
                else: # No subtrend
                    last_trend["low"] = min(last_trend["low"], current_low)
                    last_trend["high"] = max(last_trend["high"], current_high)
                i += 1
            else:  # Opposite direction
                if subtrend: # If there is an active subtrend
                    subtrend_start = candles.index.get_loc(subtrend['start'])

                    if subtrend["direction"] == "bullish" and current_close > last_trend["high"]: # Bullish trend and bullish subtrend
                        last_trend["end"] = subtrend['start']
                        trends.append({
                            "direction": current_direction,
                            "start": candles.index[subtrend_start],
                            "low": lows.iloc[subtrend_start],
                            "high": highs.iloc[subtrend_start],
                            "end": None
                        })

                        order_blocks.append({
                            "datetime": last_trend["end"],
                            "direction": last_trend["direction"],
                            "high": last_trend["high"],
                            "low": last_trend["low"]
                        })

                        i = subtrend_start + 1
                        subtrend = None
                    elif subtrend["direction"] == "bearish" and current_close < last_trend["low"]: # Bearish trend and bearish subtrend
                        last_trend["end"] = subtrend['start']
                        trends.append({
                            "direction": current_direction,
                            "start": candles.index[subtrend_start],
                            "low": lows.iloc[subtrend_start],
                            "high": highs.iloc[subtrend_start],
                            "end": None
                        })

                        order_blocks.append({
                            "datetime": last_trend["end"],
                            "direction": last_trend["direction"],
                            "high": last_trend["high"],
                            "low": last_trend["low"]
                        })

                        i = subtrend_start + 1
                        subtrend = None
                    else: # Opposite direction subtrend
                        if subtrend["direction"] == "bullish": # Bullish trend and bearish subtrend
                            subtrend["high"] = max(subtrend["high"], current_high) # Update subtrend high
                        else: # Bearish trend and bullish subtrend
                            subtrend["low"] = min(subtrend["low"], current_low) # Update subtrend low
                        i += 1
                else: # No subtrend
                    subtrend = {
                        "direction": current_direction,
                        "start": candles.index[i],
                        "low": current_low,
                        "high": current_high,
                        "end": None
                    }

    except Exception as e:
        displayError(e)

    return pd.DataFrame(trends), pd.DataFrame(order_blocks)

##############################################
#                 SESSIONS                   #
##############################################


def getSessions(candles: pd.DataFrame, sessions: list = None) -> pd.DataFrame:
    if candles.empty:
        displayError("Candles DataFrame is empty")

    try:
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

        if not sessions:
            sessions = []
            i = 0
        else:
            sessions = sessions.to_dict("records")
            datetime = sessions[-1]["datetime"]
            i = candles.get_loc(datetime) + 1

        for i in range (i, len(candles)):
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

    except Exception as e:
        displayError(e)

    return pd.DataFrame(sessions)

##############################################
#                   FVG                      #
##############################################

def findFairValueGaps(candles: pd.DataFrame, fair_value_gaps : pd.DataFrame = None) -> pd.DataFrame:
    if candles.empty:
        displayError("Candles DataFrame is empty")

    try:
        if not fair_value_gaps:
            fair_value_gaps = []
            i = 1
        else:
            fair_value_gaps = fair_value_gaps.to_dict('records')
            datetime = fair_value_gaps[-1]["datetime"]
            i = candles.get_loc(datetime) + 1
            
        for i in range(i, len(candles) - 1):
            if candles.iloc[i - 1]["low"] > candles.iloc[i + 1]["high"]: # bearish gap
                fair_value_gaps.append({
                    "datetime": candles.iloc[i].name,
                    "direction": "bearish",
                    "high": candles.iloc[i -1]["low"],
                    "low": candles.iloc[i + 1]["high"]
                })
            elif candles.iloc[i - 1]["high"] < candles.iloc[i + 1]["low"]: # bullish gap
                fair_value_gaps.append({
                    "datetime": candles.iloc[i].name,
                    "direction": "bullish",
                    "high": candles.iloc[i + 1]["low"],
                    "low": candles.iloc[i - 1]["high"]             
                })

    except Exception as e:
        displayError(e)

    return pd.DataFrame(fair_value_gaps)

##############################################
#               ORDER BLOCKS                 #
##############################################

def findOrderBlocks(candles : pd.DataFrame, trends : pd.DataFrame, order_blocks: list = None) -> pd.DataFrame:
    if candles.empty:
        displayError("Candles DataFrame is empty")

    if trends.empty:
        displayError("Trends DataFrame is empty")
    
    try:
        if not order_blocks:
            i = 0
            order_blocks = []
        else:
            order_blocks = order_blocks.to_dict(orient="records")
            datetime = order_blocks[-1]["datetime"]
            i = trends["end" == datetime].index + 1
        
        for i in range(i, len(trends)):
            current_datetime = candles.iloc[i].name
            order_blocks.append({
                "datetime": trends.iloc[i]["end"],
                "direction": trends.iloc[i]["direction"],
                "high": candles.loc[current_datetime]["high"],
                "low": candles.loc[current_datetime]["low"],
            })

    except Exception as e:
        displayError(e)

    return pd.DataFrame(order_blocks)