# PATTERN: Pandas Patterns (B/A- Level Refinement)

import pandas as pd
import os

# Create a sample DataFrame
data = {'col1': [1, 2, 3], 'col2': ['A', 'B', 'C']}
df_original = pd.DataFrame(data)

# Define a file path
pickle_file = 'sample_data.pkl'

# Save DataFrame to pickle
df_original.to_pickle(pickle_file)

# Read DataFrame from pickle
df_loaded = pd.read_pickle(pickle_file)

# Clean up the file
os.remove(pickle_file)

# PATTERN: Pandas Patterns (B/A- Level Refinement)

import pandas as pd
import io

csv_data = """
transaction_id,product_name,price,transaction_date
101,Laptop,1200.50,2023-01-15
102,Mouse,25.00,2023-01-16
103,Keyboard,75.99,2023-01-15
"""

df = pd.read_csv(
    io.StringIO(csv_data),
    dtype={'transaction_id': str, 'price': float},
    parse_dates=['transaction_date']
)

# PATTERN: Pandas Patterns (B/A- Level Refinement)

import pandas as pd

data = {
    'product': ['Apple', 'Banana', 'Orange', 'Grape', 'Apple'],
    'price': [1.20, 0.50, 0.80, 2.10, 1.30],
    'quantity': [100, 250, 150, 75, 120]
}
df = pd.DataFrame(data)

# Query for products with price > 1.00 and quantity < 100
filtered_df = df.query("price > 1.00 and quantity < 100")

# PATTERN: Pandas Patterns (B/A- Level Refinement)

import pandas as pd

data = {'city': ['New York', 'London', 'Paris', 'Tokyo'],
        'population': [8.4, 8.9, 2.1, 14.0]}
df = pd.DataFrame(data, index=['NY', 'LDN', 'PRS', 'TKY'])

# Select rows by label using loc
london_data = df.loc['LDN']

# Select rows by integer position using iloc
first_two_cities = df.iloc[0:2]

# PATTERN: Pandas Patterns (B/A- Level Refinement)

import pandas as pd

data = {
    'student_name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'score': [85, 92, 78, 65, 95],
    'grade': ['B', 'A', 'C', 'D', 'A']
}
df = pd.DataFrame(data)

# Select students with a score greater than 90
high_achievers = df[df['score'] > 90]

# Select students with grade 'A' or 'B'
top_grades = df[(df['grade'] == 'A') | (df['grade'] == 'B')]

# PATTERN: Pandas Patterns (B/A- Level Refinement)

import pandas as pd
import numpy as np

data = {
    'department': ['HR', 'IT', 'HR', 'IT', 'Finance', 'HR'],
    'employee_id': [1, 2, 3, 4, 5, 6],
    'salary': [60000, 90000, 65000, 95000, 70000, 72000],
    'years_exp': [5, 8, 6, 9, 7, 6]
}
df = pd.DataFrame(data)

# Group by department and aggregate multiple columns
department_stats = df.groupby('department').agg(
    total_employees=('employee_id', 'count'),
    avg_salary=('salary', 'mean'),
    max_years_exp=('years_exp', np.max)
)

# PATTERN: Pandas Patterns (B/A- Level Refinement)

import pandas as pd

data = {
    'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor'],
    'price': [1200, 25, 75, 300],
    'discount_rate': [0.10, 0.05, 0.15, 0.10]
}
df = pd.DataFrame(data)

# Calculate discounted price using apply with a lambda function
df['discounted_price'] = df.apply(
    lambda row: row['price'] * (1 - row['discount_rate']),
    axis=1
)

# PATTERN: Pandas Patterns (B/A- Level Refinement)

import pandas as pd

def add_tax(df_input, tax_rate):
    df_input['price_with_tax'] = df_input['price'] * (1 + tax_rate)
    return df_input

data = {'item': ['A', 'B', 'C'], 'price': [10, 20, 30]}
df = pd.DataFrame(data)

# Use pipe to insert a custom function into a method chain
processed_df = (
    df.set_index('item')
    .pipe(add_tax, tax_rate=0.05)
    .sort_values('price_with_tax', ascending=False)
)

# PATTERN: Pandas Patterns (B/A- Level Refinement)

import pandas as pd

# Orders DataFrame
orders_data = {
    'order_id': [1, 2, 3, 4],
    'customer_id': [101, 102, 101, 103],
    'order_date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04']
}
df_orders = pd.DataFrame(orders_data)

# Customers DataFrame
customers_data = {
    'customer_id': [101, 102, 103],
    'customer_name': ['Alice', 'Bob', 'Charlie']
}
df_customers = pd.DataFrame(customers_data)

# Perform an inner merge on 'customer_id'
merged_df = pd.merge(df_orders, df_customers, on='customer_id', how='inner')

# PATTERN: Pandas Patterns (B/A- Level Refinement)

import pandas as pd

# First DataFrame
df1_data = {'product': ['Laptop', 'Mouse'], 'price': [1200, 25]}
df1 = pd.DataFrame(df1_data)

# Second DataFrame
df2_data = {'product': ['Keyboard', 'Monitor'], 'price': [75, 300]}
df2 = pd.DataFrame(df2_data)

# Concatenate DataFrames vertically (default axis=0)
combined_df = pd.concat([df1, df2], ignore_index=True)

# PATTERN: Pandas Patterns (B/A- Level Refinement)

import pandas as pd
import numpy as np

