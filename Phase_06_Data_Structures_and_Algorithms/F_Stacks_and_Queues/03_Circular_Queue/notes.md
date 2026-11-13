# Circular Queue (Fixed Ring Buffer, Dynamic Unwrap Resizing & Overwriting Telemetry Buffers)

---

## 1. Introduction

A **Circular Queue** (also known as a **Ring Buffer** or **Circular Buffer**) is a FIFO queue backed by a contiguous array of capacity $k$ whose `front` and `rear` indices **wrap around** from index $k - 1$ back to index $0$ using modulo arithmetic (`% k`):

$$\text{Write Index} = (\text{front} + \text{size}) \bmod k, \qquad \text{New Front} = (\text{front} + 1) \bmod k$$

Why is a Circular Queue essential when using an array to implement a Queue?
- In a naive flat-array queue where `front` increments on each `dequeue()` without wrapping, slots $0 \dots \text{front} - 1$ become permanently unusable ("false overflow"), even when the queue holds only 1 item!
- By wrapping around modulo $k$, a Circular Queue achieves **strict $O(1)$ worst-case `enQueue` and `deQueue`**, **100% slot utilization**, and **zero heap allocations** after initialization.

---

## 2. Why is it used?

1. **OS Kernel Pipes, Network Socket Ring Buffers & Audio DSP (`io_uring`, NIC RX/TX rings):** High-throughput hardware/kernel channels preallocate a fixed power-of-two ring buffer in contiguous RAM so producers and consumers exchange packets in $O(1)$ time without triggering garbage collection or `malloc()`.
2. **Dynamic Deque/Queue Implementations:** Industrial dynamic array queues (such as Rust's `VecDeque` or Java's `ArrayDeque`) are dynamically resizing circular buffers that double capacity and unwrap elements when full.
3. **Flight Recorders & Telemetry Ring Logs:** Overwriting ring buffers continuously record the latest $k$ sensor measurements, automatically overwriting the oldest sample when full.
4. **$O(1)$ Sliding Window Stream Aggregators:** Computing a running **Moving Average from a Data Stream** (LeetCode 346) in $O(1)$ time per element by overwriting the slot at `head_idx = (head_idx + 1) % k`.

---

## 3. Syntax

### Fixed-Capacity Circular Queue Using `front` and `size` (LeetCode 622)
```python
class MyCircularQueue:
    def __init__(self, k: int) -> None:
        self._cap = k
        self._buf: list[int | None] = [None] * k
        self._front = 0
        self._size = 0

    def enQueue(self, value: int) -> bool:
        if self._size == self._cap:
            return False
        write_idx = (self._front + self._size) % self._cap
        self._buf[write_idx] = value
        self._size += 1
        return True

    def deQueue(self) -> bool:
        if self._size == 0:
            return False
        self._buf[self._front] = None
        self._front = (self._front + 1) % self._cap
        self._size -= 1
        return True
```

---

## 4. Explanation (Step-by-Step)

### 1. Why Storing `front` and `size` Is Cleaner Than Storing `front` and `rear`
If you only store `front` and `rear` without a `size` counter, both an **empty** queue and a **completely full** queue satisfy the exact same pointer equation (`(rear + 1) % k == front` or `front == rear`)!
To disambiguate full vs empty, engineers use one of three techniques:
1. **Explicit `self._size` counter (Recommended):** Empty is `self._size == 0`; Full is `self._size == k`; Rear index is `(self._front + self._size - 1) % k`. All $k$ slots are usable.
2. **Sacrificing 1 Sentinel Slot:** Allocate $k + 1$ slots; Empty is `front == rear`; Full is `(rear + 1) % (k + 1) == front`.
3. **Monotonically Increasing Unsigned 64-Bit `read_count` and `write_count` (Lock-Free Ring Buffers):** Index into the array via `write_count % k`; Empty is `write_count == read_count`; Full is `write_count - read_count == k`.

### 2. Why Dynamic Resizing Must **Unwrap** the Ring
Suppose a capacity-4 circular buffer is wrapped around: `_buf = [50, 60, 30, 40]` with `_front = 2` (logical order `[30, 40, 50, 60]`).
If we simply appended `[None, None, None, None]` to the end of `_buf` (`[50, 60, 30, 40, None, None, None, None]`), then `(front + i) % 8` for $i = 2$ would read index `(2 + 2) % 8 = 4` (`None`!) instead of index `0` (`50`)!
Therefore, `_resize(new_cap)` must **unwrap** the elements by copying `_buf[(_front + i) % old_cap]` into `new_buf[i]` for $i \in [0, \text{size} - 1]$ and resetting `_front = 0`.

---

## 5. Minimum 3 Examples

