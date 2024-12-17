from src.data_processing.data_handler import *
from src.utils.utils import *

def main():
    API_KEY = getFromEnv('API_KEY')
    data = getDataFromTwelveDataAPI(API_KEY, getValueFromConfigFile('config.json', 'Symbol'))

    print(data)

if __name__ == "__main__":
    main()