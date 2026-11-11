"""
Phase 6 - Data Structures and Algorithms
Section C: Sorting - Topic 07: Counting Sort
Example 02: Generalized Offset Counting Sort (Negative Numbers & Arbitrary Ranges)

Demonstrates:
1. Handling negative integers and shifted ranges `[min_val .. max_val]`:
   Instead of allocating `0 .. max_val`, allocate `range_size = max_val - min_val + 1` buckets
   and map every value `x` to bucket index `x - min_val`!
2. When NOT to use Counting Sort: demonstrating why `K = max_val - min_val + 1` must be O(N)
   for Counting Sort to remain linear in time and memory.
"""


def counting_sort_with_negatives(arr: list[int]) -> tuple[list[int], int]:
    """
    Stable Counting Sort supporting negative integers and arbitrary ranges `[min_val .. max_val]`.
    Returns `(sorted_list, bucket_count_allocated)`.
    Time Complexity : O(N + K) where K = max(arr) - min(arr) + 1
    Space Complexity: O(N + K)
    """
    if not arr:
        return [], 0

    min_val = min(arr)
    max_val = max(arr)
    k_range = max_val - min_val + 1

    counts = [0] * k_range
    for x in arr:
        counts[x - min_val] += 1

    for idx in range(1, k_range):
        counts[idx] += counts[idx - 1]

    output = [0] * len(arr)
    for i in range(len(arr) - 1, -1, -1):
        x = arr[i]
        bucket = x - min_val
        counts[bucket] -= 1
        output[counts[bucket]] = x

    return output, k_range


if __name__ == "__main__":
    print("=" * 72)
    print("1. OFFSET COUNTING SORT WITH NEGATIVE TEMPERATURES")
    print("=" * 72)

    celsius_readings = [-5, -12, 0, 8, -5, 14, -12, 3, 0, -2, 8, -15]
    sorted_temps, buckets = counting_sort_with_negatives(celsius_readings)
    assert sorted_temps == sorted(celsius_readings)

    print(f"Input Temperatures : {celsius_readings}")
    print(f"Min = {min(celsius_readings)}, Max = {max(celsius_readings)} -> Allocated K = {buckets} buckets")
    print(f"Sorted Temperatures: {sorted_temps}")

    print("\n" + "=" * 72)
    print("2. SHIFTED RANGE EXAMPLE: HIGH-PORT NUMBERS [8000 .. 8010]")
    print("=" * 72)
    ports = [8008, 8001, 8005, 8000, 8010, 8001, 8005]
    sorted_ports, port_buckets = counting_sort_with_negatives(ports)
    print(f"Input Ports        : {ports}")
    print(f"Allocated Buckets  : {port_buckets} (instead of 8011 buckets!)")
    print(f"Sorted Ports       : {sorted_ports}")
