"""
Topic 03: Data Structures
Question 02: List Methods and Manipulation (Deep Dive)

Master Python list methods: append vs extend vs insert, pop vs remove vs del,
in-place .sort() vs sorted(), .reverse() vs reversed(), arbitrary nesting flattening,
order-preserving deduplication, list partitioning, multiset bag arithmetic,
and in-place two-pointer compaction.
"""

from typing import Any

# ============================================================
# Q1: Mutation Methods and the "None" Return Value Pitfall
# ============================================================
# Question: Demonstrate append(), extend(), insert(), pop(), remove(), and clear().
# Highlight the classic bug: why `x = x.append(1)` assigns None.

print("=== Q1: List Mutation Methods & Pitfalls ===")

# The classic beginner bug:
my_list = [1, 2, 3]
returned_val = my_list.append(4)  # Modifies in-place, returns None!
print(f"  After my_list.append(4): my_list = {my_list}")
print(f"  Return value of .append(): {returned_val} (In-place methods return None in Python!)")

# Contrast: append() vs extend()
single_item = ["A", "B"]
single_item.append(["C", "D"])  # Appends the list as a single nested element
print(f"\n  append([C, D]): {single_item}")

multi_items = ["A", "B"]
multi_items.extend(["C", "D"])  # Unpacks and appends each element individually
print(f"  extend([C, D]): {multi_items}")

# insert(index, item)
multi_items.insert(1, "INSERTED_AT_1")
print(f"  insert(1, ...): {multi_items}")

# pop(index) removes and RETURNS the popped item
popped_item = multi_items.pop(1)
print(f"  pop(1) returned: '{popped_item}', remaining: {multi_items}")

# remove(value) removes the FIRST matching occurrence by value
multi_items.remove("C")
print(f"  remove('C'):    {multi_items}")

# clear() removes all elements in-place
multi_items.clear()
print(f"  clear():        {multi_items} (Length: {len(multi_items)})")

# Explanation: Python intentionally designs in-place mutating methods (`append`, `extend`,
# `sort`, `reverse`, `clear`) to return `None` to remind developers of state mutation.


# ============================================================
# Q2: Search and Frequency Inspection (.index and .count)
# ============================================================
# Question: Demonstrate `.index()` with slice boundaries, handle `ValueError` when
# an element is missing, and build a safe index lookup helper.

print("\n=== Q2: Search and Frequency Inspection ===")

fruits = ["apple", "banana", "cherry", "banana", "date", "banana", "elderberry"]

# Frequency count
banana_count = fruits.count("banana")
print(f"  fruits.count('banana'): {banana_count}")

# First occurrence
first_idx = fruits.index("banana")
print(f"  First 'banana' index:   {first_idx}")

# Search with start/end bounds: find second occurrence starting at index first_idx + 1
second_idx = fruits.index("banana", first_idx + 1)
print(f"  Second 'banana' index:  {second_idx}")

def safe_find_index(lst: list, value: Any, default: int = -1) -> int:
    """Finds index of value without raising ValueError if not found."""
    try:
        return lst.index(value)
    except ValueError:
        return default

print(f"  safe_find_index('cherry'): {safe_find_index(fruits, 'cherry')}")
print(f"  safe_find_index('mango'):  {safe_find_index(fruits, 'mango')} (safe fallback)")

# Explanation: `.index(x, start, end)` raises `ValueError` if `x` is absent.
# Always guard with `if x in lst:` or a `try-except ValueError` block.


# ============================================================
# Q3: In-Place .sort() vs Built-in sorted()
# ============================================================
# Question: Compare `list.sort()` (in-place, $O(1)$ extra space) with `sorted()`
# (returns new list, $O(N)$ extra space). Demonstrate multi-key sorting with `key=`.

print("\n=== Q3: In-Place .sort() vs sorted() ===")

original_nums = [45, 12, 89, 23, 7, 56]

# sorted() leaves original intact and returns a new list
new_sorted = sorted(original_nums)
print(f"  Original untouched: {original_nums}")
print(f"  sorted() returned:  {new_sorted}")

# list.sort() mutates original in-place and returns None
orig_id = id(original_nums)
sort_ret = original_nums.sort(reverse=True)
print(f"  After .sort(reverse=True): {original_nums} (id: {id(original_nums) == orig_id})")
print(f"  .sort() return value:      {sort_ret}")

# Multi-key sorting with custom lambda:
# Sort by string length ascending, then alphabetically case-insensitive
words = ["banana", "Pie", "apple", "fig", "Avocado", "pear", "kiwi"]
words.sort(key=lambda w: (len(w), w.lower()))
print(f"\n  Multi-key sorted (by length, then alpha): {words}")

# Explanation: Python uses Timsort, an adaptive, stable $O(N \log N)$ sorting algorithm.
# Stability guarantees that items with equal keys maintain their original relative order.


