# PATTERN: Date and Time Patterns

from datetime import datetime, date

# Get current local datetime
current_local_datetime = datetime.now()
print(f"Local datetime: {current_local_datetime}")

# Get current UTC datetime
current_utc_datetime = datetime.utcnow()
print(f"UTC datetime: {current_utc_datetime}")

# Get current local date
current_date = date.today()
print(f"Current date: {current_date}")

# PATTERN: Date and Time Patterns

from datetime import datetime

# Create a datetime object
current_time = datetime.now()

# Format datetime into a string (YYYY-MM-DD HH:MM:SS)
formatted_datetime = current_time.strftime("%Y-%m-%d %H:%M:%S")
print(f"Formatted datetime: {formatted_datetime}")

# Format datetime into a date-only string (Month Day, Year)
formatted_date = current_time.strftime("%B %d, %Y")
print(f"Formatted date: {formatted_date}")

# Format with weekday and time (Mon, 15:30)
formatted_short = current_time.strftime("%a, %H:%M")
print(f"Short format: {formatted_short}")

# PATTERN: Date and Time Patterns

from datetime import datetime

# Date string to parse
date_string_full = "2023-10-27 14:30:00"
date_string_short = "Oct 27, 2023"

# Format string matching the date_string_full
format_full = "%Y-%m-%d %H:%M:%S"
parsed_datetime_full = datetime.strptime(date_string_full, format_full)
print(f"Parsed full datetime: {parsed_datetime_full}")

# Format string matching the date_string_short
format_short = "%b %d, %Y"
parsed_datetime_short = datetime.strptime(date_string_short, format_short)
print(f"Parsed short datetime: {parsed_datetime_short}")

# PATTERN: Date and Time Patterns

from datetime import datetime, timedelta

# Get current datetime
now = datetime.now()
print(f"Current datetime: {now}")

# Define time differences
one_day = timedelta(days=1)
three_hours = timedelta(hours=3)
thirty_minutes = timedelta(minutes=30)

# Add a day
tomorrow = now + one_day
print(f"Tomorrow: {tomorrow}")

# Subtract three hours and thirty minutes
past_time = now - three_hours - thirty_minutes
print(f"Past time: {past_time}")

# Calculate difference between two datetimes
future_date = now + timedelta(weeks=2)
difference = future_date - now
print(f"Difference: {difference}")

# PATTERN: Date and Time Patterns

from datetime import datetime
import pytz # External dependency for timezone handling

# Get current UTC aware datetime
utc_now = datetime.now(pytz.utc)
print(f"UTC aware datetime: {utc_now}")

# Define a specific timezone
eastern_tz = pytz.timezone('America/New_York')

# Convert UTC datetime to Eastern Time
eastern_now = utc_now.astimezone(eastern_tz)
print(f"Eastern Time aware datetime: {eastern_now}")

# Create a naive datetime and make it aware
naive_dt = datetime(2023, 10, 27, 10, 0, 0)
aware_dt_eastern = eastern_tz.localize(naive_dt)
print(f"Localized Eastern Time: {aware_dt_eastern}")