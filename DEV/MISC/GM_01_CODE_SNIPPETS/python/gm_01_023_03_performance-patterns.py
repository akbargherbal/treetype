# PATTERN: Performance Patterns

import timeit

def process_data(n):
    return [x * x for x in range(n)]

# Time a function call
execution_time = timeit.timeit(
    "process_data(1000)",
    setup="from __main__ import process_data",
    number=1000
)
print(f"Execution time: {execution_time:.4f} seconds")

# PATTERN: Performance Patterns

import cProfile

def expensive_string_op(iterations):
    data = []
    for i in range(iterations):
        data.append(str(i) * 50)
    return "".join(data)

def main_profiling_target():
    result1 = expensive_string_op(1000)
    result2 = expensive_string_op(500)
    return result1 + result2

# Run the profiler on the target function
cProfile.run('main_profiling_target()')

# PATTERN: Performance Patterns

def prime_number_generator(limit):
    """Generates prime numbers up to a given limit."""
    primes = []
    for num in range(2, limit + 1):
        is_prime = True
        for p in primes:
            if p * p > num:
                break
            if num % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
            yield num

# Iterate over the generator
print("Primes up to 30:")
for prime in prime_number_generator(30):
    print(prime, end=" ")
print()

# PATTERN: Performance Patterns

def sub_task_generator(start, end):
    """A sub-generator yielding numbers in a range."""
    for i in range(start, end):
        yield f"Sub-task item {i}"

def main_workflow_generator():
    """A main generator delegating to sub-generators."""
    yield "Starting main workflow..."
    yield from sub_task_generator(1, 3) # Delegate to first sub-task
    yield "Intermediate step completed."
    yield from sub_task_generator(5, 7) # Delegate to second sub-task
    yield "Main workflow finished."

# Consume items from the main generator
for item in main_workflow_generator():
    print(item)

# PATTERN: Performance Patterns

class PointWithoutSlots:
    """A class without __slots__, using a __dict__ for attributes."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

class PointWithSlots:
    """A class with __slots__ for memory optimization."""
    __slots__ = ('x', 'y', 'color') # Define all expected attributes
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

# Create instances
p_normal = PointWithoutSlots(10, 20)
p_optimized = PointWithSlots(10, 20, "red")

# Access attributes
print(f"Normal Point: ({p_normal.x}, {p_normal.y})")
print(f"Optimized Point: ({p_optimized.x}, {p_optimized.y}, {p_optimized.color})")