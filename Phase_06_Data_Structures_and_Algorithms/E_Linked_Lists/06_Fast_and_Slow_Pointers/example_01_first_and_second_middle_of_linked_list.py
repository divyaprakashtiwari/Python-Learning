"""
Phase 6 - Data Structures and Algorithms
Section E: Linked Lists
Topic 06: Fast and Slow Pointers
Example 01: First Middle vs Second Middle of a Singly Linked List

When a list has an ODD number of nodes (e.g., 5 nodes: indices 0, 1, 2, 3, 4),
there is a single unambiguous middle node (index 2).
When a list has an EVEN number of nodes (e.g., 6 nodes: indices 0, 1, 2, 3, 4, 5),
there are TWO middle nodes:
  - First Middle (Left-Biased Middle, index 2):
    Required when splitting a list for Merge Sort or Reorder List / Palindrome List
    so that the first half does not swallow an extra node on size-2 lists!
    Loop condition: `while fast.next is not None and fast.next.next is not None:`
  - Second Middle (Right-Biased Middle, index 3):
    Required by LeetCode 876 (Middle of the Linked List).
    Loop condition: `while fast is not None and fast.next is not None:`

We also show how to delete the middle node (LeetCode 2095) in a single pass.
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


def find_first_middle(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Returns the left-biased middle node (index (n - 1) // 2).
    Essential before splitting a list into two halves for Merge Sort or Palindrome check.
    """
    if head is None:
        return None
    slow: ListNode = head
    fast: ListNode = head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next          # type: ignore[assignment]
        fast = fast.next.next
    return slow


def find_second_middle(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Returns the right-biased middle node (index n // 2, LeetCode 876).
    """
    if head is None:
        return None
    slow: Optional[ListNode] = head
    fast: Optional[ListNode] = head
    while fast is not None and fast.next is not None:
        assert slow is not None
        slow = slow.next
        fast = fast.next.next
    return slow


def delete_middle_node(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Deletes the middle node (index n // 2) in one pass and returns the modified head
    (LeetCode 2095). By starting `fast` one jump ahead (`head.next.next`), `slow`
    stops at the exact predecessor of the node to delete!
    """
    if head is None or head.next is None:
        return None

    slow: ListNode = head
    fast: Optional[ListNode] = head.next.next

    while fast is not None and fast.next is not None:
        slow = slow.next          # type: ignore[assignment]
        fast = fast.next.next

    # `slow` is now the predecessor of the middle node
    assert slow.next is not None
    slow.next = slow.next.next
    return head


if __name__ == "__main__":
    print("=" * 72)
    print("First Middle (Left-Biased) vs Second Middle (Right-Biased) & Delete Mid")
    print("=" * 72)

    for vals in [[10, 20, 30, 40, 50], [10, 20, 30, 40, 50, 60], [100, 200], [42]]:
        h = from_list(vals)
        first_mid = find_first_middle(h)
        second_mid = find_second_middle(h)
        after_del = to_list(delete_middle_node(from_list(vals)))

        print(f"\nList ({len(vals)} nodes): {vals}")
        print(f"  First Middle  (idx {(len(vals)-1)//2}): {first_mid.val if first_mid else None}")
        print(f"  Second Middle (idx {len(vals)//2}): {second_mid.val if second_mid else None}")
        print(f"  After delete_middle_node() : {after_del}")

