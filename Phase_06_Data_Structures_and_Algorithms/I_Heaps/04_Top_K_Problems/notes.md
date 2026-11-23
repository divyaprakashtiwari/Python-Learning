# Top K Problems

## 1. Introduction

**Top K Problems** represent a widely encountered class of computational challenges where the goal is to identify, rank, or reorder the $K$ most significant elements (largest, smallest, closest, or most frequent) from a dataset of size $N$.

While a naive strategy sorts the entire dataset in $O(N \log N)$ time, heap-based patterns solve Top $K$ problems in **$O(N \log K)$** time (or $O(K \log K)$ for multi-way combinations) and $O(K)$ auxiliary space, operating efficiently even over infinite or unbounded streaming data.

---

## 2. Why Use Heaps for Top K Problems?

| Algorithmic Pattern | Full Sorting | Heap Optimization | Time Improvement |
|---|---|---|---|
| **$K$ Largest Elements** | Sort all $N$ ($O(N \log N)$) | Min-Heap of size $K$ | $O(N \log N) \to O(N \log K)$ |
| **$K$ Smallest Elements** | Sort all $N$ ($O(N \log N)$) | Max-Heap of size $K$ | $O(N \log N) \to O(N \log K)$ |
| **$K$ Closest Points to Origin** | Sort all $N$ ($O(N \log N)$) | Max-Heap of size $K$ | $O(N \log N) \to O(N \log K)$ |
| **Reorganize String** | Infeasible / trial-and-error | Max-Heap of char frequencies | Greedy $O(N \log A)$ |
| **$K$ Smallest Pair Sums** | Compute all $N \times M$ pairs | Frontier Min-Heap of size $K$ | $O(NM \log(NM)) \to O(K \log K)$ |

---

## 3. The Fundamental Duality Rule

A critical insight that prevents subtle bugs:
- **To find the $K$ LARGEST elements:** Maintain a **MIN-HEAP** of size $K$. The root holds the smallest of the top $K$, acting as the threshold that candidates must exceed.
- **To find the $K$ SMALLEST elements:** Maintain a **MAX-HEAP** of size $K$. The root holds the largest of the bottom $K$, acting as the ceiling that candidates must fall below.

---

## 4. Key Algorithmic Mechanics

### 1. Fixed-Size Bounded Heap ($O(N \log K)$)
Iterate through $N$ items. If heap size $< K$, push immediately. Otherwise, if the candidate improves upon the root threshold, replace the root using `heapq.heapreplace()`, maintaining strictly $K$ elements in $O(\log K)$ time per replacement.

### 2. Multi-Way Frontier Heap (Smallest Pair Sums)
When finding pairs $(A[i], B[j])$ from two sorted arrays, avoid evaluating the full Cartesian product $O(N \cdot M)$.
1. Initialize a Min-Heap with the first column: $(A[i] + B[0], i, 0)$ for $i \in [0, \min(K, |A|)-1]$.
2. At each extraction of $(A[i] + B[j])$, push the adjacent successor $(A[i] + B[j + 1])$ into the heap.
3. This explores candidates along an expanding wavefront in strictly $O(K \log K)$ time.

### 3. Greedy Frequency Dissimilarity (Reorganize String)
Always consume the character with the **highest remaining frequency** first. To prevent adjacent duplicate letters, retain the previously used character outside the heap until another character has been placed, then push it back.

---

## 5. Examples

### Example 1: K Closest Points to Origin
```python
def k_closest(points, k):
    max_heap = []
    for x, y in points:
        dist_sq = x * x + y * y
        if len(max_heap) < k:
            heapq.heappush(max_heap, (-dist_sq, x, y))
        elif dist_sq < -max_heap[0][0]:
            heapq.heapreplace(max_heap, (-dist_sq, x, y))
    return [[x, y] for _, x, y in max_heap]
```

### Example 2: Reorganize String
```python
def reorganize_string(s):
    counts = Counter(s)
    if max(counts.values()) > (len(s) + 1) // 2:
        return ""
    max_heap = [(-freq, char) for char, freq in counts.items()]
    heapq.heapify(max_heap)
    res, prev_freq, prev_char = [], 0, ""
    while max_heap:
        freq, char = heapq.heappop(max_heap)
        res.append(char)
        if prev_freq < 0:
            heapq.heappush(max_heap, (prev_freq, prev_char))
        prev_freq, prev_char = freq + 1, char
    return "".join(res)
```

### Example 3: K Pairs with Smallest Sums
```python
def k_smallest_pairs(nums1, nums2, k):
    heap = []
    for i in range(min(k, len(nums1))):
        heapq.heappush(heap, (nums1[i] + nums2[0], i, 0))
    res = []
    while heap and len(res) < k:
        _, i, j = heapq.heappop(heap)
        res.append([nums1[i], nums2[j]])
        if j + 1 < len(nums2):
            heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))
    return res
```

