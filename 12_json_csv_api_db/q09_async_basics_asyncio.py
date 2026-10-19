"""
Topic 12: JSON, CSV, API, Database
Question 09: Async Basics (asyncio)

A comprehensive, production-grade guide to asynchronous programming with Python's
built-in `asyncio` module. Covers coroutines and event loops, concurrent gather with
return_exceptions, modern TaskGroup structured concurrency, timeouts & cancellation,
Locks & Semaphores, Event coordination, async generators, Producer-Consumer queues,
bridging sync blocking code via asyncio.to_thread, and an architectural Rate-Limited
Concurrent Worker Engine.

Every question contains standalone runnable exercises verified with 100% assertions.
"""

import asyncio
import time
from typing import List, Dict, Any, Optional, Tuple, AsyncGenerator


# =====================================================================
# Q1: Coroutines, await, and asyncio.run Execution Model
# =====================================================================
async def compute_square_async(val: int) -> int:
    """Simulates an asynchronous I/O calculation."""
    await asyncio.sleep(0.01)
    return val * val


async def q1_coroutine_basics_impl():
    # Coroutine function called without await returns a coroutine object
    coro = compute_square_async(5)
    assert asyncio.iscoroutine(coro)

    # Executing via await
    result = await coro
    assert result == 25

    # Sequential awaits
    t0 = time.time()
    res1 = await compute_square_async(3)
    res2 = await compute_square_async(4)
    elapsed = time.time() - t0

    assert res1 == 9
    assert res2 == 16
    assert elapsed >= 0.02


def q1_coroutine_basics():
    asyncio.run(q1_coroutine_basics_impl())
    print("=== Q1: Coroutines and Sequential Await Verified ===")


# =====================================================================
# Q2: Concurrent Task Execution with asyncio.gather
# =====================================================================
async def fetch_item(item_id: int, should_fail: bool = False) -> str:
    await asyncio.sleep(0.02)
    if should_fail:
        raise ValueError(f"Failed to fetch item {item_id}")
    return f"item_{item_id}"


async def q2_concurrent_gather_impl():
    t0 = time.time()
    # 1. Successful parallel gather: 3 tasks take ~0.02s combined instead of 0.06s
    results = await asyncio.gather(
        fetch_item(1),
        fetch_item(2),
        fetch_item(3)
    )
    elapsed = time.time() - t0
    assert results == ["item_1", "item_2", "item_3"]
    assert elapsed < 0.05

    # 2. Gather with return_exceptions=True
    mixed_results = await asyncio.gather(
        fetch_item(10),
        fetch_item(20, should_fail=True),
        fetch_item(30),
        return_exceptions=True
    )
    assert mixed_results[0] == "item_10"
    assert isinstance(mixed_results[1], ValueError)
    assert "Failed to fetch item 20" in str(mixed_results[1])
    assert mixed_results[2] == "item_30"


def q2_concurrent_gather():
    asyncio.run(q2_concurrent_gather_impl())
    print("=== Q2: Concurrent asyncio.gather Verified ===")


# =====================================================================
# Q3: Structured Concurrency with asyncio.TaskGroup
# =====================================================================
async def q3_structured_taskgroup_impl():
    """
    Demonstrates Python 3.11+ TaskGroup for robust structured concurrency.
    If any task inside the group fails, remaining active tasks are cancelled automatically.
    """
    results: List[str] = []

    async def worker(name: str, delay: float):
        await asyncio.sleep(delay)
        results.append(name)

    # 1. Normal TaskGroup execution
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(worker("worker_a", 0.01))
        t2 = tg.create_task(worker("worker_b", 0.02))

    assert "worker_a" in results
    assert "worker_b" in results
    assert t1.done() and t2.done()

    # 2. Error propagation and cancellation in TaskGroup
    async def faulty_worker():
        await asyncio.sleep(0.01)
        raise RuntimeError("Crash in task group")

    async def long_worker():
        try:
            await asyncio.sleep(0.2)
        except asyncio.CancelledError:
            results.append("long_worker_cancelled")
            raise

    caught_exception_group = False
    try:
        async with asyncio.TaskGroup() as tg_err:
            tg_err.create_task(faulty_worker())
            tg_err.create_task(long_worker())
    except (ExceptionGroup, RuntimeError):
        caught_exception_group = True

    assert caught_exception_group is True
    assert "long_worker_cancelled" in results


def q3_structured_taskgroup():
    asyncio.run(q3_structured_taskgroup_impl())
    print("=== Q3: Structured Concurrency with TaskGroup Verified ===")


# =====================================================================
# Q4: Timeouts and Task Cancellation
# =====================================================================
async def slow_operation(duration: float) -> str:
    try:
        await asyncio.sleep(duration)
        return "completed"
    except asyncio.CancelledError:
        # Cleanup can happen here
        raise


