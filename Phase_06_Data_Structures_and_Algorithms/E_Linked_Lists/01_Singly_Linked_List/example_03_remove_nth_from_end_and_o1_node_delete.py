"""
Phase 6 - Data Structures and Algorithms
Section E: Linked Lists - Topic 01: Singly Linked List
Example 03: Two-Pointer Gap Trick (Remove N-th Node From End in 1 Pass & O(1) Delete Given Only Node)

Demonstrates:
1. Removing the N-th Node From the End of a List in ONE Pass (LeetCode 19):
   Advance `fast` by `n + 1` steps ahead of `slow` (starting both at `dummy`).
   Then move `fast` and `slow` in lockstep until `fast` hits `None` -> `slow` sits right
   before the target node!
2. Deleting a non-tail node in O(1) time when given ONLY a reference to that node (LeetCode 237):
   Copy `node.next.val` into `node.val` and bypass `node.next`!
"""

from example_01_singly_linked_list_core_operations import ListNode
from example_02_dummy_sentinel_node_and_in_place_merge import from_list, to_list


def remove_nth_from_end_one_pass(head: ListNode | None, n: int) -> ListNode | None:
    """
    Remove the n-th node from the end of the list in a SINGLE O(L) pass and O(1) space.
    Uses `dummy` sentinel so even removing the very first node (`n == length`) works seamlessly!
    """
    dummy = ListNode(0, next=head)
    slow: ListNode = dummy
    fast: ListNode | None = dummy

    # 1. Advance `fast` by n + 1 steps to create a gap of n nodes between `slow` and `fast`
    for _ in range(n + 1):
        if fast is None:
            raise ValueError("n exceeds length of linked list")
        fast = fast.next

    # 2. Move `slow` and `fast` together until `fast` reaches the end (`None`)
    while fast is not None:
        slow = slow.next  # type: ignore[assignment]
        fast = fast.next

    # 3. `slow.next` is the exact n-th node from the end -> unlink it!
    if slow.next is not None:
        slow.next = slow.next.next

    return dummy.next


def delete_node_without_head_reference(target_node: ListNode) -> None:
    """
    Delete `target_node` (guaranteed not to be the tail) in O(1) time without access to `head`:
    Overwrite `target_node.val` with its successor's value and bypass `target_node.next`!
    """
    if target_node.next is None:
        raise ValueError("Cannot use O(1) value-copy trick on the tail node!")
    target_node.val = target_node.next.val
    target_node.next = target_node.next.next


if __name__ == "__main__":
    print("=" * 72)
    print("1. REMOVE N-TH NODE FROM END IN A SINGLE PASS (LEETCODE 19)")
    print("=" * 72)

    chain = from_list([10, 20, 30, 40, 50])
    print(f"Original Chain              : {to_list(chain)}")
    after_2nd = remove_nth_from_end_one_pass(chain, n=2)
    print(f"After removing 2nd from end : {to_list(after_2nd)} (40 removed)")
    after_head = remove_nth_from_end_one_pass(after_2nd, n=4)
    print(f"After removing 4th from end : {to_list(after_head)} (Head 10 removed)")

    print("\n" + "=" * 72)
    print("2. O(1) NODE DELETION GIVEN ONLY THE NODE REFERENCE (LEETCODE 237)")
    print("=" * 72)
    chain_2 = from_list([100, 200, 300, 400])
    node_200 = chain_2.next  # type: ignore[union-attr]
    delete_node_without_head_reference(node_200)  # type: ignore[arg-type]
    print(f"After O(1) delete(node_200) : {to_list(chain_2)}")

