# Circular Linked List (Tail-Anchored Ring, Sorted Insertion & Round-Robin Scheduling)

---

## 1. Introduction

A **Circular Linked List** is a variation of a linked list in which the last node's `.next` pointer does **not** point to `None` — instead, it points back to the first node (`head`), forming a closed continuous ring:

$$\text{head} \to 10 \to 20 \to 30 \to 40 \to (\text{back to } 10)$$

A critical architectural insight for **Circular Singly Linked Lists** is **anchoring the list at `self.tail` rather than `self.head`**:
- If you only store `self.head`, inserting a node at the front or back requires updating the last node's `.next` pointer, forcing an $O(n)$ traversal around the entire ring.
- If you store `self.tail` instead, **the head node is simply `self.tail.next`!** That gives you **$O(1)$ access to both `head` and `tail`** using only a single pointer on the container class:
  - `prepend(val)` (insert at front): $O(1)$
  - `append(val)` (insert at back): $O(1)$
  - `pop_front()` (remove from front): $O(1)$
  - `rotate_clockwise(1)` (move front element to back): $O(1)$ via `self.tail = self.tail.next`!

---

## 2. Why is it used?

1. **Operating System Round-Robin CPU Schedulers:** Active processes waiting for CPU time slices are placed in a circular queue. When a process uses up its `time_quantum` without finishing, rotating it to the back of the queue is a single pointer assignment (`tail = tail.next`) in $O(1)$ time with zero memory allocation.
2. **Multiplayer Turn-Based Games & Token Rings:** Cycling through players in Monopoly/Poker or passing network transmission tokens around a ring naturally wraps from the last participant back to the first.
3. **Continuous Media Playlists & Audio Ring Buffers:** Looping playlists and circular streaming buffers advance indefinitely without checking for `None` boundaries.
4. **Classic Algorithmic Problems:** Splitting a circular list into two halves, inserting into a sorted circular list from an arbitrary starting node (LeetCode 708), and the **Flavius Josephus Elimination Circle**.

---

## 3. Syntax

### A. Tail-Anchored Circular Singly Linked List ($O(1)$ Head & Tail Operations)
```python
class CNode:
    def __init__(self, val: int) -> None:
        self.val = val
        self.next: CNode | None = None


class TailAnchoredCircularLinkedList:
    def __init__(self) -> None:
        self.tail: CNode | None = None
        self._size: int = 0

    def prepend(self, val: int) -> None:
        new_node = CNode(val)
        if self.tail is None:
            new_node.next = new_node
            self.tail = new_node
        else:
            new_node.next = self.tail.next
            self.tail.next = new_node
        self._size += 1

    def append(self, val: int) -> None:
        self.prepend(val)
        self.tail = self.tail.next  # Advance tail to newly inserted node!
```

### B. Emulating a `do-while` Traversal Loop in Python
Because every node in a non-empty circular list has a non-`None` `.next` pointer, a standard `while curr is not None:` loop will run **forever**. Instead, use Python's `while True:` + `if curr is start: break` idiom:
```python
if head is not None:
    curr = head
    while True:
        process(curr.val)
        curr = curr.next
        if curr is head:
            break
```

---

## 4. Explanation (Step-by-Step)

### 1. Why `append(val)` is Just `prepend(val)` + `self.tail = self.tail.next`
Suppose the circular ring is `10 -> 20 -> 30 -> (back to 10)`, with `self.tail = Node(30)` and `self.tail.next = Node(10)` (the head).
- Calling `prepend(40)` splices `Node(40)` between `self.tail` (`30`) and `self.tail.next` (`10`):
  - `Node(40).next = Node(10)`
  - `Node(30).next = Node(40)`
- If we stop here, `self.tail.next` is `Node(40)`, so `40` is the **new head**.
- If we immediately execute `self.tail = self.tail.next` (`self.tail = Node(40)`), then `Node(40)` becomes the **new tail**, and `self.tail.next` remains `Node(10)` (the old head)!

