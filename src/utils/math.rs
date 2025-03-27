use crate::utils::utils::{convert_anytype_to_f64, convert_option_to_f64, convert_option_to_i32};

use num::integer::div_rem;
use plotters::prelude::LogScalable;
use polars::prelude::*;
use std::f64::consts::PI;

pub struct DivisionResult {
    pub divisor: i32,
    pub quotient: i32,
    pub remainder: i32,
}

pub fn apply_normal_distribution(x: f64, mean: f64, standard_deviation: f64) -> f64 {
    let exponent = -((x - mean).powi(2)) / (2.0 * standard_deviation.powi(2));
    let coeff = 1.0 / (standard_deviation * (2.0 * PI).sqrt());
    return coeff * exponent.exp()
}

pub fn get_normal_distribution_bars(values: Series) -> DataFrame {
    let sorted_values = values.sort(SortOptions::default()).unwrap();
    let min = convert_anytype_to_f64(sorted_values.get(0).unwrap()).unwrap();
    let max = convert_anytype_to_f64(sorted_values.get(sorted_values.len() - 1).unwrap()).unwrap();
    let chunks = generate_chunks(min, max, 20);

    let start_series = Series::new("start".into(), chunks.iter().map(|(start, _, _)| *start).collect::<Vec<f64>>());
    let end_series = Series::new("end".into(), chunks.iter().map(|(_, end, _)| *end).collect::<Vec<f64>>());
    let mean_series = Series::new("mean".into(), chunks.iter().map(|(_, _, mean)| *mean).collect::<Vec<f64>>());

    let mut df = DataFrame::new(vec![
        start_series.into(), 
        end_series.into(), 
        mean_series.into()
    ]).unwrap();

    let bars = calculate_bars(sorted_values, chunks.clone());

    df.with_column(bars.clone()).unwrap();

    let min_bars = convert_option_to_i32(bars.min().unwrap()).unwrap().as_f64();
    let max_bars = convert_option_to_i32(bars.max().unwrap()).unwrap().as_f64();

    let mean = values.mean().unwrap();
    let standard_deviation = values.std(0).unwrap();

    let chunk_std = calculate_chunk_std(chunks.clone(), mean, standard_deviation);
    let chunk_std_scale = apply_to_scale(chunk_std, min_bars, max_bars);

    df.with_column(chunk_std_scale).unwrap();

    df
}

pub fn apply_to_scale (serie: Series, min: f64, max: f64) -> Series {
    let serie_min = convert_option_to_f64(serie.min().unwrap()).unwrap();
    let serie_max = convert_option_to_f64(serie.max().unwrap()).unwrap();
    
    let serie_diff = serie_max - serie_min;
    let scale_diff = max - min;

    let updated_values = serie
        .f64()
        .unwrap()
        .into_iter()
        .map(|value| {
            let value = value.unwrap();
            let new_value = min + ((value - serie_min) / serie_diff) * scale_diff;
            new_value
        })
        .collect::<Vec<f64>>();

    Series::new("Normal distribution".into(), updated_values)
}

pub fn generate_chunks(min: f64, max: f64, chunk_number: i32) -> Vec<(f64, f64, f64)> {
    let mut chunks = Vec::new();
    let distance = max - min;
    let chunk_size = distance / chunk_number as f64;

    for i in 0..chunk_number {
        let start = min + (i as f64 * chunk_size);
        let end = start + chunk_size;
        let mean = (start + end) / 2.0;
        chunks.push((start, end, mean));
    }

    return chunks;
}

pub fn calculate_bars(values: Series, chunks: Vec<(f64, f64, f64)>) -> Series {
    let mut bars = Vec::new();
    let mut chunk_number = 0;
    let max_chunk_number = chunks.len() - 1;

    let mut count = 0;
    let len = values.len();
    let mut i = 0;

    while i < len {
        // If we are in the last chunk, we just add the remaining values
        if chunk_number == max_chunk_number {
            bars.push(count);
            break;
        }

        let value = convert_anytype_to_f64(values.get(i).unwrap()).unwrap();

        let (_start, end, _mean) = chunks[chunk_number];
        if value < end {
            count += 1;
            i += 1;
        } else {
            chunk_number += 1;
            bars.push(count);
            count = 0;
        }
    } 
    
    Series::new("bars".into(), bars)
}

pub fn calculate_chunk_std (chunks: Vec<(f64, f64, f64)>, mean: f64, standard_deviation: f64) -> Series {
    let mut chunk_std = Vec::new();
    for (_start, _end, chunk_mean) in chunks {
        let std = apply_normal_distribution(chunk_mean, mean, standard_deviation);
        chunk_std.push(std);
    }

    let serie = Series::new("std".into(), chunk_std);

    return serie;
}

pub fn get_divisors(dividend: i32) -> Vec<DivisionResult> {
    let mut divisors = Vec::new();
    for divisor in 1..=dividend {
        let (quotient, remainder) = div_rem(dividend, divisor);
        let result = DivisionResult {
            divisor: divisor,
            quotient: quotient,
            remainder: remainder,
        };

        if result.remainder == 0 {
            divisors.push(result);
        }
    }
    return divisors
}