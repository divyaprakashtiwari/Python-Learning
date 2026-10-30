"""
Question 9: Asynchronous Batch Executor with Semaphore Throttling & Timeouts
Topic: JSON, CSV, Web APIs, and Databases

Key Concepts Tested:
- asyncio non-blocking concurrency (async / await, asyncio.sleep)
- Resource concurrency throttling via asyncio.Semaphore
- Per-item timeout enforcement using asyncio.wait_for and asyncio.TimeoutError
- Resilient batch gathering with asyncio.gather(*tasks, return_exceptions=True)
- Benchmarking wall-clock speedup versus hypothetical sequential duration
"""

import time
import asyncio
from typing import List, Dict, Any


class AsyncBatchExecutor:
    """
    Asynchronous executor managing concurrent network/service requests
    with semaphore rate-limiting, per-item timeouts, and fault-tolerant aggregation.
    """

    def __init__(self) -> None:
        self.peak_concurrent = 0
        self._current_active = 0
        self._lock = asyncio.Lock()

    async def _track_start(self) -> None:
        async with self._lock:
            self._current_active += 1
            if self._current_active > self.peak_concurrent:
                self.peak_concurrent = self._current_active

    async def _track_end(self) -> None:
        async with self._lock:
            self._current_active -= 1

    async def fetch_simulated_resource(
        self,
        item_id: int,
        latency: float,
        fail: bool = False,
    ) -> Dict[str, Any]:
        """Simulates non-blocking I/O with potential failure."""
        await self._track_start()
        try:
            await asyncio.sleep(latency)
            if fail:
                raise ConnectionResetError(f"Simulated connection reset for item {item_id}")
            return {"id": item_id, "data": f"Resource data for {item_id}", "latency": latency}
        finally:
            await self._track_end()

    async def _worker_wrapper(
        self,
        item: Dict[str, Any],
        semaphore: asyncio.Semaphore,
        timeout: float,
    ) -> Dict[str, Any]:
        """Wraps task with semaphore acquisition and timeout boundary."""
        item_id = item["id"]
        latency = item.get("latency", 0.1)
        fail = item.get("fail", False)

        async with semaphore:
            try:
                result = await asyncio.wait_for(
                    self.fetch_simulated_resource(item_id, latency, fail),
                    timeout=timeout,
                )
                return {"status": "SUCCESS", "id": item_id, "data": result}
            except asyncio.TimeoutError:
                return {
                    "status": "TIMEOUT",
                    "id": item_id,
                    "error": f"Item {item_id} exceeded {timeout}s timeout (latency: {latency}s)",
                }
            except Exception as exc:
                return {
                    "status": "ERROR",
                    "id": item_id,
                    "error": f"{type(exc).__name__}: {exc}",
                }

    async def execute_batch(
        self,
        items: List[Dict[str, Any]],
        max_concurrency: int = 3,
        timeout_per_item: float = 2.0,
    ) -> Dict[str, Any]:
        """
        Executes a batch of items concurrently up to max_concurrency.
        Returns detailed summary and timing analytics.
        """
        self.peak_concurrent = 0
        self._current_active = 0
        semaphore = asyncio.Semaphore(max_concurrency)

        start_time = time.perf_counter()
        tasks = [
            self._worker_wrapper(item, semaphore, timeout_per_item)
            for item in items
        ]

        raw_results = await asyncio.gather(*tasks, return_exceptions=True)
        elapsed_time = time.perf_counter() - start_time

        successful = []
        timeouts = []
        errors = []

        for res in raw_results:
            if isinstance(res, Exception):
                errors.append(str(res))
            elif isinstance(res, dict):
                st = res.get("status")
                if st == "SUCCESS":
                    successful.append(res)
                elif st == "TIMEOUT":
                    timeouts.append(res)
                else:
                    errors.append(res)

        sequential_time = sum(item.get("latency", 0.0) for item in items)

        return {
            "total_items": len(items),
            "successful_count": len(successful),
            "timeout_count": len(timeouts),
            "error_count": len(errors),
            "successful_ids": [s["id"] for s in successful],
            "timeout_details": timeouts,
            "error_details": errors,
            "elapsed_seconds": round(elapsed_time, 2),
            "hypothetical_sequential_seconds": round(sequential_time, 2),
            "peak_concurrency_observed": self.peak_concurrent,
            "max_concurrency_limit": max_concurrency,
        }


if __name__ == "__main__":
    work_items = [
        {"id": 1, "latency": 0.5, "fail": False},
        {"id": 2, "latency": 1.2, "fail": False},
        {"id": 3, "latency": 2.5, "fail": False},  # Exceeds 1.5s timeout!
        {"id": 4, "latency": 0.3, "fail": True},   # Simulated failure
        {"id": 5, "latency": 0.6, "fail": False},
        {"id": 6, "latency": 0.4, "fail": False},
    ]

    executor = AsyncBatchExecutor()
    report = asyncio.run(executor.execute_batch(work_items, max_concurrency=3, timeout_per_item=1.5))

    print("=== Asynchronous Batch Execution Report ===")
    print(f"Batch Execution Completed in: ~{report['elapsed_seconds']} seconds (vs ~{report['hypothetical_sequential_seconds']}s sequential)")
    print(f"Total Items Dispatched: {report['total_items']}")
    print(f"Successful Results: {report['successful_count']} (IDs: {report['successful_ids']})")
    print(f"Timeouts Encountered: {report['timeout_count']} (ID: {report['timeout_details'][0]['id']} exceeded 1.5s timeout)")
    print(f"Errors Caught: {report['error_count']} (ID: {report['error_details'][0]['id']} failed with {report['error_details'][0]['error']})")
    print(f"Throttling Verification: Max concurrent tasks observed: {report['peak_concurrency_observed']} (Limit: {report['max_concurrency_limit']})")
