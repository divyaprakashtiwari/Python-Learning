"""
Phase 6 - Data Structures and Algorithms
Section E: Linked Lists - Topic 04: Reversal
Example 01: Iterative 3-Pointer Reversal vs Recursive Linked List Reversal

Demonstrates:
1. Iterative Linked List Reversal (`prev`, `curr`, `next_temp` 3-pointer pattern):
   - Time Complexity : O(N)
   - Space Complexity: O(1) auxiliary memory (the gold standard for production & interviews!)
2. Recursive Linked List Reversal (`head.next.next = head; head.next = None`):
   - Time Complexity : O(N)
   - Space Complexity: O(N) call-stack frames.
"""

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
    """
    Reverse a singly linked list in-place iteratively using 3 pointers (`prev`, `curr`, `nxt`).
    Time Complexity : O(N)
    Space Complexity: O(1)
    """
    prev: ListNode | None = None
    curr: ListNode | None = head

    while curr is not None:
        nxt = curr.next     # 1. Save reference to the rest of the chain!
        curr.next = prev    # 2. Reverse current node's pointer backward to `prev`
        prev = curr         # 3. Advance `prev` one step forward
        curr = nxt          # 4. Advance `curr` one step forward

    return prev             # `prev` now points to the new head!


def reverse_linked_list_recursive(head: ListNode | None) -> ListNode | None:
    """
    Reverse a singly linked list recursively.
    Time Complexity : O(N)
    Space Complexity: O(N) recursion call stack
    """
    # Base case: empty list or single node is its own reversal
    if head is None or head.next is None:
        return head

    # Reverse the suffix starting at `head.next`; `new_head` is the original tail
    new_head = reverse_linked_list_recursive(head.next)

    # Make `head.next` point backward to `head`, and clear `head.next`!
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

