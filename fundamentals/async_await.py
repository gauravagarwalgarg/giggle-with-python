"""
Async/Await in Python asyncio, aiohttp, concurrent.futures.

Async is essential for I/O-bound tasks: HTTP calls, DB queries, file I/O.
It lets you handle thousands of concurrent operations without threads.

Key insight: async doesn't make things faster it makes waiting more efficient.
"""
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from typing import Any


# =============================================================================
# ASYNCIO BASICS coroutines, tasks, gathering
# =============================================================================

async def fetch_data(url: str, delay: float = 1.0) -> dict:
    """Simulate an async HTTP request.

    In real code, you'd use aiohttp or httpx here.
    """
    print(f"  Fetching {url}...")
    await asyncio.sleep(delay)  # Non-blocking sleep (simulates I/O wait)
    return {"url": url, "status": 200, "data": f"Response from {url}"}


async def sequential_requests():
    """BAD: Sequential async defeats the purpose.

    Total time: sum of all delays.
    """
    start = time.perf_counter()

    result1 = await fetch_data("https://api.example.com/users", 1.0)
    result2 = await fetch_data("https://api.example.com/posts", 1.5)
    result3 = await fetch_data("https://api.example.com/comments", 0.5)

    elapsed = time.perf_counter() - start
    print(f"  Sequential: {elapsed:.2f}s (expected ~3.0s)")
    return [result1, result2, result3]


async def concurrent_requests():
    """GOOD: Concurrent async all requests run simultaneously.

    Total time: max of all delays.
    """
    start = time.perf_counter()

    # asyncio.gather runs coroutines concurrently
    results = await asyncio.gather(
        fetch_data("https://api.example.com/users", 1.0),
        fetch_data("https://api.example.com/posts", 1.5),
        fetch_data("https://api.example.com/comments", 0.5),
    )

    elapsed = time.perf_counter() - start
    print(f"  Concurrent: {elapsed:.2f}s (expected ~1.5s)")
    return results


# =============================================================================
# TASKS more control over concurrent operations
# =============================================================================

async def process_with_tasks():
    """Tasks give you more control than gather cancel, check status, etc."""

    async def download(name: str, size: int) -> str:
        await asyncio.sleep(size / 100)  # Simulate download
        return f"{name} ({size}MB) complete"

    # Create tasks
    tasks = [
        asyncio.create_task(download("file1.zip", 100), name="file1"),
        asyncio.create_task(download("file2.zip", 200), name="file2"),
        asyncio.create_task(download("file3.zip", 50), name="file3"),
    ]

    # Wait for all tasks
    done, pending = await asyncio.wait(tasks, timeout=5.0)

    for task in done:
        print(f"  ✓ {task.get_name()}: {task.result()}")

    for task in pending:
        task.cancel()
        print(f"  ✗ {task.get_name()}: cancelled (timeout)")


# =============================================================================
# ASYNC PATTERNS timeouts, semaphores, queues
# =============================================================================

async def with_timeout():
    """Set timeouts on async operations."""
    try:
        result = await asyncio.wait_for(
            fetch_data("https://slow-api.example.com", delay=5.0),
            timeout=2.0
        )
    except asyncio.TimeoutError:
        print("  Request timed out after 2s")
        result = None
    return result


async def rate_limited_requests(urls: list[str], max_concurrent: int = 3):
    """Semaphore limit concurrent operations (rate limiting).

    Without this, you might overwhelm an API with too many requests.
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    async def limited_fetch(url: str) -> dict:
        async with semaphore:
            return await fetch_data(url, delay=0.5)

    results = await asyncio.gather(*[limited_fetch(url) for url in urls])
    return results


async def producer_consumer():
    """Async queue producer/consumer pattern.

    Great for processing pipelines where producers and consumers
    work at different speeds.
    """
    queue: asyncio.Queue[str] = asyncio.Queue(maxsize=5)

    async def producer(name: str, items: list[str]):
        for item in items:
            await queue.put(item)
            print(f"  Producer {name}: put {item}")
            await asyncio.sleep(0.1)
        await queue.put(None)  # Sentinel to signal completion

    async def consumer(name: str):
        while True:
            item = await queue.get()
            if item is None:
                queue.task_done()
                break
            print(f"  Consumer {name}: processing {item}")
            await asyncio.sleep(0.3)  # Simulate processing
            queue.task_done()

    # Run producer and consumer concurrently
    await asyncio.gather(
        producer("P1", ["task1", "task2", "task3"]),
        consumer("C1"),
    )


# =============================================================================
# ASYNC GENERATORS AND ITERATORS
# =============================================================================

async def async_range(start: int, stop: int, delay: float = 0.1):
    """Async generator yields values asynchronously.

    Useful for streaming data from APIs or databases.
    """
    for i in range(start, stop):
        await asyncio.sleep(delay)
        yield i


async def paginated_fetch(base_url: str, total_pages: int = 5):
    """Simulate paginated API that yields pages asynchronously."""
    for page in range(1, total_pages + 1):
        await asyncio.sleep(0.2)  # Simulate API call
        yield {
            "page": page,
            "items": [f"item_{page}_{i}" for i in range(3)],
            "has_next": page < total_pages,
        }


async def consume_async_generator():
    """Consume an async generator with async for."""
    print("  Async range:")
    async for num in async_range(0, 5, delay=0.1):
        print(f"    Got: {num}")

    print("  Paginated fetch:")
    async for page_data in paginated_fetch("https://api.example.com/items"):
        print(f"    Page {page_data['page']}: {len(page_data['items'])} items")


# =============================================================================
# ASYNC CONTEXT MANAGERS
# =============================================================================

class AsyncDatabaseConnection:
    """Async context manager for resources that need async setup/teardown."""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connected = False

    async def __aenter__(self):
        """Async setup connect to database."""
        print(f"  Connecting to {self.connection_string}...")
        await asyncio.sleep(0.5)  # Simulate connection
        self.connected = True
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async teardown close connection."""
        print("  Closing connection...")
        await asyncio.sleep(0.1)
        self.connected = False
        return False

    async def query(self, sql: str) -> list[dict]:
        """Simulate a database query."""
        await asyncio.sleep(0.2)
        return [{"id": 1, "name": "example"}]


