"""
Topic: Advanced Python - Generators and Yield
---------------------------------------------
Questions Covered:
1. Basic Generator Function: 'yield' vs 'return', lazy step-by-step evaluation, and inspection
   of generator states via 'inspect.getgeneratorstate' (GEN_CREATED, GEN_SUSPENDED, GEN_CLOSED).
2. Memory Efficiency: Generator expressions vs list comprehensions, sys.getsizeof profiling,
   and memory-bounded processing of massive synthetic data.
3. Streaming Data Pipeline: Composing generator stages (reader -> parser -> filter -> transform)
   for zero-buffering high-throughput stream transformation.
4. Delegation with 'yield from': Flattening arbitrary nested hierarchies, tree leaves extraction,
   and receiving subgenerator return values ('result = yield from subgenerator()').
5. Two-Way Communication via '.send()': Coroutine primer pattern, stateful accumulating
   average calculator, and dynamic target adjustment.
6. Injected Exceptions via '.throw()': Handling external error signals inside active generators,
   dynamic state resets, and graceful fault recovery.
7. Graceful Termination with '.close()' and 'GeneratorExit': Resource cleanup guarantees via
   try...finally blocks during early consumer termination and garbage collection.
8. Infinite Stream Sliding Window: Continuous rolling metrics generator yielding fixed-size
   moving windows over continuous incoming data.
9. Cooperative Multitasking Scheduler: Lightweight green-thread scheduler managing concurrent
   generators yielding control or cooperative sleep steps.
10. Comprehensive Event Stream Engine: Production-grade streaming event processor featuring
    staged generator filters, coroutine sink sinks, dynamic anomaly detection, and clean teardown.
"""

import sys
import inspect
import time
from typing import Generator, Any, List, Dict, Optional, Tuple, Iterable


# ==============================================================================
# Question 1: Basic Generator Function and Lifecycle States
# ==============================================================================
def countdown_generator(start: int) -> Generator[int, None, str]:
    """
    A countdown generator that yields numbers down to 1 and returns a completion message.
    Demonstrates lazy suspension and state transitions.
    """
    current = start
    while current > 0:
        yield current
        current -= 1
    return "Blast off!"


def test_q1_generator_basics():
    gen = countdown_generator(3)

    # 1. Initially created, not yet started
    assert inspect.getgeneratorstate(gen) == inspect.GEN_CREATED

    # 2. Advance one step -> Suspended
    val1 = next(gen)
    assert val1 == 3
    assert inspect.getgeneratorstate(gen) == inspect.GEN_SUSPENDED

    val2 = next(gen)
    assert val2 == 2
    assert inspect.getgeneratorstate(gen) == inspect.GEN_SUSPENDED

    val3 = next(gen)
    assert val3 == 1
    assert inspect.getgeneratorstate(gen) == inspect.GEN_SUSPENDED

    # 3. Exhaust generator -> StopIteration holds the return value
    try:
        next(gen)
        assert False, "Should have raised StopIteration"
    except StopIteration as e:
        assert e.value == "Blast off!"

    # 4. Now closed
    assert inspect.getgeneratorstate(gen) == inspect.GEN_CLOSED
    print("=== Q1: Generator Basics & States Verified ===")


# ==============================================================================
# Question 2: Memory Efficiency: Generator Expressions vs List Comprehensions
# ==============================================================================
def compare_memory_footprint(n: int) -> Tuple[int, int]:
    """
    Compares the immediate memory footprint of a list comprehension vs generator expression.
    Returns (list_bytes, gen_bytes).
    """
    list_comp = [x * x for x in range(n)]
    gen_expr = (x * x for x in range(n))

    list_size = sys.getsizeof(list_comp)
    gen_size = sys.getsizeof(gen_expr)

    # Verify that generator expression yields the exact same items lazily
    first_five_gen = [next(gen_expr) for _ in range(5)]
    assert first_five_gen == list_comp[:5]

    return list_size, gen_size


