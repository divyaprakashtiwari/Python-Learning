# Section B: Searching — Topic 01: Linear Search (Sequential Search)

## 1. Introduction

**Linear Search** (also known as **Sequential Search**) is the most fundamental searching algorithm in computer science. Given a collection (such as a Python `list`, tuple, or unsorted stream) and a `target` value, Linear Search inspects elements one by one from left to right (`index 0` to `index n - 1`) until either:
1. An element matching `target` is found (returning its index), or
2. The end of the collection is reached without a match (returning `-1` or `None`).

Unlike Binary Search, Linear Search **does not require the data to be sorted** or even stored in contiguous memory.

---

## 2. Why is it used?

Even though $O(\log N)$ Binary Search and $O(1)$ Hash Tables exist, Linear Search remains indispensable in production software:
1. **Unsorted or One-Time Data:** Sorting an unsorted array of $N$ elements takes $O(N \log N)$ time, and building a hash set takes $O(N)$ time and $O(N)$ extra memory. If you only need to search an unsorted dataset **once** (or a few times), a single $O(N)$ Linear Search is strictly faster and uses $O(1)$ extra memory.
2. **Tiny Arrays ($N \le 32$) and CPU Cache Locality:** Modern CPUs prefetch contiguous array bytes into L1/L2 cache lines (`64 bytes` at a time). Scanning 16–32 contiguous integers sequentially has zero branch-prediction surprises and often beats binary search or hash lookups on tiny collections.
3. **Linked Lists & Generators/Streams:** Structures without $O(1)$ random index access (`singly linked lists`, file lines, network streams) *must* be searched sequentially.
4. **Complex Predicate Queries:** Finding the first server process with `cpu_percent > 80.0 and status == "running"` cannot use a single sort order unless indexed on those exact fields.

---

## 3. Syntax & Core Blueprints

### Blueprint 1: Standard Linear Search ($O(N)$ Time, $O(1)$ Space)
```python
def linear_search(arr: list[int], target: int) -> int:
    for i, val in enumerate(arr):
        if val == target:
            return i  # Early exit on match
    return -1         # Target not present
```

### Blueprint 2: Sentinel Linear Search (Eliminating Loop-Bound Checks)
```python
def sentinel_search(arr: list[int], target: int) -> int:
    n = len(arr)
    if n == 0:
        return -1
    last = arr[n - 1]
    arr[n - 1] = target  # Place sentinel at the end

    i = 0
    while arr[i] != target:
        i += 1

    arr[n - 1] = last    # Restore original last element
    if i < n - 1 or last == target:
        return i
    return -1
```

---

## 4. Step-by-Step Explanation & Complexity Analysis

### How Standard vs Sentinel Search Works
Suppose `arr = [402, 119, 875, 330, 912]` ($N = 5$) and `target = 330`:
- **Step 1 (`i = 0`):** Compare `arr[0] (402) == 330` $\rightarrow$ `False`.
- **Step 2 (`i = 1`):** Compare `arr[1] (119) == 330` $\rightarrow$ `False`.
- **Step 3 (`i = 2`):** Compare `arr[2] (875) == 330` $\rightarrow$ `False`.
- **Step 4 (`i = 3`):** Compare `arr[3] (330) == 330` $\rightarrow$ `True`! Return `3`.

Why does **Sentinel Linear Search** perform ~50% fewer comparisons in low-level loops?
- A standard `while i < n:` loop performs **two comparisons per iteration**:
  1. Bounds check: `i < n`
  2. Equality check: `arr[i] == target`
- By temporarily placing `target` at `arr[n - 1]`, the loop is **guaranteed** to find `target` at or before `n - 1`. We eliminate `i < n` inside the loop body, reducing worst-case comparisons from $2N + 1$ to $N + 2$.

### Complexity Summary

| Case | Scenario | Comparisons (Standard) | Time Complexity | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Best Case ($\Omega$)** | `target` is at index `0` | $1$ equality check | $\Omega(1)$ | $O(1)$ |
| **Average Case ($\Theta$)** | `target` is equally likely at any index | $\approx \frac{N + 1}{2}$ checks | $\Theta(N)$ | $O(1)$ |
| **Worst Case ($O$)** | `target` is at index `N - 1` or missing | $N$ equality checks | $O(N)$ | $O(1)$ |

---

## 5. Practical Examples (3 Complete Programs)

### Example 1: Standard vs Sentinel Linear Search (`example_01_standard_and_sentinel_linear_search.py`)
```python
def standard_linear_search(arr: list[int], target: int) -> tuple[int, int]:
    comparisons = 0
    n = len(arr)
    i = 0

    while True:
        comparisons += 1  # Check: i < n
        if i >= n:
            return -1, comparisons

        comparisons += 1  # Check: arr[i] == target
        if arr[i] == target:
            return i, comparisons

        i += 1


def sentinel_linear_search(arr: list[int], target: int) -> tuple[int, int]:
    n = len(arr)
    if n == 0:
        return -1, 1

    comparisons = 0
    last_element = arr[n - 1]
    arr[n - 1] = target

    i = 0
    while True:
        comparisons += 1  # Only 1 check per iteration: arr[i] == target
        if arr[i] == target:
            break
        i += 1

    arr[n - 1] = last_element

    comparisons += 1
    if i < n - 1 or last_element == target:
        return i, comparisons

    return -1, comparisons
```

