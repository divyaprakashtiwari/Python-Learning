# Min Heap

## 1. Introduction

A **Min Heap** is a specialized complete binary tree that satisfies the **Min-Heap Property**:
$$\text{For every node } i \text{ other than the root: } A[\text{parent}(i)] \le A[i]$$

In words, every parent node is smaller than or equal to its children. Consequently, the minimum element of the entire tree is guaranteed to reside at the root ($A[0]$).

Min heaps are typically stored without explicit pointers in a contiguous 1D array, where parent-child relationships are calculated using simple integer arithmetic.

---

## 2. Why Use Min Heaps?

| Operation | Unsorted Array | Sorted Array | Min Heap |
|---|---|---|---|
| **Find Minimum (`peek`)** | $O(n)$ | $O(1)$ | **$O(1)$** |
| **Extract Minimum (`pop`)** | $O(n)$ | $O(n)$ shifts | **$O(\log n)$** |
| **Insert Element (`push`)** | $O(1)$ | $O(n)$ | **$O(\log n)$** |
| **Build from Array (`heapify`)** | $O(1)$ | $O(n \log n)$ sort | **$O(n)$ (Floyd's algorithm)** |
| **Find $K$-th Largest Element** | $O(n \log n)$ | $O(1)$ lookup | **$O(n \log k)$** |

---

## 3. Array Representation and Index Formulas

For any node located at 0-indexed position $i$:
- **Parent Index:** $\lfloor (i - 1) / 2 \rfloor$
- **Left Child Index:** $2i + 1$
- **Right Child Index:** $2i + 2$
- **Last Non-Leaf Node:** $\lfloor n / 2 \rfloor - 1$

---

## 4. Key Algorithmic Mechanics

### 1. Sift-Up (Bubble-Up) $\implies O(\log n)$
When a new element is appended to the end of the array, it may violate the min-heap property. It is repeatedly swapped with its parent until $A[parent] \le A[i]$ or it becomes the root ($i = 0$).

### 2. Sift-Down (Bubble-Down) $\implies O(\log n)$
When the root is extracted, the last element in the array is moved to the root position. To restore order, it is compared with its smallest child and swapped downward until the min-heap property is satisfied at all levels.

### 3. Floyd's $O(n)$ Linear Heapify
Instead of inserting $n$ elements one by one ($O(n \log n)$), Floyd's algorithm starts at the last non-leaf parent $\lfloor n / 2 \rfloor - 1$ and calls `sift_down` backwards down to index 0:
$$\sum_{h=0}^{\lfloor \log n \rfloor} \frac{n}{2^{h+1}} O(h) = O(n)$$
Because most nodes are near the bottom of the tree with very small heights, the mathematical sum converges to $O(n)$.

---

## 5. Examples

### Example 1: Min Heap Implementation from Scratch
```python
class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, val):
        self.heap.append(val)
        i = len(self.heap) - 1
        while i > 0 and self.heap[i] < self.heap[(i - 1) // 2]:
            p = (i - 1) // 2
            self.heap[i], self.heap[p] = self.heap[p], self.heap[i]
            i = p

    def pop_min(self):
        min_val = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._sift_down(0)
        return min_val
```

### Example 2: Floyd's $O(n)$ Heapify
```python
def heapify(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(arr, i, n)
```

### Example 3: Kth Largest Element using Min Heap of Size K
```python
import heapq

def find_kth_largest(nums, k):
    h = []
    for x in nums:
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)
    return h[0]
```

---

## 6. Output

```
1. Min Heap From Scratch:
   Inserted: [15, 10, 20, 17, 8, 25, 5]
   Heap Array: [5, 10, 8, 17, 15, 25, 20]
   Minimum: 5
   Extracted Sorted Order: [5, 8, 10, 15, 17, 20, 25]

2. Floyd vs Naive Heap Construction (10 Elements):
   Floyd Swaps (O(n))     : 8 swaps
   Naive Swaps (O(n log n)): 19 swaps (2.38x more operations)

3. Kth Largest in Stream (k=3):
   [4, 5, 8] -> 4
   Add 10 -> [5, 8, 10] -> 5
   Add 9  -> [8, 9, 10] -> 8
```

---

## 7. Code Explanation

| Component | Responsibility |
|---|---|
| `(i - 1) // 2` | Calculates zero-indexed parent in complete binary tree array |
| `heapq.heappushpop(h, x)` | Faster combined push and pop maintaining size $K$ in single pass |
| `n // 2 - 1` | Bypasses all $n/2$ leaf nodes, which trivially satisfy heap property |
| `self.heap.pop()` | Avoids array shifts; moving last element to index 0 is $O(1)$ |
| Size $K$ Min Heap invariant | Stores the $K$ largest elements seen so far; root is the smallest among them (the $K$-th largest) |

---

## 8. Common Mistakes

1. **Confusing Min Heap for Top-K Largest**:
   To find the $K$-th **largest** element, use a **Min-Heap** of size $K$ (so the smallest of the top $K$ is at the top). Using a Max-Heap requires storing all $N$ elements.
2. **Assuming Heaps are Fully Sorted**:
   A heap only guarantees vertical parent-child ordering, NOT horizontal sibling ordering. `heap[1]` is not necessarily smaller than `heap[2]`.
3. **Starting Floyd's Heapify from Leaves**:
   Running `sift_down` on leaf nodes is useless because leaves have no children. Always start at $\lfloor n / 2 \rfloor - 1$.
4. **Off-by-One in Array Indexing**:
   Using 1-based indexing math ($2i, 2i+1$) on a 0-indexed Python list causes silent index errors.
5. **Modifying Elements In-Place**:
   Changing the value of an item already inside a heap violates the heap invariant. You must re-heapify or re-sift.

---

## 9. Practice Questions

1. Merge $K$ Sorted Lists into one sorted list using a Min-Heap in $O(N \log K)$ time.
2. Find the median of a continuous data stream using two heaps (Min Heap + Max Heap).
3. Connect $N$ ropes with minimum total cost using a Min-Heap (Huffman coding principle).
4. Implement `heapreplace(heap, item)` from scratch and compare with separate `heappop()` + `heappush()`.
5. Reorganize a string so that no two adjacent characters are identical using a frequency heap.

---

## 10. Interview Questions

**Q1: Why is building a heap with Floyd's algorithm $O(n)$ instead of $O(n \log n)$?**
Because a complete binary tree has $\lceil n / 2 \rceil$ leaves at height 0, $\lceil n / 4 \rceil$ nodes at height 1, and so forth. Sift-down takes time proportional to height, not depth. The weighted sum $\sum \frac{n}{2^{h+1}} h$ is bounded by a convergent geometric series that equals $O(n)$.

**Q2: What is the time complexity of searching for an arbitrary element in a Min Heap?**
$O(n)$ time. Because a heap only maintains vertical parent-child relationships and lacks horizontal ordering, locating an arbitrary element requires an exhaustive linear scan.

**Q3: How does Python's built-in `heapq` handle max heaps?**
Python's `heapq` only provides min heaps. To emulate a max heap, either invert the numeric sign of values (store $-x$) or use a custom comparator wrapper object implementing inverted `__lt__`.

**Q4: Can a binary heap be implemented with dynamic sizing without losing $O(1)$ amortized insertion?**
Yes. Since Python lists use dynamic array resizing with geometric growth, appending to the end of the heap array takes $O(1)$ amortized time.

**Q5: What is the difference between Binary Heap and Fibonacci Heap?**
Binary heaps have $O(\log n)$ insertion, deletion, and decrease-key. Fibonacci heaps achieve $O(1)$ amortized time for `insert`, `decrease-key`, and `merge`, making them asymptotically optimal for Dijkstra's and Prim's algorithms on dense graphs.
