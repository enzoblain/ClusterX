import asyncio
from src.data_processing.data_handler import getDataFromTwelveDataAPI, getDataFrameFromCsv
from src.utils.utils import setIndex
from src.data_processing.data_saver import saveDataFrameToCsv
from src.utils.utils import getFromEnv, getValueFromConfigFile
from src.utils.log import initLog
from src.data_processing.data_analyzer import checkDataContinuity
from src.execution.algo import algo
from src.utils.discord import DiscordBot

async def main(): 
    initLog()

    api_key = getFromEnv('API_KEY')
    symbol = getValueFromConfigFile('config.json', 'Symbol')

    interval = '1min'

    APIdata = getDataFromTwelveDataAPI(api_key, symbol, interval=interval)
    csv_path = saveDataFrameToCsv(symbol, "1min", APIdata)
    csv_data = getDataFrameFromCsv(csv_path)

    data = setIndex(csv_data, 'datetime')

    holes = checkDataContinuity(data)

    discord_bot = DiscordBot()
    _ = asyncio.create_task(discord_bot.start())
    await discord_bot.wait_until_ready()

    try:
        while True:
            await algo(discord_bot)
            await asyncio.sleep(5)

    except Exception as e:
        raise e

if __name__ == "__main__":
    asyncio.run(main())