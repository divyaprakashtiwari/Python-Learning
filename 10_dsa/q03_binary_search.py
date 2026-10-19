"""
Topic: Data Structures and Algorithms (DSA) - Binary Search
-----------------------------------------------------------
Questions Covered:
1. Standard Iterative & Recursive Binary Search: Exact target match with overflow-safe midpoint.
2. Lower Bound (First Occurrence / bisect_left): Finding the first index satisfying val >= target.
3. Upper Bound (Right Insertion / bisect_right): Finding the first index satisfying val > target.
4. Search in Rotated Sorted Array: Identifying sorted halves to locate target in O(log n).
5. Find Minimum in Rotated Sorted Array: Locating inflection/pivot point in rotated arrays.
6. Search in 2D Row-Column Sorted Matrix: Virtual 1D flattening for O(log(m*n)) search.
7. Binary Search on Answer (Square Root): Computing integer and high-precision floating square roots.
8. Monotonic Predicate Optimization (Capacity to Ship Packages): Binary search on answer space.
9. Find Peak Element: Logarithmic peak finding in arrays using slope comparison.
10. Architectural System: Timestamp Range Index & Log Query Engine with binary search slicing.
"""

from typing import List, Tuple, Optional, Any, Dict


# ==============================================================================
# Question 1: Standard Iterative and Recursive Binary Search
# ==============================================================================
def binary_search_iterative(arr: List[int], target: int) -> int:
    """
    Finds exact index of target in sorted arr, or returns -1.
    Time Complexity: O(log n), Space Complexity: O(1).
    """
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def binary_search_recursive(arr: List[int], target: int, left: int = 0, right: Optional[int] = None) -> int:
    """Recursive binary search formulation."""
    if right is None:
        right = len(arr) - 1

    if left > right:
        return -1

    mid = left + (right - left) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)


def test_q1_standard_binary_search():
    data = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    assert binary_search_iterative(data, 23) == 5
    assert binary_search_iterative(data, 2) == 0
    assert binary_search_iterative(data, 91) == 9
    assert binary_search_iterative(data, 50) == -1

    assert binary_search_recursive(data, 23) == 5
    assert binary_search_recursive(data, 50) == -1
    print("=== Q1: Standard Binary Search (Iterative & Recursive) Verified ===")


# ==============================================================================
# Question 2: Lower Bound (bisect_left / First Occurrence)
# ==============================================================================
def lower_bound(arr: List[int], target: int) -> int:
    """
    Returns the index of the first element in arr that is >= target.
    If all elements are < target, returns len(arr).
    Equivalent to bisect.bisect_left.
    """
    left = 0
    right = len(arr)

    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] >= target:
            right = mid
        else:
            left = mid + 1

    return left


def test_q2_lower_bound():
    data = [1, 2, 4, 4, 4, 6, 8]
    # First index of 4 is index 2
    assert lower_bound(data, 4) == 2
    # Value 5 is not present; first element >= 5 is 6 at index 5
    assert lower_bound(data, 5) == 5
    # Value 0 is smaller than all; insertion at index 0
    assert lower_bound(data, 0) == 0
    # Value 10 is greater than all; returns len(data) = 7
    assert lower_bound(data, 10) == 7
    print("=== Q2: Lower Bound (First Occurrence) Verified ===")


# ==============================================================================
# Question 3: Upper Bound (bisect_right / Right Insertion)
# ==============================================================================
def upper_bound(arr: List[int], target: int) -> int:
    """
    Returns the index of the first element in arr that is > target.
    If all elements are <= target, returns len(arr).
    Equivalent to bisect.bisect_right.
    """
    left = 0
    right = len(arr)

    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] > target:
            right = mid
        else:
            left = mid + 1

    return left


def count_occurrences(arr: List[int], target: int) -> int:
    """Counts occurrences of target in sorted arr in O(log n) time using lower & upper bounds."""
    return upper_bound(arr, target) - lower_bound(arr, target)


def test_q3_upper_bound_and_count():
    data = [1, 2, 4, 4, 4, 6, 8]
    # First element > 4 is 6 at index 5
    assert upper_bound(data, 4) == 5
    # Occurrences of 4 = upper_bound(4) - lower_bound(4) = 5 - 2 = 3
    assert count_occurrences(data, 4) == 3
    assert count_occurrences(data, 7) == 0
    assert count_occurrences(data, 8) == 1
    print("=== Q3: Upper Bound & Frequency Counting Verified ===")


