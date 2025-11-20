# PATTERN: Python Best Practices Patterns

def main_application_logic():
    """Runs the main logic of the application."""
    print("Starting the application...")
    # Simulate some work
    print("Application finished.")

if __name__ == '__main__':
    main_application_logic()

# PATTERN: Python Best Practices Patterns

def calculate_rectangle_area(length: float, width: float) -> float:
    """Calculates the area of a rectangle.

    Args:
        length: The length of the rectangle. Must be a positive number.
        width: The width of the rectangle. Must be a positive number.

    Returns:
        The calculated area of the rectangle.

    Raises:
        ValueError: If either length or width is not a positive number.
    """
    if length <= 0 or width <= 0:
        raise ValueError("Length and width must be positive.")
    return length * width

# PATTERN: Python Best Practices Patterns

def get_user_setting_eafp(user_profile: dict, setting_key: str, default_value: str) -> str:
    """Retrieves a user setting using the EAFP (Easier to Ask for Forgiveness than Permission) pattern."""
    try:
        value = user_profile[setting_key]
    except KeyError:
        value = default_value
    return value

user_data = {"name": "Alice", "email": "alice@example.com"}
city = get_user_setting_eafp(user_data, "city", "Unknown")
# print(f"User city: {city}")

# PATTERN: Python Best Practices Patterns

import subprocess
import sys
import os

env_name = "my_project_env"

# Create a virtual environment if it doesn't already exist
if not os.path.exists(env_name):
    subprocess.run([sys.executable, "-m", "venv", env_name], check=True)

# To activate this environment, run one of these commands in your shell:
# On Windows: .\%s\Scripts\activate
# On Linux/macOS: source ./%s/bin/activate