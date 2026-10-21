"""
Topic 13: Testing and Debugging
Question 08: Profiling and Timing

A comprehensive, production-grade guide to performance profiling and memory benchmarking
in Python using standard library modules (time, timeit, cProfile, pstats, tracemalloc, sys).
Covers perf_counter vs process_time, timing context managers, timeit micro-benchmarking,
cProfile execution profiling, pstats analysis and sorting, tracemalloc memory snapshot
comparisons, recursive deep object sizing, peak memory tracking, function profiler decorators,
and an architectural Enterprise Benchmark & Latency Percentile Suite.

Every question contains standalone runnable exercises verified with 100% assertions.
"""

import time
import timeit
import cProfile
import pstats
import tracemalloc
import sys
import io
from typing import List, Dict, Any, Callable, Tuple, Optional


# =====================================================================
# Q1: Wall-Clock (perf_counter) vs CPU-Time (process_time)
# =====================================================================
def q1_perf_counter_vs_process_time():
    """
    Demonstrates the fundamental difference between:
    - time.perf_counter(): Wall-clock elapsed time (includes I/O and sleep)
    - time.process_time(): CPU core active time (excludes sleep and idle I/O)
    """
    t0_wall = time.perf_counter()
    t0_cpu = time.process_time()

    # Sleep 0.05 seconds (idle I/O)
    time.sleep(0.05)

    # Perform a light CPU calculation
    total = sum(i * i for i in range(10000))

    elapsed_wall = time.perf_counter() - t0_wall
    elapsed_cpu = time.process_time() - t0_cpu

    # Wall time includes the 50ms sleep
    assert elapsed_wall >= 0.045
    # CPU time ignores sleep! It should be significantly smaller than wall time
    assert elapsed_cpu < elapsed_wall
    assert total > 0

    print("=== Q1: perf_counter vs process_time Verified ===")


# =====================================================================
# Q2: Reusable Timing Context Manager
# =====================================================================
class CodeTimer:
    """Reusable high-resolution timing context manager."""
    def __init__(self, name: str = "block"):
        self.name = name
        self.elapsed: float = 0.0
        self._start: float = 0.0

    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self._start


def q2_timing_context_manager():
    with CodeTimer("list_generation") as timer:
        data = [x * 2 for x in range(50000)]

    assert len(data) == 50000
    assert timer.elapsed > 0.0
    assert timer.name == "list_generation"

    print("=== Q2: Timing Context Manager Verified ===")


# =====================================================================
# Q3: Micro-Benchmarking with timeit
# =====================================================================
def q3_timeit_micro_benchmarks():
    """
    Demonstrates using timeit.timeit to benchmark isolated execution speeds
    (e.g., list comprehension vs map).
    """
    # Benchmarking list comprehension
    stmt_comp = "[x * 2 for x in range(100)]"
    time_comp = timeit.timeit(stmt=stmt_comp, number=1000)

    # Benchmarking map with lambda
    stmt_map = "list(map(lambda x: x * 2, range(100)))"
    time_map = timeit.timeit(stmt=stmt_map, number=1000)

    # Both benchmarks ran 1,000 times successfully and returned positive durations
    assert time_comp > 0.0
    assert time_map > 0.0

    # timeit.repeat runs multiple trials to evaluate stability
    trials = timeit.repeat(stmt="sum(range(50))", repeat=3, number=500)
    assert len(trials) == 3
    assert all(t > 0.0 for t in trials)

    print("=== Q3: Micro-Benchmarking with timeit Verified ===")


# =====================================================================
# Q4: Execution Profiling with cProfile
# =====================================================================
def helper_math(n):
    return sum(i * 2 for i in range(n))


def complex_task():
    for _ in range(5):
        helper_math(5000)


def q4_cprofile_execution_profiling():
    profiler = cProfile.Profile()
    profiler.enable()

    complex_task()

    profiler.disable()

    # Capture stats in memory stream
    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.print_stats()
    profile_text = stream.getvalue()

    # Verify that functions are recorded
    assert "complex_task" in profile_text
    assert "helper_math" in profile_text
    # 5 calls to helper_math
    assert "5" in profile_text

    print("=== Q4: Execution Profiling with cProfile Verified ===")