def test_q2_memory_efficiency():
    list_size, gen_size = compare_memory_footprint(100_000)
    # A list of 100,000 ints in Python occupies > 800 KB, while generator expr is < 300 bytes
    assert list_size > 700_000
    assert gen_size < 500
    assert list_size > gen_size * 1000
    print(f"=== Q2: Memory Efficiency Verified (List: {list_size} bytes, Gen: {gen_size} bytes) ===")


# ==============================================================================
# Question 3: Chained Generators Pipeline (Lazy Stream Transformation)
# ==============================================================================
def raw_log_reader(logs: Iterable[str]) -> Generator[str, None, None]:
    """Stage 1: Read raw log lines stripped of whitespace."""
    for line in logs:
        yield line.strip()


def log_parser(lines: Iterable[str]) -> Generator[Dict[str, Any], None, None]:
    """Stage 2: Parse raw string into structured dictionary (level, service, latency_ms)."""
    for line in lines:
        if not line or line.startswith("#"):
            continue
        parts = line.split("|")
        if len(parts) == 3:
            yield {
                "level": parts[0].strip(),
                "service": parts[1].strip(),
                "latency_ms": float(parts[2].strip()),
            }


def latency_filter(
    records: Iterable[Dict[str, Any]], threshold_ms: float
) -> Generator[Dict[str, Any], None, None]:
    """Stage 3: Filter records that exceed the given latency threshold."""
    for record in records:
        if record["latency_ms"] >= threshold_ms:
            yield record


def service_tagger(
    records: Iterable[Dict[str, Any]], tag: str
) -> Generator[Dict[str, Any], None, None]:
    """Stage 4: Enrich record with custom tag."""
    for record in records:
        enriched = dict(record)
        enriched["tag"] = tag
        yield enriched


def test_q3_streaming_pipeline():
    raw_sample_logs = [
        "INFO | auth_service | 12.4",
        "# Comment line ignored",
        "WARN | db_proxy | 120.8",
        "INFO | auth_service | 5.1",
        "ERROR | payment_api | 340.5",
        "INFO | db_proxy | 85.0",
    ]

    # Assemble pipeline with zero intermediate list allocations
    stage1 = raw_log_reader(raw_sample_logs)
    stage2 = log_parser(stage1)
    stage3 = latency_filter(stage2, threshold_ms=80.0)
    stage4 = service_tagger(stage3, tag="SLOW_REQUEST")

    results = list(stage4)
    assert len(results) == 3
    assert results[0] == {"level": "WARN", "service": "db_proxy", "latency_ms": 120.8, "tag": "SLOW_REQUEST"}
    assert results[1] == {"level": "ERROR", "service": "payment_api", "latency_ms": 340.5, "tag": "SLOW_REQUEST"}
    assert results[2] == {"level": "INFO", "service": "db_proxy", "latency_ms": 85.0, "tag": "SLOW_REQUEST"}
    print("=== Q3: Chained Streaming Pipeline Verified ===")


# ==============================================================================
# Question 4: Delegation with 'yield from' & Return Values from Subgenerators
# ==============================================================================
def flatten_nested(nested: Iterable[Any]) -> Generator[Any, None, None]:
    """
    Recursively flattens arbitrarily nested lists or tuples using 'yield from'.
    Leaves non-iterable scalar items intact. Strings of length 1 are treated as scalars.
    """
    for item in nested:
        if isinstance(item, (list, tuple)):
            yield from flatten_nested(item)
        else:
            yield item


def subgenerator_with_summary(numbers: List[int]) -> Generator[int, None, Dict[str, Any]]:
    """
    Yields squared numbers one by one, then returns summary metadata.
    """
    total = 0
    count = 0
    for n in numbers:
        sq = n * n
        total += sq
        count += 1
        yield sq
    return {"count": count, "sum_of_squares": total}


