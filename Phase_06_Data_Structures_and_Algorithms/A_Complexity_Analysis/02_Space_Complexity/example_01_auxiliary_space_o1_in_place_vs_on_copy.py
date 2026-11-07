"""
Phase 6 - Section A (Complexity Analysis) - Topic 02: Space Complexity
Example 01: Auxiliary Space O(1) In-Place Array Reversal vs O(n) Out-of-Place Copy

Demonstrates:
  - Total Space vs Auxiliary Space (extra memory allocated beyond the input itself)
  - Reversing a list in O(1) auxiliary space using two pointers vs O(n) slice allocation
"""


def reverse_out_of_place_on(nums: list[int]) -> list[int]:
    """Allocate a brand-new list of length N -> O(n) auxiliary space."""
    return nums[::-1]


def reverse_in_place_o1(nums: list[int]) -> None:
    """Swap elements in-place using two scalar index variables -> O(1) auxiliary space."""
    left = 0
    right = len(nums) - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1


def main() -> None:
    original = [10, 20, 30, 40, 50]

    print("=== 1. Out-of-Place Reversal (`O(n)` Auxiliary Space) ===")
    copied = reverse_out_of_place_on(original)
    print(f"  New object allocated? {copied is not original} | Result: {copied}")

    print("\n=== 2. In-Place Two-Pointer Reversal (`O(1)` Auxiliary Space) ===")
    before_id = id(original)
    reverse_in_place_o1(original)
    print(f"  Same list object in memory? {id(original) == before_id} | Result: {original}")


if __name__ == "__main__":
    main()
