import polars as pl
from src.visualisation import plot
import time
from collections import deque
from src.structures import processCandle, processSession, processFairValueGap, processTrend
from concurrent.futures import ThreadPoolExecutor
from src.redis import findCollection, create_collection, delAll, executePipe

def main():
    data = pl.read_csv("data/data.csv")
    data = data.with_columns(
        pl.col("datetime")
        .str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S")
        .alias("datetime"),
    )
    data = data.select(["datetime", "open", "high", "low", "close"])
    # data = data[:1000]

    pause_time = 0.0001
    results = []

    collection_name = "Backtest-1"

    collection_name = findCollection()
    create_collection(collection_name)

    last_session = {
        "Name": None,
        "Open": None,
        "Start": None,
        "High": None,
        "Low": None,
        "End": None,
        "Close": None
    }

    last_candle = {
        "datetime": None,
        "open": None,
        "high": None,
        "low": None,
        "close": None,
        "average": None,
        "direction": None
    }

    moving3candles = [
        {
            "datetime": None,
            "open": None,
            "high": None,
            "low": None,
            "close": None,
            "direction": None,
        }, {
            "datetime": None,
            "open": None,
            "high": None,
            "low": None,
            "close": None,
            "direction": None,
        }, {
            "datetime": None,
            "open": None,
            "high": None,
            "low": None,
            "close": None,
            "direction": None,
        }
    ]

    trend = {
        "Start": None,
        "End": None,
        "High": None,
        "Low": None,
        "Direction": None,

        "High datetime": None,
        "Low datetime": None
    }

    subtrend = {
        "Start": None,
        "End": None,
        "High": None,
        "Low": None,
        "Direction": None,

        "Last relative high datetime": None,
        "Last relative low datetime": None,

        "Last candle": None
    }

    timerange = "1min"

    queue = deque()

    total_time = 0

    for candle in data.iter_rows(named=True):
        start = time.time()

        processCandle(candle, collection_name, timerange)
        
        # handle_candle(candle, last_session, collection_name, moving3candles, queue, last_candle, trend, subtrend, timerange)


        processSession(candle, last_session, collection_name)
        processFairValueGap(candle, moving3candles, collection_name, timerange)
        processTrend(queue, candle, last_candle, trend, subtrend, collection_name, timerange)

        executePipe()

        results.append(candle)

        if pause_time > 0:
            time.sleep(pause_time)

        elif pause_time == -1:
            break

        duration = time.time() - start
        total_time += duration

    avg_time_per_candle = (total_time / len(data)) * 1000

    print(f"Average time per candle: {avg_time_per_candle:.2f} ms")
    
    # results = pl.DataFrame(results)
    # plot(results)

def handle_candle(candle, last_session, collection_name, moving3candles, queue, last_candle, trend, subtrend, timerange):

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(processSession, candle, last_session, collection_name),
            executor.submit(processFairValueGap, candle, moving3candles, collection_name, timerange),
            executor.submit(processTrend, queue, candle, last_candle, trend, subtrend, collection_name, timerange)
        ]
        
        for future in futures:
            future.result()

        executePipe()

if __name__ == "__main__":
   main() 
