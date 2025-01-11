import pandas as pd

def findFairValueGaps(candles: pd.DataFrame, fair_value_gaps : pd.DataFrame = None) -> pd.DataFrame:
    if not fair_value_gaps:
        fair_value_gaps = []
        i = 1
    else:
        fair_value_gaps = fair_value_gaps.to_dict('records')
        datetime = fair_value_gaps[-1]["datetime"]
        i = candles.get_loc(datetime) + 1
        
    for i in range(i, len(candles) - 1):
        if candles.iloc[i - 1]["low"] > candles.iloc[i + 1]["high"]: # bearish gap
            fair_value_gaps.append({
                "datetime": candles.iloc[i].name,
                "direction": "bearish",
                "high": candles.iloc[i -1]["low"],
                "low": candles.iloc[i + 1]["high"]
            })
        elif candles.iloc[i - 1]["high"] < candles.iloc[i + 1]["low"]: # bullish gap
            fair_value_gaps.append({
                "datetime": candles.iloc[i].name,
                "direction": "bullish",
                "high": candles.iloc[i + 1]["low"],
                "low": candles.iloc[i - 1]["high"]             
            })

    return pd.DataFrame(fair_value_gaps)