# ============================================================
# Q4: In-Place .reverse() vs reversed() Iterator
# ============================================================
# Question: Demonstrate in-place reversal via `.reverse()` versus lazy iteration
# via `reversed()`.

print("\n=== Q4: In-Place .reverse() vs reversed() ===")

stream = [10, 20, 30, 40, 50]
print(f"  Original list:              {stream}")

# reversed() returns a lazy iterator
rev_iter = reversed(stream)
print(f"  reversed(stream) type:      {type(rev_iter)}")
print(f"  Iterating lazy reversed():  {[x for x in rev_iter]}")
print(f"  Original still untouched:   {stream}")

# .reverse() mutates the list in-place and returns None
ret_rev = stream.reverse()
print(f"  After stream.reverse():     {stream}")
print(f"  .reverse() return value:    {ret_rev}")

# Explanation: Use `reversed()` when you want to loop backward through a collection
# without mutating it or allocating a new reversed list in memory.


# ============================================================
# Q5: Deletion Strategies Comparison (remove vs pop vs del vs filter)
# ============================================================
# Question: Compare deleting elements by value, by index, by statement,
# and deleting all occurrences of a duplicate value.

print("\n=== Q5: Element Deletion Strategies ===")

# Strategy 1: remove(val) - by value, first occurrence only
items1 = ["A", "B", "C", "B", "D"]
items1.remove("B")
print(f"  1. remove('B') (first occurrence only): {items1}")

# Strategy 2: pop(idx) - by index, returns removed value
items2 = ["A", "B", "C", "D"]
popped = items2.pop(2)
print(f"  2. pop(2) returned '{popped}', list is:    {items2}")

# Strategy 3: del lst[idx] - statement, by index or slice
items3 = ["A", "B", "C", "D", "E"]
del items3[1:3]
print(f"  3. del items[1:3]:                      {items3}")

# Strategy 4: Delete ALL occurrences of a value (Comprehension / Filter)
items4 = ["A", "B", "C", "B", "D", "B", "E"]
target = "B"
filtered = [x for x in items4 if x != target]
print(f"  4. Remove ALL '{target}' occurrences:         {filtered}")

# Explanation: `remove()` is $O(N)$ and stops at the first match. To remove all matches,
# a list comprehension `[x for x in lst if x != val]` is $O(N)$ and significantly faster.


# ============================================================
# Q6: Arbitrary Depth Nested List Flattener
# ============================================================
# Question: Write a recursive and an iterative function to flatten a list containing
# arbitrarily deep nested lists into a single flat list.

print("\n=== Q6: Arbitrary Depth Nested List Flattener ===")

deeply_nested = [1, [2, [3, 4], 5], [[6, 7]], [8, [9, [10]]]]

def flatten_recursive(nested: list) -> list:
    """Recursively flattens nested lists of arbitrary depth."""
    flat = []
    for item in nested:
        if isinstance(item, list):
            flat.extend(flatten_recursive(item))
        else:
            flat.append(item)
    return flat

def flatten_iterative(nested: list) -> list:
    """Iteratively flattens nested lists using an explicit stack."""
    flat = []
    stack = [nested]
    
    while stack:
        current = stack.pop()
        if isinstance(current, list):
            # Push elements in reverse so they are popped in correct original order
            stack.extend(reversed(current))
        else:
            flat.append(current)
            
    return flat

print(f"  Nested input:       {deeply_nested}")
print(f"  Recursive flatten:  {flatten_recursive(deeply_nested)}")
print(f"  Iterative flatten:  {flatten_iterative(deeply_nested)}")

# Explanation: The recursive approach is intuitive, while the iterative stack-based approach
# avoids Python's default recursion depth limit (`sys.getrecursionlimit()`).


# ============================================================
# Q7: Order-Preserving Duplicate Removal
# ============================================================
# Question: Remove duplicates from a list while strictly preserving the original
# insertion order of the first occurrence of each element.

print("\n=== Q7: Order-Preserving Deduplication ===")

raw_data = ["apple", "banana", "apple", "cherry", "banana", "date", "apple"]

# Approach 1: dict.fromkeys() (Python 3.7+ dictionaries maintain insertion order)
deduped_dict = list(dict.fromkeys(raw_data))
print(f"  Approach 1 (dict.fromkeys): {deduped_dict}")

# Approach 2: Tracking with a set (Fastest O(N) for general iterables)
def deduplicate_ordered(seq: list) -> list:
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]

print(f"  Approach 2 (set tracking):  {deduplicate_ordered(raw_data)}")

# Comparison: set() loses insertion order
unordered_set = list(set(raw_data))
print(f"  Standard set() (ORDER LOST): {unordered_set}")

