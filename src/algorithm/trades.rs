use chrono::NaiveDateTime;
use once_cell::sync::Lazy;
use polars::prelude::*;
use std::fs::File;
use std::io::BufWriter;
use std::sync::Mutex;


pub static TRADES: Lazy<Mutex<DataFrame>> = Lazy::new(|| {
    Mutex::new(
        DataFrame::new(vec![
            Series::new("beginning".into(), Vec::<NaiveDateTime>::new()).into(),
            Series::new("ending".into(), Vec::<NaiveDateTime>::new()).into(),
            Series::new("reason".into(), Vec::<String>::new()).into(),
            Series::new("success".into(), Vec::<bool>::new()).into(),
            Series::new("signal".into(), Vec::<String>::new()).into(),
            Series::new("entry".into(), Vec::<f64>::new()).into(),
            Series::new("exit".into(), Vec::<f64>::new()).into(),
            Series::new("amount".into(), Vec::<f64>::new()).into(),
            Series::new("result".into(), Vec::<f64>::new()).into(),
            Series::new("profit".into(), Vec::<f64>::new()).into(),
        ])
        .unwrap(),
    )
});

pub fn add_to_trades(beginning: NaiveDateTime, ending: NaiveDateTime, reason: String, success: bool, signal: String, entry: f64, exit: f64, amount: f64, result: f64) {
    let beginning_series = Series::new("beginning".into(), vec![beginning]);
    let ending_series = Series::new("ending".into(), vec![ending]);
    let reason_series = Series::new("reason".into(), vec![reason]);
    let success_series = Series::new("success".into(), vec![success]);
    let signal_series = Series::new("signal".into(), vec![signal]);
    let entry_series = Series::new("entry".into(), vec![entry]);
    let exit_series = Series::new("exit".into(), vec![exit]);
    let amount_series = Series::new("amount".into(), vec![amount]);
    let result_series = Series::new("result".into(), vec![result]);
    let profit_series = Series::new("profit".into(), vec![result - amount]);

    let df = DataFrame::new(vec![
        beginning_series.into(),
        ending_series.into(),
        reason_series.into(),
        success_series.into(),
        signal_series.into(),
        entry_series.into(),
        exit_series.into(),
        amount_series.into(),
        result_series.into(),
        profit_series.into(),
    ]);

    let mut trades = TRADES.lock().unwrap();
    let mut trades_df = trades.clone();

    trades_df.vstack_mut(&df.unwrap()).unwrap();
    *trades = trades_df;
}

pub fn save_trades() {
    let mut trades_df = TRADES.lock().unwrap().clone();
    let file = File::create("result/trades.csv").unwrap();
    let mut writer = BufWriter::new(file);

    CsvWriter::new(&mut writer)
        .finish(&mut trades_df)
        .unwrap();
}