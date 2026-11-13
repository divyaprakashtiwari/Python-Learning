# Queue Implementation (Linked FIFO Queue, `collections.deque`, Two-Stack Queue & Rate Limiting)

---

## 1. Introduction

A **Queue** is a linear **First-In, First-Out (FIFO)** abstract data type in which new elements are added at the **rear (back / tail)** and existing elements are removed from the **front (head)**, just like customers waiting in a checkout line:

$$\text{Front (`dequeue() -> 10`)} \leftarrow [10, \; 20, \; 30, \; 40] \leftarrow \text{Rear (`enqueue(50)`)}$$

Every core Queue operation runs in **$O(1)$ time**:
- **`enqueue(x)` / `append(x)`**: Insert `x` at the rear of the queue.
- **`dequeue()` / `popleft()`**: Remove and return the front element (raises `IndexError` if empty).
- **`peek()` / `front()`**: Read the front element without removing it.
- **`is_empty()` / `__len__()`**: Check if the queue contains 0 elements.

---

## 2. Why is it used?

1. **Breadth-First Search (BFS) & Level-Order Tree Traversal:** Visiting nodes layer-by-layer in graphs and trees requires a FIFO queue so that all nodes at distance $d$ are processed before any node at distance $d + 1$.
2. **Task Queues, Message Brokers & Event Loops:** Producer-consumer pipelines (`asyncio`, Celery, RabbitMQ, OS IO queues) buffer incoming requests in arrival order.
3. **Sliding Time-Window Rate Limiters & Hit Counters:** API gateways store request timestamps in a FIFO queue and evict expired timestamps from the front in amortized $O(1)$ time (LeetCode 362 / 933).
4. **Why `list.pop(0)` Must Never Be Used as a Queue:** Removing index `0` from a Python `list` shifts all $n - 1$ remaining elements left in memory ($O(n)$ per dequeue, or $O(n^2)$ to drain $n$ items). Always use `collections.deque` or a pointer-based `LinkedQueue`!

---

## 3. Syntax

### A. Idiomatic Python FIFO Queue Using `collections.deque`
```python
from collections import deque

q: deque[str] = deque()
q.append("task_1")          # enqueue at rear  -> O(1)
q.append("task_2")          # enqueue at rear  -> O(1)
front_item = q[0]           # peek at front    -> O(1)
item = q.popleft()          # dequeue at front -> O(1)
```

### B. Queue Using Two Stacks in Amortized $O(1)$ Time (LeetCode 232)
```python
class TwoStackQueue:
    def __init__(self) -> None:
        self._in: list[int] = []
        self._out: list[int] = []

    def enqueue(self, x: int) -> None:
        self._in.append(x)

    def dequeue(self) -> int:
        if not self._out:
            while self._in:
                self._out.append(self._in.pop())
        return self._out.pop()
```

---

## 4. Explanation (Step-by-Step)

### 1. Why a Singly Linked Queue Needs Both `_head` and `_tail` Pointers
In a singly linked list `head -> ... -> tail -> None`:
- Removing at `head` (`_head = _head.next`) takes $O(1)$ time.
- Appending at `tail` (`_tail.next = new_node; _tail = new_node`) also takes $O(1)$ time.
- **Crucial Edge Case:** When the last remaining node is dequeued (`_head` becomes `None`), you **must** also set `_tail = None` so `_tail` does not retain a dangling reference to the removed node!

### 2. Amortized $O(1)$ Proof for `TwoStackQueue` (Banker's / Accounting Method)
Why is `TwoStackQueue.dequeue()` amortized $O(1)$ even though the `while self._in:` transfer loop takes $O(k)$ time when `_out` is empty?
- Track the lifecycle of any single element $x$:
  1. Pushed onto `_in` **once** ($1$ operation).
  2. Popped from `_in` and pushed onto `_out` **once** ($2$ operations).
  3. Popped from `_out` **once** ($1$ operation).
- Across $n$ total `enqueue` and `dequeue` calls, every element participates in **at most $4$ stack operations**, so the total work is bounded by $4n = O(n)$, which averages to **$O(1)$ amortized time per operation**!

---

## 5. Minimum 3 Examples

### Example 1: Singly Linked List FIFO Queue vs `collections.deque` vs `list.pop(0)`
File: [`example_01_linked_list_queue_vs_deque.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/F_Stacks_and_Queues/02_Queue_Implementation/example_01_linked_list_queue_vs_deque.py)

```python
class LinkedQueue(Generic[T]):
    """
    FIFO Queue backed by a singly linked list with both `_head` (front) and
    `_tail` (rear) pointers for strict O(1) worst-case enqueue and dequeue.
    """

    def __init__(self) -> None:
        self._head: Optional[_QNode[T]] = None
        self._tail: Optional[_QNode[T]] = None
        self._size: int = 0

    def enqueue(self, item: T) -> None:
        new_node = _QNode(item)
        if self._tail is None:
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1

    def dequeue(self) -> T:
        if self._head is None:
            raise IndexError("dequeue from an empty LinkedQueue")
        front_val = self._head.val
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return front_val
```

---

### Example 2: Queue Using Two Stacks (LeetCode 232) & Stack Using One Queue (LeetCode 225)
File: [`example_02_queue_using_two_stacks_and_stack_using_queues.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/F_Stacks_and_Queues/02_Queue_Implementation/example_02_queue_using_two_stacks_and_stack_using_queues.py)