# Explanation: `dict.fromkeys()` provides $O(N)$ deduplication while preserving order
# because Python dictionaries retain key insertion order as a language guarantee since 3.7.


# ============================================================
# Q8: Partitioning a List by Predicate in a Single Pass
# ============================================================
# Question: Partition a list into two sub-lists: elements satisfying a condition
# and elements failing it, in a single O(N) pass.

print("\n=== Q8: List Partitioning by Predicate ===")

def partition(lst: list, predicate) -> tuple[list, list]:
    """Splits lst into (matching, non_matching) in a single pass."""
    matching = []
    non_matching = []
    for item in lst:
        if predicate(item):
            matching.append(item)
        else:
            non_matching.append(item)
    return matching, non_matching

accounts = [
    {"user": "u1", "balance": 150.0, "active": True},
    {"user": "u2", "balance": -20.0, "active": True},
    {"user": "u3", "balance": 500.0, "active": False},
    {"user": "u4", "balance": 0.0,   "active": True},
    {"user": "u5", "balance": -80.0, "active": False},
]

# Partition by active status
active_users, inactive_users = partition(accounts, lambda u: u["active"])
print(f"  Active Accounts ({len(active_users)}):   {[u['user'] for u in active_users]}")
print(f"  Inactive Accounts ({len(inactive_users)}): {[u['user'] for u in inactive_users]}")

# Partition by positive balance
solvent, indebted = partition(accounts, lambda u: u["balance"] >= 0)
print(f"  Solvent Accounts:   {[u['user'] for u in solvent]}")
print(f"  Indebted Accounts:  {[u['user'] for u in indebted]}")

# Explanation: Single-pass partitioning iterates the list once ($O(N)$) and directs each
# element to its designated bucket without multiple full-array scans.


# ============================================================
# Q9: Multiset / Bag Arithmetic on Lists (Preserving Counts)
# ============================================================
# Question: Implement multiset intersection and difference on lists where duplicate
# counts are respected (e.g. [A, A, B] intersect [A, B, B] = [A, B]).

print("\n=== Q9: Multiset List Arithmetic ===")

from collections import Counter

def multiset_intersection(list_a: list, list_b: list) -> list:
    """Computes multiset intersection taking min counts."""
    count_a = Counter(list_a)
    count_b = Counter(list_b)
    common = count_a & count_b  # Min count operator
    return list(common.elements())

def multiset_difference(list_a: list, list_b: list) -> list:
    """Computes multiset difference (A - B) taking max(0, count_a - count_b)."""
    count_a = Counter(list_a)
    count_b = Counter(list_b)
    diff = count_a - count_b  # Keeps only positive counts
    return list(diff.elements())

inv_warehouse = ["screw", "screw", "screw", "bolt", "bolt", "nut"]
inv_needed    = ["screw", "screw", "bolt", "washer"]

fulfilled = multiset_intersection(inv_warehouse, inv_needed)
remaining_stock = multiset_difference(inv_warehouse, inv_needed)

print(f"  Warehouse Inventory: {inv_warehouse}")
print(f"  Order Needed:        {inv_needed}")
print(f"  Fulfilled from stock: {fulfilled}")
print(f"  Remaining in stock:   {remaining_stock}")

# Explanation: Unlike mathematical sets which discard cardinality, multisets (bags)
# model physical inventories where having 3 items vs 1 item is critically distinct.


# ============================================================
# Q10: In-Place Two-Pointer Deduplication (LeetCode #26 Pattern)
# ============================================================
# Question: Given a SORTED list, remove duplicates in-place with O(1) auxiliary memory.
# Do not allocate a new list. Return the length K of the unique prefix.

print("\n=== Q10: In-Place Two-Pointer Deduplication ===")

def remove_duplicates_sorted_inplace(nums: list[int]) -> int:
    """Overwrites duplicate elements in-place using two-pointer technique.
    Returns k, the count of unique elements."""
    if not nums:
        return 0
        
    write_ptr = 1  # Index where the next unique element should be placed
    
    # read_ptr scans forward through the array
    for read_ptr in range(1, len(nums)):
        if nums[read_ptr] != nums[read_ptr - 1]:
            nums[write_ptr] = nums[read_ptr]
            write_ptr += 1
            
    return write_ptr

sorted_with_dups = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
print(f"  Original sorted array: {sorted_with_dups}")

k_unique = remove_duplicates_sorted_inplace(sorted_with_dups)
print(f"  Unique count k:        {k_unique}")
print(f"  Array prefix [0:{k_unique}]:   {sorted_with_dups[:k_unique]}")

# Truncate the list in-place to unique elements
del sorted_with_dups[k_unique:]
print(f"  Truncated in-place list: {sorted_with_dups}")

# Summary Output
print("\n" + "=" * 55)
print("  All 10 Questions for Topic 03 - Q02 executed successfully!")
print("=" * 55)
