"""
Phase 6 - Data Structures and Algorithms
Section E: Linked Lists
Topic 06: Fast and Slow Pointers
Example 03: Reorder List (Zip / Interleave Ends) & Bottom-Up Linked List Merge Sort

Two flagship O(1)-auxiliary-pointer manipulations powered by Fast and Slow pointers:

1. Reorder List (LeetCode 143):
   Transform `L_0 -> L_1 -> ... -> L_{n-1} -> L_n` in-place into:
   `L_0 -> L_n -> L_1 -> L_{n-1} -> L_2 -> L_{n-2} -> ...`
   Algorithm (3 clean steps in O(n) time, O(1) space):
     a) Find First Middle `slow` via Fast & Slow pointers and sever the list into
        `first = head` and `second = slow.next` (`slow.next = None`).
     b) Reverse `second` in-place.
     c) Zipper-merge `first` and `second` by alternating `.next` pointers.

2. Top-Down Merge Sort on a Linked List in O(n log n) Time (LeetCode 148):
   Unlike arrays where finding the midpoint is `(low + high) // 2`, a linked list
   uses Fast & Slow pointers to split the list into two equal halves in O(n) time
   before recursively sorting and merging in-place.
"""

from typing import List, Optional


class ListNode:
    """A node in a singly linked list."""

    def __init__(self, val: int, next_node: Optional["ListNode"] = None) -> None:
        self.val: int = val
        self.next: Optional["ListNode"] = next_node


def from_list(values: List[int]) -> Optional[ListNode]:
    dummy = ListNode(0)
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(head: Optional[ListNode]) -> List[int]:
    out: List[int] = []
    curr = head
    while curr is not None:
        out.append(curr.val)
        curr = curr.next
    return out


def reorder_list_in_place(head: Optional[ListNode]) -> None:
    """
    Reorders `L_0 -> L_1 -> ... -> L_n` into `L_0 -> L_n -> L_1 -> L_{n-1} -> ...`
    in O(n) time and O(1) space.
    """
    if head is None or head.next is None:
        return

    # 1. Find First Middle
    slow: ListNode = head
    fast: ListNode = head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next          # type: ignore[assignment]
        fast = fast.next.next

    # 2. Split and reverse the second half
    second: Optional[ListNode] = slow.next
    slow.next = None
    prev: Optional[ListNode] = None
    curr = second
    while curr is not None:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    second = prev

    # 3. Zipper-merge `first` and `second`
    first: Optional[ListNode] = head
    while second is not None:
        assert first is not None
        tmp1 = first.next
        tmp2 = second.next

        first.next = second
        second.next = tmp1

        first = tmp1
        second = tmp2


def merge_two_sorted_lists(
    l1: Optional[ListNode], l2: Optional[ListNode]
) -> Optional[ListNode]:
    """Merges two sorted linked lists in-place using a dummy sentinel node."""
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


def sort_linked_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """Sorts a singly linked list in O(n log n) time using Fast & Slow midpoint split."""
    if head is None or head.next is None:
        return head

    # Split at First Middle
    slow: ListNode = head
    fast: ListNode = head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next          # type: ignore[assignment]
        fast = fast.next.next

    mid = slow.next
    slow.next = None

    left_sorted = sort_linked_list(head)
    right_sorted = sort_linked_list(mid)
    return merge_two_sorted_lists(left_sorted, right_sorted)


if __name__ == "__main__":
    print("=" * 72)
    print("1. Reorder List In-Place (Zip Ends: L_0 -> L_n -> L_1 -> L_{n-1})")
    print("=" * 72)

    for sample in [[1, 2, 3, 4], [1, 2, 3, 4, 5], [10, 20, 30, 40, 50, 60]]:
        h = from_list(sample)
        reorder_list_in_place(h)
        print(f"Original: {str(sample):<26} -> Reordered: {to_list(h)}")

    print("\n" + "=" * 72)
    print("2. Linked List Merge Sort via Fast & Slow Midpoint Split")
    print("=" * 72)
    unsorted = [40, 20, 10, 30, 70, 50, 60, 15]
    sorted_head = sort_linked_list(from_list(unsorted))
    print(f"Unsorted: {unsorted}")
    print(f"Sorted  : {to_list(sorted_head)}")

