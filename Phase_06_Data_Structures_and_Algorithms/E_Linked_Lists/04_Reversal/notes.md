# Linked List Reversal (`prev`, `curr`, `nxt` & In-Place Sublist Splicing)

---

## 1. Introduction

**Reversing a Singly Linked List** means flipping the direction of every `.next` pointer in-place so that the original tail node becomes the new `head` and the original `head` becomes the new tail pointing to `None`:

$$\text{Before: } 10 \to 20 \to 30 \to 40 \to \text{None}$$
$$\text{After: } 40 \to 30 \to 20 \to 10 \to \text{None}$$

Mastering in-place reversal is one of the highest-leverage skills in Data Structures & Algorithms because it is the core building block inside dozens of medium and hard interview problems:
- **Full List Reversal** (Iterative $O(1)$-space 3-pointer pattern vs Recursive $O(n)$-stack pattern — LeetCode 206).
- **Sublist Reversal Between Positions `[left .. right]`** in a single pass using the **Head-Insertion (Tail-Pulling) Trick** (LeetCode 92).
- **Reverse Nodes in $k$-Group** (LeetCode 25 Hard) and **Swap Nodes in Pairs** (LeetCode 24).
- **Palindrome Linked List** & **Reorder List** (reversing the second half in $O(1)$ space).

---

## 2. Why is it used?

1. **Zero Extra Memory ($O(1)$ Auxiliary Space):** Unlike arrays where you can read backward from index `n - 1` down to `0`, a singly linked list only has forward `.next` pointers. Copying nodes into a Python `list` or stack to traverse backward wastes $O(n)$ heap memory. Reversing pointers in-place achieves backward traversal in $O(1)$ auxiliary memory.
2. **Localized Window Reordering:** Packet buffers, undo logs, and memory allocators frequently need to reverse or swap contiguous chunks of nodes ($k$-groups or `[left..right]` ranges) without reallocating node objects.
3. **Interview Gatekeeper:** Pointer reversal tests whether a candidate can update multiple coupled references (`prev`, `curr`, `nxt`, `sub_prev`, `sub_tail`) in the exact order required without losing the rest of the chain or creating an accidental two-node cycle.

---

## 3. Syntax

### A. Iterative 3-Pointer Reversal ($O(n)$ Time, $O(1)$ Space)
```python
def reverse_list(head: ListNode | None) -> ListNode | None:
    prev: ListNode | None = None
    curr: ListNode | None = head

    while curr is not None:
        nxt = curr.next     # 1. Save next node before overwriting curr.next
        curr.next = prev    # 2. Flip pointer backward
        prev = curr         # 3. Advance prev forward
        curr = nxt          # 4. Advance curr forward

    return prev             # prev is the new head
```

### B. Recursive Reversal ($O(n)$ Time, $O(n)$ Call Stack)
```python
def reverse_list_recursive(head: ListNode | None) -> ListNode | None:
    if head is None or head.next is None:
        return head
    new_head = reverse_list_recursive(head.next)
    head.next.next = head   # Make next node point back to head
    head.next = None        # Prevent 2-node cycle at the new tail!
    return new_head
```

### C. One-Pass Sublist Reversal `[left .. right]` (Head-Insertion Splice)
```python
def reverse_between(head: ListNode | None, left: int, right: int) -> ListNode | None:
    dummy = ListNode(0, next=head)
    sub_prev = dummy
    for _ in range(left - 1):
        sub_prev = sub_prev.next

    sub_tail = sub_prev.next
    for _ in range(right - left):
        move_node = sub_tail.next
        sub_tail.next = move_node.next
        move_node.next = sub_prev.next
        sub_prev.next = move_node

    return dummy.next
```

---

## 4. Explanation (Step-by-Step)

### Step-by-Step Trace of Iterative 3-Pointer Reversal on `10 -> 20 -> 30 -> None`

1. **Initialization:** `prev = None`, `curr = Node(10)`.
2. **Iteration 1 (`curr = 10`):**
   - `nxt = curr.next` (`Node(20)`).
   - `curr.next = prev` (`10 -> None`).
   - `prev = curr` (`prev = Node(10)`).
   - `curr = nxt` (`curr = Node(20)`).