async def q4_timeouts_and_cancellation_impl():
    # 1. Timeout using asyncio.wait_for
    timed_out = False
    try:
        await asyncio.wait_for(slow_operation(0.2), timeout=0.03)
    except TimeoutError:
        timed_out = True
    assert timed_out is True

    # 2. Explicit task cancellation
    task = asyncio.create_task(slow_operation(0.5))
    await asyncio.sleep(0.01)
    task.cancel()

    cancelled = False
    try:
        await task
    except asyncio.CancelledError:
        cancelled = True

    assert cancelled is True
    assert task.cancelled() is True


def q4_timeouts_and_cancellation():
    asyncio.run(q4_timeouts_and_cancellation_impl())
    print("=== Q4: Timeouts and Task Cancellation Verified ===")


# =====================================================================
# Q5: Synchronization: Locks and Semaphores
# =====================================================================
class SharedCounter:
    def __init__(self):
        self.count = 0
        self.lock = asyncio.Lock()

    async def increment(self):
        async with self.lock:
            # Critical section protected against concurrent race conditions
            current = self.count
            await asyncio.sleep(0.001)
            self.count = current + 1


async def q5_locks_and_semaphores_impl():
    # 1. Async Lock
    counter = SharedCounter()
    tasks = [asyncio.create_task(counter.increment()) for _ in range(20)]
    await asyncio.gather(*tasks)
    assert counter.count == 20

    # 2. Async Semaphore (rate limiter / pool gate)
    sem = asyncio.Semaphore(2)  # max 2 workers active concurrently
    active_workers = 0
    max_observed_concurrent = 0

    async def worker():
        nonlocal active_workers, max_observed_concurrent
        async with sem:
            active_workers += 1
            if active_workers > max_observed_concurrent:
                max_observed_concurrent = active_workers
            await asyncio.sleep(0.01)
            active_workers -= 1

    worker_tasks = [asyncio.create_task(worker()) for _ in range(10)]
    await asyncio.gather(*worker_tasks)

    # Max concurrency never exceeded semaphore capacity
    assert max_observed_concurrent <= 2
    assert active_workers == 0


def q5_locks_and_semaphores():
    asyncio.run(q5_locks_and_semaphores_impl())
    print("=== Q5: Async Locks and Semaphores Verified ===")


# =====================================================================
# Q6: Event Flags for Cross-Coroutine Coordination
# =====================================================================
async def q6_event_coordination_impl():
    """
    Demonstrates asyncio.Event for signaling state transitions between coroutines.
    """
    ready_event = asyncio.Event()
    worker_started = []

    async def waiter(name: str):
        # Wait until event is set
        await ready_event.wait()
        worker_started.append(name)

    tasks = [
        asyncio.create_task(waiter("W1")),
        asyncio.create_task(waiter("W2")),
        asyncio.create_task(waiter("W3")),
    ]

    await asyncio.sleep(0.01)
    assert len(worker_started) == 0  # Still waiting

    # Trigger event
    ready_event.set()
    assert ready_event.is_set() is True
    await asyncio.gather(*tasks)

    assert len(worker_started) == 3
    assert set(worker_started) == {"W1", "W2", "W3"}


def q6_event_coordination():
    asyncio.run(q6_event_coordination_impl())
    print("=== Q6: Async Event Coordination Verified ===")


# =====================================================================
# Q7: Asynchronous Iterators and Generators
# =====================================================================
async def async_range(start: int, stop: int, delay: float = 0.005) -> AsyncGenerator[int, None]:
    """An asynchronous generator producing values over time."""
    for i in range(start, stop):
        await asyncio.sleep(delay)
        yield i


class AsyncDatabaseCursor:
    """Custom asynchronous iterator with __aiter__ and __anext__."""
    def __init__(self, items: List[str]):
        self.items = items
        self.idx = 0

    def __aiter__(self):
        return self

    async def __anext__(self) -> str:
        if self.idx >= len(self.items):
            raise StopAsyncIteration
        await asyncio.sleep(0.002)
        val = self.items[self.idx]
        self.idx += 1
        return val


async def q7_async_iterators_and_generators_impl():
    # 1. Async generator with 'async for'
    numbers = []
    async for num in async_range(1, 6):
        numbers.append(num)
    assert numbers == [1, 2, 3, 4, 5]

    # 2. Custom async iterator
    cursor = AsyncDatabaseCursor(["record_1", "record_2", "record_3"])
    extracted = []
    async for rec in cursor:
        extracted.append(rec)
    assert extracted == ["record_1", "record_2", "record_3"]


def q7_async_iterators_and_generators():
    asyncio.run(q7_async_iterators_and_generators_impl())
    print("=== Q7: Async Iterators and Generators Verified ===")


# =====================================================================
# Q8: Producer-Consumer Queue Architecture
# =====================================================================
async def producer(queue: asyncio.Queue, items: List[int]):
    for item in items:
        await queue.put(item)
        await asyncio.sleep(0.001)


async def consumer(queue: asyncio.Queue, results: List[int]):
    while True:
        item = await queue.get()
        try:
            # Process item
            await asyncio.sleep(0.002)
            results.append(item * 2)
        finally:
            queue.task_done()