### Example 2: Multi-Occurrence, 2D Unsorted Matrix, and Pairwise Min/Max (`example_02_multi_occurrence_and_2d_matrix_search.py`)
```python
def find_all_occurrences(arr: list[str], target: str) -> list[int]:
    return [index for index, value in enumerate(arr) if value == target]


def search_2d_unsorted_matrix(
    matrix: list[list[int]], target: int
) -> tuple[int, int] | None:
    for row_idx, row in enumerate(matrix):
        for col_idx, cell_value in enumerate(row):
            if cell_value == target:
                return (row_idx, col_idx)
    return None
```

### Example 3: Custom Predicate & Move-To-Front Self-Organizing Search (`example_03_custom_predicate_and_self_organizing_search.py`)
```python
def move_to_front_search(arr: list[str], target: str) -> tuple[int, int]:
    for i, val in enumerate(arr):
        if val == target:
            if i > 0:
                item = arr.pop(i)
                arr.insert(0, item)
            return i, i + 1
    return -1, len(arr)
```

---

## 6. Verified Console Output

### Output of `example_01_standard_and_sentinel_linear_search.py`
```text
========================================================================
1. STANDARD vs SENTINEL LINEAR SEARCH (COMPARISON COUNT BENCHMARK)
========================================================================
Array (n=10): [402, 119, 875, 330, 912, 654, 208, 741, 559, 183]

Scenario                       | Target |  Idx | Standard Comps | Sentinel Comps
------------------------------------------------------------------------------
First element (Best Case)      |    402 |    0 |              2 |              2
Middle element (Index 4)       |    912 |    4 |             10 |              6
Last element (Index 9)         |    183 |    9 |             20 |             11
Missing element (Worst Case)   |    999 |   -1 |             21 |             11

Key Insight:
  Standard Linear Search executes ~2N comparisons in the worst case (bound + equality).
  Sentinel Linear Search executes ~N + 2 comparisons by eliminating the loop-bound check!
```

### Output of `example_02_multi_occurrence_and_2d_matrix_search.py`
```text
========================================================================
1. FINDING ALL OCCURRENCES OF A TARGET IN LOG STREAM
========================================================================
Status Stream       : ['200', '200', '500', '404', '200', '500', '201', '500']
Indices of '500'    : [2, 5, 7] (Count: 3)

========================================================================
2. UNSORTED 2D MATRIX LINEAR SEARCH O(R * C)
========================================================================
  Searching for 23 -> Coordinates (row, col): (1, 2)
  Searching for 42 -> Coordinates (row, col): (2, 2)
  Searching for 99 -> Coordinates (row, col): None

========================================================================
3. PAIRWISE MIN & MAX IN A SINGLE LINEAR SCAN (1.5N COMPARISONS)
========================================================================
Readings (n=10)      : [42, 19, 88, 7, 63, 95, 31, 12, 54, 76]
Minimum = 7, Maximum = 95
Pairwise Comparisons : 13 (vs 18 in naive 2*(n-1) scan)
```

### Output of `example_03_custom_predicate_and_self_organizing_search.py`
```text
========================================================================
1. PREDICATE-BASED LINEAR SEARCH ON OBJECT RECORDS
========================================================================
First high-CPU process (>80%): Index 2 -> ServerProcess(pid=1089, name='worker_etl', cpu_percent=92.4, status='running')
First sleeping process       : Index 3 -> ServerProcess(pid=1104, name='redis', cpu_percent=2.1, status='sleeping')

========================================================================
2. SELF-ORGANIZING LINEAR SEARCH (MOVE-TO-FRONT CACHE HEURISTIC)
========================================================================
Initial List : ['theme', 'locale', 'timezone', 'api_timeout', 'feature_flag_x']
  Query 1: 'feature_flag_x' found at idx 4 (5 comps) -> Updated List: ['feature_flag_x', 'theme', 'locale', 'timezone', 'api_timeout']
  Query 2: 'feature_flag_x' found at idx 0 (1 comps) -> Updated List: ['feature_flag_x', 'theme', 'locale', 'timezone', 'api_timeout']
  Query 3: 'api_timeout   ' found at idx 4 (5 comps) -> Updated List: ['api_timeout', 'feature_flag_x', 'theme', 'locale', 'timezone']
  Query 4: 'feature_flag_x' found at idx 1 (2 comps) -> Updated List: ['feature_flag_x', 'api_timeout', 'theme', 'locale', 'timezone']
Total comparisons across 4 queries with MTF: 13 (vs 19 without MTF)
```

