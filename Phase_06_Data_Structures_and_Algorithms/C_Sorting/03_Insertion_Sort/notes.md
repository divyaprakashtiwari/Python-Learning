# Section C: Sorting — Topic 03: Insertion Sort

## 1. Introduction

**Insertion Sort** works the exact same way most people sort a hand of playing cards:
- You start with the first card `arr[0]` as a trivially sorted 1-element hand on the left.
- Then, for each subsequent card `key = arr[i]` (`i = 1, 2, ..., n - 1`), you compare `key` backward against the cards already in your sorted left hand (`arr[i - 1], arr[i - 2], ...`), **shifting** larger cards one slot to the right until you find the exact spot where `key` belongs, and **insert** `key` there.

---

## 2. Why is it used?

Even though Insertion Sort is $O(N^2)$ in the average and worst cases, it is **one of the most heavily used sorting algorithms in production standard libraries**:
1. **The Inner Engine of Hybrid Sorts (`Timsort` & `Introsort`):**
   - Python's built-in `list.sort()` and `sorted()` use **Timsort** (a hybrid of Merge Sort and **Binary Insertion Sort**). Whenever a run is smaller than `minrun` (32 to 64 elements), Timsort uses Insertion Sort because its tiny constant factor and L1 cache locality beat $O(N \log N)$ algorithms on small arrays!
   - C++ `std::sort` (**Introsort**) switches from Quick Sort to Insertion Sort when subarray size drops below `16`.
2. **$O(N)$ Adaptive Performance on Nearly-Sorted Data:**
   If an array has $I$ inversions, Insertion Sort runs in **$O(N + I)$** time. When data is already sorted ($I = 0$) or $k$-sorted ($I \le kN$), Insertion Sort finishes in **$O(N)$ linear time**, outperforming even Quick Sort and Merge Sort!
3. **Online Algorithm:** Insertion Sort can sort elements **as they arrive** from a network socket or stream without waiting for the entire dataset to be loaded into memory.
4. **Strict Stability & In-Place $O(1)$ Space:** Stopping the backward scan when `arr[j] <= key` guarantees equal elements never cross each other.

---

## 3. Syntax & Core Blueprints

### Blueprint 1: Standard Shift-Based Insertion Sort ($O(N)$ Best, $O(N^2)$ Worst)
```python
def insertion_sort(arr: list[int]) -> list[int]:
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        # Shift elements of arr[0 .. i-1] that are strictly greater than key
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
```

### Blueprint 2: Binary Insertion Sort ($O(N \log N)$ Comparisons)
```python
import bisect

def binary_insertion_sort(arr: list[int]) -> list[int]:
    for i in range(1, len(arr)):
        key = arr[i]
        # Find insertion index in arr[0 .. i-1] in O(log i) comparisons
        ins_idx = bisect.bisect_right(arr, key, 0, i)
        # Shift arr[ins_idx .. i-1] right by 1 slot
        for j in range(i - 1, ins_idx - 1, -1):
            arr[j + 1] = arr[j]
        arr[ins_idx] = key
    return arr
```

---

## 4. Step-by-Step Explanation & Complexity Analysis

### Tracing Shift-Based Insertion Sort on `arr = [30, 10, 20, 5]`
1. **Initial:** Sorted prefix `[30]`, unsorted `[10, 20, 5]`.
2. **`i = 1` (`key = 10`):** Compare `arr[0] (30) > 10` $\rightarrow$ shift `30` right (`arr[1] = 30`). `j` becomes `-1`. Place `arr[0] = 10` $\rightarrow$ `[10, 30, 20, 5]`.
3. **`i = 2` (`key = 20`):** Compare `arr[1] (30) > 20` $\rightarrow$ shift `30` right (`arr[2] = 30`). Next compare `arr[0] (10) > 20` $\rightarrow$ `False` (stop immediately!). Place `arr[1] = 20` $\rightarrow$ `[10, 20, 30, 5]`.
4. **`i = 3` (`key = 5`):** Shift `30`, `20`, and `10` right by 1 slot; place `arr[0] = 5` $\rightarrow$ `[5, 10, 20, 30]`.

### Why Exact Shifts Equal Exact Inversions ($I$)
Every time the inner `while` loop executes `arr[j + 1] = arr[j]`, the element `key` moves one position to the left past a strictly larger element `arr[j]`, eliminating **exactly 1 inversion**. Therefore:
$$\text{Total Shifts} = I \quad\text{and}\quad I \le \text{Total Comparisons} \le I + (N - 1)$$

