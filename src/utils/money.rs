use crate::algorithm::trades::add_to_trades;
use crate::utils::log::display_log;

use chrono::NaiveDateTime;
use once_cell::sync::Lazy;
use std::sync::Mutex;

pub static MONEY: Lazy<Mutex<f64>> = Lazy::new(|| {
    Mutex::new(0.0)
});

pub static MONEY_IN_TRADES: Lazy<Mutex<f64>> = Lazy::new(|| {
    Mutex::new(0.0)
});

pub fn init_money(money: f64) {
    let mut money_lock = MONEY.lock().unwrap();
    *money_lock = money;
}

pub fn get_trade_result(entry: f64, exit: f64, signal: String, amount: f64, beginning: NaiveDateTime, ending: NaiveDateTime, finished: bool, reason: String) -> f64 {
    let mut percentage_diff = (exit - entry) / entry;
    if signal == "sell" {
        percentage_diff = -percentage_diff;
    }
    let result = (1.0 + percentage_diff) * amount;

    if finished {
        if result > amount {
            display_log(format!("Trade successful (Entry: {}, Exit: {}, Signal: {}, Amount: {})", entry, exit, signal, amount));
        } else {
            display_log(format!("Trade unsuccessful (Entry: {}, Exit: {}, Signal: {}, Amount: {})", entry, exit, signal, amount));
        }

        add_to_trades(
            beginning,
            ending,
            reason,
            result > amount,
            signal,
            entry,
            exit,
            amount,
            result,
        );
    }

    result
}