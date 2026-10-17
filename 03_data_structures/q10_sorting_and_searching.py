"""
Topic 03: Data Structures
Question 10: Sorting and Searching (Deep Dive)

Master Python sorting algorithms and search strategies:
- In-place list.sort() vs sorted() mechanics, return types, and stability
- Multi-key sorting with operator.itemgetter and tuple negation
- Custom sorting comparators with functools.cmp_to_key (e.g. Largest Number)
- Binary search mechanics with bisect_left, bisect_right, and insort
- Binary search on answer (monotonic predicate bisection)
- Empirical benchmark: Linear Search vs Hash Lookup vs Binary Search
- Quickselect algorithm (k-th smallest element in O(N) average time)
- Priority queues and Top-K elements with heapq
- Multi-way merge of sorted streams (external sorting)
- Real-world inverted index and prefix autocomplete engine
"""

import bisect
import functools
import heapq
import operator
import time
from typing import Any, Callable, Dict, List, Optional, Tuple


# ============================================================
# Q1: In-Place list.sort() vs sorted() Mechanics & Stability
# ============================================================
# Question: Compare `list.sort()` and `sorted()` in terms of in-place mutation, return value,
# memory allocation, and stability (preserving relative order of equal keys).

print("=== Q1: list.sort() vs sorted() & Stability ===")

records = [
    {"name": "Alice", "score": 90, "entry_id": 1},
    {"name": "Bob",   "score": 85, "entry_id": 2},
    {"name": "Charlie", "score": 90, "entry_id": 3},  # Tied with Alice
    {"name": "Diana", "score": 85, "entry_id": 4},  # Tied with Bob
]

# 1. sorted() produces a brand new list without modifying original
sorted_copy = sorted(records, key=lambda r: r["score"])
print(f"  sorted() returned new list (len={len(sorted_copy)}); original is untouched.")
assert sorted_copy is not records
assert records[0]["name"] == "Alice"  # Original order preserved

# 2. list.sort() sorts IN-PLACE and returns None (common beginner pitfall: x = x.sort())
sort_retval = records.sort(key=lambda r: r["score"])
print(f"  list.sort() return value: {sort_retval} (Always None!)")
assert sort_retval is None
assert records[0]["name"] in ("Bob", "Diana")

# 3. Stability check: Timsort guarantees tied items retain their relative order
# Bob (entry 2) was before Diana (entry 4), Alice (entry 1) before Charlie (entry 3)
assert records[0]["entry_id"] == 2 and records[1]["entry_id"] == 4
assert records[2]["entry_id"] == 1 and records[3]["entry_id"] == 3
print("  Timsort stability verified: tied elements retain their original relative order.")

# Explanation: `list.sort()` is only available on lists and mutates in-place (O(1) extra memory).
# `sorted()` works on any iterable and constructs a new list (O(N) memory).


# ============================================================
# Q2: Multi-Key Sorting & Direction Control
# ============================================================
# Question: Sort employee records by:
# Primary: Department (Ascending alphabetical)
# Secondary: Salary (Descending numeric)
# Tertiary: Name (Ascending alphabetical)
# Demonstrate how to invert numeric keys in a tuple key function.

print("\n=== Q2: Multi-Key Sorting with Mixed Directions ===")

employees = [
    {"name": "Zach",  "dept": "Sales", "salary": 70000},
    {"name": "Alice", "dept": "Eng",   "salary": 120000},
    {"name": "Bob",   "dept": "Eng",   "salary": 140000},
    {"name": "Carol", "dept": "Eng",   "salary": 120000},  # Tied salary with Alice
    {"name": "Dan",   "dept": "Sales", "salary": 90000},
]

# Sort key tuple: (dept, -salary, name)
# Negating salary achieves descending order while dept and name remain ascending!
employees.sort(key=lambda e: (e["dept"], -e["salary"], e["name"]))

print("  Sorted employees (Dept ASC, Salary DESC, Name ASC):")
for e in employees:
    print(f"    {e['dept']:<6} | ${e['salary']:<7} | {e['name']}")

assert employees[0]["name"] == "Bob"    # Eng, $140,000
assert employees[1]["name"] == "Alice"  # Eng, $120,000 (Alice < Carol alphabetically)
assert employees[2]["name"] == "Carol"  # Eng, $120,000
assert employees[3]["name"] == "Dan"    # Sales, $90,000
assert employees[4]["name"] == "Zach"   # Sales, $70,000

# Explanation: Python compares tuples lexicographically from left to right.
# Negating numeric values (`-val`) allows mixing ascending and descending directions.


