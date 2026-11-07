# Section C: Sorting — Topic 01: Bubble Sort

## 1. Introduction

**Bubble Sort** (also called **Sinking Sort**) is the simplest comparison-based sorting algorithm. It repeatedly steps through the array from left to right, compares **adjacent pairs** of elements (`arr[j]` and `arr[j + 1]`), and **swaps** them if they are out of order (`arr[j] > arr[j + 1]`).

Why is it called "Bubble Sort"?
- During the **1st pass**, the largest element in the entire array is guaranteed to "bubble up" to the rightmost index (`n - 1`).
- During the **2nd pass**, the second-largest element bubbles up to index `n - 2`.
- After `k` passes, the rightmost `k` elements are locked in their final sorted positions!

---

## 2. Why is it used?

While Bubble Sort's $O(N^2)$ average and worst-case time complexity makes it too slow for large unsorted datasets (where $O(N \log N)$ Timsort, Merge Sort, or Quick Sort are used), it has important educational and niche properties:
1. **$O(N)$ Adaptive Best-Case Detection:** With a simple `swapped` boolean flag (or `last_swap_idx` tracker), Bubble Sort verifies whether an array is **already sorted** in a single $O(N)$ pass ($N - 1$ comparisons, $0$ swaps) and $O(1)$ space.
2. **Inversion Counting Intuition:** Every adjacent swap in Bubble Sort removes **exactly 1 inversion** (a pair $(i, j)$ where $i < j$ and $\text{arr}[i] > \text{arr}[j]$). Therefore, the exact number of swaps performed by Bubble Sort equals the number of inversions in the array!
3. **Strict Stability & $O(1)$ In-Place Memory:** Because Bubble Sort only swaps adjacent elements when `arr[j] > arr[j + 1]` (never when `==`), equal elements never cross each other.

---

## 3. Syntax & Core Blueprints

### Blueprint 1: Standard Early-Exit Bubble Sort ($O(N)$ Best, $O(N^2)$ Worst)
```python
def bubble_sort(arr: list[int]) -> list[int]:
    n = len(arr)
    for pass_num in range(n - 1):
        swapped = False
        # Last `pass_num` elements are already in final position
        for j in range(n - 1 - pass_num):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break  # Array is completely sorted!
    return arr
```

### Blueprint 2: Boundary-Tightening Bubble Sort (`last_swap_idx` Optimization)
```python
def bubble_sort_last_swap(arr: list[int]) -> list[int]:
    unsorted_end = len(arr) - 1
    while unsorted_end > 0:
        last_swap_idx = 0
        for j in range(unsorted_end):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                last_swap_idx = j
        unsorted_end = last_swap_idx  # Everything after last_swap_idx is sorted!
    return arr
```

---

## 4. Step-by-Step Explanation & Complexity Analysis

### Tracing Pass-by-Pass on `arr = [50, 20, 40, 10]` ($N = 4$)
- **Pass 1 (`j = 0..2`):**
  - Compare `50 > 20` $\rightarrow$ swap $\rightarrow$ `[20, 50, 40, 10]`
  - Compare `50 > 40` $\rightarrow$ swap $\rightarrow$ `[20, 40, 50, 10]`
  - Compare `50 > 10` $\rightarrow$ swap $\rightarrow$ `[20, 40, 10, 50]` (**`50` locked at index 3**)
- **Pass 2 (`j = 0..1`):**
  - Compare `20 > 40` $\rightarrow$ no swap
  - Compare `40 > 10` $\rightarrow$ swap $\rightarrow$ `[20, 10, 40, 50]` (**`40` locked at index 2**)
- **Pass 3 (`j = 0`):**
  - Compare `20 > 10` $\rightarrow$ swap $\rightarrow$ `[10, 20, 40, 50]` (**`20` locked at index 1, `10` at index 0**)

### The "Rabbits and Turtles" Problem & Cocktail Shaker Sort
- **Rabbits:** A large number at the beginning (like `99` at index `0`) bubbles all the way to the right end in **a single pass**.
- **Turtles:** A tiny number at the very end (like `1` at the end of `[2, 3, 4, 5, 6, 7, 8, 9, 1]`) only shifts left by **1 position per pass**, forcing $N - 1$ passes!
- **Cocktail Shaker Sort (Bidirectional Bubble Sort)** fixes Turtles by alternating a forward pass (left-to-right) with a backward pass (right-to-left).

### Complexity Summary

