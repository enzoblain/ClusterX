import pandas as pd

def getTrends(candles: pd.DataFrame, trends: list = None):
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

    return pd.DataFrame(trends)