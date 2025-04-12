use crate::Candle;
use crate::CONFIG;
use crate::strategies;
use crate::algorithm::decision::take_decision;
use crate::algorithm::order::{place_order, check_orders};

pub fn algorithm(current_candle: Candle, ticker: String) {
    // Check if some orders has been liquidated or out of time
    check_orders(&current_candle, &ticker);
    
    // Get all the strategies required
    let strategies = {
        let config = CONFIG.lock().unwrap();
        config.strategies.clone()
    };

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

    // Place the order
    place_order(decision, ticker).unwrap();
}