# Priority Queue

## 1. Introduction

A **Priority Queue** is an abstract data type (ADT) similar to a standard queue or stack, but where each element has an associated **priority**.

In a priority queue, an element with high priority is served before an element with low priority. If two elements have the same priority, they are served according to their ordering in the queue (or via explicit tie-breaking rules such as FIFO). While priority queues can be implemented with arrays or linked lists, they are most efficiently implemented using a **Binary Heap**, achieving $O(\log n)$ insertions and extractions.

---

## 2. Why Use Priority Queues?

| Problem / System Domain | Naive Approach | Priority Queue Approach | Time Improvement |
|---|---|---|---|
| **Dijkstra's Shortest Path** | Scan all vertices ($O(V^2)$) | Min-PQ extraction | $O(V^2) \to O((V + E) \log V)$ |
| **Prim's Minimum Spanning Tree** | Linear edge scan ($O(V^2)$) | Min-PQ key extraction | $O(V^2) \to O(E \log V)$ |
| **Merge $K$ Sorted Lists** | Compare all $K$ heads ($O(N \cdot K)$) | Min-PQ of size $K$ | $O(N \cdot K) \to O(N \log K)$ |
| **CPU Task Scheduling** | Sorting on each cycle ($O(n^2)$) | Max-PQ + Cooldown Queue | $O(n)$ scheduling |
| **Event-Driven Simulation** | Chronological sort per insert | Timestamp Priority Queue | $O(\log n)$ event scheduling |

---

## 3. Syntax / API Reference

### Python `heapq` as a Priority Queue
```python
import heapq
import itertools

pq = []
counter = itertools.count()  # Unique tie-breaker sequence

# Enqueue
heapq.heappush(pq, (priority, next(counter), task))

# Dequeue
priority, count, task = heapq.heappop(pq)
```

### Thread-Safe `queue.PriorityQueue`
```python
from queue import PriorityQueue
q = PriorityQueue()
q.put((priority, item))
item = q.get()
```

---

## 4. Key Algorithmic Mechanics

### 1. The Comparison Tuple Pattern & Tie-Breaking
Python compares tuples lexicographically: `(a1, a2, a3) < (b1, b2, b3)`.
If `a1 == b1`, Python compares `a2` and `b2`.
If tasks are custom objects lacking `__lt__`, equal priorities cause a `TypeError: '<' not supported between instances`.
Adding a strictly increasing sequence counter `(priority, count, task)` guarantees that:
- Priorities are checked first.
- If priorities are identical, `count` breaks ties in strict **FIFO order**.
- Python never attempts to compare the actual `task` objects.

### 2. Indexed Priority Queue (IPQ) & `decrease_key`
Standard heaps take $O(n)$ to locate an element. An **Indexed Priority Queue** maintains an auxiliary hash map `pos[key] = index` tracking each item's current slot in the heap array.
Whenever two heap elements swap, their indices in `pos` are updated in $O(1)$. This allows:
- `decrease_key(key, new_prio)` in $O(\log n)$ by sifting up from `pos[key]`.
- `delete(key)` in $O(\log n)$ by swapping with the last element and sifting.

---

## 5. Examples

### Example 1: Stable Priority Queue (FIFO Tie-Breaking)
```python
class StablePriorityQueue:
    def __init__(self):
        self.pq = []
        self.counter = itertools.count()

    def push(self, task, priority=0):
        entry = (priority, next(self.counter), task)
        heapq.heappush(self.pq, entry)

    def pop(self):
        return heapq.heappop(self.pq)[2]
```

### Example 2: Indexed Priority Queue (Decrease-Key)
```python
class IndexedPriorityQueue:
    def __init__(self):
        self.heap, self.pos = [], {}

    def decrease_key(self, key, new_priority):
        idx = self.pos[key]
        self.heap[idx][1] = new_priority
        self._sift_up(idx)
```

### Example 3: Merge $K$ Sorted Lists
```python
def merge_k_lists(lists):
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))
    dummy = ListNode(0)
    tail = dummy
    while heap:
        val, i, node = heapq.heappop(heap)
        tail.next = node
        tail = tail.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next
```

---

## 6. Output