# ============================================================
# Q3: Custom Comparator Functions using functools.cmp_to_key
# ============================================================
# Question: Solve the "Largest Number" problem: given a list of non-negative integers,
# arrange them such that they form the largest possible number.
# Example: [3, 30, 34, 5, 9] -> "9534330". Use `functools.cmp_to_key`.

print("\n=== Q3: Custom Comparator via cmp_to_key (Largest Number) ===")

def compare_numbers(a: str, b: str) -> int:
    """Return positive if b+a > a+b (b should come before a for descending order)."""
    if a + b > b + a:
        return -1  # 'a' should come first
    elif a + b < b + a:
        return 1   # 'b' should come first
    return 0

def largest_number(nums: List[int]) -> str:
    # Convert all integers to strings
    str_nums = [str(x) for x in nums]
    str_nums.sort(key=functools.cmp_to_key(compare_numbers))
    
    # Handle leading zeroes (e.g. [0, 0] -> "0")
    result = "".join(str_nums)
    return "0" if result[0] == "0" else result

sample_nums = [3, 30, 34, 5, 9]
largest_str = largest_number(sample_nums)

print(f"  Input: {sample_nums}")
print(f"  Largest concatenated number: {largest_str}")

assert largest_str == "9534330"
assert largest_number([0, 0]) == "0"

# Explanation: `cmp_to_key` bridges legacy two-argument comparator functions
# `cmp(x, y)` to Python 3's key-function architecture.


# ============================================================
# Q4: Binary Search with bisect (bisect_left, bisect_right)
# ============================================================
# Question: Use Python's built-in `bisect` module to:
# 1) Find the exact index of an element in O(log N)
# 2) Count total occurrences of a duplicate value in a sorted list
# 3) Maintain a continuously sorted list using `bisect.insort`

print("\n=== Q4: Binary Search with bisect Module ===")

sorted_scores = [12, 25, 45, 45, 45, 60, 78, 88, 95]

def binary_search_find(arr: List[int], target: int) -> int:
    """Returns index of target if present, otherwise -1."""
    idx = bisect.bisect_left(arr, target)
    if idx < len(arr) and arr[idx] == target:
        return idx
    return -1

def count_occurrences_sorted(arr: List[int], target: int) -> int:
    """Counts duplicates in O(log N) time using bisect_right - bisect_left."""
    left = bisect.bisect_left(arr, target)
    right = bisect.bisect_right(arr, target)
    return right - left

idx_60 = binary_search_find(sorted_scores, 60)
idx_99 = binary_search_find(sorted_scores, 99)
count_45 = count_occurrences_sorted(sorted_scores, 45)

print(f"  Index of 60:        {idx_60}")
print(f"  Index of 99:        {idx_99}")
print(f"  Occurrences of 45:  {count_45}")

assert idx_60 == 5
assert idx_99 == -1
assert count_45 == 3

# insort maintains sort order without full O(N log N) re-sort
live_list = [10, 30, 50]
bisect.insort(live_list, 25)
bisect.insort(live_list, 40)
print(f"  Live list after insort: {live_list}")
assert live_list == [10, 25, 30, 40, 50]

# Explanation: `bisect_left` returns the earliest index to insert x while maintaining sort order.
# `bisect_right` returns the latest index. The difference `right - left` is the count of duplicates.


# ============================================================
# Q5: Binary Search on Monotonic Predicate (Integer Square Root)
# ============================================================
# Question: Implement integer square root `isqrt(n)` using binary search over the range [0, n]
# in O(log n) time without floating-point math or math.sqrt.

print("\n=== Q5: Binary Search on Monotonic Predicate ===")

def integer_sqrt(n: int) -> int:
    """Returns largest integer x such that x^2 <= n."""
    if n < 0:
        raise ValueError("Cannot compute sqrt of negative integer")
    if n < 2:
        return n

    low, high = 1, n // 2
    ans = 1

    while low <= high:
        mid = (low + high) // 2
        sq = mid * mid
        if sq == n:
            return mid
        elif sq < n:
            ans = mid      # mid is a valid candidate
            low = mid + 1  # search for larger
        else:
            high = mid - 1 # search for smaller

    return ans

test_vals = [(0, 0), (1, 1), (4, 2), (8, 2), (9, 3), (15, 3), (16, 4), (100, 10), (101, 10)]
for val, expected in test_vals:
    res = integer_sqrt(val)
    assert res == expected, f"Failed for {val}: got {res}, expected {expected}"

print(f"  sqrt(100): {integer_sqrt(100)}, sqrt(101): {integer_sqrt(101)}, sqrt(15): {integer_sqrt(15)}")

# Explanation: Binary search works on any monotonic predicate: if f(x) is False,
# then for all y >= x, f(y) is False. This enables searching answer spaces efficiently.


