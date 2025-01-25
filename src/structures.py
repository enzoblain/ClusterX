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
#            TRENDS & ORDER BLOCKS           #
##############################################

from typing import Tuple
import pandas as pd

def getTrends(candles: pd.DataFrame, trends: pd.DataFrame = None, order_blocks: pd.DataFrame = None, breaks_of_structure: pd.DataFrame = None, changes_of_character: pd.DataFrame = None, relative_highs_lows: pd.DataFrame = None) -> Tuple[pd.DataFrame]:
    if candles.empty:
        displayError("Candles DataFrame is empty")
    
    if order_blocks.empty:
        order_blocks = []
    else:
        order_blocks = order_blocks.to_dict("records")

    if breaks_of_structure.empty:
        breaks_of_structure = []
    else:
        breaks_of_structure = breaks_of_structure.to_dict("records")

    if changes_of_character.empty:
        changes_of_character = []
    else:
        changes_of_character = changes_of_character.to_dict("records")

    if relative_highs_lows.empty:
        relative_highs_lows = []
    else:
        relative_highs_lows = relative_highs_lows.to_dict("records")

    if not trends.empty:  # If old trends are provided
        trends = trends.to_dict("records")
        last_trend_start = trends[-1]["start"]
        last_trend_start_index = candles[candles['datetime'] == last_trend_start].index[0]
        i = last_trend_start_index + 1  # Start from the next candle after the last trend start
        
    else:  # If no old trends are provided
        first_candle = candles.iloc[0]
        trends = [{
            "direction": first_candle['direction'],
            "start": first_candle['datetime'],
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
            last_trend_high_datetime = trends[-1]["start"]
            last_trend_low_datetime = trends[-1]["start"]

            if current_direction == last_trend["direction"]:  # Same direction as the trend
                if subtrend:
                    if subtrend["direction"] == "bullish":  # Bullish subtrend
                        if current_close < subtrend["low"]:
                            breaks_of_structure.append({
                                "datetime": candles.iloc[i]["datetime"],
                                "type": "Break of Structure",
                                "direction": "Bearish",
                                "reference": subtrend["start"],
                                "price": subtrend["low"]
                            })

                            relative_highs_lows.append({
                                "datetime": subtrend_relative_high_datetime,
                                "type": "Relative High/Low",
                                "direction": "High",
                                "price": subtrend["high"]
                            })

                            last_trend["high"] = subtrend["high"]  # Update trend high

                            subtrend = None
                        else:
                            if current_high > subtrend["high"]:
                                subtrend_relative_high_datetime = candles.iloc[i]["datetime"]
                                subtrend["high"] = current_high

                    else:  # Bearish subtrend
                        if current_close > subtrend["high"]:
                            breaks_of_structure.append({
                                "datetime": candles.iloc[i]["datetime"],
                                "type": "Break of Structure",
                                "direction": "Bullish",
                                "reference": subtrend["start"],
                                "price": subtrend["high"]
                            })

                            relative_highs_lows.append({
                                "datetime": subtrend_relative_low_datetime,
                                "type": "Relative High/Low",
                                "direction": "Low",
                                "price": subtrend["low"]
                            })

                            last_trend["low"] = subtrend["low"]  # Update trend low
                            subtrend = None
                        else:
                            if current_low < subtrend["low"]:
                                subtrend_relative_low_datetime = candles.iloc[i]["datetime"]
                                subtrend["low"] = current_low

                else: # No subtrend
                    if last_trend['low'] > current_low:
                        last_trend['low'] = current_low
                        last_trend_low_datetime = candles.iloc[i]["datetime"]
                    
                    if last_trend['high'] < current_high:
                        last_trend['high'] = current_high
                        last_trend_high_datetime = candles.iloc[i]["datetime"]

                i += 1
            else:  # Opposite direction
                if subtrend: # If there is an active subtrend
                    subtrend_start = candles[candles['datetime'] == subtrend['start']].index[0]

                    if subtrend["direction"] == "bullish" and current_close > last_trend["high"]: # Bullish trend and bullish subtrend
                        last_trend["end"] = subtrend['start']

                        trends.append({
                            "direction": current_direction,
                            "start": subtrend['start'],
                            "low": lows.iloc[subtrend_start],
                            "high": highs.iloc[subtrend_start],
                            "end": None
                        })

                        order_blocks.append({
                            "datetime": last_trend["end"],
                            "type": "Order Block",
                            "direction": last_trend["direction"],
                            "high": last_trend["high"],
                            "low": last_trend["low"],
                        })

                        changes_of_character.append({
                            "datetime": last_trend["end"],
                            "type": "Change of Character",
                            "direction": "Bullish",
                            "reference": last_trend_high_datetime,
                            "price": last_trend["high"],
                        })

                        relative_highs_lows.append({
                            "datetime": subtrend_relative_low_datetime,
                            "type": "Relative High/Low",
                            "direction": "Low",
                            "price": last_trend["low"]
                        })

                        i = subtrend_start + 1
                        subtrend = None
                    elif subtrend["direction"] == "bearish" and current_close < last_trend["low"]: # Bearish trend and bearish subtrend
                        last_trend["end"] = subtrend['start']

                        trends.append({
                            "direction": current_direction,
                            "start": subtrend['start'],
                            "low": lows.iloc[subtrend_start],
                            "high": highs.iloc[subtrend_start],
                            "end": None
                        })

                        order_blocks.append({
                            "datetime": last_trend["end"],
                            "type": "Order Block",
                            "direction": last_trend["direction"],
                            "high": last_trend["high"],
                            "low": last_trend["low"],
                        })

                        changes_of_character.append({
                            "datetime": last_trend["end"],
                            "type": "Change of Character",
                            "direction": "Bearish",
                            "reference": last_trend_low_datetime,
                            "price": last_trend["low"],
                        })

                        relative_highs_lows.append({
                            "datetime": subtrend_relative_high_datetime,
                            "type": "Relative High/Low",
                            "direction": "High",
                            "price": last_trend["high"]
                        })

                        i = subtrend_start + 1
                        subtrend = None
                    else: # Opposite direction subtrend
                        if subtrend["direction"] == "bullish": # Bullish trend and bearish subtrend
                            if current_high > subtrend["high"]:
                                subtrend_relative_high_datetime = candles.iloc[i]["datetime"]
                                subtrend["high"] = current_high
                        
                        else: # Bearish trend and bullish subtrend
                            if current_low < subtrend["low"]:
                                subtrend_relative_low_datetime = candles.iloc[i]["datetime"]
                                subtrend["low"] = current_low
                        i += 1
                else: # No subtrend
                    subtrend = {
                        "direction": current_direction,
                        "start": candles.iloc[i]["datetime"],
                        "low": current_low,
                        "high": current_high,
                        "end": None
                    }

                    subtrend_relative_low_datetime = candles.iloc[i]["datetime"]
                    subtrend_relative_high_datetime = candles.iloc[i]["datetime"]

    except Exception as e:
        displayError(e)

    return pd.DataFrame(trends), pd.DataFrame(order_blocks), pd.DataFrame(breaks_of_structure), pd.DataFrame(changes_of_character), pd.DataFrame(relative_highs_lows)


##############################################
#                 SESSIONS                   #
##############################################


def getSessions(candles: pd.DataFrame, sessions: pd.DataFrame = None) -> pd.DataFrame:
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

        if sessions.empty:
            sessions = []
            i = 0
        else:
            sessions = sessions.to_dict("records")
            datetime = sessions[-1]["start"]
            i = candles[candles['datetime'] == datetime].index[0] + 1

        for i in range (i, len(candles)):
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
        if fair_value_gaps.empty:
            fair_value_gaps = []
            i = 1
        else:
            fair_value_gaps = fair_value_gaps.to_dict('records')
            datetime = fair_value_gaps[-1]["datetime"]
            i = candles[candles['datetime'] == datetime].index[0] + 1
            
        for i in range(i, len(candles) - 1):
            if candles.iloc[i - 1]["low"] > candles.iloc[i + 1]["high"]: # bearish gap
                fair_value_gaps.append({
                    "datetime": candles.iloc[i]['datetime'],
                    "type": "Fair Value Gap",
                    "direction": "bearish",
                    "high": candles.iloc[i -1]["low"],
                    "low": candles.iloc[i + 1]["high"]
                })
            elif candles.iloc[i - 1]["high"] < candles.iloc[i + 1]["low"]: # bullish gap
                fair_value_gaps.append({
                    "datetime": candles.iloc[i]['datetime'],
                    "type": "Fair Value Gap",
                    "direction": "bullish",
                    "high": candles.iloc[i + 1]["low"],
                    "low": candles.iloc[i - 1]["high"]       
                })

    except Exception as e:
        displayError(e)

    return pd.DataFrame(fair_value_gaps)