### 2. All 4 Edge Cases of Inserting into a Sorted Circular List (LeetCode 708)
Given an arbitrary node `entry` in a non-decreasing circular list:
1. **Case 0 (`entry is None`):** Create a single node pointing to itself (`new_node.next = new_node`).
2. **Case 1 (`prev.val <= insert_val <= curr.val`):** Normal middle insertion between two adjacent sorted nodes.
3. **Case 2 (`prev.val > curr.val`):** We are standing at the **wrap-around cliff** where the maximum tail (`prev`) meets the minimum head (`curr`). If `insert_val >= prev.val` (new global maximum) or `insert_val <= curr.val` (new global minimum), insert right here at the cliff!
4. **Case 3 (`prev is entry` after a full lap):** All nodes in the ring have identical values (e.g., `7 -> 7 -> 7`), so insert right after `prev`.

---

## 5. Minimum 3 Examples

### Example 1: Tail-Anchored Circular Singly Linked List & Splitting a Ring in Halves
File: [`example_01_tail_anchored_circular_singly_linked_list.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/E_Linked_Lists/03_Circular_Linked_List/example_01_tail_anchored_circular_singly_linked_list.py)

```python
from typing import Any, List, Optional, Tuple


class CNode:
    """A node in a circular singly linked list."""

    def __init__(self, val: Any) -> None:
        self.val: Any = val
        self.next: Optional["CNode"] = None


class TailAnchoredCircularLinkedList:
    """
    A Circular Singly Linked List anchored at `self.tail` where `self.tail.next`
    always points back to the head node.
    """

    def __init__(self) -> None:
        self.tail: Optional[CNode] = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self.tail is None

    def prepend(self, val: Any) -> None:
        """Inserts `val` at the front (head) in O(1) time."""
        new_node = CNode(val)
        if self.tail is None:
            new_node.next = new_node
            self.tail = new_node
        else:
            new_node.next = self.tail.next
            self.tail.next = new_node
        self._size += 1

    def append(self, val: Any) -> None:
        """Inserts `val` at the back (tail) in O(1) time."""
        self.prepend(val)
        assert self.tail is not None
        self.tail = self.tail.next

    def pop_front(self) -> Any:
        """Removes and returns the head element in O(1) time."""
        if self.tail is None:
            raise IndexError("pop_front from an empty circular linked list")

        head = self.tail.next
        assert head is not None
        if head is self.tail:
            self.tail = None
        else:
            self.tail.next = head.next
        self._size -= 1
        return head.val

    def rotate_clockwise(self, steps: int = 1) -> None:
        """Advances the circular ring by `steps` positions in O(steps) time."""
        if self.tail is None or self._size <= 1:
            return
        steps %= self._size
        for _ in range(steps):
            assert self.tail is not None
            self.tail = self.tail.next

    insert_back = append
    rotate_forward = rotate_clockwise

    def to_list(self) -> List[Any]:
        """Traverses the ring exactly once from head (`tail.next`) to `tail`."""
        if self.tail is None:
            return []
        result: List[Any] = []
        curr = self.tail.next
        while True:
            assert curr is not None
            result.append(curr.val)
            if curr is self.tail:
                break
            curr = curr.next
        return result


CircularSinglyLinkedList = TailAnchoredCircularLinkedList


def split_circular_list_in_halves(head: Optional[CNode]) -> Tuple[Optional[CNode], Optional[CNode]]:
    if head is None or head.next is head:
        return head, None

    slow: CNode = head
    fast: CNode = head

    while fast.next is not head and fast.next.next is not head:
        slow = slow.next          # type: ignore[assignment]
        fast = fast.next.next     # type: ignore[assignment]

    if fast.next.next is head:
        fast = fast.next          # type: ignore[assignment]

    head1 = head
    head2 = slow.next

    slow.next = head1
    fast.next = head2

    return head1, head2
```

---

### Example 2: Insert into a Sorted Circular Linked List (All 4 Edge Cases — LeetCode 708)
File: [`example_02_insert_into_sorted_circular_linked_list.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/E_Linked_Lists/03_Circular_Linked_List/example_02_insert_into_sorted_circular_linked_list.py)

