#include "config.h"
#include "candle.h"
#include "system_operator.h"

struct Candle* getCandles(char *symbol, char *interval, int limit) {
    struct Candle* candles = malloc(limit * sizeof(struct Candle));

    if (!candles) {
        printf("Memory allocation failed\n");

        exit(1);
    }

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
    char *lines[1000];
    int lines_count = 0;

    // Stock candles
    fgets(line, sizeof(line), file); // Remove header line
    while (fgets(line, sizeof(line), file) != NULL) {
        lines[lines_count] = strdup(line);

        lines_count++;
    }

    fclose(file);

    // Take only the last limit candles
    int start_index = 0;
    if (lines_count > limit) {
        start_index = lines_count - limit;
    }

    for (int i = 0; i < start_index; i++) {
        free(lines[i]); // Free unused candle
    }
    
    int index = 0; // Index for candles array
    for (int i = start_index; i < lines_count; i++) {
        time_t datetime = atol(strtok(lines[i], ",")); // First column
        float high = atof(strtok(NULL, ",")); // Second column
        float open = atof(strtok(NULL, ",")); // Third column
        float close = atof(strtok(NULL, ",")); // Fourth column
        float low = atof(strtok(NULL, ",")); // Fifth column

        char *tmp = strtok(NULL, ",");
        if (tmp != NULL) { // Check if there are more columns
            printf("Error in csv file (line %d)\n", i + 2);

            // Free memory before exiting
            free(candles);
            exit(1);
        }

        candles[index] = (struct Candle){datetime, high, open, close, low};

        free(lines[i]); // Free used candle
        index++;
    }

    return candles;
}

void saveCandles(struct Candle *candles, int length, char *symbol, char *interval) {
    char filepath[100];
    sprintf(filepath, "data/%s/%s", symbol, interval);

    // Create the directories if it does not exist
    if (create_full_path(filepath) == -1) {
        exit(1);
    }   

    // Get the entire file path (with the file name)
    sprintf(filepath, "%s/candles.csv", filepath);

    FILE *file = fopen(filepath, "w");

    if (file == NULL) {
        perror("Error while saving file: ");

        exit(1);
    }

    fprintf(file, "datetime,high,open,close,low\n"); // Header
    for (int i = 0; i < length; i++) {
        if (candles[i].datetime == 0) { // Do not after the first empty candle
            break;
        }

        fprintf(file, "%ld,%.6f,%.6f,%.6f,%.6f\n", candles[i].datetime, candles[i].high, candles[i].open, candles[i].close, candles[i].low);
    }

    fclose(file);
}