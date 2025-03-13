use chrono;
use std::io::Write;

use crate::config;

pub fn init_log() {
    let log_file = config::LOG_PATH;

    // Create the log file
    std::fs::write(&log_file, "").unwrap();

    display_log("INFO", "BACKEND", "Initializing log");
}

pub fn display_log(log_type: &str, source: &str, message: &str) {
    let actual_time = chrono::Local::now();
    let formatted_time = actual_time.format("%Y-%m-%d %H:%M:%S");

    let log_message = format!("{} [{}] [{}] {}\n", formatted_time, log_type, source, message);

    let mut file = std::fs::OpenOptions::new()
        .create(true)
        .append(true)
        .open(config::LOG_PATH)
        .unwrap();

    write!(file, "{}", log_message).unwrap();
}