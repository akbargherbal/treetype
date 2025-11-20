# PATTERN: Itertools Patterns

import itertools

list_of_lists = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
flattened_sequence = list(itertools.chain.from_iterable(list_of_lists))

# print(flattened_sequence)
# Expected output: [1, 2, 3, 4, 5, 6, 7, 8, 9]

# PATTERN: Itertools Patterns

import itertools

sales_data = [
    {'product': 'Laptop', 'region': 'East', 'sales': 120},
    {'product': 'Mouse', 'region': 'West', 'sales': 50},
    {'product': 'Laptop', 'region': 'East', 'sales': 150},
    {'product': 'Keyboard', 'region': 'West', 'sales': 70},
    {'product': 'Mouse', 'region': 'East', 'sales': 60},
]

# Data must be sorted by the key for groupby to work correctly
sales_data.sort(key=lambda x: x['region'])

sales_by_region = {}
for region, items_iter in itertools.groupby(sales_data, key=lambda x: x['region']):
    total_sales = sum(item['sales'] for item in items_iter)
    sales_by_region[region] = total_sales

# print(sales_by_region)
# Expected output: {'East': 330, 'West': 120}

# PATTERN: Itertools Patterns

import itertools

# Simulate a large or infinite iterator
def generate_sensor_readings():
    reading_id = 0
    while True:
        yield f"Reading-{reading_id}"
        reading_id += 1

sensor_readings_iterator = generate_sensor_readings()

# Get 5 readings starting from the 10th reading (index 9)
# islice(iterable, start, stop)
selected_readings = list(itertools.islice(sensor_readings_iterator, 9, 14))

# print(selected_readings)
# Expected output: ['Reading-9', 'Reading-10', 'Reading-11', 'Reading-12', 'Reading-13']

# PATTERN: Itertools Patterns

import itertools

shirt_colors = ['Red', 'Blue', 'Green']
shirt_sizes = ['S', 'M', 'L', 'XL']
shirt_materials = ['Cotton', 'Polyester']

# Generate all possible combinations of shirt variants
all_variants = list(itertools.product(shirt_colors, shirt_sizes, shirt_materials))

# print(all_variants[:5]) # Print first 5 for brevity
# Expected output: [('Red', 'S', 'Cotton'), ('Red', 'S', 'Polyester'), ('Red', 'M', 'Cotton'), ('Red', 'M', 'Polyester'), ('Red', 'L', 'Cotton')]

# PATTERN: Itertools Patterns

import itertools

candidate_pool = ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
committee_size = 3

# Find all unique combinations of 3-person committees
possible_committees = list(itertools.combinations(candidate_pool, committee_size))

# print(possible_committees)
# Expected output: [('Alice', 'Bob', 'Charlie'), ('Alice', 'Bob', 'David'), ('Alice', 'Bob', 'Eve'),
#                   ('Alice', 'Charlie', 'David'), ('Alice', 'Charlie', 'Eve'), ('Alice', 'David', 'Eve'),
#                   ('Bob', 'Charlie', 'David'), ('Bob', 'Charlie', 'Eve'), ('Bob', 'David', 'Eve'),
#                   ('Charlie', 'David', 'Eve')]