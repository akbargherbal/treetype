# PATTERN: Async Python Patterns

import asyncio

async def fetch_user_data(user_id: int) -> dict:
    """Simulates fetching user data from a database or API."""
    await asyncio.sleep(0.5) # Simulate network/DB delay
    return {"id": user_id, "name": f"User {user_id}", "email": f"user{user_id}@example.com"}

async def main():
    user_data = await fetch_user_data(123)
    print(f"Fetched: {user_data['name']}")

if __name__ == "__main__":
    asyncio.run(main())

# PATTERN: Async Python Patterns

import asyncio

async def simulate_io_operation(duration: float) -> str:
    """Simulates an I/O-bound operation."""
    await asyncio.sleep(duration)
    return f"Operation completed in {duration} seconds."

async def process_data():
    print("Starting data processing...")
    result1 = await simulate_io_operation(1.0) # Awaiting the coroutine
    print(result1)
    result2 = await simulate_io_operation(0.5)
    print(result2)
    print("Data processing finished.")

if __name__ == "__main__":
    asyncio.run(process_data())

# PATTERN: Async Python Patterns

import asyncio

async def startup_message():
    await asyncio.sleep(0.1)
    print("Application started successfully!")

async def main_application_logic():
    print("Executing main application logic...")
    await startup_message()
    print("Main logic finished.")

if __name__ == "__main__":
    asyncio.run(main_application_logic())

# PATTERN: Async Python Patterns

import asyncio
import time

async def perform_task(task_name: str, delay: float) -> str:
    """Simulates an asynchronous task with a delay."""
    start_time = time.time()
    await asyncio.sleep(delay)
    end_time = time.time()
    return f"{task_name} finished in {end_time - start_time:.2f}s"

async def run_parallel_tasks():
    print("Starting parallel tasks...")
    results = await asyncio.gather(
        perform_task("Task A", 2),
        perform_task("Task B", 1),
        perform_task("Task C", 1.5)
    )
    print("All tasks completed:")
    for res in results:
        print(f"- {res}")

if __name__ == "__main__":
    asyncio.run(run_parallel_tasks())

# PATTERN: Async Python Patterns

import asyncio

async def async_number_generator(count: int):
    """An asynchronous generator yielding numbers."""
    for i in range(count):
        await asyncio.sleep(0.1) # Simulate async operation per item
        yield i * 10

async def process_numbers():
    print("Starting async number processing...")
    async for number in async_number_generator(5):
        print(f"Processed number: {number}")
    print("Finished async number processing.")

if __name__ == "__main__":
    asyncio.run(process_numbers())

# PATTERN: Async Python Patterns

import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def async_resource_manager(name: str):
    """An asynchronous context manager for managing a resource."""
    print(f"Entering async resource: {name}")
    await asyncio.sleep(0.1) # Simulate async setup
    try:
        yield f"Managed_{name}"
    finally:
        await asyncio.sleep(0.1) # Simulate async cleanup
        print(f"Exiting async resource: {name}")

async def use_async_resource():
    print("Attempting to use async resource...")
    async with async_resource_manager("DatabaseConnection") as db_conn:
        print(f"Using resource: {db_conn}")
        await asyncio.sleep(0.2) # Simulate work with resource
    print("Finished using async resource.")

if __name__ == "__main__":
    asyncio.run(use_async_resource())

# PATTERN: Async Python Patterns

import asyncio
import time

async def background_job(job_id: int, delay: float):
    """A long-running background job."""
    print(f"Job {job_id}: Starting...")
    await asyncio.sleep(delay)
    print(f"Job {job_id}: Finished after {delay} seconds.")
    return f"Job {job_id} result"

async def main_with_background_tasks():
    print("Main: Starting...")
    task1 = asyncio.create_task(background_job(1, 3))
    task2 = asyncio.create_task(background_job(2, 1))

    print("Main: Tasks created, continuing main work...")
    await asyncio.sleep(0.5) # Main thread does some work
    print("Main: Waiting for tasks to complete...")

    results = await asyncio.gather(task1, task2) # Await tasks to get results
    print(f"Main: All tasks completed. Results: {results}")
    print("Main: Finished.")

if __name__ == "__main__":
    asyncio.run(main_with_background_tasks())