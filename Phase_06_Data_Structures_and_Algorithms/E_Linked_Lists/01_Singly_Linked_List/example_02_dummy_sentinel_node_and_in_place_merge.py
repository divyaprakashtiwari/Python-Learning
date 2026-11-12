"""
Phase 6 - Data Structures and Algorithms
Section E: Linked Lists - Topic 01: Singly Linked List
Example 02: The Dummy (Sentinel) Head Pattern (Delete by Value, Remove All Occurrences, & Merge)

Demonstrates:
1. Why Linked List interview code often gets messy with `if head is None` or `if head.val == target`
   special cases when the `head` node itself is deleted or replaced.
2. How creating a `dummy = ListNode(0, next=head)` sentinel node unifies `head` with every
   other node so `prev.next = curr.next` works identically everywhere, returning `dummy.next`!
3. Merging Two Sorted Linked Lists in-place in O(N + M) time and O(1) auxiliary space!
"""

from example_01_singly_linked_list_core_operations import ListNode


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


def remove_all_occurrences(head: ListNode | None, target: int) -> ListNode | None:
    """
    Remove ALL nodes with `node.val == target` (LeetCode 203) in O(N) time and O(1) space.
    The `dummy` sentinel node handles even the case where the first several nodes (or ALL nodes)
    equal `target` without a single special `if` branch!
    """
    dummy = ListNode(0, next=head)
    prev = dummy
    curr = head

    while curr is not None:
        if curr.val == target:
            prev.next = curr.next  # Bypass `curr`; do NOT advance `prev`!
        else:
            prev = curr
        curr = curr.next

    return dummy.next


def merge_two_sorted_linked_lists(
    l1: ListNode | None, l2: ListNode | None
) -> ListNode | None:
    """
    Merge two sorted linked lists in-place by relinking `.next` pointers (LeetCode 21).
    Time Complexity : O(N + M)
    Space Complexity: O(1) auxiliary space (zero new heap nodes allocated!)
    """
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


if __name__ == "__main__":
    print("=" * 72)
    print("1. DUMMY HEAD PATTERN: REMOVE ALL OCCURRENCES (INCLUDING HEAD!)")
    print("=" * 72)

    head_1 = from_list([6, 6, 1, 2, 6, 3, 4, 5, 6])
    cleaned = remove_all_occurrences(head_1, target=6)
    print(f"Original : [6, 6, 1, 2, 6, 3, 4, 5, 6]")
    print(f"Remove 6 : {to_list(cleaned)}")

    head_all = from_list([7, 7, 7])
    print(f"Remove 7 from [7, 7, 7] -> {to_list(remove_all_occurrences(head_all, 7))}")

    print("\n" + "=" * 72)
    print("2. MERGE TWO SORTED LINKED LISTS IN O(1) AUXILIARY SPACE")
    print("=" * 72)
    a = from_list([10, 30, 50, 70])
    b = from_list([20, 30, 40, 60, 80])
    merged = merge_two_sorted_linked_lists(a, b)
    print(f"Merged Chain : {to_list(merged)}")

