# Hash Maps

## 1. Introduction

A **Hash Map** (in Python, implemented as the built-in `dict` type) is an associative key-value container offering average **O(1)** time complexity for search, insertion, and deletion operations. 

While hash tables define the foundational data structure and bucket mechanics, hash maps represent the high-level paradigm and algorithmic patterns applied to solve complex computational problems. Hash maps trade auxiliary space to achieve linear or constant runtime bounds, transforming brute-force $O(n^2)$ lookup procedures into single-pass $O(n)$ solutions.

---

## 2. Why Use Hash Maps?

| Pattern / Technique | Brute Force Time | Hash Map Time | Core Benefit |
|---|---|---|---|
| **Complement Lookup (Two Sum)** | $O(n^2)$ | $O(n)$ | Check for $(target - x)$ in $O(1)$ |
| **Prefix Sum Frequency Counting** | $O(n^2)$ | $O(n)$ | Count subarrays summing to $k$ in one pass |
| **Bijective / Isomorphic Mapping** | $O(n^2)$ | $O(n)$ | Enforce one-to-one character/word relations |
| **Equivalence Class Grouping** | $O(n^2 \cdot m)$ | $O(n \cdot m)$ | Canonical tuple hashing for anagrams/shifts |
| **Continuous Boundary Tracking** | $O(n \log n)$ | $O(n)$ | Dynamic stream sequence expansion |

---

## 3. Syntax / API Reference

```python
# Initialization
mapping = {}
counter = dict()

# Safe Key Retrieval with Defaults
val = mapping.get(key, 0)

# Set Default / Insertion
mapping.setdefault(key, []).append(item)

# Membership Check (Average O(1))
if key in mapping:
    del mapping[key]

# Iterating Keys, Values, and Key-Value Tuples
for k in mapping.keys(): ...
for v in mapping.values(): ...
for k, v in mapping.items(): ...
```

---

## 4. Key Algorithmic Patterns

### 1. Complement / Counterpart Lookup
Store previously seen elements to answer future queries instantly.
```
For element x, complement = target - x.
Check if complement in map before storing x.
```

### 2. Prefix Sum Frequency Hashing
Subarray sum between indices $i$ and $j$ equals `prefix[j] - prefix[i - 1]`.
To find subarrays where `sum == k`:
```
prefix[j] - prefix[i - 1] = k  ==>  prefix[i - 1] = prefix[j] - k
Count occurrences of (prefix[j] - k) stored in hash map.
```

### 3. Bidirectional Bijective Maps
To verify strict 1-to-1 relationships between alphabet sets (e.g. `s` and `t`), use **two** hash maps (`s_to_t` and `t_to_s`) to avoid many-to-one collisions.

---

## 5. Examples

### Example 1: Complement Lookup & Prefix Sum Subarrays
```python
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return (seen[target - x], i)
        seen[x] = i
    return None

def subarray_sum_equals_k(nums, k):
    count = 0
    curr_sum = 0
    prefix_counts = {0: 1}
    for num in nums:
        curr_sum += num
        count += prefix_counts.get(curr_sum - k, 0)
        prefix_counts[curr_sum] = prefix_counts.get(curr_sum, 0) + 1
    return count
```

### Example 2: Longest Consecutive Sequence
```python
def longest_consecutive(nums):
    num_set = set(nums)
    longest = 0
    for num in num_set:
        if num - 1 not in num_set:  # Only start at beginning of sequence
            curr = num
            streak = 1
            while curr + 1 in num_set:
                curr += 1
                streak += 1
            longest = max(longest, streak)
    return longest
```

### Example 3: Bijective Word Pattern & Isomorphism
```python
def is_isomorphic(s, t):
    if len(s) != len(t):
        return False
    s_to_t, t_to_s = {}, {}
    for c1, c2 in zip(s, t):
        if s_to_t.get(c1, c2) != c2 or t_to_s.get(c2, c1) != c1:
            return False
        s_to_t[c1] = c2
        t_to_s[c2] = c1
    return True
```

---

## 6. Output

```
1. Two Sum:
   Array: [2, 7, 11, 15], Target: 9 -> Indices: (0, 1)

2. Subarray Sum Equals K:
   Array: [1, 2, 3, -2, 1, 4, -1], k: 3 -> Subarray Count: 5

3. Longest Consecutive Sequence:
   Input: [100, 4, 200, 1, 3, 2] -> Length: 4 ([1, 2, 3, 4])

4. Isomorphic Strings:
   'egg' and 'add' -> True
   'foo' and 'bar' -> False
```

---

## 7. Code Explanation

| Component | Responsibility |
|---|---|
| `seen[x] = i` | Caches indices for instant complement retrieval |
| `prefix_counts = {0: 1}` | Initializes identity prefix for subarrays starting from index 0 |
| `num - 1 not in num_set` | Filters out non-starting elements, preventing redundant $O(n^2)$ scans |
| `(s_to_t, t_to_s)` | Enforces bijectivity (injective and surjective) mapping |
| Normalized diff tuple | Provides an invariant canonical key for equivalence grouping |

---

## 8. Common Mistakes

1. **Unidirectional Bijection Check**:
   Mapping only `s -> t` without `t -> s` mistakenly accepts `'ab' -> 'aa'`.
2. **Missing Base Prefix `{0: 1}` in Subarray Sum**:
   Omitting `{0: 1}` misses valid subarrays starting at index `0`.
3. **Redundant Iterations in Consecutive Sequences**:
   Checking sequences starting from middle elements degrades runtime from $O(n)$ to $O(n^2)$.
4. **Modifying Map during Iteration**:
   Altering keys during an active iterator loop raises a `RuntimeError`.
5. **Using Mutable Keys**:
   Lists or dicts cannot be used as map keys. Convert them to tuples or frozensets.

---

## 9. Practice Questions

1. Implement **Four Sum II** ($A[i] + B[j] + C[k] + D[l] = 0$) in $O(n^2)$ time using a hash map.
2. Given a binary array, find the maximum length of a contiguous subarray with an equal number of 0s and 1s using prefix sums.
3. Design a data structure that supports `insert`, `delete`, and `getRandom` in $O(1)$ average time.
4. Solve **Subarray Sums Divisible by K** using modulo arithmetic and hash maps.
5. Group anagrams from an array of strings in $O(n \cdot k)$ using character count tuples as keys.

---

## 10. Interview Questions

**Q1: What is the average vs worst-case time complexity of hash map operations?**
Average is $O(1)$ for insert, lookup, and delete. Worst case is $O(n)$ if all keys hash to the same bucket (severe collision degradation).

**Q2: Why must hash map keys be immutable?**
Hash maps compute a bucket index from `hash(key)`. If a key's state changes while inside the map, its hash changes, making it impossible to locate the bucket in future lookups.

**Q3: How does the prefix sum hash map find negative numbers correctly?**
Because it checks for mathematical difference (`curr_sum - k`), it does not require monotonicity (unlike two pointers / sliding window), making it correct even with negative values.

**Q4: How does Python's dictionary maintain insertion order?**
Since Python 3.6/3.7, dicts use a compact array of entries storing `(hash, key, value)` sequentially and a sparse index table pointing to indices in that array.

**Q5: What is the difference between `dict.get(key)` and `dict[key]`?**
`dict[key]` raises `KeyError` if the key does not exist, whereas `dict.get(key, default)` returns `None` (or the supplied default) safely without raising an exception.
