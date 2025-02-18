#ifndef SYSTEM_OPERATOR_H
#define SYSTEM_OPERATOR_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <errno.h>

int create_directory(const char *path);
int create_full_path(const char *filepath);

#endif // SYSTEM_OPERATOR_H