### Example 1: Fixed-Capacity Circular Queue / Ring Buffer (LeetCode 622)
File: [`example_01_fixed_array_circular_queue.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/F_Stacks_and_Queues/03_Circular_Queue/example_01_fixed_array_circular_queue.py)

```python
class MyCircularQueue(Generic[T]):
    """
    Fixed-capacity Ring Buffer implementation (LeetCode 622) using `front` index
    and explicit `size` counter to distinguish full (`size == k`) from empty (`size == 0`).
    """

    def __init__(self, k: int) -> None:
        if k <= 0:
            raise ValueError("Capacity k must be positive")
        self._capacity: int = k
        self._buffer: List[Optional[T]] = [None] * k
        self._front: int = 0
        self._size: int = 0

    def enQueue(self, value: T) -> bool:
        if self.isFull():
            return False
        write_idx = (self._front + self._size) % self._capacity
        self._buffer[write_idx] = value
        self._size += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self._buffer[self._front] = None
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return True

    def Front(self) -> Optional[T]:
        return None if self.isEmpty() else self._buffer[self._front]

    def Rear(self) -> Optional[T]:
        if self.isEmpty():
            return None
        rear_idx = (self._front + self._size - 1) % self._capacity
        return self._buffer[rear_idx]
```

---

### Example 2: Dynamically Resizing Circular Array Queue (Doubling & Halving with Unwrap)
File: [`example_02_dynamic_resizing_circular_buffer.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/F_Stacks_and_Queues/03_Circular_Queue/example_02_dynamic_resizing_circular_buffer.py)

```python
class DynamicCircularQueue(Generic[T]):
    """Amortized O(1) dynamically resizing circular array queue."""

    MIN_CAPACITY = 4

    def __init__(self, initial_capacity: int = 4) -> None:
        cap = max(self.MIN_CAPACITY, initial_capacity)
        self._buffer: List[Optional[T]] = [None] * cap
        self._front: int = 0
        self._size: int = 0

    def _resize(self, new_capacity: int) -> None:
        """Unwraps the circular queue into a fresh contiguous buffer of `new_capacity`."""
        new_buf: List[Optional[T]] = [None] * new_capacity
        old_cap = len(self._buffer)
        for i in range(self._size):
            new_buf[i] = self._buffer[(self._front + i) % old_cap]
        self._buffer = new_buf
        self._front = 0
```

---

