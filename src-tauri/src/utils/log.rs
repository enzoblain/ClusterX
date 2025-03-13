use chrono;
use std::io::Write;

use crate::config;

pub fn find_log_number() {
    let log_folder = std::path::Path::new(config::LOG_FOLDER);
    let mut last_log_number = 0;

    if !log_folder.exists() {
        std::fs::create_dir(log_folder).unwrap();
    }else {
        match std::fs::read_dir(log_folder) {
            Ok(dir) => {
                for entry in dir {
                    match entry {
                        Ok(entry) => {
                            let file_name = entry.file_name();
                            let file_name = file_name.to_str().unwrap();

                            // Check only the files that start with "log_"
                            if file_name.starts_with("log_") {
                                let log_number = file_name.replace("log_", "").replace(".log", "").parse::<u32>().unwrap();

                                if log_number > last_log_number {
                                    last_log_number = log_number;
                                }
                            }
                        }

                        Err(e) => {
                            eprintln!("Error reading log folder: {:?}", e);
                            
                            std::process::exit(1);
                        }
                    }
                }
            }

            Err(e) => {
                eprintln!("Error reading log folder: {:?}", e);

                std::process::exit(1);
            }
        }
    }

    let mut global_log_number = config::log_number.lock().unwrap();
    *global_log_number = last_log_number + 1; // Increment the log number because we are creating a new log file

}  

pub fn init_log() {
    find_log_number();
     let log_file = format!("{}/log_{}.log", config::LOG_FOLDER, config::log_number.lock().unwrap());

    // Create the log file
    std::fs::write(&log_file, "").unwrap();

    display_log("INFO", "BACKEND", "Initializing log");
}

pub fn display_log(log_type: &str, source: &str, message: &str) {
    let actual_time = chrono::Local::now();
    let formatted_time = actual_time.format("%Y-%m-%d %H:%M:%S");

    let log_file = format!("{}/log_{}.log", config::LOG_FOLDER, config::log_number.lock().unwrap());
    let log_message = format!("{} [{}] [{}] {}\n", formatted_time, log_type, source, message);

    let mut file = std::fs::OpenOptions::new()
        .create(true)
        .append(true)
        .open(log_file)
        .unwrap();

    write!(file, "{}", log_message).unwrap();
}