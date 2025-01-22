# Local imports
from src.log import displayError

# External imports
import numpy as np

from typing import List

def fibonacciRetracement(start: np.float64, end: np.float64) -> List[np.float64]:
    if not start or not end:
        displayError("Invalid start or end value for fibonacciRetracement")

    levels = [0.236, 0.382, 0.5, 0.618, 0.786]
    retracement = [start]

    try:
        for level in levels:
            retracement.append(start + (end - start) * level)

        retracement.append(end)

    except Exception as e:
        displayError(e)

    return retracement

def lotSizeCalculator(balance: np.float64, risk: np.float64, stop_loss_pips: np.float64, symbol: str) -> np.float64:
    if not balance or not risk or not stop_loss_pips or not symbol:
        displayError("Invalid balance, risk or stopLoss value for lotSizeCalculator")

    pip_values = {
        "EURUSD": 0.0001,
    }

    if symbol not in pip_values:
        displayError(f"Invalid symbol \”{symbol}\”")

    try:
        risk_amount = balance * (risk / 100)
        pip_value = pip_values[symbol]
        lot_size =  risk_amount / (stop_loss_pips * pip_value)
        
        return (balance * risk) / stop_loss_pips

    except Exception as e:
        displayError(e)