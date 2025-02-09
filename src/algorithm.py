from src.api import getDataFromTwelveDataApi
from src.data import saveDataframetoCSV, getDataFrameFromCsv, combineDataFrames, loadOldData, updateData
from src.utils import getFromConfigFile, delNonAlphaChars
from src.structures import getSessions, getCandlesDirection, getFVG

import pandas as pd

def algorithm():
    env = getFromConfigFile("Environment")
    symbol = getFromConfigFile("Symbol")

    data = loadOldData(env, symbol) # Load old data
    data = updateData(data, env, symbol) # Update the data

    print(data)