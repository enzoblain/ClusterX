import pandas as pd

def findOrderBlocks(candles : pd.DataFrame, trends : pd.DataFrame, order_blocks: list = None):
    if not order_blocks:
        i = 0
        order_blocks = []
    else:
        order_blocks = order_blocks.to_dict(orient="records")
        datetime = order_blocks[-1]["datetime"]
        i = trends["end" == datetime].index + 1
    
    for i in range(i, len(trends)):
        current_datetime = candles.iloc[i].name
        order_blocks.append({
            "datetime": trends.iloc[i]["end"],
            "direction": trends.iloc[i]["direction"],
            "high": candles.loc[current_datetime]["high"],
            "low": candles.loc[current_datetime]["low"],
        })

    return order_blocks