pub fn formula(mean: f64, std: f64, x: f64) -> f64 {
    let exponent = -((x - mean).powi(2)) / (2.0 * std.powi(2));
    let coefficient = 1.0 / (std * (2.0 * std::f64::consts::PI).sqrt());
    coefficient * exponent.exp()
}