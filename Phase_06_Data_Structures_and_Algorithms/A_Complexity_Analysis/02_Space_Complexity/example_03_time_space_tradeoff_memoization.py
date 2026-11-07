"""
Phase 6 - Section A (Complexity Analysis) - Topic 02: Space Complexity
Example 03: Time-Space Tradeoff — O(n^2) Time / O(1) Space vs O(n) Time / O(n) Space (`Two Sum`)

Demonstrates:
  - Trading O(n) extra hash-map memory to reduce time complexity from O(n^2) to O(n)
"""


def two_sum_brute_force_o1_space(nums: list[int], target: int) -> tuple[tuple[int, int] | None, int]:
    """O(n^2) time, O(1) auxiliary space: check all pairs without extra containers."""
    checks = 0
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            checks += 1
            if nums[i] + nums[j] == target:
                return (i, j), checks
    return None, checks


def two_sum_hashmap_on_space(nums: list[int], target: int) -> tuple[tuple[int, int] | None, int, int]:
    """O(n) time, O(n) auxiliary space: store seen values in a hash map."""
    seen: dict[int, int] = {}
    checks = 0
    for idx, val in enumerate(nums):
        checks += 1
        complement = target - val
        if complement in seen:
            return (seen[complement], idx), checks, len(seen)
        seen[val] = idx
    return None, checks, len(seen)


def main() -> None:
    nums = [3, 8, 12, 19, 25, 31, 44, 50, 62, 77]
    target = 139  # 62 + 77 at indices (8, 9)

    print("=== Time-Space Tradeoff on `two_sum` (N=10, target=139) ===")
    pair_bf, checks_bf = two_sum_brute_force_o1_space(nums, target)
    pair_hm, checks_hm, dict_entries = two_sum_hashmap_on_space(nums, target)

    print(f"  Brute Force (O(1) space, O(n^2) time) -> pair={pair_bf}, loop checks={checks_bf}, dict_size=0")
    print(f"  Hash Map    (O(n) space, O(n) time)   -> pair={pair_hm}, loop checks={checks_hm}, dict_size={dict_entries}")


if __name__ == "__main__":
    main()
