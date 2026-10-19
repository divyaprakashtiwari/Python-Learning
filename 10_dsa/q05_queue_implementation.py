"""
Topic: Data Structures and Algorithms (DSA) - Queue Implementation
------------------------------------------------------------------
Questions Covered:
1. Circular Queue (Ring Buffer): Fixed-size array with modulo pointer indexing.
2. Linked List Queue: O(1) head/tail pointer queue with dynamic allocation.
3. Queue via Two Stacks: Amortized O(1) enqueue/dequeue using in/out stack transfer.
4. Double-Ended Queue (Deque): Doubly linked list supporting bidirectional operations.
5. Sliding Window Maximum (Monotonic Deque): Linear O(n) window maximum calculation.
6. Binary Min-Heap Priority Queue: Array-based heap with sift_up and sift_down from scratch.
7. Moving Average from Data Stream: O(1) sliding window average with bounded circular buffer.
8. Breadth-First Search (BFS) Level-Order Queue: Level-by-level tree/graph layer grouping.
9. First Non-Repeating Character in Stream: Real-time candidate queue with frequency index.
10. Architectural System: Multi-Tenant Fair-Share Task Scheduler with Deficit Round-Robin.
"""

from typing import List, Tuple, Optional, Any, Dict


# ==============================================================================
# Question 1: Circular Queue (Ring Buffer)
# ==============================================================================
class CircularQueue:
    """
    Fixed-capacity circular queue implemented with a preallocated array and modulo arithmetic.
    """
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self._capacity = capacity
        self._buffer: List[Optional[Any]] = [None] * capacity
        self._head = 0
        self._tail = 0
        self._size = 0

    def enqueue(self, val: Any) -> bool:
        if self._size == self._capacity:
            return False  # Queue is full
        self._buffer[self._tail] = val
        self._tail = (self._tail + 1) % self._capacity
        self._size += 1
        return True

    def dequeue(self) -> Optional[Any]:
        if self._size == 0:
            return None  # Queue is empty
        val = self._buffer[self._head]
        self._buffer[self._head] = None
        self._head = (self._head + 1) % self._capacity
        self._size -= 1
        return val

    def front(self) -> Optional[Any]:
        return self._buffer[self._head] if self._size > 0 else None

    def rear(self) -> Optional[Any]:
        if self._size == 0:
            return None
        last_idx = (self._tail - 1 + self._capacity) % self._capacity
        return self._buffer[last_idx]

    def is_empty(self) -> bool:
        return self._size == 0

    def is_full(self) -> bool:
        return self._size == self._capacity

    def __len__(self) -> int:
        return self._size


def test_q1_circular_queue():
    cq = CircularQueue(3)
    assert cq.is_empty() is True
    assert cq.enqueue(1) is True
    assert cq.enqueue(2) is True
    assert cq.enqueue(3) is True
    assert cq.is_full() is True
    assert cq.enqueue(4) is False  # Full

    assert cq.front() == 1
    assert cq.rear() == 3
    assert cq.dequeue() == 1
    assert cq.is_full() is False

    # Wraparound insertion
    assert cq.enqueue(4) is True
    assert cq.rear() == 4
    assert cq.dequeue() == 2
    assert cq.dequeue() == 3
    assert cq.dequeue() == 4
    assert cq.is_empty() is True
    print("=== Q1: Circular Queue (Ring Buffer) Verified ===")


# ==============================================================================
# Question 2: Linked List Queue (O(1) Head & Tail)
# ==============================================================================
class QueueNode:
    def __init__(self, val: Any):
        self.val = val
        self.next: Optional["QueueNode"] = None


class LinkedQueue:
    """Queue implemented using singly linked list with head and tail pointers."""
    def __init__(self):
        self._head: Optional[QueueNode] = None
        self._tail: Optional[QueueNode] = None
        self._size = 0

    def enqueue(self, val: Any) -> None:
        node = QueueNode(val)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def dequeue(self) -> Any:
        if self._head is None:
            raise IndexError("dequeue from empty queue")
        val = self._head.val
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return val

    def peek(self) -> Any:
        if self._head is None:
            raise IndexError("peek from empty queue")
        return self._head.val

    def is_empty(self) -> bool:
        return self._size == 0

    def __len__(self) -> int:
        return self._size


def test_q2_linked_queue():
    lq = LinkedQueue()
    lq.enqueue("first")
    lq.enqueue("second")
    assert lq.peek() == "first"
    assert len(lq) == 2
    assert lq.dequeue() == "first"
    assert lq.dequeue() == "second"
    assert lq.is_empty() is True

    try:
        lq.dequeue()
        assert False, "Should raise IndexError"
    except IndexError:
        pass
    print("=== Q2: Linked List Queue Verified ===")