---

## 7. Code Explanation

1. **Sentinel Restoration (`arr[n - 1] = last_element`):** In `sentinel_linear_search`, we temporarily overwrite `arr[n - 1]` with `target` so the `while` loop never reads out of bounds. Before returning, we **must** restore `arr[n - 1] = last_element` so the caller's list is not mutated.
2. **Pairwise Min/Max Trick ($1.5N$ vs $2N$ comparisons):** A naive scan compares every element against `current_min` AND against `current_max` ($2(N - 1)$ comparisons). By taking elements in pairs `(a, b)`, we first compare `a < b` (1 comparison), then compare the smaller one only against `current_min` (1 comparison) and the larger one only against `current_max` (1 comparison) — 3 comparisons per 2 elements, or $\frac{3}{2}N$ total!
3. **Self-Organizing Search (Move-To-Front / Transposition):** Real-world queries follow a Pareto distribution (80% of searches ask for 20% of the items). Moving accessed items to the front (`MTF`) or swapping them one step left (`Transposition`) keeps hot items near index `0` without maintaining a separate hash table.

---

## 8. Common Mistakes

1. **Returning `-1` Inside the `else` Clause of the `if` Check:**
   ```python
   # WRONG: Only inspects index 0!
   for i, x in enumerate(arr):
       if x == target:
           return i
       else:
           return -1  # Bug: exits immediately on first mismatch!
   ```
   Always place `return -1` **outside** and **after** the `for` loop.
2. **Calling `list.index(x)` Without Handling `ValueError`:** Python's built-in `arr.index(target)` performs a C-speed linear search, but raises `ValueError` if `target` is absent instead of returning `-1`. Either guard with `if target in arr:` (which does two linear scans!) or wrap `arr.index(target)` in `try...except ValueError`.
3. **Using Linear Search Repeatedly Inside a Loop ($O(N^2)$ Trap):**
   Checking `if x in large_list:` inside a loop over $M$ queries takes $O(M \cdot N)$ time. If $M$ is large ($M > \log N$), convert `large_list` to a `set` once ($O(N)$) so each lookup is $O(1)$, reducing total time to $O(N + M)$.

---

## 9. Practice Questions

1. **Easy — Last Occurrence Without Reversing Copy:** Write a function `find_last_occurrence(arr: list[int], target: int) -> int` that returns the **highest index** where `target` appears (or `-1` if missing) by scanning backward from `len(arr) - 1` down to `0` in $O(1)$ space. Explain why scanning backward is faster on average when the caller specifically wants the last occurrence.
2. **Medium — Bidirectional (Two-Way) Linear Search:** Implement `bidirectional_search(arr: list[int], target: int) -> int` that checks `arr[left]` and `arr[right]` simultaneously in each iteration, moving `left += 1` and `right -= 1`. Does this change the asymptotic worst-case Big-O when `target` is missing? What if `target` is near the end of the array?
3. **Hard — Second Largest Distinct Element in One Pass:** Write `second_largest_distinct(arr: list[int]) -> int | None` that finds the second largest **distinct** integer in a single $O(N)$ pass with $O(1)$ space (handling duplicates like `[10, 10, 9]` $\rightarrow$ `9` and all-equal `[5, 5, 5]` $\rightarrow$ `None`).

---

## 10. Interview Questions

### Q1: When is $O(N)$ Linear Search actually faster in wall-clock time than $O(\log N)$ Binary Search?
**Answer:**
1. **When the input is unsorted and queried only once (or $K < \log N$ times):** Sorting first costs $O(N \log N)$, which dominates a single $O(N)$ linear scan.
2. **When $N$ is very small ($N \le 32$):** Python/C contiguous arrays fit inside a few CPU cache lines (`64 bytes` each). Sequential scanning enables hardware prefetching and simple branch prediction, whereas binary search jumps around memory and suffers branch mispredictions on random queries.

### Q2: How does Python's `in` operator (`target in my_list`) work under the hood?
**Answer:**
For a `list` or `tuple`, CPython's `list_contains` C function performs a sequential Linear Search from index `0` to `len(my_list) - 1`. First it checks pointer identity (`item is target` — an ultra-fast memory address check), and if that is false, it calls rich equality (`item == target`). Thus `target in my_list` is $\Omega(1)$ best case and $O(N)$ average/worst case.

### Q3: Why is the pairwise Min-Max algorithm ($1.5N$ comparisons) preferred over naive Min-Max ($2N$ comparisons) in numerical libraries?
**Answer:**
When comparing expensive objects (e.g., long strings, custom composite keys, or arbitrary-precision decimals), comparisons dominate execution time. Grouping elements into pairs reduces the comparison count by **25%** (from $2N - 2$ down to $\lfloor 1.5N \rfloor - 2$), which is information-theoretically optimal for finding both extrema simultaneously.