# ==============================================================================
# Question 4: Search in Rotated Sorted Array
# ==============================================================================
def search_rotated_sorted(nums: List[int], target: int) -> int:
    """
    Searches for target in a rotated sorted array of unique integers in O(log n).
    Returns index of target, or -1 if not found.
    """
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid

        # Check if left half is normally sorted
        if nums[left] <= nums[mid]:
            # Target lies in sorted left half
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            # Right half is normally sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1


def test_q4_search_rotated_sorted():
    nums = [4, 5, 6, 7, 0, 1, 2]
    assert search_rotated_sorted(nums, 0) == 4
    assert search_rotated_sorted(nums, 3) == -1
    assert search_rotated_sorted(nums, 4) == 0
    assert search_rotated_sorted(nums, 2) == 6
    print("=== Q4: Search in Rotated Sorted Array Verified ===")


# ==============================================================================
# Question 5: Find Minimum in Rotated Sorted Array
# ==============================================================================
def find_min_rotated_sorted(nums: List[int]) -> int:
    """
    Finds minimum element in a rotated sorted array of unique integers in O(log n).
    """
    left = 0
    right = len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2
        # If mid element is greater than rightmost element, min lies in right half
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            # Min lies at mid or to the left of mid
            right = mid

    return nums[left]


def test_q5_find_min_rotated():
    assert find_min_rotated_sorted([3, 4, 5, 1, 2]) == 1
    assert find_min_rotated_sorted([4, 5, 6, 7, 0, 1, 2]) == 0
    assert find_min_rotated_sorted([11, 13, 15, 17]) == 11
    assert find_min_rotated_sorted([2, 1]) == 1
    print("=== Q5: Find Minimum in Rotated Sorted Array Verified ===")


# ==============================================================================
# Question 6: Search in a 2D Row-Column Sorted Matrix
# ==============================================================================
def search_2d_matrix(matrix: List[List[int]], target: int) -> bool:
    """
    Searches an m x n matrix where:
    - Integers in each row are sorted from left to right.
    - First integer of each row is greater than the last integer of the previous row.
    Treats matrix as flattened virtual 1D array of size m * n.
    Time Complexity: O(log(m * n)).
    """
    if not matrix or not matrix[0]:
        return False

    rows = len(matrix)
    cols = len(matrix[0])
    left = 0
    right = rows * cols - 1

    while left <= right:
        mid = left + (right - left) // 2
        row = mid // cols
        col = mid % cols
        mid_val = matrix[row][col]

        if mid_val == target:
            return True
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1

    return False


def test_q6_search_2d_matrix():
    mat = [
        [1, 3, 5, 7],
        [10, 11, 16, 20],
        [23, 30, 34, 60],
    ]
    assert search_2d_matrix(mat, 3) is True
    assert search_2d_matrix(mat, 16) is True
    assert search_2d_matrix(mat, 13) is False
    assert search_2d_matrix(mat, 0) is False
    assert search_2d_matrix(mat, 100) is False
    print("=== Q6: Search in 2D Matrix Verified ===")


# ==============================================================================
# Question 7: Binary Search on Answer (Square Root Calculation)
# ==============================================================================
def integer_square_root(x: int) -> int:
    """Computes integer square root floor(sqrt(x)) in O(log x)."""
    if x < 2:
        return x

    left = 1
    right = x // 2
    ans = 1

    while left <= right:
        mid = left + (right - left) // 2
        sq = mid * mid
        if sq == x:
            return mid
        elif sq < x:
            ans = mid
            left = mid + 1
        else:
            right = mid - 1

    return ans


def float_square_root(x: float, precision: float = 1e-7) -> float:
    """Computes floating-point square root using binary search on real numbers."""
    if x < 0:
        raise ValueError("Cannot take square root of negative number")
    if x == 0:
        return 0.0

    left = 0.0
    right = max(1.0, x)

    while (right - left) > precision:
        mid = left + (right - left) / 2.0
        if mid * mid < x:
            left = mid
        else:
            right = mid

    return (left + right) / 2.0


def test_q7_binary_search_square_root():
    assert integer_square_root(4) == 2
    assert integer_square_root(8) == 2
    assert integer_square_root(16) == 4
    assert integer_square_root(0) == 0
    assert integer_square_root(1) == 1

    flt_res = float_square_root(2.0, precision=1e-6)
    assert abs(flt_res - 1.41421356) < 1e-5
    print("=== Q7: Binary Search on Answer (Square Root) Verified ===")


