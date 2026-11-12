"""
Phase 6 - Data Structures and Algorithms
Section E: Linked Lists - Topic 01: Singly Linked List
Example 01: Singly Linked List Node & Core Operations (O(1) Head/Tail Insert & Head Delete)

Demonstrates:
1. Why a Singly Linked List with both `head` and `tail` pointers supports:
   - `prepend(val)` (insert at head) in strictly O(1) time (vs O(N) in an array!).
   - `append(val)` (insert at tail) in strictly O(1) time (with zero resize spikes!).
   - `pop_front()` (delete at head) in strictly O(1) time (vs O(N) `list.pop(0)`!).
2. Why `insert_at(index, val)` and `pop_back()` (deleting the tail in a SINGLY linked list)
   still require O(N) pointer traversal!
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class ListNode:
    val: int
    next: ListNode | None = None


class SinglyLinkedList:
    """Singly Linked List maintaining `head`, `tail`, and `_size`."""

    def __init__(self) -> None:
        self.head: ListNode | None = None
        self.tail: ListNode | None = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def prepend(self, val: int) -> None:
        """Insert `val` at the front (`head`) in strictly O(1) time."""
        new_node = ListNode(val, next=self.head)
        self.head = new_node
        if self.tail is None:
            self.tail = new_node
        self._size += 1

    def append(self, val: int) -> None:
        """Insert `val` at the back (`tail`) in strictly O(1) time."""
        new_node = ListNode(val)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def pop_front(self) -> int:
        """Remove and return the head element in strictly O(1) time."""
        if self.head is None:
            raise IndexError("pop_front from empty SinglyLinkedList")
        removed_val = self.head.val
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self._size -= 1
        return removed_val

    def to_list(self) -> list[int]:
        out: list[int] = []
        curr = self.head
        while curr is not None:
            out.append(curr.val)
            curr = curr.next
        return out

    def format_chain(self) -> str:
        return " -> ".join(str(x) for x in self.to_list()) + " -> None"


if __name__ == "__main__":
    print("=" * 72)
    print("1. SINGLY LINKED LIST O(1) PREPEND, APPEND, AND POP_FRONT")
    print("=" * 72)

    sll = SinglyLinkedList()
    for x in [20, 30, 40]:
        sll.append(x)
    print(f"After append(20, 30, 40) : {sll.format_chain()} (len={len(sll)})")

    sll.prepend(10)
    sll.prepend(5)
    print(f"After prepend(10), (5)   : {sll.format_chain()} (len={len(sll)})")

    popped = sll.pop_front()
    print(f"After pop_front() -> {popped:>2}  : {sll.format_chain()} (len={len(sll)})")

