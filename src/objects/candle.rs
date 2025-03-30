use chrono::NaiveDateTime;
use polars::prelude::*;

#[derive(Debug, Clone)]
pub struct Candle {
    pub datetime: NaiveDateTime,
    pub direction: String,
    pub open: f64,
    pub high: f64,
    pub low: f64,
    pub close: f64,
    pub volume: i64,
    pub fluctuation: f64,
}

impl Candle {
    // Constructor for Candle
    pub fn new_candle(datetime: NaiveDateTime, open: f64, high: f64, low: f64, close: f64, volume: i64) -> Self {
        Candle {
            datetime,
            direction: if open < close { "bullish".into() } else { "bearish".into() },
            open,
            high,
            low,
            close,
            volume,
            fluctuation: get_fluctuation(open, close),
        }
    }

    // Easily convert a Candle to a DataFrame row
    // This is useful for adding the candle to a DataFrame
    pub fn get_candle_as_row(&self) -> DataFrame {
        let datetime = Series::new("datetime".into(), vec![self.datetime]);
        let open = Series::new("open".into(), vec![self.open]);
        let high = Series::new("high".into(), vec![self.high]);
        let low = Series::new("low".into(), vec![self.low]);
        let close = Series::new("close".into(), vec![self.close]);
        let volume = Series::new("volume".into(), vec![self.volume]);
        let fluctuation = Series::new("fluctuation".into(), vec![self.fluctuation]);

        DataFrame::new(vec![
            datetime.into(),
            open.into(),
            high.into(),
            low.into(),
            close.into(),
            volume.into(),
            fluctuation.into(),
        ])
        .unwrap()
    }
}

// Function to calculate the fluctuation of a candle
// Percentage difference between open and close prices
pub fn get_fluctuation(open: f64, close: f64) -> f64 {
    let fluctuation = (close - open) / open * 100.0;
    fluctuation
}