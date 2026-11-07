"""
Phase 6 - Data Structures and Algorithms
Section B: Searching - Topic 01: Linear Search
Example 02: Multi-Occurrence Search, 2D Matrix Search, and Min/Max Scan

Demonstrates:
1. Finding all indices where a target occurs (handling duplicates).
2. Searching an unsorted 2D matrix (row-by-row linear traversal in O(R * C) time).
3. Finding both Minimum and Maximum in a single linear pass using pairwise comparisons.
"""


def find_all_occurrences(arr: list[str], target: str) -> list[int]:
    """Return a list of all 0-based indices where target appears in arr."""
    matching_indices: list[int] = []
    for index, value in enumerate(arr):
        if value == target:
            matching_indices.append(index)
    return matching_indices


def search_2d_unsorted_matrix(
    matrix: list[list[int]], target: int
) -> tuple[int, int] | None:
    """
    Search an unsorted 2D grid of R rows and C columns.
    Time Complexity : O(R * C)
    Space Complexity: O(1) auxiliary space
    """
    for row_idx, row in enumerate(matrix):
        for col_idx, cell_value in enumerate(row):
            if cell_value == target:
                return (row_idx, col_idx)
    return None


def find_min_and_max_single_pass(arr: list[int]) -> tuple[int, int, int]:
    """
    Find (minimum, maximum, comparisons) in a single O(N) linear scan
    using ~1.5N comparisons by comparing elements in pairs!
    """
    n = len(arr)
    if n == 0:
        raise ValueError("Array must not be empty")

    comparisons = 0
    if n % 2 == 1:
        current_min = current_max = arr[0]
        start_idx = 1
    else:
        comparisons += 1
        if arr[0] < arr[1]:
            current_min, current_max = arr[0], arr[1]
        else:
            current_min, current_max = arr[1], arr[0]
        start_idx = 2

    # Process remaining elements in pairs (3 comparisons per 2 elements = 1.5N)
    for i in range(start_idx, n, 2):
        a, b = arr[i], arr[i + 1]
        comparisons += 1
        if a < b:
            smaller, larger = a, b
        else:
            smaller, larger = b, a

        comparisons += 1
        if smaller < current_min:
            current_min = smaller

        comparisons += 1
        if larger > current_max:
            current_max = larger

    return current_min, current_max, comparisons


if __name__ == "__main__":
    print("=" * 72)
    print("1. FINDING ALL OCCURRENCES OF A TARGET IN LOG STREAM")
    print("=" * 72)
    http_status_stream = ["200", "200", "500", "404", "200", "500", "201", "500"]
    error_indices = find_all_occurrences(http_status_stream, "500")
    print(f"Status Stream       : {http_status_stream}")
    print(f"Indices of '500'    : {error_indices} (Count: {len(error_indices)})")

    print("\n" + "=" * 72)
    print("2. UNSORTED 2D MATRIX LINEAR SEARCH O(R * C)")
    print("=" * 72)
    warehouse_grid = [
        [48, 12, 91, 34],
        [77, 56, 23, 89],
        [15, 64, 42, 70],
    ]
    for query in [23, 42, 99]:
        coords = search_2d_unsorted_matrix(warehouse_grid, query)
        print(f"  Searching for {query:>2} -> Coordinates (row, col): {coords}")

    print("\n" + "=" * 72)
    print("3. PAIRWISE MIN & MAX IN A SINGLE LINEAR SCAN (1.5N COMPARISONS)")
    print("=" * 72)
    readings = [42, 19, 88, 7, 63, 95, 31, 12, 54, 76]
    low, high, comps = find_min_and_max_single_pass(readings)
    naive_comps = 2 * (len(readings) - 1)
    print(f"Readings (n={len(readings)})      : {readings}")
    print(f"Minimum = {low}, Maximum = {high}")
    print(f"Pairwise Comparisons : {comps} (vs {naive_comps} in naive 2*(n-1) scan)")
