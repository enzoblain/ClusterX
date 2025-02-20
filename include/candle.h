#ifndef CANDLE_H
#define CANDLE_H

#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Candle structure
struct Candle {
    time_t datetime;
    float high;
    float open;
    float close;
    float low;
    char direction[8];
};

struct Candle* initCandles(int limit);

void addTestCandle(char *symbol, char *timeframe, int limit, struct Candle *candles);
void setCandleDirection(struct Candle *candle);
void printCandle(struct Candle candle);

#endif
