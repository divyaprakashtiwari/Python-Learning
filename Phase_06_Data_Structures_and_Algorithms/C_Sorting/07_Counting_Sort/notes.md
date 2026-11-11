# Section C: Sorting — Topic 07: Counting Sort

## 1. Introduction

Every sorting algorithm we have studied so far (Bubble, Selection, Insertion, Merge, Quick, and Heap Sort) is a **Comparison-Based Sort** that determines order by comparing pairs of elements (`a[i] < a[j]`). Information theory proves that any comparison-based sort requires at least $\Omega(N \log N)$ comparisons in the worst case ($\log_2(N!) = \Theta(N \log N)$).

**Counting Sort** shatters the $\Omega(N \log N)$ barrier and runs in **$O(N + K)$ linear time** (where $K$ is the range of integer keys `max_val - min_val + 1`) because it **never compares two elements against each other**! Instead, it uses the integer keys directly as **array indices** in a frequency table (`counts`), computes cumulative prefix sums to determine each key's exact starting/ending output index, and places every record directly into its sorted slot.

---

## 2. Why is it used?

1. **True $O(N)$ Linear-Time Sorting for Bounded Integer Keys:**
   When sorting $N = 10,000,000$ exam scores (`0..100`), customer ages (`0..120`), HTTP status codes (`100..599`), or ASCII/byte values (`0..255`), $K$ is a tiny constant ($K \le 600$), so $O(N + K) = O(N)$ beats any $O(N \log N)$ comparison sort!
2. **The Core Engine of Radix Sort:**
   Standalone Counting Sort cannot sort 32-bit integers ($K = 2^{32} \approx 4.29 \times 10^9$ buckets would consume 16 GB of RAM). **LSD Radix Sort** solves this by calling **Stable Counting Sort** once per digit (in base $10$, $16$, or $256$), sorting 32-bit integers in just 4 passes ($b = 256$) in $O(N)$ linear time!
3. **Guaranteed Stability:**
   By accumulating prefix sums and traversing the input array **backward** (`n - 1` down to `0`), Counting Sort preserves the exact relative order of records with equal keys.

---

## 3. Syntax & Core Blueprints

### Blueprint 1: Generalized Stable Counting Sort (Supports Negative Integers)
```python
def counting_sort_stable(arr: list[int]) -> list[int]:
    if not arr:
        return []
    min_val, max_val = min(arr), max(arr)
    k_range = max_val - min_val + 1

    # Step 1: Frequency count
    counts = [0] * k_range
    for x in arr:
        counts[x - min_val] += 1

    # Step 2: Cumulative prefix sums (counts[b] = number of elements <= b + min_val)
    for b in range(1, k_range):
        counts[b] += counts[b - 1]

    # Step 3: Place elements backward into output array to guarantee stability
    output = [0] * len(arr)
    for i in range(len(arr) - 1, -1, -1):
        x = arr[i]
        bucket = x - min_val
        counts[bucket] -= 1
        output[counts[bucket]] = x

    return output
```

---

## 4. Step-by-Step Explanation & Complexity Analysis

### Why Step 3 Traverses the Input Array BACKWARD (`n - 1` down to `0`)
Suppose we sort two records with the same score `85`: `[(Aarav, 85), (Rohan, 85)]`, and cumulative `counts[85] = 4` (meaning the two `85`s belong at output indices `2` and `3`):
- Because `counts[85]` points to **one past the last slot** (`4`), the **first** `85` we place will decrement `counts[85]` to `3` (the **rightmost** slot of the `85` group), and the **second** `85` we place will decrement `counts[85]` to `2` (the **leftmost** slot of the `85` group).
- Therefore, by scanning the input **from right to left (`n - 1` down to `0`)**, `(Rohan, 85)` is processed first and placed at index `3`, while `(Aarav, 85)` is processed second and placed at index `2` — preserving `(Aarav, 85)` before `(Rohan, 85)` (**FIFO stability**)!

### Complexity Summary

| Metric | Complexity | Explanation |
| :--- | :--- | :--- |
| **Time Complexity (Best / Avg / Worst)** | $\Theta(N + K)$ | $O(N)$ to count + $O(K)$ prefix sum + $O(N)$ output placement |
| **Auxiliary Space Complexity** | $\Theta(N + K)$ | `output` array of size $N$ + `counts` array of size $K = \max - \min + 1$ |
| **Stable?** | **Yes** | Guaranteed by prefix sums + backward input traversal |

