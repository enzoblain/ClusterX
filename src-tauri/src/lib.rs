// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
pub mod config;
pub mod data;
pub mod utils;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![
            data::analyzer::get_data_folders,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
