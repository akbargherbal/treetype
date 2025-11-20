# PATTERN: API Design Patterns

import time

class RateLimiter:
    def __init__(self, calls_per_second):
        self.min_interval = 1.0 / calls_per_second
        self.last_call_time = 0

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            elapsed = time.time() - self.last_call_time
            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)
            self.last_call_time = time.time()
            return func(*args, **kwargs)
        return wrapper

# PATTERN: API Design Patterns

import time
import random
import functools

def retry_with_backoff(retries=3, initial_delay=1, backoff_factor=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for i in range(retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if i == retries:
                        raise
                    time.sleep(delay + random.uniform(0, 0.1 * delay))
                    delay *= backoff_factor
        return wrapper
    return decorator

# PATTERN: API Design Patterns

class ApiResponse:
    def __init__(self, success: bool, message: str = "", data: dict = None, status_code: int = 200):
        self.success = success
        self.message = message
        self.data = data if data is not None else {}
        self.status_code = status_code

    def to_dict(self):
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "status_code": self.status_code
        }

# PATTERN: API Design Patterns

def fetch_all_paginated_data(api_fetch_function, initial_params=None):
    all_items = []
    current_params = initial_params if initial_params is not None else {}
    next_page_token = None

    while True:
        response = api_fetch_function(next_page_token=next_page_token, **current_params)
        all_items.extend(response.get("items", []))
        next_page_token = response.get("next_page_token")
        if not next_page_token:
            break
    return all_items