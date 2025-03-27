use clusterx::CONFIG;
use clusterx::data::handler::{get_from_api, get_dataframe_from_csv, get_series_from_dataframe};
use clusterx::data::analyzer::add_growing_percentage;
use clusterx::utils::math::get_normal_distribution_bars;

use plotters::prelude::*;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let (tickers, timerange) = {
        let config = CONFIG.lock().unwrap();
        (config.tickers.clone(), config.timerange.clone())
    };

    let start_date = "2020-01-01";
    let end_date = "2024-31-12";
    
    if true == false {
        for ticker in tickers {
            get_from_api(&ticker, &timerange, Some(start_date), Some(end_date))?;
        }
    }

    let mut df = get_dataframe_from_csv("example.csv")?;
    add_growing_percentage(&mut df)?;

    let growing_percentage = get_series_from_dataframe(&df, "growing_percentage")?;

    df = get_normal_distribution_bars(growing_percentage);

    let start_values = get_series_from_dataframe(&df, "start")?.f64().unwrap().into_no_null_iter().collect::<Vec<f64>>();
    let end_values = get_series_from_dataframe(&df, "end")?.f64().unwrap().into_no_null_iter().collect::<Vec<f64>>();
    let mean_values = get_series_from_dataframe(&df, "mean")?.f64().unwrap().into_no_null_iter().collect::<Vec<f64>>();
    let bars = get_series_from_dataframe(&df, "bars")?.i32().unwrap().into_no_null_iter().collect::<Vec<i32>>();
    let normalized_std = get_series_from_dataframe(&df, "Normal distribution")?.f64().unwrap().into_no_null_iter().collect::<Vec<f64>>();

    let max_bar = bars.iter().max().unwrap();

    let root_area = BitMapBackend::new("histogram.png", (800, 600))
        .into_drawing_area();
    root_area.fill(&WHITE)?;

    let mut chart = ChartBuilder::on(&root_area)
        .caption("Growing Percentage Apple", ("sans-serif", 30))
        .set_label_area_size(LabelAreaPosition::Left, 60)
        .set_label_area_size(LabelAreaPosition::Bottom, 60)
        .build_cartesian_2d(
            start_values[0]..end_values[end_values.len() - 1],
            0.0..(*max_bar as f64),
        )?;

    chart.configure_mesh().draw()?;

    chart.configure_mesh()
        .x_labels(4) 
        .y_labels(5) 
        .x_label_formatter(&|x| format!("{:.1}", x)) 
        .draw()?;

    chart.draw_series(
        bars.into_iter().enumerate().map(|(i, count )| {
            let x0 = start_values[i];
            let x1 = end_values[i];
            let y0 = 0.0;
            let y1 = count as f64;

            Rectangle::new(
                [(x0, y0), (x1, y1)], 
                RED.filled(),
            )
        }),
    )?;


    chart.draw_series(LineSeries::new(
        mean_values.iter().zip(normalized_std.iter()).map(|(&x, &y)| (x as f64, y as f64)),
        &BLUE,
    ))?;
    
    Ok(())
}