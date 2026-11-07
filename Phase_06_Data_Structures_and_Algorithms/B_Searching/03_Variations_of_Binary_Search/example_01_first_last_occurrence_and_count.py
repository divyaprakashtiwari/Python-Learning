"""
Phase 6 - Data Structures and Algorithms
Section B: Searching - Topic 03: Variations of Binary Search
Example 01: First Occurrence, Last Occurrence, and Frequency Count in O(log N)

Demonstrates:
1. Finding the First (Leftmost) Occurrence of a duplicate target in a sorted array.
2. Finding the Last (Rightmost) Occurrence of a duplicate target in a sorted array.
3. Counting total occurrences of a target in O(log N) time (`last - first + 1`)
   instead of scanning linearly after a standard binary search hit.
"""


def find_first_occurrence(arr: list[int], target: int) -> int:
    """
    Return the lowest (leftmost) index `i` where `arr[i] == target`, or -1 if absent.
    Key modification: when `arr[mid] == target`, record `result = mid` and keep
    searching the LEFT half (`high = mid - 1`) to see if an earlier copy exists!
    Time Complexity: O(log N)
    """
    low = 0
    high = len(arr) - 1
    first_idx = -1

    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            first_idx = mid
            high = mid - 1  # Continue searching left!
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return first_idx


def find_last_occurrence(arr: list[int], target: int) -> int:
    """
    Return the highest (rightmost) index `i` where `arr[i] == target`, or -1 if absent.
    Key modification: when `arr[mid] == target`, record `result = mid` and keep
    searching the RIGHT half (`low = mid + 1`) to see if a later copy exists!
    Time Complexity: O(log N)
    """
    low = 0
    high = len(arr) - 1
    last_idx = -1

    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            last_idx = mid
            low = mid + 1  # Continue searching right!
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return last_idx


def count_occurrences_log_n(arr: list[int], target: int) -> tuple[int, int, int]:
    """
    Return (count, first_index, last_index) of `target` in sorted `arr` in O(log N) time.
    """
    first = find_first_occurrence(arr, target)
    if first == -1:
        return 0, -1, -1
    last = find_last_occurrence(arr, target)
    return (last - first + 1), first, last


if __name__ == "__main__":
    print("=" * 72)
    print("1. FIRST & LAST OCCURRENCE + O(log N) FREQUENCY COUNT")
    print("=" * 72)

    sorted_latencies = [10, 15, 20, 20, 20, 20, 20, 35, 35, 50, 80]
    print(f"Sorted Array (n={len(sorted_latencies)}): {sorted_latencies}")
    print(f"Indices                 : {list(range(len(sorted_latencies)))}\n")

    for target in [20, 35, 10, 99]:
        count, first_i, last_i = count_occurrences_log_n(sorted_latencies, target)
        print(
            f"  Target {target:>2} -> First Idx: {first_i:>2} | "
            f"Last Idx: {last_i:>2} | Total Count: {count}"
        )