# =====================================================================
# Q5: Analyzing and Sorting Profiler Statistics with pstats
# =====================================================================
def q5_pstats_sorting_and_filtering():
    profiler = cProfile.Profile()
    profiler.runcall(complex_task)

    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)

    # Sort by cumulative time and limit to top 10 functions
    stats.strip_dirs().sort_stats(pstats.SortKey.CUMULATIVE).print_stats(10)
    output = stream.getvalue()

    assert "cumtime" in output
    assert "complex_task" in output

    print("=== Q5: pstats Sorting and Filtering Verified ===")


# =====================================================================
# Q6: Memory Allocation Tracking with tracemalloc
# =====================================================================
def allocate_data():
    return [f"string_item_{i}" for i in range(10000)]


def q6_tracemalloc_memory_snapshots():
    tracemalloc.start()
    snapshot1 = tracemalloc.take_snapshot()

    # Allocate memory
    data = allocate_data()

    snapshot2 = tracemalloc.take_snapshot()
    tracemalloc.stop()

    # Compare snapshots to see top memory consuming lines
    top_diffs = snapshot2.compare_to(snapshot1, "lineno")
    assert len(top_diffs) > 0

    # The top allocation difference must be positive
    top_diff = top_diffs[0]
    assert top_diff.size_diff > 0
    assert len(data) == 10000

    print("=== Q6: tracemalloc Memory Snapshots Verified ===")


# =====================================================================
# Q7: Recursive Deep Object Sizing
# =====================================================================
def get_deep_sizeof(obj: Any, seen: Optional[set] = None) -> int:
    """
    Recursively computes the true total memory footprint of an object
    including nested mappings, sequences, sets, and cycle prevention.
    """
    if seen is None:
        seen = set()

    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)

    size = sys.getsizeof(obj)

    if isinstance(obj, dict):
        size += sum(get_deep_sizeof(k, seen) + get_deep_sizeof(v, seen) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set, frozenset)):
        size += sum(get_deep_sizeof(item, seen) for item in obj)

    return size


def q7_deep_object_sizing():
    nested_data = {
        "users": [
            {"id": 1, "name": "Alice", "tags": ["admin", "root"]},
            {"id": 2, "name": "Bob", "tags": ["user"]},
        ],
        "meta": {"active": True}
    }

    shallow_size = sys.getsizeof(nested_data)
    deep_size = get_deep_sizeof(nested_data)

    # Shallow size only measures the root dict pointer table
    assert shallow_size > 0
    # Deep size includes strings, nested dicts, lists, and ints
    assert deep_size > shallow_size

    # Cycle detection test
    cyclic_list = [1, 2]
    cyclic_list.append(cyclic_list)
    cyclic_size = get_deep_sizeof(cyclic_list)
    assert cyclic_size > 0  # Did not enter infinite recursion!

    print("=== Q7: Recursive Deep Object Sizing Verified ===")


# =====================================================================
# Q8: Profiler Decorator
# =====================================================================
def profile_function(fn: Callable) -> Callable:
    """Decorator profiling function execution and attaching runtime stats."""
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        try:
            result = fn(*args, **kwargs)
        finally:
            pr.disable()
            s = io.StringIO()
            ps = pstats.Stats(pr, stream=s).sort_stats(pstats.SortKey.CUMULATIVE)
            ps.print_stats()
            wrapper.last_profile_output = s.getvalue()
        return result
    wrapper.last_profile_output = ""
    return wrapper


@profile_function
def compute_cubes(count: int) -> int:
    return sum(x ** 3 for x in range(count))


def q8_profiler_decorator():
    res = compute_cubes(5000)
    assert res > 0
    assert "compute_cubes" in compute_cubes.last_profile_output

    print("=== Q8: Profiler Decorator Verified ===")


# =====================================================================
# Q9: Peak Memory Consumption Comparison (Generators vs Lists)
# =====================================================================
def build_list(n: int) -> List[int]:
    return [i for i in range(n)]


