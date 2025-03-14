use tauri::command;

use crate::config;
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