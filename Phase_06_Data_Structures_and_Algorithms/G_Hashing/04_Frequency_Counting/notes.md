# Frequency Counting

## 1. Introduction

**Frequency Counting** is one of the most ubiquitous algorithmic paradigms in computer science. It involves aggregating the occurrence counts of elements (characters, integers, tokens, or states) into a hash map or fixed-size lookup table.

Frequency counting transforms unstructured sequences into structured distributions, enabling optimal solutions to problems such as anagram detection, top-k frequent elements, majority elements, and frequency-based filtering in linear **$O(n)$** time.

---

## 2. Why Use Frequency Counting?

| Problem Type | Naive Approach | Frequency Counting Approach | Time Improvement |
|---|---|---|---|
| **Top K Frequent Elements** | Sort elements ($O(n \log n)$) | Bucket Inversion ($O(n)$) | $O(n \log n) \to O(n)$ |
| **Anagram Check** | Sort strings ($O(k \log k)$) | 26-element count array ($O(k)$) | Eliminates sorting overhead |
| **Group Anagrams** | Sort each word ($O(n \cdot k \log k)$) | Count tuple hash key ($O(n \cdot k)$) | Linear in total characters |
| **First Unique Element** | Nested iteration ($O(n^2)$) | Two-pass frequency count ($O(n)$) | Quadratic to linear |
| **Majority Element** | Count per element ($O(n^2)$) | Hash Map count / Boyer-Moore ($O(n)$) | Single pass lookup |

---

## 3. Syntax / API Reference

```python
from collections import Counter, defaultdict

# Built-in Counter
counts = Counter("abracadabra")
counts['a']                # Returns 5
counts['z']                # Returns 0 (missing keys default to 0)
counts.most_common(2)      # Returns [('a', 5), ('b', 2)]

# Defaultdict integer counting
freq = defaultdict(int)
for x in array:
    freq[x] += 1

# Fixed-size alphabet frequency array
alpha_counts = [0] * 26
for char in word:
    alpha_counts[ord(char) - ord('a')] += 1
```

---

## 4. Key Algorithmic Patterns

### 1. Bucket Sort Frequency Inversion ($O(n)$)
To find Top $K$ frequent items without sorting or heaps:
1. Count frequencies using a hash map: `counts = Counter(nums)`.
2. Create an array of buckets of size $n + 1$, where `buckets[freq]` stores a list of elements having that exact frequency.
3. Traverse buckets backwards from index $n$ down to 1, collecting elements until $K$ elements are accumulated.

### 2. Frequency Tuple Signature for Equivalence Classes
Group strings by creating a fixed-length tuple of character counts:
```python
signature = tuple(count_array)  # Hashable, can serve as dict key
groups[signature].append(word)
```

### 3. Two-Pass Frequency Inspection
- **Pass 1:** Populate the frequency map.
- **Pass 2:** Iterate through the original sequence in order and inspect the frequency map to identify the first unique element or meeting specific frequency thresholds.

---

## 5. Examples

### Example 1: Top K Frequent Elements via Bucket Inversion
```python
def top_k_frequent(nums, k):
    counts = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in counts.items():
        buckets[freq].append(num)

    result = []
    for freq in range(len(buckets) - 1, 0, -1):
        for num in buckets[freq]:
            result.append(num)
            if len(result) == k:
                return result
    return result
```

### Example 2: Group Anagrams via 26-Tuple Count Key
```python
def group_anagrams(strs):
    groups = defaultdict(list)
    for word in strs:
        count = [0] * 26
        for ch in word:
            count[ord(ch) - ord('a')] += 1
        groups[tuple(count)].append(word)
    return list(groups.values())
```

### Example 3: First Unique Character & Boyer-Moore Majority
```python
def first_unique_char(s):
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1

def majority_element(nums):
    candidate, count = None, 0
    for num in nums:
        if count == 0:
            candidate = num
        count += (1 if num == candidate else -1)
    return candidate
```

