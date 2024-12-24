import asyncio
from src.data_processing.data_handler import getDataFromTwelveDataAPI
from src.utils.data_utils import getDataFrameFromCsv
from src.utils.data_utils import setDatetimeIndex
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

    APIdata = getDataFromTwelveDataAPI(api_key, symbol)
    saveDataFrameToCsv(symbol, "1min",APIdata)
    data = setDatetimeIndex(getDataFrameFromCsv(f"data/{symbol.replace('/', '')}/1min.csv"))

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