| Case | Scenario | Comparisons | Swaps | Time Complexity | Space | Stable? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Best Case ($\Omega$)** | Already sorted (with `swapped` flag) | $N - 1$ | $0$ | $\Omega(N)$ | $O(1)$ | Yes |
| **Average Case ($\Theta$)** | Random permutation | $\approx \frac{N(N-1)}{2}$ | $\approx \frac{N(N-1)}{4}$ | $\Theta(N^2)$ | $O(1)$ | Yes |
| **Worst Case ($O$)** | Reverse-sorted array | $\frac{N(N-1)}{2}$ | $\frac{N(N-1)}{2}$ | $O(N^2)$ | $O(1)$ | Yes |

---

## 5. Practical Examples (3 Complete Programs)

### Example 1: Standard vs Optimized Bubble Sort (`example_01_standard_vs_early_exit_bubble_sort.py`)
```python
def bubble_sort_optimized(arr: list[int]) -> tuple[list[int], int, int, int]:
    a = arr.copy()
    unsorted_end = len(a) - 1
    comparisons = 0
    swaps = 0
    passes = 0

    while unsorted_end > 0:
        passes += 1
        last_swap_idx = 0

        for j in range(unsorted_end):
            comparisons += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                last_swap_idx = j

        unsorted_end = last_swap_idx

    return a, passes, comparisons, swaps
```

### Example 2: Cocktail Shaker Sort & The "Turtles" Problem (`example_02_cocktail_shaker_sort_and_turtles.py`)
```python
def cocktail_shaker_sort(arr: list[int]) -> tuple[list[int], int, int]:
    a = arr.copy()
    start = 0
    end = len(a) - 1
    sweeps = 0
    comparisons = 0

    while start < end:
        swapped = False
        sweeps += 1
        for i in range(start, end):
            comparisons += 1
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True
        end -= 1
        if not swapped:
            break

        swapped = False
        sweeps += 1
        for i in range(end, start, -1):
            comparisons += 1
            if a[i - 1] > a[i]:
                a[i - 1], a[i] = a[i], a[i - 1]
                swapped = True
        start += 1
        if not swapped:
            break

    return a, sweeps, comparisons
```

### Example 3: Stability Verification & Custom Key Function (`example_03_stability_and_custom_key_bubble_sort.py`)
```python
def stable_bubble_sort_by_key(
    items: list[T],
    key: Callable[[T], int | float | str],
    reverse: bool = False,
) -> list[T]:
    result = items.copy()
    n = len(result)

    for pass_num in range(n - 1):
        swapped = False
        for j in range(n - 1 - pass_num):
            left_key = key(result[j])
            right_key = key(result[j + 1])

            should_swap = (left_key < right_key) if reverse else (left_key > right_key)
            if should_swap:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True

        if not swapped:
            break

    return result
```

---

## 6. Verified Console Output

### Output of `example_01_standard_vs_early_exit_bubble_sort.py`
```text
========================================================================
1. STANDARD vs OPTIMIZED BUBBLE SORT ACROSS INPUT DISTRIBUTIONS
========================================================================

[Already Sorted (Best Case)] Input: [10, 20, 30, 40, 50, 60, 70, 80]
  Standard Bubble Sort  -> Comps: 28 | Swaps:  0
  Optimized Bubble Sort -> Comps:  7 | Swaps:  0 | Passes: 1

[Nearly Sorted (Tail Sorted)] Input: [20, 10, 30, 40, 50, 60, 70, 80]
  Standard Bubble Sort  -> Comps: 28 | Swaps:  1
  Optimized Bubble Sort -> Comps:  7 | Swaps:  1 | Passes: 1

[Random Order (Average Case)] Input: [64, 34, 25, 12, 22, 11, 90, 45]
  Standard Bubble Sort  -> Comps: 28 | Swaps: 16
  Optimized Bubble Sort -> Comps: 21 | Swaps: 16 | Passes: 5

[Reverse Sorted (Worst Case)] Input: [80, 70, 60, 50, 40, 30, 20, 10]
  Standard Bubble Sort  -> Comps: 28 | Swaps: 28
  Optimized Bubble Sort -> Comps: 28 | Swaps: 28 | Passes: 7
```

### Output of `example_02_cocktail_shaker_sort_and_turtles.py`
```text
========================================================================
1. THE 'TURTLE' PROBLEM: SMALL ELEMENT AT THE END OF SORTED ARRAY
========================================================================
Turtle Array (n=9): [2, 3, 4, 5, 6, 7, 8, 9, 1]

Unidirectional Bubble Sort -> Passes: 8 | Comparisons: 36
Cocktail Shaker Sort       -> Sweeps: 3 | Comparisons: 21
Sorted Result              : [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### Output of `example_03_stability_and_custom_key_bubble_sort.py`
```text
========================================================================
1. VERIFYING SORTING STABILITY ON SUPPORT TICKET QUEUE
========================================================================
Sorted by Priority (1 = Urgent first), preserving FIFO submission order:
  TCK-102 | Priority: 1 | Original Arrival Order: #2
  TCK-104 | Priority: 1 | Original Arrival Order: #4
  TCK-106 | Priority: 1 | Original Arrival Order: #6
  TCK-101 | Priority: 2 | Original Arrival Order: #1
  TCK-103 | Priority: 2 | Original Arrival Order: #3
  TCK-105 | Priority: 3 | Original Arrival Order: #5