```python
from typing import List, Optional


class Node:
    def __init__(self, val: int, next_node: Optional["Node"] = None) -> None:
        self.val: int = val
        self.next: Optional["Node"] = next_node


def insert_into_sorted_circular_list(entry: Optional[Node], insert_val: int) -> Node:
    new_node = Node(insert_val)

    # Case 0: Empty list -> create a 1-node ring pointing to itself
    if entry is None:
        new_node.next = new_node
        return new_node

    prev: Node = entry
    curr: Node = entry.next  # type: ignore[assignment]

    while True:
        # Case 1: Normal sorted interval where prev.val <= insert_val <= curr.val
        if prev.val <= insert_val <= curr.val:
            break

        # Case 2: At the wrap-around cliff where max tail (prev) meets min head (curr)
        if prev.val > curr.val:
            if insert_val >= prev.val or insert_val <= curr.val:
                break

        prev = curr
        curr = curr.next  # type: ignore[assignment]

        # Case 3: Completed a full revolution (all nodes are uniform values)
        if prev is entry:
            break

    prev.next = new_node
    new_node.next = curr
    return entry
```

---

### Example 3: OS Round-Robin CPU Scheduler & Josephus Circle Simulation
File: [`example_03_round_robin_scheduler_and_josephus_problem.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/E_Linked_Lists/03_Circular_Linked_List/example_03_round_robin_scheduler_and_josephus_problem.py)

```python
from dataclasses import dataclass
from example_01_tail_anchored_circular_singly_linked_list import (
    CNode,
    CircularSinglyLinkedList,
)


@dataclass
class TaskBurst:
    name: str
    remaining_ms: int


def simulate_round_robin_scheduler(
    tasks: list[tuple[str, int]], quantum_ms: int
) -> list[tuple[str, int]]:
    ring = CircularSinglyLinkedList()
    for name, burst in tasks:
        ring.insert_back(TaskBurst(name, burst))

    clock_ms = 0
    completed: list[tuple[str, int]] = []

    while len(ring) > 0:
        assert ring.tail is not None and ring.tail.next is not None
        head_task: TaskBurst = ring.tail.next.val
        run_slice = min(quantum_ms, head_task.remaining_ms)
        clock_ms += run_slice
        head_task.remaining_ms -= run_slice

        if head_task.remaining_ms == 0:
            ring.pop_front()
            completed.append((head_task.name, clock_ms))
        else:
            ring.rotate_forward()

    return completed
```

---

## 6. Output

### Output — Example 1 (`example_01_tail_anchored_circular_singly_linked_list.py`)
```text
========================================================================
1. Tail-Anchored Circular Singly Linked List (O(1) Head & Tail Ops)
========================================================================
After prepend(10) & append(20..50): [10, 20, 30, 40, 50]
  Head (tail.next) = 10, Tail = 50, Size = 5
After rotate_clockwise(2):          [30, 40, 50, 10, 20]
  New Head = 30, New Tail = 20
After pop_front() -> 30:            [40, 50, 10, 20]

========================================================================
2. Splitting a Circular Linked List into Two Circular Halves
========================================================================
Original Ring (5 nodes): [1, 2, 3, 4, 5]
  First Circular Half  : [1, 2, 3]
  Second Circular Half : [4, 5]
Original Ring (6 nodes): [10, 20, 30, 40, 50, 60]
  First Circular Half  : [10, 20, 30]
  Second Circular Half : [40, 50, 60]
```

### Output — Example 2 (`example_02_insert_into_sorted_circular_linked_list.py`)
```text
========================================================================
Insert into a Sorted Circular Linked List (All 4 Edge Cases)
========================================================================
Case 0 (Empty List -> insert 10)        : [10]
Initial Ring (anchored at arbitrary 20) : [20, 30, 10]
Case 1 (Middle insert 25)               : [20, 25, 30, 10]
Case 2a (New global minimum 5)          : [20, 25, 30, 5, 10]
Case 2b (New global maximum 40)         : [20, 25, 30, 40, 5, 10]

Uniform Ring before insert              : [7, 7, 7]
Case 3 (Uniform ring -> insert 9)       : [7, 9, 7, 7]
```

### Output — Example 3 (`example_03_round_robin_scheduler_and_josephus_problem.py`)
```text
========================================================================
1. OS ROUND-ROBIN CPU SCHEDULER (TIME QUANTUM = 4 ms)
========================================================================
Initial Tasks (Name, Burst ms): [('P1_Web', 10), ('P2_DB', 4), ('P3_Auth', 6)]
  Task P2_DB    completed at t =  8 ms
  Task P3_Auth  completed at t = 18 ms
  Task P1_Web   completed at t = 20 ms

========================================================================
2. JOSEPHUS ELIMINATION CIRCLE (N = 7, EVERY K = 3RD ELIMINATED)
========================================================================
Elimination Order : [3, 6, 2, 7, 5, 1]
Last Survivor     : Person #4
```

---

## 7. Code Explanation

1. **Single-Node Deallocation in `pop_front()`:**
   When `self.tail.next is self.tail`, the circular list contains only **one** node pointing to itself. Setting `self.tail = None` breaks the self-reference and leaves the list cleanly empty.
2. **Splitting a Ring into Two Circular Halves (`split_circular_list_in_halves`):**
   Using Fast & Slow pointers with termination condition `while fast.next is not head and fast.next.next is not head:`, `slow` stops at the tail of the first half, and `fast` stops at (or one node before) the tail of the second half. Closing both halves via `slow.next = head1` and `fast.next = head2` creates two independent circular lists in $O(1)$ space.

---

## 8. Common Mistakes

1. **Using `while curr is not None:` on a Circular List:**
   Because no node in a non-empty circular list has `.next is None`, a standard `while curr:` loop causes an **infinite loop**. Always compare node identity (`is`) against your starting anchor node.
2. **Comparing Node Values (`curr.val == head.val`) Instead of Object Identity (`curr is head`):**
   If duplicate values exist in the ring, stopping when `curr.val == head.val` terminates early before completing a full traversal. Always use `curr is head`.
3. **Forgetting to Set `self.tail = None` When Deleting the Last Remaining Node:**
   If you execute `self.tail.next = head.next` when `head is self.tail`, the single node stays linked to itself and is never removed!

---

## 9. Practice Questions

1. **Easy — Check if a Linked List is Strictly Circular:**
   Given the `head` of a singly linked list, write a function `is_circular_from_head(head)` that returns `True` if every node is part of a single cycle that returns directly to `head`, and `False` if it terminates at `None` or enters a cycle that does not include `head`.
2. **Medium — Delete a Value from a Tail-Anchored Circular Linked List:**
   Implement `remove(val)` on `TailAnchoredCircularLinkedList` that deletes the first occurrence of `val` in $O(n)$ time, properly handling deleting the head (`tail.next`), deleting the `tail` itself (updating `self.tail` to its predecessor), and deleting the sole node in a 1-node ring.
3. **Hard — Josephus Problem in $O(n)$ Mathematical Recurrence vs $O(n \cdot k)$ Ring Simulation:**
   Derive and implement the $O(n)$ mathematical recurrence $J(n, k) = (J(n - 1, k) + k) \bmod n$ (0-indexed) and verify that `josephus_math(n, k) + 1` matches `josephus_circle_simulation(n, k)[0]` for all $1 \le n, k \le 50$.

---

## 10. Interview Questions

### Q1: Why does a Circular Singly Linked List store `self.tail` instead of `self.head`?
**Answer:** In a singly linked ring, moving forward from `tail` to `head` takes 1 step (`head = tail.next`), whereas moving backward from `head` to `tail` takes $n - 1$ steps. Storing `self.tail` gives $O(1)$ access to both ends (`self.tail` and `self.tail.next`), making `prepend`, `append`, and `pop_front` all $O(1)$.

### Q2: Can a Circular Singly Linked List support `pop_back()` (removing `self.tail`) in $O(1)$ time?
**Answer:** No! Removing `self.tail` requires updating the **second-to-last** node's `.next` pointer to point to `head` and setting `self.tail` to that predecessor. Finding the predecessor of `self.tail` in a singly linked ring requires traversing $n - 1$ nodes ($O(n)$ time). If $O(1)$ `pop_back()` is required, use a **Circular Doubly Linked List** (such as CPython's internal doubly linked ring or sentinel DLL).

### Q3: In `insert_into_sorted_circular_list` (LeetCode 708), what happens if all nodes in the ring have the same value (e.g., `5 -> 5 -> 5`) and we insert `8`?
**Answer:** Neither `prev.val <= 8 <= curr.val` nor `prev.val > curr.val` will ever be true because `prev.val == curr.val == 5` everywhere. Without the third termination check `if prev is entry: break` after advancing `prev` and `curr`, the loop would spin forever.
