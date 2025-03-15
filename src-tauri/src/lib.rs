// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
pub mod config;
pub mod data;
pub mod utils;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .setup(|_app| {
            utils::log::init_log();
            utils::log::display_log("INFO", "BACKEND", "Starting application");

            Ok(())
        })
        .on_window_event(|_window, event| {
            if let tauri::WindowEvent::CloseRequested { api: _, .. } = event {
                utils::log::display_log("INFO", "BACKEND", "Closing application");
            }
        })
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![
            data::analyzer::get_data_folders,
            data::handler::rename_dataset,
            data::handler::copy_dataset,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
