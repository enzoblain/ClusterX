# Local imports
from src.log import addLog
from src.data import getDataFromTwelveDataAPI, getDataFrameFromCsv, saveDataFrameToCsv
from src.structures import getCandlesDirection, getTrendsAndOrderBlocks, getSessions, findFairValueGaps
from src.utils import getValueFromConfigFile, getFromEnv, setIndex

async def algo(discord_bot: object):
    # message = "Test message"
    # await discord_bot.send_message(message)

    api_key = getFromEnv('API_KEY')
    symbol = getValueFromConfigFile('config.json', 'Symbol')

    # intervals = ['1min', '5min', '15min', '30min', '1h', '4h', '1day', '1week']
    intervals  = ['1min']

    for interval in intervals:
        addLog(f"Preparing data for analysis (interval: {interval})")

        addLog(f"Getting data from Twelve Data API")
        APIdata = getDataFromTwelveDataAPI(api_key, symbol, interval=interval)

        addLog(f"Saving data to CSV")
        csv_path = saveDataFrameToCsv(symbol, interval, APIdata)
        csv_data = getDataFrameFromCsv(csv_path)

        candles = setIndex(csv_data, 'datetime')

        addLog(f"Adding candle data")
        candles = getCandlesDirection(candles)
        
        addLog(f"Defining the trends and the order blocks in market data")
        trends, order_blocks = getTrendsAndOrderBlocks(candles=candles)

        addLog(f"Defining the sessions caracteristics in market data")
        sessions = getSessions(candles=candles)

        addLog(f"Searching for fair value gaps in market data")
        fair_value_gaps = findFairValueGaps(candles)