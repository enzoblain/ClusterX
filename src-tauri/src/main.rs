// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]
mod config;
mod utils;

fn main() {
    utils::log::init_log();
    utils::log::display_log("INFO", "BACKEND", "Starting the app");

    clusterx_lib::run()
}
