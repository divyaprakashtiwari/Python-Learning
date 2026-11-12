"""
Phase 6 - Data Structures and Algorithms
Section E: Linked Lists - Topic 04: Reversal
Example 02: Reverse Sublist Between Positions [Left .. Right] in 1 Pass (Head-Insertion Splice)

Demonstrates:
1. Reverse Linked List II (LeetCode 92):
   Given 1-based positions `left` and `right`, reverse ONLY the nodes from position `left`
   to position `right` in a SINGLE O(N) pass and O(1) auxiliary space!
2. The "Head-Insertion (Tail-Pulling) Trick":
   Keep `sub_prev` anchored right before position `left` and `sub_tail` anchored on the
   original `left`-th node. For `right - left` iterations, pull `sub_tail.next` to the front
   right after `sub_prev`!
"""

from example_01_iterative_and_recursive_linked_list_reversal import (
    ListNode,
    from_list,
    to_list,
)


def reverse_between_one_pass(
    head: ListNode | None, left: int, right: int
) -> ListNode | None:
    """
    Reverse the nodes of the list from 1-based position `left` to `right` in one pass.
    Time Complexity : O(N)
    Space Complexity: O(1)
    """
    if head is None or left == right:
        return head

    dummy = ListNode(0, next=head)
    sub_prev: ListNode = dummy

    # 1. Walk `sub_prev` to the node immediately BEFORE position `left` (left - 1 steps)
    for _ in range(left - 1):
        assert sub_prev.next is not None
        sub_prev = sub_prev.next

    # `sub_tail` is the first node of the sublist (which will end up at the tail of the sublist)
    sub_tail = sub_prev.next
    assert sub_tail is not None

    # 2. Repeatedly pull `move_node = sub_tail.next` and insert it right after `sub_prev`!
    for _ in range(right - left):
        move_node = sub_tail.next
        assert move_node is not None
        sub_tail.next = move_node.next
        move_node.next = sub_prev.next
        sub_prev.next = move_node

    return dummy.next


if __name__ == "__main__":
    print("=" * 72)
    print("1. REVERSE SUBLIST BETWEEN POSITIONS [LEFT .. RIGHT] (LEETCODE 92)")
    print("=" * 72)

    chain = from_list([10, 20, 30, 40, 50, 60, 70])
    print(f"Original Chain (1..7)          : {to_list(chain)}")

    res = reverse_between_one_pass(chain, left=2, right=5)
    print(f"Reverse Between [left=2..5]    : {to_list(res)} ([20,30,40,50] -> [50,40,30,20])")

    # Edge case: reversing from left=1 (includes original head!)
    res_head = reverse_between_one_pass(res, left=1, right=3)
    print(f"Reverse Between [left=1..3]    : {to_list(res_head)}")

