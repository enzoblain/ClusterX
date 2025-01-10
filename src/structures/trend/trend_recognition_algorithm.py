import pandas as pd

def getTrends(candles: pd.DataFrame, trends: list = None):
    if trends: # if old trends are provided
        last_trend_start = trends[-1]["start"]
        last_trend_start_index = candles.index.get_loc(last_trend_start) # find the index of the last trend start

        i = last_trend_start_index + 1 # start from the next candle after the last trend start

    else: # if no old trends are provided
        first_candle = candles.iloc[0]
        trends = [
            {
                "direction": first_candle['direction'],
                "start": first_candle.name,
                "low": first_candle['low'],
                "high": first_candle['high'],
                "end": None
            }
        ]

        i = 1 # start from the second candle because the trend is defined by the first candle

        subtrend = None

    while i < len(candles):
        current_candle = candles.iloc[i]

        if current_candle["direction"] == trends[-1]["direction"]: # if the current candle is in the same direction as the trend
            if subtrend: # if there is a subtrend
                if subtrend["direction"] == "bullish": # if the trend is bearish but subtrend is bullish
                    if current_candle['close'] < subtrend["low"]: # if the current candle closes below the subtrend low
                        trends[-1]["high"] = subtrend["high"] # set the trend last high to the subtrend high
                        subtrend = None

                    else:
                        subtrend["high"] = max(subtrend["high"], current_candle['high'])

                else: # if the trend is bullish but subtrend is bearish
                    if current_candle['close'] > subtrend["high"]:
                        trends[-1]["low"] = subtrend["low"] # set the trend last low to the subtrend low
                        subtrend = None

                    else:
                        subtrend["low"] = min(subtrend["low"], current_candle['low'])

            else:
                trends[-1]["low"] = min(trends[-1]["low"], current_candle['low'])
                trends[-1]["high"] = max(trends[-1]["high"], current_candle['high'])

            i += 1 # move to the next candle

        else: # if the current candle is in the opposite direction of the trend
            if subtrend:
                if subtrend["direction"] == "bullish":
                    subtrend["high"] = max(subtrend["high"], current_candle['high'])

                    if current_candle['close'] > trends[-1]["high"]: # if the current candle closes above the trend high
                        trends[-1]["end"] = subtrend['start']

                        first_candle = candles.iloc[candles.index.get_loc(subtrend['start'])]

                        trends.append({
                            "direction": current_candle["direction"],
                            "start": first_candle.name,
                            "low": first_candle['low'],
                            "high": first_candle['high'],
                            "end": None,
                        })

                        i = candles.index.get_loc(subtrend['start']) + 1 # reset the index to the next candle after the current candle
                        subtrend = None

                    else:
                        subtrend["high"] = max(subtrend["high"], current_candle['high'])
                        trends[-1]["high"] = min(trends[-1]["high"], current_candle['high']) # set the trend high to the current candle high

                        i += 1 # move to the next candle

                else:
                    subtrend["low"] = min(subtrend["low"], current_candle['low']) 

                    if current_candle['close'] < trends[-1]["low"]: # if the current candle closes below the trend low
                        trends[-1]["end"] = subtrend['start']

                        first_candle = candles.iloc[candles.index.get_loc(subtrend['start'])]

                        trends.append({
                            "direction": current_candle["direction"],
                            "start": first_candle.name,
                            "low": first_candle['low'],
                            "high": first_candle['high'],
                            "end": None
                        })

                        i = candles.index.get_loc(subtrend['start']) + 1
                        subtrend = None

                    else:
                        subtrend["low"] = min(subtrend["low"], current_candle['low'])
                        trends[-1]["low"] = max(trends[-1]["low"], current_candle['low']) # set the trend low to the current candle low

                        i += 1 # move to the next candle

            else:
                subtrend = {
                    "direction": current_candle["direction"],
                    "start": current_candle.name,
                    "low": current_candle['low'],
                    "high": current_candle['high'],
                    "end": None
                }

                # stay on the same candle to test if the subtrend should continue or if it's a one candle reversal

    return trends