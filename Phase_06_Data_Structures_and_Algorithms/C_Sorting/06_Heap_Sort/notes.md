# Section C: Sorting — Topic 06: Heap Sort

## 1. Introduction

**Heap Sort** (invented by J. W. J. Williams in 1964 and refined by Robert Floyd) is an **in-place, comparison-based sorting algorithm** that combines the best worst-case time guarantee of Merge Sort ($O(N \log N)$ in **all** cases) with the $O(1)$ auxiliary memory footprint of Insertion/Selection Sort!

Conceptually, **Heap Sort is Selection Sort accelerated by a Binary Max-Heap**:
- Instead of scanning the unsorted suffix linearly in $O(N)$ time on each pass to find the maximum element, Heap Sort organizes the array in-place as a **Binary Max-Heap** (where every parent is $\ge$ both its children, so the maximum element is always sitting at `arr[0]`).
- On each step, it swaps the maximum at `arr[0]` with the last element of the active heap (`arr[end]`), shrinks the heap boundary by $1$, and restores the heap invariant in **$O(\log N)$** time using `sift_down`!

---

## 2. Why is it used?

1. **Simultaneous $O(N \log N)$ Worst-Case Time AND $O(1)$ Auxiliary Space:**
   - Merge Sort guarantees $O(N \log N)$ worst-case time, but requires $O(N)$ extra memory.
   - Quick Sort uses $O(\log N)$ stack memory, but can degrade to $O(N^2)$ worst-case time.
   - **Heap Sort guarantees BOTH $O(N \log N)$ worst-case time AND strictly $O(1)$ auxiliary memory**, making it vital for safety-critical embedded systems, Linux kernel sorting (`lib/sort.c`), and the fallback stage of C++ `std::sort` (**Introsort**).
2. **Zero Pointer Overhead (Implicit Complete Binary Tree in an Array):**
   A Binary Heap does not allocate `Node` objects with `.left` and `.right` pointers. Instead, for any 0-based array index `i`:
   - `parent(i) = (i - 1) // 2`
   - `left_child(i) = 2 * i + 1`
   - `right_child(i) = 2 * i + 2`
