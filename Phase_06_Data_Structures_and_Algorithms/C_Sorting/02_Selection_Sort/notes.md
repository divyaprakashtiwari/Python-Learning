# Section C: Sorting — Topic 02: Selection Sort

## 1. Introduction

**Selection Sort** is an in-place, comparison-based sorting algorithm that divides the array into two conceptual subarrays:
1. **A Sorted Prefix** `arr[0 .. i - 1]` on the left (initially empty), and
2. **An Unsorted Suffix** `arr[i .. n - 1]` on the right (initially the whole array).

On pass `i` (`0 <= i < n - 1`), Selection Sort scans the entire unsorted suffix `arr[i .. n - 1]` to find the index (`min_idx`) of the **smallest element**, and then **swaps** `arr[min_idx]` with `arr[i]`, growing the sorted prefix by 1 element.

---

## 2. Why is it used?

Even though Selection Sort always performs $\Theta(N^2)$ comparisons, it possesses one unique hardware property among all simple sorting algorithms:
1. **Minimum Possible Memory Writes (At Most $N - 1$ Swaps — $O(N)$ Writes):**
   Whereas Bubble Sort and Insertion Sort perform up to $\frac{N(N-1)}{2} = \Theta(N^2)$ memory writes in the worst case, Selection Sort performs **at most $N - 1$ swaps** ($\le 2(N - 1)$ array writes). When writing to memory is orders of magnitude more expensive or destructive than reading (e.g., **EEPROM, Flash memory, NVRAM**, or moving massive multi-kilobyte structs stored by value), Selection Sort (or its cousin Cycle Sort) minimizes write wear!
2. **Partial Top-$K$ Selection ($O(N \cdot K)$ Time):**
   If you only need the **$K$ smallest** elements out of $N$ items where $K$ is tiny (e.g., $K = 3$), stopping Selection Sort after just $K$ passes finds them in $O(N \cdot K) = O(N)$ time and $O(1)$ space without sorting the remaining $N - K$ elements.

---

## 3. Syntax & Core Blueprints

### Blueprint 1: Standard Swap-Based Selection Sort ($O(N^2)$ Comparisons, $\le N-1$ Swaps)
```python
def selection_sort(arr: list[int]) -> list[int]:
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
```

### Blueprint 2: Stable Shift-Based Selection Sort
```python
def stable_selection_sort(arr: list[int]) -> list[int]:
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        min_val = arr[min_idx]
        while min_idx > i:
            arr[min_idx] = arr[min_idx - 1]
            min_idx -= 1
        arr[i] = min_val
    return arr
```

---

## 4. Step-by-Step Explanation & Complexity Analysis

### Tracing Why Standard Selection Sort Is UNSTABLE
Consider `[(4, 'First_4'), (4, 'Second_4'), (1, 'Min_1'), (5, 'Five')]`:
- **Pass `i = 0`:** The algorithm scans indices `0..3` and finds the minimum key `1` at `min_idx = 2` (`(1, 'Min_1')`).
- It **swaps** index `0` (`(4, 'First_4')`) with index `2` (`(1, 'Min_1')`).
- The array becomes: `[(1, 'Min_1'), (4, 'Second_4'), (4, 'First_4'), (5, 'Five')]`.
- Notice that `(4, 'First_4')` was **teleported across `(4, 'Second_4')`** by a long-distance swap! Their original relative order is reversed, proving standard Selection Sort is **unstable**.

### Mathematical Comparison Count (Input-Insensitive $\Theta(N^2)$)
Regardless of whether the input is already sorted, random, or reverse-sorted, the inner loop `for j in range(i + 1, n):` has **no early exit** because it cannot know whether a smaller minimum hides at the very end until it checks every element:
$$\text{Total Comparisons} = (N - 1) + (N - 2) + \dots + 1 = \frac{N(N - 1)}{2} = \Theta(N^2)$$

| Case | Comparisons | Swaps (Memory Writes) | Time Complexity | Auxiliary Space | Stable? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Best Case ($\Omega$)** | $\frac{N(N-1)}{2}$ | $0$ (if `min_idx != i` guarded) | $\Omega(N^2)$ | $O(1)$ | No (Swap) |
| **Average Case ($\Theta$)** | $\frac{N(N-1)}{2}$ | $\approx N - H_N$ ($O(N)$) | $\Theta(N^2)$ | $O(1)$ | No (Swap) |
| **Worst Case ($O$)** | $\frac{N(N-1)}{2}$ | At most $N - 1$ ($O(N)$) | $O(N^2)$ | $O(1)$ | No (Swap) |

