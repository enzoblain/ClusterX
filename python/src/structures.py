import pytz
from datetime import datetime, time, timezone, timedelta
from src.redis import addCandle, addSession, addFairValueGap, addTrend, addBreakOfStructure, addRelativeHighsLows, addOrderBlock, addChangeOfCharacter

## CANDLES
sydney_tz = pytz.timezone("Australia/Sydney")
utc_tz = pytz.utc

def convertToUTC(candle):
    localized_datetime = sydney_tz.localize(candle['datetime'])
    utc_datetime = localized_datetime.astimezone(utc_tz)

    candle['datetime'] = utc_datetime

    return

def getAverage(candle):
    candle["average"] = (candle["open"] + candle["high"] + candle["low"] + candle["close"]) / 4

    return 

def getDirection(candle):
    if candle["open"] > candle["close"]:
        candle["direction"] = "Bearish"
    elif candle["open"] < candle["close"]:
        candle["direction"] = "Bullish"
    else:
        candle["direction"] = "Doji"

    return

def processCandle(candle, collection_name, timerange):
    convertToUTC(candle)
    getAverage(candle)
    getDirection(candle)

    addCandle(collection_name, timerange, candle)

    return

## SESSIONS

def is_time_in_range(start, end, check_time):
    if start <= end:
        return start <= check_time < end
    else:
        return check_time >= start or check_time < end

def processSession(candle, last_session, collection_name):
    sessions = {
        "ASIAN_SESSION": {
            "Name": "Asian Session",
            "Start": time(22, 0),
            "End": time(7, 30)
        }, # 22:00 - 07:30 UTC
        "LONDON_SESSION": {
            "Name": "London Session",
            "Start": time(7, 30),
            "End": time(12, 0)
        }, # 07:30 - 12:00 UTC
        "NEWYORK_AM_SESSION": {
            "Name": "New York AM Session",
            "Start": time(12, 0),
            "End": time(16, 30)
        }, # 12:00 - 16:30 UTC
        "NEWYORK_PM_SESSION": {
            "Name": "New York PM Session",
            "Start": time(16, 30),
            "End": time(22, 0)
        } # 16:30 - 22:00 UTC
    }

    if not last_session["Start"] or not is_time_in_range(last_session["Start"], last_session["End"], candle["datetime"]):    
        for session in sessions:
            if is_time_in_range(sessions[session]["Start"], sessions[session]["End"], candle["datetime"].time()):
                last_session["Name"] = sessions[session]["Name"]

                last_session["Open"] = None
                last_session["Close"] = None

                last_session["Start"] = datetime.combine(candle["datetime"].date(), sessions[session]["Start"], tzinfo=timezone.utc)
                last_session["End"] = datetime.combine(candle["datetime"].date(), sessions[session]["End"], tzinfo=timezone.utc)

                last_session["High"] = candle["high"]
                last_session["Low"] = candle["low"]
            
                if session == "ASIAN_SESSION":
                    if candle["datetime"].time() >= time(22, 00):
                        last_session["End"] += timedelta(days=1)
                    else:
                        last_session["Start"] -= timedelta(days=1)

                if candle["datetime"].time() == sessions[session]["Start"]:
                    last_session["Open"] = candle["open"]

                break

    else:
        if candle["high"] > last_session["High"]:
            last_session["High"] = candle["high"]
        if candle["low"] < last_session["Low"]:
            last_session["Low"] = candle["low"]

        if candle["datetime"].time() == (last_session["End"] - timedelta(minutes=1)).time():
            last_session["Close"] = candle["close"]

    addSession(collection_name, last_session)

def processFairValueGap(candle, moving3candles, collection_name, timerange):
    moving3candles.pop(0)
    moving3candles.append(candle)

    direction = None

    for candle in moving3candles:
        if not candle["direction"]:
            return
        
        if not direction:
            direction = candle["direction"]
        elif direction != candle["direction"]:
            return
        
    fvg = {
        "Datetime": moving3candles[1]["datetime"],
        "Direction": direction,
        "High": None,
        "Low": None,
    }

    if direction == "Bullish":
        if moving3candles[0]["high"] < moving3candles[2]["low"]:
            fvg["High"] = moving3candles[0]["high"]
            fvg["Low"] = moving3candles[2]["low"]
    elif direction == "Bearish":
        if moving3candles[0]["low"] > moving3candles[2]["high"]:
            fvg["High"] = moving3candles[2]["high"]
            fvg["Low"] = moving3candles[0]["low"]

    if fvg["High"]:
        addFairValueGap(collection_name, timerange, fvg)

def processTrend(queue, candle, last_candle, trend, subtrend, collection_name, timerange):
    queue.append(candle)

    datetime = getTrends(trend, subtrend, candle, last_candle, collection_name, timerange)

    if datetime is not None:
        processQueue(queue, datetime)

        processing_required = True

        while processing_required:
            processing_required = False

            for i in range(len(queue)):
                datetime = getTrends(trend, subtrend, queue[i], last_candle, collection_name, timerange)

                if datetime is not None:
                    processing_required = True

                    processQueue(queue, datetime)

                    break

def resetDict(dict):
    for key in dict:
            dict[key] = None

def processQueue(queue, datetime):
    while queue and queue[0]["datetime"] < datetime:
        queue.popleft()

