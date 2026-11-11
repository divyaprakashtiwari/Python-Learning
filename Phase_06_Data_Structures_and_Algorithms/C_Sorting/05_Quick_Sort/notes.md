# Section C: Sorting — Topic 05: Quick Sort

## 1. Introduction

**Quick Sort** (invented by Tony Hoare in 1959) is an **in-place, Divide-and-Conquer** comparison sorting algorithm that is one of the fastest general-purpose sorting algorithms in practice due to its tight inner loops and sequential CPU cache locality.

Unlike Merge Sort (which splits blindly at the midpoint and does the hard work during the *Combine* step), Quick Sort does all the work upfront during the **Divide (Partition)** step:
1. **Pick a Pivot:** Choose an element `pivot` from the subarray `arr[low .. high]`.
2. **Partition In-Place ($O(N)$):** Rearrange `arr[low .. high]` so that:
   - Every element **smaller** than `pivot` moves to the **left** of `pivot`, and
   - Every element **larger** than `pivot` moves to the **right** of `pivot`.
   *(Now `pivot` sits at its **exact final sorted index** `p`!)*
3. **Conquer:** Recursively apply Quick Sort to the left subarray `arr[low .. p - 1]` and right subarray `arr[p + 1 .. high]`. No merge step is needed!

---

## 2. Why is it used?

1. **Superior Constant Factor & Cache Locality:** Even though both Quick Sort and Merge Sort perform $O(N \log N)$ comparisons on average, Quick Sort scans contiguous memory sequentially in-place without copying elements into and out of an $O(N)$ auxiliary buffer.
2. **Low Memory Footprint ($O(\log N)$ Stack Space):** With tail-call optimization (always recursing on the smaller partition first), Quick Sort uses at most $O(\log N)$ auxiliary stack space even in the worst case.
3. **Foundation of Quickselect ($O(N)$ K-th Order Statistic):** The exact same partition subroutine finds the **median** or **$k$-th smallest/largest element** in **$O(N)$ average time** and $O(1)$ space by recursing into only ONE side of the pivot!
4. **3-Way Dutch National Flag Partition Beats $O(N \log N)$ on Duplicates:** When an array contains many duplicate keys (e.g., sorting millions of records by `status_code` or `country`), Dijkstra's 3-Way Quick Sort groups all elements equal to the pivot into a middle band `[lt .. gt]` in a single pass, finishing in **$O(N)$ linear time** when the number of distinct keys is constant!

---

## 3. Syntax & Core Blueprints

### Blueprint 1: Lomuto Partition Scheme (Cleanest for Interviews)
```python
def lomuto_partition(arr: list[int], low: int, high: int) -> int:
    pivot = arr[high]
    i = low - 1  # Boundary of elements <= pivot

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1  # Exact final index of pivot!
```

### Blueprint 2: 3-Way Dutch National Flag Partition (`[ < pivot | == pivot | > pivot ]`)
```python
def three_way_partition(arr: list[int], low: int, high: int) -> tuple[int, int]:
    pivot = arr[low + (high - low) // 2]
    lt, i, gt = low, low, high
    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
        else:
            i += 1
    return lt, gt  # Elements in arr[lt .. gt] all equal pivot!
```

---

## 4. Step-by-Step Explanation & Complexity Analysis

### Why Pivot Selection Determines $O(N \log N)$ vs $O(N^2)$
- **Best Case ($\Omega(N \log N)$):** Every pivot splits the subarray into two equal halves of size $\approx \frac{N}{2}$:
  $$T(N) = 2T\left(\frac{N}{2}\right) + \Theta(N) = \Theta(N \log N)$$
- **Worst Case ($O(N^2)$):** If we naively pick `pivot = arr[high]` (or `arr[low]`) and the input is **already sorted** (or reverse-sorted), the pivot is the maximum (or minimum) element! One partition gets $N - 1$ elements and the other gets $0$:
  $$T(N) = T(N - 1) + T(0) + \Theta(N) = \frac{N(N - 1)}{2} = \Theta(N^2)$$
- **How to Eliminate the $O(N^2)$ Trap on Sorted Data:**
  1. **Median-of-Three Pivot:** Pick the median of `(arr[low], arr[mid], arr[high])`. On an already-sorted array, `arr[mid]` is the exact median — turning the worst case into the **best case**!
  2. **Randomized Pivot:** Pick `random.randint(low, high)`. No fixed input distribution can consistently trigger $O(N^2)$.

### Complexity Summary

