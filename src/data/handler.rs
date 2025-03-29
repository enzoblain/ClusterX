use crate::{CONFIG, ENV};

use chrono::NaiveDateTime;
use polars::prelude::*;
use reqwest::blocking::get;
use std::collections::HashMap;
use std::fs::File;
use std::vec;

#[derive(Debug)]
pub struct Candle {
    pub datetime: NaiveDateTime,
    pub open: f64,
    pub high: f64,
    pub low: f64,
    pub close: f64,
    pub volume: i64,
}

pub fn get_backtest_data (tickers: &Vec<String>) -> Result<HashMap<String, DataFrame>, Box<dyn std::error::Error>> {
    // Check the data folder
    // And get all the folders inside
    // Then check if the folder name is in the tickers list
    // If it is, then keep it for later
    let data_folder = CONFIG.lock().unwrap().data_folder.clone();
    let mut available_tickers = Vec::new();
    if let Ok(entries) = std::fs::read_dir(data_folder) {
        for entry in entries {
            let path = entry?.path();
            let folder_name = path.file_name().unwrap().to_str().unwrap().to_string();
            if path.is_dir() {
                if tickers.contains(&folder_name) {
                    available_tickers.push(path.clone());
                }
            }
        }
    } else {
        Err("Failed to read data folder")?;
    }

    // Create a HashMap to store the dataframes
    // The key will be the ticker name and the value will be the dataframe
    let mut dataframes: HashMap<String,DataFrame> = HashMap::new();

    // For each ticker, check if there is a data.csv file
    for ticker in &available_tickers {
        let ticker_data = ticker.join("data.csv");
        let ticker_name = ticker.file_name().unwrap().to_str().unwrap().to_string();
        if ticker_data.exists() {
            // If it exists, then read the data from the csv file
            let df = get_dataframe_from_csv(ticker_data.to_str().unwrap())?;
            dataframes.insert(ticker_name, df);
        } else {
            println!("Could not find data.csv for ticker {}", ticker_name);
        }
    }

    Ok(dataframes)
}

pub fn get_last_candle_from_api(ticker: &str, timerange: &str) -> Result<Candle, Box<dyn std::error::Error>> {
    // Get the api endpoint and the api key from the config
    let api_endpoint = CONFIG.lock().unwrap().api_endpoint.clone();
    let api_key = ENV.lock().unwrap().api_key.clone();

    let url = format!("{}symbol={}&interval={}&apikey={}&outputsize=1", api_endpoint, ticker, timerange, api_key);

    // Make the request to the API
    // And parse the response
    let response = get(&url)?;
    let body = response.text()?;
    let parsed = serde_json::from_str::<serde_json::Value>(&body)?;

    // Check if the response is ok
    let status: Option<String> = Some(parsed.get("status").unwrap().as_str().unwrap().to_string());
    if let Some(ref value) = status {
        if value != "ok" {
            Err(format!("API returned an error: {}", body))?;
        }
    } else {
        Err("The value is None")?;
    }

    let values = parsed.get("values").and_then(|v| v.as_array()).ok_or("No 'values' field found in the response.")?;
    let not_parsed_candle = values.get(0).ok_or("No values found in the response.")?;
    
    // Parse the datetime field
    // If the timerange is 1day, 1week or 1month, then we need to add the time to the datetime
    // Otherwise, we just need the date
    let mut datetime_str = not_parsed_candle.get("datetime").unwrap().as_str().unwrap().to_string();
    if vec!["1day", "1week", "1month"].contains(&timerange) {
        datetime_str = format!("{} 00:00:00", datetime_str);
    }
    let datetime = NaiveDateTime::parse_from_str(&datetime_str, "%Y-%m-%d %H:%M:%S")?; // Parse the datetime string to NaiveDateTime

    // Parse the other fields
    let open = not_parsed_candle.get("open").unwrap().as_str().unwrap().parse::<f64>()?;
    let high = not_parsed_candle.get("high").unwrap().as_str().unwrap().parse::<f64>()?;
    let low = not_parsed_candle.get("low").unwrap().as_str().unwrap().parse::<f64>()?;
    let close = not_parsed_candle.get("close").unwrap().as_str().unwrap().parse::<f64>()?;
    let volume = not_parsed_candle.get("volume").unwrap().as_str().unwrap().parse::<i64>()?;

    let candle = Candle {
        datetime,
        open,
        high,
        low,
        close,
        volume,
    };

    Ok(candle) 
}

pub fn get_dataframe_from_csv(path: &str) -> Result<DataFrame, PolarsError> {
    // Read the csv file and parse it to a dataframe
    let file = File::open(path).expect("could not open file");
    let df = CsvReader::new(file).finish()?;

    // Parse the datetime column to a datetime type
    let df = df.lazy()
        .with_columns([
            col("datetime")
            .str()
            .to_datetime(
                Some(TimeUnit::Microseconds),
                None,
                StrptimeOptions {
                    format: Some("%Y-%m-%dT%H:%M:%S%.3f".into()),
                    ..Default::default()
                },
                lit("raise"),
            )
        ])
    .collect()?;

    Ok(df)
}

pub fn get_series_from_dataframe(df: &DataFrame, column_name: &str) -> Result<Series, PolarsError> {
    let series = df.column(column_name)?.as_series().unwrap().to_owned();
    Ok(series)
}