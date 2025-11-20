# PATTERN: Decorators (Level Up)

def log_execution(func):
    def wrapper(*args, **kwargs):
        print(f"Executing {func.__name__}...")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}.")
        return result
    return wrapper

@log_execution
def calculate_sum(a, b):
    return a + b

# calculate_sum(5, 3)

# PATTERN: Decorators (Level Up)

def repeat_n_times(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat_n_times(n=3)
def say_hello(name):
    print(f"Hello, {name}!")

# say_hello("Alice")

# PATTERN: Decorators (Level Up)

def validate_input(func):
    def wrapper(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Input must be a number.")
        return func(self, value)
    return wrapper

class DataProcessor:
    def __init__(self, initial_value=0):
        self._data = initial_value

    @validate_input
    def set_data(self, value):
        self._data = value
        print(f"Data set to {value}")

# processor = DataProcessor()
# processor.set_data(100)

# PATTERN: Decorators (Level Up)

class Product:
    def __init__(self, base_price):
        self._base_price = base_price

    @property
    def price(self):
        # Calculate price with a small markup
        return self._base_price * 1.1

# item = Product(100)
# print(item.price)

# PATTERN: Decorators (Level Up)

class Product:
    def __init__(self, initial_price):
        self._price = initial_price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        if new_price < 0:
            raise ValueError("Price cannot be negative.")
        self._price = new_price

# item = Product(100)
# item.price = 120
# print(item.price)

# PATTERN: Decorators (Level Up)

class MathUtils:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def multiply(a, b):
        return a * b

# result_add = MathUtils.add(5, 3)
# result_multiply = MathUtils.multiply(5, 3)

# PATTERN: Decorators (Level Up)

class Logger:
    _instance_count = 0

    def __init__(self):
        Logger._instance_count += 1

    @classmethod
    def get_instance_count(cls):
        return cls._instance_count

    @classmethod
    def create_default_logger(cls):
        # A factory method using class context
        return cls()

# logger1 = Logger.create_default_logger()
# logger2 = Logger()
# print(Logger.get_instance_count())

# PATTERN: Decorators (Level Up)

import functools

def debug_info(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        return func(*args, **kwargs)
    return wrapper

@debug_info
def greet(name, greeting="Hello"):
    """Greets a person."""
    return f"{greeting}, {name}!"

# print(greet.__name__)
# print(greet.__doc__)

# PATTERN: Decorators (Level Up)

def uppercase_result(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper

def add_exclamation(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) + "!"
    return wrapper

@add_exclamation
@uppercase_result
def get_message(text):
    return text

# print(get_message("hello world"))

# PATTERN: Decorators (Level Up)

def create_logger_decorator(log_level="INFO"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"[{log_level}] Executing {func.__name__}...")
            result = func(*args, **kwargs)
            print(f"[{log_level}] Finished {func.__name__}.")
            return result
        return wrapper
    return decorator

@create_logger_decorator(log_level="DEBUG")
def process_data(data):
    return data * 2

# process_data(10)

# PATTERN: Decorators (Level Up)

def add_timestamp_attribute(cls):
    import datetime
    setattr(cls, 'creation_timestamp', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return cls

@add_timestamp_attribute
class Report:
    def __init__(self, title):
        self.title = title

    def display(self):
        print(f"Report: {self.title} (Created: {self.creation_timestamp})")

# my_report = Report("Monthly Sales")
# my_report.display()