# ==============================================================================
# Question 8: Monotonic Predicate Optimization (Ship Packages Within D Days)
# ==============================================================================
def ship_within_days(weights: List[int], days: int) -> int:
    """
    Finds minimum ship weight capacity needed to ship all packages in 'days' days.
    Packages must be shipped in given order.
    Answer range: max(weights) to sum(weights).
    """
    def can_ship_with_capacity(capacity: int) -> bool:
        required_days = 1
        current_load = 0
        for w in weights:
            if current_load + w > capacity:
                required_days += 1
                current_load = w
            else:
                current_load += w
        return required_days <= days

    left = max(weights)
    right = sum(weights)
    ans = right

    while left <= right:
        mid = left + (right - left) // 2
        if can_ship_with_capacity(mid):
            ans = mid
            right = mid - 1  # Try smaller capacity
        else:
            left = mid + 1   # Capacity too small, increase

    return ans


def test_q8_ship_within_days():
    weights1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # Min capacity to ship in 5 days is 15
    assert ship_within_days(weights1, 5) == 15

    weights2 = [3, 2, 2, 4, 1, 4]
    assert ship_within_days(weights2, 3) == 6
    print("=== Q8: Monotonic Predicate Optimization (Capacity to Ship) Verified ===")


# ==============================================================================
# Question 9: Find Peak Element
# ==============================================================================
def find_peak_element(nums: List[int]) -> int:
    """
    A peak element is an element strictly greater than its neighbors.
    Finds the index of ANY peak element in O(log n) time.
    Assumes nums[-1] = nums[n] = -inf.
    """
    left = 0
    right = len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2
        # If mid element is smaller than right neighbor, peak must lie to the right
        if nums[mid] < nums[mid + 1]:
            left = mid + 1
        else:
            # Otherwise, peak lies at mid or to the left
            right = mid

    return left


def test_q9_find_peak_element():
    nums1 = [1, 2, 3, 1]
    peak_idx1 = find_peak_element(nums1)
    assert peak_idx1 == 2  # value 3

    nums2 = [1, 2, 1, 3, 5, 6, 4]
    peak_idx2 = find_peak_element(nums2)
    # Valid peaks are index 1 (value 2) or index 5 (value 6)
    assert peak_idx2 in (1, 5)
    print("=== Q9: Find Peak Element Verified ===")


# ==============================================================================
# Question 10: Architectural System: Timestamp Range Query & Log Index Engine
# ==============================================================================
class TimestampLogIndex:
    """
    High-performance in-memory indexed log store with O(log n) time range querying.
    Maintains sorted timestamp array and uses binary search lower/upper bounds
    to slice arbitrary intervals [start_time, end_time].
    """
    def __init__(self):
        self._timestamps: List[int] = []
        self._records: List[Dict[str, Any]] = []

    def insert(self, timestamp: int, payload: Dict[str, Any]) -> None:
        """Inserts record maintaining sorted timestamp order via binary search insertion index."""
        # Find insertion position via upper_bound
        idx = upper_bound(self._timestamps, timestamp)
        self._timestamps.insert(idx, timestamp)
        self._records.insert(idx, payload)

    def query_range(self, start_ts: int, end_ts: int) -> List[Dict[str, Any]]:
        """
        Returns all records where start_ts <= timestamp <= end_ts in O(log n + k) time.
        """
        if not self._timestamps or start_ts > end_ts:
            return []

        # Find first index with ts >= start_ts
        start_idx = lower_bound(self._timestamps, start_ts)
        # Find first index with ts > end_ts
        end_idx = upper_bound(self._timestamps, end_ts)

        return self._records[start_idx:end_idx]


def test_q10_timestamp_log_index():
    index = TimestampLogIndex()

    # Insert out-of-order logs
    index.insert(1050, {"event": "login", "user": "alice"})
    index.insert(1000, {"event": "init", "user": "system"})
    index.insert(1200, {"event": "logout", "user": "alice"})
    index.insert(1100, {"event": "payment", "user": "bob"})
    index.insert(1050, {"event": "page_view", "user": "charlie"})

    # Query range [1050, 1150]
    # Matching timestamps: 1050 (alice), 1050 (charlie), 1100 (bob)
    results = index.query_range(1050, 1150)
    assert len(results) == 3
    assert results[0]["user"] in ("alice", "charlie")
    assert results[1]["user"] in ("alice", "charlie")
    assert results[2]["user"] == "bob"

    # Query empty range
    empty_results = index.query_range(1500, 2000)
    assert empty_results == []
    print("=== Q10: Architectural Timestamp Range Query Engine Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_standard_binary_search()
    test_q2_lower_bound()
    test_q3_upper_bound_and_count()
    test_q4_search_rotated_sorted()
    test_q5_find_min_rotated()
    test_q6_search_2d_matrix()
    test_q7_binary_search_square_root()
    test_q8_ship_within_days()
    test_q9_find_peak_element()
    test_q10_timestamp_log_index()
    print("\nAll 10 binary search DSA questions passed successfully!")
