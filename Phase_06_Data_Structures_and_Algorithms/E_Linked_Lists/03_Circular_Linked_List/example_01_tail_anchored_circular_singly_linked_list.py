"""
Phase 6 - Data Structures and Algorithms
Section E: Linked Lists
Topic 03: Circular Linked List
Example 01: Tail-Anchored Circular Singly Linked List (O(1) Head and Tail Ops)

Why maintain a `tail` pointer instead of a `head` pointer in a Circular Singly Linked List?
- If we only store `head`, inserting at the head or tail requires finding the last
  node (to update its `.next` pointer), which takes O(n) traversal.
- If we store `tail` instead:
  - The head node is simply `tail.next` (accessible in O(1) time!).
  - `prepend(val)` (insert at head) is O(1): insert right after `tail`.
  - `append(val)` (insert at tail) is O(1): insert right after `tail`, then advance `tail`.
  - `pop_front()` (remove head) is O(1): bypass `tail.next`.

We also demonstrate splitting a Circular Linked List into two halves in O(n) time
using the Fast and Slow pointer technique.
"""

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
            new_node.next = new_node  # Points to itself
            self.tail = new_node
        else:
            new_node.next = self.tail.next  # Point to old head
            self.tail.next = new_node       # Tail now points to new head
        self._size += 1

    def append(self, val: Any) -> None:
        """Inserts `val` at the back (tail) in O(1) time."""
        self.prepend(val)
        # Advancing `tail` to the newly prepended node moves it from head to tail!
        assert self.tail is not None
        self.tail = self.tail.next

    def pop_front(self) -> Any:
        """Removes and returns the head element in O(1) time."""
        if self.tail is None:
            raise IndexError("pop_front from an empty circular linked list")

        head = self.tail.next
        assert head is not None
        if head is self.tail:
            # Single-node circular list becomes empty
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

    # Aliases used by Round-Robin & Josephus examples
    insert_back = append
    rotate_forward = rotate_clockwise

    def to_list(self) -> List[Any]:
        """Traverses the ring exactly once from head (`tail.next`) to `tail`."""
        if self.tail is None:
            return []
        result: List[Any] = []
        curr = self.tail.next  # Start at head
        while True:
            assert curr is not None
            result.append(curr.val)
            if curr is self.tail:
                break
            curr = curr.next
        return result


CircularSinglyLinkedList = TailAnchoredCircularLinkedList


def split_circular_list_in_halves(head: Optional[CNode]) -> Tuple[Optional[CNode], Optional[CNode]]:
    """
    Splits a circular singly linked list starting at `head` into two separate
    circular singly linked lists of sizes ceil(n/2) and floor(n/2).

    Time Complexity:  O(n) using slow and fast pointers
    Space Complexity: O(1)
    """
    if head is None or head.next is head:
        return head, None

    slow: CNode = head
    fast: CNode = head

    # Advance slow by 1 and fast by 2 until fast reaches the end of the ring
    while fast.next is not head and fast.next.next is not head:
        slow = slow.next          # type: ignore[assignment]
        fast = fast.next.next     # type: ignore[assignment]

    # If the list has an even number of nodes, move `fast` one step to the true tail
    if fast.next.next is head:
        fast = fast.next          # type: ignore[assignment]

    head1 = head
    head2 = slow.next

    # Close the first circular half: slow becomes tail of half 1
    slow.next = head1
    # Close the second circular half: fast becomes tail of half 2
    fast.next = head2

    return head1, head2


def circular_head_to_list(head: Optional[CNode]) -> List[Any]:
    """Helper to convert a raw circular `head` reference into a Python list."""
    if head is None:
        return []
    out: List[Any] = []
    curr: CNode = head
    while True:
        out.append(curr.val)
        curr = curr.next  # type: ignore[assignment]
        if curr is head:
            break
    return out


if __name__ == "__main__":
    print("=" * 72)
    print("1. Tail-Anchored Circular Singly Linked List (O(1) Head & Tail Ops)")
    print("=" * 72)

    cll = TailAnchoredCircularLinkedList()
    for val in [20, 30, 40]:
        cll.append(val)
    cll.prepend(10)
    cll.append(50)

    assert cll.tail is not None and cll.tail.next is not None
    print(f"After prepend(10) & append(20..50): {cll.to_list()}")
    print(f"  Head (tail.next) = {cll.tail.next.val}, Tail = {cll.tail.val}, Size = {len(cll)}")

    cll.rotate_clockwise(2)
    print(f"After rotate_clockwise(2):          {cll.to_list()}")
    print(f"  New Head = {cll.tail.next.val}, New Tail = {cll.tail.val}")

    popped = cll.pop_front()
    print(f"After pop_front() -> {popped}:            {cll.to_list()}")

    print("\n" + "=" * 72)
    print("2. Splitting a Circular Linked List into Two Circular Halves")
    print("=" * 72)

    for values in [[1, 2, 3, 4, 5], [10, 20, 30, 40, 50, 60]]:
        ring = TailAnchoredCircularLinkedList()
        for v in values:
            ring.append(v)
        assert ring.tail is not None
        raw_head = ring.tail.next
        h1, h2 = split_circular_list_in_halves(raw_head)
        print(f"Original Ring ({len(values)} nodes): {values}")
        print(f"  First Circular Half  : {circular_head_to_list(h1)}")
        print(f"  Second Circular Half : {circular_head_to_list(h2)}")
