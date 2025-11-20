# PATTERN: File and Path Operations

from pathlib import Path

# Create a Path object
file_path = Path("documents/report.txt")
print(f"File path: {file_path}")

# Get parent directory
print(f"Parent directory: {file_path.parent}")

# Get file name and suffix
print(f"File name: {file_path.name}")
print(f"File suffix: {file_path.suffix}")

# Join paths
data_dir = Path("data")
full_path = data_dir / "config.json"
print(f"Joined path: {full_path}")

# PATTERN: File and Path Operations

from pathlib import Path
import os

# Create a dummy file for demonstration
dummy_file = Path("temp_data.txt")
dummy_file.write_text("Hello, world!")

# Check if path exists
print(f"'{dummy_file}' exists: {dummy_file.exists()}")
print(f"'{dummy_file}' is a file: {dummy_file.is_file()}")

# Check for a non-existent file
non_existent = Path("no_such_file.log")
print(f"'{non_existent}' exists: {non_existent.exists()}")

# Check for a directory
current_dir = Path(".")
print(f"'{current_dir}' is a directory: {current_dir.is_dir()}")

# Clean up
os.remove(dummy_file)

# PATTERN: File and Path Operations

from pathlib import Path
import shutil

# Define a nested directory path
new_dir_path = Path("project_files/logs/daily")

# Create the directory, including any necessary parent directories
# exist_ok=True prevents an error if the directory already exists
new_dir_path.mkdir(parents=True, exist_ok=True)
print(f"Directory created: {new_dir_path.exists()}")

# Clean up the top-level directory created
shutil.rmtree(new_dir_path.parent.parent)
print(f"Directory cleaned up: {new_dir_path.parent.parent.exists()}")

# PATTERN: File and Path Operations

from pathlib import Path
import os

# Create a temporary directory and some dummy files
temp_dir = Path("temp_reports")
temp_dir.mkdir(exist_ok=True)
(temp_dir / "report_2023.txt").write_text("...")
(temp_dir / "data_2024.csv").write_text("...")
(temp_dir / "summary.txt").write_text("...")
(temp_dir / "image.png").write_text("...")

# Find all .txt files
print("TXT files:")
for file_path in temp_dir.glob("*.txt"):
    print(f"- {file_path.name}")

# Find all files starting with 'data'
print("\nFiles starting with 'data':")
for file_path in temp_dir.glob("data*"):
    print(f"- {file_path.name}")

# Find all files in the directory
print("\nAll files:")
for file_path in temp_dir.glob("*"):
    print(f"- {file_path.name}")

# Clean up
for file_path in temp_dir.glob("*"):
    os.remove(file_path)
os.rmdir(temp_dir)

# PATTERN: File and Path Operations

from pathlib import Path
import os

# Define a file path
config_file = Path("app_config.ini")

# Write text to the file
content_to_write = "[Settings]\nversion=1.0\nauthor=Pythonista"
config_file.write_text(content_to_write)
print(f"Content written to '{config_file.name}'.")

# Read text from the file
read_content = config_file.read_text()
print(f"\nContent read from '{config_file.name}':")
print(read_content)

# Clean up
os.remove(config_file)

# PATTERN: File and Path Operations

import shutil
from pathlib import Path
import os

# Create a dummy file
source_file = Path("original_document.txt")
source_file.write_text("This is the original content.")

# Define destination paths
copy_destination = Path("backup_document.txt")
move_destination = Path("archive/final_document.txt")
move_destination.parent.mkdir(exist_ok=True)

# Copy the file
shutil.copy(source_file, copy_destination)
print(f"Copied '{source_file.name}' to '{copy_destination.name}'.")

# Move the copied file
shutil.move(copy_destination, move_destination)
print(f"Moved '{copy_destination.name}' to '{move_destination}'.")

# Clean up
os.remove(source_file)
os.remove(move_destination)
os.rmdir(move_destination.parent)

# PATTERN: File and Path Operations

import json
from pathlib import Path
import os

# Data to be stored in JSON
data = {
    "name": "Alice",
    "age": 30,
    "isStudent": False,
    "courses": ["Math", "Science"]
}

# Define the JSON file path
json_file = Path("user_profile.json")

# Write data to JSON file
with open(json_file, 'w') as f:
    json.dump(data, f, indent=4)
print(f"Data dumped to '{json_file.name}'.")

# Read data from JSON file
with open(json_file, 'r') as f:
    loaded_data = json.load(f)
print(f"\nData loaded from '{json_file.name}':")
print(loaded_data)
print(f"Loaded name: {loaded_data['name']}")

# Clean up
os.remove(json_file)