### Example 3: Overwriting Telemetry Ring Buffer & $O(1)$ Moving Average from Data Stream
File: [`example_03_overwriting_ring_buffer_and_moving_average.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/F_Stacks_and_Queues/03_Circular_Queue/example_03_overwriting_ring_buffer_and_moving_average.py)

```python
class MovingAverageStream:
    """
    Computes the moving average of the last `window_size` numbers in strict O(1) time
    per `.next(val)` call using a circular array of length `window_size` (LeetCode 346).
    """

    def __init__(self, window_size: int) -> None:
        self._window_size = window_size
        self._ring: List[float] = [0.0] * window_size
        self._head_idx: int = 0
        self._count: int = 0
        self._window_sum: float = 0.0

    def next(self, val: float) -> float:
        evicted = self._ring[self._head_idx] if self._count == self._window_size else 0.0
        self._ring[self._head_idx] = val
        self._head_idx = (self._head_idx + 1) % self._window_size
        if self._count < self._window_size:
            self._count += 1
        self._window_sum += val - evicted
        return self._window_sum / self._count
```

---

## 6. Output

### Output — Example 1 (`example_01_fixed_array_circular_queue.py`)
```text
========================================================================
Fixed-Capacity Circular Queue / Ring Buffer (Capacity k = 4)
========================================================================
enQueue(10) -> 1     | buffer=[10, None, None, None], front=0, size=1/4, Front()=10, Rear()=10
enQueue(20) -> 1     | buffer=[10, 20, None, None], front=0, size=2/4, Front()=10, Rear()=20
enQueue(30) -> 1     | buffer=[10, 20, 30, None], front=0, size=3/4, Front()=10, Rear()=30
enQueue(40) -> 1     | buffer=[10, 20, 30, 40], front=0, size=4/4, Front()=10, Rear()=40
enQueue(50) on full queue -> False

Dequeueing 2 items to free slots 0 and 1:
After 2 deQueues  | buffer=[None, None, 30, 40], front=2, size=2/4, Front()=30, Rear()=40

Wrapping around the end of the array (enQueue 50 and 60 into slots 0 & 1):
After enQueue(50) | buffer=[50, None, 30, 40], front=2, size=3/4, Front()=30, Rear()=50
After enQueue(60) | buffer=[50, 60, 30, 40], front=2, size=4/4, Front()=30, Rear()=60
```

### Output — Example 2 (`example_02_dynamic_resizing_circular_buffer.py`)
```text
========================================================================
Dynamically Resizing Circular Buffer (Wrap + Unwrap on Double/Shrink)
========================================================================
Wrapped Full State (size=4/4):
  Raw Buffer  : [50, 60, 30, 40] (front=2)
  Logical FIFO: [30, 40, 50, 60]

Triggering 2x Capacity Doubling via enqueue(70) & enqueue(80):
  Raw Buffer  : [30, 40, 50, 60, 70, 80, None, None] (front=0, size=6/8)
  Logical FIFO: [30, 40, 50, 60, 70, 80]

Draining 4 items to trigger quarter-full capacity halving:
  Raw Buffer  : [70, 80, None, None] (front=0, size=2/4)
  Logical FIFO: [70, 80]
```

### Output — Example 3 (`example_03_overwriting_ring_buffer_and_moving_average.py`)
```text
========================================================================
1. Overwriting Telemetry Ring Buffer (Capacity k = 4)
========================================================================
  push(E1_Boot   ) -> Evicted: None     | Chronological Ring: ['E1_Boot']
  push(E2_Auth   ) -> Evicted: None     | Chronological Ring: ['E1_Boot', 'E2_Auth']
  push(E3_Query  ) -> Evicted: None     | Chronological Ring: ['E1_Boot', 'E2_Auth', 'E3_Query']
  push(E4_Cache  ) -> Evicted: None     | Chronological Ring: ['E1_Boot', 'E2_Auth', 'E3_Query', 'E4_Cache']
  push(E5_Alert  ) -> Evicted: E1_Boot  | Chronological Ring: ['E2_Auth', 'E3_Query', 'E4_Cache', 'E5_Alert']
  push(E6_Recover) -> Evicted: E2_Auth  | Chronological Ring: ['E3_Query', 'E4_Cache', 'E5_Alert', 'E6_Recover']

========================================================================
2. O(1) Moving Average from Data Stream via Circular Array (Window = 3)
========================================================================
  next( 1) -> window_sum =  1.0, moving_avg = 1.00
  next(10) -> window_sum = 11.0, moving_avg = 5.50
  next( 3) -> window_sum = 14.0, moving_avg = 4.67
  next( 5) -> window_sum = 18.0, moving_avg = 6.00
  next( 8) -> window_sum = 16.0, moving_avg = 5.33
  next(12) -> window_sum = 25.0, moving_avg = 8.33
```

---

## 7. Code Explanation

1. **Why `deQueue` Sets `self._buffer[self._front] = None`:**
   In garbage-collected languages like Python and Java, simply advancing `self._front = (self._front + 1) % self._capacity` without clearing the old slot leaves a hidden reference ("loitering object") inside `self._buffer`, preventing the garbage collector from freeing that object until the slot is overwritten later!
2. **Why `DynamicCircularQueue` Shrinks at `size == cap // 4` Instead of `size == cap // 2`:**
   If a buffer doubled at full (`size == cap`) and immediately halved at half-full (`size == cap // 2`), alternating `enqueue()` and `dequeue()` at the boundary would trigger an $O(n)$ resize on every single call! Shrinking only at **one-quarter full (`cap // 4`)** guarantees at least $O(n)$ operations between consecutive resizes.

---

## 8. Common Mistakes

1. **Computing `Rear()` as `(self._front + self._size) % self._capacity`:**
   `(self._front + self._size) % self._capacity` is the **next empty write slot**, not the last occupied element! The last occupied element is at `(self._front + self._size - 1) % self._capacity`.
2. **Forgetting to Unwrap Elements When Doubling Capacity:**
   Extending a wrapped circular buffer in-place breaks the modulo invariant `(front + i) % new_capacity`.
3. **Not Checking `isEmpty()` in `Front()` / `Rear()`:**
   When `self._size == 0`, `(self._front + self._size - 1) % k` wraps to `(self._front - 1) % k`, which would return whatever stale value or `None` sits there unless `isEmpty()` is checked first.

---

## 9. Practice Questions

1. **Easy — Design Circular Queue With Sentinel Slot (No `size` Variable):**
   Implement `MyCircularQueue(k)` using an internal array of length `k + 1` and only two integer fields `self._front` and `self._rear` (no `self._size` field).
2. **Medium — Product of the Last $K$ Numbers in a Bounded Window:**
   Modify `MovingAverageStream` to maintain the running product of the last $k$ integers (handling zeros cleanly by tracking the index of the most recent zero).
3. **Hard — Lock-Free Single-Producer Single-Consumer (SPSC) Ring Buffer:**
   Using monotonically increasing `read_pos` and `write_pos` counters and a power-of-two capacity $k = 2^m$, replace `% k` with bitwise masking `& (k - 1)` and implement batch `write_slice` and `read_slice`.

---

## 10. Interview Questions

### Q1: Why do high-performance C/Rust ring buffers (like Linux `kfifo`) require the capacity $k$ to be a power of 2 ($2^m$)?
**Answer:** Integer division/modulo (`idx % k`) takes ~15–20 CPU clock cycles, whereas when $k = 2^m$, `idx % k` is identical to the single-cycle bitwise AND instruction **`idx & (k - 1)`**!

### Q2: How can a Single-Producer Single-Consumer (SPSC) circular queue operate across two threads without a mutex lock?
**Answer:** The producer thread is the **only** thread that modifies `write_pos`, and the consumer thread is the **only** thread that modifies `read_pos`. Using atomic acquire/release loads and stores on `write_pos` and `read_pos`, the two threads never contend on the same variable.

### Q3: What is "loitering" in array-backed queues/stacks, and how do you prevent it?
**Answer:** Loitering occurs when an element is logically removed by moving an index (`front` or `top`), but the underlying array slot still holds a reference to the object, preventing garbage collection. Explicitly assigning `self._buffer[self._front] = None` upon `deQueue()` prevents loitering.

