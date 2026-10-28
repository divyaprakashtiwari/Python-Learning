"""
Question 4: Class-Based Rate-Limiting & Retry Decorator
Topic: Advanced Python

Key Concepts Tested:
- Class decorator architecture (__init__ for config, __call__ for wrapping)
- Sliding-window rate limiting using collections.deque
- Exponential backoff retry mechanism
- Instance-level state and telemetry tracking
- Decorator metadata preservation (@functools.wraps)
"""

import time
import functools
import collections
from typing import Callable, Any, Deque


class RateLimitedRetry:
    """
    Class decorator implementing sliding-window rate limiting
    and exponential backoff retries.
    """

    def __init__(
        self,
        max_retries: int = 3,
        max_calls_per_second: int = 5,
        backoff_base: float = 0.05,
    ) -> None:
        self.max_retries = max_retries
        self.max_calls_per_second = max_calls_per_second
        self.backoff_base = backoff_base

        self.call_timestamps: Deque[float] = collections.deque()
        self.total_calls: int = 0
        self.total_retries: int = 0

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            now = time.time()

            # Evict timestamps older than 1.0 second
            while self.call_timestamps and (now - self.call_timestamps[0] > 1.0):
                self.call_timestamps.popleft()

            # Check capacity
            if len(self.call_timestamps) >= self.max_calls_per_second:
                raise RuntimeError(
                    f"Rate limit exceeded: Maximum {self.max_calls_per_second} calls/sec allowed"
                )

            # Record call
            self.call_timestamps.append(now)
            self.total_calls += 1

            # Execute with retry logic
            last_exception: Exception = RuntimeError("Unexpected execution state")
            for attempt in range(self.max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exception = exc
                    if attempt < self.max_retries:
                        self.total_retries += 1
                        delay = self.backoff_base * (2 ** attempt)
                        time.sleep(delay)
                    else:
                        raise last_exception

        wrapper.decorator_instance = self  # type: ignore[attr-defined]
        return wrapper


@RateLimitedRetry(max_retries=2, max_calls_per_second=3, backoff_base=0.01)
def fetch_api_data(query_id: int, simulate_failure: bool = False):
    """Fetches remote data payload."""
    if simulate_failure:
        raise ConnectionResetError("Remote server closed socket prematurely")
    return {"id": query_id, "data": "OK"}


if __name__ == "__main__":
    print("=== Test 1: Successful Call ===")
    res1 = fetch_api_data(101)
    print(f"Successful Fetch: {res1}")

    print("\n=== Test 2: Rate Limit Violation (Rapid calls with limit 3/sec) ===")
    try:
        for i in range(5):
            fetch_api_data(200 + i)
    except RuntimeError as err:
        print(f"Caught Limit Breach: {err}")

    print("\n=== Test 3: Inspect Decorator Instance State ===")
    stats = fetch_api_data.decorator_instance
    print("Decorator State:")
    print(f"- Total Calls Tracked: {stats.total_calls}")
    print(f"- Total Retries Tracked: {stats.total_retries}")
    print(f"- Function Name Preserved: '{fetch_api_data.__name__}'")
    print(f"- Function Doc Preserved: '{fetch_api_data.__doc__}'")

    print("\n=== Test 4: Retry Mechanism with Failure & Recovery ===")
    fail_counter = 0

    @RateLimitedRetry(max_retries=3, max_calls_per_second=10, backoff_base=0.01)
    def flaky_network_call():
        global fail_counter
        fail_counter += 1
        if fail_counter < 3:
            raise ConnectionError(f"Transient network glitch #{fail_counter}")
        return "Connected successfully after retries"

    result = flaky_network_call()
    print(f"Result: {result}")
    print(f"Total Retries Observed: {flaky_network_call.decorator_instance.total_retries}")
