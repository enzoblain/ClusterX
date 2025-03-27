use std::fs;
use std::sync::Mutex;
use once_cell::sync::Lazy;
use serde::Deserialize;

#[derive(Deserialize)]
pub struct Config {
    pub tickers: Vec<String>,
    pub timerange: String,
    pub api_endpoint: String,
}

pub static CONFIG: Lazy<Mutex<Config>> = Lazy::new(|| {
    let config_file= "config/config.toml";
    let toml_content = fs::read_to_string(config_file).expect("Failed to read config.toml");
    let config: Config = toml::from_str(&toml_content).expect("Failed to parse env.toml");

    Mutex::new(config)
});

#[derive(Deserialize)]
pub struct Env {
    pub api_key: String,
}

pub static ENV: Lazy<Mutex<Env>> = Lazy::new(|| {
    let config_file = "config/env.toml";
    let toml_content = fs::read_to_string(config_file).expect("Failed to read env.toml");
    let env: Env = toml::from_str(&toml_content).expect("Failed to parse config.toml");
    
    Mutex::new(env)
});