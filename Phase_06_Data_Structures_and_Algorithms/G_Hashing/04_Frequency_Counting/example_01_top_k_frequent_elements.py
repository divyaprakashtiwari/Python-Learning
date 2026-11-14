"""
Phase 6 - Section G.04: Frequency Counting
Example 01: Top K Frequent Elements

Demonstrating:
1. Top K Frequent Elements via O(n) Bucket Sort frequency inversion.
2. Top K Frequent Elements via Min-Heap O(n log k).
3. Pythonic standard library approach using collections.Counter.
"""

from collections import Counter
import heapq


def top_k_frequent_bucket_sort(nums, k):
    """
    Find the k most frequent elements in O(n) time using bucket sort.
    Buckets index represents frequency; contents are lists of numbers with that frequency.
    """
    counts = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]

    for num, freq in counts.items():
        buckets[freq].append(num)

    result = []
    # Traverse buckets from highest frequency downwards
    for freq in range(len(buckets) - 1, 0, -1):
        for num in buckets[freq]:
            result.append(num)
            if len(result) == k:
                return result

    return result


def top_k_frequent_heap(nums, k):
    """
    Find top k frequent elements using a min-heap of size k.
    Time Complexity: O(n log k)
    Space Complexity: O(n + k)
    """
    counts = Counter(nums)
    # Heap stores (freq, num)
    heap = []
    for num, freq in counts.items():
        heapq.heappush(heap, (freq, num))
        if len(heap) > k:
            heapq.heappop(heap)

    return [num for freq, num in heap]


def top_k_frequent_counter(nums, k):
    """
    Pythonic baseline using Counter.most_common().
    """
    return [num for num, _ in Counter(nums).most_common(k)]


def main():
    print("=" * 60)
    print("1. Top K Frequent Elements (Bucket Sort O(n))")
    print("=" * 60)
    nums1, k1 = [1, 1, 1, 2, 2, 3], 2
    res_bucket = top_k_frequent_bucket_sort(nums1, k1)
    print(f"nums = {nums1}, k = {k1}")
    print(f"Bucket Sort Result (Top {k1}):", res_bucket)

    print("\n" + "=" * 60)
    print("2. Top K Frequent Elements (Min-Heap O(n log k))")
    print("=" * 60)
    nums2, k2 = [4, 1, -1, 2, -1, 2, 3], 2
    res_heap = top_k_frequent_heap(nums2, k2)
    print(f"nums = {nums2}, k = {k2}")
    print(f"Min-Heap Result (Top {k2}):", sorted(res_heap))

    print("\n" + "=" * 60)
    print("3. Pythonic collections.Counter Comparison")
    print("=" * 60)
    res_counter = top_k_frequent_counter(nums2, k2)
    print(f"Counter.most_common Result:", sorted(res_counter))


if __name__ == "__main__":
    main()
