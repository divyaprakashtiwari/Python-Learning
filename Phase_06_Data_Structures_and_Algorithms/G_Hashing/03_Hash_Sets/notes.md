# Hash Sets

## 1. Introduction

A **Hash Set** is an unordered collection of unique elements implemented using an underlying hash table. In Python, it is provided by the built-in `set` (and immutable `frozenset`) type.

Hash sets store only distinct keys without associated values. They provide average **O(1)** time complexity for search (`in`), insertion (`add`), and deletion (`remove`/`discard`), making them the standard choice for deduplication, membership testing, sliding window uniqueness tracking, and cycle detection.

---

## 2. Why Use Hash Sets?

| Problem Type | Standard Array Time | Hash Set Time | Advantage |
|---|---|---|---|
| **Membership Testing (`x in S`)** | $O(n)$ | $O(1)$ | Instant lookup regardless of collection size |
| **Deduplication** | $O(n^2)$ or $O(n \log n)$ | $O(n)$ | Remove duplicates in a single pass |
| **Intersection / Union** | $O(n \cdot m)$ | $O(n + m)$ | Fast mathematical set operations |
| **Sliding Window Uniqueness** | $O(k)$ per step | $O(1)$ per step | Constant-time duplicate detection |
| **Cycle Detection** | $O(n)$ space / cycle check | $O(1)$ lookup | Catch repeated states in infinite sequences |

---

## 3. Syntax / API Reference

```python
# Initialization
s = set()
s = {1, 2, 3}

# Modifying Elements
s.add(4)
s.remove(2)     # Raises KeyError if 2 is absent
s.discard(99)   # Does not raise error if missing
elem = s.pop()  # Removes and returns arbitrary element

# Mathematical Operations
union = s1 | s2          # or s1.union(s2)
intersection = s1 & s2   # or s1.intersection(s2)
difference = s1 - s2     # or s1.difference(s2)
sym_diff = s1 ^ s2       # or s1.symmetric_difference(s2)
subset = s1 <= s2        # or s1.issubset(s2)
```

---

## 4. Key Algorithmic Patterns

### 1. Sliding Window with Hash Set
Maintain elements present within the current window $[L, R]$. When a duplicate element is encountered at $R$, increment $L$ and remove elements from the set until uniqueness is restored.
```
Window: [L ... R]
While nums[R] in seen:
    seen.remove(nums[L])
    L += 1
seen.add(nums[R])
```

### 2. State & Cycle Detection (Happy Number / Graph Visited)
To detect cycles in dynamic state transformations (e.g., $x \to f(x)$), record each visited state in a set. If $f(x)$ was already seen, a cycle exists.

### 3. k-Sized Fixed Sliding Window Set
To check if duplicate values exist within distance $k$: maintain a set containing at most $k$ elements. If `len(set) > k`, remove `nums[i - k]`.

---

## 5. Examples

### Example 1: Contains Duplicate and Nearby Duplicate
```python
def contains_nearby_duplicate(nums, k):
    window = set()
    for i, x in enumerate(nums):
        if x in window:
            return True
        window.add(x)
        if len(window) > k:
            window.remove(nums[i - k])
    return False
```

### Example 2: Longest Substring Without Repeating Characters
```python
def length_of_longest_substring(s):
    seen = set()
    left = 0
    max_len = 0
    for right in range(len(s)):
        while s[right] in seen:
            seen.remove(s[left])
            left += 1
        seen.add(s[right])
        max_len = max(max_len, right - left + 1)
    return max_len
```

### Example 3: Cycle Detection with Happy Number
```python
def is_happy(n):
    def next_num(num):
        total = 0
        while num > 0:
            num, d = divmod(num, 10)
            total += d * d
        return total

    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = next_num(n)
    return n == 1
```

---

## 6. Output

```
1. Contains Nearby Duplicate:
   nums = [1, 2, 3, 1], k = 3 -> True
   nums = [1, 2, 3, 1, 2, 3], k = 2 -> False

2. Longest Substring Without Repeating Characters:
   s = 'abcabcbb' -> Length: 3 ('abc')
   s = 'pwwkew'   -> Length: 3 ('wke')

3. Happy Number:
   19 -> True (19 -> 82 -> 68 -> 100 -> 1)
   2  -> False (cycles infinitely: 2, 4, 16, 37, 58, 89, 145, 42, 20, 4...)
```

---

## 7. Code Explanation

| Operation | Explanation |
|---|---|
| `seen.add(x)` | Hashes `x` and stores it into the bucket table |
| `window.remove(nums[i - k])` | Maintains invariant that set only contains elements within index distance $k$ |
| `while s[right] in seen:` | Shrinks sliding window from left until duplicate is evicted |
| `seen.add(n)` in cycle check | Saves previous numerical states to avoid infinite loops |
| `s1 & s2` | Iterates through smaller set and tests presence in larger set ($O(\min(|s1|, |s2|))$) |

---

## 8. Common Mistakes

1. **Attempting to Add Mutable Items**:
   Sets require elements to be hashable. Adding a `list` or `set` raises `TypeError: unhashable type`. Use `tuple` or `frozenset`.
2. **Confusing `remove()` and `discard()`**:
   `remove(x)` raises a `KeyError` if $x$ is not present; `discard(x)` silently ignores absent keys.
3. **Empty Set Literal Mistake**:
   Writing `{}` creates an empty dictionary, not an empty set. Always use `set()`.
4. **Expecting Ordered Elements**:
   Sets do not guarantee order. Iteration order depends on bucket layout and Python's hash seed.
5. **Set Mutation During Iteration**:
   Adding or removing elements while iterating over a set triggers a `RuntimeError: Set changed size during iteration`.

---

## 9. Practice Questions

1. Given two integer arrays, return an array of their intersection where each element is unique.
2. Implement **Single Number** ($O(n)$ time, $O(1)$ space using bitwise XOR vs $O(n)$ space using a hash set).
3. Find all numbers disappeared in an array $[1, n]$ using a hash set in $O(n)$ time.
4. Check if an array can be divided into pairs whose sums are divisible by $k$ using a hash set / frequency remainder set.
5. Implement a bloom filter probabilistic set using multiple hash functions.

---

## 10. Interview Questions

**Q1: How does Python's `set` differ from `dict` under the hood?**
A `set` is effectively a `dict` where only keys exist and values are ignored (implemented with a dummy value pointer in CPython), sharing the same hash-table mechanics.

**Q2: What is the time complexity of set union and intersection?**
For sets $A$ and $B$, union $A \cup B$ takes $O(|A| + |B|)$ time. Intersection $A \cap B$ takes $O(\min(|A|, |B|))$ time because Python iterates over the smaller set and checks membership in the larger.

**Q3: Can a `frozenset` be used as a set element or dictionary key?**
Yes. `frozenset` is an immutable variant of `set` that implements `__hash__`, allowing it to be inserted into sets or used as a hash map key.

**Q4: How does cycle detection in Happy Number compare to Floyd's Cycle Detection?**
Both detect cycles. The hash set uses $O(k)$ auxiliary space and $O(1)$ lookup, while Floyd's Tortoise and Hare pointer algorithm uses $O(1)$ auxiliary space and $O(k)$ steps.

**Q5: What happens when two different objects produce the same hash code in a set?**
Python verifies equality with `==`. If the hashes match but `a == b` is False, the collision resolution algorithm (open addressing with perturbation) probes for the next slot.
