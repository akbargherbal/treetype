# PATTERN: Multiprocessing/Threading

import threading
import time

def worker_function(name):
    time.sleep(1)
    print(f"Worker {name} finished task.")

thread1 = threading.Thread(target=worker_function, args=("Alpha",))
thread2 = threading.Thread(target=worker_function, args=("Beta",))

thread1.start()
thread2.start()

thread1.join()
thread2.join()
print("All workers completed.")

# PATTERN: Multiprocessing/Threading

import concurrent.futures
import time

def process_data(item):
    time.sleep(0.5) # Simulate work
    return f"Processed item {item}"

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    data_items = [1, 2, 3, 4, 5]
    futures = [executor.submit(process_data, item) for item in data_items]
    
    for future in futures:
        print(future.result())

# PATTERN: Multiprocessing/Threading

import concurrent.futures
import time

def calculate_square(number):
    time.sleep(0.1) # Simulate CPU-bound work
    return number * number

if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    results = []

    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(calculate_square, num) for num in numbers]
        for future in futures:
            results.append(future.result())
    
    print(f"Squares: {results}")

# PATTERN: Multiprocessing/Threading

import concurrent.futures
import time

def fetch_url(url):
    time.sleep(len(url) % 3 + 1) # Simulate varying network latency
    return f"Finished fetching {url}"

urls = ["http://example.com/1", "http://example.com/2", "http://example.com/3", "http://example.com/4"]

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    future_to_url = {executor.submit(fetch_url, url): url for url in urls}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            result = future.result()
            print(f"{url}: {result}")
        except Exception as exc:
            print(f"{url} generated an exception: {exc}")

# PATTERN: Multiprocessing/Threading

import threading
import time

shared_counter = 0
counter_lock = threading.Lock()

def increment_counter(iterations):
    global shared_counter
    for _ in range(iterations):
        with counter_lock:
            current_value = shared_counter
            time.sleep(0.001) # Simulate some work
            shared_counter = current_value + 1

threads = []
for i in range(5):
    thread = threading.Thread(target=increment_counter, args=(1000,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print(f"Final shared counter value: {shared_counter}")