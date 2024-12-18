from src.data_processing.data_handler import *
from src.data_processing.data_saver import saveDataFrameToCsv
from src.utils.utils import getFromEnv, getValueFromConfigFile
from src.utils.log import initLog

from src.utils.discord import launchBot

def main(): 
    initLog()
    launchBot()
    
    # api_key = getFromEnv('API_KEY')
    # symbol = getValueFromConfigFile('config.json', 'Symbol')
    
    # data = getDataFromTwelveDataAPI(api_key, symbol)
    # saveDataFrameToCsv(symbol, "1min", data)

if __name__ == "__main__":
    main()