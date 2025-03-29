use std::collections::HashMap;

#[derive(Clone)]
pub struct Decision {
    pub signal: String, // "buy" or "sell" or "nothing"
    pub price: f64,
    pub stop_loss: f64,
    pub take_profit: f64,
}

pub fn take_decision (decisions: HashMap<String, Decision>) -> Decision {
    // This function will take the decision based on the signals
    // Should use a ml algorithm to take the decision
    // Such as a random forest or a neural network
    // For now it will just return the first signal
    let keys = decisions.keys().cloned().collect::<Vec<String>>();
    let first_signal = decisions.get(&keys[0]).unwrap().clone();
    
    first_signal
}