3. **Iteration 2 (`curr = 20`):**
   - `nxt = curr.next` (`Node(30)`).
   - `curr.next = prev` (`20 -> 10 -> None`).
   - `prev = curr` (`prev = Node(20)`).
   - `curr = nxt` (`curr = Node(30)`).
4. **Iteration 3 (`curr = 30`):**
   - `nxt = curr.next` (`None`).
   - `curr.next = prev` (`30 -> 20 -> 10 -> None`).
   - `prev = curr` (`prev = Node(30)`).
   - `curr = nxt` (`curr = None`).
5. **Termination:** `curr is None`, loop exits, and we return `prev` (`Node(30)`).

### Step-by-Step Trace of One-Pass Sublist Reversal (`left=2, right=4` on `10 -> 20 -> 30 -> 40 -> 50`)

- Anchor `sub_prev` at `Node(10)` (just before position 2) and `sub_tail` at `Node(20)`.
- **Pull 1 (`move_node = 30`):** Detach `30` (`20.next = 40`), insert `30` right after `10` (`30.next = 20`, `10.next = 30`). Chain becomes `10 -> 30 -> 20 -> 40 -> 50`.
- **Pull 2 (`move_node = 40`):** Detach `40` (`20.next = 50`), insert `40` right after `10` (`40.next = 30`, `10.next = 40`). Chain becomes `10 -> 40 -> 30 -> 20 -> 50`.

---

## 5. Minimum 3 Examples

### Example 1: Iterative $O(1)$-Space vs Recursive $O(n)$-Stack Reversal
File: [`example_01_iterative_and_recursive_linked_list_reversal.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/E_Linked_Lists/04_Reversal/example_01_iterative_and_recursive_linked_list_reversal.py)

```python
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class ListNode:
    val: int
    next: ListNode | None = None


def from_list(values: list[int]) -> ListNode | None:
    dummy = ListNode(0)
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(head: ListNode | None) -> list[int]:
    out: list[int] = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


def reverse_linked_list_iterative(head: ListNode | None) -> ListNode | None:
    prev: ListNode | None = None
    curr: ListNode | None = head

    while curr is not None:
        nxt = curr.next     # 1. Save reference to the rest of the chain!
        curr.next = prev    # 2. Reverse current node's pointer backward to `prev`
        prev = curr         # 3. Advance `prev` one step forward
        curr = nxt          # 4. Advance `curr` one step forward

    return prev             # `prev` now points to the new head!


def reverse_linked_list_recursive(head: ListNode | None) -> ListNode | None:
    if head is None or head.next is None:
        return head

    new_head = reverse_linked_list_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head


if __name__ == "__main__":
    print("=" * 72)
    print("1. ITERATIVE O(1)-SPACE vs RECURSIVE O(N)-STACK LINKED LIST REVERSAL")
    print("=" * 72)

    original = [10, 20, 30, 40, 50]
    h1 = from_list(original)
    rev_iter = reverse_linked_list_iterative(h1)
    print(f"Original Chain             : {original}")
    print(f"Iterative Reversal O(1)    : {to_list(rev_iter)}")

    rev_back = reverse_linked_list_recursive(rev_iter)
    print(f"Recursive Reversal Back    : {to_list(rev_back)}")
```

---

### Example 2: Reverse Sublist Between Positions `[left .. right]` in One Pass
File: [`example_02_reverse_between_sublist_one_pass.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/E_Linked_Lists/04_Reversal/example_02_reverse_between_sublist_one_pass.py)

