# PATTERN: Environment and Config

import os

# In a real scenario, environment variables would be set externally
# For demonstration, we can simulate setting one:
# os.environ['APP_SECRET_KEY'] = 'super_secret_value_123'

# Access an environment variable, providing a default if not set
secret_key = os.environ.get('APP_SECRET_KEY', 'default_fallback_key')
db_connection_string = os.environ.get('DATABASE_URL') # Will be None if not set

print(f"Application Secret Key: {secret_key}")
print(f"Database Connection String: {db_connection_string}")

if db_connection_string is None:
    print("DATABASE_URL environment variable is not set.")

# PATTERN: Environment and Config

import os
from dotenv import load_dotenv

# Assume a .env file exists in the same directory with content like:
# API_KEY="your_api_key_from_env"
# SERVICE_URL="https://api.example.com"

load_dotenv() # Load environment variables from .env file

api_key = os.environ.get("API_KEY")
service_url = os.environ.get("SERVICE_URL", "http://localhost:8000")

print(f"Loaded API Key: {api_key}")
print(f"Loaded Service URL: {service_url}")

if api_key is None:
    print("API_KEY was not found in .env or environment.")

# PATTERN: Environment and Config

import configparser
import io

# Simulate a config.ini file content for demonstration
config_content = """
[server]
host = 127.0.0.1
port = 8080
debug = True

[database]
type = sqlite
path = /var/data/app.db
"""

config = configparser.ConfigParser()
config.read_string(config_content) # Read configuration from a string

server_host = config['server']['host']
server_port = config.getint('server', 'port') # Get as integer
db_path = config.get('database', 'path')

print(f"Server Host: {server_host}")
print(f"Server Port: {server_port}")
print(f"Database Path: {db_path}")

if config.getboolean('server', 'debug'):
    print("Debug mode is enabled.")