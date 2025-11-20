# PATTERN: Error Handling Patterns

def safe_divide(numerator, denominator):
    try:
        result = numerator / denominator
    except ZeroDivisionError:
        print("Error: Cannot divide by zero!")
        return None
    except TypeError:
        print("Error: Inputs must be numbers.")
        return None
    else:
        print(f"Division successful. Result: {result}")
        return result
    finally:
        print("Division attempt concluded.")

safe_divide(10, 2)
safe_divide(10, 0)
safe_divide(10, "a")

# PATTERN: Error Handling Patterns

def process_user_input(value_str):
    try:
        number = int(value_str)
        if number < 0:
            raise ValueError("Number must be non-negative.")
        result = 100 / number
    except ValueError as e:
        print(f"Input validation error: {e}")
    except ZeroDivisionError:
        print("Calculation error: Cannot divide by zero.")
    except Exception as e: # Catch any other unexpected errors
        print(f"An unexpected error occurred: {e}")
    else:
        print(f"Processing successful. Result: {result}")

process_user_input("20")
process_user_input("abc")
process_user_input("-5")
process_user_input("0")

# PATTERN: Error Handling Patterns

class InvalidConfigurationError(Exception):
    """Custom exception for issues with application configuration."""
    def __init__(self, message="Invalid configuration detected", config_key=None):
        super().__init__(message)
        self.config_key = config_key

def load_application_config(settings):
    if not isinstance(settings, dict):
        raise InvalidConfigurationError("Configuration must be a dictionary.")
    if "api_key" not in settings or not settings["api_key"]:
        raise InvalidConfigurationError("API key is missing or empty.", config_key="api_key")
    print("Configuration loaded successfully.")

try:
    load_application_config({"timeout": 30})
except InvalidConfigurationError as e:
    print(f"Caught custom error: {e}")
    if e.config_key:
        print(f"Problematic key: {e.config_key}")

try:
    load_application_config({"api_key": "some_secret_key"})
except InvalidConfigurationError as e:
    print(f"Caught custom error: {e}")

# PATTERN: Error Handling Patterns

import os

def read_data_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError as e:
        # Chain the original exception to provide more context
        raise IOError(f"Failed to access data file: {filename}") from e
    except PermissionError as e:
        raise IOError(f"Permission denied for file: {filename}") from e

try:
    # Attempt to read a non-existent file
    read_data_file("non_existent_data.txt")
except IOError as e:
    print(f"Caught chained error: {e}")
    if e.__cause__:
        print(f"Original cause: {type(e.__cause__).__name__}: {e.__cause__}")

# PATTERN: Error Handling Patterns

def process_order(item_count, unit_price):
    # Ensure item_count is positive
    assert item_count > 0, "Item count must be positive."
    # Ensure unit_price is non-negative
    assert unit_price >= 0, "Unit price cannot be negative."

    total_cost = item_count * unit_price
    print(f"Order processed: {item_count} items at ${unit_price} each. Total: ${total_cost}")
    return total_cost

# This call will pass
process_order(5, 10.50)

# The following calls would raise an AssertionError if uncommented:
# process_order(0, 10.50)
# process_order(5, -2.00)