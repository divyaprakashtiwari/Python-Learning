# Max Heap

## 1. Introduction

A **Max Heap** is a specialized complete binary tree data structure that satisfies the **Max-Heap Property**:
$$\text{For every node } i \text{ other than the root: } A[\text{parent}(i)] \ge A[i]$$

This invariant ensures that the value of every parent node is greater than or equal to the values of its children. Consequently, the largest element in the entire heap always resides at the root ($A[0]$).

Max heaps serve as the engine for priority queues with descending urgency, heap sort, greedy task selection, and continuous data stream median tracking.

---

## 2. Why Use Max Heaps?

| Operation | Unsorted Array | Sorted Array | Max Heap |
|---|---|---|---|
| **Find Maximum (`peek`)** | $O(n)$ | $O(1)$ | **$O(1)$** |
| **Extract Maximum (`pop_max`)** | $O(n)$ | $O(n)$ shifts | **$O(\log n)$** |
| **Insert Element (`push`)** | $O(1)$ | $O(n)$ | **$O(\log n)$** |
| **Build from Array (`heapify`)** | $O(1)$ | $O(n \log n)$ sort | **$O(n)$ (Floyd's algorithm)** |
| **Dynamic Stream Tracking** | $O(n \log n)$ per insert | $O(n)$ per insert | **$O(\log n)$ per insert** |

---

## 3. Syntax / Python Idioms

Because Python's standard `heapq` module only provides min-heap functionality, max-heaps are implemented using several recognized idioms:

### 1. Value Negation (Most Common)
```python
import heapq
max_heap = []
heapq.heappush(max_heap, -val)
largest = -heapq.heappop(max_heap)
```

### 2. Custom Wrapper with Inverted `__lt__`
```python
class MaxHeapItem:
    def __init__(self, val):
        self.val = val
    def __lt__(self, other):
        return self.val > other.val  # Inverted comparison
```

### 3. CPython Internal Helpers
```python
import heapq
heapq._heapify_max(arr)
largest = heapq._heappop_max(arr)
```

---

## 4. Key Algorithmic Mechanics

### 1. Sift-Up for Max Heap
When a new value is appended, compare it to its parent at `(i - 1) // 2`. If `heap[i] > heap[parent]`, swap them and repeat upward until reaching the root or finding a parent with greater/equal value.

### 2. Sift-Down for Max Heap
After replacing the root with the last array element, compare it with the larger of its two children (`left = 2i + 1`, `right = 2i + 2`). Swap downward with the larger child until the node is greater than or equal to both children.

### 3. Dual-Heap Stream Median Pattern
To maintain running median of an incoming stream of numbers in $O(\log n)$ add and $O(1)$ lookup:
- **Max-Heap (`small`):** Holds the smaller half of the numbers.
- **Min-Heap (`large`):** Holds the larger half of the numbers.
- Invariant: `len(small) == len(large)` (even) or `len(small) == len(large) + 1` (odd).

---

## 5. Examples

### Example 1: Max Heap from Scratch
```python
class MaxHeap:
    def __init__(self):
        self.heap = []

    def push(self, val):
        self.heap.append(val)
        i = len(self.heap) - 1
        while i > 0 and self.heap[i] > self.heap[(i - 1) // 2]:
            p = (i - 1) // 2
            self.heap[i], self.heap[p] = self.heap[p], self.heap[i]
            i = p

    def pop_max(self):
        val = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._sift_down(0)
        return val
```

### Example 2: Last Stone Weight Simulation
```python
import heapq

def last_stone_weight(stones):
    max_heap = [-s for s in stones]
    heapq.heapify(max_heap)
    while len(max_heap) > 1:
        s1 = -heapq.heappop(max_heap)
        s2 = -heapq.heappop(max_heap)
        if s1 != s2:
            heapq.heappush(max_heap, -(s1 - s2))
    return -max_heap[0] if max_heap else 0
```

### Example 3: Running Median via Dual Heaps
```python
class MedianFinder:
    def __init__(self):
        self.small = []  # max-heap (negated)
        self.large = []  # min-heap

    def add_num(self, num):
        heapq.heappush(self.small, -num)
        if self.small and self.large and (-self.small[0] > self.large[0]):
            heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.small) > len(self.large) + 1:
            heapq.heappush(self.large, -heapq.heappop(self.small))
        elif len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def find_median(self):
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0
```

---

## 6. Output

```
1. Max Heap from Scratch:
   Inserted: [10, 30, 20, 5, 1, 40, 15]
   Heap Array: [40, 10, 30, 5, 1, 20, 15]
   Maximum: 40
   Extracted Descending: [40, 30, 20, 15, 10, 5, 1]

2. Last Stone Weight:
   Stones: [2, 7, 4, 1, 8, 1] -> Remaining Stone: 1

3. Data Stream Median:
   Add 5  -> Median: 5.00
   Add 15 -> Median: 10.00
   Add 1  -> Median: 5.00
   Add 3  -> Median: 4.00
```

---

## 7. Code Explanation

| Component | Responsibility |
|---|---|
| `while i > 0 and heap[i] > heap[parent]` | Sift-up condition guaranteeing parent is always strictly greater or equal |
| `-s for s in stones` | Standard inversion technique transforming min-heap logic into max-heap semantics |
| `Dual Heaps (small, large)` | Partitions stream into lower half and upper half, balancing boundaries at median |
| `heapq._heapify_max` | Private CPython implementation of Floyd's max-heap construction algorithm |
| Inverted `__lt__` | Allows complex user-defined objects to be ordered in descending priority |

---

## 8. Common Mistakes

1. **Forgetting to Negate When Extracting**:
   Popping from a negated max-heap returns a negative value. Forgetting the leading `-` produces incorrect signs (`-100` instead of `100`).
2. **Tuple Sorting Pitfalls**:
   When storing tuples `(-priority, task_object)`, Python compares `task_object` if priorities are equal. If the object lacks `__lt__`, a `TypeError` occurs. Use a unique counter `(-priority, count, task)` to break ties safely.
3. **Imbalance in Dual-Heap Median Finder**:
   Failing to rebalance when `len(large) > len(small)` leads to an incorrect median index calculation.
4. **Using Private `_heappop_max` in Production**:
   Methods with leading underscores (`_heappop_max`) are internal implementation details not guaranteed to remain stable across Python versions. Negation or wrapper classes are preferred.
5. **Direct Indexing on Unsorted Array**:
   `heap[1]` is not necessarily the second largest element; it could be smaller than `heap[2]`. Only `heap[0]` is guaranteed to be maximal.

---

## 9. Practice Questions

1. Implement **Sliding Window Median** using dual heaps with lazy deletion of out-of-window elements.
2. Find the $K$ pairs with the smallest sums from two sorted arrays using a heap.
3. Implement a priority CPU Task Scheduler with cooldown intervals using a max-heap and queue.
4. Reorganize string characters so that the most frequent characters are separated by at least distance $d$.
5. Implement in-place **Heap Sort** in ascending order using a Max-Heap.

---

## 10. Interview Questions

**Q1: Why does in-place Heap Sort in ascending order use a Max-Heap instead of a Min-Heap?**
Because a Max-Heap places the maximum element at index 0. By swapping `heap[0]` with `heap[end]` and reducing heap size, the largest elements are naturally deposited into the back of the array in ascending order without requiring auxiliary storage.

**Q2: What is the time complexity of building a Max-Heap using Floyd's algorithm?**
$O(n)$ time. Sifting down from index $\lfloor n / 2 \rfloor - 1$ down to 0 spends less work on nodes with larger subtrees and more work on fewer nodes at higher heights.

**Q3: How does the Dual-Heap pattern maintain the running median in $O(\log n)$?**
By maintaining equal (or off-by-one) sizes between a Max-Heap (lower half) and a Min-Heap (upper half), the median is always accessible at the roots in $O(1)$ time, and additions take $O(\log n)$ to sift into the correct half.

**Q4: How do you handle element deletions in a heap when the element is not at the root?**
Standard binary heaps take $O(n)$ to locate an arbitrary element. To support $O(\log n)$ arbitrary deletion, maintain an auxiliary hash map (`val -> index`) and update indices on every swap (Indexed Priority Queue).

**Q5: What is the worst-case space complexity of a Max-Heap?**
$O(n)$ to store the array of $n$ elements. Auxiliary space during heap operations is $O(1)$ iterative.
