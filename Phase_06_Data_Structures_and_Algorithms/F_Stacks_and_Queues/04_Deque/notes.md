# Deque — Double-Ended Queue (Circular Array Deque, Work-Stealing & 0-1 BFS)

---

## 1. Introduction

A **Deque** (**Double-Ended Queue**, pronounced *"deck"*) is a generalized linear data structure that supports **$O(1)$ insertion and deletion at both the front and the rear**:

$$\text{Front (`appendleft` / `popleft`)} \longleftrightarrow [10, \; 20, \; 30, \; 40] \longleftrightarrow \text{Rear (`append` / `pop`)}$$

A Deque unifies both **Stacks (LIFO)** and **Queues (FIFO)** into a single container:
- Using only `append()` + `pop()` turns a Deque into a **LIFO Stack**.
- Using only `append()` + `popleft()` turns a Deque into a **FIFO Queue**.
- Using all four operations unlocks **Work-Stealing Thread Schedulers**, **0-1 Breadth-First Search ($O(V + E)$ shortest paths)**, **Sliding Window Monotonic Queues**, and **Two-Ended Palindrome Verification**.

---

## 2. Why is it used?

1. **Python's Built-In `collections.deque`:** Implemented in C as a doubly linked list of 64-element fixed arrays (`BLOCKLEN = 64`), guaranteeing **strict worst-case $O(1)$** `append`, `appendleft`, `pop`, and `popleft` with zero whole-array reallocation pauses.
2. **0-1 BFS Shortest Paths on Binary-Weight Graphs:** When graph edge weights are in $\{0, 1\}$, pushing $0$-weight transitions to the **front** (`appendleft`) and $1$-weight transitions to the **back** (`append`) finds shortest paths in **$O(V + E)$ linear time** (faster than Dijkstra's $O((V + E) \log V)$ heap algorithm!).
3. **Work-Stealing Multi-Core Schedulers (Go runtime, Tokio, Java `ForkJoinPool`):** Each CPU core executes its own spawned tasks in LIFO order from the **front** (`popleft`) for cache warmth, while idle CPU cores steal coarse tasks in FIFO order from the **rear** (`pop`) to minimize contention.
4. **Bounded Sliding History (`deque(maxlen=k)`):** Automatically evicts the oldest element from the opposite end in $O(1)$ time whenever a new item is appended to a full deque (just like Unix `tail -n k`).

---

## 3. Syntax

### A. Python `collections.deque` Core API
```python
from collections import deque

dq: deque[int] = deque([20, 30])
dq.appendleft(10)       # [10, 20, 30] -> O(1)
dq.append(40)           # [10, 20, 30, 40] -> O(1)
left_val = dq.popleft() # 10 -> O(1)
right_val = dq.pop()    # 40 -> O(1)
dq.rotate(1)            # Rotate right by 1 step -> O(k)
```

### B. Circular Array Deque Backward-Wrap Formula (LeetCode 641)
```python
def insertFront(self, value: int) -> bool:
    if self.isFull():
        return False
    # Step `_front` backward by 1 modulo capacity!
    self._front = (self._front - 1) % self._capacity
    self._buffer[self._front] = value
    self._size += 1
    return True
```

---

## 4. Explanation (Step-by-Step)

### 1. How Circular Array `insertFront` and `deleteLast` Work in $O(1)$
In a Circular Queue, `_front` only ever moves **forward** (`(_front + 1) % k`), and new items are written at `(_front + _size) % k`.
To upgrade a Circular Queue into a **Circular Deque**:
- **`insertFront(val)`:** Decrements `_front` modulo $k$ **before** writing:
  $$\text{self.\_front} = (\text{self.\_front} - 1) \bmod k$$
  (In Python, `-1 % 4 == 3`, so stepping backward from index `0` wraps directly to index `k - 1`!)
- **`deleteLast()`:** Simply clears the rear slot `(_front + _size - 1) % k` and decrements `_size -= 1` without touching `_front`!

### 2. Why 0-1 BFS Works in $O(V + E)$ Time
In standard BFS, the queue maintains the **Two-Layer Distance Invariant**: at any moment, the queue contains vertices of distance $d$ followed by vertices of distance $d + 1$.
When relaxing an edge $(u, v)$ from vertex $u$ at distance $d$ (popped from the front):
- If weight $w = 0$, $v$ also has distance $d$, so pushing $v$ to the **front** (`appendleft`) keeps it among the distance-$d$ vertices!
- If weight $w = 1$, $v$ has distance $d + 1$, so pushing $v$ to the **back** (`append`) places it with the distance-$(d + 1)$ vertices!
Thus the deque remains sorted by distance at all times without a heap!

---

## 5. Minimum 3 Examples

### Example 1: Circular Array Deque Implementation (LeetCode 641)
File: [`example_01_circular_array_deque_implementation.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/F_Stacks_and_Queues/04_Deque/example_01_circular_array_deque_implementation.py)

```python
class MyCircularDeque(Generic[T]):
    """Fixed-capacity Circular Array Deque (LeetCode 641) with O(1) operations at both ends."""

    def __init__(self, k: int) -> None:
        if k <= 0:
            raise ValueError("Capacity k must be positive")
        self._capacity: int = k
        self._buffer: List[Optional[T]] = [None] * k
        self._front: int = 0
        self._size: int = 0

    def insertFront(self, value: T) -> bool:
        if self.isFull():
            return False
        self._front = (self._front - 1) % self._capacity
        self._buffer[self._front] = value
        self._size += 1
        return True

    def insertLast(self, value: T) -> bool:
        if self.isFull():
            return False
        rear_write = (self._front + self._size) % self._capacity
        self._buffer[rear_write] = value
        self._size += 1
        return True
```

---

### Example 2: `collections.deque` Rotation, Bounded `maxlen` & Work-Stealing Scheduler
File: [`example_02_collections_deque_and_work_stealing.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/F_Stacks_and_Queues/04_Deque/example_02_collections_deque_and_work_stealing.py)

```python
def is_palindrome_via_deque(text: str) -> bool:
    """Checks alphanumeric palindrome by popping from both ends of a deque simultaneously."""
    cleaned = [ch.lower() for ch in text if ch.isalnum()]
    dq: Deque[str] = deque(cleaned)
    while len(dq) > 1:
        if dq.popleft() != dq.pop():
            return False
    return True
```

---

### Example 3: 0-1 BFS Shortest Path & Design Front-Middle-Back Queue (LeetCode 1670)
File: [`example_03_zero_one_bfs_and_front_middle_back_queue.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/F_Stacks_and_Queues/04_Deque/example_03_zero_one_bfs_and_front_middle_back_queue.py)

```python
def zero_one_bfs_shortest_path(
    num_nodes: int, adj: Dict[int, List[Tuple[int, int]]], src: int
) -> List[int]:
    INF = 10**9
    dist = [INF] * num_nodes
    dist[src] = 0
    dq: Deque[int] = deque([src])

    while dq:
        u = dq.popleft()
        for v, weight in adj.get(u, []):
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                if weight == 0:
                    dq.appendleft(v)
                else:
                    dq.append(v)

    return dist
```

---

## 6. Output

### Output — Example 1 (`example_01_circular_array_deque_implementation.py`)
```text
========================================================================
Circular Array Deque (LeetCode 641) — O(1) Front and Rear Operations
========================================================================
After insertLast(20, 30) & insertFront(10, 5):
  Logical Deque : [5, 10, 20, 30] (Front=5, Rear=30)
  Raw Buffer    : [20, 30, 5, 10] (_front=2, isFull=True)

After deleteFront() & deleteLast():
  Logical Deque : [10, 20] (Front=10, Rear=20)
  Raw Buffer    : [20, None, None, 10] (_front=3)
```

### Output — Example 2 (`example_02_collections_deque_and_work_stealing.py`)
```text
========================================================================
1. `collections.deque` Rotation & Bounded `maxlen` Tail Window
========================================================================
After rotate(+2) on [10..50]: [40, 50, 10, 20, 30]
After rotate(-2)            : [10, 20, 30, 40, 50]
Bounded deque(maxlen=3) after 6 lines: ['log_line_4', 'log_line_5', 'log_line_6']

========================================================================
2. Two-Ended Deque Palindrome Check
========================================================================
  'A man, a plan, a canal: Panama' -> True
  'Race a car' -> False

========================================================================
3. Work-Stealing Deque Scheduler (LIFO Local Front, FIFO Steal Rear)
========================================================================
Initial Worker 0 Deque (front -> rear): ['Subtask_A1', 'Subtask_A2', 'Root_Chunk_A', 'Root_Chunk_B', 'Root_Chunk_C']
Initial Worker 1 Deque (idle)         : []

Worker 1 steals coarse task from Worker 0's rear -> 'Root_Chunk_C'
Worker 0 Deque now: ['Subtask_A1', 'Subtask_A2', 'Root_Chunk_A', 'Root_Chunk_B']
Worker 1 Deque now: ['Root_Chunk_C']
Worker 0 executes front (LIFO): 'Subtask_A1'
Worker 1 executes stolen task : 'Root_Chunk_C'
```

### Output — Example 3 (`example_03_zero_one_bfs_and_front_middle_back_queue.py`)
```text
========================================================================
1. 0-1 BFS Shortest Path on a Binary-Weight Graph in O(V + E) Time
========================================================================
Graph edges (u -> (v, w in {0,1})): {0: [(1, 1), (2, 1)], 2: [(3, 0)], 3: [(1, 0), (4, 1)], 1: [(4, 1)]}
Shortest distances from node 0     : [0, 1, 1, 1, 2]

========================================================================
2. Front-Middle-Back Queue in O(1) via Two Balanced Deques (LeetCode 1670)
========================================================================
After pushFront(1), pushBack(2), pushMiddle(3), pushMiddle(4): [1, 4, 3, 2]
popFront()  -> 1 | Queue: [4, 3, 2]
popMiddle() -> 3 | Queue: [4, 2]
popMiddle() -> 4 | Queue: [2]
popBack()   -> 2 | Queue: []
```

---

## 7. Code Explanation

1. **How `FrontMiddleBackQueue` Achieves $O(1)$ Middle Access Using Two Deques:**
   A single deque cannot insert or delete at the middle in $O(1)$ time (middle indexing on `collections.deque` is $O(n)$). By splitting the queue into `left` (first $\lfloor n/2 \rfloor$ items) and `right` (remaining $\lceil n/2 \rceil$ items), the **middle of the whole queue is just the rear of `left` (`left[-1]`) or the front of `right` (`right[0]`)**, where deque operations are $O(1)$!
2. **Negative Modulo in C/Java vs Python for `insertFront`:**
   In Python, `(-1) % k` is `k - 1`. In C, C++, Java, and JavaScript, `(-1) % k` evaluates to `-1`! In those languages, you must write `(front - 1 + k) % k`.

---

## 8. Common Mistakes

1. **Random Indexing `dq[n // 2]` Inside a Loop on `collections.deque`:**
   Because CPython's `collections.deque` is a doubly linked list of 64-item blocks (not a single contiguous array), accessing `dq[i]` near the middle walks $O(n / 64) = O(n)$ block pointers! Use a Python `list` if you need $O(1)$ random middle indexing, or two balanced deques if you need $O(1)$ front, middle, and back updates.
2. **Slicing a `collections.deque` (`dq[1:4]`):**
   `collections.deque` does not support slice syntax (`TypeError: sequence index must be integer, not 'slice'`). Use `itertools.islice(dq, start, stop)` or `popleft()`/`pop()`.

---

## 9. Practice Questions

1. **Easy — Zigzag Level Order / Spiral Array Construction:**
   Given a list of integers `[1..n]`, alternately pop from the front and back of a deque to construct a wave-like permutation `[1, n, 2, n-1, 3, ...]`.
2. **Medium — Minimum Obstacle Removal to Reach Corner (LeetCode 2290):**
   Given a 2D grid of `0` (empty) and `1` (obstacle), model each cell transition into a `0` cell as weight $0$ (`appendleft`) and into a `1` cell as weight $1$ (`append`), solving minimum obstacles removed via 0-1 BFS in $O(R \cdot C)$ time.
3. **Hard — Minimum Cost to Make at Least One Valid Path in a Grid (LeetCode 1368):**
   Each cell has a directional arrow (`R`, `L`, `D`, `U`). Following the arrow costs $0$; changing the arrow costs $1$. Use a Deque and 0-1 BFS to find the minimum cost from `(0, 0)` to `(R - 1, C - 1)` in $O(R \cdot C)$ time.

---

## 10. Interview Questions

### Q1: How is CPython's `collections.deque` implemented under the hood in C?
**Answer:** Unlike Java's `ArrayDeque` (a single dynamically resizing circular array), CPython implements `collections.deque` as a **doubly linked list of fixed-size 64-pointer blocks (`struct BLOCK`)**, maintaining `leftblock`/`leftindex` and `rightblock`/`rightindex` pointers plus a free-list of up to 2 spare blocks. This gives **strict worst-case $O(1)$** ends operations without ever copying $O(n)$ elements during a resize!

### Q2: Why do work-stealing thread pools have the local worker pop from the **front (LIFO)** while thief threads steal from the **back (FIFO)**?
**Answer:**
1. **Cache Locality:** The most recently spawned subtask at the front operates on data still hot in the local CPU core's L1/L2 cache.
2. **Work Granularity:** Tasks at the rear (oldest tasks) are high up in the recursion tree and represent large chunks of work, so stealing one task from the rear keeps the thief thread busy for a long time and minimizes lock/atomic contention between the owner (at the front) and thieves (at the rear).

### Q3: Can 0-1 BFS be used if edge weights are in $\{0, 1, 2\}$?
**Answer:** Standard 0-1 BFS only works when edge weights are in $\{0, 1\}$ (or $\{0, w\}$ for a single constant $w$) because a deque has only two ends (distance $d$ at the front, $d + 1$ at the back). For weights in $\{0, 1, \dots, K\}$ with small integer $K$, use **Dial's Algorithm** (an array of $K + 1$ buckets).

