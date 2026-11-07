"""
Phase 6 - Data Structures and Algorithms
Section B: Searching - Topic 02: Binary Search
Example 01: Iterative vs Recursive Binary Search & Halving Trace

Demonstrates:
1. Iterative Binary Search: O(log N) time, O(1) auxiliary space.
2. Recursive Binary Search: O(log N) time, O(log N) call-stack space.
3. Overflow-safe midpoint formula: `mid = low + (high - low) // 2`.
4. Step-by-step halving trace showing how the search window [low, high] shrinks by 50% each step.
"""


def binary_search_iterative(
    arr: list[int], target: int, trace: bool = False
) -> tuple[int, int]:
    """
    Iterative Binary Search on a sorted ascending list.
    Returns (index, comparisons). Returns (-1, comparisons) if not found.
    Time Complexity : O(log N)
    Space Complexity: O(1)
    """
    low = 0
    high = len(arr) - 1
    step = 0

    while low <= high:
        step += 1
        # Overflow-safe midpoint calculation (vital in fixed-width integer languages like C++/Java)
        mid = low + (high - low) // 2
        mid_val = arr[mid]

        if trace:
            window_size = high - low + 1
            print(
                f"  Step {step}: low={low:>2}, high={high:>2} (window={window_size:>2}) "
                f"-> mid={mid:>2} (arr[mid]={mid_val})"
            )

        if mid_val == target:
            return mid, step
        elif mid_val < target:
            # Target must lie in the right half: discard [low .. mid]
            low = mid + 1
        else:
            # Target must lie in the left half: discard [mid .. high]
            high = mid - 1

    return -1, step


def binary_search_recursive(
    arr: list[int], target: int, low: int, high: int, depth: int = 1
) -> tuple[int, int]:
    """
    Recursive Binary Search on `arr[low .. high]`.
    Returns (index, max_recursion_depth).
    Time Complexity : O(log N)
    Space Complexity: O(log N) call-stack frames
    """
    if low > high:
        return -1, depth - 1

    mid = low + (high - low) // 2
    if arr[mid] == target:
        return mid, depth
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, high, depth + 1)
    else:
        return binary_search_recursive(arr, target, low, mid - 1, depth + 1)


if __name__ == "__main__":
    sorted_timestamps = [
        105, 112, 128, 144, 159, 173, 188, 204,
        219, 235, 250, 268, 281, 297, 310, 325,
    ]
    print("=" * 72)
    print("1. STEP-BY-STEP BINARY SEARCH HALVING TRACE (N = 16)")
    print("=" * 72)
    print(f"Sorted Array: {sorted_timestamps}\n")

    print("Tracing search for target = 281 (Present at index 12):")
    idx, steps = binary_search_iterative(sorted_timestamps, 281, trace=True)
    print(f"-> Result: Found at index {idx} in {steps} steps (log2(16) = 4)\n")

    print("Tracing search for target = 190 (Missing element):")
    idx_miss, steps_miss = binary_search_iterative(sorted_timestamps, 190, trace=True)
    print(f"-> Result: Not found ({idx_miss}) after {steps_miss} steps")

    print("\n" + "=" * 72)
    print("2. ITERATIVE O(1) SPACE vs RECURSIVE O(log N) STACK SPACE")
    print("=" * 72)
    for query in [105, 204, 325, 999]:
        i_idx, i_steps = binary_search_iterative(sorted_timestamps, query)
        r_idx, r_depth = binary_search_recursive(
            sorted_timestamps, query, 0, len(sorted_timestamps) - 1
        )
        assert i_idx == r_idx
        print(
            f"Query {query:>3} -> Index: {i_idx:>2} | "
            f"Iterative Steps: {i_steps} | Recursive Stack Depth: {r_depth}"
        )