async def q8_producer_consumer_queue_impl():
    queue: asyncio.Queue[int] = asyncio.Queue(maxsize=5)
    processed_results: List[int] = []

    # Spawn 2 consumer workers
    consumer_tasks = [
        asyncio.create_task(consumer(queue, processed_results))
        for _ in range(2)
    ]

    # Run producer to put 10 items
    await producer(queue, list(range(1, 11)))

    # Wait until all items have been processed by consumers
    await queue.join()

    # Cancel background consumers
    for c in consumer_tasks:
        c.cancel()
    await asyncio.gather(*consumer_tasks, return_exceptions=True)

    assert len(processed_results) == 10
    assert set(processed_results) == {i * 2 for i in range(1, 11)}


def q8_producer_consumer_queue():
    asyncio.run(q8_producer_consumer_queue_impl())
    print("=== Q8: Producer-Consumer Queue Architecture Verified ===")


# =====================================================================
# Q9: Bridging Blocking Code with asyncio.to_thread
# =====================================================================
def cpu_heavy_hash(data: str) -> str:
    """Synchronous CPU or blocking I/O operation."""
    time.sleep(0.02)
    import hashlib
    return hashlib.sha256(data.encode("utf-8")).hexdigest()[:8]


async def q9_bridging_blocking_code_impl():
    """
    Demonstrates offloading blocking functions to a thread pool executor
    so the main event loop remains responsive.
    """
    t0 = time.time()
    # Run 3 blocking calls concurrently in worker threads
    h1, h2, h3 = await asyncio.gather(
        asyncio.to_thread(cpu_heavy_hash, "payload_1"),
        asyncio.to_thread(cpu_heavy_hash, "payload_2"),
        asyncio.to_thread(cpu_heavy_hash, "payload_3")
    )
    elapsed = time.time() - t0

    assert len(h1) == 8 and len(h2) == 8 and len(h3) == 8
    assert h1 != h2 and h2 != h3
    assert h1 == cpu_heavy_hash("payload_1")
    assert elapsed < 0.5


def q9_bridging_blocking_code():
    asyncio.run(q9_bridging_blocking_code_impl())
    print("=== Q9: Bridging Blocking Code via asyncio.to_thread Verified ===")


# =====================================================================
# Q10: Architectural Rate-Limited Concurrent Worker Engine
# =====================================================================
class AsyncBatchProcessor:
    """
    Production-grade concurrent worker engine:
    - Bounded concurrency with Semaphore
    - Per-task error isolation and retry logic
    - Summary execution metrics (successes, errors, execution time)
    """
    def __init__(self, max_concurrency: int = 3, max_retries: int = 2):
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.max_retries = max_retries

    async def _execute_with_retry(self, item_id: int, worker_fn) -> Dict[str, Any]:
        attempts = 0
        async with self.semaphore:
            while attempts < self.max_retries:
                attempts += 1
                try:
                    res = await worker_fn(item_id)
                    return {"id": item_id, "status": "success", "data": res, "attempts": attempts}
                except Exception as err:
                    if attempts >= self.max_retries:
                        return {"id": item_id, "status": "failed", "error": str(err), "attempts": attempts}
                    await asyncio.sleep(0.005 * attempts)

    async def run(self, item_ids: List[int], worker_fn) -> Dict[str, Any]:
        t0 = time.time()
        tasks = [
            asyncio.create_task(self._execute_with_retry(item_id, worker_fn))
            for item_id in item_ids
        ]
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - t0

        successful = [r for r in results if r["status"] == "success"]
        failed = [r for r in results if r["status"] == "failed"]

        return {
            "total": len(item_ids),
            "successful_count": len(successful),
            "failed_count": len(failed),
            "results": results,
            "duration": round(elapsed, 4)
        }


async def q10_architectural_batch_processor_impl():
    # Worker that succeeds on all items except item 4
    async def sample_task(item_id: int):
        await asyncio.sleep(0.01)
        if item_id == 4:
            raise ValueError("Unrecoverable item 4")
        return f"result_for_{item_id}"

    processor = AsyncBatchProcessor(max_concurrency=3, max_retries=2)
    summary = await processor.run([1, 2, 3, 4, 5], sample_task)

    assert summary["total"] == 5
    assert summary["successful_count"] == 4
    assert summary["failed_count"] == 1

    item4_res = next(r for r in summary["results"] if r["id"] == 4)
    assert item4_res["status"] == "failed"
    assert item4_res["attempts"] == 2
    assert "Unrecoverable item 4" in item4_res["error"]


def q10_architectural_batch_processor():
    asyncio.run(q10_architectural_batch_processor_impl())
    print("=== Q10: Architectural Async Rate-Limited Batch Processor Verified ===")


# =====================================================================
# Main Test Runner
# =====================================================================
if __name__ == "__main__":
    q1_coroutine_basics()
    q2_concurrent_gather()
    q3_structured_taskgroup()
    q4_timeouts_and_cancellation()
    q5_locks_and_semaphores()
    q6_event_coordination()
    q7_async_iterators_and_generators()
    q8_producer_consumer_queue()
    q9_bridging_blocking_code()
    q10_architectural_batch_processor()

    print("\nAll 10 async basics (asyncio) practice questions passed successfully!")