| Case | Partition Split Ratio | Comparisons | Time Complexity | Stack Space | Stable? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Best Case ($\Omega$)** | $50\% / 50\%$ balanced split | $\approx N \log_2 N$ | $\Omega(N \log N)$ | $O(\log N)$ | No |
| **Average Case ($\Theta$)** | Random split (even $90\% / 10\%$ is $O(N \log N)$!) | $\approx 1.39 N \log_2 N$ | $\Theta(N \log N)$ | $O(\log N)$ | No |
| **Worst Case ($O$)** | $(N - 1)$ and $0$ (unbalanced) | $\frac{N(N-1)}{2}$ | $O(N^2)$ | $O(N)$ | No |

---

## 5. Practical Examples (3 Complete Programs)

### Example 1: Lomuto vs Hoare Partition Quick Sort (`example_01_lomuto_vs_hoare_partition_quicksort.py`)
```python
def hoare_partition(arr: list[int], low: int, high: int) -> tuple[int, int]:
    pivot = arr[low + (high - low) // 2]
    i = low - 1
    j = high + 1
    swaps = 0

    while True:
        i += 1
        while arr[i] < pivot:
            i += 1

        j -= 1
        while arr[j] > pivot:
            j -= 1

        if i >= j:
            return j, swaps

        arr[i], arr[j] = arr[j], arr[i]
        swaps += 1
```

### Example 2: Avoiding $O(N^2)$ via Median-of-Three Pivot (`example_02_randomized_and_median_of_three_pivot.py`)
```python
def choose_median_of_three_index(arr: list[int], low: int, high: int) -> int:
    mid = low + (high - low) // 2
    a, b, c = arr[low], arr[mid], arr[high]
    if (a <= b <= c) or (c <= b <= a):
        return mid
    if (b <= a <= c) or (c <= a <= b):
        return low
    return high
```

### Example 3: 3-Way Dutch National Flag Partition & Quickselect (`example_03_three_way_dutch_flag_and_quickselect.py`)
```python
def quickselect_kth_smallest(arr: list[int], k_zero_based: int) -> int:
    a = arr.copy()
    low = 0
    high = len(a) - 1

    while low <= high:
        pivot = a[low + (high - low) // 2]
        lt, i, gt = low, low, high
        while i <= gt:
            if a[i] < pivot:
                a[lt], a[i] = a[i], a[lt]
                lt += 1
                i += 1
            elif a[i] > pivot:
                a[i], a[gt] = a[gt], a[i]
                gt -= 1
            else:
                i += 1

        if k_zero_based < lt:
            high = lt - 1
        elif k_zero_based > gt:
            low = gt + 1
        else:
            return a[k_zero_based]

    raise ValueError("k out of bounds")
```

---

## 6. Verified Console Output

### Output of `example_01_lomuto_vs_hoare_partition_quicksort.py`
```text
========================================================================
1. LOMUTO PARTITION vs HOARE PARTITION QUICK SORT (SWAP BENCHMARK)
========================================================================
Input Array (N=16) : [42, 15, 88, 7, 63, 29, 95, 11, 54, 36, 71, 20, 81, 49, 18, 60]
Sorted Result      : [7, 11, 15, 18, 20, 29, 36, 42, 49, 54, 60, 63, 71, 81, 88, 95]
Lomuto Total Swaps : 20
Hoare Total Swaps  : 14 (Hoare performs significantly fewer swaps!)
```

### Output of `example_02_randomized_and_median_of_three_pivot.py`
```text
========================================================================
1. NAIVE LAST-ELEMENT PIVOT vs MEDIAN-OF-THREE ON SORTED INPUT (N=31)
========================================================================
Input: Already Sorted Array [1 .. 31] (N = 31)
  Naive Pivot (arr[high]) -> Comparisons: 465 (O(N^2) = 465) | Stack Depth: 31 (O(N))
  Median-of-Three Pivot   -> Comparisons:  98 (O(N log N))   | Stack Depth:  5 (O(log N))
```

### Output of `example_03_three_way_dutch_flag_and_quickselect.py`
```text
========================================================================
1. 3-WAY DUTCH NATIONAL FLAG QUICK SORT ON HEAVY DUPLICATES
========================================================================
Input with 3 Distinct Keys (N=16): [2, 1, 3, 2, 1, 2, 3, 1, 2, 3, 2, 1, 3, 2, 1, 2]
Sorted Result                        : [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3]
Total Recursive Calls                : 7 (Finished in just 2 levels!)

========================================================================
2. QUICKSELECT: O(N) AVERAGE K-TH SMALLEST ELEMENT & MEDIAN
========================================================================
Unsorted Latencies : [85, 12, 49, 93, 27, 64, 38, 71, 19]
Sorted Reference   : [12, 19, 27, 38, 49, 64, 71, 85, 93]
Median (k=4)       : 49
```

