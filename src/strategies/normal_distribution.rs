use crate::Candle;
use crate::Decision;
use crate::maths::normal_distribution::formula;
use crate::utils::utils::{generate_chunks, convert_anytype_to_f64};

use chrono::NaiveDateTime;
use once_cell::sync::Lazy;
use polars::prelude::*;
use std::sync::Mutex;
use std::vec;

// Use to store the candles in a DataFrame
// As a sliding window
pub static CANDLES: Lazy<Mutex<DataFrame>> = Lazy::new(|| {
    Mutex::new(
        DataFrame::new(vec![
            Series::new("datetime".into(), Vec::<NaiveDateTime>::new()).into(),
            Series::new("open".into(), Vec::<f64>::new()).into(),
            Series::new("high".into(), Vec::<f64>::new()).into(),
            Series::new("low".into(), Vec::<f64>::new()).into(),
            Series::new("close".into(), Vec::<f64>::new()).into(),
            Series::new("volume".into(), Vec::<i64>::new()).into(),
            Series::new("fluctuation".into(), Vec::<f64>::new()).into(),
        ])
        .unwrap(),
    )
});

pub fn strategy(current_candle: Candle) -> Vec<Decision> {
    let mut candle = CANDLES.lock().unwrap();
    let current_candle_row = current_candle.get_candle_as_row();

    // Add the current candle to the DataFrame
    *candle = candle.vstack(&current_candle_row).unwrap();

    // If we reach the sliding window size, we remove the oldest candle
    // Else, we don't have enough data to make a decision
    if candle.height() == 50 + 1{
        *candle = candle.slice(1, candle.height() - 1);
    } else {
        let decision = Decision {
            signal: "none".into(),
            price: None,
            stop_loss: None,
            take_profit: None,
            limit: None,
        };
    
        return vec![decision]
    }

    // Get the min and max fluctuation to generate the chunks
    let min_fluctuation = candle.column("fluctuation").unwrap().f64().unwrap().min().unwrap();
    let max_fluctuation = candle.column("fluctuation").unwrap().f64().unwrap().max().unwrap();
    let chunk_number = 25;
    let chunks = generate_chunks(min_fluctuation, max_fluctuation, chunk_number);
    
    // Create a new DataFrame to store the normal distribution
    let mut normal_distribution = DataFrame::new(vec![
        Series::new("start".into(), Vec::<f64>::new()).into(),
        Series::new("end".into(), Vec::<f64>::new()).into(),
        Series::new("mean".into(), Vec::<f64>::new()).into(),
        Series::new("count".into(), Vec::<f64>::new()).into(),
    ]).unwrap();

    for (index, chunk) in chunks.iter().enumerate() {
        let start = *chunk.get("start").unwrap();
        let end = *chunk.get("end").unwrap();
        let mean = *chunk.get("mean").unwrap();

        // Get the number of candles in the chunk
        let fluctuation_col = candle.column("fluctuation").unwrap().f64().unwrap();
        let mask = fluctuation_col.gt_eq(start) & fluctuation_col.lt(end);
        let mut count = candle.filter(&mask).unwrap().height();
        
        // If it's the last chunk, we need to add the last candle
        if index as i32 == chunk_number - 1 {
            count += 1;
        }

        // Transform the chunk into a DataFrame
        // To store the normal distribution
        let chunk_row = DataFrame::new(vec![
            Series::new("start".into(), vec![start]).into(),
            Series::new("end".into(), vec![end]).into(),
            Series::new("mean".into(), vec![mean]).into(),
            Series::new("count".into(), vec![count as f64]).into(),
        ]).unwrap();

        normal_distribution = normal_distribution.vstack(&chunk_row).unwrap();
    }

    // Calculate the parameters of the normal distribution
    let mean = normal_distribution.column("mean").unwrap().f64().unwrap().mean().unwrap();
    let std = normal_distribution.column("mean").unwrap().f64().unwrap().std(0).unwrap();

    let mean_col = normal_distribution.column("mean").unwrap().f64().unwrap();
    let distribution = mean_col.apply(
        |x| Some(formula(mean, std, x.unwrap()) * 50 as f64),
    );
    let distribution_series = Series::new("distribution".into(), distribution).into_column();
    normal_distribution = normal_distribution.hstack(&vec![distribution_series]).unwrap();

    // Calculate the difference between the normal distribution and the count
    let count_col = normal_distribution.column("count").unwrap().f64().unwrap();
    let distribution_col = normal_distribution.column("distribution").unwrap().f64().unwrap();
    let diff = count_col - distribution_col;
    let diff_series = Series::new("diff".into(), diff).into_column();
    normal_distribution = normal_distribution.hstack(&vec![diff_series]).unwrap();

    // Create a abs diff column to see the max difference
    let diff_col = normal_distribution.column("diff").unwrap().f64().unwrap();
    let abs_diff = diff_col.apply(|x| Some(x.unwrap().abs()));
    let abs_diff_series = Series::new("abs diff".into(), abs_diff).into_column();
    normal_distribution = normal_distribution.hstack(&vec![abs_diff_series]).unwrap();

    // Due to the normal distribution,
    // We multiply the difference by a factor based on the position of each value.
    // The values closer to the center (middle) are multiplied by the highest factor,
    // While the values at the extremes (first and last) are multiplied by the smallest factor.
    let mean = normal_distribution.column("abs diff").unwrap().f64().unwrap().mean().unwrap();
    let std = normal_distribution.column("abs diff").unwrap().f64().unwrap().std(0).unwrap();
    let abs_diff_col = normal_distribution.column("abs diff").unwrap().f64().unwrap();
    let abusive_diff = abs_diff_col.apply(
        |x| Some(formula(mean, std / 5 as f64, x.unwrap())),
    );
    let abusive_diff_series = Series::new("abusive diff".into(), abusive_diff).into_column();
    normal_distribution = normal_distribution.hstack(&vec![abusive_diff_series]).unwrap();

    // Get the max value of the abusive diff
    // Store all the rows with the max value
    let max_abusive_diff = normal_distribution.column("abusive diff").unwrap().f64().unwrap().max().unwrap();
    let max_abusive_diff_col = normal_distribution.column("abusive diff").unwrap().f64().unwrap();
    let mask = max_abusive_diff_col.equal(max_abusive_diff);
    let max_abusive_diff_row = normal_distribution.filter(&mask).unwrap();

    // Store all the decisions
    let mut decisions = Vec::new();

    for i in 0..max_abusive_diff_row.height() {
        let row = max_abusive_diff_row.get(i).unwrap();
        let obj_percentage = convert_anytype_to_f64(row.get(2).unwrap()).unwrap();

        // Determine the signal based on the difference
        let signal;
        if obj_percentage > 0.0 {
            signal = "buy";
        } else {
            signal = "sell";
        }

        let price = current_candle.close;
        let take_profit = price * (100 as f64+ obj_percentage) / 100 as f64;
        let stop_loss = 0.0;

        let decision = Decision {
            signal: signal.into(),
            price: Some(price),
            stop_loss: Some(stop_loss),
            take_profit: Some(take_profit),
            limit: None,
        };

        decisions.push(decision);
    }

    decisions
}