---

## 5. Practical Examples (3 Complete Programs)

### Example 1: Basic Frequency vs Prefix-Sum Stable Counting Sort (`example_01_frequency_and_prefix_sum_stable_counting_sort.py`)
```python
def stable_counting_sort_records(
    records: list[ExamSubmission], max_score: int
) -> list[ExamSubmission]:
    n = len(records)
    if n <= 1:
        return records.copy()

    counts = [0] * (max_score + 1)
    for rec in records:
        counts[rec.score] += 1

    for k in range(1, max_score + 1):
        counts[k] += counts[k - 1]

    output: list[ExamSubmission] = [None] * n  # type: ignore[list-item]
    for i in range(n - 1, -1, -1):
        rec = records[i]
        counts[rec.score] -= 1
        target_idx = counts[rec.score]
        output[target_idx] = rec

    return output
```

### Example 2: Offset Counting Sort for Negative Numbers & Shifted Ranges (`example_02_negative_numbers_and_offset_counting_sort.py`)
```python
def counting_sort_with_negatives(arr: list[int]) -> tuple[list[int], int]:
    if not arr:
        return [], 0

    min_val = min(arr)
    max_val = max(arr)
    k_range = max_val - min_val + 1

    counts = [0] * k_range
    for x in arr:
        counts[x - min_val] += 1

    for idx in range(1, k_range):
        counts[idx] += counts[idx - 1]

    output = [0] * len(arr)
    for i in range(len(arr) - 1, -1, -1):
        x = arr[i]
        bucket = x - min_val
        counts[bucket] -= 1
        output[counts[bucket]] = x

    return output, k_range
```

### Example 3: LSD Radix Sort Using Stable Counting Sort (`example_03_lsd_radix_sort_using_stable_counting_sort.py`)
```python
def lsd_radix_sort(arr: list[int], trace: bool = False) -> list[int]:
    if not arr:
        return []
    a = arr.copy()
    max_num = max(a)
    exp = 1
    pass_num = 0

    while max_num // exp > 0:
        pass_num += 1
        a = counting_sort_by_digit(a, exp, base=10)
        if trace:
            print(f"  Pass {pass_num} (place value {exp:>4}s): {a}")
        exp *= 10

    return a
```

---

## 6. Verified Console Output

### Output of `example_01_frequency_and_prefix_sum_stable_counting_sort.py`
```text
========================================================================
1. BASIC FREQUENCY COUNTING SORT O(N + K)
========================================================================
Dice Rolls (N=12, K=6) : [4, 2, 6, 1, 4, 3, 2, 6, 5, 1, 2, 4]
Sorted Rolls               : [1, 1, 2, 2, 2, 3, 4, 4, 4, 5, 6, 6]

========================================================================
2. STABLE PREFIX-SUM COUNTING SORT ON OBJECT RECORDS
========================================================================
  Score: 78 | Student: Meera  | Submission #4
  Score: 85 | Student: Aarav  | Submission #1
  Score: 85 | Student: Rohan  | Submission #3
  Score: 85 | Student: Ananya | Submission #6
  Score: 92 | Student: Priya  | Submission #2
  Score: 92 | Student: Kabir  | Submission #5
```

### Output of `example_02_negative_numbers_and_offset_counting_sort.py`
```text
========================================================================
1. OFFSET COUNTING SORT WITH NEGATIVE TEMPERATURES
========================================================================
Input Temperatures : [-5, -12, 0, 8, -5, 14, -12, 3, 0, -2, 8, -15]
Min = -15, Max = 14 -> Allocated K = 30 buckets
Sorted Temperatures: [-15, -12, -12, -5, -5, -2, 0, 0, 3, 8, 8, 14]

========================================================================
2. SHIFTED RANGE EXAMPLE: HIGH-PORT NUMBERS [8000 .. 8010]
========================================================================
Input Ports        : [8008, 8001, 8005, 8000, 8010, 8001, 8005]
Allocated Buckets  : 11 (instead of 8011 buckets!)
Sorted Ports       : [8000, 8001, 8001, 8005, 8005, 8008, 8010]
```

