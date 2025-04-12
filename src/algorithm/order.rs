use crate::Candle;
use crate::CONFIG;
use crate::Decision;
use crate::MONEY;
use crate::MONEY_IN_TRADES;
use crate::utils::money::get_trade_result;

use once_cell::sync::Lazy;
use std::collections::HashMap;
use std::sync::Mutex;

// Store all the orders
// Each orders is contained in a vector which is stored in a hashmap
// The key is the ticker
pub static ORDERS: Lazy<Mutex<HashMap<String, Vec<Decision>>>> = Lazy::new(|| {
    let orders = HashMap::new();
    Mutex::new(orders)
});

pub fn place_order(mut decision: Decision, ticker: String) -> Result<(),  Box<dyn std::error::Error>> {
    let config = CONFIG.lock().unwrap();
    let env = config.env.clone();

    // If the decision tells us to do nothing, pass
    if decision.signal == "nothing" {
        Ok(())
    } else {
        let gain = decision.take_profit.unwrap() - decision.price.unwrap();
        let loss = decision.price.unwrap() - decision.stop_loss.unwrap_or(0.0);
    
        if decision.signal == "sell" {
            if decision.stop_loss.is_none() {
                // If the decision is to sell, we need to set a stop loss
                return Err("You need to set a stop loss for a sell order".into());
            }

            if gain > 0.0 || loss > 0.0 || gain < loss {
                return Err("You need to set a valid stop loss for a sell order".into());

            }
        }
        if env == "dev" {
            // Update the available money
            // By getting the right risk
            let mut money = MONEY.lock().unwrap();
            let amount = config.risk / 100.0 * *money;

            decision.amount = Some(amount);
            *money -= amount;

            let mut orders = ORDERS.lock().unwrap();

            // If the ticker is not in the orders, add it
            if !orders.contains_key(&ticker) {
                orders.insert(ticker.clone(), Vec::new());
            }

            // Add the decision to the orders
            orders.get_mut(&ticker).unwrap().push(decision.clone());
        }

        Ok(())

    }

}

pub fn check_orders(candle: &Candle, ticker: &String) {
    let env = {
        let config = CONFIG.lock().unwrap();
        config.env.clone()
    };
    let mut money = MONEY.lock().unwrap();
    let mut money_in_trades = MONEY_IN_TRADES.lock().unwrap();

    // Reset the money in trades
    *money_in_trades = 0.0;

    if env == "dev" {
        let mut order_lock = ORDERS.lock().unwrap();
        let mut orders = order_lock.clone();

        // Check if the ticker is in the orders
        if orders.contains_key(ticker) {
            let mut i = 0;
            while i < orders.get(ticker).unwrap().len() {
                let order = orders.get(ticker).unwrap()[i].clone();

                if order.signal == "buy" {
                    // Check if the order is liquidated
                    if order.stop_loss.is_some() && candle.close < order.stop_loss.unwrap() {
                        orders.get_mut(ticker).unwrap().remove(i);
                        let result = get_trade_result(order.price.unwrap(), order.stop_loss.unwrap(), order.signal.clone(), order.amount.unwrap(), order.datetime, candle.datetime, true, "Stop loss".to_string());
                        *money += result;
                        continue;
                    }

                    if order.take_profit.is_some() && candle.close > order.take_profit.unwrap() {
                        orders.get_mut(ticker).unwrap().remove(i);
                        let result = get_trade_result(order.price.unwrap(), order.take_profit.unwrap(), order.signal.clone(), order.amount.unwrap(), order.datetime, candle.datetime, true, "Take profit".to_string());
                        *money += result;
                        continue;
                    }
                } else {
                    // Check if the order is liquidated
                    if order.stop_loss.is_some() && candle.close > order.stop_loss.unwrap() {
                        orders.get_mut(ticker).unwrap().remove(i);
                        let result = get_trade_result(order.price.unwrap(), order.stop_loss.unwrap(), order.signal.clone(), order.amount.unwrap(), order.datetime, candle.datetime, true, "Stop loss".to_string());
                        *money += result;
                        continue;
                    }

                    if order.take_profit.is_some() && candle.close < order.take_profit.unwrap() {
                        orders.get_mut(ticker).unwrap().remove(i);
                        let result = get_trade_result(order.price.unwrap(), order.take_profit.unwrap(), order.signal.clone(), order.amount.unwrap(), order.datetime, candle.datetime, true, "Take profit".to_string());
                        *money += result;
                        continue;
                    }
                }

                if order.limit.is_some() {
                    // Check if the order is out of time
                    if candle.datetime > order.limit.unwrap() {
                        let result = get_trade_result(order.price.unwrap(), candle.close, order.signal.clone(), order.amount.unwrap(), order.datetime, candle.datetime, true, "Time limit".to_string());
                        *money += result;
                        continue;
                    }
                }

                // Update the money in trades
                let result = get_trade_result(order.price.unwrap(), candle.close, order.signal.clone(), order.amount.unwrap(), order.datetime, candle.datetime, false, "".to_string());
                *money_in_trades += result;

                i += 1;
            }

            *order_lock = orders;
        }

    }
}