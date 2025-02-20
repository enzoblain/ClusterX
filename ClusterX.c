#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

#include "include/config.h"
#include "include/candle.h"
#include "include/session.h"


int main() {
    // Create the candles array
    struct Candle *candles_1min = initCandles(MAX_1MIN_ARRAY_LENGTH);
    struct Session *sessions_1min = initSessions(MAX_SESSION_ARRAY_LENGTH);

    // Get a new candle from the file
    for (int i = 0; i < 15; i++) {
        addTestCandle("EURUSD", "1min", MAX_1MIN_ARRAY_LENGTH, candles_1min);

        if (candles_1min[i].datetime == 0) {
            break;
        }
        
        getSessions(sessions_1min, candles_1min[i], MAX_SESSION_ARRAY_LENGTH);
    }

    for (int i = 0; i < 15; i++) {
        if (sessions_1min[i].start == 0) {
            break;
        }
        printSession(sessions_1min[i]);
    }

    // struct Session* sessions_1min = getSessions(candles_1min);

    // Free all the stuff
    free(candles_1min);
    free(sessions_1min);

    return 0;
}