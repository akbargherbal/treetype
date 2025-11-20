# PATTERN: Type Hints (Modern Python)

def calculate_area(length: float, width: float) -> float:
    """Calculates the area of a rectangle."""
    return length * width

area = calculate_area(10.5, 5.0)
# print(f"The area is: {area}")

# PATTERN: Type Hints (Modern Python)

def greet_user(name: str, greeting_message: str | None = None) -> str:
    """Greets a user with an optional custom message."""
    if greeting_message:
        return f"{greeting_message}, {name}!"
    return f"Hello, {name}!"

message1 = greet_user("Alice")
message2 = greet_user("Bob", "Good morning")
# print(message1)
# print(message2)

# PATTERN: Type Hints (Modern Python)

def process_id(user_id: int | str) -> str:
    """Processes a user ID which can be an integer or a string."""
    if isinstance(user_id, int):
        return f"User ID (int): {user_id}"
    return f"User ID (str): {user_id.upper()}"

result1 = process_id(123)
result2 = process_id("abc-456")
# print(result1)
# print(result2)

# PATTERN: Type Hints (Modern Python)

def analyze_data(
    numbers: list[int],
    metadata: dict[str, str],
    tags: set[str]
) -> dict[str, int]:
    """Analyzes a list of numbers, metadata, and tags."""
    total_sum = sum(numbers)
    unique_tags = len(tags)
    return {"total_sum": total_sum, "unique_tags": unique_tags}

data_numbers = [1, 2, 3, 4, 5]
data_metadata = {"source": "sensor", "unit": "celsius"}
data_tags = {"temperature", "sensor", "data"}
analysis_result = analyze_data(data_numbers, data_metadata, data_tags)
# print(analysis_result)

# PATTERN: Type Hints (Modern Python)

from typing import Callable

def apply_operation(data: list[int], operation: Callable[[int], int]) -> list[int]:
    """Applies a given operation to each element in a list."""
    return [operation(item) for item in data]

def double(x: int) -> int:
    return x * 2

numbers = [1, 2, 3]
doubled_numbers = apply_operation(numbers, double)
# print(doubled_numbers)

# PATTERN: Type Hints (Modern Python)

from typing import TypeAlias

# Define a type alias for a complex dictionary structure
SensorReading: TypeAlias = dict[str, float | int]

def process_sensor_data(readings: list[SensorReading]) -> float:
    """Processes a list of sensor readings and returns the average temperature."""
    total_temp = 0.0
    count = 0
    for reading in readings:
        if "temperature" in reading and isinstance(reading["temperature"], (float, int)):
            total_temp += float(reading["temperature"])
            count += 1
    return total_temp / count if count > 0 else 0.0

data = [
    {"timestamp": 1678886400, "temperature": 25.5, "humidity": 60},
    {"timestamp": 1678886460, "temperature": 26, "pressure": 1012.5},
]
avg_temp = process_sensor_data(data)
# print(f"Average temperature: {avg_temp:.2f}")

# PATTERN: Type Hints (Modern Python)

from typing import Protocol

class HasName(Protocol):
    name: str

class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

def get_item_name(item: HasName) -> str:
    """Returns the name of an item that structurally conforms to HasName."""
    return item.name

user_obj = User("Alice", "alice@example.com")
product_obj = Product("Laptop", 1200.0)

user_name = get_item_name(user_obj)
product_name = get_item_name(product_obj)
# print(f"User name: {user_name}")
# print(f"Product name: {product_name}")