async def use_async_context():
    """Demonstrate async context manager."""
    async with AsyncDatabaseConnection("postgres://localhost/mydb") as db:
        results = await db.query("SELECT * FROM users")
        print(f"  Query results: {results}")


# =============================================================================
# CONCURRENT.FUTURES threads and processes for CPU-bound work
# =============================================================================

def cpu_intensive_task(n: int) -> int:
    """CPU-bound task use ProcessPoolExecutor for these."""
    return sum(i * i for i in range(n))


def io_bound_task(url: str) -> str:
    """I/O-bound task use ThreadPoolExecutor for these."""
    time.sleep(1)  # Simulate blocking I/O
    return f"Response from {url}"


def thread_pool_example():
    """ThreadPoolExecutor for blocking I/O in sync code.

    Use when you can't use async (e.g., libraries that don't support it).
    """
    urls = [f"https://api.example.com/page/{i}" for i in range(5)]

    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all tasks
        futures = {executor.submit(io_bound_task, url): url for url in urls}

        # Process results as they complete
        for future in as_completed(futures):
            url = futures[future]
            try:
                result = future.result()
                print(f"  {url}: {result}")
            except Exception as e:
                print(f"  {url}: Error {e}")


def process_pool_example():
    """ProcessPoolExecutor for CPU-bound work.

    Uses multiple processes to bypass the GIL.
    """
    numbers = [10_000_000, 20_000_000, 30_000_000]

    start = time.perf_counter()
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(cpu_intensive_task, numbers))
    elapsed = time.perf_counter() - start

    print(f"  Process pool: {len(results)} tasks in {elapsed:.2f}s")


# =============================================================================
# MIXING ASYNC WITH SYNC run_in_executor
# =============================================================================

async def async_with_blocking_io():
    """Use run_in_executor to run blocking code in async context.

    This is how you use libraries that don't support async.
    """
    loop = asyncio.get_event_loop()

    # Run blocking function in a thread pool
    result = await loop.run_in_executor(
        None,  # Use default executor
        io_bound_task,
        "https://blocking-api.example.com"
    )
    print(f"  Blocking result: {result}")


# =============================================================================
# REAL-WORLD PATTERN: aiohttp example (commented needs pip install aiohttp)
# =============================================================================

"""
import aiohttp

async def fetch_many_urls(urls: list[str]) -> list[dict]:
    '''Fetch multiple URLs concurrently with aiohttp.'''
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)

async def fetch_one(session: aiohttp.ClientSession, url: str) -> dict:
    '''Fetch a single URL with error handling.'''
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            data = await resp.json()
            return {"url": url, "status": resp.status, "data": data}
    except aiohttp.ClientError as e:
        return {"url": url, "error": str(e)}
"""


if __name__ == "__main__":
    print("=" * 60)
    print("Async/Await Demo")
    print("=" * 60)

    # Run async examples
    print("\n--- Sequential vs Concurrent ---")
    asyncio.run(sequential_requests())
    asyncio.run(concurrent_requests())

    print("\n--- Tasks ---")
    asyncio.run(process_with_tasks())

    print("\n--- Timeout ---")
    asyncio.run(with_timeout())

    print("\n--- Rate Limiting (Semaphore) ---")
    urls = [f"https://api.example.com/{i}" for i in range(6)]
    asyncio.run(rate_limited_requests(urls, max_concurrent=2))

    print("\n--- Async Generators ---")
    asyncio.run(consume_async_generator())

    print("\n--- Async Context Manager ---")
    asyncio.run(use_async_context())

    print("\n--- Thread Pool (Sync) ---")
    thread_pool_example()

    print("\nDone!")
