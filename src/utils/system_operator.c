#include "system_operator.h"

int create_directory(const char *path) {
    // Create the directory with full permissions
    if (mkdir(path, 0777) == -1) {
        if (errno != EEXIST) {
            perror("Error creating directory: ");

            return -1;
        }
    }

    return 0;
}

int create_full_path(const char *filepath) {
    char path[256];
    strcpy(path, filepath);

    // Traverse the path and create directories
    for (int i = 1; path[i] != '\0'; i++) {
        if (path[i] == '/') {
            path[i] = '\0';
            if (create_directory(path) == -1) {
                return -1;
            }
            path[i] = '/';
        }
    }

    // Create the last directory
    if (create_directory(path) == -1) {
        return -1;
    }

    return 0;
}