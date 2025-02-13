# Name of the final executable
TARGET = ClusterX

# Directories
SRC_DIR = src
OBJ_DIR = obj
INCLUDE_DIR = include

# Source files - Get ClusterX.c (main script) and all .c files in the src directory and its subdirectories
SRC_FILES = ClusterX.c $(wildcard $(SRC_DIR)/**/*.c)
OBJ_FILES = $(SRC_FILES:$(SRC_DIR)/%.c=$(OBJ_DIR)/%.o)

# Compiler and flags
CC = gcc
CFLAGS = -Wall -g -I$(INCLUDE_DIR)

# Main rule: compile the executable
$(TARGET): $(OBJ_FILES)
	@$(CC) -o $(TARGET) $(OBJ_FILES)

# Rule for object files: Create object files in obj/ directory corresponding to src/ directory structure
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(OBJ_DIR)/$(dir $*)
	@$(CC) $(CFLAGS) -c $< -o $@

# Clean: remove object files and executable
clean:
	@rm -rf $(OBJ_DIR) $(TARGET)

# Rebuild: clean and recompile
rebuild: clean $(TARGET)

.PHONY: clean rebuild
