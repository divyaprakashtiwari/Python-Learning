"""
Phase 6 - Data Structures and Algorithms
Section D: Arrays and Strings - Topic 01: Array Operations
Example 02: In-Place Array Reversal & K-Step Cyclic Rotation (3-Reverse Algorithm)

Demonstrates:
1. In-Place Array Reversal using two converging pointers (`left`, `right`) in O(N) time
   and strictly O(1) auxiliary space.
2. Rotating an array right by `k` steps in O(N) time and O(1) space using the classic
   **Three-Reversal Algorithm** (instead of O(N * k) repeated 1-step shifts or O(N) slicing):
   - Step 1: Reverse the entire array `[0 .. n - 1]`.
   - Step 2: Reverse the first `k` elements `[0 .. k - 1]`.
   - Step 3: Reverse the remaining `n - k` elements `[k .. n - 1]`.
"""


def reverse_subarray_in_place(arr: list[int], left: int, right: int) -> None:
    """Reverse `arr[left .. right]` in-place in O(right - left) time and O(1) space."""
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1


def rotate_right_in_place(arr: list[int], k: int, trace: bool = False) -> list[int]:
    """
    Rotate `arr` to the right by `k` steps in O(N) time and O(1) auxiliary space.
    Normalizes `k = k % len(arr)` so `k >= len(arr)` is handled automatically!
    """
    a = arr.copy()
    n = len(a)
    if n <= 1:
        return a

    k = k % n
    if k == 0:
        return a

    # 1. Reverse all N elements
    reverse_subarray_in_place(a, 0, n - 1)
    if trace:
        print(f"  Step 1 (Reverse all [0..{n-1}])     : {a}")

    # 2. Reverse first k elements [0 .. k - 1]
    reverse_subarray_in_place(a, 0, k - 1)
    if trace:
        print(f"  Step 2 (Reverse prefix [0..{k-1}])  : {a}")

    # 3. Reverse remaining n - k elements [k .. n - 1]
    reverse_subarray_in_place(a, k, n - 1)
    if trace:
        print(f"  Step 3 (Reverse suffix [{k}..{n-1}])  : {a}")

    return a


if __name__ == "__main__":
    print("=" * 72)
    print("1. IN-PLACE RIGHT ROTATION BY K STEPS (THREE-REVERSAL ALGORITHM)")
    print("=" * 72)

    nums = [1, 2, 3, 4, 5, 6, 7]
    print(f"Original Array (N={len(nums)}): {nums}, Rotate Right by k = 3:\n")
    rotated = rotate_right_in_place(nums, k=3, trace=True)
    print(f"\nFinal Rotated Array   : {rotated}")

    # Verify k > N normalization (e.g., k = 10 on N = 7 is equivalent to k = 3)
    assert rotate_right_in_place(nums, k=10) == rotated
    print(f"Rotate by k = 10 (10 % 7 == 3): {rotate_right_in_place(nums, k=10)}")
