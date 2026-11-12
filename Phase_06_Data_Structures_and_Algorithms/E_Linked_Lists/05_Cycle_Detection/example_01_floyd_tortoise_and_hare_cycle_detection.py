"""
Phase 6 - Data Structures and Algorithms
Section E: Linked Lists
Topic 05: Cycle Detection
Example 01: Floyd's Tortoise and Hare vs Hash Set Cycle Detection

Given the `head` of a singly linked list, determine whether the list contains a
cycle (a node whose `.next` pointer points back to an earlier node in the list).

We compare two approaches:
  1. Hash Set of Visited Node Identities (`id(node)`):
     - Time Complexity:  O(n)
     - Space Complexity: O(n) auxiliary memory
  2. Floyd's Cycle-Finding Algorithm (Tortoise & Hare):
     - `slow` advances 1 step per iteration (`slow = slow.next`).
     - `fast` advances 2 steps per iteration (`fast = fast.next.next`).
     - If there is no cycle, `fast` reaches `None` in n/2 steps.
     - If there is a cycle of length lambda, once `slow` enters the cycle, the distance
       between `fast` and `slow` along the cycle decreases by 1 on every step,
       guaranteeing a collision inside the cycle within at most lambda steps!
     - Time Complexity:  O(n)
     - Space Complexity: O(1) auxiliary memory
"""

from typing import List, Optional, Set, Tuple


class ListNode:
    """A node in a singly linked list."""

    def __init__(self, val: int) -> None:
        self.val: int = val
        self.next: Optional["ListNode"] = None


def build_linked_list_with_cycle(values: List[int], pos: int) -> Optional[ListNode]:
    """
    Builds a linked list from `values` where the tail's `.next` points back to
    the 0-indexed node at `pos` (or `None` if `pos == -1`).
    """
    if not values:
        return None
    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if 0 <= pos < len(nodes):
        nodes[-1].next = nodes[pos]
    return nodes[0]


def has_cycle_hash_set(head: Optional[ListNode]) -> bool:
    """Detects a cycle in O(n) time and O(n) space using a set of object IDs."""
    visited_ids: Set[int] = set()
    curr = head
    while curr is not None:
        node_id = id(curr)
        if node_id in visited_ids:
            return True
        visited_ids.add(node_id)
        curr = curr.next
    return False


def has_cycle_floyd_with_trace(head: Optional[ListNode]) -> Tuple[bool, List[str]]:
    """
    Detects a cycle in O(n) time and O(1) space using Floyd's Tortoise and Hare,
    recording each step of `slow` and `fast`.
    """
    trace: List[str] = []
    slow = head
    fast = head
    step = 0

    while fast is not None and fast.next is not None:
        step += 1
        slow = slow.next          # type: ignore[assignment]
        fast = fast.next.next
        assert slow is not None
        fast_str = str(fast.val) if fast is not None else "None"
        trace.append(f"Step {step}: slow={slow.val}, fast={fast_str}")
        if slow is fast:
            return True, trace

    return False, trace


if __name__ == "__main__":
    print("=" * 72)
    print("Floyd's Tortoise & Hare vs Hash Set Cycle Detection")
    print("=" * 72)

    test_cases = [
        ("Cyclic List (tail -> index 1 [val 20])", [10, 20, 30, 40, 50], 1),
        ("Self-Loop Single Node (pos = 0)", [99], 0),
        ("Acyclic List (pos = -1)", [1, 2, 3, 4, 5], -1),
        ("Empty List", [], -1),
    ]

    for label, vals, cycle_pos in test_cases:
        head_node = build_linked_list_with_cycle(vals, cycle_pos)
        set_res = has_cycle_hash_set(head_node)
        floyd_res, steps_trace = has_cycle_floyd_with_trace(head_node)
        assert set_res == floyd_res

        print(f"\nCase: {label}")
        print(f"  Values={vals}, cycle_pos={cycle_pos} -> Has Cycle: {floyd_res}")
        for line in steps_trace:
            print(f"    {line}")

