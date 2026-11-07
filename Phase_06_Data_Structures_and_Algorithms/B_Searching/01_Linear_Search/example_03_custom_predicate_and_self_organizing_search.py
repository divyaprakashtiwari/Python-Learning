"""
Phase 6 - Data Structures and Algorithms
Section B: Searching - Topic 01: Linear Search
Example 03: Custom Predicate Search & Self-Organizing Search (Move-to-Front / Transposition)

Demonstrates:
1. Predicate-based Linear Search (`find_first_matching`) on structured records/dataclasses.
2. Self-Organizing Linear Search heuristics for skewed access patterns (80/20 Pareto rule):
   - Move-To-Front (MTF): moves accessed item to index 0 so repeated queries take O(1).
   - Transposition: swaps accessed item one position closer to the front.
"""

from dataclasses import dataclass
from typing import Callable, TypeVar

T = TypeVar("T")


@dataclass
class ServerProcess:
    pid: int
    name: str
    cpu_percent: float
    status: str


def find_first_matching(
    items: list[T], predicate: Callable[[T], bool]
) -> tuple[int, T | None]:
    """
    Generic Linear Search accepting a boolean predicate function.
    Returns (index, item) of the first element satisfying `predicate(item)`.
    """
    for idx, item in enumerate(items):
        if predicate(item):
            return idx, item
    return -1, None


def move_to_front_search(arr: list[str], target: str) -> tuple[int, int]:
    """
    Linear search with Move-To-Front (MTF) heuristic:
    When `target` is found at index `i`, move it to index 0 so future searches
    for hot items finish immediately in 1 comparison!
    Returns (found_index_before_move, comparisons).
    """
    for i, val in enumerate(arr):
        if val == target:
            if i > 0:
                # Pop from i and insert at front (index 0)
                item = arr.pop(i)
                arr.insert(0, item)
            return i, i + 1
    return -1, len(arr)


if __name__ == "__main__":
    print("=" * 72)
    print("1. PREDICATE-BASED LINEAR SEARCH ON OBJECT RECORDS")
    print("=" * 72)

    processes = [
        ServerProcess(1012, "nginx", 4.2, "running"),
        ServerProcess(1045, "postgres", 18.7, "running"),
        ServerProcess(1089, "worker_etl", 92.4, "running"),
        ServerProcess(1104, "redis", 2.1, "sleeping"),
    ]

    # Search for first runaway process using > 80% CPU
    idx, proc = find_first_matching(processes, lambda p: p.cpu_percent > 80.0)
    print(f"First high-CPU process (>80%): Index {idx} -> {proc}")

    # Search for sleeping service
    idx_slp, proc_slp = find_first_matching(processes, lambda p: p.status == "sleeping")
    print(f"First sleeping process       : Index {idx_slp} -> {proc_slp}")

    print("\n" + "=" * 72)
    print("2. SELF-ORGANIZING LINEAR SEARCH (MOVE-TO-FRONT CACHE HEURISTIC)")
    print("=" * 72)

    config_keys = ["theme", "locale", "timezone", "api_timeout", "feature_flag_x"]
    queries = ["feature_flag_x", "feature_flag_x", "api_timeout", "feature_flag_x"]

    print(f"Initial List : {config_keys}")
    total_comps = 0
    for step, q in enumerate(queries, start=1):
        found_at, comps = move_to_front_search(config_keys, q)
        total_comps += comps
        print(
            f"  Query {step}: '{q:<14}' found at idx {found_at} "
            f"({comps} comps) -> Updated List: {config_keys}"
        )
    print(f"Total comparisons across {len(queries)} queries with MTF: {total_comps} (vs 19 without MTF)")