---

## 6. Output

```
1. K Closest Points to Origin:
   Points: [[1, 3], [-2, 2], [5, 8], [0, 1]], k = 2
   Result: [[-2, 2], [0, 1]]

2. Reorganize String:
   'aab'     -> 'aba'
   'aaab'    -> '' (Impossible: max frequency exceeds (N+1)//2)
   'vvvlo'   -> 'vlvov'

3. Smallest Pair Sums:
   nums1 = [1, 7, 11], nums2 = [2, 4, 6], k = 3
   Result: [[1, 2], [1, 4], [1, 6]]
```

---

## 7. Code Explanation

| Mechanism | Purpose |
|---|---|
| `dist_sq = x*x + y*y` | Avoids expensive floating-point `sqrt()` while preserving monotonic distance order |
| `heapq.heapreplace()` | Combines pop and push into a single $O(\log K)$ sift operation |
| `prev_freq < 0` delay | Prevents the same character from being placed consecutively |
| Frontier push `(i, j + 1)` | Increments column index on demand, avoiding memory allocation for all pairs |
| Alphabet bound $O(N \log A)$ | Since $|A| \le 26$, string reorganization runs in linear $O(N)$ real time |

---

## 8. Common Mistakes

1. **Inverting Heap Type (Min vs Max)**:
   Using a Min-Heap for $K$ smallest causes the smallest elements to be evicted early. Always use a Max-Heap for $K$ smallest and Min-Heap for $K$ largest.
2. **Generating Full Cartesian Product**:
   Computing all $N \times M$ pairs before pushing to a heap uses $O(NM)$ space and $O(NM \log(NM))$ time. Always use an index-driven frontier heap.
3. **Pigeonhole Principle Check Omission in Reorganize String**:
   If any character frequency exceeds $\lfloor (N + 1) / 2 \rfloor$, it is mathematically impossible to avoid adjacent duplicates. Checking this upfront saves processing time.
4. **Floating Point Roundoff in Distance Sorting**:
   Using `math.sqrt(x**2 + y**2)` can introduce floating-point inaccuracies when comparing coordinates. Compare raw integer squared sums $x^2 + y^2$.
5. **Over-Allocating Initial Frontier**:
   Pushing all $N$ elements into the pair heap when $K < N$ wastes memory. Bound initial pushes by $\min(K, N)$.

---

## 9. Practice Questions

1. Implement **Top K Frequent Words** sorted by frequency descending, then lexicographically ascending.
2. Solve **Ugly Numbers II** (finding the $N$-th ugly number) using a Min-Heap generator.
3. Find the $K$-th smallest element in a row-wise and column-wise sorted 2D matrix in $O(K \log(\min(K, N)))$ time.
4. Implement **Rearrange String K Distance Apart** using a max-heap and a sliding cooldown queue.
5. Solve **Meeting Rooms II** (minimum conference rooms required) using a Min-Heap of end times.

---

## 10. Interview Questions

**Q1: When is QuickSelect preferred over a Heap for finding the $K$-th largest element?**
QuickSelect achieves $O(N)$ average time and $O(1)$ auxiliary space, outperforming the heap's $O(N \log K)$ time. However, QuickSelect modifies the array in-place, has $O(N^2)$ worst-case time, and cannot handle continuous streaming data. For streams, bounded heaps are mandatory.

**Q2: How does `heapq.nsmallest(k, arr)` work internally in Python?**
For small $K$ ($K \le N / 4$), Python builds a max-heap of size $K$ and iterates through the remaining elements with `heapreplace`, running in $O(N \log K)$. For large $K$, it simply calls `sorted(arr)[:k]` in $O(N \log N)$ (using Timsort).

**Q3: How does the frontier heap avoid visiting all $N \times M$ pairs in Smallest Pair Sums?**
Because the arrays are sorted, $A[i] + B[j] \le A[i] + B[j + 1]$. Pushing only the next column candidate $j + 1$ upon popping guarantees that the next smallest pair must already be in the heap without enumerating the rest of the matrix.

**Q4: What is the maximum frequency of any character for a valid string reorganization with no adjacent duplicates?**
$\lfloor (N + 1) / 2 \rfloor$. By the Pigeonhole Principle, if any character appears more than this threshold, at least two occurrences must sit adjacent to each other.

**Q5: Can Top K Problems be solved in $O(N)$ worst-case time deterministically?**
Yes, using the Median-of-Medians (BFPRT) selection algorithm, which guarantees $O(N)$ worst-case time for finding the $K$-th element, followed by partitioning.
