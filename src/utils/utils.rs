use polars::prelude::*;
use std::collections::HashMap;

// This functions generate chunks of a given range
// A chunk represents a range of values
// All chunks are of the same size
pub fn generate_chunks(min: f64, max: f64, chunk_number: i32) -> Vec<HashMap<String, f64>> {
    let mut chunks = Vec::new();
    let distance = max - min;
    let chunk_size = distance / chunk_number as f64;

    for i in 0..chunk_number {
        let start = min + (i as f64 * chunk_size);
        let end = start + chunk_size;
        let mean = (start + end) / 2.0;
        chunks.push(
            HashMap::from([
                ("start".to_string(), start),
                ("end".to_string(), end),
                ("mean".to_string(), mean),
            ]),
        );
    }

    return chunks;
}

// This function converts a value of type AnyValue to f64
// In case of selecting value in a DataFrame
pub fn convert_anytype_to_f64(value: &AnyValue<'_>) -> Result<f64, PolarsError> {
    match value {
        AnyValue::Float64(value) => Ok(*value),
        _ => Err(PolarsError::ComputeError(format!("Unsuported value type {:?}", value).into())),
    }
}