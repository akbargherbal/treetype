# PATTERN: Common Automation Patterns

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"File created: {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            print(f"File modified: {event.src_path}")

# Create a dummy directory for watching
watch_directory = "temp_watch_dir"
os.makedirs(watch_directory, exist_ok=True)

event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, watch_directory, recursive=True)
observer.start()

try:
    print(f"Watching directory: {watch_directory}. Create/modify files to see events.")
    time.sleep(5) # Watch for 5 seconds
finally:
    observer.stop()
    observer.join()
    os.rmdir(watch_directory) # Clean up

# PATTERN: Common Automation Patterns

import schedule
import time

def daily_report_job():
    """A task to generate a daily report."""
    print(f"Running daily report job at {time.ctime()}")

def hourly_backup_job():
    """A task to perform an hourly backup."""
    print(f"Running hourly backup job at {time.ctime()}")

# Schedule jobs
schedule.every(10).seconds.do(daily_report_job)
schedule.every(5).seconds.do(hourly_backup_job)

print("Scheduler started. Jobs will run every few seconds. Press Ctrl+C to stop.")
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("Scheduler stopped.")

# PATTERN: Common Automation Patterns

import smtplib, ssl
from email.mime.text import MIMEText

sender_email = "your_email@example.com" # Replace with your email
receiver_email = "recipient@example.com" # Replace with recipient email
password = "your_app_password" # Replace with your email's app password

message = MIMEText("This is a test email sent from Python automation.")
message["Subject"] = "Python Automation Test Email"
message["From"] = sender_email
message["To"] = receiver_email

# Use Gmail's SMTP server as an example
smtp_server = "smtp.gmail.com"
port = 465  # For SSL

# Create a secure SSL context
context = ssl.create_default_context()

try:
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.send_message(message)
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")

# PATTERN: Common Automation Patterns

import subprocess

try:
    # Run a simple command and capture its output
    result = subprocess.run(
        ["echo", "Hello from subprocess!"],
        capture_output=True,
        text=True, # Decode stdout/stderr as text
        check=True # Raise CalledProcessError for non-zero exit codes
    )

    print(f"Command executed successfully. Exit Code: {result.returncode}")
    print(f"Stdout: {result.stdout.strip()}")
    print(f"Stderr: {result.stderr.strip()}")

    # Example of a command that might fail (uncomment to test)
    # subprocess.run(["non_existent_command"], check=True)

except subprocess.CalledProcessError as e:
    print(f"Command failed with exit code {e.returncode}")
    print(f"Stderr: {e.stderr.strip()}")
except FileNotFoundError:
    print("Error: Command not found. Ensure 'echo' is in your system's PATH.")

# PATTERN: Common Automation Patterns

import zipfile
import os

# Create some dummy files to be zipped
file1_name = "report_data.txt"
file2_name = "logs.log"
with open(file1_name, "w") as f:
    f.write("This is some important report data.\nLine 2 of report.")
with open(file2_name, "w") as f:
    f.write("Application log entry 1.\nApplication log entry 2.")

zip_filename = "archive.zip"

try:
    # Create a new zip file
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file1_name)
        zipf.write(file2_name, arcname="nested_logs/logs.log") # Add with a different path inside zip
    print(f"Successfully created '{zip_filename}' containing '{file1_name}' and 'nested_logs/logs.log'.")

except Exception as e:
    print(f"Error creating zip file: {e}")
finally:
    # Clean up dummy files
    os.remove(file1_name)
    os.remove(file2_name)
    # Optionally remove the zip file for repeated runs
    # os.remove(zip_filename)

# PATTERN: Common Automation Patterns

import os

# Default configuration settings
default_config = {
    "DATABASE_URL": "sqlite:///dev.db",
    "API_KEY": "default_dev_key",
    "LOG_LEVEL": "INFO"
}

# Load configuration, overriding defaults with environment variables
app_config = default_config.copy()

app_config["DATABASE_URL"] = os.getenv("APP_DATABASE_URL", app_config["DATABASE_URL"])
app_config["API_KEY"] = os.getenv("APP_API_KEY", app_config["API_KEY"])
app_config["LOG_LEVEL"] = os.getenv("APP_LOG_LEVEL", app_config["LOG_LEVEL"])

print("--- Application Configuration ---")
for key, value in app_config.items():
    print(f"{key}: {value}")
print("---------------------------------")

# To test:
# Set environment variables before running, e.g.:
# export APP_DATABASE_URL="postgresql://user:pass@prod_db:5432/app_prod"
# export APP_LOG_LEVEL="DEBUG"
# python your_script.py