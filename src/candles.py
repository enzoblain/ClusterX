# Internal Imports
from src.log import addLog, displayError

# External Imports
import numpy as np
import pandas as pd

class Candles:
    def __init__(self, 
                 candles: pd.DataFrame, 
                 trends: pd.DataFrame,
                 sessions: pd.DataFrame,
                 one_dimension_structures: pd.DataFrame,
                 two_dimensions_structures: pd.DataFrame) -> None:
        
        self.candles = candles
        self.candles['datetime'] = pd.to_datetime(self.candles['datetime'])
        self.candles['direction'] = np.where(self.candles['close'] > self.candles['open'], 'Bullish', 'Bearish')

        self.trends = trends
        self.trends['datetime'] = pd.to_datetime(self.trends['datetime'])

        self.sessions = sessions
        self.sessions['datetime'] = pd.to_datetime(self.sessions['datetime'])
        
        self.one_dimension_structures = one_dimension_structures
        self.one_dimension_structures['datetime'] = pd.to_datetime(self.one_dimension_structures['datetime'])

        if not self.one_dimension_structures.empty:
            self.breaks_of_structure = self.one_dimension_structures[self.one_dimension_structures['type'] == 'Break of Structure']
            self.changes_of_character = self.one_dimension_structures[self.one_dimension_structures['type'] == 'Change of Character']
            self.relative_highs_lows = self.one_dimension_structures[self.one_dimension_structures['type'] == 'Relative High/Low']
        else:
            self.breaks_of_structure = pd.DataFrame()
            self.changes_of_character = pd.DataFrame()
            self.relative_highs_lows = pd.DataFrame()

        self.two_dimensions_structures = two_dimensions_structures
        self.two_dimensions_structures['datetime'] = pd.to_datetime(self.two_dimensions_structures['datetime'])

        if not self.two_dimensions_structures.empty:
            self.order_blocks = self.two_dimensions_structures[self.two_dimensions_structures['type'] == 'Order Block']
            self.fair_value_gaps = self.two_dimensions_structures[self.two_dimensions_structures['type'] == 'Fair Value Gap']
        else:
            self.order_blocks = pd.DataFrame()
            self.fair_value_gaps = pd.DataFrame()