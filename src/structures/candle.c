#include "candle.h"
#include "utils.h"

// For the backtest / test of the strategy
// Requires data in DATA directory
int CANDLE_1MIN_LAST_INDEX = 0;

// Function to initialize the candles array
struct Candle* initCandles(int limit){
    struct Candle* candles = malloc(limit * sizeof(struct Candle));

    if (!candles) {
        perror("malloc failed");

        return NULL;
    }

    return candles;
}

// Function for backtesting or testing the strategy
// Get the candles from the file instead of the API
void addTestCandle(char *symbol, char *interval, int limit, struct Candle* candles) {
    // Get the entire file path
    char filepath[100];
    sprintf(filepath, "data/%s/%s/candles.csv", symbol, interval);

    FILE *file = fopen(filepath, "r");

    if (file == NULL) {
        printf("Error while loading file: %s\n", filepath);

        free(candles);  // Free memory before exiting
        exit(1);
    }

    char line[256];
    int lines_count = 0;

    // To know where to stop reading the file (the first candle we don't have)
    int max_index = CANDLE_1MIN_LAST_INDEX + 1;
    struct Candle new_candle = {0};

    // Stock candles
    fgets(line, sizeof(line), file); // Remove header line
    while (fgets(line, sizeof(line), file) != NULL) {
        if (lines_count == max_index){
            // Get the candle data
            sscanf(line, "%ld,%f,%f,%f,%f",
                &new_candle.datetime,
                &new_candle.high,
                &new_candle.open,
                &new_candle.close,
                &new_candle.low);

            setCandleDirection(&new_candle);

            break;
        }

        lines_count++;
    }

    fclose(file);

    if (new_candle.datetime == 0){
        printf("No new candle found\n");

        return;
    }

    // Add the new candle to the array   
    // If the array is full, remove the first element (shift left) and add the new candle to the end 
    if (CANDLE_1MIN_LAST_INDEX >= limit){
        int index = 0;

        while (index < limit - 2){
            candles[index] = candles[index + 1];

            index++;
        }

        candles[limit - 1] = new_candle;
            
    }else{
        candles[CANDLE_1MIN_LAST_INDEX] = new_candle;
    }

    // Increment the index
    CANDLE_1MIN_LAST_INDEX++;
}

// Function to set the direction
void setCandleDirection(struct Candle *candle) {
    // Bullish if going up, Bearish if going down
    strcpy(candle->direction, (candle->open > candle->close) ? "Bearish" : "Bullish");
}

// Function to print the candle (for debugging)
void printCandle(struct Candle candle){
    char *datetime = getStringDatetime(candle.datetime);
    
    printf("Candle datetime: %s\n", datetime);
    printf("High: %.6f\n", candle.high);
    printf("Open: %.6f\n", candle.open);
    printf("Close: %.6f\n", candle.close);
    printf("Low: %.6f\n", candle.low);
    printf("Direction: %s\n", candle.direction);
}