use tauri::command;

use crate::config;
use crate::utils;

#[command(async)]
pub fn get_data_folders() -> Result<Vec<String>, ()> {
    let data_folder = config::USER_DATA_FOLDER;
    let mut data_folders= Vec::new();

    match std::fs::read_dir(data_folder) {
        Ok(dir) => {
            for entry in dir {
                match entry {
                    Ok(entry) => {
                        let path = entry.path();

                        if path.is_dir() {
                            let folder_name = path.file_name().unwrap();

                            data_folders.push(folder_name.to_str().unwrap().to_string());
                        }
                    }
                    Err(e) => {
                        utils::log::display_log("ERROR", "BACKEND", &format!("Error reading data folder: {:?}", e));
                        return Err(());
                    }
                }
            }
        }

        Err(e) => {
            if e.kind() == std::io::ErrorKind::NotFound {
                std::fs::create_dir(data_folder).expect("Error creating data folder");
            } else {
                utils::log::display_log("ERROR", "BACKEND", &format!("Error reading data folder: {:?}", e));
                return Err(());
            }
        }
    }

    utils::log::display_log("INFO", "BACKEND", &format!("{} folder(s) loaded successfully: {:?}", data_folders.len(), data_folders));
    return Ok(data_folders);
} 