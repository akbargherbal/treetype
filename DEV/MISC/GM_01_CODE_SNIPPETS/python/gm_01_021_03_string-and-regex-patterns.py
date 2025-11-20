# PATTERN: String and Regex Patterns

import re

log_line = "ERROR: Failed to connect to database on 2023-10-27."
pattern = r"ERROR: (.*) on (\d{4}-\d{2}-\d{2})"

match = re.search(pattern, log_line)

if match:
    print(f"Error message: {match.group(1)}")
    print(f"Date: {match.group(2)}")
else:
    print("No error found.")

# PATTERN: String and Regex Patterns

import re

document_text = "The product codes are P101, P205, and P310. Also, check P007."
product_code_pattern = r"P\d{3}"

all_codes = re.findall(product_code_pattern, document_text)

print(f"Found product codes: {all_codes}")

# Example with capturing groups
data = "User: Alice, ID: 123; User: Bob, ID: 456"
user_ids = re.findall(r"User: (\w+), ID: (\d+)", data)
print(f"User IDs: {user_ids}")

# PATTERN: String and Regex Patterns

import re

raw_text = "  This is a sentence.  It has extra   spaces.  "
# Replace multiple spaces with a single space and strip leading/trailing spaces
cleaned_text = re.sub(r"\s+", " ", raw_text).strip()

print(f"Original: '{raw_text}'")
print(f"Cleaned:  '{cleaned_text}'")

# Replace specific words
message = "Please contact support@example.com for assistance."
anonymized_message = re.sub(r"support@example.com", "admin@company.org", message)
print(f"Anonymized: {anonymized_message}")

# PATTERN: String and Regex Patterns

import re

# Compile the regex pattern once for efficiency
email_pattern = re.compile(r"[\w\.-]+@[\w\.-]+")

text_data_1 = "Contact us at info@example.com or sales@domain.org."
text_data_2 = "No email addresses found in this text."
text_data_3 = "Support: help@service.net"

emails_1 = email_pattern.findall(text_data_1)
emails_2 = email_pattern.findall(text_data_2)
emails_3 = email_pattern.findall(text_data_3)

print(f"Emails in text 1: {emails_1}")
print(f"Emails in text 2: {emails_2}")
print(f"Emails in text 3: {emails_3}")

# PATTERN: String and Regex Patterns

import re

log_entry = "2023-10-27 14:35:01 INFO User 'alice' logged in from 192.168.1.100"
# Define a pattern with capturing groups for date, time, username, and IP
pattern = r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) INFO User '(\w+)' logged in from ([\d.]+)"

match = re.search(pattern, log_entry)

if match:
    # Access groups by index
    date = match.group(1)
    time = match.group(2)
    username = match.group(3)
    ip_address = match.group(4)

    print(f"Date: {date}")
    print(f"Time: {time}")
    print(f"Username: {username}")
    print(f"IP Address: {ip_address}")

    # Or unpack all groups at once
    # date, time, username, ip_address = match.groups()
else:
    print("No match found.")