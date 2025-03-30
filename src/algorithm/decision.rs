use std::collections::HashMap;

#[derive(Clone, Debug)]
pub struct Decision {
    pub signal: String, // "buy" or "sell" or "nothing"
    pub price: Option<f64>,
    pub stop_loss: Option<f64>,
    pub take_profit: Option<f64>,
    pub limit: Option<String>,
}

pub fn take_decision (decisions: HashMap<String, Vec<Decision>>) -> Decision {
    // This function will take the decision based on the signals
    // Should use a ml algorithm to take the decision
    // Such as a random forest or a neural network
    // For now it will just return the first signal
    let keys = decisions.keys().cloned().collect::<Vec<String>>();
    let first_signal = decisions.get(&keys[0]).unwrap().clone().get(0).unwrap().clone();
    
    first_signal
}