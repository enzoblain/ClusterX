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
};

struct Candle* getCandles(char *symbol, char *interval, int limit);
void saveCandles(struct Candle *candles, int length, char *symbol, char *interval);

#endif
