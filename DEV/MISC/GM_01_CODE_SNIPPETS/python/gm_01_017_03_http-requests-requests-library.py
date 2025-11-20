# PATTERN: HTTP Requests (requests library)

import requests

try:
    response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
    response.raise_for_status() # Raise an exception for HTTP errors
    print(f"Status Code: {response.status_code}")
    print(f"Todo Title: {response.json()['title']}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")

# PATTERN: HTTP Requests (requests library)

import requests

post_data = {"title": "foo", "body": "bar", "userId": 1}
try:
    response = requests.post("https://jsonplaceholder.typicode.com/posts", json=post_data)
    response.raise_for_status()
    print(f"Status Code: {response.status_code}")
    print(f"Response JSON: {response.json()}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")

# PATTERN: HTTP Requests (requests library)

import requests

with requests.Session() as session:
    # Set a cookie
    session.get("https://httpbin.org/cookies/set/sessioncookie/12345")
    # Get cookies, should include the one set above
    response = session.get("https://httpbin.org/cookies")
    response.raise_for_status()
    print(f"Session Cookies: {response.json()['cookies']}")

# PATTERN: HTTP Requests (requests library)

import requests

headers = {"User-Agent": "MyCustomApp/1.0", "Accept": "application/json"}
params = {"name": "Alice", "city": "New York"}

try:
    response = requests.get("https://httpbin.org/get", headers=headers, params=params)
    response.raise_for_status()
    print(f"Status Code: {response.status_code}")
    print(f"Received Headers: {response.json()['headers']['User-Agent']}")
    print(f"Received Params: {response.json()['args']}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")

# PATTERN: HTTP Requests (requests library)

import requests

url_to_check = "https://jsonplaceholder.typicode.com/nonexistent" # This URL will return 404

try:
    response = requests.get(url_to_check)
    response.raise_for_status() # This will raise an HTTPError for 4xx/5xx responses
    print(f"Request successful: {response.status_code}")
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error occurred: {e}")
    print(f"Status Code: {e.response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"An unexpected error occurred: {e}")

# PATTERN: HTTP Requests (requests library)

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Timeout example
try:
    response = requests.get("https://httpbin.org/delay/5", timeout=2)
    print(f"Timeout successful: {response.status_code}")
except requests.exceptions.Timeout:
    print("Request timed out after 2 seconds.")

# Retry example
session = requests.Session()
retries = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502])
session.mount('https://', HTTPAdapter(max_retries=retries))
try:
    response = session.get("https://httpbin.org/status/500")
    response.raise_for_status()
    print(f"Retry successful: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Retry failed after attempts: {e}")