"""
Phase 6 - Data Structures and Algorithms
Section E: Linked Lists - Topic 02: Doubly Linked List
Example 01: Sentinel-Bounded Doubly Linked List (O(1) Front/Back Insert, Delete, & Arbitrary Node Unlink)

Demonstrates:
1. Why a Doubly Linked List (`prev` and `next` pointers on every node) solves the fatal
   weakness of a Singly Linked List:
   - `pop_back()` (deleting the tail) is now strictly O(1) instead of O(N)!
   - `unlink_node(node)` (removing ANY node given its reference, INCLUDING the tail!) is
     strictly O(1) because `node.prev` is immediately available!
2. Using Dummy `head_sentinel` and `tail_sentinel` boundary nodes so `insert_between` and
   `unlink_node` NEVER have `if node.prev is None` or `if node.next is None` branches!
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class DListNode:
    val: int
    prev: DListNode | None = None
    next: DListNode | None = None


class DoublyLinkedList:
    """
    Production-grade Doubly Linked List using `head_sentinel` and `tail_sentinel`
    guard nodes so every real node ALWAYS has a non-None `prev` and `next`!
    """

    def __init__(self) -> None:
        self.head_sentinel = DListNode(0)
        self.tail_sentinel = DListNode(0)
        self.head_sentinel.next = self.tail_sentinel
        self.tail_sentinel.prev = self.head_sentinel
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def _insert_between(
        self, val: int, left_node: DListNode, right_node: DListNode
    ) -> DListNode:
        """Insert a new node between `left_node` and `right_node` in strictly O(1) time."""
        node = DListNode(val, prev=left_node, next=right_node)
        left_node.next = node
        right_node.prev = node
        self._size += 1
        return node

    def unlink_node(self, node: DListNode) -> int:
        """Unlink ANY real `node` from the list in strictly O(1) time."""
        if node is self.head_sentinel or node is self.tail_sentinel:
            raise ValueError("Cannot unlink sentinel guard nodes!")
        left_node = node.prev
        right_node = node.next
        assert left_node is not None and right_node is not None
        left_node.next = right_node
        right_node.prev = left_node
        node.prev = node.next = None
        self._size -= 1
        return node.val

    def append_left(self, val: int) -> DListNode:
        """Insert at front in O(1) time."""
        assert self.head_sentinel.next is not None
        return self._insert_between(val, self.head_sentinel, self.head_sentinel.next)

    def append_right(self, val: int) -> DListNode:
        """Insert at back in O(1) time."""
        assert self.tail_sentinel.prev is not None
        return self._insert_between(val, self.tail_sentinel.prev, self.tail_sentinel)

    def pop_left(self) -> int:
        """Remove and return front element in O(1) time."""
        if self._size == 0:
            raise IndexError("pop_left from empty DoublyLinkedList")
        assert self.head_sentinel.next is not None
        return self.unlink_node(self.head_sentinel.next)

    def pop_right(self) -> int:
        """Remove and return back (tail) element in O(1) time!"""
        if self._size == 0:
            raise IndexError("pop_right from empty DoublyLinkedList")
        assert self.tail_sentinel.prev is not None
        return self.unlink_node(self.tail_sentinel.prev)

    def to_list_forward(self) -> list[int]:
        out: list[int] = []
        curr = self.head_sentinel.next
        while curr is not None and curr is not self.tail_sentinel:
            out.append(curr.val)
            curr = curr.next
        return out

    def to_list_backward(self) -> list[int]:
        out: list[int] = []
        curr = self.tail_sentinel.prev
        while curr is not None and curr is not self.head_sentinel:
            out.append(curr.val)
            curr = curr.prev
        return out


if __name__ == "__main__":
    print("=" * 72)
    print("1. SENTINEL-BOUNDED DOUBLY LINKED LIST O(1) OPERATIONS")
    print("=" * 72)

    dll = DoublyLinkedList()
    n20 = dll.append_right(20)
    n30 = dll.append_right(30)
    n40 = dll.append_right(40)
    dll.append_left(10)

    print(f"Forward Traversal      : {dll.to_list_forward()} (len={len(dll)})")
    print(f"Backward Traversal     : {dll.to_list_backward()}")

    # Unlink middle node `n30` directly in O(1) time!
    dll.unlink_node(n30)
    print(f"After O(1) unlink(n30) : {dll.to_list_forward()}")
    print(f"After O(1) pop_right() -> {dll.pop_right()}: {dll.to_list_forward()}")

