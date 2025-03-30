use crate::utils::log::display_log;

use std::collections::HashMap;

#[derive(Clone, Debug)]
pub struct Decision {
    pub signal: String, // "buy" or "sell" or "nothing"
    pub price: Option<f64>,
    pub stop_loss: Option<f64>,
    pub take_profit: Option<f64>,
    pub limit: Option<String>,
}

pub fn take_decision (decisions: HashMap<String, Vec<Decision>>, ticker: &str) -> Decision {
    for strategy in decisions.keys() {
        for decision in decisions.get(strategy).unwrap(){
            if decision.signal == "nothing" {
                display_log(format!("Strategy: \"{}\" return nothing for \"{}\"", strategy, ticker));
            } else {
                display_log(format!("Strategy: \"{}\" return signal to \"{}\" with take profit at \"{}\" for \"{}\"", strategy, decision.signal, decision.take_profit.unwrap(), ticker));
            }
        }
    }
    // This function will take the decision based on the signals
    // Should use a ml algorithm to take the decision
    // Such as a random forest or a neural network
    // For now it will just return the first signal
    let keys = decisions.keys().cloned().collect::<Vec<String>>();
    let first_signal = decisions.get(&keys[0]).unwrap().clone().get(0).unwrap().clone();
    
    first_signal
}