def getTrends(trend, subtrend, candle, last_candle,  collection_name, timerange):
    index = None
                
    if not trend["Start"]:
        trend["Start"] = candle["datetime"]
        trend["High"] = candle["high"]
        trend["Low"] = candle["low"]
        trend["Direction"] = candle["direction"]

        trend["High datetime"] = candle["datetime"]
        trend["Low datetime"] = candle["datetime"]
        
        return None
    
    if candle["direction"] == trend["Direction"]:
        if subtrend["Start"]:
            if subtrend["Direction"] == "Bullish":
                if candle["close"] < subtrend["Low"]:
                    break_of_structure = {
                        "Datetime": candle["datetime"],
                        "Price": subtrend["Low"],
                        "Reference": subtrend["Last candle"]["datetime"],
                        "Direction": "Bearish"
                    }
                    addBreakOfStructure(collection_name, timerange, break_of_structure)

                    trend["High"] = subtrend["High"]

                    relativeHigh = {
                        "Datetime": subtrend["Last relative high datetime"],
                        "Price": subtrend["High"],
                        "Type": "Relative High"
                    }

                    relativeLow = {
                        "Datetime": candle["datetime"],
                        "Price": subtrend["Low"],
                        "Type": "Relative Low"
                    }

                    addRelativeHighsLows(collection_name, timerange, relativeHigh)
                    addRelativeHighsLows(collection_name, timerange, relativeLow)

                    resetDict(subtrend)
                else:
                     if candle["high"] > subtrend["High"]:
                        subtrend["Last relative high datetime"] = candle["datetime"]
                        subtrend["High"] = candle["high"]

            else:
                if candle["close"] > subtrend["High"]:
                    break_of_structure = {
                        "Datetime": candle["datetime"],
                        "Price": subtrend["High"],
                        "Reference": subtrend["Last candle"]["datetime"],
                        "Direction": "Bullish"
                    }
                    addBreakOfStructure(collection_name, timerange, break_of_structure)

                    trend["Low"] = subtrend["Low"]

                    relativeHigh = {
                        "Datetime": candle["datetime"],
                        "Price": subtrend["High"],
                        "Type": "Relative High"
                    }

                    relativeLow = {
                        "Datetime": subtrend["Last relative low datetime"],
                        "Price": subtrend["Low"],
                        "Type": "Relative Low"
                    }

                    addRelativeHighsLows(collection_name, timerange, relativeHigh)
                    addRelativeHighsLows(collection_name, timerange, relativeLow)

                    resetDict(subtrend)
                else:
                    if candle["low"] < subtrend["Low"]:
                        subtrend["Last relative low datetime"] = candle["datetime"]
                        subtrend["Low"] = candle["low"]

        else:
            if trend["Low"] > candle["low"]:
                trend["Low"] = candle["low"]
                trend["Low datetime"] = candle["datetime"]

            if trend["High"] < candle["high"]:
                trend["High"] = candle["high"]
                trend["High datetime"] = candle["datetime"]

    else:
        if subtrend["Start"]:
            if subtrend["Direction"] == "Bullish" and candle["close"] > trend["High"]:
                index = subtrend["Start"]

                last_candle_previous_trend = subtrend["Last candle"]

                order_block = {
                    "Datetime": last_candle_previous_trend["datetime"],
                    "High": last_candle_previous_trend["high"],
                    "Low": last_candle_previous_trend["low"],
                    "Direction": "Bullish"
                }

                addOrderBlock(collection_name, timerange, order_block)

                change_of_character = {
                    "Datetime": candle["datetime"],
                    "Price": trend["High"],
                    "Reference": trend["High datetime"],
                    "Direction": "Bullish"
                }

                addChangeOfCharacter(collection_name, timerange, change_of_character)

            elif subtrend["Direction"] == "Bearish" and candle["close"] < trend["Low"]:
                index = subtrend["Start"]

                last_candle_previous_trend = subtrend["Last candle"]

                order_block = {
                    "Datetime": last_candle_previous_trend["datetime"],
                    "High": last_candle_previous_trend["high"],
                    "Low": last_candle_previous_trend["low"],
                    "Direction": "Bearish"
                }

                addOrderBlock(collection_name, timerange, order_block)

                change_of_character = {
                    "Datetime": candle["datetime"],
                    "Price": trend["Low"],
                    "Reference": trend["Low datetime"],
                    "Direction": "Bearish"
                }
                addChangeOfCharacter(collection_name, timerange, change_of_character)

        else:
            subtrend["Start"] = candle["datetime"]
            subtrend["End"] = candle["datetime"]
            subtrend["High"] = candle["high"]
            subtrend["Low"] = candle["low"]
            subtrend["Direction"] = candle["direction"]

            subtrend["Last relative high datetime"] = candle["datetime"]
            subtrend["Last relative low datetime"] = candle["datetime"]

            subtrend["Last candle"] = last_candle


    for key in candle:
        last_candle[key] = candle[key]

    if index:
        match timerange:
            case "1min":
                trend["End"] = subtrend["Start"] - timedelta(minutes=1)

        addTrend(collection_name, timerange, trend)

        resetDict(trend)
        resetDict(subtrend)

        return index

    return None