use tauri::command;

use crate::config;
use crate::data::analyzer;
use crate::utils::log;

#[command]
pub fn rename_dataset(dataset: String, name: String) -> Result<(), ()> {  
    let data_folder = config::USER_DATA_FOLDER;

    let old_path = format!("{}/{}", data_folder, dataset);
    let new_path = format!("{}/{}", data_folder, name);

    match std::fs::rename(&old_path, &new_path) {
        Ok(_) => {
            log::display_log("INFO", "BACKEND", &format!("Dataset \"{}\" renamed to \"{}\"", dataset, name));

            return Ok(());
        }

        Err(e) => {
            log::display_log("ERROR", "BACKEND", &format!("Error renaming dataset: {:?}", e));
            return Err(());
        }
    }
}

#[command(async)] 
pub fn copy_dataset(source: &str) -> Result<(), ()> {
    let datasets = match analyzer::get_data_folders() {
        Ok(d) => d.into_iter().map(|s| s.to_lowercase()).collect::<Vec<String>>(),
        Err(_) => return Err(()),
    };

    let mut backtest_number = 0;

    // Find the next available backtest number
    loop {
        let backtest_name = format!("Backtest-{}", backtest_number).to_lowercase();
        if datasets.contains(&backtest_name) {
            backtest_number += 1;
        } else {
            break;
        }
    }

    let files = vec!["1min", "5min", "15min", "30min", "1hour", "4hour", "1day", "1week", "1month"];

    let destination = format!("{}/Backtest-{}", config::USER_DATA_FOLDER,backtest_number);
    let source_path = std::path::Path::new(source);
    let destination_path = std::path::Path::new(&destination);

    std::fs::create_dir(destination_path).unwrap();

    if !source_path.exists() {
        log::display_log("ERROR", "BACKEND", "Source folder does not exist");

        return Err(());
    }

    match std::fs::read_dir(source_path) {
        Ok(dir) => {
            // Check each entry in the source folder
            for entry in dir {
                match entry {
                    Ok(entry) => {
                        // Check if entry is a folder
                        if entry.path().is_dir() {
                            let dir_name = entry.file_name();

                            // If folder is "candles", create a new folder in the destination folder
                            if dir_name == "candles" {
                                let new_dir_path = format!("{}/{}", destination, dir_name.to_str().unwrap());
                                std::fs::create_dir(&new_dir_path).unwrap();
                                log::display_log("INFO", "BACKEND", &format!("Folder {:?} created successfully", new_dir_path));

                                // Copy all csv files in the "candles" folder to the new folder 
                                // Only the ones with goods names
                                match std::fs::read_dir(entry.path()) {
                                    Ok(candle_folder) => {
                                        for file in candle_folder {
                                            match file {
                                                Ok(file) => {
                                                    let path = file.path();

                                                    // Only copy files, not folders
                                                    if path.is_dir() {
                                                        continue;
                                                    }

                                                    let file_name = path.file_name().unwrap();
                                                    let file_name_without_ext = file_name.to_str().unwrap().split('.').collect::<Vec<&str>>()[0];
                                                    let file_extension = file_name.to_str().unwrap().split('.').collect::<Vec<&str>>()[1];

                                                    // Only copy csv files
                                                    if file_extension != "csv" {
                                                        continue;
                                                    }

                                                    // Only copy files with good names
                                                    if !files.contains(&file_name_without_ext) {
                                                        continue;
                                                    }

                                                    let new_path = format!("{}/{}", new_dir_path, file_name.to_str().unwrap());

                                                    match std::fs::copy(&path, new_path) {
                                                        Ok(_) => {
                                                            log::display_log("INFO", "BACKEND", &format!("File {:?} copied successfully", path));
                                                        }

                                                        Err(e) => {
                                                            log::display_log("ERROR", "BACKEND", &format!("Error copying file: {:?}", e));
                                                        }
                                                    }
                                                }

                                                Err(e) => {
                                                    log::display_log("ERROR", "BACKEND", &format!("Error reading candle folder: {:?}", e));
                                                }
                                            }
                                        }
                                    }

                                    Err(e) => {
                                        log::display_log("ERROR", "BACKEND", &format!("Error reading candle folder: {:?}", e));
                                    }
                                }
                            }    

                        } 
                    }

                    Err(e) => {
                        log::display_log("ERROR", "BACKEND", &format!("Error reading source folder: {:?}", e));
                    }
                }
            }

            init_dataset(&destination);

            log::display_log("INFO", "BACKEND", &format!("Folder {:?} copied successfully", source_path));
            return Ok(());
        }



        Err(e) => {
            log::display_log("ERROR", "BACKEND", &format!("Error reading source folder: {:?}", e));
            return Err(());
        }
    }
    
}

pub fn init_dataset(dataset: &str) {
    let data = serde_json::json!({
        "strategy": ""
    });

    let dataset_path = std::path::Path::new(&dataset);
    let config_path = dataset_path.join("config.json");

    std::fs::write(&config_path, serde_json::to_string_pretty(&data).unwrap()).unwrap();
}