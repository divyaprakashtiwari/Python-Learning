# Section C: Sorting — Topic 04: Merge Sort

## 1. Introduction

**Merge Sort** (invented by John von Neumann in 1945) is a classic **Divide-and-Conquer** sorting algorithm that guarantees **$O(N \log N)$ time complexity in the Best, Average, AND Worst cases**.

It operates in three recursive phases:
1. **Divide:** Split the array of $N$ elements at the midpoint `mid = N // 2` into two halves (`left` of size $\lfloor N/2 \rfloor$ and `right` of size $\lceil N/2 \rceil$).
2. **Conquer:** Recursively sort both halves until base-case subarrays of size $\le 1$ are reached (a 1-element array is already sorted!).
3. **Combine (Merge):** Merge the two sorted halves into a single sorted array in **$O(N)$ linear time** using the **Two-Pointer Technique** (`i` on `left`, `j` on `right`), always picking the smaller front element (`left[i] <= right[j]`).

---

## 2. Why is it used?

1. **Bulletproof $O(N \log N)$ Worst-Case Guarantee:** Unlike Quick Sort (which can degrade to $O(N^2)$ on adversarial pivot choices), Merge Sort never exceeds $N \lceil \log_2 N \rceil$ comparisons regardless of the input distribution.
2. **Strict Sorting Stability:** By picking from the **left** subarray whenever keys are tied (`if left[i] <= right[j]:`), equal elements never cross each other. Merge Sort is the foundational algorithm behind Python's **Timsort** (`list.sort()`) and Java's `Arrays.sort(Object[])`.
3. **The Gold Standard for Linked Lists & External (Disk) Sorting:**
   - Merging two sorted **Linked Lists** requires **$O(1)$ auxiliary memory** (just relinking `.next` pointers — zero array allocation!) and runs in $O(N \log N)$ time.
   - **External Merge Sort** sorts multi-terabyte database tables that do not fit in RAM by sorting chunks in memory and streaming $K$-way sequential merges from disk.
4. **Solving Divide-and-Conquer Counting Problems:** Piggybacking on the `merge` step solves **Counting Inversions**, **Count of Smaller Numbers After Self**, and **Reverse Pairs** in $O(N \log N)$ time instead of $O(N^2)$.

---

## 3. Syntax & Core Blueprints

### Blueprint 1: Top-Down Recursive Merge Sort ($O(N \log N)$ Time, $O(N)$ Space)
```python
def merge(left: list[int], right: list[int]) -> list[int]:
    merged: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:  # `<=` guarantees stability!
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def merge_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left_sorted = merge_sort(arr[:mid])
    right_sorted = merge_sort(arr[mid:])
    return merge(left_sorted, right_sorted)
```

### Blueprint 2: Bottom-Up Iterative Merge Sort (Zero Recursion Overhead)
```python
def bottom_up_merge_sort(arr: list[int]) -> list[int]:
    n = len(arr)
    aux = [0] * n
    width = 1
    while width < n:
        for left in range(0, n, 2 * width):
            mid = min(left + width, n)
            right = min(left + 2 * width, n)
            if mid < right:
                merge_into_buffer(arr, aux, left, mid, right)
        width *= 2
    return arr
```

---

## 4. Step-by-Step Explanation & Complexity Analysis

### Master Theorem & Recursion Tree Analysis
A recursion tree for Merge Sort on $N$ elements has:
- **Height of tree:** $\lceil \log_2 N \rceil$ levels (since $N$ is halved at each level: $N \to N/2 \to N/4 \to \dots \to 1$).
- **Work per level:** At level $d$, there are $2^d$ subproblems each of size $\frac{N}{2^d}$. Merging all pairs at level $d$ takes $2^d \times O\left(\frac{N}{2^d}\right) = O(N)$ total operations.
- **Total Time:**
$$T(N) = 2T\left(\frac{N}{2}\right) + \Theta(N) = \Theta(N \log_2 N)$$

### Space Complexity Breakdown (Arrays vs Linked Lists)
- **Contiguous Array Merge Sort:** Merging two adjacent subarrays in $O(N)$ time requires an auxiliary buffer of size $O(N)$, plus $O(\log N)$ recursion call-stack frames $\rightarrow$ **$O(N)$ total auxiliary space**. (Note: Do not sum $O(N)$ across all $\log N$ levels — memory from completed child merges is reclaimed before sibling/parent merges run, or a single shared `aux` buffer of size $N$ is reused!).
- **Linked List Merge Sort:** Relinking `.next` pointers requires $O(1)$ heap space (and $O(1)$ stack space if implemented bottom-up!).