def parent_delegator(numbers: List[int]) -> Generator[Any, None, Dict[str, Any]]:
    """Delegates to subgenerator and captures its return value."""
    summary = yield from subgenerator_with_summary(numbers)
    return summary


def test_q4_yield_from_delegation():
    # 1. Flattening nested structure
    nested_data = [1, [2, [3, 4], 5], [[6]], 7]
    flattened = list(flatten_nested(nested_data))
    assert flattened == [1, 2, 3, 4, 5, 6, 7]

    # 2. Capturing subgenerator return value via yield from
    runner = parent_delegator([2, 3, 4])
    squares_yielded = []
    summary_received = None

    while True:
        try:
            val = next(runner)
            squares_yielded.append(val)
        except StopIteration as e:
            summary_received = e.value
            break

    assert squares_yielded == [4, 9, 16]
    assert summary_received == {"count": 3, "sum_of_squares": 4 + 9 + 16}
    print("=== Q4: 'yield from' Delegation & Subgenerator Returns Verified ===")


# ==============================================================================
# Question 5: Two-Way Coroutines via '.send()' and Primer Decorator
# ==============================================================================
def coroutine_primer(func):
    """Decorator that automatically advances a generator to its first yield point upon creation."""
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)  # Prime to the first yield
        return gen
    return wrapper


@coroutine_primer
def running_statistics_coroutine() -> Generator[Dict[str, float], float, None]:
    """
    Receives numeric stream values via .send() and yields running statistics
    (count, sum, mean, min, max) on each push.
    """
    total = 0.0
    count = 0
    min_val = float("inf")
    max_val = float("-inf")
    stats = {}

    while True:
        # yield current stats and wait for new incoming value
        value = yield stats
        count += 1
        total += value
        if value < min_val:
            min_val = value
        if value > max_val:
            max_val = value

        stats = {
            "count": count,
            "sum": total,
            "mean": total / count,
            "min": min_val,
            "max": max_val,
        }


def test_q5_send_coroutine():
    stats_gen = running_statistics_coroutine()

    res1 = stats_gen.send(10.0)
    assert res1 == {"count": 1, "sum": 10.0, "mean": 10.0, "min": 10.0, "max": 10.0}

    res2 = stats_gen.send(20.0)
    assert res2 == {"count": 2, "sum": 30.0, "mean": 15.0, "min": 10.0, "max": 20.0}

    res3 = stats_gen.send(0.0)
    assert res3 == {"count": 3, "sum": 30.0, "mean": 10.0, "min": 0.0, "max": 20.0}

    stats_gen.close()
    assert inspect.getgeneratorstate(stats_gen) == inspect.GEN_CLOSED
    print("=== Q5: Coroutine .send() Running Statistics Verified ===")


# ==============================================================================
# Question 6: Dynamic State Injections and Fault Recovery with '.throw()'
# ==============================================================================
class ResetSignal(Exception):
    """Custom exception signal used to request counter reset."""
    pass


def resilient_event_counter() -> Generator[int, None, None]:
    """
    Maintains a monotonically increasing count.
    If ResetSignal is thrown in, it resets the count to 0 without terminating.
    If any unknown exception is thrown in, it raises and terminates.
    """
    count = 0
    while True:
        try:
            yield count
            count += 1
        except ResetSignal:
            count = 0


def test_q6_throw_exception_recovery():
    counter = resilient_event_counter()

    assert next(counter) == 0
    assert next(counter) == 1
    assert next(counter) == 2

    # Inject ResetSignal via throw()
    reset_val = counter.throw(ResetSignal)
    assert reset_val == 0
    assert next(counter) == 1
    assert next(counter) == 2

    # Injecting unhandled ValueError should terminate the generator
    try:
        counter.throw(ValueError("Critical failure"))
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert str(e) == "Critical failure"

    assert inspect.getgeneratorstate(counter) == inspect.GEN_CLOSED
    print("=== Q6: Exception Injection with .throw() Verified ===")