```
1. Stable Priority Queue:
   Priority 1: Task(Urgent Alert)
   Priority 2: Task(Email Digest)  (Enqueued first)
   Priority 2: Task(DB Backup)      (Enqueued second, FIFO preserved)
   Priority 3: Task(Health Check)

2. Indexed Priority Queue:
   Initial distance to 'B': 25
   decrease_key('B', 5) -> Sifted up to index 0
   Popped minimum: 'B' with distance 5

3. Merge K Sorted Lists:
   Input: [[1, 4, 5], [1, 3, 4], [2, 6]]
   Merged: [1, 1, 2, 3, 4, 4, 5, 6]
```

---

## 7. Code Explanation

| Mechanism | Purpose |
|---|---|
| `itertools.count()` | Generates monotonically increasing integers for $O(1)$ collision resolution |
| `pos[key] = index` | Dual mapping enables $O(1)$ random access to arbitrary heap positions |
| `list_index` in tuple | Resolves identical node values in Merge $K$ Lists without comparing `ListNode` |
| `cooldown_q = deque()` | Holds completed tasks with `(task, ready_time)` until cooldown expires |
| Thread-Safe `queue.PriorityQueue` | Uses internal locks and condition variables for multithreaded worker pools |

---

## 8. Common Mistakes

1. **Unorderable Object Exception**:
   Pushing `(priority, task)` directly causes `TypeError` when two tasks share the same priority. Always insert an integer counter `(priority, count, task)`.
2. **Confusing Thread-Safe Queue with `heapq`**:
   `queue.PriorityQueue` carries thread locking overhead and is significantly slower for pure algorithmic competitive programming than `heapq`.
3. **Lazy Deletion Stale Entries**:
   When implementing Dijkstra with standard `heapq`, updating a distance pushes a new tuple `(new_dist, u)`. Forgetting to check `if d > dist[u]: continue` wastes time processing outdated paths.
4. **Mutating Priorities Outside the Queue**:
   Directly altering `task.priority` while the item is already inside the heap breaks heap ordering. You must use an IPQ or push a fresh entry.
5. **Memory Leaks in Graph Algorithms**:
   Not discarding or skipping visited nodes in dense graphs causes the priority queue to balloon to $O(E)$ memory.

---

## 9. Practice Questions

1. Implement **Dijkstra's Algorithm** with an Indexed Priority Queue and compare runtime against lazy-deletion standard heap.
2. Solve **Reorganize String** using a Priority Queue of character frequencies.
3. Implement a dynamic **Median Maintenance** system using two priority queues.
4. Solve **Swim in Rising Water** using a priority queue (modified Dijkstra on grid).
5. Design a Rate Limiter allowing at most $K$ events per time window using a timestamp priority queue.

---

## 10. Interview Questions

**Q1: What is the difference between a Queue and a Priority Queue?**
A standard Queue strictly obeys First-In, First-Out (FIFO) ordering. A Priority Queue serves elements based on highest (or lowest) priority score, regardless of insertion order.

**Q2: What is an Indexed Priority Queue and why is it important?**
An Indexed Priority Queue maintains a map from key to array index, enabling `decrease_key` and arbitrary deletions in $O(\log n)$ time. It improves Dijkstra's algorithm from $O(E \log E)$ space/time with duplicate pushes to optimal $O((V + E) \log V)$ with at most $V$ entries in the heap.

**Q3: How do you implement a priority queue if all priorities are small integers (e.g., $1 \dots K$)?**
Use **Dial's Algorithm** (Bucket Queue): an array of $K$ FIFO queues (or linked lists) where `buckets[p]` holds elements of priority $p$. Pushing and popping take $O(1)$ time, outperforming binary heaps.

**Q4: Can a priority queue be made stable (preserving FIFO for equal priorities)?**
Yes, by appending a monotonic sequence counter to each entry: `(priority, count, item)`. Because `count` strictly increments, equal priorities are tie-broken by `count`, guaranteeing FIFO ordering.

**Q5: What is the time complexity of building a Priority Queue from $N$ items?**
$O(N)$ time using Floyd's bottom-up `heapify()`. Inserting elements one by one takes $O(N \log N)$.