```python
from example_01_iterative_and_recursive_linked_list_reversal import (
    ListNode,
    from_list,
    to_list,
)


def reverse_between_one_pass(
    head: ListNode | None, left: int, right: int
) -> ListNode | None:
    if head is None or left == right:
        return head

    dummy = ListNode(0, next=head)
    sub_prev: ListNode = dummy

    for _ in range(left - 1):
        assert sub_prev.next is not None
        sub_prev = sub_prev.next

    sub_tail = sub_prev.next
    assert sub_tail is not None

    for _ in range(right - left):
        move_node = sub_tail.next
        assert move_node is not None
        sub_tail.next = move_node.next
        move_node.next = sub_prev.next
        sub_prev.next = move_node

    return dummy.next


if __name__ == "__main__":
    print("=" * 72)
    print("1. REVERSE SUBLIST BETWEEN POSITIONS [LEFT .. RIGHT] (LEETCODE 92)")
    print("=" * 72)

    chain = from_list([10, 20, 30, 40, 50, 60, 70])
    print(f"Original Chain (1..7)          : {to_list(chain)}")

    res = reverse_between_one_pass(chain, left=2, right=5)
    print(f"Reverse Between [left=2..5]    : {to_list(res)} ([20,30,40,50] -> [50,40,30,20])")

    res_head = reverse_between_one_pass(res, left=1, right=3)
    print(f"Reverse Between [left=1..3]    : {to_list(res_head)}")
```

---

