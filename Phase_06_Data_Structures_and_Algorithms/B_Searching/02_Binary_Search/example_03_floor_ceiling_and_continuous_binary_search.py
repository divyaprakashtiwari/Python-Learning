"""
Phase 6 - Data Structures and Algorithms
Section B: Searching - Topic 02: Binary Search
Example 03: Floor, Ceiling, and Real-Valued (Continuous) Binary Search

Demonstrates:
1. Finding the Floor (greatest element <= target) and Ceiling (smallest element >= target)
   in a sorted array in O(log N) time.
2. Continuous Binary Search (Bisection Method) over floating-point numbers to compute
   the N-th root of a positive number to within `epsilon = 1e-9` precision.
"""


def find_floor_and_ceiling(
    arr: list[int], target: int
) -> tuple[int | None, int | None]:
    """
    Return (floor_val, ceiling_val) for `target` in sorted ascending array `arr`.
    - Floor  : largest element in `arr` that is <= target (or None if all elements > target)
    - Ceiling: smallest element in `arr` that is >= target (or None if all elements < target)
    Time Complexity: O(log N)
    """
    low = 0
    high = len(arr) - 1
    floor_val: int | None = None
    ceiling_val: int | None = None

    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            # Exact match is both its own floor and ceiling!
            return arr[mid], arr[mid]
        elif arr[mid] < target:
            # arr[mid] is a candidate for Floor; look right for a larger one <= target
            floor_val = arr[mid]
            low = mid + 1
        else:
            # arr[mid] is a candidate for Ceiling; look left for a smaller one >= target
            ceiling_val = arr[mid]
            high = mid - 1

    return floor_val, ceiling_val


def continuous_binary_search_sqrt(
    number: float, epsilon: float = 1e-9
) -> tuple[float, int]:
    """
    Compute the square root of `number >= 0` using Continuous Binary Search (Bisection)
    without using `math.sqrt` or `** 0.5`.
    Returns (approx_sqrt, iterations).
    """
    if number < 0:
        raise ValueError("Cannot compute real square root of a negative number.")
    if number == 0:
        return 0.0, 0

    # If number < 1 (e.g., 0.25), its square root (0.5) is larger than `number`, so high = 1.0
    low = 0.0
    high = max(1.0, number)
    iterations = 0

    while (high - low) > epsilon:
        iterations += 1
        mid = low + (high - low) / 2.0
        if mid * mid < number:
            low = mid
        else:
            high = mid

    return low + (high - low) / 2.0, iterations


if __name__ == "__main__":
    print("=" * 72)
    print("1. FINDING FLOOR AND CEILING IN A SORTED ARRAY O(log N)")
    print("=" * 72)

    server_capacities = [16, 32, 64, 128, 256, 512]
    print(f"Available Server RAM Capacities (GB): {server_capacities}\n")

    for req_gb in [10, 32, 50, 100, 256, 600]:
        flr, ceil = find_floor_and_ceiling(server_capacities, req_gb)
        print(
            f"  Requested {req_gb:>3} GB -> "
            f"Floor (<= req): {str(flr):>4} GB | Ceiling (>= req): {str(ceil):>4} GB"
        )

    print("\n" + "=" * 72)
    print("2. CONTINUOUS BINARY SEARCH ( FLOATING-POINT SQUARE ROOT )")
    print("=" * 72)

    for val in [2.0, 49.0, 0.25, 1000.0]:
        approx, steps = continuous_binary_search_sqrt(val, epsilon=1e-9)
        actual = val ** 0.5
        print(
            f"  sqrt({val:>6.2f}) -> Approx: {approx:.9f} | "
            f"Actual: {actual:.9f} | Bisection Steps: {steps}"
        )
