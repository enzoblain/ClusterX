use lazy_static::lazy_static;
use std::sync::Mutex;

pub static USER_DATA_FOLDER: &str = "../public/data";
pub static LOG_FOLDER: &str = "../logs";

// Var that should be changed in the code
lazy_static! {
    pub static ref log_number: Mutex<u32> = Mutex::new(0);
}