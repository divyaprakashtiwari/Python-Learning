# Section E: Linked Lists — Topic 01: Singly Linked List

## 1. Introduction

A **Singly Linked List** is a dynamic linear data structure composed of heap-allocated **nodes**, where each `ListNode` stores two things:
1. **`val` (Data Payload):** The value stored in the node.
2. **`next` (Pointer / Reference):** A reference to the next `ListNode` in the chain (or `None` at the end of the list).

```
[head] -> [ 10 | * ] -> [ 20 | * ] -> [ 30 | * ] -> [ 40 | None ] <- [tail]
```

Unlike a contiguous array (`list`), linked list nodes can live at **any scattered addresses in memory**. You never have to pre-allocate capacity or shift elements when inserting/deleting at the front or splicing between known nodes!

---

## 2. Why is it used?

1. **Guaranteed $O(1)$ Worst-Case Front Insertion (`prepend`), Front Deletion (`pop_front`), and Tail Append:**
   In a dynamic array, `arr.insert(0, x)` and `arr.pop(0)` shift $N$ elements in **$O(N)$ time**, and `arr.append(x)` occasionally triggers an $O(N)$ resize copy. A Singly Linked List with `head` and `tail` pointers performs `prepend`, `pop_front`, and `append` in **strictly $O(1)$ worst-case time** (zero shifting, zero resizing).
2. **$O(1)$ Splicing and In-Place Merging:**
   Merging two sorted linked lists or moving a sub-chain of 1,000,000 nodes from one list to another requires relinking just **2 pointers** ($O(1)$ auxiliary memory!).
3. **Building Block of Hash Table Chains, Stacks, Queues, and Memory Allocators:**
   Separate-chaining hash tables, OS free-memory lists, and lock-free concurrent stacks are all built on Singly Linked Lists.

---

## 3. Syntax & Core Blueprints

### Blueprint 1: Node Definition & The Dummy (Sentinel) Head Pattern
```python
class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None) -> None:
        self.val = val
        self.next = next

def filter_linked_list(head: ListNode | None, target: int) -> ListNode | None:
    # Dummy node eliminates special `if head` branches when the head itself is deleted!
    dummy = ListNode(0, next=head)
    prev = dummy
    curr = head
    while curr is not None:
        if curr.val == target:
            prev.next = curr.next  # Unlink curr
        else:
            prev = curr
        curr = curr.next
    return dummy.next
```

---

## 4. Step-by-Step Explanation & Complexity Analysis

### Singly Linked List vs Dynamic Array (`list`) Complexity Comparison

| Operation | Dynamic Array (`list`) | Singly Linked List (with `head` & `tail`) | Why? |
| :--- | :--- | :--- | :--- |
| **Access by Index `i` (`arr[i]`)** | **$O(1)$** | $O(N)$ | Linked list must follow `i` `.next` pointers |
| **Insert at Front (`prepend`)** | $O(N)$ (shifts all) | **$O(1)$** | `new_node.next = head; head = new_node` |
| **Delete at Front (`pop_front`)** | $O(N)$ (`pop(0)`) | **$O(1)$** | `head = head.next` |
| **Insert at Back (`append`)** | $O(1)$ amortized | **$O(1)$** strict | `tail.next = new_node; tail = new_node` |
| **Delete at Back (`pop_back`)** | **$O(1)$** (`pop()`) | $O(N)$ | Must traverse from `head` to find node *before* `tail`! |
| **Delete After Known `node`** | $O(N)$ | **$O(1)$** | `node.next = node.next.next` |

### Why Deleting the Tail (`pop_back`) IsStill $O(N)$ Even With a `tail` Pointer!
To delete `tail`, you must set the **second-to-last node's `.next` to `None`** and update `tail` to point to that second-to-last node. Because pointers in a Singly Linked List are **one-way**, `tail` has no `.prev` pointer to its predecessor — you must walk all the way from `head` in $O(N)$ time! (Doubly Linked Lists fix this in Topic 02.)

---

## 5. Practical Examples (3 Complete Programs)

### Example 1: Core Operations — $O(1)$ `prepend`, `append`, and `pop_front` (`example_01_singly_linked_list_core_operations.py`)
```python
class SinglyLinkedList:
    def __init__(self) -> None:
        self.head: ListNode | None = None
        self.tail: ListNode | None = None
        self._size: int = 0

    def prepend(self, val: int) -> None:
        new_node = ListNode(val, next=self.head)
        self.head = new_node
        if self.tail is None:
            self.tail = new_node
        self._size += 1

    def append(self, val: int) -> None:
        new_node = ListNode(val)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1
```

### Example 2: Dummy Sentinel Node & In-Place Merge of Sorted Lists (`example_02_dummy_sentinel_node_and_in_place_merge.py`)
```python
def merge_two_sorted_linked_lists(
    l1: ListNode | None, l2: ListNode | None
) -> ListNode | None:
    dummy = ListNode(0)
    tail = dummy

    while l1 is not None and l2 is not None:
        if l1.val <= l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next

    tail.next = l1 if l1 is not None else l2
    return dummy.next
```

### Example 3: Remove $N$-th Node From End in 1 Pass & $O(1)$ Node Delete (`example_03_remove_nth_from_end_and_o1_node_delete.py`)
```python
def remove_nth_from_end_one_pass(head: ListNode | None, n: int) -> ListNode | None:
    dummy = ListNode(0, next=head)
    slow: ListNode = dummy
    fast: ListNode | None = dummy

    for _ in range(n + 1):
        if fast is None:
            raise ValueError("n exceeds length of linked list")
        fast = fast.next

    while fast is not None:
        slow = slow.next  # type: ignore[assignment]
        fast = fast.next

    if slow.next is not None:
        slow.next = slow.next.next

    return dummy.next
```

