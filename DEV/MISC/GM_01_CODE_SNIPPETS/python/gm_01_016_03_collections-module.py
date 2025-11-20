# PATTERN: Collections Module

from collections import Counter

# Count occurrences of items in a list
fruits = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple', 'grape']
fruit_counts = Counter(fruits)

print(f"Total fruit counts: {fruit_counts}")
print(f"Count of 'apple': {fruit_counts['apple']}")
print(f"Two most common fruits: {fruit_counts.most_common(2)}")

# PATTERN: Collections Module

from collections import defaultdict

# Grouping items by a key
student_grades = [
    ('Alice', 'A'), ('Bob', 'B'), ('Alice', 'B'),
    ('Charlie', 'A'), ('Bob', 'A')
]

grades_by_student = defaultdict(list)
for student, grade in student_grades:
    grades_by_student[student].append(grade)

print(f"Grades by student: {grades_by_student}")
print(f"Alice's grades: {grades_by_student['Alice']}")
print(f"David's grades (default empty list): {grades_by_student['David']}")

# PATTERN: Collections Module

from collections import OrderedDict

# Create an OrderedDict to preserve insertion order
product_prices = OrderedDict()
product_prices['Laptop'] = 1200
product_prices['Mouse'] = 25
product_prices['Keyboard'] = 75
product_prices['Monitor'] = 300

print("Products and prices in insertion order:")
for product, price in product_prices.items():
    print(f"{product}: ${price}")

# Demonstrate moving an item to the end
product_prices.move_to_end('Laptop')
print("\nAfter moving 'Laptop' to end:")
for product, price in product_prices.items():
    print(f"{product}: ${price}")

# PATTERN: Collections Module

from collections import deque

# Create a deque
recent_activities = deque(['login', 'view_product', 'add_to_cart'])

print(f"Initial activities: {list(recent_activities)}")

# Add new activity to the right (end)
recent_activities.append('checkout')
print(f"After append: {list(recent_activities)}")

# Add new activity to the left (beginning)
recent_activities.appendleft('page_load')
print(f"After appendleft: {list(recent_activities)}")

# Remove from the right (end)
last_activity = recent_activities.pop()
print(f"Popped '{last_activity}'. Current: {list(recent_activities)}")

# Remove from the left (beginning)
first_activity = recent_activities.popleft()
print(f"Poppedleft '{first_activity}'. Current: {list(recent_activities)}")

# PATTERN: Collections Module

from collections import ChainMap

# Define multiple dictionaries
default_settings = {'theme': 'dark', 'font_size': 14, 'notifications': True}
user_settings = {'font_size': 16, 'notifications': False}
session_settings = {'theme': 'light'}

# Create a ChainMap
# Lookup order: session_settings -> user_settings -> default_settings
combined_settings = ChainMap(session_settings, user_settings, default_settings)

print(f"Combined settings: {combined_settings}")
print(f"Theme: {combined_settings['theme']}")
print(f"Font size: {combined_settings['font_size']}")
print(f"Notifications: {combined_settings['notifications']}")
print(f"All maps: {combined_settings.maps}")