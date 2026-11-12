"""
Phase 6 - Data Structures and Algorithms
Section E: Linked Lists - Topic 04: Reversal
Example 03: Reverse Nodes in k-Group (LeetCode 25 Hard) & Swap Nodes in Pairs

Demonstrates:
1. Reverse Nodes in k-Group (LeetCode 25 Hard):
   Reverses the linked list `k` nodes at a time in O(N) time and O(1) space.
   If the number of remaining nodes at the end is NOT a multiple of `k`, those `< k` nodes
   are left in their original order!
2. Swap Nodes in Pairs (LeetCode 24) as the special case `k = 2`.
"""

from example_01_iterative_and_recursive_linked_list_reversal import (
    ListNode,
    from_list,
    to_list,
)


def reverse_k_group(head: ListNode | None, k: int) -> ListNode | None:
    """
    Reverse nodes of a linked list `k` at a time in O(N) time and strictly O(1) space.
    Leftover nodes (< k at the end) remain as-is.
    """
    if head is None or k <= 1:
        return head

    dummy = ListNode(0, next=head)
    group_prev: ListNode = dummy

    while True:
        # 1. Check if at least `k` nodes remain ahead of `group_prev`
        kth_node: ListNode | None = group_prev
        for _ in range(k):
            assert kth_node is not None
            kth_node = kth_node.next
            if kth_node is None:
                return dummy.next  # Fewer than k nodes left -> done!

        group_next = kth_node.next  # First node of the NEXT group

        # 2. Reverse the current k-node group `[group_prev.next .. kth_node]`
        prev: ListNode | None = group_next
        curr: ListNode | None = group_prev.next
        while curr is not group_next:
            assert curr is not None
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        # 3. Connect `group_prev` to `kth_node` (the new front of this group)
        #    and advance `group_prev` to `old_group_head` (now the tail of this group!)
        old_group_head = group_prev.next
        assert old_group_head is not None
        group_prev.next = kth_node
        group_prev = old_group_head


if __name__ == "__main__":
    print("=" * 72)
    print("1. REVERSE NODES IN K-GROUP IN O(1) SPACE (LEETCODE 25 HARD)")
    print("=" * 72)

    for k_val in [2, 3, 4]:
        sample = from_list([1, 2, 3, 4, 5, 6, 7, 8])
        reversed_k = reverse_k_group(sample, k=k_val)
        print(f"  Input [1..8], k = {k_val} -> {to_list(reversed_k)}")

