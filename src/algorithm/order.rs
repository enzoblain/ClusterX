use crate::Decision;

pub fn place_order(decision: Decision, _ticker: String) -> Result<(),  Box<dyn std::error::Error>> {
    // If the decision tells us to do nothing, pas
    if decision.signal == "nothing" {
        Ok(())
    } else {
        unimplemented!() 
    }

}