```python
class TwoStackQueue(Generic[T]):
    """FIFO Queue implemented using two LIFO stacks in amortized O(1) time."""

    def __init__(self) -> None:
        self._in_stack: List[T] = []
        self._out_stack: List[T] = []
        self.total_transfers: int = 0

    def _transfer_if_needed(self) -> None:
        if not self._out_stack:
            while self._in_stack:
                self._out_stack.append(self._in_stack.pop())
                self.total_transfers += 1

    def enqueue(self, item: T) -> None:
        self._in_stack.append(item)

    def dequeue(self) -> T:
        self._transfer_if_needed()
        if not self._out_stack:
            raise IndexError("dequeue from empty TwoStackQueue")
        return self._out_stack.pop()
```

---

### Example 3: Binary Number Generator ($1 \dots N$) & Sliding Time-Window Rate Limiter
File: [`example_03_binary_number_generator_and_rate_limiter.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/F_Stacks_and_Queues/02_Queue_Implementation/example_03_binary_number_generator_and_rate_limiter.py)

```python
class SlidingWindowRateLimiter:
    """
    Allows at most `max_requests` within any rolling `window_sec` time window
    using a FIFO queue of accepted request timestamps.
    """

    def __init__(self, max_requests: int, window_sec: int) -> None:
        self.max_requests = max_requests
        self.window_sec = window_sec
        self._timestamps: Deque[int] = deque()

    def allow_request(self, timestamp_sec: int) -> Tuple[bool, int]:
        cutoff = timestamp_sec - self.window_sec
        while self._timestamps and self._timestamps[0] <= cutoff:
            self._timestamps.popleft()

        if len(self._timestamps) < self.max_requests:
            self._timestamps.append(timestamp_sec)
            return True, len(self._timestamps)
        return False, len(self._timestamps)
```

---

## 6. Output

### Output — Example 1 (`example_01_linked_list_queue_vs_deque.py`)
```text
========================================================================
1. LinkedQueue (Head + Tail Pointers) vs `collections.deque` FIFO Check
========================================================================
After enqueueing 4 jobs: ['Job_A_Upload', 'Job_B_Transcode', 'Job_C_Thumbnail', 'Job_D_Notify']
Front of queue (`peek()`): Job_A_Upload == Job_A_Upload

Processing FIFO queue in arrival order:
  Dequeued: Job_A_Upload       | Remaining in queue: 3
  Dequeued: Job_B_Transcode    | Remaining in queue: 2
  Dequeued: Job_C_Thumbnail    | Remaining in queue: 1
  Dequeued: Job_D_Notify       | Remaining in queue: 0
After draining: is_empty=True, _head=None, _tail=None

========================================================================
2. Why `list.pop(0)` is O(n^2) for Draining n Elements vs O(n) Queue
========================================================================
  n =   1000 items -> list.pop(0) element shifts =    499,500 | LinkedQueue/deque ops =  1,000
  n =  10000 items -> list.pop(0) element shifts = 49,995,000 | LinkedQueue/deque ops = 10,000
```

### Output — Example 2 (`example_02_queue_using_two_stacks_and_stack_using_queues.py`)
```text
========================================================================
1. TwoStackQueue (LeetCode 232) — Amortized O(1) FIFO Verification
========================================================================
After enqueue(10, 20, 30): in_stack=[10, 20, 30], out_stack=[]
First dequeue() -> 10 (triggered lazy transfer!)
State now        : in_stack=[], out_stack=[30, 20]
After enqueue(40, 50): in_stack=[40, 50], out_stack=[30, 20]
Drained remaining FIFO order: [20, 30, 40, 50]
Total in->out transfers for 5 elements: 5 (exactly 1 per element!)

========================================================================
2. OneQueueStack (LeetCode 225) — LIFO Behaviour from a Single Queue
========================================================================
Pushed ['A', 'B', 'C', 'D'] -> Popped LIFO order: ['D', 'C', 'B', 'A']
```

### Output — Example 3 (`example_03_binary_number_generator_and_rate_limiter.py`)
```text
========================================================================
1. Generate Binary Numbers 1..12 via FIFO Queue BFS
========================================================================
  Decimal  1 -> Binary    1
  Decimal  2 -> Binary   10
  Decimal  3 -> Binary   11
  Decimal  4 -> Binary  100
  Decimal  5 -> Binary  101
  Decimal  6 -> Binary  110
  Decimal  7 -> Binary  111
  Decimal  8 -> Binary 1000
  Decimal  9 -> Binary 1001
  Decimal 10 -> Binary 1010
  Decimal 11 -> Binary 1011
  Decimal 12 -> Binary 1100

========================================================================
2. Sliding Time-Window API Rate Limiter (Max 3 reqs / 10 seconds)
========================================================================
  t =  1s -> ALLOWED                           | Active window timestamps: [1]
  t =  2s -> ALLOWED                           | Active window timestamps: [1, 2]
  t =  4s -> ALLOWED                           | Active window timestamps: [1, 2, 4]
  t =  8s -> BLOCKED (429 Too Many Requests)   | Active window timestamps: [1, 2, 4]
  t = 11s -> ALLOWED                           | Active window timestamps: [2, 4, 11]
  t = 12s -> ALLOWED                           | Active window timestamps: [4, 11, 12]
  t = 13s -> BLOCKED (429 Too Many Requests)   | Active window timestamps: [4, 11, 12]
```

---

## 7. Code Explanation

1. **Lazy Transfer in `TwoStackQueue._transfer_if_needed()`:**
   We **only** pour `_in_stack` into `_out_stack` when `_out_stack` is **completely empty**. Pouring while `_out_stack` still has older elements would place newer elements on top of older ones, violating FIFO order!
2. **BFS Binary Generation (`generate_binary_1_to_n`):**
   Appending `"0"` to binary string $s$ corresponds to $2x$ (left bit-shift), and appending `"1"` corresponds to $2x + 1$. Because a FIFO queue visits the binary tree level by level, strings are generated in exact ascending numeric order $1, 2, 3, \dots, n$.

---

## 8. Common Mistakes

1. **Using `list.pop(0)` in BFS or Sliding Window Problems:**
   On a graph with $100{,}000$ vertices, `queue.pop(0)` turns an $O(V + E)$ BFS into an $O(V^2)$ Time-Limit-Exceeded failure. Always import `from collections import deque` and call `queue.popleft()`.
2. **Transferring `_in_stack` to `_out_stack` on Every `dequeue()` Even When `_out_stack` is Non-Empty:**
   This both corrupts FIFO ordering and degrades `dequeue()` to $O(n)$ per call.
3. **Forgetting to Reset `self._tail = None` When `LinkedQueue` Becomes Empty:**
   If `dequeue()` removes the sole node so `self._head` becomes `None`, leaving `self._tail` pointing to that removed node causes the next `enqueue()` to check `if self._tail is None:` (which is `False`!) and attach the new node to a dead, unreachable node instead of setting `self._head`!

---

## 9. Practice Questions

1. **Easy — Number of Recent Calls (LeetCode 933):**
   Implement the `RecentCounter` class with `ping(t: int) -> int` that returns the number of requests that have happened in the inclusive time range $[t - 3000, t]$ using a FIFO queue.
2. **Medium — Time Needed to Buy Tickets (LeetCode 2073) & Dota2 Senate (LeetCode 649):**
   Simulate two competing factions (`Radiant` and `Dire`) voting in rounds where each senator bans the next opposing senator using two index queues `rad_q` and `dire_q`.
3. **Hard — Reveal Cards In Increasing Order (LeetCode 950):**
   Given an array `deck`, simulate the index-dealing process (reveal top, move next top to bottom) using a queue of indices `0..n-1` to determine the initial deck ordering that reveals cards in sorted ascending order.

---

## 10. Interview Questions

### Q1: When should you use `queue.Queue` instead of `collections.deque` in Python?
**Answer:**
- Use `collections.deque` for **all single-threaded algorithmic/DSA code** (`append` and `popleft` are lock-free C operations with minimal overhead).
- Use `queue.Queue` for **multi-threaded producer-consumer synchronization**, where threads need blocking `.get(timeout=...)`, `.put()`, mutex locks, and `.task_done()` / `.join()` signaling.

### Q2: In `OneQueueStack` (LeetCode 225), can we make `push()` $O(1)$ and `pop()` $O(n)$ instead of `push()` $O(n)$ and `pop()` $O(1)$?
**Answer:** Yes! If `push(x)` simply enqueues `x` in $O(1)$ time, then `pop()` can rotate the first $n - 1$ elements (`q.append(q.popleft())`) in $O(n)$ time and then `popleft()` the $n$-th element. Making `push` $O(n)$ is usually preferred because then both `pop()` and `top()` are $O(1)$.

### Q3: How would you scale `SlidingWindowRateLimiter` if $1{,}000{,}000$ requests arrive within the same second?
**Answer:** Storing $1{,}000{,}000$ individual timestamps in the queue wastes memory when many requests share the same timestamp. Instead, coalesce requests arriving in the same second (or millisecond bucket) into a single `(timestamp_sec, count)` pair at the rear of the queue and maintain a running `active_count` integer!