---

## 6. Verified Console Output

### Output of `example_01_singly_linked_list_core_operations.py`
```text
========================================================================
1. SINGLY LINKED LIST O(1) PREPEND, APPEND, AND POP_FRONT
========================================================================
After append(20, 30, 40) : 20 -> 30 -> 40 -> None (len=3)
After prepend(10), (5)   : 5 -> 10 -> 20 -> 30 -> 40 -> None (len=5)
After pop_front() ->  5  : 10 -> 20 -> 30 -> 40 -> None (len=4)
```

### Output of `example_02_dummy_sentinel_node_and_in_place_merge.py`
```text
========================================================================
1. DUMMY HEAD PATTERN: REMOVE ALL OCCURRENCES (INCLUDING HEAD!)
========================================================================
Original : [6, 6, 1, 2, 6, 3, 4, 5, 6]
Remove 6 : [1, 2, 3, 4, 5]
Remove 7 from [7, 7, 7] -> []

========================================================================
2. MERGE TWO SORTED LINKED LISTS IN O(1) AUXILIARY SPACE
========================================================================
Merged Chain : [10, 20, 30, 30, 40, 50, 60, 70, 80]
```

### Output of `example_03_remove_nth_from_end_and_o1_node_delete.py`
```text
========================================================================
1. REMOVE N-TH NODE FROM END IN A SINGLE PASS (LEETCODE 19)
========================================================================
Original Chain              : [10, 20, 30, 40, 50]
After removing 2nd from end : [10, 20, 30, 50] (40 removed)
After removing 4th from end : [20, 30, 50] (Head 10 removed)

========================================================================
2. O(1) NODE DELETION GIVEN ONLY THE NODE REFERENCE (LEETCODE 237)
========================================================================
After O(1) delete(node_200) : [100, 300, 400]
```

---

## 7. Code Explanation

1. **Why the Dummy Sentinel Head (`dummy = ListNode(0, next=head)`) Is a Superpower:**
   In `remove_all_occurrences` and `remove_nth_from_end_one_pass`, what if the node to be removed is the **first node (`head`)** itself? Without `dummy`, `head` has no predecessor `prev`, forcing you to write a separate `while head and head.val == target: head = head.next` loop. By placing `dummy` before `head`, `head` now has a predecessor (`dummy`), and `return dummy.next` returns the new head (or `None` if all nodes were removed)!
2. **How the Two-Pointer Gap Trick (`n + 1` steps ahead) Works in 1 Pass:**
   When `fast` starts at `dummy` and advances `n + 1` steps, the distance between `slow` and `fast` is `n + 1` links. When `fast` reaches `None` (1 past the tail), `slow` sits `n + 1` steps before `None` — which is the **exact predecessor** of the $n$-th node from the end!

---

## 8. Common Mistakes

1. **Losing the Rest of the Chain by Overwriting `.next` Too Early:**
   If you write `prev.next = new_node` before `new_node.next = prev.next`, `new_node.next` points to **itself** (creating an infinite 1-node cycle) and the entire suffix of the list is lost! Always wire the **new node's outgoing pointer first** (`new_node.next = prev.next`), then update `prev.next = new_node`.
2. **Advancing `prev = curr` Even When `curr` Was Just Deleted:**
   In `remove_all_occurrences`, if `curr.val == target`, we set `prev.next = curr.next`. At that moment, `prev` is **still** the predecessor of the next surviving node! If you advance `prev = curr` after deleting `curr`, consecutive duplicates like `[6, 6]` will leave the second `6` in the list!

---

## 9. Practice Questions

1. **Easy — Remove Duplicates from Sorted Linked List (LeetCode 83):** Given the `head` of a sorted linked list, delete all duplicates such that each element appears only once in $O(N)$ time and $O(1)$ space.
2. **Medium — Add Two Numbers Represented as Reversed Linked Lists (LeetCode 2):** Given two non-empty linked lists representing two non-negative integers in reverse digit order, return their sum as a linked list (handling `carry` properly, including a final `carry == 1` after both lists end!).
3. **Hard — Partition List Around Pivot $X$ Preserving Relative Order (LeetCode 86):** Given a linked list and a value `x`, partition it in $O(N)$ time and $O(1)$ auxiliary space using two dummy heads (`less_dummy` and `greater_equal_dummy`), splicing the two chains together at the end (and setting `greater_tail.next = None` to prevent a cycle!).

---

## 10. Interview Questions

### Q1: In Partition List (or Odd-Even Linked List), why is forgetting `greater_tail.next = None` at the end one of the most common causes of `Time Limit Exceeded` (infinite loop)?
**Answer:**
Because you are reusing existing nodes in-place without allocating new ones, the last node added to the `greater` chain (`greater_tail`) might not have been the last node of the original list — its `.next` pointer may still point back to a node in the `less` chain! Explicitly terminating `greater_tail.next = None` breaks that stale link.

### Q2: Why does the $O(1)$ "copy next node's value and bypass `node.next`" deletion trick (LeetCode 237) fail if `target_node` is the last (tail) node?
**Answer:**
To turn `target_node` into a clone of its successor, a successor (`target_node.next`) must exist! If `target_node` is the tail (`target_node.next is None`), there is no next node to copy from, and setting `target_node = None` only reassigns the local variable without modifying the predecessor's `.next` pointer.

