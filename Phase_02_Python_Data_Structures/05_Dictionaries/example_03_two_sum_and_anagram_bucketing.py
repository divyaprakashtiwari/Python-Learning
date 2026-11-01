"""
Topic 05: Dictionaries
Example 03: Placement DSA Classics — Two Sum (Indices) & Group Anagrams

Demonstrates how `O(1)` dictionary lookups solve top coding interview problems:
1. Two Sum (LeetCode #1): Find indices `(i, j)` where `nums[i] + nums[j] == target` in `O(n)` time.
2. Group Anagrams (LeetCode #49): Bucket words by their sorted character tuple key.
"""


def two_sum_indices(nums: list[int], target: int) -> tuple[int, int] | None:
    """Return indices of the two numbers that add up to `target` in O(n) time."""
    seen_index: dict[int, int] = {}
    for idx, value in enumerate(nums):
        complement = target - value
        if complement in seen_index:
            return (seen_index[complement], idx)
        seen_index[value] = idx
    return None


def group_anagrams(words: list[str]) -> list[list[str]]:
    """Group words that are anagrams of each other using a tuple key."""
    buckets: dict[tuple[str, ...], list[str]] = {}
    for word in words:
        signature = tuple(sorted(word))
        buckets.setdefault(signature, []).append(word)
    return list(buckets.values())


def main() -> None:
    print("=== 1. Two Sum (Returning Indices in O(n) Time) ===")
    nums = [2, 11, 7, 15]
    target = 9
    indices = two_sum_indices(nums, target)
    print(f"Array: {nums}, Target: {target} -> Indices: {indices}")

    print("\n=== 2. Group Anagrams ===")
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    grouped = group_anagrams(words)
    for group in grouped:
        print(f"  Anagram Group: {group}")


if __name__ == "__main__":
    main()