# ==============================================================================
# Question 3: Queue Implemented via Two Stacks
# ==============================================================================
class MyQueueTwoStacks:
    """
    Queue implemented using two stacks (in_stack, out_stack).
    Amortized O(1) operations.
    """
    def __init__(self):
        self._in_stack: List[Any] = []
        self._out_stack: List[Any] = []

    def push(self, x: Any) -> None:
        self._in_stack.append(x)

    def _shift_stacks(self) -> None:
        if not self._out_stack:
            while self._in_stack:
                self._out_stack.append(self._in_stack.pop())

    def pop(self) -> Any:
        self._shift_stacks()
        if not self._out_stack:
            raise IndexError("pop from empty queue")
        return self._out_stack.pop()

    def peek(self) -> Any:
        self._shift_stacks()
        if not self._out_stack:
            raise IndexError("peek from empty queue")
        return self._out_stack[-1]

    def empty(self) -> bool:
        return not self._in_stack and not self._out_stack


def test_q3_queue_two_stacks():
    q = MyQueueTwoStacks()
    q.push(1)
    q.push(2)
    assert q.peek() == 1
    assert q.pop() == 1
    assert q.empty() is False
    q.push(3)
    assert q.pop() == 2
    assert q.pop() == 3
    assert q.empty() is True
    print("=== Q3: Queue via Two Stacks Verified ===")


# ==============================================================================
# Question 4: Double-Ended Queue (Deque) via Doubly Linked List
# ==============================================================================
class DequeNode:
    def __init__(self, val: Any):
        self.val = val
        self.prev: Optional["DequeNode"] = None
        self.next: Optional["DequeNode"] = None


class DoublyLinkedDeque:
    """Deque supporting O(1) insertions and deletions at both ends."""
    def __init__(self):
        self._head: Optional[DequeNode] = None
        self._tail: Optional[DequeNode] = None
        self._size = 0

    def append_left(self, val: Any) -> None:
        node = DequeNode(val)
        if self._head is None:
            self._head = self._tail = node
        else:
            node.next = self._head
            self._head.prev = node
            self._head = node
        self._size += 1

    def append_right(self, val: Any) -> None:
        node = DequeNode(val)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            node.prev = self._tail
            self._tail = node
        self._size += 1

    def pop_left(self) -> Any:
        if self._head is None:
            raise IndexError("pop from empty deque")
        val = self._head.val
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        else:
            self._head.prev = None
        self._size -= 1
        return val

    def pop_right(self) -> Any:
        if self._tail is None:
            raise IndexError("pop from empty deque")
        val = self._tail.val
        self._tail = self._tail.prev
        if self._tail is None:
            self._head = None
        else:
            self._tail.next = None
        self._size -= 1
        return val

    def peek_left(self) -> Any:
        if self._head is None:
            raise IndexError("peek from empty deque")
        return self._head.val

    def peek_right(self) -> Any:
        if self._tail is None:
            raise IndexError("peek from empty deque")
        return self._tail.val

    def __len__(self) -> int:
        return self._size


def test_q4_doubly_linked_deque():
    dq = DoublyLinkedDeque()
    dq.append_right(10)
    dq.append_right(20)
    dq.append_left(5)  # 5, 10, 20

    assert dq.peek_left() == 5
    assert dq.peek_right() == 20
    assert len(dq) == 3

    assert dq.pop_left() == 5
    assert dq.pop_right() == 20
    assert dq.pop_left() == 10
    assert len(dq) == 0
    print("=== Q4: Double-Ended Queue (Deque) Verified ===")


# ==============================================================================
# Question 5: Sliding Window Maximum (Monotonic Deque)
# ==============================================================================
def max_sliding_window(nums: List[int], k: int) -> List[int]:
    """
    Finds maximum value in each sliding window of size k moving across nums.
    Runs in linear O(n) time using a monotonic decreasing deque of indices.
    """
    if not nums or k <= 0:
        return []

    dq: List[int] = []  # Stores indices of elements in descending order of value
    result: List[int] = []

    for i in range(len(nums)):
        # 1. Remove indices outside current sliding window [i - k + 1, i]
        if dq and dq[0] < i - k + 1:
            dq.pop(0)

        # 2. Maintain monotonic decreasing order (remove smaller elements from back)
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()

        dq.append(i)

        # 3. Append maximum (at index dq[0]) once window of size k is formed
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result


def test_q5_sliding_window_maximum():
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    # Windows:
    # [1, 3, -1] -> 3
    # [3, -1, -3] -> 3
    # [-1, -3, 5] -> 5
    # [-3, 5, 3] -> 5
    # [5, 3, 6] -> 6
    # [3, 6, 7] -> 7
    res = max_sliding_window(nums, k)
    assert res == [3, 3, 5, 5, 6, 7]
    print("=== Q5: Sliding Window Maximum (Monotonic Deque) Verified ===")


