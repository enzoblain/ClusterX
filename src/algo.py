# Local imports
from src.log import addLog, displayError
from src.data import getDataFromTwelveDataAPI, getDataFrameFromCsv, saveDataFrameToCsv
from src.structures import getCandlesDirection, getTrends, getSessions, findFairValueGaps
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
        two_dimensions_structures = getDataFrameFromCsv(f'data/{symbol}/{interval}/2dStructures.csv', returnNone=True)
        one_dimension_structures = getDataFrameFromCsv(f'data/{symbol}/{interval}/1dStructures.csv', returnNone=True)

        if two_dimensions_structures.empty:
            addLog("No 2d structures data found")
            order_blocks = pd.DataFrame()
            fair_value_gaps = pd.DataFrame()
        else: 
            order_blocks = two_dimensions_structures[two_dimensions_structures['type'] == 'Order Block']
            fair_value_gaps = two_dimensions_structures[two_dimensions_structures['type'] == 'Fair Value Gap']

        if one_dimension_structures.empty:
            addLog("No 1d structures data found")
            breaks_of_structure = pd.DataFrame()
            changes_of_character = pd.DataFrame()
            relative_highs_lows = pd.DataFrame()
        else:
            breaks_of_structure = one_dimension_structures[one_dimension_structures['type'] == 'Break of Structure']
            changes_of_character = one_dimension_structures[one_dimension_structures['type'] == 'Change of Character']
            relative_highs_lows = one_dimension_structures[one_dimension_structures['type'] == 'Relative High/Low']

        
        addLog(f"Defining the trends and the order blocks in market data")
        trends, order_blocks, breaks_of_structure, changes_of_character, relative_highs_lows = getTrends(candles=candles, trends=trends, order_blocks=order_blocks, breaks_of_structure=one_dimension_structures, changes_of_character=one_dimension_structures, relative_highs_lows=relative_highs_lows)

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

        one_dimension_structures_types = [breaks_of_structure, changes_of_character, relative_highs_lows]
        one_dimension_structures_not_empty = []

        for one_dimension_structure_type in one_dimension_structures_types:
            if not one_dimension_structure_type.empty:
                one_dimension_structure_type['datetime'] = pd.to_datetime(one_dimension_structure_type['datetime'])
                one_dimension_structures_not_empty.append(one_dimension_structure_type)

        if one_dimension_structures_not_empty:
            one_dimension_structures = pd.concat(one_dimension_structures_not_empty, ignore_index=True)
            one_dimension_structures.sort_values(by='datetime', inplace=True)
            one_dimension_structures.reset_index(drop=True, inplace=True)

            addLog(f"Saving 1d structures data to CSV")
            saveDataFrameToCsv(symbol, interval, '1dStructures', one_dimension_structures, 'datetime')
        
        else:
            addLog("None new 1d structures found")

        two_dimensions_structures_types = [order_blocks, fair_value_gaps]
        two_dimensions_structures_not_empty = []

        for two_dimensions_structure_type in two_dimensions_structures_types:
            if not two_dimensions_structure_type.empty:
                two_dimensions_structure_type['datetime'] = pd.to_datetime(two_dimensions_structure_type['datetime'])
                two_dimensions_structures_not_empty.append(two_dimensions_structure_type)            

        if two_dimensions_structures_not_empty:
            two_dimensions_structures = pd.concat(two_dimensions_structures_not_empty, ignore_index=True)
            two_dimensions_structures.sort_values(by='datetime', inplace=True)
            two_dimensions_structures.reset_index(drop=True, inplace=True)

            addLog(f"Saving 2d structures data to CSV")
            saveDataFrameToCsv(symbol, interval, '2dStructures', two_dimensions_structures, 'datetime')

        else:
            addLog("None new 2d structures found")