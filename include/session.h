#ifndef SESSION_H
#define SESSION_H

#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

// Reference session structure
// For Asian, London, New York (AM and PM)
struct RefSession{
    char name[11];
    time_t start;
    time_t end;
};

// Reference sessions
// In Sydney time
#define ASION_SESSION {"Asian", 32400, 66600} // 9:00 - 18:30
#define LONDON_SESSION {"London", 66600, 82800} // 18:30 - 23:00
#define NEWYORK_AM_SESSION {"New York AM", 82800, 12600} // 23:00 - 3:30
#define NEWYORK_PM_SESSION {"New York PM", 12600, 32400} // 3:30 - 9:00

// Session structure
struct Session{
    char name[12];
    time_t start;
    float high;
    float low;
    time_t end;
};

struct Session* initSessions(int limit);

bool isInSession(time_t datetime, int index);
bool isInThisSession(time_t datetime, struct Session session);

void getSessions(struct Session *sessions, struct Candle candle, int last_index);
void printSession(struct Session session);

#endif