# ==============================================================================
# Question 6: Binary Min-Heap Priority Queue from Scratch
# ==============================================================================
class BinaryMinHeap:
    """
    Array-based binary min-heap supporting insert, extract_min, and peek in O(log n).
    Children of index i are at 2*i + 1 and 2*i + 2. Parent is at (i - 1) // 2.
    """
    def __init__(self):
        self._heap: List[int] = []

    def insert(self, val: int) -> None:
        self._heap.append(val)
        self._sift_up(len(self._heap) - 1)

    def extract_min(self) -> int:
        if not self._heap:
            raise IndexError("extract_min from empty heap")
        if len(self._heap) == 1:
            return self._heap.pop()

        min_val = self._heap[0]
        self._heap[0] = self._heap.pop()  # Move last element to root
        self._sift_down(0)
        return min_val

    def peek(self) -> int:
        if not self._heap:
            raise IndexError("peek from empty heap")
        return self._heap[0]

    def _sift_up(self, idx: int) -> None:
        parent = (idx - 1) // 2
        while idx > 0 and self._heap[idx] < self._heap[parent]:
            self._heap[idx], self._heap[parent] = self._heap[parent], self._heap[idx]
            idx = parent
            parent = (idx - 1) // 2

    def _sift_down(self, idx: int) -> None:
        n = len(self._heap)
        while True:
            smallest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2

            if left < n and self._heap[left] < self._heap[smallest]:
                smallest = left
            if right < n and self._heap[right] < self._heap[smallest]:
                smallest = right

            if smallest != idx:
                self._heap[idx], self._heap[smallest] = self._heap[smallest], self._heap[idx]
                idx = smallest
            else:
                break

    def __len__(self) -> int:
        return len(self._heap)


def test_q6_binary_min_heap():
    heap = BinaryMinHeap()
    for num in [15, 10, 20, 17, 8, 30]:
        heap.insert(num)

    extracted = [heap.extract_min() for _ in range(len(heap))]
    assert extracted == [8, 10, 15, 17, 20, 30]
    print("=== Q6: Binary Min-Heap Priority Queue Verified ===")


# ==============================================================================
# Question 7: Moving Average from Data Stream
# ==============================================================================
class MovingAverageStream:
    """
    Computes moving average of the last 'size' numbers seen in a stream in O(1) time.
    """
    def __init__(self, size: int):
        self.size = size
        self.queue: List[float] = []
        self.running_sum = 0.0

    def next(self, val: float) -> float:
        self.queue.append(val)
        self.running_sum += val
        if len(self.queue) > self.size:
            evicted = self.queue.pop(0)
            self.running_sum -= evicted
        return self.running_sum / len(self.queue)


def test_q7_moving_average():
    ma = MovingAverageStream(3)
    assert ma.next(1.0) == 1.0  # 1 / 1
    assert ma.next(10.0) == 5.5  # (1 + 10) / 2
    assert abs(ma.next(3.0) - 4.666666) < 1e-5  # (1 + 10 + 3) / 3 = 14 / 3
    assert ma.next(5.0) == 6.0  # (10 + 3 + 5) / 3 = 18 / 3
    print("=== Q7: Moving Average from Data Stream Verified ===")


# ==============================================================================
# Question 8: BFS Level-Order Queue Traversal
# ==============================================================================
class TreeNode:
    def __init__(self, val: int, left: Optional["TreeNode"] = None, right: Optional["TreeNode"] = None):
        self.val = val
        self.left = left
        self.right = right


def level_order_traversal(root: Optional[TreeNode]) -> List[List[int]]:
    """
    Performs level-order BFS traversal using a FIFO queue.
    Returns list of node values grouped by level.
    """
    if root is None:
        return []

    result: List[List[int]] = []
    queue: List[TreeNode] = [root]

    while queue:
        level_size = len(queue)
        current_level: List[int] = []

        for _ in range(level_size):
            node = queue.pop(0)
            current_level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(current_level)

    return result


def test_q8_level_order_traversal():
    # Tree:
    #        3
    #       / \
    #      9   20
    #         /  \
    #        15   7
    tree = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    levels = level_order_traversal(tree)
    assert levels == [
        [3],
        [9, 20],
        [15, 7],
    ]
    assert level_order_traversal(None) == []
    print("=== Q8: BFS Level-Order Queue Traversal Verified ===")


