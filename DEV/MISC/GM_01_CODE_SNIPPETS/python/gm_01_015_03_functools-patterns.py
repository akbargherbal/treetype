# PATTERN: Functools Patterns

import functools
import time

@functools.lru_cache(maxsize=None)
def calculate_expensive_result(n):
    time.sleep(0.1) # Simulate an expensive computation
    return n * 2

print(f"First call: {calculate_expensive_result(5)}")
print(f"Second call (cached): {calculate_expensive_result(5)}")
print(f"Third call (new arg): {calculate_expensive_result(10)}")

# PATTERN: Functools Patterns

import functools

def power(base, exponent):
    return base ** exponent

# Create a new function 'square' that always raises to the power of 2
square = functools.partial(power, exponent=2)

# Create a new function 'cube' that always raises to the power of 3
cube = functools.partial(power, exponent=3)

print(f"5 squared is: {square(5)}")
print(f"3 cubed is: {cube(3)}")
print(f"2 to the power of 10 is: {power(2, 10)}")

# PATTERN: Functools Patterns

import functools
import operator

numbers = [1, 2, 3, 4, 5]

# Sum all numbers in the list
sum_of_numbers = functools.reduce(operator.add, numbers)
print(f"Sum of numbers: {sum_of_numbers}")

# Find the product of all numbers in the list
product_of_numbers = functools.reduce(operator.mul, numbers)
print(f"Product of numbers: {product_of_numbers}")

# Concatenate strings
words = ["Hello", " ", "World", "!"]
sentence = functools.reduce(operator.add, words)
print(f"Concatenated sentence: '{sentence}'")