---

## 6. Output

```
1. Top K Frequent:
   nums = [1, 1, 1, 2, 2, 3], k = 2 -> [1, 2]

2. Anagram Grouping:
   ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']
   -> [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]

3. First Unique Character:
   'leetcode' -> index 0 ('l')
   'loveleetcode' -> index 2 ('v')

4. Majority Element:
   [2, 2, 1, 1, 1, 2, 2] -> 2
```

---

## 7. Code Explanation

| Component | Responsibility |
|---|---|
| `Counter(nums)` | Single-pass hash map populating item frequencies |
| `buckets[freq].append(num)` | Frequency-indexed array mapping counts back to elements |
| `tuple(count)` | Converts mutable array into immutable hashable key for dictionary grouping |
| `ord(ch) - ord('a')` | Maps lowercase ASCII character to direct $0..25$ array offset |
| `count += (1 if num == candidate else -1)` | Cancels out non-majority occurrences in Boyer-Moore |

---

## 8. Common Mistakes

1. **Mutable Array as Dictionary Key**:
   Trying to use a `list` as a dict key raises `TypeError: unhashable type: 'list'`. Always wrap in `tuple()`.
2. **Off-by-One in Bucket Array Size**:
   Allocating `len(nums)` instead of `len(nums) + 1` causes an `IndexError` when an element appears with frequency equal to `len(nums)`.
3. **Overusing Heaps for Top-K**:
   Using a heap takes $O(n \log k)$. For integer frequency bounded by array length $n$, bucket sort achieves strictly linear $O(n)$ runtime.
4. **Incorrect Space Complexity Claims**:
   Claiming a 26-letter frequency array is $O(n)$ space. It is actually $O(1)$ auxiliary space because the alphabet size is constant.
5. **Modifying Counter in a Loop**:
   Deleting keys from a `Counter` or `dict` during iteration triggers a `RuntimeError`.

---

## 9. Practice Questions

1. Implement **Sort Characters By Frequency** in $O(n)$ using frequency bucket sorting.
2. Find the minimum window substring containing all characters of pattern $T$ using frequency balancing.
3. Solve **Majority Element II** (elements appearing more than $\lfloor n / 3 \rfloor$ times) using extended Boyer-Moore voting.
4. Determine if a string can be rearranged into a palindrome by checking character frequency parities.
5. Implement a frequency stack (`FreqStack`) that pushes and pops the most frequent element in $O(1)$ time.

---

## 10. Interview Questions

**Q1: How does bucket sort achieve $O(n)$ time for Top K Frequent Elements?**
Since an element's frequency can range at most from $1$ to $n$, we allocate an array of $n + 1$ buckets. Inverting the frequency map takes $O(n)$, and scanning buckets from $n$ down to $1$ takes $O(n)$, yielding overall $O(n)$ time.

**Q2: Why use a 26-tuple instead of sorted string as the hash key in Group Anagrams?**
Sorting a string of length $k$ takes $O(k \log k)$ time. Counting frequencies takes $O(k)$ time. For long strings, the $O(k)$ frequency tuple key significantly outperforms sorting.

**Q3: When does Boyer-Moore Voting Algorithm fail?**
It only guarantees finding the majority element if one actually exists with frequency $> \lfloor n / 2 \rfloor$. If no majority element exists, it may return an arbitrary candidate; a second confirmation pass is required.

**Q4: What is the difference between `defaultdict(int)` and `Counter`?**
Both return `0` for missing keys, but `Counter` provides specialized multiset operations like `.most_common()`, mathematical arithmetic (`+`, `-`, `&`, `|`), and subtractive updates.

**Q5: Can frequency counting handle stream data with infinite elements?**
No, an unbounded hash map requires $O(U)$ memory for $U$ unique elements. For infinite streams, probabilistic counting structures like Count-Min Sketch or Misra-Gries algorithms must be used.
