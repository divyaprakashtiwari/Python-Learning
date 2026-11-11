# Section D: Arrays and Strings — Topic 03: Sliding Window

## 1. Introduction

The **Sliding Window Technique** is an optimization over contiguous subarrays or substrings that transforms **$O(N \cdot K)$ or $O(N^2)$ nested-loop brute force into a single $O(N)$ linear pass**.

Think of a window `[left .. right]` as a caterpillar crawling from left to right across the array:
- Instead of recomputing the sum, character frequency, or state of `[left .. right]` from scratch every time the window moves, we **incrementally update** the window state in $O(1)$ time by:
  1. **Expanding `right`** (`right += 1`): adding the single entering element `arr[right]` to the window state.
  2. **Shrinking `left`** (`left += 1`): removing the single leaving element `arr[left]` from the window state.

---

## 2. Why is it used?

1. **Eliminates Redundant Overlapping Work ($O(N \cdot K) \to O(N)$):**
   Two consecutive windows of size $K = 10,000$ (`arr[0..9999]` and `arr[1..10000]`) share **$9,999$ identical elements**! Re-summing all $10,000$ elements wastes $99.99\%$ of CPU work. Updating `window_sum += arr[right] - arr[right - k]` does just **1 addition and 1 subtraction** per step!
2. **Solves Variable-Length Subarray & Substring Optimization in $O(N)$ Time:**
   Problems asking for the **Longest / Shortest contiguous subarray or substring** satisfying a condition (e.g., *Longest Substring Without Repeating Characters*, *Minimum Size Subarray Sum $\ge S$*, *Minimum Window Substring*, *Max Consecutive Ones III*) are solved in $O(N)$ time.

---

## 3. Syntax & Core Blueprints

### Blueprint 1: Fixed-Size Sliding Window (Exact Window Length $K$)
```python
def fixed_sliding_window(arr: list[int], k: int) -> int:
    window_sum = sum(arr[:k])
    best = window_sum

    for right in range(k, len(arr)):
        # Add entering element arr[right], subtract leaving element arr[right - k]
        window_sum += arr[right] - arr[right - k]
        best = max(best, window_sum)

    return best
```

### Blueprint 2: Variable-Size Sliding Window (Longest Valid Window)
```python
def longest_valid_window(arr: list[int]) -> int:
    left = 0
    best_len = 0
    # Initialize window state (sum, counter, etc.)

    for right in range(len(arr)):
        # 1. Add arr[right] to window state
        while window_is_invalid():
            # 2. Remove arr[left] from window state and shrink!
            left += 1
        # 3. Window [left .. right] is now guaranteed valid!
        best_len = max(best_len, right - left + 1)

    return best_len
```

### Blueprint 3: Variable-Size Sliding Window (Shortest Valid Window)
```python
def shortest_valid_window(arr: list[int]) -> int:
    left = 0
    min_len = len(arr) + 1

    for right in range(len(arr)):
        # 1. Add arr[right] to window state
        while window_is_valid():
            # 2. Window [left .. right] is valid -> record answer, then shrink to try shorter!
            min_len = min(min_len, right - left + 1)
            # Remove arr[left] from window state
            left += 1

    return 0 if min_len > len(arr) else min_len
```

---

## 4. Step-by-Step Explanation & Complexity Analysis

### Why Variable-Size Sliding Window Is $O(N)$ — NOT $O(N^2)$!
Beginners often look at the `while` loop nested inside the `for right in range(n):` loop and assume the time complexity is $O(N^2)$.
**Use Amortized Aggregate Analysis:**
- The pointer `right` starts at `0` and increments at most $N$ times.
- The pointer `left` starts at `0`, **never moves backward**, and increments at most $N$ times across the **entire execution of the algorithm**!
- Therefore, each element `arr[i]` enters the window **once** (via `right`) and leaves the window **at most once** (via `left`):
$$\text{Total Pointer Operations} \le N_{\text{enter}} + N_{\text{leave}} = 2N = \Theta(N)$$

### Complexity Summary

| Window Pattern | Example Problem | Time Complexity | Auxiliary Space |
| :--- | :--- | :--- | :--- |
| **Fixed Window ($K$)** | Max Sum Subarray of Size $K$ | $O(N)$ | $O(1)$ |
| **Variable Shrinking (Min)** | Min Subarray Sum $\ge$ Target | $O(N)$ | $O(1)$ |
| **Variable Expanding (Max)** | Longest Unique Substring (LC 3) | $O(N)$ | $O(\min(N, |\Sigma|))$ |
| **Frequency Map Window** | Minimum Window Substring (LC 76) | $O(|S| + |T|)$ | $O(|\Sigma|)$ |