| Case | Comparisons | Time Complexity | Auxiliary Space (Array) | Stable? |
| :--- | :--- | :--- | :--- | :--- |
| **Best Case ($\Omega$)** | $\approx \frac{1}{2} N \log_2 N$ | $\Omega(N \log N)$ | $O(N)$ | Yes |
| **Average Case ($\Theta$)** | $\approx N \log_2 N - 1.26N$ | $\Theta(N \log N)$ | $O(N)$ | Yes |
| **Worst Case ($O$)** | $N \lceil \log_2 N \rceil - 2^{\lceil \log_2 N \rceil} + 1$ | $O(N \log N)$ | $O(N)$ | Yes |

---

## 5. Practical Examples (3 Complete Programs)

### Example 1: Top-Down Recursive Merge Sort (`example_01_top_down_recursive_merge_sort.py`)
```python
def merge_two_sorted_lists(
    left: list[int], right: list[int]
) -> tuple[list[int], int]:
    merged: list[int] = []
    i = 0
    j = 0
    comparisons = 0

    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    if i < len(left):
        merged.extend(left[i:])
    if j < len(right):
        merged.extend(right[j:])

    return merged, comparisons
```

### Example 2: Bottom-Up Iterative Merge Sort (`example_02_bottom_up_iterative_merge_sort.py`)
```python
def bottom_up_merge_sort(arr: list[int], trace: bool = False) -> list[int]:
    a = arr.copy()
    n = len(a)
    if n <= 1:
        return a

    aux = [0] * n
    width = 1
    pass_num = 0

    while width < n:
        pass_num += 1
        for left in range(0, n, 2 * width):
            mid = min(left + width, n)
            right = min(left + 2 * width, n)
            if mid < right:
                merge_into_buffer(a, aux, left, mid, right)

        if trace:
            print(f"  After Pass {pass_num} (merging width={width:>2} -> {2*width:>2}): {a}")
        width *= 2

    return a
```

### Example 3: Counting Array Inversions in $O(N \log N)$ (`example_03_counting_inversions_with_merge_sort.py`)
```python
def sort_and_count_inversions(arr: list[int]) -> tuple[list[int], int]:
    if len(arr) <= 1:
        return arr.copy(), 0

    mid = len(arr) // 2
    left_sorted, left_inv = sort_and_count_inversions(arr[:mid])
    right_sorted, right_inv = sort_and_count_inversions(arr[mid:])

    merged: list[int] = []
    i = 0
    j = 0
    split_inv = 0

    while i < len(left_sorted) and j < len(right_sorted):
        if left_sorted[i] <= right_sorted[j]:
            merged.append(left_sorted[i])
            i += 1
        else:
            merged.append(right_sorted[j])
            split_inv += len(left_sorted) - i
            j += 1

    merged.extend(left_sorted[i:])
    merged.extend(right_sorted[j:])
    return merged, (left_inv + right_inv + split_inv)
```

---

## 6. Verified Console Output

### Output of `example_01_top_down_recursive_merge_sort.py`
```text
========================================================================
1. TOP-DOWN RECURSIVE MERGE SORT ACROSS INPUT DISTRIBUTIONS (N = 16)
========================================================================

[Already Sorted (Best Case)] (N = 16, N*log2(N) = 64)
  Comparisons : 32 (Guaranteed <= N*log2(N) = 64 in ALL cases!)
  Sorted Head : [10, 20, 30, 40, 50, 60, 70, 80] ...

[Random Order (Average Case)] (N = 16, N*log2(N) = 64)
  Comparisons : 48 (Guaranteed <= N*log2(N) = 64 in ALL cases!)
  Sorted Head : [10, 20, 30, 40, 50, 60, 70, 80] ...

[Reverse Sorted (Worst Case)] (N = 16, N*log2(N) = 64)
  Comparisons : 32 (Guaranteed <= N*log2(N) = 64 in ALL cases!)
  Sorted Head : [10, 20, 30, 40, 50, 60, 70, 80] ...
```

### Output of `example_02_bottom_up_iterative_merge_sort.py`
```text
========================================================================
1. BOTTOM-UP ITERATIVE MERGE SORT TRACE (ZERO RECURSION)
========================================================================
Initial Array (N=10): [38, 27, 43, 3, 9, 82, 10, 19, 55, 12]

  After Pass 1 (merging width= 1 ->  2): [27, 38, 3, 43, 9, 82, 10, 19, 12, 55]
  After Pass 2 (merging width= 2 ->  4): [3, 27, 38, 43, 9, 10, 19, 82, 12, 55]
  After Pass 3 (merging width= 4 ->  8): [3, 9, 10, 19, 27, 38, 43, 82, 12, 55]
  After Pass 4 (merging width= 8 -> 16): [3, 9, 10, 12, 19, 27, 38, 43, 55, 82]

Final Sorted Array     : [3, 9, 10, 12, 19, 27, 38, 43, 55, 82]
```

