# Local imports
from src.log import addLog, displayError
from src.data import getDataFromTwelveDataAPI, getDataFrameFromCsv, saveDataFrameToCsv
from src.structures import getCandlesDirection, getTrendsAndOrderBlocks, getSessions, findFairValueGaps
from src.utils import getValueFromConfigFile, getFromEnv

# External imports
import pandas as pd

async def algo(discord_bot: object):
    # message = "Test message"
    # await discord_bot.send_message(message)

    api_key = getFromEnv('API_KEY')
    symbol = getValueFromConfigFile('config.json', 'Symbol')
    env = getValueFromConfigFile('config.json', 'Environment')

    if env not in ['prd', 'dev', 'test']:
       displayError(f"Invalid run type \"{env}\"")

    if env == 'prd' or env == 'dev':
        intervals = ['1min', '5min', '15min', '30min', '1h', '4h', '1day', '1week']
    elif env == 'test':
        intervals  = ['1min']
        

    for interval in intervals:
        if env == 'prd' or env == 'dev':
            addLog(f"Preparing data for analysis (interval: {interval})")

            addLog(f"Getting data from Twelve Data API")
            APIdata = getDataFromTwelveDataAPI(api_key, symbol, interval=interval)

            addLog(f"Saving candles data to CSV")
            csv_path = saveDataFrameToCsv(symbol, interval, 'candles', APIdata, 'datetime')
        
        elif env == 'test':
            csv_path = f'data/{symbol}/{interval}/candles.csv'
    
        candles = getDataFrameFromCsv(csv_path)

        addLog(f"Adding candle data")
        candles = getCandlesDirection(candles)

        addLog(f"Getting trends data")
        trends = getDataFrameFromCsv(f'data/{symbol}/{interval}/trends.csv', returnNone=True)

        addLog(f"Getting structures data")
        structures = getDataFrameFromCsv(f'data/{symbol}/{interval}/structures.csv', returnNone=True)

        if structures.empty:
            addLog("No structures data found")
            order_blocks = pd.DataFrame()
            fair_value_gaps = pd.DataFrame()
        else: 
            order_blocks = structures[structures['type'] == 'Order Block']
            fair_value_gaps = structures[structures['type'] == 'Fair Value Gap']
        
        addLog(f"Defining the trends and the order blocks in market data")
        trends, order_blocks = getTrendsAndOrderBlocks(candles=candles, trends=trends, order_blocks=order_blocks)

        addLog(f"Saving trends data to CSV")
        saveDataFrameToCsv(symbol, interval, 'trends', trends, 'start')

        addLog(f"Getting sessions data")
        sessions = getDataFrameFromCsv(f'data/{symbol}/{interval}/sessions.csv', returnNone=True)

        addLog(f"Defining the sessions caracteristics in market data")
        sessions = getSessions(candles=candles, sessions=sessions)

        addLog(f"Saving sessions data to CSV")
        saveDataFrameToCsv(symbol, interval, 'sessions', sessions, 'start')

        addLog(f"Searching for fair value gaps in market data")
        fair_value_gaps = findFairValueGaps(candles, fair_value_gaps)

        fair_value_gaps['datetime'] = pd.to_datetime(fair_value_gaps['datetime'])
        order_blocks['datetime'] = pd.to_datetime(order_blocks['datetime'])

        structures = pd.concat([order_blocks, fair_value_gaps], ignore_index=True)
        structures.sort_values(by='datetime', inplace=True)
        structures.reset_index(drop=True, inplace=True)

        addLog(f"Saving structures data to CSV")
        saveDataFrameToCsv(symbol, interval, 'structures', structures, 'datetime')