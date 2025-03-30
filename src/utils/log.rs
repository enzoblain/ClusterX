use crate::CONFIG;

use std::sync::Mutex;
use std::io::Write;

pub static LOG_FOLDER: &str = "logs";
pub static LOG_FILENAME: Mutex<String> = Mutex::new(String::new());

pub fn init_log() {
    // Create the log folder if it doesn't exist
    if !std::path::Path::new(LOG_FOLDER).exists() {
        std::fs::create_dir(LOG_FOLDER).expect("Failed to create log folder");
    }

    // Get the log number
    get_log_filename();

    let config = CONFIG.lock().unwrap();
    let env = config.env.clone();

    // Create the log file
    let log_filename = LOG_FILENAME.lock().unwrap().clone();
    std::fs::write(&log_filename, "").expect("Failed to create log file");

    display_log("Welcome to ClusterX !".to_string());
    display_log("Version: 0.1.0".to_string());
    display_log(format!("Running algorithm in environment: {}", env));
}

pub fn get_log_filename() {
    // Scan the log folder for files
    let paths = std::fs::read_dir(&LOG_FOLDER).expect("Failed to read log folder");
    let mut log_number = 0;
    for path in paths {
        let path = path.expect("Failed to read path").path();
        if path.is_file() {
            // Check if the file name starts with "log" and ends with ".txt"
            if let Some(file_name) = path.file_name() {
                if let Some(file_name_str) = file_name.to_str() {
                    if file_name_str.starts_with("log_") && file_name_str.ends_with(".log") {
                        // Extract the number from the file name
                        let file_number = file_name_str[4..file_name_str.len()-4].parse::<u32>().unwrap();
                        
                        // Find the maximum number
                        if file_number > log_number {
                            log_number = file_number;
                        }
                    }
                }
            }
        }
    }

    // Increment the log number for the new log file
    log_number += 1;
    let log_filename = format!("{}/log_{}.log", LOG_FOLDER, log_number);
    let mut log_filename_mutex = LOG_FILENAME.lock().unwrap();
    *log_filename_mutex = log_filename;
}

pub fn display_log(message: String) {
    let log_filename = LOG_FILENAME.lock().unwrap().clone();

    let mut file = std::fs::OpenOptions::new()
        .append(true)  // Append to the file instead of overwriting
        .open(log_filename)
        .expect("Failed to open log file");

    let now = chrono::Local::now();
    let timestamp = now.format("%d-%m-%Y %H:%M:%S").to_string();

    writeln!(file, "[{}] {}", timestamp, message).expect("Failed to write to log file");
}