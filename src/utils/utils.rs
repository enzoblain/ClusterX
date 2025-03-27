use polars::prelude::*;

pub fn convert_anytype_to_f64(value: AnyValue<'_>) -> Result<f64, PolarsError> {
    match value {
        AnyValue::Float64(value) => Ok(value),
        _ => Err(PolarsError::ComputeError(format!("Unsuported value type {:?}", value).into())),
    }

}
pub fn convert_option_to_f64(value: Option<f64>) -> Result<f64, PolarsError> {
    match value {
        Some(value) => Ok(value),
        None => Err(PolarsError::ComputeError("Value is None".into())),
    }
}

pub fn convert_option_to_i32(value: Option<i32>) -> Result<i32, PolarsError> {
    match value {
        Some(value) => Ok(value),
        None => Err(PolarsError::ComputeError("Value is None".into())),
    }
}