---

## 5. Practical Examples (3 Complete Programs)

### Example 1: Fixed-Size Sliding Window — Max Sum & Rolling Averages (`example_01_fixed_size_sliding_window_max_sum_and_averages.py`)
```python
def max_sum_subarray_fixed_k(
    arr: list[int], k: int
) -> tuple[int, int, list[int]]:
    n = len(arr)
    if k <= 0 or k > n:
        raise ValueError(f"Window size k={k} must be in [1 .. {n}]")

    window_sum = sum(arr[:k])
    max_sum = window_sum
    best_start = 0

    for right in range(k, n):
        window_sum += arr[right] - arr[right - k]
        if window_sum > max_sum:
            max_sum = window_sum
            best_start = right - k + 1

    return max_sum, best_start, arr[best_start : best_start + k]
```

### Example 2: Variable-Size Sliding Window — Min Subarray Sum & Longest Unique Substring (`example_02_variable_size_sliding_window_min_and_max.py`)
```python
def longest_unique_substring(s: str) -> tuple[int, str]:
    last_seen: dict[str, int] = {}
    left = 0
    best_len = 0
    best_start = 0

    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1

        last_seen[ch] = right
        curr_len = right - left + 1
        if curr_len > best_len:
            best_len = curr_len
            best_start = left

    return best_len, s[best_start : best_start + best_len]
```

### Example 3: Frequency-Map Sliding Window — All Anagrams & Minimum Window Substring (`example_03_frequency_map_anagrams_and_min_window_substring.py`)
```python
def min_window_substring(s: str, t: str) -> str:
    if not s or not t or len(t) > len(s):
        return ""

    need = Counter(t)
    required_unique = len(need)
    window: dict[str, int] = {}
    formed_unique = 0

    left = 0
    best_len = len(s) + 1
    best_slice = (0, 0)

    for right, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1
        if ch in need and window[ch] == need[ch]:
            formed_unique += 1

        while formed_unique == required_unique:
            curr_len = right - left + 1
            if curr_len < best_len:
                best_len = curr_len
                best_slice = (left, right + 1)

            leave_ch = s[left]
            window[leave_ch] -= 1
            if leave_ch in need and window[leave_ch] < need[leave_ch]:
                formed_unique -= 1
            left += 1

    return "" if best_len > len(s) else s[best_slice[0] : best_slice[1]]
```

---

## 6. Verified Console Output

### Output of `example_01_fixed_size_sliding_window_max_sum_and_averages.py`
```text
========================================================================
1. FIXED-SIZE SLIDING WINDOW: MAX SUBARRAY SUM OF SIZE K = 3
========================================================================
Hourly Traffic (N=9): [120, 340, 210, 580, 490, 150, 620, 310, 280]
Peak 3-Hour Window    : Start Index 2 -> [210, 580, 490] (Sum = 1280)

========================================================================
2. 4-DAY ROLLING MOVING AVERAGES IN O(N) TIME
========================================================================
Daily Closing Prices  : [100, 104, 108, 102, 110, 116, 112, 120]
4-Day Moving Averages : [103.5, 106.0, 109.0, 110.0, 114.5]
```

### Output of `example_02_variable_size_sliding_window_min_and_max.py`
```text
========================================================================
1. MINIMUM SIZE SUBARRAY SUM >= TARGET (SHRINKING WINDOW)
========================================================================
Input Array : [2, 3, 1, 2, 4, 3], Target >= 7
Shortest Subarray : [4, 3] (Length = 2)

========================================================================
2. LONGEST SUBSTRING WITHOUT REPEATING CHARACTERS (LC 3)
========================================================================
  'abcabcbb          ' -> Max Length:  3 | Substring: 'abc'
  'bbbbb             ' -> Max Length:  1 | Substring: 'b'
  'pwwkew            ' -> Max Length:  3 | Substring: 'wke'
  'antigravity_python' -> Max Length:  9 | Substring: 'gravity_p'
```