# ==============================================================================
# Question 9: First Non-Repeating Character in Stream
# ==============================================================================
class FirstUniqueStream:
    """
    Finds the first non-repeating character in real-time as characters are added.
    Uses a queue of candidates and frequency dictionary.
    """
    def __init__(self):
        self._counts: Dict[str, int] = {}
        self._candidates: List[str] = []

    def add(self, ch: str) -> None:
        self._counts[ch] = self._counts.get(ch, 0) + 1
        self._candidates.append(ch)

    def get_first_unique(self) -> Optional[str]:
        # Evict any candidates from front that now have count > 1
        while self._candidates and self._counts[self._candidates[0]] > 1:
            self._candidates.pop(0)
        return self._candidates[0] if self._candidates else None


def test_q9_first_unique_stream():
    stream = FirstUniqueStream()
    stream.add("a")
    assert stream.get_first_unique() == "a"
    stream.add("b")
    assert stream.get_first_unique() == "a"
    stream.add("a")  # 'a' is now repeated
    assert stream.get_first_unique() == "b"
    stream.add("b")  # 'b' is now repeated
    assert stream.get_first_unique() is None
    stream.add("c")
    assert stream.get_first_unique() == "c"
    print("=== Q9: First Non-Repeating Character in Stream Verified ===")


# ==============================================================================
# Question 10: Architectural Multi-Tenant Fair-Share Task Scheduler
# ==============================================================================
class FairShareTenantQueue:
    """
    Production-grade multi-tenant task scheduler implementing Deficit Round-Robin (DRR).
    Ensures high-volume tenants cannot starve low-volume tenants.
    """
    def __init__(self, quantum_credits: int = 100):
        self.quantum = quantum_credits
        self._queues: Dict[str, List[Dict[str, Any]]] = {}
        self._deficits: Dict[str, int] = {}
        self._active_tenants: List[str] = []

    def submit_task(self, tenant_id: str, task_id: str, cost: int) -> None:
        if tenant_id not in self._queues:
            self._queues[tenant_id] = []
            self._deficits[tenant_id] = 0
            self._active_tenants.append(tenant_id)
        self._queues[tenant_id].append({"task_id": task_id, "cost": cost})

    def schedule_next(self) -> Optional[Dict[str, Any]]:
        """
        Picks the next task to process using Deficit Round-Robin scheduling.
        Returns task dictionary or None if all queues are empty.
        """
        if not self._active_tenants:
            return None

        searched = 0
        while searched < len(self._active_tenants):
            tenant = self._active_tenants[0]
            queue = self._queues[tenant]

            if not queue:
                # Remove exhausted tenant from round-robin rotation
                self._active_tenants.pop(0)
                continue

            self._deficits[tenant] += self.quantum

            # Process tasks while deficit covers cost
            if queue and self._deficits[tenant] >= queue[0]["cost"]:
                task = queue.pop(0)
                self._deficits[tenant] -= task["cost"]
                # Rotate tenant to back of active list
                self._active_tenants.append(self._active_tenants.pop(0))
                return {"tenant": tenant, "task": task}

            # Rotate to next tenant
            self._active_tenants.append(self._active_tenants.pop(0))
            searched += 1

        return None


def test_q10_fair_share_task_scheduler():
    scheduler = FairShareTenantQueue(quantum_credits=100)

    # Tenant A submits 3 heavy tasks (cost 80 each)
    scheduler.submit_task("TenantA", "task_A1", cost=80)
    scheduler.submit_task("TenantA", "task_A2", cost=80)
    scheduler.submit_task("TenantA", "task_A3", cost=80)

    # Tenant B submits 2 light tasks (cost 40 each)
    scheduler.submit_task("TenantB", "task_B1", cost=40)
    scheduler.submit_task("TenantB", "task_B2", cost=40)

    dispatched = []
    while True:
        job = scheduler.schedule_next()
        if not job:
            break
        dispatched.append(f"{job['tenant']}:{job['task']['task_id']}")

    # Verifies both tenants are serviced in fair interleaved round-robin
    assert len(dispatched) == 5
    assert "TenantA:task_A1" in dispatched
    assert "TenantB:task_B1" in dispatched
    # Tenant B is not starved behind Tenant A's 3 tasks
    assert dispatched.index("TenantB:task_B1") < 3
    print("=== Q10: Architectural Multi-Tenant Fair-Share Task Scheduler Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_circular_queue()
    test_q2_linked_queue()
    test_q3_queue_two_stacks()
    test_q4_doubly_linked_deque()
    test_q5_sliding_window_maximum()
    test_q6_binary_min_heap()
    test_q7_moving_average()
    test_q8_level_order_traversal()
    test_q9_first_unique_stream()
    test_q10_fair_share_task_scheduler()
    print("\nAll 10 queue implementation DSA questions passed successfully!")
