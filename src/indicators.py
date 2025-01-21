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