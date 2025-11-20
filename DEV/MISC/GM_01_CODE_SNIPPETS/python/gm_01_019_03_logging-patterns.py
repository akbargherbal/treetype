# PATTERN: Logging Patterns

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Application started successfully.")
logging.warning("Configuration file not found, using default settings.")
logging.debug("This message will not be shown with INFO level.")

# PATTERN: Logging Patterns

import logging

# Get a specific logger instance
app_logger = logging.getLogger('my_application')
app_logger.setLevel(logging.DEBUG)

# Create a console handler and set level to debug
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

# Add formatter to console handler
console_handler.setFormatter(formatter)

# Add console handler to logger
app_logger.addHandler(console_handler)

app_logger.info("User 'admin' logged in.")
app_logger.debug("Database connection established.")

# PATTERN: Logging Patterns

import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

logging.debug("This is a debug message, useful for detailed diagnostics.")
logging.info("This is an informational message, indicating normal operation.")
logging.warning("This is a warning message, indicating a potential issue.")
logging.error("This is an error message, indicating a serious problem.")
logging.critical("This is a critical message, indicating a severe error.")

# PATTERN: Logging Patterns

import logging

# Get a logger instance
file_logger = logging.getLogger('file_processor')
file_logger.setLevel(logging.INFO)

# Create a file handler
file_handler = logging.FileHandler('application.log')
file_handler.setLevel(logging.INFO)

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
file_logger.addHandler(file_handler)

file_logger.info("Data processing started for batch_001.")
file_logger.warning("Skipped 3 invalid records in batch_001.")

# PATTERN: Logging Patterns

import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
app_logger = logging.getLogger('exception_handler')

def divide_numbers(a, b):
    try:
        result = a / b
        app_logger.info(f"Division successful: {a} / {b} = {result}")
        return result
    except ZeroDivisionError:
        app_logger.exception("Attempted to divide by zero!")
    except TypeError:
        app_logger.exception("Invalid operand type for division!")

divide_numbers(10, 2)
divide_numbers(10, 0)
divide_numbers(10, "a")