| Variant / Case | Comparisons | Shifts (Moves) | Time Complexity | Space | Stable? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Standard — Best Case** (Sorted) | $N - 1$ | $0$ | $\Omega(N)$ | $O(1)$ | Yes |
| **Standard — Average Case** | $\approx \frac{N^2}{4}$ | $\approx \frac{N^2}{4}$ | $\Theta(N^2)$ | $O(1)$ | Yes |
| **Standard — Worst Case** (Reverse) | $\frac{N(N-1)}{2}$ | $\frac{N(N-1)}{2}$ | $O(N^2)$ | $O(1)$ | Yes |
| **Binary Insertion Sort** (Worst) | $\Theta(N \log N)$ | $\frac{N(N-1)}{2}$ | $O(N^2)$ moves | $O(1)$ | Yes |

---

## 5. Practical Examples (3 Complete Programs)

### Example 1: Standard Shift-Based Insertion Sort & Adaptivity (`example_01_shift_based_insertion_sort_and_adaptivity.py`)
```python
def insertion_sort(arr: list[int]) -> tuple[list[int], int, int]:
    a = arr.copy()
    n = len(a)
    comparisons = 0
    shifts = 0

    for i in range(1, n):
        key = a[i]
        j = i - 1

        while j >= 0:
            comparisons += 1
            if a[j] > key:
                a[j + 1] = a[j]
                shifts += 1
                j -= 1
            else:
                break

        a[j + 1] = key

    return a, comparisons, shifts
```

### Example 2: Binary Insertion Sort ($O(N \log N)$ Comparisons) (`example_02_binary_insertion_sort.py`)
```python
def binary_insertion_sort(arr: list[int]) -> tuple[list[int], int, int]:
    a = arr.copy()
    n = len(a)
    total_comps = 0
    total_shifts = 0

    for i in range(1, n):
        key = a[i]
        ins_idx, comps = binary_search_upper_bound(a, key, 0, i - 1)
        total_comps += comps

        for j in range(i - 1, ins_idx - 1, -1):
            a[j + 1] = a[j]
            total_shifts += 1

        a[ins_idx] = key

    return a, total_comps, total_shifts
```

### Example 3: Online Stream Insertion Sort & Shell Sort Preview (`example_03_online_stream_and_shell_sort_preview.py`)
```python
def shell_sort(arr: list[int]) -> tuple[list[int], int]:
    a = arr.copy()
    n = len(a)
    gap = n // 2
    shifts = 0

    while gap > 0:
        for i in range(gap, n):
            key = a[i]
            j = i
            while j >= gap and a[j - gap] > key:
                a[j] = a[j - gap]
                shifts += 1
                j -= gap
            a[j] = key
        gap //= 2

    return a, shifts
```

---

## 6. Verified Console Output

### Output of `example_01_shift_based_insertion_sort_and_adaptivity.py`
```text
========================================================================
1. SHIFT-BASED INSERTION SORT ACROSS INPUT DISTRIBUTIONS
========================================================================

[Already Sorted (Best Case)] Input: [10, 20, 30, 40, 50, 60, 70, 80]
  Sorted -> [10, 20, 30, 40, 50, 60, 70, 80] | Comparisons:  7 | Element Shifts (= Inversions):  0

[Nearly Sorted (2 Inversions)] Input: [10, 30, 20, 40, 50, 70, 60, 80]
  Sorted -> [10, 20, 30, 40, 50, 60, 70, 80] | Comparisons:  9 | Element Shifts (= Inversions):  2

[Random Order (Average Case)] Input: [64, 34, 25, 12, 22, 11, 90, 45]
  Sorted -> [11, 12, 22, 25, 34, 45, 64, 90] | Comparisons: 19 | Element Shifts (= Inversions): 16

[Reverse Sorted (Worst Case)] Input: [80, 70, 60, 50, 40, 30, 20, 10]
  Sorted -> [10, 20, 30, 40, 50, 60, 70, 80] | Comparisons: 28 | Element Shifts (= Inversions): 28
```

### Output of `example_02_binary_insertion_sort.py`
```text
========================================================================
1. STANDARD INSERTION SORT vs BINARY INSERTION SORT (COMPARISONS)
========================================================================
Reverse-Sorted Input (N=16): [160, 150, 140, 130, 120, 110, 100, 90, 80, 70, 60, 50, 40, 30, 20, 10]
  Standard Insertion Sort -> Comparisons: 120 (O(N^2))     | Shifts: 120
  Binary Insertion Sort   -> Comparisons:  38 (O(N log N)) | Shifts: 120
```

