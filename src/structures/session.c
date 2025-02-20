#include "config.h"
#include "candle.h"
#include "session.h"
#include "utils.h"

// Store the reference sessions in an array
const struct RefSession ref_sessions[4] = {NEWYORK_PM_SESSION, ASION_SESSION, LONDON_SESSION, NEWYORK_AM_SESSION};

// Store the index of the last session
int last_session_index;
int session_count = 0;

// Initialize the sessions array
struct Session* initSessions(int limit){
    struct Session* sessions = malloc(limit * sizeof(struct Candle));

    if (!sessions) {
        perror("malloc failed");

        return NULL;
    }

    return sessions;
}

// Get the sessions from the candles
void getSessions(struct Session* sessions, struct Candle candle, int last_index) {
    time_t datetime = getDayTime(candle.datetime);
    time_t day = candle.datetime - datetime;

    // Get the index of the session to update or add
    // If the array is full, update the last session and shift the rest
    // Else, add a new session
    int index = (session_count >= MAX_SESSION_ARRAY_LENGTH) ? MAX_SESSION_ARRAY_LENGTH - 1 : session_count;

    // If the session array is empty, find the correct one
    // Or if the session is not the same as the last one, find the correct one
    if (session_count == 0 || !isInSession(datetime, last_session_index)) {
        // Find the correct session
        // Sometimes the data may have holes or the market may have been closed
        // So we need to find the correct session instead of just using the next one
        for (int i = 0; i < 5; i++) {
            if (isInSession(datetime, i)) {
                last_session_index = i;

                // If the array is full, shift the sessions
                // Because we need to update the last session
                // Else, add a new session
                if (session_count >= MAX_SESSION_ARRAY_LENGTH) {
                    for (int j = 0; j < MAX_SESSION_ARRAY_LENGTH - 1; j++) {
                        sessions[j] = sessions[j + 1];
                    }
                } else {
                    session_count++;
                }

                // Only update time fields, everything will be updated later to avoid code duplication
                strcpy(sessions[index].name, ref_sessions[i].name);
                sessions[index].start = day + ref_sessions[i].start;
                sessions[index].end = day + ref_sessions[i].end;

                // Handle New York AM session (crossing midnight)
                if (i == 3) {
                    if (datetime >= ref_sessions[i].start) {
                        sessions[index].end += ref_sessions[i].end;
                    } else {
                        sessions[index].start -= 86400;
                    }
                }

                break;
            }
        }
    }

    // Update only high and low values
    sessions[index].high = (candle.high > sessions[index].high) ? candle.high : sessions[index].high;
    sessions[index].low = (candle.low < sessions[index].low || sessions[index].low == 0) ? candle.low : sessions[index].low;
}

// Function to check if the datetime is in the session
bool isInSession(time_t datetime, int session_index){
    // Handle the New York AM session (crossing midnight)
    if (session_index == 3){
        return (datetime >= ref_sessions[session_index].start || datetime <= ref_sessions[session_index].end);
    }

    return (datetime >= ref_sessions[session_index].start && datetime <= ref_sessions[session_index].end);
}

// Print the session
void printSession(struct Session session){
    printf("Session name: %s\n", session.name);
    printf("Session start: %s\n", getStringDatetime(session.start));
    printf("Session end: %s\n", getStringDatetime(session.end));
    printf("Session high: %.5f\n", session.high);
    printf("Session low: %.5f\n", session.low);
    printf("\n");
}