"""
Phase 6 - Section G.03: Hash Sets
Example 01: Contains Duplicate and Array Intersection

Demonstrating:
1. Contains Duplicate I in O(n) using a hash set.
2. Contains Duplicate II (within distance k) using a sliding window set.
3. Intersection of two arrays with deduplication.
"""


def contains_duplicate(nums):
    """
    Check if any value appears at least twice in nums.
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False


def contains_nearby_duplicate(nums, k):
    """
    Check if nums[i] == nums[j] and abs(i - j) <= k.
    Maintains a sliding window hash set of max size k.
    Time Complexity: O(n)
    Space Complexity: O(min(n, k))
    """
    window = set()
    for i, x in enumerate(nums):
        if x in window:
            return True
        window.add(x)
        if len(window) > k:
            window.remove(nums[i - k])
    return False


def intersection_of_two_arrays(nums1, nums2):
    """
    Find unique intersection elements between two arrays.
    Time Complexity: O(len(nums1) + len(nums2))
    Space Complexity: O(min(len(nums1), len(nums2)))
    """
    set1 = set(nums1)
    set2 = set(nums2)
    return list(set1 & set2)


def main():
    print("=" * 60)
    print("1. Contains Duplicate")
    print("=" * 60)
    t1 = [1, 2, 3, 1]
    t2 = [1, 2, 3, 4]
    print(f"nums = {t1} -> Duplicate: {contains_duplicate(t1)}")
    print(f"nums = {t2} -> Duplicate: {contains_duplicate(t2)}")

    print("\n" + "=" * 60)
    print("2. Contains Nearby Duplicate (within distance k)")
    print("=" * 60)
    arr1, k1 = [1, 2, 3, 1], 3
    arr2, k2 = [1, 2, 3, 1, 2, 3], 2
    print(f"nums = {arr1}, k = {k1} -> Nearby Duplicate: {contains_nearby_duplicate(arr1, k1)}")
    print(f"nums = {arr2}, k = {k2} -> Nearby Duplicate: {contains_nearby_duplicate(arr2, k2)}")

    print("\n" + "=" * 60)
    print("3. Intersection of Two Arrays")
    print("=" * 60)
    n1 = [1, 2, 2, 1]
    n2 = [2, 2]
    inter1 = intersection_of_two_arrays(n1, n2)
    print(f"n1 = {n1}, n2 = {n2} -> Intersection: {inter1}")

    n3 = [4, 9, 5]
    n4 = [9, 4, 9, 8, 4]
    inter2 = intersection_of_two_arrays(n3, n4)
    print(f"n3 = {n3}, n4 = {n4} -> Intersection: {sorted(inter2)}")


if __name__ == "__main__":
    main()
