import mplfinance as mpf
import pandas as pd

def plot(candles):
    df = candles.to_pandas()
    df["datetime"] = pd.to_datetime(df["datetime"])  # Convertir en datetime
    df.set_index("datetime", inplace=True)
    mpf.plot(df, type="candle", style="charles", volume=False, title="Candlestick Chart", ylabel="Price")