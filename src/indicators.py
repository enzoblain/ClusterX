import numpy as np

from typing import List

def fibonacciRetracement(start: np.float64, end: np.float64) -> List[np.float64]:
    if not start or not end:
        raise ValueError("Invalid start or end value for Fibonacci Retracement")

    levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1] # Basics Fibonacci levels 
    retracement = [start + (end - start) * level for level in levels] # Calculate the retracement levels

    return retracement

def lotSizeCalculator(balance: np.float64, risk: np.float64, stop_loss_pips: np.float64, symbol: str) -> np.float64:
    if not balance or not risk or not stop_loss_pips or not symbol:
        raise Exception("Invalid balance, risk or stopLoss value for lotSizeCalculator")

    pip_values = { # Pip values for each symbol
        "EUR/USD": 0.0001,
    }

    if symbol not in pip_values:
        raise Exception(f"Invalid symbol \”{symbol}\”")

    risk_amount = balance * (risk / 100)
    pip_value = pip_values[symbol]
    lot_size = risk_amount / (stop_loss_pips * pip_value)

    return lot_size