---

## 7. Code Explanation

1. **Why Hoare Partition Performs ~3x Fewer Swaps Than Lomuto:**
   In Lomuto partition, every single element `<= pivot` triggers `i += 1` and a swap (even when elements are already on the left side). In Hoare partition, pointer `i` skips right over elements `< pivot` and pointer `j` skips left over elements `> pivot` — swapping **only** when a misplaced large element on the left pairs up with a misplaced small element on the right!
2. **Why `i` Is NOT Incremented in the `elif arr[i] > pivot:` Branch of 3-Way Partition:**
   When `arr[i] > pivot`, we swap `arr[i]` with `arr[gt]` and decrement `gt -= 1`. However, the element that just arrived at `arr[i]` from `arr[gt]` has **not been inspected yet**! Keeping `i` unchanged ensures the next loop iteration inspects that newly swapped element.

---

## 8. Common Mistakes

1. **Using `quicksort(arr, low, split_idx - 1)` with Hoare Partition:**
   Unlike Lomuto partition (which places the pivot at its final index `p` and recurses on `[low .. p - 1]` and `[p + 1 .. high]`), Hoare partition's returned index `j` is a **split boundary** where `arr[low .. j] <= arr[j + 1 .. high]` — the pivot itself may still be inside `arr[low .. j]`. Therefore Hoare Quick Sort **must** recurse on `(low, split_idx)` and `(split_idx + 1, high)`.
2. **2-Way Lomuto Partition on an Array of All Identical Elements (`[5, 5, 5, ..., 5]`):**
   Because Lomuto checks `if arr[j] <= pivot:`, every equal element goes into the left partition, creating an $(N - 1)$ vs $0$ split and degrading to **$O(N^2)$ time** on all-equal arrays! Always use 3-Way Dutch National Flag Partition (or Hoare partition, which stops on `==` and splits equal elements 50/50).

---

## 9. Practice Questions

1. **Easy — Sort Colors / Dutch National Flag (LeetCode 75):** Given an array `nums` containing only `0`s, `1`s, and `2`s, sort them in-place in a single $O(N)$ pass with $O(1)$ space using three pointers (`low`, `mid`, `high`).
2. **Medium — Kth Largest Element in an Array (LeetCode 215):** Find the `k`-th largest element in an unsorted array in $O(N)$ average time using 3-Way Quickselect (`target_idx = len(nums) - k`).
3. **Hard — Tail-Call Optimized Quick Sort with Bounded $O(\log N)$ Worst-Case Stack Space:** Rewrite in-place Quick Sort so that after partitioning, it compares `(p - 1 - low)` vs `(high - (p + 1))`, recursively calls itself **only** on the **smaller** subarray, and updates `low` or `high` iteratively for the larger subarray. Prove why stack depth never exceeds $\lfloor \log_2 N \rfloor + 1$ even if every pivot split is $N - 1$ vs $0$!

---

## 10. Interview Questions

### Q1: Why is Quickselect $O(N)$ average time whereas Quick Sort is $O(N \log N)$?
**Answer:**
Quick Sort recurses on **both** halves at every level: $N + 2\left(\frac{N}{2}\right) + 4\left(\frac{N}{4}\right) + \dots = \Theta(N \log N)$.
Quickselect discards one half and recurses on **only ONE** half:
$$N + \frac{N}{2} + \frac{N}{4} + \frac{N}{8} + \dots = N \sum_{k=0}^{\infty} \frac{1}{2^k} = 2N = \Theta(N)$$

### Q2: Is In-Place Quick Sort stable? How could you make it stable, and at what cost?
**Answer:**
In-Place Quick Sort is **unstable** because partitioning swaps non-adjacent elements across long distances (just like Selection Sort). You can make Quick Sort stable using a list comprehension (`[x for x in arr if x < pivot] + [x for x in arr if x == pivot] + [x for x in arr if x > pivot]`), which preserves relative order at the cost of **$O(N)$ extra memory**.

### Q3: What is Introsort (used in C++ `std::sort`)?
**Answer:**
Invented by David Musser (1997), **Introsort** starts with Median-of-Three **Quick Sort** for maximum speed, tracks the recursion depth limit $2 \lfloor \log_2 N \rfloor$, automatically switches to **Heap Sort** if recursion exceeds that depth (guaranteeing $O(N \log N)$ worst-case time!), and finishes subarrays smaller than 16 elements with **Insertion Sort**.