# ============================================================
# Q6: Benchmark: Linear Search vs Hash Lookup vs Binary Search
# ============================================================
# Question: Empirically compare lookup performance across:
# 1) Linear search in list: O(N)
# 2) Binary search in sorted list: O(log N)
# 3) Hash table lookup in set: O(1)

print("\n=== Q6: Search Performance Benchmark ===")

N = 100_000
data_list = list(range(0, N * 2, 2))  # [0, 2, 4, ..., 199998]
data_set = set(data_list)
target = 199998  # Worst-case at the very end

# 1. Linear search
t0 = time.perf_counter()
found_linear = target in data_list
t_linear = time.perf_counter() - t0

# 2. Binary search
t0 = time.perf_counter()
idx = bisect.bisect_left(data_list, target)
found_bin = (idx < len(data_list) and data_list[idx] == target)
t_binary = time.perf_counter() - t0

# 3. Hash set lookup
t0 = time.perf_counter()
found_hash = target in data_set
t_hash = time.perf_counter() - t0

print(f"  Linear search time (O(N)):      {t_linear * 1000:.4f} ms")
print(f"  Binary search time (O(log N)):  {t_binary * 1000:.4f} ms")
print(f"  Hash set lookup time (O(1)):     {t_hash * 1000:.4f} ms")

assert found_linear and found_bin and found_hash
assert t_binary < t_linear
assert t_hash < t_linear

# Explanation: In an N=100,000 array, linear search tests 100,000 items.
# Binary search requires at most 17 comparisons (log2(100000) ~ 16.6).
# Hash table performs a direct constant-time hash computation.


# ============================================================
# Q7: Quickselect (K-th Smallest Element in O(N) Average Time)
# ============================================================
# Question: Implement the Quickselect algorithm to find the K-th smallest element
# in an unsorted list in O(N) average time without sorting the whole list.

print("\n=== Q7: Quickselect Algorithm ===")

