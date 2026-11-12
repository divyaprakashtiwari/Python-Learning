"""
Phase 6 - Data Structures and Algorithms
Section E: Linked Lists
Topic 05: Cycle Detection
Example 02: Finding Exact Cycle Entry Node (mu), Cycle Length (lambda), and Unlinking

Why does resetting one pointer to `head` after collision and moving both at speed 1
always meet at the exact cycle entry node (LeetCode 142)?

Mathematical Proof:
  - Let `mu` be the number of edges from `head` to the cycle entry node.
  - Let `lambda` be the length (number of nodes) of the cycle.
  - Let `k` be the distance from the cycle entry node to the collision point where
    `slow` and `fast` first meet.
  - When they collide:
      Distance traveled by `slow` = mu + k
      Distance traveled by `fast` = mu + k + m * lambda   (for some integer m >= 1)
  - Since `fast` moves at exactly twice the speed of `slow`:
      2 * (mu + k) = mu + k + m * lambda
      => mu + k = m * lambda
      => mu = m * lambda - k = (m - 1) * lambda + (lambda - k)
  - Notice that `(lambda - k)` is the exact remaining distance from the collision
    point forward along the cycle back to the cycle entry node!
  - Therefore, starting `ptr1` at `head` (distance `mu` from entry) and `ptr2` at
    the collision point (distance `lambda - k` from entry, plus `m - 1` full laps)
    at 1 step per iteration guarantees they collide at the EXACT cycle entry node!

Time Complexity:  O(n)
Space Complexity: O(1)
"""

from typing import List, Optional, Tuple


class ListNode:
    """A node in a singly linked list."""

    def __init__(self, val: int) -> None:
        self.val: int = val
        self.next: Optional["ListNode"] = None


def build_cyclic_list(values: List[int], pos: int) -> Optional[ListNode]:
    if not values:
        return None
    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if 0 <= pos < len(nodes):
        nodes[-1].next = nodes[pos]
    return nodes[0]


def analyze_and_remove_cycle(
    head: Optional[ListNode],
) -> Tuple[Optional[ListNode], int, int]:
    """
    Finds the cycle entry node, computes `mu` (tail-lead length before cycle) and
    `lambda` (cycle length), and breaks the cycle by setting the cycle tail's
    `.next` pointer back to `None`.

    Returns `(entry_node, mu, lambda_len)` or `(None, 0, 0)` if acyclic.
    """
    slow = head
    fast = head

    # Phase 1: Detect collision inside the cycle
    while fast is not None and fast.next is not None:
        slow = slow.next          # type: ignore[assignment]
        fast = fast.next.next
        if slow is fast:
            break
    else:
        return None, 0, 0

    # Phase 2: Find the exact cycle entry node and count `mu`
    ptr1 = head
    ptr2 = slow
    mu = 0
    while ptr1 is not ptr2:
        assert ptr1 is not None and ptr2 is not None
        ptr1 = ptr1.next
        ptr2 = ptr2.next
        mu += 1

    entry_node = ptr1
    assert entry_node is not None

    # Phase 3: Walk around the cycle once to measure `lambda` and locate cycle tail
    cycle_tail = entry_node
    lambda_len = 1
    while cycle_tail.next is not entry_node:
        assert cycle_tail.next is not None
        cycle_tail = cycle_tail.next
        lambda_len += 1

    # Break the cycle cleanly in O(1)
    cycle_tail.next = None

    return entry_node, mu, lambda_len


def to_list(head: Optional[ListNode]) -> List[int]:
    out: List[int] = []
    curr = head
    while curr is not None:
        out.append(curr.val)
        curr = curr.next
    return out


if __name__ == "__main__":
    print("=" * 72)
    print("Cycle Entry Node (mu), Cycle Length (lambda), and Cycle Removal")
    print("=" * 72)

    cases = [
        ([10, 20, 30, 40, 50, 60, 70], 2),
        ([100, 200, 300, 400], 0),
        ([5, 15, 25], 2),
        ([1, 2, 3, 4], -1),
    ]

    for vals, pos in cases:
        head_node = build_cyclic_list(vals, pos)
        entry, mu_val, lambda_val = analyze_and_remove_cycle(head_node)
        print(f"\nInput List: {vals} with tail connected to pos={pos}")
        if entry is None:
            print("  Result: Acyclic list (no cycle detected)")
        else:
            print(
                f"  Cycle Entry Node = {entry.val} (mu = {mu_val} steps from head, "
                f"cycle length lambda = {lambda_val})"
            )
            print(f"  After unlinking cycle tail -> Acyclic List: {to_list(head_node)}")