### Example 3: Reverse Nodes in $k$-Group in $O(1)$ Space (LeetCode 25 Hard)
File: [`example_03_reverse_nodes_in_k_group.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/E_Linked_Lists/04_Reversal/example_03_reverse_nodes_in_k_group.py)

```python
from example_01_iterative_and_recursive_linked_list_reversal import (
    ListNode,
    from_list,
    to_list,
)


def reverse_k_group(head: ListNode | None, k: int) -> ListNode | None:
    if head is None or k <= 1:
        return head

    dummy = ListNode(0, next=head)
    group_prev: ListNode = dummy

    while True:
        kth_node: ListNode | None = group_prev
        for _ in range(k):
            assert kth_node is not None
            kth_node = kth_node.next
            if kth_node is None:
                return dummy.next

        group_next = kth_node.next

        prev: ListNode | None = group_next
        curr: ListNode | None = group_prev.next
        while curr is not group_next:
            assert curr is not None
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        old_group_head = group_prev.next
        assert old_group_head is not None
        group_prev.next = kth_node
        group_prev = old_group_head


if __name__ == "__main__":
    print("=" * 72)
    print("1. REVERSE NODES IN K-GROUP IN O(1) SPACE (LEETCODE 25 HARD)")
    print("=" * 72)

    for k_val in [2, 3, 4]:
        sample = from_list([1, 2, 3, 4, 5, 6, 7, 8])
        reversed_k = reverse_k_group(sample, k=k_val)
        print(f"  Input [1..8], k = {k_val} -> {to_list(reversed_k)}")
```

---

## 6. Output

### Output — Example 1 (`example_01_iterative_and_recursive_linked_list_reversal.py`)
```text
========================================================================
1. ITERATIVE O(1)-SPACE vs RECURSIVE O(N)-STACK LINKED LIST REVERSAL
========================================================================
Original Chain             : [10, 20, 30, 40, 50]
Iterative Reversal O(1)    : [50, 40, 30, 20, 10]
Recursive Reversal Back    : [10, 20, 30, 40, 50]
```

### Output — Example 2 (`example_02_reverse_between_sublist_one_pass.py`)
```text
========================================================================
1. REVERSE SUBLIST BETWEEN POSITIONS [LEFT .. RIGHT] (LEETCODE 92)
========================================================================
Original Chain (1..7)          : [10, 20, 30, 40, 50, 60, 70]
Reverse Between [left=2..5]    : [10, 50, 40, 30, 20, 60, 70] ([20,30,40,50] -> [50,40,30,20])
Reverse Between [left=1..3]    : [40, 50, 10, 30, 20, 60, 70]
```

### Output — Example 3 (`example_03_reverse_nodes_in_k_group.py`)
```text
========================================================================
1. REVERSE NODES IN K-GROUP IN O(1) SPACE (LEETCODE 25 HARD)
========================================================================
  Input [1..8], k = 2 -> [2, 1, 4, 3, 6, 5, 8, 7]
  Input [1..8], k = 3 -> [3, 2, 1, 6, 5, 4, 7, 8]
  Input [1..8], k = 4 -> [4, 3, 2, 1, 8, 7, 6, 5]
```

---

## 7. Code Explanation

1. **Why Dummy Sentinel is Mandatory in `reverse_between` and `reverse_k_group`:**
   When `left == 1` (or for the very first $k$-group), the original `head` of the linked list moves away from position 1. By attaching `dummy.next = head`, position 1 is treated identically to any interior sublist, and `dummy.next` automatically points to the new global head at the end.
2. **Initial `prev = group_next` in `reverse_k_group`:**
   In standard full-list reversal, we initialize `prev = None` because the old head becomes the new tail pointing to `None`. When reversing a $k$-group `[group_prev.next .. kth_node]`, initializing `prev = group_next` makes the first node of the group automatically point to `group_next` on the very first iteration of the inner loop!

---

## 8. Common Mistakes

1. **Overwriting `curr.next` Before Saving `nxt = curr.next`:**
   Writing `curr.next = prev` first permanently orphans the entire remaining suffix of the linked list.
2. **Forgetting `head.next = None` in Recursive Reversal:**
   After `head.next.next = head`, the first two nodes of the original list point to each other (`Node1 <-> Node2`), creating an infinite two-node cycle at the tail of the reversed list unless you explicitly set `head.next = None`.
3. **Returning `curr` Instead of `prev` After the Iterative Loop:**
   When `while curr is not None:` terminates, `curr` is guaranteed to be `None`. The new head is stored in `prev`.
4. **Using `sub_prev.next` Instead of `sub_tail.next` in One-Pass Sublist Reversal:**
   In the head-insertion loop, `sub_prev.next` changes on every iteration (it always points to the most recently pulled front node), whereas `sub_tail` stays fixed on the original `left`-th node as it slides rightward toward `right`.

---

## 9. Practice Questions

1. **Easy — Swap Nodes in Pairs (LeetCode 24):**
   Given a linked list, swap every two adjacent nodes in-place (changing links, not `.val` attributes) and return its head. Solve it both directly with a dummy node and by invoking `reverse_k_group(head, k=2)`.
2. **Medium — Double a Number Represented as a Linked List (LeetCode 2816):**
   Given the head of a non-empty linked list representing a non-negative integer without leading zeroes (most significant digit at `head`), reverse the list, multiply each digit by 2 with carry propagation in $O(1)$ space, and reverse it back.
3. **Hard — Reverse Nodes in Even Length Groups (LeetCode 2074):**
   Nodes are grouped sequentially into lengths $1, 2, 3, 4, \dots$ (the last group may be shorter). Reverse the nodes of each group whose actual node count is **even** in $O(n)$ time and $O(1)$ space.

---

## 10. Interview Questions

### Q1: Why is iterative reversal strongly preferred over recursive reversal in production Python?
**Answer:** Python does not perform Tail-Call Optimization (TCO) and enforces a default recursion limit (`sys.getrecursionlimit() == 1000`). Reversing a linked list of $5{,}000$ nodes recursively raises a `RecursionError` and consumes $O(n)$ stack frames, whereas iterative 3-pointer reversal runs in $O(1)$ auxiliary memory for lists of any size.

### Q2: Can you write the 4-line body of iterative linked list reversal in a single Python tuple-unpacking line? Is it recommended?
**Answer:** Yes: `curr.next, prev, curr = prev, curr, curr.next` (because Python evaluates the right-hand side tuple `(prev, curr, curr.next)` completely before assigning left-to-right). However, in interviews, writing the explicit 4-line block with `nxt = curr.next` is much clearer and less error-prone to explain on a whiteboard.

### Q3: In `reverse_k_group`, we walk $k$ steps to find `kth_node` and then walk $k$ steps again to reverse the group. Why is this still $O(n)$ time and not $O(n \cdot k)$?
**Answer:** Each node is visited at most **twice**: once by the lookahead pointer `kth_node` and once by the reversal pointer `curr`. Thus the total number of pointer steps across the entire list is bounded by $2n = O(n)$, independent of $k$.