def quickselect(nums: List[int], k: int) -> int:
    """Finds k-th smallest element (1-indexed) in O(N) average time."""
    if not (1 <= k <= len(nums)):
        raise IndexError("k out of bounds")

    target_idx = k - 1  # 0-indexed position

    def _select(left: int, right: int) -> int:
        if left == right:
            return nums[left]

        # Use median-of-three or middle as pivot
        pivot_val = nums[(left + right) // 2]
        
        # 3-way partition: elements < pivot, == pivot, > pivot
        lows = [x for x in nums[left:right + 1] if x < pivot_val]
        pivots = [x for x in nums[left:right + 1] if x == pivot_val]
        highs = [x for x in nums[left:right + 1] if x > pivot_val]

        # Reconstruct partitioned subsegment
        nums[left:right + 1] = lows + pivots + highs

        pivot_start = left + len(lows)
        pivot_end = pivot_start + len(pivots) - 1

        if target_idx < pivot_start:
            return _select(left, pivot_start - 1)
        elif target_idx > pivot_end:
            return _select(pivot_end + 1, right)
        else:
            return nums[target_idx]

    # Work on a shallow copy
    arr = list(nums)
    return _select(0, len(arr) - 1)

raw_arr = [38, 27, 43, 3, 9, 82, 10]
# Sorted: [3, 9, 10, 27, 38, 43, 82]
first_min = quickselect(raw_arr, 1)
third_min = quickselect(raw_arr, 3)
largest_val = quickselect(raw_arr, len(raw_arr))

print(f"  Array: {raw_arr}")
print(f"  1st smallest: {first_min} (min)")
print(f"  3rd smallest: {third_min}")
print(f"  7th smallest: {largest_val} (max)")

assert first_min == 3
assert third_min == 10
assert largest_val == 82

# Explanation: Quickselect only recurses into the partition containing the target index,
# yielding a recurrence of T(N) = T(N/2) + O(N) = O(N) average time complexity.


# ============================================================
# Q8: Top-K Elements with Priority Queue (heapq)
# ============================================================
# Question: Extract the top K highest earning transactions from a stream using `heapq`
# in O(N log K) time and O(K) space, demonstrating why a min-heap is used for Top-K.

print("\n=== Q8: Top-K Elements via Min-Heap (heapq) ===")

transactions = [
    {"id": "tx1", "amount": 450.0},
    {"id": "tx2", "amount": 1200.0},
    {"id": "tx3", "amount": 80.0},
    {"id": "tx4", "amount": 3400.0},
    {"id": "tx5", "amount": 620.0},
    {"id": "tx6", "amount": 2100.0},
    {"id": "tx7", "amount": 950.0},
]

K = 3

# Top K using heapq.nlargest
top_k_direct = heapq.nlargest(K, transactions, key=lambda t: t["amount"])

# Manual streaming min-heap of size K: (amount, tx_id)
# Any candidate larger than the heap's minimum displaces it
min_heap: List[Tuple[float, str]] = []
for tx in transactions:
    item = (tx["amount"], tx["id"])
    if len(min_heap) < K:
        heapq.heappush(min_heap, item)
    elif item[0] > min_heap[0][0]:
        heapq.heapreplace(min_heap, item)

# The min-heap contains the K largest elements
top_k_stream = sorted([tx_id for _, tx_id in min_heap], reverse=True)

print(f"  Top {K} transactions by amount:")
for tx in top_k_direct:
    print(f"    {tx['id']}: ${tx['amount']:.2f}")

assert [t["id"] for t in top_k_direct] == ["tx4", "tx6", "tx2"]
assert set([t["id"] for t in top_k_direct]) == set(top_k_stream)

# Explanation: Maintaining a min-heap of size K keeps the smallest of the top K at the root.
# Checking against the root takes O(1) and heap replacement takes O(log K).


# ============================================================
# Q9: Multi-Way Merge of Sorted Iterables (heapq.merge)
# ============================================================
# Question: Merge three pre-sorted daily temperature sensor logs into a single sorted
# chronological stream without loading all records into memory at once.

print("\n=== Q9: Multi-Way Merge of Sorted Streams ===")

sensor_a = [(1, "10:00", 21.5), (4, "10:15", 22.0), (7, "10:30", 22.4)]
sensor_b = [(2, "10:05", 21.7), (5, "10:20", 22.1), (8, "10:35", 22.5)]
sensor_c = [(3, "10:10", 21.9), (6, "10:25", 22.3), (9, "10:40", 22.8)]

# heapq.merge performs an external merge in O(N log K) time and O(K) space
merged_stream = list(heapq.merge(sensor_a, sensor_b, sensor_c, key=lambda entry: entry[0]))

print("  Chronologically merged sensor events (timestamp sequence):")
for event_id, ts, temp in merged_stream:
    print(f"    Seq #{event_id} at {ts}: {temp} deg C")

# Verify strictly ascending sequence numbers
assert [item[0] for item in merged_stream] == [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Explanation: `heapq.merge` lazily pulls the next smallest item across K sorted
# iterables using a min-heap of size K, making it the foundation for external sorting.


# ============================================================
# Q10: Real-World Inverted Index & Prefix Autocomplete Engine
# ============================================================
# Question: Build an in-memory prefix autocomplete engine.
# 1) Store words in a sorted index.
# 2) Use binary search (`bisect_left`) to find candidate prefixes in O(log N).
# 3) Rank matches by popularity score.

print("\n=== Q10: Autocomplete Search Engine with Binary Search ===")

class AutocompleteEngine:
    def __init__(self, vocabulary: Dict[str, int]):
        """vocabulary maps word -> search popularity score."""
        self._scores = vocabulary
        # Maintain a strictly sorted list of terms for binary search
        self._sorted_terms: List[str] = sorted(vocabulary.keys())

    def search(self, prefix: str, max_results: int = 3) -> List[Tuple[str, int]]:
        """Returns top matching words ranked by popularity score."""
        prefix = prefix.lower()
        # Find the starting point of words starting with prefix
        start_idx = bisect.bisect_left(self._sorted_terms, prefix)
        
        candidates: List[Tuple[str, int]] = []
        # Scan forward while words continue to match prefix
        for i in range(start_idx, len(self._sorted_terms)):
            term = self._sorted_terms[i]
            if not term.startswith(prefix):
                break
            candidates.append((term, self._scores[term]))

        # Rank candidates by popularity score descending
        candidates.sort(key=lambda c: c[1], reverse=True)
        return candidates[:max_results]

vocab = {
    "python": 1000,
    "pytorch": 850,
    "pypy": 400,
    "pytest": 600,
    "pycharm": 500,
    "pandas": 900,
    "performance": 350,
    "programming": 950
}

engine = AutocompleteEngine(vocab)
py_results = engine.search("py", max_results=3)
pro_results = engine.search("pro", max_results=2)
empty_results = engine.search("xyz")

print(f"  Prefix 'py' top 3:  {py_results}")
print(f"  Prefix 'pro' top 2: {pro_results}")
print(f"  Prefix 'xyz':       {empty_results}")

assert [w for w, _ in py_results] == ["python", "pytorch", "pytest"]
assert [w for w, _ in pro_results] == ["programming"]
assert len(empty_results) == 0

print("\nAll 10 sorting and searching questions executed and asserted successfully!")
