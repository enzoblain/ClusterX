#include "utils.h"

// Function to get cool displayable datetime (day-month-year hour:minute:second)
char *getStringDatetime(time_t time){
    const char format[] = "%d-%m-%Y %H:%M:%S";
    char *datetime = malloc(20);

    struct tm *timeinfo = localtime(&time);
    strftime(datetime, 19, format, timeinfo);

    return datetime;
}

// Function to get the time from the beginning of the day in seconds
time_t getDayTime(time_t time){
    struct tm *timeinfo = localtime(&time);
    time_t total_seconds = timeinfo->tm_hour * 3600 + timeinfo->tm_min * 60 + timeinfo->tm_sec;

    return total_seconds;
}