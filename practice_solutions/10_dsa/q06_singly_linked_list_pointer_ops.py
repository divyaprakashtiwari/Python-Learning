"""
Question 6: Singly Linked List In-Place Pointer Manipulation & Floyd's Cycle Detection
Topic: Data Structures & Algorithms (DSA)

Key Concepts Tested:
- Node-based Singly Linked List architecture (without list backing)
- In-place iterative reversal using 3 pointers (prev, curr, next_node)
- Tortoise and Hare fast/slow pointer middle node search
- Floyd's cycle detection and entry point discovery
- In-place sorted linked list merging using dummy head splicing
"""

from typing import TypeVar, Generic, Optional, List, Tuple

T = TypeVar("T")


class ListNode(Generic[T]):
    """Individual linked list node."""

    def __init__(self, val: T, next_node: Optional["ListNode[T]"] = None) -> None:
        self.val = val
        self.next = next_node

    def __repr__(self) -> str:
        return f"ListNode({self.val})"


class SinglyLinkedList(Generic[T]):
    """
    Singly linked list providing pointer-based mutations, reversal,
    middle element retrieval, and cycle detection.
    """

    def __init__(self) -> None:
        self.head: Optional[ListNode[T]] = None

    def append(self, val: T) -> None:
        """Inserts a new node at the tail."""
        new_node = ListNode(val)
        if not self.head:
            self.head = new_node
            return

        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node

    def prepend(self, val: T) -> None:
        """Inserts a new node at the head in O(1) time."""
        self.head = ListNode(val, next_node=self.head)

    def delete_value(self, val: T) -> bool:
        """Deletes the first occurrence of val. Returns True if deleted, else False."""
        if not self.head:
            return False

        if self.head.val == val:
            self.head = self.head.next
            return True

        curr = self.head
        while curr.next and curr.next.val != val:
            curr = curr.next

        if curr.next:
            curr.next = curr.next.next
            return True

        return False

    def to_list(self) -> List[T]:
        """Converts linked list into a standard Python list (traversing up to 1000 nodes if circular)."""
        elements: List[T] = []
        curr = self.head
        visited = set()
        while curr and id(curr) not in visited:
            visited.add(id(curr))
            elements.append(curr.val)
            curr = curr.next
        return elements

    def reverse(self) -> None:
        """Reverses the linked list in-place in O(N) time and O(1) auxiliary space."""
        prev: Optional[ListNode[T]] = None
        curr = self.head

        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node

        self.head = prev

    def find_middle(self) -> Optional[T]:
        """
        Finds the middle node value using fast and slow pointers in a single pass.
        For even lengths, returns the second middle node.
        """
        if not self.head:
            return None

        slow: Optional[ListNode[T]] = self.head
        fast: Optional[ListNode[T]] = self.head

        while fast and fast.next:
            slow = slow.next  # type: ignore[union-attr]
            fast = fast.next.next

        return slow.val if slow else None

    def detect_cycle(self) -> Tuple[bool, Optional[T]]:
        """
        Floyd's Cycle Finding Algorithm:
        Detects if a cycle exists and locates the entry point of the loop.
        """
        if not self.head or not self.head.next:
            return (False, None)

        slow = self.head
        fast = self.head

        has_cycle = False
        while fast and fast.next:
            slow = slow.next  # type: ignore[assignment]
            fast = fast.next.next
            if slow is fast:
                has_cycle = True
                break

        if not has_cycle:
            return (False, None)

        # Locate cycle entry point: reset one pointer to head
        entry_ptr = self.head
        while entry_ptr is not slow:
            entry_ptr = entry_ptr.next  # type: ignore[assignment]
            slow = slow.next  # type: ignore[assignment]

        return (True, entry_ptr.val)


def build_linked_list(items: List[T]) -> Optional[ListNode[T]]:
    """Helper creating a node chain from a list."""
    dummy = ListNode(None)  # type: ignore[arg-type]
    curr = dummy
    for item in items:
        curr.next = ListNode(item)
        curr = curr.next
    return dummy.next


def linked_list_to_list(head: Optional[ListNode[T]]) -> List[T]:
    """Helper converting node chain to a Python list."""
    res = []
    curr = head
    while curr:
        res.append(curr.val)
        curr = curr.next
    return res


def merge_sorted_lists(l1: Optional[ListNode[int]], l2: Optional[ListNode[int]]) -> Optional[ListNode[int]]:
    """
    Merges two sorted linked lists in-place by updating pointer references.
    """
    dummy = ListNode(0)
    tail = dummy

    curr1 = l1
    curr2 = l2

    while curr1 and curr2:
        if curr1.val <= curr2.val:
            tail.next = curr1
            curr1 = curr1.next
        else:
            tail.next = curr2
            curr2 = curr2.next
        tail = tail.next

    tail.next = curr1 if curr1 else curr2
    return dummy.next


if __name__ == "__main__":
    # 1. SLL Appending, Middle Node, and In-place Reversal
    sll = SinglyLinkedList[int]()
    for x in [10, 20, 30, 40, 50]:
        sll.append(x)

    mid_val = sll.find_middle()
    print(f"Middle Node of [10, 20, 30, 40, 50]: {mid_val}")

    sll.reverse()
    reversed_list = sll.to_list()
    print(f"Reversed Linked List: {reversed_list}")

    # 2. Cycle Detection with Floyd's Algorithm
    cycle_sll = SinglyLinkedList[int]()
    for x in [1, 2, 3, 4, 5]:
        cycle_sll.append(x)

    # Artificially create cycle connecting node 5 back to node 3
    node_3 = cycle_sll.head.next.next  # type: ignore[union-attr]
    tail_node = node_3.next.next  # type: ignore[union-attr]
    tail_node.next = node_3  # type: ignore[union-attr]

    has_cycle, cycle_entry = cycle_sll.detect_cycle()
    print(f"Cycle Detected: {has_cycle}, Cycle Entry Node Value: {cycle_entry}")

    # 3. Merge Two Sorted Lists In-Place
    l1 = build_linked_list([1, 3, 5])
    l2 = build_linked_list([2, 4, 6])
    merged_head = merge_sorted_lists(l1, l2)
    merged_list = linked_list_to_list(merged_head)
    print(f"Merged Sorted List: {merged_list}")

    # 4. Edge Cases: Empty list & Single node
    empty_sll = SinglyLinkedList[int]()
    print(f"Empty list middle: {empty_sll.find_middle()}")
    empty_sll.reverse()
    print(f"Empty list reversed: {empty_sll.to_list()}")
    print(f"Empty list cycle: {empty_sll.detect_cycle()}")