Priority-1 arrival orders after sort: [2, 4, 6] (Strictly increasing -> STABLE!)
```

---

## 7. Code Explanation

1. **Why `last_swap_idx` Beats a Simple Boolean `swapped` Flag:**
   Look at `[20, 10, 30, 40, 50, 60, 70, 80]` in Example 1. With a simple `swapped` flag, Pass 1 swaps `20` and `10` (`swapped = True`), so a 2nd pass over `j = 0..6` is still required to confirm `swapped == False` ($7 + 6 = 13$ comparisons). With `last_swap_idx`, the last swap occurred at `j = 0`, so `unsorted_end` immediately drops to `0` after Pass 1 — finishing in just **7 comparisons (1 pass)**!
2. **Why `>=` Destroys Stability:**
   If you write `if a[j] >= a[j + 1]:`, then two equal elements (`TCK-102` and `TCK-104`, both Priority 1) will swap places on contact, destroying FIFO arrival order and doing unnecessary writes. Always use strict `>`.

---

## 8. Common Mistakes

1. **Running the Inner Loop All the Way to `n` (`for j in range(n):`):**
   Evaluating `a[j + 1]` when `j == n - 1` raises `IndexError: list index out of range`. Even `range(n - 1)` wastes comparisons re-checking the already-sorted suffix `n - 1 - pass_num`. Always use `range(n - 1 - pass_num)`.
2. **Claiming Unoptimized Bubble Sort Has $\Omega(N)$ Best-Case Time:**
   Without the `swapped` early-exit flag, Bubble Sort blindly executes all $\frac{N(N-1)}{2}$ comparisons even on an already sorted list (`Theta(N^2)` in all cases). You **must** include the `swapped` check to achieve $\Omega(N)$ best case.

---

## 9. Practice Questions

1. **Easy — Minimum Adjacent Swaps to Sort:** Given an array of integers, return the minimum number of **adjacent swaps** required to sort the array in non-decreasing order. Verify using small arrays that this count equals the exact number of swaps performed by Bubble Sort.
2. **Medium — Recursive Bubble Sort:** Implement `recursive_bubble_sort(arr: list[int], n: int) -> None` where each recursive call performs 1 pass bubbling the maximum of `arr[0..n-1]` to `arr[n-1]` (stopping early if 0 swaps occurred) and then recurses on `n - 1`. What are its time and call-stack space complexities?
3. **Hard — Even-Odd (Brick) Sort for Parallel SIMD Hardware:** Implement `odd_even_sort(arr: list[int]) -> list[int]` which alternates between comparing odd-indexed adjacent pairs `(1,2), (3,4), ...` and even-indexed adjacent pairs `(0,1), (2,3), ...`. Explain why all pairs within a single phase are disjoint and can execute in parallel on GPU threads.

---

## 10. Interview Questions

### Q1: Why is Insertion Sort preferred over Bubble Sort in practice (e.g., inside Timsort and introsort for small subarrays), even though both are $O(N^2)$ worst-case and $\Omega(N)$ best-case?
**Answer:**
1. **Fewer Writes:** Each step of Bubble Sort performs a full swap (**3 array writes**: `tmp = a[j]; a[j] = a[j+1]; a[j+1] = tmp`), whereas Insertion Sort shifts elements (**1 array write** per inner-loop step: `a[j+1] = a[j]`) and writes `key` once at the end.
2. **Fewer Comparisons on Random Data:** When inserting the $i$-th element, Insertion Sort stops scanning as soon as `a[j] <= key` (averaging $\frac{N^2}{4}$ comparisons), whereas Bubble Sort must scan the entire remaining unsorted prefix on every pass unless the tail happens to be completely sorted.

### Q2: How many passes of Bubble Sort are needed to sort an array where every element is at most $k$ positions away from its sorted position?
**Answer:**
If every element is at most $k$ positions to the **right** of its sorted position (i.e., the furthest "Turtle" needs to move left by at most $k$ indices), Bubble Sort finishes in at most **$k + 1$ passes** ($O(k \cdot N)$ time). However, if a small element starts at index $N - 1$ and belongs at index $0$, $k = N - 1$ passes are required.
