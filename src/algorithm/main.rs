use crate::Candle;
use crate::CONFIG;
use crate::strategies;
use crate::algorithm::decision::take_decision;
use crate::algorithm::order::place_order;

pub fn algorithm(current_candle: Candle, ticker: String) {
    let config = CONFIG.lock().unwrap();
    // Get all the strategies required
    let strategies = config.strategies.clone();

    // Check if strategies are empty
    if strategies.is_empty() {
        panic!("No strategies found in the config file");
    }

    // Do all the strategies to get the decisions
    let mut decisions  = std::collections::HashMap::new();
    if strategies.contains(&"Normal Distribution".to_string()) {
        // Call the normal distribution strategy
        decisions.insert("Normal Distribution".to_string(), strategies::normal_distribution::strategy(&current_candle));
    }

    // Call the decision function to take the final decision
    let decision = take_decision(decisions, &ticker);

    if config.env != "dev" { 
        // Place the order
        place_order(decision, ticker).unwrap();
    }
}