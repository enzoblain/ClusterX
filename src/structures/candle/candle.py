import pandas as pd

def getCandlesDirection(candles: pd.DataFrame):
    candles['direction'] = candles.apply(
        lambda row: 'bullish' if row['close'] > row['open'] else 'bearish', axis=1
    )
    
    return candles