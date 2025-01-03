from src.data_processing.data_analyzer import checkDataContinuity
from src.data_processing.data_handler import getDataFromTwelveDataAPI, getDataFrameFromCsv
from src.utils.utils import setIndex
from src.data_processing.data_saver import saveDataFrameToCsv
from src.utils.utils import getFromEnv, getValueFromConfigFile
from src.structures.candle.candle import getCandlesDirection

async def algo(discord_bot: object):
    # message = "Test message"
    # await discord_bot.send_message(message)

    api_key = getFromEnv('API_KEY')
    symbol = getValueFromConfigFile('config.json', 'Symbol')

    intervals = ['1min', '5min', '15min', '30min', '1h', '4h', '1day', '1week']

    for interval in intervals:
        APIdata = getDataFromTwelveDataAPI(api_key, symbol, interval=interval)
        csv_path = saveDataFrameToCsv(symbol, interval, APIdata)
        csv_data = getDataFrameFromCsv(csv_path)

        data = setIndex(csv_data, 'datetime')
        data = getCandlesDirection(data)

        holes = checkDataContinuity(data)