### Output of `example_03_online_stream_and_shell_sort_preview.py`
```text
========================================================================
1. ONLINE STREAM INSERTION SORT (REAL-TIME LEADERBOARD)
========================================================================
  Arrived 450 (0 shifts) -> Live Sorted Stream: [450]
  Arrived 820 (0 shifts) -> Live Sorted Stream: [450, 820]
  Arrived 610 (1 shifts) -> Live Sorted Stream: [450, 610, 820]
  Arrived 900 (0 shifts) -> Live Sorted Stream: [450, 610, 820, 900]
  Arrived 520 (3 shifts) -> Live Sorted Stream: [450, 520, 610, 820, 900]
  Arrived 750 (2 shifts) -> Live Sorted Stream: [450, 520, 610, 750, 820, 900]

========================================================================
2. SHELL SORT (GAPPED INSERTION SORT) vs STANDARD INSERTION SORT
========================================================================
Reverse-Sorted Array (N=16): [160, 150, 140, 130, 120, 110, 100, 90, 80, 70, 60, 50, 40, 30, 20, 10]
  Standard Insertion Sort Shifts : 120
  Shell Sort (Gapped) Shifts     : 32 (nearly 4x fewer moves!)
```

---

## 7. Code Explanation

1. **Shifting vs Swapping (`a[j + 1] = a[j]`):**
   Instead of swapping `a[j]` and `a[j + 1]` on every step of the inner `while` loop (which performs 3 assignments per step), we save `key = a[i]` once, perform a single assignment `a[j + 1] = a[j]` per inner step, and write `a[j + 1] = key` once when the loop finishes.
2. **Why Binary Insertion Sort Must Use `upper_bound` (`bisect_right`) for Stability:**
   When `key` equals an existing element in the sorted prefix `a[0 .. i - 1]`, we must insert `key` **after** all existing equal elements (`if arr[mid] <= key: low = mid + 1`) so their relative order is preserved and we don't needlessly shift equal elements!

---

## 8. Common Mistakes

1. **Using `arr[j] >= key` in the Inner `while` Loop:**
   Writing `while j >= 0 and arr[j] >= key:` causes `key` to shift past elements equal to itself, **destroying stability** and doing extra memory writes on arrays with duplicates. Always use strict `arr[j] > key`.
2. **Thinking Binary Insertion Sort Reduces Total Time Complexity to $O(N \log N)$:**
   Binary Insertion Sort reduces **comparisons** from $O(N^2)$ to $O(N \log N)$, which is a huge win when comparing strings or complex objects. However, inserting into a contiguous array still requires shifting $O(i)$ elements in the worst case, so **element moves remain $O(N^2)$**.

---

## 9. Practice Questions

1. **Easy — Insertion Sort List (LeetCode 147):** Given the `head` of a singly linked list, sort the list using Insertion Sort by building a `dummy` sorted list head and spliced-inserting each node in $O(1)$ auxiliary space. Why does Linked List Insertion Sort require **zero element shifting** once the insertion point is found?
2. **Medium — Sort a $k$-Sorted (Nearly Sorted) Array:** Given an array where every element is at most $k$ positions away from its target sorted position, compare the time complexity of Insertion Sort ($O(N \cdot k)$) versus a Min-Heap of size $k + 1$ ($O(N \log k)$). For what values of $k$ does Insertion Sort win?
3. **Hard — Shell Sort with Ciura / Knuth Gap Sequence ($3^k - 1) / 2$:** Implement Shell Sort using Knuth's gap sequence `1, 4, 13, 40, 121, ...` ($O(N^{3/2})$ worst-case time) and benchmark its shift count against standard $N // 2$ Shell Sort on $N = 1,000$ random integers.

---

## 10. Interview Questions

### Q1: Why does Python's `Timsort` use Binary Insertion Sort for small runs ($N < 64$) instead of running Merge Sort all the way down to size $1$?
**Answer:**
1. **Zero Recursion & Allocation Overhead:** Merge Sort down to size 1 creates $O(N)$ recursive function frames and slice/buffer copies.
2. **CPU Cache Locality:** A 32-to-64 element subarray fits completely inside a couple of L1 CPU cache lines. Shifting 32 contiguous 8-byte pointers in L1 cache takes nanoseconds, whereas `bisect_right` reduces Python rich-comparison (`__lt__`) calls to at most $\lceil \log_2 64 \rceil = 6$ per element!

### Q2: Why does Shell Sort run so much faster than Insertion Sort even though its final pass is literally `gap = 1` Insertion Sort?
**Answer:**
In standard Insertion Sort (`gap = 1`), each shift moves an element by only **1 index**, so it removes only **1 inversion** per shift. In Shell Sort's early passes (`gap = 8, 4, 2`), a single swap across distance `gap` can eliminate **up to `2 * gap - 1` inversions at once**! By the time Shell Sort reaches `gap = 1`, the array is already nearly sorted, where Insertion Sort runs in near-$O(N)$ time.