### Output of `example_03_frequency_map_anagrams_and_min_window_substring.py`
```text
========================================================================
1. FIND ALL ANAGRAMS IN A STRING (FIXED FREQUENCY WINDOW)
========================================================================
String: 'cbaebabacd', Pattern: 'abc'
Anagram Start Indices: [0, 6] -> ['cba', 'bac']

========================================================================
2. MINIMUM WINDOW SUBSTRING (LEETCODE 76 HARD)
========================================================================
Source s = 'ADOBECODEBANC', Target t = 'ABC'
Minimum Window Substring: 'BANC'
```

---

## 7. Code Explanation

1. **Why `if ch in last_seen and last_seen[ch] >= left:` Checks `>= left`:**
   In `longest_unique_substring("abba")`, when `right = 2` (`'b'`), `left` jumps to index `2`. Then when `right = 3` (`'a'`), `last_seen['a']` is `0`, which is **to the left of `left = 2`** (already outside our current window!). Checking `last_seen[ch] >= left` (or `left = max(left, last_seen[ch] + 1)`) prevents `left` from ever jumping backward!
2. **How `formed_unique == required_unique` Avoids $O(|\Sigma|)$ Dictionary Comparisons on Every Step:**
   In `min_window_substring`, instead of comparing the entire `window` dictionary against `need` on every step, we increment a single integer counter `formed_unique` whenever a character's count in `window` reaches its exact required count in `need`, and decrement `formed_unique` only when a required character drops below `need[leave_ch]`. That makes each step strictly $O(1)$!

---

## 8. Common Mistakes

1. **Using Variable-Size Sliding Window on Subarray Sums When the Array Contains NEGATIVE Numbers:**
   Variable-size sum windows rely on **monotonicity**: adding `nums[right]` must increase (or keep equal) `window_sum`, and removing `nums[left]` must decrease `window_sum`. If `nums` contains negative numbers (e.g., `[2, -1, 2]`), shrinking `left` can actually **increase** `window_sum`, breaking the Sliding Window invariant! For subarray sums with negative numbers, use **Prefix Sum + Hash Map** (or Prefix Sum + Monotonic Deque for shortest subarray $\ge K$, LeetCode 862).
2. **Forgetting to Delete Zero-Count Keys When Comparing Two `Counter` Objects in Python < 3.10:**
   In `find_all_anagram_indices`, when `window_count[leave_ch]` drops to `0`, deleting the key (`if window_count[leave_ch] == 0: del window_count[leave_ch]`) keeps the `dict` size bounded by $O(K)$ and ensures clean equality checks across all Python structures.

---

## 9. Practice Questions

1. **Easy — Max Consecutive Ones III (LeetCode 1004):** Given a binary array `nums` and an integer `k`, return the maximum number of consecutive `1`s in the array if you can flip at most `k` `0`s (find the longest window `[left .. right]` containing at most `k` zeros!).
2. **Medium — Longest Repeating Character Replacement (LeetCode 424):** Given a string `s` and an integer `k`, find the length of the longest substring containing the same letter you can get after replacing at most `k` characters (`(right - left + 1) - max_freq_in_window <= k`).
3. **Hard — Subarrays with Exactly $K$ Different Integers (LeetCode 992):** Write a helper `at_most_k_distinct(nums, k)` using a variable sliding window, and compute `exactly_k(nums, k) = at_most_k_distinct(nums, k) - at_most_k_distinct(nums, k - 1)` in $O(N)$ time!

---

## 10. Interview Questions

### Q1: Why can't a single standard Variable Sliding Window directly count subarrays with **EXACTLY** $K$ distinct elements (or exact sum $K$), and why does `atMost(K) - atMost(K - 1)` solve it?
**Answer:**
With an "at most $K$" constraint, validity is **monotonic**: if `[left .. right]` has $\le K$ distinct elements, then **every** suffix `[i .. right]` for `left <= i <= right` also has $\le K$ distinct elements (`right - left + 1` valid subarrays ending at `right`). With "exact $K$", shrinking `left` may keep the distinct count at $K$ for several steps before dropping to $K - 1$. Decomposing `Exact(K) = AtMost(K) - AtMost(K - 1)` restores monotonicity and solves it in two $O(N)$ passes!

### Q2: How do you find the Maximum Element in every Sliding Window of size $K$ (LeetCode 239) in $O(N)$ time?
**Answer:**
Unlike sums (`window_sum += enter - leave`), you cannot "subtract" a leaving element from `max()`! We use a **Monotonic Decreasing Deque** (covered in Section F Topic 06) that stores indices in decreasing order of their values, maintaining the window maximum at `deque[0]` in $O(1)$ amortized time per step ($O(N)$ total time).
