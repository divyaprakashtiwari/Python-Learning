"""
Topic 13: Testing & Debugging - Question 8: Performance Profiling Suite
Demonstrating microbenchmarking and deterministic hotspot profiling using
standard library cProfile, pstats, timeit, and high-resolution timing contexts.
"""

from contextlib import contextmanager
import cProfile
import pstats
import statistics
import time
from typing import Any, Callable, Dict, Iterator, List, Tuple


# ==========================================
# Benchmark Workloads
# ==========================================
def dedup_naive(items: List[str]) -> List[str]:
    """O(N^2) naive deduplication using membership lookup on growing result list."""
    seen: List[str] = []
    for item in items:
        if item not in seen:
            seen.append(item)
    return seen


def dedup_optimal(items: List[str]) -> List[str]:
    """O(N) optimal deduplication preserving insertion order via dict keys."""
    return list(dict.fromkeys(items))


# ==========================================
# High-Resolution Context Manager
# ==========================================
@contextmanager
def timing_context(label: str) -> Iterator[Dict[str, float]]:
    """Context manager for high-precision elapsed time measurement in microseconds."""
    stats = {"elapsed_us": 0.0, "elapsed_ms": 0.0}
    start_ns = time.perf_counter_ns()
    try:
        yield stats
    finally:
        end_ns = time.perf_counter_ns()
        elapsed_ns = end_ns - start_ns
        stats["elapsed_us"] = elapsed_ns / 1_000.0
        stats["elapsed_ms"] = elapsed_ns / 1_000_000.0


# ==========================================
# Performance Analyzer
# ==========================================
class PerformanceAnalyzer:
    """Orchestrates statistical microbenchmarking and cProfile hotspot diagnosis."""

    def benchmark_timeit(
        self,
        func: Callable[..., Any],
        *args: Any,
        number: int = 10,
        repeat: int = 5
    ) -> Dict[str, float]:
        """
        Executes repetitions with monotonic perf_counter clock.
        Computes minimum, mean, and standard deviation per invocation.
        """
        per_call_times: List[float] = []

        for _ in range(repeat):
            start = time.perf_counter()
            for _ in range(number):
                func(*args)
            total_duration = time.perf_counter() - start
            per_call_times.append(total_duration / number)

        min_time = min(per_call_times)
        mean_time = statistics.mean(per_call_times)
        stdev_time = statistics.stdev(per_call_times) if len(per_call_times) > 1 else 0.0

        return {
            "min_sec": min_time,
            "mean_sec": mean_time,
            "stdev_sec": stdev_time,
            "mean_ms": mean_time * 1000.0,
        }

    def profile_execution(
        self,
        func: Callable[..., Any],
        *args: Any,
        **kwargs: Any
    ) -> pstats.Stats:
        """Runs function under cProfile and returns compiled pstats.Stats object."""
        profiler = cProfile.Profile()
        profiler.enable()
        try:
            func(*args, **kwargs)
        finally:
            profiler.disable()
        return pstats.Stats(profiler)

    def analyze_hotspots(
        self,
        stats: pstats.Stats,
        top_n: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Extracts top_n expensive function bottlenecks sorted by cumulative time.
        Computes call counts, total time, cumulative time, and percentage contribution.
        """
        records: List[Dict[str, Any]] = []
        total_runtime = sum(stat[2] for stat in stats.stats.values()) or 1e-9

        for (filename, lineno, func_name), (cc, nc, tottime, cumtime, callers) in stats.stats.items():
            clean_name = func_name
            if "append" in func_name:
                clean_name = "list.append"

            pct = (tottime / total_runtime) * 100.0
            records.append({
                "function": clean_name,
                "calls": nc,
                "tottime": tottime,
                "cumtime": cumtime,
                "pct_workload": pct,
            })

        # Sort descending by cumulative time
        records.sort(key=lambda r: r["cumtime"], reverse=True)
        return records[:top_n]


# ==========================================
# Driver Execution
# ==========================================
if __name__ == "__main__":
    analyzer = PerformanceAnalyzer()

    # Generate synthetic workload: 5,000 items with heavy duplication (50 distinct items)
    dataset = [f"item_{i % 50}" for i in range(5000)]

    # 1. Microbenchmark comparison
    naive_res = analyzer.benchmark_timeit(dedup_naive, dataset, number=10)
    optimal_res = analyzer.benchmark_timeit(dedup_optimal, dataset, number=10)

    speedup = max(1.0, naive_res["mean_sec"] / max(1e-9, optimal_res["mean_sec"]))

    # 2. cProfile hotspot analysis
    stats = analyzer.profile_execution(dedup_naive, dataset)
    hotspots = analyzer.analyze_hotspots(stats, top_n=3)

    print("Microbenchmark Results (Mean time for 10 runs):")
    print(f"- dedup_naive (O(N^2)): ~{naive_res['mean_ms']:.2f} ms")
    print(f"- dedup_optimal (O(N)): ~{optimal_res['mean_ms']:.2f} ms")
    print(f"Speedup Factor: ~{int(round(speedup))}x")

    print("Top Bottlenecks Identified in dedup_naive:")
    rank = 1
    for h in hotspots:
        if "disable" in h["function"]:
            continue
        if h["function"] == "list.append":
            print(f"{rank}. `{h['function']}`: {h['calls']} calls, cumtime: {h['cumtime']:.4f}s")
            rank += 1
        elif "dedup_naive" in h["function"]:
            print(f"{rank}. `dedup_naive`: {h['calls']} call, tottime: {h['tottime']:.4f}s (accounts for {h['pct_workload']:.1f}% of workload)")
            rank += 1
