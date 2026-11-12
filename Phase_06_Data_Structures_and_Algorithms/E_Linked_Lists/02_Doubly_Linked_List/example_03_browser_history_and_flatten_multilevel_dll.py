"""
Phase 6 - Data Structures and Algorithms
Section E: Linked Lists - Topic 02: Doubly Linked List
Example 03: Browser History Navigation & Flattening a Multilevel Doubly Linked List

Demonstrates:
1. Browser History (LeetCode 1472): O(1) `visit(url)` (which truncates forward history in O(1)
   simply by dropping `curr.next = None`!) and step-by-step `back(steps)` / `forward(steps)`.
2. Flattening a Multilevel Doubly Linked List (LeetCode 430) in O(N) time and O(1) space
   by splicing each `.child` chain between `curr` and `curr.next`!
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class PageNode:
    url: str
    prev: PageNode | None = None
    next: PageNode | None = None


class BrowserHistoryDLL:
    """Browser back/forward history backed by a Doubly Linked List."""

    def __init__(self, homepage: str) -> None:
        self.curr = PageNode(homepage)

    def visit(self, url: str) -> None:
        """Visit `url` from current page, clearing all forward history in O(1) time!"""
        new_page = PageNode(url, prev=self.curr)
        self.curr.next = new_page
        self.curr = new_page

    def back(self, steps: int) -> str:
        while steps > 0 and self.curr.prev is not None:
            self.curr = self.curr.prev
            steps -= 1
        return self.curr.url

    def forward(self, steps: int) -> str:
        while steps > 0 and self.curr.next is not None:
            self.curr = self.curr.next
            steps -= 1
        return self.curr.url


@dataclass
class MultiLevelDNode:
    val: int
    prev: MultiLevelDNode | None = None
    next: MultiLevelDNode | None = None
    child: MultiLevelDNode | None = None


def flatten_multilevel_dll(head: MultiLevelDNode | None) -> list[int]:
    """
    Flatten a multilevel doubly linked list in-place in O(N) time and O(1) auxiliary space!
    Whenever `curr.child` is non-None, find the tail of the child list and splice
    `curr <-> child_head ... child_tail <-> original_next`.
    """
    curr = head
    while curr is not None:
        if curr.child is not None:
            child_head = curr.child
            # Find tail of the child chain
            child_tail = child_head
            while child_tail.next is not None:
                child_tail = child_tail.next

            # Splice child chain between `curr` and `curr.next`
            orig_next = curr.next
            curr.next = child_head
            child_head.prev = curr
            curr.child = None

            if orig_next is not None:
                child_tail.next = orig_next
                orig_next.prev = child_tail

        curr = curr.next

    # Collect values while asserting bidirectional `.prev`/`.next` integrity
    out: list[int] = []
    node = head
    while node is not None:
        if node.next is not None:
            assert node.next.prev is node, "Broken prev pointer!"
        out.append(node.val)
        node = node.next
    return out


if __name__ == "__main__":
    print("=" * 72)
    print("1. BROWSER HISTORY NAVIGATION (LEETCODE 1472)")
    print("=" * 72)
    bh = BrowserHistoryDLL("docs.python.org")
    bh.visit("github.com")
    bh.visit("leetcode.com")
    bh.visit("pypi.org")
    print(f"back(2)                -> {bh.back(2)}")
    print(f"forward(1)             -> {bh.forward(1)}")
    bh.visit("peps.python.org")  # Truncates pypi.org!
    print(f"visit('peps...'), forward(2) -> {bh.forward(2)} (Forward history cleared!)")
    print(f"back(2)                -> {bh.back(2)}")

    print("\n" + "=" * 72)
    print("2. FLATTEN A MULTILEVEL DOUBLY LINKED LIST IN O(1) SPACE (LC 430)")
    print("=" * 72)
    # Level 1: 1 <-> 2 <-> 3
    #                |
    # Level 2:       4 <-> 5
    n1, n2, n3 = MultiLevelDNode(1), MultiLevelDNode(2), MultiLevelDNode(3)
    n4, n5 = MultiLevelDNode(4), MultiLevelDNode(5)
    n1.next, n2.prev, n2.next, n3.prev = n2, n1, n3, n2
    n4.next, n5.prev = n5, n4
    n2.child = n4
    print(f"Flattened Multilevel Chain: {flatten_multilevel_dll(n1)}")