3. **Partial Top-$K$ and Streaming Priority Queues:**
   Building a heap in $O(N)$ time (Floyd's `heapify`) and extracting only the top $K$ items takes $O(N + K \log N)$ time — much faster than a full $O(N \log N)$ sort when $K \ll N$.

---

## 3. Syntax & Core Blueprints

### Blueprint 1: Iterative `sift_down` ($O(\log N)$ Time, $O(1)$ Space)
```python
def sift_down_max(arr: list[int], start: int, end_exclusive: int) -> None:
    root = start
    while True:
        left = 2 * root + 1
        if left >= end_exclusive:
            break
        right = left + 1
        largest = root

        if arr[left] > arr[largest]:
            largest = left
        if right < end_exclusive and arr[right] > arr[largest]:
            largest = right

        if largest == root:
            break

        arr[root], arr[largest] = arr[largest], arr[root]
        root = largest
```

### Blueprint 2: Two-Phase In-Place Heap Sort
```python
def heap_sort(arr: list[int]) -> list[int]:
    n = len(arr)
    # Phase 1: Floyd's Bottom-Up Build-Max-Heap in O(N) time
    for i in range(n // 2 - 1, -1, -1):
        sift_down_max(arr, i, n)

    # Phase 2: Extract max N - 1 times in O(N log N) time
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        sift_down_max(arr, 0, end)
    return arr
```

---

## 4. Step-by-Step Explanation & Complexity Analysis

### Why Floyd's Bottom-Up `build_max_heap` Is $O(N)$ — Not $O(N \log N)$!
A common beginner misconception is that calling `sift_down` ($O(\log N)$) on $\frac{N}{2}$ internal nodes takes $O(N \log N)$ time. In reality, **most nodes in a complete binary tree are near the bottom and have tiny heights**:
- $\lceil N / 2 \rceil$ nodes are **leaves** (height $h = 0$) $\rightarrow$ $0$ work!
- $\lceil N / 4 \rceil$ nodes are at height $h = 1$ $\rightarrow$ at most $1$ swap each.
- $\lceil N / 8 \rceil$ nodes are at height $h = 2$ $\rightarrow$ at most $2$ swaps each.
- Summing across all heights $h$:
$$\text{Total Swaps} \le \sum_{h=0}^{\lfloor \log_2 N \rfloor} \frac{N}{2^{h+1}} \cdot h = \frac{N}{2} \sum_{h=0}^{\infty} \frac{h}{2^h} = \frac{N}{2} \cdot 2 = N = \Theta(N)$$

### Complexity Summary

| Phase / Case | Time Complexity | Auxiliary Space | Stable? |
| :--- | :--- | :--- | :--- |
| **Phase 1: Bottom-Up `build_max_heap`** | $\Theta(N)$ ($\le N$ swaps, $\le 2N$ comparisons) | $O(1)$ | N/A |
| **Phase 2: $N - 1$ Max Extractions** | $O(N \log N)$ | $O(1)$ | No |
| **Total Heap Sort (Best / Avg / Worst)** | $\Theta(N \log N)$ | $O(1)$ | No |

---

## 5. Practical Examples (3 Complete Programs)

### Example 1: In-Place Max-Heap Sort (`example_01_in_place_max_heap_sort.py`)
```python
def heap_sort_in_place(arr: list[int]) -> tuple[list[int], int, int]:
    a = arr.copy()
    n = len(a)
    build_comps = 0
    extract_comps = 0

    for i in range(n // 2 - 1, -1, -1):
        build_comps += sift_down_max(a, i, n)

    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        extract_comps += sift_down_max(a, 0, end)

    return a, build_comps, extract_comps
```

### Example 2: Floyd's Bottom-Up $O(N)$ vs Top-Down $O(N \log N)$ Heapify (`example_02_floyd_bottom_up_heapify_vs_top_down.py`)
```python
def build_max_heap_bottom_up_floyd(arr: list[int]) -> tuple[list[int], int]:
    a = arr.copy()
    n = len(a)
    swaps = 0

    for start in range(n // 2 - 1, -1, -1):
        root = start
        while True:
            left = 2 * root + 1
            if left >= n:
                break
            right = left + 1
            largest = root
            if a[left] > a[largest]:
                largest = left
            if right < n and a[right] > a[largest]:
                largest = right
            if largest == root:
                break
            a[root], a[largest] = a[largest], a[root]
            swaps += 1
            root = largest

    return a, swaps
```

### Example 3: Python's `heapq` Module & Sorting a $K$-Sorted Stream (`example_03_heapq_module_and_k_sorted_stream.py`)
```python
import heapq

def sort_k_sorted_array(arr: list[int], k: int) -> list[int]:
    if not arr or k <= 0:
        return arr.copy()

    n = len(arr)
    window_size = min(k + 1, n)
    min_heap = arr[:window_size]
    heapq.heapify(min_heap)

    result: list[int] = []
    for idx in range(window_size, n):
        smallest = heapq.heappushpop(min_heap, arr[idx])
        result.append(smallest)

    while min_heap:
        result.append(heapq.heappop(min_heap))

    return result
```

---

## 6. Verified Console Output

### Output of `example_01_in_place_max_heap_sort.py`
```text
========================================================================
1. IN-PLACE MAX-HEAP SORT (O(N log N) TIME, O(1) AUXILIARY SPACE)
========================================================================
  Already Sorted   (N=16) -> Build-Heap Comps: 24 (O(N)) | Extract Comps: 61 (O(N log N)) | Total: 85
  Random Order     (N=16) -> Build-Heap Comps: 23 (O(N)) | Extract Comps: 57 (O(N log N)) | Total: 80
  Reverse Sorted   (N=16) -> Build-Heap Comps: 15 (O(N)) | Extract Comps: 57 (O(N log N)) | Total: 72
```

### Output of `example_02_floyd_bottom_up_heapify_vs_top_down.py`
```text
========================================================================
1. TOP-DOWN SIFT-UP O(N log N) vs FLOYD'S BOTTOM-UP SIFT-DOWN O(N)
========================================================================
  N =  31 | Top-Down Sift-Up Swaps:   98 (O(N log N)) | Floyd Bottom-Up Swaps:  26 (< N, strictly O(N)!)
  N = 127 | Top-Down Sift-Up Swaps:  642 (O(N log N)) | Floyd Bottom-Up Swaps: 120 (< N, strictly O(N)!)
  N = 511 | Top-Down Sift-Up Swaps: 3586 (O(N log N)) | Floyd Bottom-Up Swaps: 502 (< N, strictly O(N)!)
```

### Output of `example_03_heapq_module_and_k_sorted_stream.py`
```text
========================================================================
1. PYTHON `heapq` MODULE HEAPSORT & TOP-K EXTRACTION
========================================================================
Original Scores : [72, 15, 98, 44, 63, 89, 21, 95, 53, 38]
heapsort_heapq  : [15, 21, 38, 44, 53, 63, 72, 89, 95, 98]
3 Largest (O(N)): [98, 95, 89]
3 Smallest(O(N)): [15, 21, 38]

========================================================================
2. SORTING A K-SORTED (NEARLY SORTED) ARRAY IN O(N log K) TIME
========================================================================
2-Sorted Input  : [3, 2, 1, 6, 4, 5, 9, 7, 8]
Sorted in O(N log 2) via size-3 Min-Heap: [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

---

## 7. Code Explanation

1. **Why Ascending In-Place Heap Sort Uses a MAX-Heap (Not a Min-Heap):**
   If you built a Min-Heap in-place, the smallest element would already be at `arr[0]`. Extracting it to `arr[0]` leaves `arr[1 .. n-1]` with a shifted root index where parent/child formulas (`2*i + 1`) would change for every node! By using a **Max-Heap**, the root `arr[0]` (the largest element) is swapped into the **back** of the array (`arr[end]`), while the remaining heap stays anchored at index `0`!
2. **Why `range(n // 2 - 1, -1, -1)` Starts at `n // 2 - 1`:**
   In a 0-indexed array of length $n$, the last element is at index $n - 1$, and its parent is at `((n - 1) - 1) // 2 = n // 2 - 1`. Every index $\ge \lfloor n/2 \rfloor$ is a **leaf node** that has no children and trivially satisfies the heap property!

---

## 8. Common Mistakes

1. **Using Recursive `sift_down` When Claiming $O(1)$ Auxiliary Space:**
   A recursive `max_heapify` function consumes $O(\log N)$ call-stack frames. Always write `sift_down` with a `while True:` loop so auxiliary space is strictly $O(1)$.
2. **Forgetting the `end_exclusive` Boundary During Phase 2 Extractions:**
   If `sift_down` checks `if left < len(arr):` instead of `if left < end_exclusive:`, it will sift elements back into the already-sorted suffix at the end of the array, corrupting the sorted output!

---

## 9. Practice Questions

1. **Easy — Descending In-Place Heap Sort Using a Min-Heap:** Implement `min_heap_sort_descending(arr: list[int]) -> list[int]` that builds a Min-Heap in-place and repeatedly swaps the minimum element at `arr[0]` to the back (`arr[end]`), sorting the array in descending order in $O(N \log N)$ time and $O(1)$ space.
2. **Medium — Last Stone Weight / Top-$K$ Frequent Elements (LeetCode 1046 / 347):** Use Python's `heapq` (negating values to simulate a Max-Heap) to simulate smashing the two heaviest stones in $O(N \log N)$ time.
3. **Hard — Merge $K$ Sorted Lists in $O(N \log K)$ Time (LeetCode 23):** Use a Min-Heap of size at most $K$ holding `(node.val, list_idx, node)` to merge $K$ sorted linked lists or streams in $O(N \log K)$ time and $O(K)$ space.

---

## 10. Interview Questions

### Q1: If Heap Sort has $O(N \log N)$ worst-case time and $O(1)$ space, why is Quick Sort (or Timsort) usually 2x–3x faster in wall-clock time on large arrays?
**Answer:**
**Poor CPU Cache Locality!**
- Quick Sort and Merge Sort scan contiguous memory sequentially (`i += 1`), so a single 64-byte L1 cache line fetch serves 8 consecutive comparisons.
- Heap Sort jumps from index `i` to `2*i + 1` on every step (`0 -> 1 -> 3 -> 7 -> 15 -> ...`). For a million-element array, deep heap levels jump across distant memory addresses, causing **L1/L2 cache misses** on almost every comparison!

### Q2: What is the Best-Case time complexity of Heap Sort when all elements are distinct versus when all elements are identical?
**Answer:**
- When all elements are **distinct**, even if the array is already sorted, Phase 1 builds a Max-Heap (reversing the order) and Phase 2 sifts each new root all the way down $\approx \log_2 N$ levels — taking **$\Theta(N \log N)$** in the best, average, and worst cases.
- Only when **all elements are identical** (`[5, 5, ..., 5]`) does every `sift_down` stop after 1 comparison, taking $O(N)$ time.
