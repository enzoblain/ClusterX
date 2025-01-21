# Local imports
from src.log import addLog
from src.data import getDataFromTwelveDataAPI, getDataFrameFromCsv, saveDataFrameToCsv
from src.structures import getCandlesDirection, getTrendsAndOrderBlocks, getSessions, findFairValueGaps
from src.utils import getValueFromConfigFile, getFromEnv, setIndex

# External imports
import pandas as pd

async def algo(discord_bot: object):
    # message = "Test message"
    # await discord_bot.send_message(message)

    api_key = getFromEnv('API_KEY')
    symbol = getValueFromConfigFile('config.json', 'Symbol')

    # intervals = ['1min', '5min', '15min', '30min', '1h', '4h', '1day', '1week']
    intervals  = ['1min']

    run_type = getValueFromConfigFile('config.json', 'Run type')

    for interval in intervals:
        if run_type != 'test':
            addLog(f"Preparing data for analysis (interval: {interval})")

            addLog(f"Getting data from Twelve Data API")
            APIdata = getDataFromTwelveDataAPI(api_key, symbol, interval=interval)

            addLog(f"Saving data to CSV")
            csv_path = saveDataFrameToCsv(symbol, interval, 'candles', APIdata)
        
        else:
            csv_path = 'data/EURUSD/1min/candles.csv'
    
        candles = getDataFrameFromCsv(csv_path)
        candles.index = pd.to_datetime(candles.index)

        addLog(f"Adding candle data")
        candles = getCandlesDirection(candles)
        
        addLog(f"Defining the trends and the order blocks in market data")
        trends, order_blocks = getTrendsAndOrderBlocks(candles=candles)

        addLog(f"Defining the sessions caracteristics in market data")
        sessions = getSessions(candles=candles)

        addLog(f"Searching for fair value gaps in market data")
        fair_value_gaps = findFairValueGaps(candles)

        structure = pd.concat([order_blocks, fair_value_gaps], ignore_index=True)
        structure.sort_values(by='datetime', inplace=True)
        structure.reset_index(drop=True, inplace=True)

        saveDataFrameToCsv(symbol, interval, 'structures', structure)