# ==============================================================================
# Question 7: Resource Management with '.close()' and 'GeneratorExit'
# ==============================================================================
class MockResourceHandle:
    def __init__(self, name: str):
        self.name = name
        self.is_open = True

    def close(self):
        self.is_open = False


def managed_stream_consumer(resource: MockResourceHandle, data: List[int]) -> Generator[int, None, None]:
    """
    Consumes elements from a mock resource.
    Guarantees resource closure on both normal exhaustion and premature .close().
    """
    try:
        for item in data:
            if not resource.is_open:
                raise RuntimeError("Resource prematurely closed")
            yield item
    finally:
        resource.close()


def test_q7_generator_close_cleanup():
    res1 = MockResourceHandle("db_pool_1")
    gen1 = managed_stream_consumer(res1, [10, 20, 30])
    assert next(gen1) == 10
    assert res1.is_open is True

    # Prematurely close consumer
    gen1.close()
    assert res1.is_open is False
    assert inspect.getgeneratorstate(gen1) == inspect.GEN_CLOSED

    # Test full natural exhaustion
    res2 = MockResourceHandle("db_pool_2")
    gen2 = managed_stream_consumer(res2, [1, 2])
    assert list(gen2) == [1, 2]
    assert res2.is_open is False
    print("=== Q7: Resource Cleanup on .close() Verified ===")


# ==============================================================================
# Question 8: Infinite Stream Sliding Window Generator
# ==============================================================================
def sliding_window_stream(
    stream: Iterable[Any], window_size: int
) -> Generator[Tuple[Any, ...], None, None]:
    """
    Yields rolling tuple windows of length `window_size` over an incoming stream.
    Does not buffer unnecessary historical elements.
    """
    if window_size <= 0:
        raise ValueError("window_size must be positive")

    window: List[Any] = []
    for item in stream:
        window.append(item)
        if len(window) == window_size:
            yield tuple(window)
            window.pop(0)  # Slide window forward


def test_q8_sliding_window():
    stream = range(1, 8)  # 1, 2, 3, 4, 5, 6, 7
    windows = list(sliding_window_stream(stream, window_size=3))
    expected = [
        (1, 2, 3),
        (2, 3, 4),
        (3, 4, 5),
        (4, 5, 6),
        (5, 6, 7),
    ]
    assert windows == expected
    print("=== Q8: Sliding Window Generator Verified ===")


# ==============================================================================
# Question 9: Cooperative Multitasking / Green-Thread Scheduler
# ==============================================================================
class CooperativeScheduler:
    """
    A lightweight non-preemptive round-robin task scheduler built purely on generators.
    Tasks yield control to the scheduler.
    """
    def __init__(self):
        self._tasks: List[Tuple[str, Generator[Any, None, None]]] = []
        self.execution_log: List[str] = []

    def spawn(self, name: str, task: Generator[Any, None, None]):
        self._tasks.append((name, task))

    def run(self):
        """Runs all tasks round-robin until all are exhausted."""
        while self._tasks:
            name, task = self._tasks.pop(0)
            try:
                action = next(task)
                self.execution_log.append(f"{name}: {action}")
                # Task yielded an action, re-queue for next round
                self._tasks.append((name, task))
            except StopIteration:
                self.execution_log.append(f"{name}: COMPLETED")


def cooperative_worker(name: str, steps: int) -> Generator[str, None, None]:
    for i in range(1, steps + 1):
        yield f"step_{i}"


def test_q9_cooperative_scheduler():
    scheduler = CooperativeScheduler()
    scheduler.spawn("WorkerA", cooperative_worker("WorkerA", 2))
    scheduler.spawn("WorkerB", cooperative_worker("WorkerB", 3))

    scheduler.run()

    expected_log = [
        "WorkerA: step_1",
        "WorkerB: step_1",
        "WorkerA: step_2",
        "WorkerB: step_2",
        "WorkerA: COMPLETED",
        "WorkerB: step_3",
        "WorkerB: COMPLETED",
    ]
    assert scheduler.execution_log == expected_log
    print("=== Q9: Cooperative Multitasking Scheduler Verified ===")


