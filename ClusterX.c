#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

#include "include/config.h"
#include "include/candle.h"


int main() {
    // Example of how to use the functions defined in candle.h
    struct Candle* candles_1min = getCandles("EURUSD", "1min", MAX_1MIN_ARRAY_LENGTH);
    saveCandles(candles_1min, MAX_1MIN_ARRAY_LENGTH, "EURUSD", "1min");

    return 0;
}