# PATTERN: Core Python Patterns (Quick Refresh)

numbers = [1, 2, 3, 4, 5]
squares = [n * n for n in numbers]
print(squares)

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_squares = [n * n for n in numbers if n % 2 == 0]
print(even_squares)

fruits = ["apple", "banana", "cherry"]
fruit_lengths = {fruit: len(fruit) for fruit in fruits}
print(fruit_lengths)

words = ["hello", "world", "hello", "python", "world"]
unique_lengths = {len(word) for word in words}
print(unique_lengths)

# PATTERN: Core Python Patterns (Quick Refresh)

numbers = [1, 2, 3, 4, 5]
square_generator = (n * n for n in numbers)

print(next(square_generator))
print(list(square_generator))

# PATTERN: Core Python Patterns (Quick Refresh)

coordinates = (10, 20, 30)
x, y, z = coordinates
print(f"X: {x}, Y: {y}, Z: {z}")

person_info = ["Alice", 30, "New York"]
name, age, city = person_info
print(f"{name} is {age} years old and lives in {city}.")

# PATTERN: Core Python Patterns (Quick Refresh)

data = [1, 2, 3, 4, 5, 6]
first, second, *rest = data
print(f"First: {first}, Second: {second}, Rest: {rest}")

header, *rows, footer = ["ID", "Name", "Email", "Phone", "End"]
print(f"Header: {header}, Rows: {rows}, Footer: {footer}")

# PATTERN: Core Python Patterns (Quick Refresh)

def greet_person(name, age, city):
    print(f"Hello {name}, you are {age} and live in {city}.")

person_details = {"name": "Bob", "age": 25, "city": "London"}
greet_person(**person_details)

defaults = {"color": "blue", "size": "medium"}
options = {"size": "large", "material": "wood"}
merged_config = {**defaults, **options}
print(merged_config)

# PATTERN: Core Python Patterns (Quick Refresh)

name = "Charlie"
score = 95.6789
percentage = 0.85

print(f"Player: {name}")
print(f"Score: {score:.2f}")
print(f"Progress: {percentage:.1%}")
print(f"Aligned: {name:>10} | {score:<10.1f}")

# PATTERN: Core Python Patterns (Quick Refresh)

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
if (n := len(data)) > 5:
    print(f"List is long, it has {n} elements.")

while (line := input("Enter text (or 'quit'): ")) != 'quit':
    print(f"You entered: {line}")

# PATTERN: Core Python Patterns (Quick Refresh)

age = 20
status = "Adult" if age >= 18 else "Minor"
print(f"Age {age} is {status}.")

temperature = 25
weather = "Hot" if temperature > 30 else "Warm" if temperature > 20 else "Cold"
print(f"Temperature {temperature}°C is {weather}.")

# PATTERN: Core Python Patterns (Quick Refresh)

tasks = ["Buy groceries", "Clean house", "Pay bills"]

print("Tasks for today:")
for index, task in enumerate(tasks, start=1):
    print(f"{index}. {task}")

items = ["apple", "banana", "cherry"]
for i, item in enumerate(items, 101):
    print(f"Item {i}: {item}")

# PATTERN: Core Python Patterns (Quick Refresh)

names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
cities = ["New York", "London", "Paris"]

for name, age, city in zip(names, ages, cities):
    print(f"{name} is {age} years old and lives in {city}.")

products = ["Laptop", "Mouse"]
prices = [1200, 25]
stock = [10, 50]
for product, price, qty in zip(products, prices, stock):
    print(f"{product}: ${price} ({qty} in stock)")

# PATTERN: Core Python Patterns (Quick Refresh)

numbers = [2, 4, 6, 8, 10]
has_odd = any(n % 2 != 0 for n in numbers)
print(f"Are there any odd numbers? {has_odd}")

all_even = all(n % 2 == 0 for n in numbers)
print(f"Are all numbers even? {all_even}")

grades = [85, 92, 78, 60]
passed_all = all(g >= 60 for g in grades)
print(f"Did everyone pass? {passed_all}")

# PATTERN: Core Python Patterns (Quick Refresh)

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

user1 = User("Alice", "alice@example.com")

# Get existing attribute
username = getattr(user1, "name", "Guest")
print(f"Username: {username}")

# Get non-existing attribute with a default
phone = getattr(user1, "phone", "N/A")
print(f"Phone: {phone}")

# Get non-existing attribute without a default (would raise AttributeError)
# address = getattr(user1, "address")