---

## 5. Practical Examples (3 Complete Programs)

### Example 1: Standard Selection Sort & Minimal Swap Count (`example_01_standard_selection_sort_and_swap_count.py`)
```python
def selection_sort(arr: list[int]) -> tuple[list[int], int, int]:
    a = arr.copy()
    n = len(a)
    comparisons = 0
    swaps = 0

    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if a[j] < a[min_idx]:
                min_idx = j

        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            swaps += 1

    return a, comparisons, swaps
```

### Example 2: Unstable (Swap) vs Stable (Shift) Selection Sort (`example_02_unstable_vs_stable_selection_sort.py`)
```python
def stable_selection_sort_tagged(
    items: list[tuple[int, str]]
) -> list[tuple[int, str]]:
    a = items.copy()
    n = len(a)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if a[j][0] < a[min_idx][0]:
                min_idx = j

        min_item = a[min_idx]
        while min_idx > i:
            a[min_idx] = a[min_idx - 1]
            min_idx -= 1
        a[i] = min_item

    return a
```

### Example 3: Bidirectional (Double) Selection Sort & Partial Top-$K$ (`example_03_bidirectional_and_partial_k_selection_sort.py`)
```python
def bidirectional_selection_sort(arr: list[int]) -> tuple[list[int], int]:
    a = arr.copy()
    left = 0
    right = len(a) - 1
    passes = 0

    while left < right:
        passes += 1
        min_idx = left
        max_idx = left

        for i in range(left + 1, right + 1):
            if a[i] < a[min_idx]:
                min_idx = i
            if a[i] > a[max_idx]:
                max_idx = i

        if min_idx != left:
            a[left], a[min_idx] = a[min_idx], a[left]
            if max_idx == left:
                max_idx = min_idx

        if max_idx != right:
            a[right], a[max_idx] = a[max_idx], a[right]

        left += 1
        right -= 1

    return a, passes
```

---

## 6. Verified Console Output

### Output of `example_01_standard_selection_sort_and_swap_count.py`
```text
========================================================================
1. SELECTION SORT: O(N^2) COMPARISONS BUT AT MOST N - 1 SWAPS!
========================================================================

[Already Sorted (Best Case)] (N = 8)
  Input       : [10, 20, 30, 40, 50, 60, 70, 80]
  Sorted      : [10, 20, 30, 40, 50, 60, 70, 80]
  Comparisons : 28 (Always N*(N-1)//2 = 28) | Swaps (Memory Writes): 0 (<= N - 1 = 7)

[Random Order (Average Case)] (N = 8)
  Input       : [64, 25, 12, 22, 11, 90, 45, 33]
  Sorted      : [11, 12, 22, 25, 33, 45, 64, 90]
  Comparisons : 28 (Always N*(N-1)//2 = 28) | Swaps (Memory Writes): 6 (<= N - 1 = 7)

[Reverse Sorted (Worst Case)] (N = 8)
  Input       : [80, 70, 60, 50, 40, 30, 20, 10]
  Sorted      : [10, 20, 30, 40, 50, 60, 70, 80]
  Comparisons : 28 (Always N*(N-1)//2 = 28) | Swaps (Memory Writes): 4 (<= N - 1 = 7)
```

### Output of `example_02_unstable_vs_stable_selection_sort.py`
```text
========================================================================
1. WHY STANDARD SELECTION SORT IS UNSTABLE (LONG-DISTANCE SWAP)
========================================================================
Original Input            : [(4, 'First_4'), (4, 'Second_4'), (1, 'Min_1'), (5, 'Five')]

Standard (Swap) Selection : [(1, 'Min_1'), (4, 'Second_4'), (4, 'First_4'), (5, 'Five')]
  -> Notice (4, 'Second_4') now appears BEFORE (4, 'First_4')! (UNSTABLE)

Stable (Shift) Selection  : [(1, 'Min_1'), (4, 'First_4'), (4, 'Second_4'), (5, 'Five')]
  -> Notice (4, 'First_4') remains BEFORE (4, 'Second_4')! (STABLE)
```

