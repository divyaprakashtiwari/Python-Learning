"""
Phase 6 - Data Structures and Algorithms
Section E: Linked Lists
Topic 06: Fast and Slow Pointers
Example 02: Palindrome Linked List in O(n) Time and O(1) Auxiliary Space
            (with List Restoration)

How do we check if a singly linked list is a palindrome without allocating an O(n)
array or O(n) recursion stack (LeetCode 234)?
  1. Find the First Middle (`slow`) using Fast and Slow pointers.
  2. Reverse the second half of the list (`slow.next`) in-place.
  3. Compare the first half and the reversed second half node-by-node.
  4. **Production Best Practice:** Reverse the second half a second time and
     re-attach it to `slow.next` so the caller's linked list is restored intact!

We also solve **Maximum Twin Sum of a Linked List** (LeetCode 2130) using the same
pattern.
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


def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """Reverses a singly linked list in-place in O(n) time and O(1) space."""
    prev: Optional[ListNode] = None
    curr = head
    while curr is not None:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev


def is_palindrome_linked_list(head: Optional[ListNode]) -> bool:
    """
    Checks whether `head` is a palindrome in O(n) time and O(1) space,
    restoring the original list structure before returning.
    """
    if head is None or head.next is None:
        return True

    # Step 1: Locate the end of the first half (First Middle)
    slow: ListNode = head
    fast: ListNode = head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next          # type: ignore[assignment]
        fast = fast.next.next

    # Step 2: Reverse the second half in-place
    second_half_head = reverse_list(slow.next)

    # Step 3: Compare both halves
    p1: Optional[ListNode] = head
    p2: Optional[ListNode] = second_half_head
    is_pal = True
    while p2 is not None:
        assert p1 is not None
        if p1.val != p2.val:
            is_pal = False
            break
        p1 = p1.next
        p2 = p2.next

    # Step 4: Restore the original list before returning!
    slow.next = reverse_list(second_half_head)
    return is_pal


def max_twin_sum(head: Optional[ListNode]) -> int:
    """
    In a linked list of even length `n`, the i-th node (0-indexed) is the twin of
    the (n - 1 - i)-th node. Computes the maximum twin sum in O(n) time and O(1) space.
    """
    if head is None:
        return 0

    slow: ListNode = head
    fast: ListNode = head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next          # type: ignore[assignment]
        fast = fast.next.next

    second_half = reverse_list(slow.next)
    best = 0
    p1: Optional[ListNode] = head
    p2: Optional[ListNode] = second_half
    while p2 is not None:
        assert p1 is not None
        best = max(best, p1.val + p2.val)
        p1 = p1.next
        p2 = p2.next

    slow.next = reverse_list(second_half)
    return best


if __name__ == "__main__":
    print("=" * 72)
    print("1. O(1) Space Palindrome Linked List (with Structure Restoration)")
    print("=" * 72)

    test_lists = [
        [1, 2, 3, 2, 1],
        [10, 20, 20, 10],
        [1, 2, 3, 4],
        [7],
    ]
    for vals in test_lists:
        head_node = from_list(vals)
        res = is_palindrome_linked_list(head_node)
        restored = to_list(head_node)
        assert restored == vals, "Original list must be restored!"
        print(f"Input: {str(vals):<18} -> Palindrome: {str(res):<5} | Restored: {restored}")

    print("\n" + "=" * 72)
    print("2. Maximum Twin Sum of an Even-Length Linked List (LeetCode 2130)")
    print("=" * 72)
    twin_input = [5, 4, 2, 1, 10, 3]
    h_twin = from_list(twin_input)
    print(f"List: {twin_input} -> Max Twin Sum (4 + 10 = 14): {max_twin_sum(h_twin)}")

