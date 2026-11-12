# Cycle Detection (Floyd's Tortoise and Hare, Cycle Entry $\mu$, Length $\lambda$ & Implicit Graphs)

---

## 1. Introduction

A **Cycle** (or loop) in a singly linked list occurs when a node's `.next` pointer points back to an earlier node in the list rather than terminating at `None`, creating a lollipop-shaped structure with a non-cyclic lead-in stem of length $\mu$ and a closed loop of length $\lambda$:

$$\text{head} \xrightarrow{\mu \text{ edges}} \text{Entry Node} \to \dots \to \text{Cycle Tail} \to (\text{back to Entry Node, } \lambda \text{ nodes in loop})$$

**Floyd's Cycle-Finding Algorithm (Tortoise and Hare)** solves cycle detection, cycle entry discovery, and cycle length measurement in **$O(n)$ time and $O(1)$ auxiliary memory** using two pointers moving at different speeds:
- **Tortoise (`slow`):** advances **1 step** per iteration (`slow = slow.next`).
- **Hare (`fast`):** advances **2 steps** per iteration (`fast = fast.next.next`).

---

## 2. Why is it used?

1. **Preventing Infinite Loops in Corrupted Pointer Structures:** Any traversal on a linked list, file-system allocation chain, or memory free-list with an accidental pointer loop will hang forever without cycle detection.
2. **$O(1)$ Memory Footprint vs $O(n)$ Hash Set:** Recording visited node addresses in a `set` takes $O(n)$ memory. Floyd's algorithm uses only two pointer variables (`slow` and `fast`), working even in embedded systems or kernel space where heap allocation is forbidden.
3. **Implicit Functional Graphs ($f: S \to S$):** Any deterministic function mapping a finite set to itself forms a lollipop graph (`x -> f(x) -> f(f(x))`). Floyd's algorithm solves **Find the Duplicate Number** in a read-only array in $O(1)$ space (LeetCode 287), **Happy Number** (LeetCode 202), and **Pollard's rho** integer factorization / cryptographic hash collision search!

---

## 3. Syntax

### A. Phase 1: Detecting Whether a Cycle Exists (LeetCode 141)
```python
def has_cycle(head: ListNode | None) -> bool:
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
```

### B. Phase 2: Finding the Exact Cycle Entry Node (LeetCode 142)
```python
def detect_cycle_entry(head: ListNode | None) -> ListNode | None:
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            # Collision inside cycle! Reset ptr1 to head; move both at speed 1
            ptr1 = head
            ptr2 = slow
            while ptr1 is not ptr2:
                ptr1 = ptr1.next
                ptr2 = ptr2.next
            return ptr1
    return None
```

---

## 4. Explanation (Step-by-Step Mathematical Proof)

### 1. Why `fast` Can Never "Jump Over" `slow` Without Colliding
Once both `slow` and `fast` are inside the cycle of length $\lambda$:
- At each step, `slow` moves forward by $1$ and `fast` moves forward by $2$.
- Therefore, the cyclic distance from `fast` forward to `slow` **decreases by exactly $1$ on every single step** ($\Delta d = 1 - 2 = -1 \pmod{\lambda}$).
- Because the distance decreases by $1$ each step (never by $2$), it cannot skip over $0$ — they are guaranteed to land on the exact same node within at most $\lambda$ iterations after `slow` enters the cycle!

### 2. Why Resetting One Pointer to `head` Meets at the Exact Cycle Entry ($\mu$)
Let:
- $\mu$ = number of edges from `head` to the **Cycle Entry Node**.
- $\lambda$ = number of nodes in the cycle.
- $k$ = distance along the cycle from the **Cycle Entry Node** to the **Collision Node** where `slow` and `fast` meet.

When `slow` and `fast` collide:
$$\text{Distance}(slow) = \mu + k$$
$$\text{Distance}(fast) = \mu + k + m\lambda \quad (\text{for some integer } m \ge 1)$$

Since `fast` travels twice as many steps as `slow`:
$$2(\mu + k) = \mu + k + m\lambda \implies \mu + k = m\lambda \implies \mu = (m - 1)\lambda + (\lambda - k)$$

