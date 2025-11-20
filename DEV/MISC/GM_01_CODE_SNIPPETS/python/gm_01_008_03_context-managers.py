# PATTERN: Context Managers

file_path = "report.txt"

# Write to a file
with open(file_path, "w") as output_file:
    output_file.write("Sales Report 2023\n")
    output_file.write("Total Revenue: $1,234,567\n")
    output_file.write("Total Expenses: $876,543")

# Read from the file
with open(file_path, "r") as input_file:
    content = input_file.read()
    print(content)

import os
os.remove(file_path) # Clean up

# PATTERN: Context Managers

import contextlib
import time

@contextlib.contextmanager
def timer_context(operation_name):
    start_time = time.time()
    print(f"Starting '{operation_name}'...")
    try:
        yield
    finally:
        end_time = time.time()
        duration = end_time - start_time
        print(f"Finished '{operation_name}'. Duration: {duration:.4f} seconds.")

with timer_context("data_processing"):
    time.sleep(0.15) # Simulate some work
    print("Processing data...")
    time.sleep(0.05)

# PATTERN: Context Managers

source_file = "input_data.txt"
destination_file = "processed_data.txt"
log_file = "processing_log.txt"

with open(source_file, "w") as f:
    f.write("Line 1\nLine 2\nLine 3")

with open(source_file, "r") as src, \
     open(destination_file, "w") as dest, \
     open(log_file, "a") as log:
    for line_num, line in enumerate(src, 1):
        processed_line = line.strip().upper() + " (PROCESSED)\n"
        dest.write(processed_line)
        log.write(f"Processed line {line_num}: {line.strip()}\n")
    print("Files processed and logged.")

import os
os.remove(source_file)
os.remove(destination_file)
os.remove(log_file)

# PATTERN: Context Managers

import contextlib
import os

file_to_remove = "temp_report.txt"

print("Attempting to remove a file that might not exist...")
with contextlib.suppress(FileNotFoundError):
    os.remove(file_to_remove)
    print(f"Successfully removed '{file_to_remove}' (if it existed).")

print("\nAttempting a division by zero, suppressing the error...")
with contextlib.suppress(ZeroDivisionError):
    result = 10 / 0
    print(f"Result of division: {result}") # This line won't be reached

print("\nProgram continues after suppressed operations.")