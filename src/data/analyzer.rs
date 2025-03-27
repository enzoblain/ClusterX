use polars::prelude::*;

pub fn add_growing_percentage(df: &mut DataFrame) -> Result<(), PolarsError> {
    let close_series = df.column("close").unwrap();
    let close_series = close_series.f64().unwrap();
    let mut growing_percentage = Vec::new();
    let mut previous_value = 0.0;
    for value in close_series.into_iter() {
        let value = value.unwrap();
        let percentage = if previous_value == 0.0 {
            0.0
        } else {
            (value - previous_value) / previous_value * 100.0
        };
        growing_percentage.push(percentage);
        previous_value = value;
    }
    let growing_percentage_series = Series::new("growing_percentage".into(), growing_percentage);
    df.with_column(growing_percentage_series).unwrap();

    Ok(())

}