def build_generator(n: int):
    for i in range(n):
        yield i


def q9_peak_memory_tracking():
    # 1. Measure list memory
    tracemalloc.start()
    data_list = build_list(100000)
    _, peak_list = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # 2. Measure generator memory
    tracemalloc.start()
    gen = build_generator(100000)
    first_item = next(gen)
    _, peak_gen = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    assert len(data_list) == 100000
    assert first_item == 0
    # Generator peak memory must be substantially smaller than full list allocation!
    assert peak_gen < peak_list

    print("=== Q9: Peak Memory Tracking (Generators vs Lists) Verified ===")


# =====================================================================
# Q10: Architectural Enterprise Benchmark & Percentile Suite
# =====================================================================
class BenchmarkResult:
    def __init__(self, name: str, timings: List[float], mem_delta_bytes: int):
        self.name = name
        self.timings = sorted(timings)
        self.mem_delta_bytes = mem_delta_bytes

    @property
    def min(self) -> float:
        return round(self.timings[0], 6)

    @property
    def max(self) -> float:
        return round(self.timings[-1], 6)

    @property
    def mean(self) -> float:
        return round(sum(self.timings) / len(self.timings), 6)

    @property
    def p50(self) -> float:
        idx = int(0.50 * len(self.timings))
        return round(self.timings[idx], 6)

    @property
    def p95(self) -> float:
        idx = min(int(0.95 * len(self.timings)), len(self.timings) - 1)
        return round(self.timings[idx], 6)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "runs": len(self.timings),
            "mean_sec": self.mean,
            "min_sec": self.min,
            "p50_sec": self.p50,
            "p95_sec": self.p95,
            "max_sec": self.max,
            "mem_delta_kb": round(self.mem_delta_bytes / 1024, 2)
        }


class BenchmarkSuite:
    """Enterprise performance benchmarking and latency distribution engine."""
    def __init__(self, warmup_runs: int = 2, benchmark_runs: int = 15):
        self.warmup_runs = warmup_runs
        self.benchmark_runs = benchmark_runs

    def run(self, name: str, fn: Callable, *args, **kwargs) -> BenchmarkResult:
        # Warmup phase (JIT/cache priming)
        for _ in range(self.warmup_runs):
            fn(*args, **kwargs)

        timings = []
        tracemalloc.start()
        snap_before = tracemalloc.take_snapshot()

        for _ in range(self.benchmark_runs):
            t0 = time.perf_counter()
            fn(*args, **kwargs)
            t1 = time.perf_counter()
            timings.append(t1 - t0)

        snap_after = tracemalloc.take_snapshot()
        tracemalloc.stop()

        diffs = snap_after.compare_to(snap_before, "lineno")
        total_mem_delta = sum(d.size_diff for d in diffs if d.size_diff > 0)

        return BenchmarkResult(name, timings, total_mem_delta)


def q10_architectural_benchmark_suite():
    suite = BenchmarkSuite(warmup_runs=2, benchmark_runs=20)

    def string_join_algorithm():
        return "".join(str(i) for i in range(500))

    result = suite.run("StringJoinBenchmark", string_join_algorithm)
    data = result.to_dict()

    assert data["name"] == "StringJoinBenchmark"
    assert data["runs"] == 20
    assert data["min_sec"] <= data["p50_sec"] <= data["p95_sec"] <= data["max_sec"]
    assert data["mean_sec"] > 0.0

    print("=== Q10: Architectural Benchmark & Percentile Suite Verified ===")


# =====================================================================
# Main Test Runner
# =====================================================================
if __name__ == "__main__":
    q1_perf_counter_vs_process_time()
    q2_timing_context_manager()
    q3_timeit_micro_benchmarks()
    q4_cprofile_execution_profiling()
    q5_pstats_sorting_and_filtering()
    q6_tracemalloc_memory_snapshots()
    q7_deep_object_sizing()
    q8_profiler_decorator()
    q9_peak_memory_tracking()
    q10_architectural_benchmark_suite()

    print("\nAll 10 profiling and timing practice questions passed successfully!")
