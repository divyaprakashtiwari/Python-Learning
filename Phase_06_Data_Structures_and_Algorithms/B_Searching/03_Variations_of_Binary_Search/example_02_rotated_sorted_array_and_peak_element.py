"""
Phase 6 - Data Structures and Algorithms
Section B: Searching - Topic 03: Variations of Binary Search
Example 02: Search in Rotated Sorted Array, Minimum in Rotated Array, and Peak Element

Demonstrates:
1. Searching for a target in a Rotated Sorted Array (distinct elements) in O(log N):
   At any midpoint `mid`, at least one half (`[low..mid]` or `[mid..high]`) is strictly sorted!
2. Finding the Minimum Element (Pivot / Rotation Count) in a Rotated Sorted Array in O(log N).
3. Finding a Peak Element (`arr[i] > neighbors`) in O(log N) by climbing the rising slope.
"""


def search_rotated_sorted_array(arr: list[int], target: int) -> int:
    """
    Search for `target` in a rotated sorted array of distinct integers in O(log N) time.
    Example: [45, 60, 75, 90, 10, 20, 30]
    """
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            return mid

        # Check if the LEFT half [low .. mid] is sorted
        if arr[low] <= arr[mid]:
            if arr[low] <= target < arr[mid]:
                high = mid - 1  # Target lies inside the sorted left half
            else:
                low = mid + 1   # Target lies in the right half
        # Otherwise, the RIGHT half [mid .. high] MUST be sorted
        else:
            if arr[mid] < target <= arr[high]:
                low = mid + 1   # Target lies inside the sorted right half
            else:
                high = mid - 1  # Target lies in the left half

    return -1


def find_min_in_rotated_sorted_array(arr: list[int]) -> tuple[int, int]:
    """
    Return (min_index, min_value) in a rotated sorted array of distinct elements in O(log N).
    Note: `min_index` also equals the number of right-rotations!
    """
    low = 0
    high = len(arr) - 1

    while low < high:
        mid = low + (high - low) // 2
        # If arr[mid] > arr[high], the minimum (cliff drop) is strictly to the right of mid
        if arr[mid] > arr[high]:
            low = mid + 1
        else:
            # Minimum is at mid or to the left of mid
            high = mid

    return low, arr[low]


def find_peak_element(arr: list[int]) -> tuple[int, int]:
    """
    Find any peak element index `i` where `arr[i]` is strictly greater than its neighbors
    in O(log N) time by moving toward the rising slope.
    """
    low = 0
    high = len(arr) - 1

    while low < high:
        mid = low + (high - low) // 2
        if arr[mid] < arr[mid + 1]:
            # Rising slope to the right -> a peak is guaranteed in [mid + 1 .. high]
            low = mid + 1
        else:
            # Falling slope (or peak at mid) -> a peak is guaranteed in [low .. mid]
            high = mid

    return low, arr[low]


if __name__ == "__main__":
    print("=" * 72)
    print("1. SEARCH IN A ROTATED SORTED ARRAY O(log N)")
    print("=" * 72)

    rotated = [45, 60, 75, 90, 10, 20, 30]
    print(f"Rotated Array: {rotated}")
    for q in [75, 10, 30, 50]:
        print(f"  Search {q:>2} -> Index: {search_rotated_sorted_array(rotated, q)}")

    min_idx, min_val = find_min_in_rotated_sorted_array(rotated)
    print(f"  Minimum Element: {min_val} at index {min_idx} (Rotated by {min_idx} positions)")

    print("\n" + "=" * 72)
    print("2. FIND PEAK ELEMENT IN AN UNSORTED / BITONIC ARRAY O(log N)")
    print("=" * 72)

    elevation_profile = [12, 28, 45, 82, 64, 51, 30, 15]
    p_idx, p_val = find_peak_element(elevation_profile)
    print(f"Elevation Profile: {elevation_profile}")
    print(f"Peak Element     : {p_val} at index {p_idx}")