### Output of `example_03_lsd_radix_sort_using_stable_counting_sort.py`
```text
========================================================================
1. LSD RADIX SORT powered by STABLE COUNTING SORT SUBROUTINE
========================================================================
Unsorted Invoices (N=10): [170, 45, 75, 90, 802, 24, 2, 66, 519, 304]

  Pass 1 (place value    1s): [170, 90, 802, 2, 24, 304, 45, 75, 66, 519]
  Pass 2 (place value   10s): [802, 2, 304, 519, 24, 45, 66, 170, 75, 90]
  Pass 3 (place value  100s): [2, 24, 45, 66, 75, 90, 170, 304, 519, 802]

Final Sorted Invoices    : [2, 24, 45, 66, 75, 90, 170, 304, 519, 802]
```

---

## 7. Code Explanation

1. **Why Offset Shifting (`x - min_val`) Saves Both Time and Memory:**
   Look at `[8008, 8001, 8005, 8000, 8010, 8001, 8005]`. Without subtracting `min_val = 8000`, `counts` would allocate `8011` buckets (`0..8010`), wasting `8000` unused slots. Subtracting `min_val` allocates only `8010 - 8000 + 1 = 11` buckets and seamlessly handles negative numbers (`x - (-15) = x + 15`)!
2. **Why LSD Radix Sort Fails If Counting Sort Is Unstable:**
   In Pass 1 (`1s` place), `45` and `75` both have last digit `5`. In Pass 2 (`10s` place), `45` (tens digit `4`) is placed before `75` (tens digit `7`). In Pass 3 (`100s` place), **both `45` and `75` have hundreds digit `0`!** Only because Pass 3's Counting Sort is **stable** does `45` stay before `75` when tied on the hundreds digit!

---

## 8. Common Mistakes

1. **Running Counting Sort When $K \gg N$ (e.g., `[1, 1_000_000_000]`):**
   For a 2-element list `[1, 10^9]`, $K = 10^9$ allocates a 1-billion-element list (`~8 GB` in Python) and raises `MemoryError` or freezes the machine! Only use standalone Counting Sort when $K = O(N)$; otherwise use Radix Sort or comparison-based $O(N \log N)$ sort.
2. **Iterating Forward (`for i in range(n):`) in Step 3 When Stability Is Required:**
   Iterating forward while decrementing `counts[key]` reverses the order of duplicate elements (`LIFO` instead of `FIFO`), breaking stability and breaking LSD Radix Sort!

---

## 9. Practice Questions

1. **Easy — Height Checker / Relative Sort Array (LeetCode 1051 / 1122):** Given `heights` where `1 <= heights[i] <= 100`, use Counting Sort in $O(N + 100)$ time (instead of $O(N \log N)$ `sorted()`) to count how many indices differ from the expected non-decreasing order.
2. **Medium — H-Index in $O(N)$ Time via Bucket Counting (LeetCode 274):** Given an array of `citations` for $N$ papers, cap any citation count $> N$ at bucket $N$ (`counts[min(c, N)] += 1`) and scan backward from $N$ down to $0$ to find the researcher's H-Index in $O(N)$ time and space.
3. **Hard — Maximum Gap in $O(N)$ Linear Time (LeetCode 164):** Given an unsorted array `nums`, return the maximum difference between two successive elements in its sorted form in $O(N)$ time and space using either LSD Radix Sort (base 256) or Pigeonhole Bucket Sort.

---

## 10. Interview Questions

### Q1: How can Counting Sort achieve $O(N)$ time if the theoretical lower bound for sorting is $\Omega(N \log N)$?
**Answer:**
The $\Omega(N \log N)$ lower bound applies **strictly to the Comparison Tree Model**, where the only way an algorithm can gain information about element order is a binary yes/no comparison (`a[i] < a[j]`, yielding at most 1 bit of information per step). Counting Sort uses **direct array indexing** (`counts[x]`), where a single indexing operation branches across $K$ possible buckets at once ($\log_2 K$ bits of information per step).

### Q2: Once the `counts` prefix-sum array is built in $O(N + K)$ time, how fast can you answer a range count query *"How many elements in `arr` fall in `[L, R]`"*?
**Answer:**
In **$O(1)$ constant time!** Since `counts[x]` stores the number of elements $\le x$, the number of elements in $[L, R]$ is simply `counts[R] - counts[L - 1]` (or `counts[R]` if $L == 0$).