### Output of `example_03_counting_inversions_with_merge_sort.py`
```text
========================================================================
1. COUNTING INVERSIONS IN O(N log N) VIA MERGE SORT
========================================================================
  Sorted Array (0 Inversions)      | Input: [10, 20, 30, 40, 50]       -> Inversions: 0
  Classic Example [2, 4, 1, 3, 5]  | Input: [2, 4, 1, 3, 5]            -> Inversions: 3
  Reverse Array (Max N*(N-1)//2)   | Input: [50, 40, 30, 20, 10]       -> Inversions: 10
  User Ranking Similarity Array    | Input: [8, 4, 2, 1, 7, 3, 6, 5]   -> Inversions: 15
```

---

## 7. Code Explanation

1. **Why `split_inv += len(left_sorted) - i` Works in $O(1)$ per Step:**
   Because `left_sorted` and `right_sorted` are both already sorted in ascending order, the moment we discover `left_sorted[i] > right_sorted[j]`, we know that `left_sorted[i], left_sorted[i + 1], ..., left_sorted[-1]` are **all** strictly greater than `right_sorted[j]`. That single comparison uncovers `len(left_sorted) - i` inversions simultaneously!
2. **Early-Skip Optimization (`if a[mid - 1] <= a[mid]: return`):**
   In `merge_into_buffer`, `a[mid - 1]` is the largest element of the left sorted run and `a[mid]` is the smallest element of the right sorted run. If `a[mid - 1] <= a[mid]`, the two runs are already in sorted order and we skip copying altogether — making Merge Sort run in **$O(N)$ time on already-sorted arrays**!

---

## 8. Common Mistakes

1. **Using `left.pop(0)` Inside the Merge Loop ($O(N^2)$ Disaster):**
   Writing `merged.append(left.pop(0))` instead of advancing an integer index `i += 1` shifts the entire remaining `left` list in $O(N)$ time on every step, turning Merge Sort into an **$O(N^2)$** algorithm! Always use index pointers `i` and `j`.
2. **Using `<` Instead of `<=` (`if left[i] < right[j]:`):**
   If `left[i] == right[j]` and you take `right[j]` first, an element that originally appeared later in the array is placed before an equal element from the left half, **breaking stability** (and miscounting inversions in `sort_and_count_inversions`!).

---

## 9. Practice Questions

1. **Easy — Merge Sorted Array In-Place from the Back (LeetCode 88):** Given `nums1` of length $m + n$ (where the first $m$ elements are sorted and the last $n$ slots are `0`s) and `nums2` of length $n$, merge `nums2` into `nums1` in-place without extra memory by filling from the **back** (`write_idx = m + n - 1`).
2. **Medium — Sort a Singly Linked List in $O(N \log N)$ Time (LeetCode 148):** Use Tortoise-and-Hare (`slow`/`fast` pointers) to find the midpoint of a linked list, recursively sort both halves, and merge them in-place by relinking `.next` pointers.
3. **Hard — Reverse Pairs (LeetCode 493):** Given an integer array `nums`, return the number of **reverse pairs** `(i, j)` where `0 <= i < j < len(nums)` and `nums[i] > 2 * nums[j]`. Solve in $O(N \log N)$ time using Merge Sort.

---

## 10. Interview Questions

### Q1: Why is Merge Sort preferred over Quick Sort for sorting Linked Lists, whereas Quick Sort (or Introsort) is often preferred for primitive arrays in C++?
**Answer:**
- **For Linked Lists:** Merge Sort does not require random access (`arr[mid]`) and can merge two sorted linked lists in **$O(1)$ extra space** purely by adjusting `.next` pointers. Quick Sort on a linked list suffers from poor cache locality when jumping pointers.
- **For Contiguous Primitive Arrays:** Merge Sort requires an $O(N)$ auxiliary array buffer, whereas In-Place Quick Sort uses only $O(\log N)$ stack space and exhibits superior L1 cache locality during sequential partition scans.

### Q2: Does recursive Merge Sort use $O(N \log N)$ space because there are $\log N$ levels and each level allocates $O(N)$ lists?
**Answer:**
**No — peak auxiliary space is $O(N)$, not $O(N \log N)$!** Because recursion executes **depth-first**, only one root-to-leaf path of the recursion tree is active on the call stack at any instant. The memory allocated in `merge_sort(arr[:mid])` is freed/reclaimed before `merge_sort(arr[mid:])` finishes, so total active auxiliary memory at any point in time is bounded by $N + \frac{N}{2} + \frac{N}{4} + \dots < 2N = O(N)$.