### Output of `example_03_bidirectional_and_partial_k_selection_sort.py`
```text
========================================================================
1. BIDIRECTIONAL (DOUBLE) SELECTION SORT (MIN & MAX EACH PASS)
========================================================================
Input (N=10) : [78, 12, 95, 34, 61, 8, 47, 89, 23, 50]
Sorted Output : [8, 12, 23, 34, 47, 50, 61, 78, 89, 95]
Outer Passes  : 5 (Half of standard N - 1 = 9 passes!)

========================================================================
2. PARTIAL SELECTION SORT: FIND 3 SMALLEST LATENCIES IN O(N * K)
========================================================================
All Latencies (ms)   : [142, 89, 210, 17, 64, 310, 24, 95, 11, 180]
3 Lowest Latencies   : [11, 17, 24] (Computed in just 3 outer passes!)
```

---

## 7. Code Explanation

1. **Why Reverse-Sorted Array `[80, 70, 60, 50, 40, 30, 20, 10]` Took Only 4 Swaps (`N // 2`):**
   On Pass 1 (`i = 0`), `80` swaps with `10` $\rightarrow$ `[10, 70, 60, 50, 40, 30, 20, 80]`. Notice that **both** `10` AND `80` landed in their final sorted positions in a single swap! After 4 swaps (`8 // 2`), the entire array is sorted, so the remaining 3 passes have `min_idx == i` ($0$ swaps).
2. **The Aliasing Trap in Bidirectional Selection Sort (`if max_idx == left: max_idx = min_idx`):**
   Suppose `a[left]` happens to hold the **maximum** element of the window. When we first swap `a[left]` with `a[min_idx]`, the maximum element is no longer at index `left` — it was just moved to `min_idx`! Updating `if max_idx == left: max_idx = min_idx` prevents the second swap from putting the minimum element at `right`.

---

## 8. Common Mistakes

1. **Swapping Inside the Inner Loop (`if a[j] < a[i]: swap(a[i], a[j])`):**
   Beginners sometimes swap immediately inside the `j` loop instead of tracking `min_idx` and swapping once after the inner loop ends. Swapping inside the inner loop turns Selection Sort into an inefficient Exchange Sort that performs $O(N^2)$ swaps instead of $\le N - 1$ swaps!
2. **Assuming Selection Sort Can Be Made $O(N)$ on Sorted Input Using a Flag:**
   Unlike Bubble Sort (which compares adjacent pairs `a[j] > a[j+1]`), Selection Sort compares every element `a[j]` against a single fixed element `a[min_idx]`. Even if `a[0]` is the minimum of the array, knowing that `a[0] < a[1..n-1]` tells you **nothing** about whether `a[1 .. n-1]` are sorted among themselves!

---

## 9. Practice Questions

1. **Easy — Selection Sort on Singly Linked List by Value Swapping:** Given the head of a singly linked list, sort it in ascending order using Selection Sort by swapping `.val` attributes between the current node and `min_node` in $O(1)$ space.
2. **Medium — Minimum Swaps to Sort an Array of Distinct Integers:** Given an array of $N$ distinct integers, find the minimum number of swaps (between any two indices) required to sort the array. Compare why Selection Sort performs $\le N - 1$ swaps and when it equals the exact cycle-decomposition minimum.
3. **Hard — Stable Selection Sort on Linked List via Pointer Manipulation:** Implement Selection Sort on a singly linked list **without modifying `.val`** (only relinking `.next` pointers) while preserving stability. Explain why relinking nodes on a linked list makes Stable Selection Sort $O(1)$ per extraction instead of $O(N)$ array shifting!

---

## 10. Interview Questions

### Q1: Which $O(N^2)$ sorting algorithm performs the fewest memory writes in the worst case: Bubble Sort, Insertion Sort, or Selection Sort?
**Answer:**
**Selection Sort** performs at most **$N - 1$ swaps** ($\le 2N - 2$ array writes), which is $O(N)$ memory writes. Both Bubble Sort and Insertion Sort perform $\Theta(N^2)$ array writes on reverse-sorted input. (If the absolute theoretical minimum number of writes is required where every element is written at most once, **Cycle Sort** achieves that at the cost of extra comparisons.)

### Q2: How does Heap Sort relate to Selection Sort?
**Answer:**
**Heap Sort is literally Selection Sort accelerated with a Binary Heap!**
- Standard Selection Sort takes $O(N)$ linear scans to find the minimum/maximum in each of the $N$ passes: $N \times O(N) = O(N^2)$.
- Heap Sort maintains the unsorted suffix as a **Max-Heap**, finding and extracting the maximum element in $O(\log N)$ time per pass: $N \times O(\log N) = O(N \log N)$ time and $O(1)$ auxiliary space!

