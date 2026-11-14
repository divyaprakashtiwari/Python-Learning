"""
Phase 6 - Section G.02: Hash Maps
Example 01: Two Sum and Subarray Sum Equals K

Demonstrating core hash map algorithms:
1. Two Sum in O(n) using value-to-index complement map.
2. Subarray Sum Equals K in O(n) using prefix sum frequency map.
"""


def two_sum(nums, target):
    """
    Find two numbers in nums that add up to target.
    Returns (index1, index2) or None.
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    seen = {}  # val -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return None


def subarray_sum_equals_k(nums, k):
    """
    Count the total number of continuous subarrays whose sum equals k.
    Uses prefix sum with hash map counting frequencies.
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    count = 0
    curr_sum = 0
    prefix_counts = {0: 1}  # base case: empty prefix has sum 0

    for num in nums:
        curr_sum += num
        need = curr_sum - k
        if need in prefix_counts:
            count += prefix_counts[need]
        prefix_counts[curr_sum] = prefix_counts.get(curr_sum, 0) + 1

    return count


def main():
    print("=" * 60)
    print("1. Two Sum Problem")
    print("=" * 60)
    arr1 = [2, 7, 11, 15]
    t1 = 9
    res1 = two_sum(arr1, t1)
    print("Array:", arr1, "Target:", t1)
    print("Indices:", res1, "Values:", [arr1[i] for i in res1] if res1 else None)

    arr2 = [3, 2, 4]
    t2 = 6
    res2 = two_sum(arr2, t2)
    print("Array:", arr2, "Target:", t2)
    print("Indices:", res2, "Values:", [arr2[i] for i in res2] if res2 else None)

    print("\n" + "=" * 60)
    print("2. Subarray Sum Equals K")
    print("=" * 60)
    sub_arr1 = [1, 1, 1]
    k1 = 2
    print("Array:", sub_arr1, "k:", k1)
    print("Subarray count:", subarray_sum_equals_k(sub_arr1, k1))

    sub_arr2 = [1, 2, 3, -2, 1, 4, -1]
    k2 = 3
    print("Array:", sub_arr2, "k:", k2)
    print("Subarray count:", subarray_sum_equals_k(sub_arr2, k2))


if __name__ == "__main__":
    main()