Notice what this equation says:
- Starting `ptr1` at `head` requires **$\mu$ steps** to reach the Cycle Entry Node.
- Starting `ptr2` at the Collision Node (which is already $k$ steps past the entry) and walking $\mu = (m - 1)\lambda + (\lambda - k)$ steps walks the remaining **$K' = \lambda - k$ steps** to complete the current lap back to the **Cycle Entry Node**, plus $m - 1$ full laps around the cycle!
- Therefore, advancing `ptr1` from `head` and `ptr2` from the Collision Node at **1 step per iteration** guarantees they meet for the first time at the **exact Cycle Entry Node**!

---

## 5. Minimum 3 Examples

### Example 1: Floyd's Tortoise and Hare vs Hash Set Cycle Detection
File: [`example_01_floyd_tortoise_and_hare_cycle_detection.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/E_Linked_Lists/05_Cycle_Detection/example_01_floyd_tortoise_and_hare_cycle_detection.py)

```python
from typing import List, Optional, Set, Tuple


class ListNode:
    """A node in a singly linked list."""

    def __init__(self, val: int) -> None:
        self.val: int = val
        self.next: Optional["ListNode"] = None


def build_linked_list_with_cycle(values: List[int], pos: int) -> Optional[ListNode]:
    if not values:
        return None
    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if 0 <= pos < len(nodes):
        nodes[-1].next = nodes[pos]
    return nodes[0]


def has_cycle_hash_set(head: Optional[ListNode]) -> bool:
    visited_ids: Set[int] = set()
    curr = head
    while curr is not None:
        node_id = id(curr)
        if node_id in visited_ids:
            return True
        visited_ids.add(node_id)
        curr = curr.next
    return False


def has_cycle_floyd_with_trace(head: Optional[ListNode]) -> Tuple[bool, List[str]]:
    trace: List[str] = []
    slow = head
    fast = head
    step = 0

    while fast is not None and fast.next is not None:
        step += 1
        slow = slow.next          # type: ignore[assignment]
        fast = fast.next.next
        assert slow is not None
        fast_str = str(fast.val) if fast is not None else "None"
        trace.append(f"Step {step}: slow={slow.val}, fast={fast_str}")
        if slow is fast:
            return True, trace

    return False, trace
```

---

### Example 2: Finding Exact Cycle Entry Node ($\mu$), Cycle Length ($\lambda$), and Cycle Removal
File: [`example_02_cycle_entry_node_length_and_removal.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/E_Linked_Lists/05_Cycle_Detection/example_02_cycle_entry_node_length_and_removal.py)

```python
def analyze_and_remove_cycle(
    head: Optional[ListNode],
) -> Tuple[Optional[ListNode], int, int]:
    slow = head
    fast = head

    # Phase 1: Detect collision inside the cycle
    while fast is not None and fast.next is not None:
        slow = slow.next          # type: ignore[assignment]
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None, 0, 0

    # Phase 2: Find the exact cycle entry node and count `mu`
    ptr1 = head
    ptr2 = slow
    mu = 0
    while ptr1 is not ptr2:
        assert ptr1 is not None and ptr2 is not None
        ptr1 = ptr1.next
        ptr2 = ptr2.next
        mu += 1

    entry_node = ptr1
    assert entry_node is not None

    # Phase 3: Walk around the cycle once to measure `lambda` and locate cycle tail
    cycle_tail = entry_node
    lambda_len = 1
    while cycle_tail.next is not entry_node:
        assert cycle_tail.next is not None
        cycle_tail = cycle_tail.next
        lambda_len += 1

    # Break the cycle cleanly in O(1)
    cycle_tail.next = None

    return entry_node, mu, lambda_len
```

---

