use crate::Candle;
use crate::CONFIG;
use crate::strategies;
use crate::algorithm::decision::take_decision;
use crate::algorithm::order::place_order;

pub fn algorithm(current_candle: Candle, ticker: String) {
    // Do all the strategies to get the decisions
    let mut decisions  = std::collections::HashMap::new();
    decisions.insert(ticker.clone(), strategies::normal_distribution::strategy(current_candle));

    let config = CONFIG.lock().unwrap();
    if config.env != "dev" { 
        // Call the decision function to take the final decision
        let decision = take_decision(decisions);

        // Place the order
        place_order(decision, ticker).unwrap();
    }
}