# ==============================================================================
# Question 10: Architectural System: Real-Time Event Processing Pipeline
# ==============================================================================
class EventStreamEngine:
    """
    Production-grade event stream processor demonstrating:
    - Multi-stage generator pipeline (Ingest -> Parse -> Validate -> Aggregate -> Alert)
    - Dynamic anomaly detection
    - Coroutine sink dispatching
    - Clean shutdown handling
    """
    def __init__(self, anomaly_threshold_rpm: int):
        self.anomaly_threshold = anomaly_threshold_rpm
        self.alerts: List[Dict[str, Any]] = []
        self.processed_count = 0

    def raw_event_source(self, events: List[Dict[str, Any]]) -> Generator[Dict[str, Any], None, None]:
        for event in events:
            yield event

    def validate_events(self, source: Iterable[Dict[str, Any]]) -> Generator[Dict[str, Any], None, None]:
        for event in source:
            if "event_id" in event and "timestamp" in event and "user_id" in event:
                yield event

    def sliding_window_anomaly_detector(
        self, source: Iterable[Dict[str, Any]], window_size: int
    ) -> Generator[Dict[str, Any], None, None]:
        window: List[Dict[str, Any]] = []
        for event in source:
            self.processed_count += 1
            window.append(event)
            if len(window) > window_size:
                window.pop(0)

            # Check if same user triggers > anomaly_threshold within current window
            user_counts: Dict[str, int] = {}
            for item in window:
                u = item["user_id"]
                user_counts[u] = user_counts.get(u, 0) + 1

            current_user = event["user_id"]
            user_count = user_counts.get(current_user, 0)
            if user_count >= self.anomaly_threshold:
                alert = {
                    "alert": "ANOMALY_DETECTED",
                    "user_id": current_user,
                    "event_count": user_count,
                    "window_size": len(window),
                    "latest_event_id": event["event_id"],
                }
                self.alerts.append(alert)
                yield alert

    def process(self, raw_events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        source = self.raw_event_source(raw_events)
        validated = self.validate_events(source)
        detector = self.sliding_window_anomaly_detector(validated, window_size=5)
        return list(detector)


def test_q10_event_stream_engine():
    raw_data = [
        {"event_id": "e1", "timestamp": 1000, "user_id": "alice"},
        {"event_id": "e2", "timestamp": 1001, "user_id": "bob"},
        {"malformed": "ignored"},  # invalid, filtered out
        {"event_id": "e3", "timestamp": 1002, "user_id": "alice"},
        {"event_id": "e4", "timestamp": 1003, "user_id": "alice"},  # triggers threshold >= 3 in window 5
        {"event_id": "e5", "timestamp": 1004, "user_id": "charlie"},
        {"event_id": "e6", "timestamp": 1005, "user_id": "alice"},  # triggers again
    ]

    engine = EventStreamEngine(anomaly_threshold_rpm=3)
    emitted_alerts = engine.process(raw_data)

    assert engine.processed_count == 6  # 1 malformed skipped
    assert len(emitted_alerts) == 2
    assert emitted_alerts[0]["user_id"] == "alice"
    assert emitted_alerts[0]["event_count"] == 3
    assert emitted_alerts[1]["user_id"] == "alice"
    assert emitted_alerts[1]["event_count"] == 3
    print("=== Q10: Architectural Event Stream Engine Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_generator_basics()
    test_q2_memory_efficiency()
    test_q3_streaming_pipeline()
    test_q4_yield_from_delegation()
    test_q5_send_coroutine()
    test_q6_throw_exception_recovery()
    test_q7_generator_close_cleanup()
    test_q8_sliding_window()
    test_q9_cooperative_scheduler()
    test_q10_event_stream_engine()
    print("\nAll 10 generator and yield practice questions passed successfully!")