### Example 3: Implicit Linked List Cycle Detection (Find Duplicate Number & Happy Number)
File: [`example_03_implicit_cycle_duplicate_number_and_happy_number.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/E_Linked_Lists/05_Cycle_Detection/example_03_implicit_cycle_duplicate_number_and_happy_number.py)

```python
from typing import List, Tuple


def find_duplicate_number_floyd(nums: List[int]) -> int:
    """
    Finds the duplicate number in `nums` (length n + 1, values in 1..n) in
    O(n) time and O(1) auxiliary space without modifying `nums`.
    """
    # Phase 1: Intersect inside the cycle
    slow = nums[0]
    fast = nums[nums[0]]
    while slow != fast:
        slow = nums[slow]
        fast = nums[nums[fast]]

    # Phase 2: Find the entrance to the cycle (the duplicate number)
    ptr1 = 0
    ptr2 = slow
    while ptr1 != ptr2:
        ptr1 = nums[ptr1]
        ptr2 = nums[ptr2]

    return ptr1
```

---

## 6. Output

### Output — Example 1 (`example_01_floyd_tortoise_and_hare_cycle_detection.py`)
```text
========================================================================
Floyd's Tortoise & Hare vs Hash Set Cycle Detection
========================================================================

Case: Cyclic List (tail -> index 1 [val 20])
  Values=[10, 20, 30, 40, 50], cycle_pos=1 -> Has Cycle: True
    Step 1: slow=20, fast=30
    Step 2: slow=30, fast=50
    Step 3: slow=40, fast=30
    Step 4: slow=50, fast=50

Case: Self-Loop Single Node (pos = 0)
  Values=[99], cycle_pos=0 -> Has Cycle: True
    Step 1: slow=99, fast=99

Case: Acyclic List (pos = -1)
  Values=[1, 2, 3, 4, 5], cycle_pos=-1 -> Has Cycle: False
    Step 1: slow=2, fast=3
    Step 2: slow=3, fast=5

Case: Empty List
  Values=[], cycle_pos=-1 -> Has Cycle: False
```

### Output — Example 2 (`example_02_cycle_entry_node_length_and_removal.py`)
```text
========================================================================
Cycle Entry Node (mu), Cycle Length (lambda), and Cycle Removal
========================================================================

Input List: [10, 20, 30, 40, 50, 60, 70] with tail connected to pos=2
  Cycle Entry Node = 30 (mu = 2 steps from head, cycle length lambda = 5)
  After unlinking cycle tail -> Acyclic List: [10, 20, 30, 40, 50, 60, 70]

Input List: [100, 200, 300, 400] with tail connected to pos=0
  Cycle Entry Node = 100 (mu = 0 steps from head, cycle length lambda = 4)
  After unlinking cycle tail -> Acyclic List: [100, 200, 300, 400]

Input List: [5, 15, 25] with tail connected to pos=2
  Cycle Entry Node = 25 (mu = 2 steps from head, cycle length lambda = 1)
  After unlinking cycle tail -> Acyclic List: [5, 15, 25]

Input List: [1, 2, 3, 4] with tail connected to pos=-1
  Result: Acyclic list (no cycle detected)
```

### Output — Example 3 (`example_03_implicit_cycle_duplicate_number_and_happy_number.py`)
```text
========================================================================
1. Find the Duplicate Number via Implicit Linked List (LeetCode 287)
========================================================================
Array: [1, 3, 4, 2, 2]
  Duplicate (Cycle Entry Node) = 2
Array: [3, 1, 3, 4, 2]
  Duplicate (Cycle Entry Node) = 3
Array: [2, 5, 9, 6, 9, 3, 8, 9, 7, 1]
  Duplicate (Cycle Entry Node) = 9

========================================================================
2. Happy Number Cycle Detection in O(1) Space (LeetCode 202)
========================================================================
n = 19 -> Happy: True  | Fast-Pointer Sample: [19, 82, 100, 1]
n = 2  -> Happy: False | Fast-Pointer Sample: [2, 4, 37, 89, 42, 4, 37, 89, 42]
n = 7  -> Happy: True  | Fast-Pointer Sample: [7, 49, 130, 1]
n = 20 -> Happy: False | Fast-Pointer Sample: [20, 4, 37, 89, 42, 4, 37, 89, 42]
```

---

## 7. Code Explanation

1. **Why `while fast is not None and fast.next is not None:` is the Exact Guard:**
   Because `fast` jumps two steps (`fast.next.next`), we must verify both that `fast` itself is not `None` and that `fast.next` is not `None` before accessing `fast.next.next`. Since `slow` trails behind `fast`, `slow` is guaranteed not to be `None`.
2. **Why `find_duplicate_number_floyd` Starts at Index `0`:**
   In LeetCode 287, the array has length $n + 1$ and contains integers in $[1, n]$. Because $0$ is never a value in `nums`, index $0$ has **in-degree $0$** — no index points back to $0$. That guarantees index $0$ lies strictly outside the cycle, so starting at `0` avoids getting trapped inside a disconnected self-loop!

---

## 8. Common Mistakes

1. **Initializing `slow = head` and `fast = head.next` Without Adjusting Phase 2:**
   If you start `fast = head.next` instead of `fast = head`, `fast` begins 1 step ahead at $t = 0$. When `slow` and `fast` collide, $\text{Distance}(fast) = 2 \cdot \text{Distance}(slow) + 1$, which shifts the Phase 2 meeting point off by 1 (`ptr2` must start at `slow.next` instead of `slow`). Always initialize **both** `slow = head` and `fast = head` so the algebra $\mu = m\lambda - k$ holds cleanly!
2. **Storing `curr.val` Instead of `id(curr)` (or `curr`) in a Hash Set:**
   Linked list nodes can have duplicate `.val` integers without forming a cycle. Always store node object references (or `id(curr)`) in the visited set.
3. **Only Checking `while fast.next is not None:`:**
   When the list has an even number of nodes and no cycle, `fast` lands on `None`, so evaluating `fast.next` raises `AttributeError: 'NoneType' object has no attribute 'next'`.

---

## 9. Practice Questions

1. **Easy — Linked List Cycle Length ($\lambda$) Only:**
   Given the `head` of a linked list, return the number of nodes in the cycle if a cycle exists, or `0` if the list is acyclic, in $O(n)$ time and $O(1)$ space.
2. **Medium — Intersection of Two Acyclic Linked Lists via Temporary Cycle (LeetCode 160):**
   Given heads `headA` and `headB` of two acyclic singly linked lists, temporarily link the tail of list A to `headB`, run `detect_cycle_entry(headA)` to find their intersection node in $O(1)$ space, and restore list A's tail to `None` before returning.
3. **Hard — Circular Array Loop (LeetCode 457):**
   Given a circular array `nums` of non-zero positive and negative step offsets, determine in $O(n)$ time and $O(1)$ space whether there is a cycle of length $> 1$ where all steps in the cycle move in the **same direction** (all forward or all backward).

---

## 10. Interview Questions

### Q1: What happens if the fast pointer moves 3 steps at a time (`fast = fast.next.next.next`) instead of 2?
**Answer:** It still works on a cyclic list, and on an acyclic list it reaches `None` slightly faster ($n/3$ iterations), **but**:
1. You must check three `None` conditions per iteration (`fast and fast.next and fast.next.next`).
2. Inside a cycle of even length $\lambda$, the relative gap decreases by $2$ per step, which can skip over $0$ on the first lap and require up to $2$ laps to collide. Moving by 2 steps is strictly simpler and guarantees collision on the very first lap after `slow` enters the cycle.

### Q2: What is the worst-case total number of steps `slow` takes before colliding with `fast`?
**Answer:** At most $\mu + \lambda - 1 < n$ steps! `slow` takes $\mu$ steps to reach the cycle entry node, and once inside the cycle of length $\lambda$, the gap between `fast` and `slow` is at most $\lambda - 1$ and shrinks by $1$ every step. Thus `slow` never completes even one full lap of the cycle before `fast` catches it.

### Q3: What is Brent's Cycle Detection Algorithm, and how does it compare to Floyd's?
**Answer:** Brent's algorithm ("Teleporting Turtle") moves only one pointer (`fast`) at each step and teleports `slow = fast` whenever the step count reaches a power of two ($1, 2, 4, 8, \dots$). It uses the same $O(1)$ space and $O(n)$ asymptotic time as Floyd's, makes ~36% fewer `.next` evaluations on average, and directly yields the cycle length $\lambda$ during Phase 1.