data = {
    'region': ['East', 'West', 'East', 'West', 'East', 'West'],
    'product_type': ['A', 'B', 'A', 'A', 'B', 'B'],
    'sales': [100, 150, 120, 90, 110, 160],
    'units_sold': [10, 15, 12, 9, 11, 16]
}
df = pd.DataFrame(data)

# Create a pivot table to show average sales and total units by region and product type
pivot_df = pd.pivot_table(
    df,
    values=['sales', 'units_sold'],
    index='region',
    columns='product_type',
    aggfunc={'sales': np.mean, 'units_sold': np.sum}
)

# PATTERN: Pandas Patterns (B/A- Level Refinement)

import pandas as pd

# Wide format DataFrame
data = {
    'country': ['USA', 'Canada', 'Mexico'],
    '2020_gdp': [21.4, 1.6, 1.2],
    '2021_gdp': [23.3, 2.0, 1.3],
    '2022_gdp': [25.5, 2.2, 1.4]
}
df_wide = pd.DataFrame(data)

# Melt the DataFrame to long format
df_long = pd.melt(
    df_wide,
    id_vars=['country'],
    var_name='year_gdp',
    value_name='gdp_trillions'
)

# PATTERN: Pandas Patterns (B/A- Level Refinement)

import pandas as pd

data = {
    'id': [1, 2, 3],
    'value': ['100', '200', '300'],
    'category': ['A', 'B', 'A']
}
df = pd.DataFrame(data)

# Convert 'id' to string and 'value' to integer
df['id'] = df['id'].astype(str)
df['value'] = df['value'].astype(int)

# Convert 'category' to a categorical type
df['category'] = df['category'].astype('category')

# PATTERN: Pandas Patterns (B/A- Level Refinement)

import pandas as pd
import numpy as np

data = {
    'A': [1, 2, np.nan, 4],
    'B': [np.nan, 6, 7, 8],
    'C': [9, 10, 11, np.nan]
}
df = pd.DataFrame(data)

# Fill NaN values in column 'A' with 0
df['A'] = df['A'].fillna(0)

# Fill all remaining NaN values with the mean of their respective columns
df_filled_mean = df.fillna(df.mean(numeric_only=True))

# Drop rows that contain any NaN values
df_dropped = df.dropna()

# PATTERN: Pandas Patterns (B/A- Level Refinement)

import pandas as pd

data = {
    'product_code': ['ABC-123', 'DEF-456', 'GHI-789', 'abc-000'],
    'description': ['Laptop Pro', 'Wireless Mouse', 'Gaming Keyboard', 'USB Hub']
}
df = pd.DataFrame(data)

# Convert 'product_code' to uppercase
df['product_code_upper'] = df['product_code'].str.upper()

# Check if 'description' contains 'Mouse'
df['is_mouse'] = df['description'].str.contains('Mouse', case=False)

# Extract first three characters from 'product_code'
df['prefix'] = df['product_code'].str[:3]

# PATTERN: Pandas Patterns (B/A- Level Refinement)

import pandas as pd

data = {
    'event_name': ['Meeting', 'Workshop', 'Deadline'],
    'event_date': ['2023-01-15 10:00:00', '2023-02-20 14:30:00', '2023-03-01 23:59:59']
}
df = pd.DataFrame(data)

# Convert 'event_date' to datetime objects
df['event_date'] = pd.to_datetime(df['event_date'])

# Extract year, month, and day name
df['year'] = df['event_date'].dt.year
df['month'] = df['event_date'].dt.month
df['day_of_week'] = df['event_date'].dt.day_name()

# PATTERN: Pandas Patterns (B/A- Level Refinement)

import pandas as pd

data = {
    'item': ['A', 'B', 'C', 'D'],
    'price': [100, 200, 150, 300],
    'quantity': [2, 1, 3, 2]
}
df = pd.DataFrame(data)

# Use assign to create new columns 'total_cost' and 'discounted_price'
df_with_new_cols = df.assign(
    total_cost=lambda x: x['price'] * x['quantity'],
    discounted_price=lambda x: x['price'] * 0.9 if x['price'] > 150 else x['price']
)

# PATTERN: Pandas Patterns (B/A- Level Refinement)

import pandas as pd

data = {
    'old_col_name_1': [1, 2, 3],
    'old_col_name_2': ['A', 'B', 'C'],
    'another_old_col': [True, False, True]
}
df = pd.DataFrame(data)

# Rename specific columns using a dictionary
df_renamed = df.rename(columns={
    'old_col_name_1': 'new_col_1',
    'old_col_name_2': 'new_col_2'
})

# PATTERN: Pandas Patterns (B/A- Level Refinement)

import pandas as pd

data = {
    'product_id': [101, 102, 103, 104],
    'product_name': ['Laptop', 'Mouse', 'Keyboard', 'Monitor'],
    'price': [1200, 25, 75, 300]
}
df = pd.DataFrame(data)

# Set 'product_id' as the index
df_indexed = df.set_index('product_id')

# Reset the index, moving 'product_id' back to a column
df_reset = df_indexed.reset_index()

# PATTERN: Pandas Patterns (B/A- Level Refinement)

import pandas as pd

data = {
    'department': ['HR', 'IT', 'HR', 'IT', 'Finance', 'HR'],
    'employee_name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank'],
    'salary': [60000, 90000, 65000, 95000, 70000, 72000],
    'years_exp': [5, 8, 6, 9, 7, 6]
}
df = pd.DataFrame(data)

# Sort by 'department' ascending, then by 'salary' descending
df_sorted = df.sort_values(by=['department', 'salary'], ascending=[True, False])