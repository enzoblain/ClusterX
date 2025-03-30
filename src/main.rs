use clusterx::algorithm::main::algorithm;
use clusterx::Candle;
use clusterx::CONFIG;
use clusterx::data::handler::{get_backtest_data, get_last_candle_from_api};

use chrono::NaiveDateTime;
use polars::prelude::DataFrame;
use std::collections::HashMap;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let (env, mut tickers, timerange) = {
        let config = CONFIG.lock().unwrap();
        (config.env.clone(), config.tickers.clone(), config.timerange.clone())
    };

    let mut data: HashMap<String, DataFrame> = HashMap::new(); // This will only be used in dev mode
    if env == "dev" {
        // In dev mode, we get the data from folders
        data = get_backtest_data(&tickers)?;
        tickers = data.keys().cloned().collect(); // Only keep the tickers that are in the data
    }

    // Main algorithm
    let mut _i = 0; // Counter for the row number
    loop {
        if tickers.is_empty() {
            // If there are no tickers left, break the loop
            break;
        }
        for ticker in tickers.clone() {
            let current_candle: Candle;

            if env == "dev" {
                let ticker_data = data.get(&ticker).unwrap();

                if _i == ticker_data.height() - 1{
                    // If we are at the end of the data, revmove the ticker from the list
                    // Because no more data is available
                    tickers.retain(|x| x != &ticker);
                }
                
                // Get the i candle from the data
                current_candle = Candle::new_candle(
                    NaiveDateTime::parse_from_str(&ticker_data.column("datetime").unwrap().get(_i).unwrap().to_string(), "%Y-%m-%d %H:%M:%S").unwrap(),
                    ticker_data.column("open").unwrap().get(_i).unwrap().to_string().parse::<f64>().unwrap(),
                    ticker_data.column("high").unwrap().get(_i).unwrap().to_string().parse::<f64>().unwrap(),
                    ticker_data.column("low").unwrap().get(_i).unwrap().to_string().parse::<f64>().unwrap(),
                    ticker_data.column("close").unwrap().get(_i).unwrap().to_string().parse::<f64>().unwrap(),
                    ticker_data.column("volume").unwrap().get(_i).unwrap().to_string().parse::<i64>().unwrap(),
                );

                _i += 1;
            } else {
                std::thread::sleep(std::time::Duration::from_secs(60)); // Sleep for 1 minute
                current_candle = get_last_candle_from_api(&ticker, &timerange)?;
            }

            algorithm(current_candle.clone(), ticker.clone());
        }
        
    }
    
    Ok(())
}