use crate::{CONFIG, ENV};

use chrono::NaiveDateTime;
use polars::prelude::*;
use reqwest::blocking::get;
use std::fs::File;

pub fn get_from_api(ticker: &str, timerange: &str, start_date: Option<&str>, end_date: Option<&str>) -> Result<(), Box<dyn std::error::Error>> {
    let api_endpoint = CONFIG.lock().unwrap().api_endpoint.clone();
    let api_key = ENV.lock().unwrap().api_key.clone();

    let mut url = api_endpoint;

    if let Some(start_date) = start_date {
        url = format!("{}?start_date={}", url, start_date);
    }

    if let Some(end_date) = end_date {
        url = format!("{}?end_date={}", url, end_date);
    }

    url = format!("{}&symbol={}&interval={}&apikey={}", url, ticker, timerange, api_key);

    let response = get(&url)?;
    let body = response.text()?;
    let parsed = serde_json::from_str::<serde_json::Value>(&body)?;

    let status: Option<String> = Some(parsed.get("status").unwrap().as_str().unwrap().to_string());
    
    if let Some(ref value) = status {
        if value != "ok" {
            Err(format!("API returned an error: {}", body))?;
        }
    } else {
        println!("The value is None");
    }
    if let Some(values) = parsed.get("values").and_then(|v| v.as_array()) {
        let datetime_vals: Vec<NaiveDateTime>;
        if vec!["1day", "1week", "1month"].contains(&timerange) {
            println!("Parsing date with format %Y-%m-%d");
            datetime_vals = values.iter()
            .filter_map(|v| {
                v.get("datetime")
                    .and_then(|n| n.as_str())
                    .and_then(|s| {
                        let datetime_str = if s.len() == 10 {
                            format!("{} 00:00:00", s)
                        } else {
                            s.to_string()
                        };
    
                        NaiveDateTime::parse_from_str(&datetime_str, "%Y-%m-%d %H:%M:%S").ok()
                    })
            })
            .collect();
        } else {
            datetime_vals = values.iter().filter_map(|v| v.get("datetime").and_then(|n| n.as_str()).and_then(|s| NaiveDateTime::parse_from_str(s, "%Y-%m-%d %H:%M:%S").ok())).collect();
        }
        let open_vals: Vec<f64> = values.iter().filter_map(|v| v.get("open").and_then(|n| n.as_str()).map(|s| s.parse::<f64>().unwrap())).collect();
        let high_vals: Vec<f64> = values.iter().filter_map(|v| v.get("high").and_then(|n| n.as_str()).map(|s| s.parse::<f64>().unwrap())).collect();
        let low_vals: Vec<f64> = values.iter().filter_map(|v| v.get("low").and_then(|n| n.as_str()).map(|s| s.parse::<f64>().unwrap())).collect();
        let close_vals: Vec<f64> = values.iter().filter_map(|v| v.get("close").and_then(|n| n.as_str()).map(|s| s.parse::<f64>().unwrap())).collect();
        let volume_vals: Vec<i64> = values.iter().filter_map(|v| v.get("volume").and_then(|n| n.as_str()).map(|s| s.parse::<i64>().unwrap())).collect();

        let datetime_series = Series::new("datetime".into(), datetime_vals);
        let open_series = Series::new("open".into(), open_vals);
        let high_series = Series::new("high".into(), high_vals);
        let low_series = Series::new("low".into(), low_vals);
        let close_series = Series::new("close".into(), close_vals);
        let volume_series = Series::new("volume".into(), volume_vals);

        let mut df = DataFrame::new(vec![
            datetime_series.into(), open_series.into(), high_series.into(), low_series.into(), close_series.into(), volume_series.into()
        ])?;

        save_dataframe_to_csv(&mut df)?;

    } else {
        Err("No 'values' field found in the response.")?;
    }

    Ok(())
}

pub fn save_dataframe_to_csv(df: &mut DataFrame) -> Result<(), PolarsError> {
    let mut file = File::create("example.csv").expect("could not create file");
    CsvWriter::new(&mut file)
        .include_header(true) 
        .with_separator(b',')
        .finish(df)?;
    
    Ok(())
}

pub fn get_dataframe_from_csv(path: &str) -> Result<DataFrame, PolarsError> {
    let file = File::open(path).expect("could not open file");
    let df = CsvReader::new(file).finish()?;

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