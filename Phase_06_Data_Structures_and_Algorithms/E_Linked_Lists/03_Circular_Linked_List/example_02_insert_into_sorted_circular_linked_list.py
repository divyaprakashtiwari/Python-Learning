"""
Phase 6 - Data Structures and Algorithms
Section E: Linked Lists
Topic 03: Circular Linked List
Example 02: Insert into a Sorted Circular Linked List (All 4 Edge Cases)

Given a node reference `entry` pointing to an arbitrary node in a non-decreasing
sorted Circular Singly Linked List, insert a new value `insert_val` such that the
circular list remains sorted.

Why is this a classic interview favorite (LeetCode 708)?
Because `entry` is NOT guaranteed to be the minimum head node, and there are four
distinct cases to handle cleanly in a single circular pass:
  Case 0: The list is empty (`entry is None`) -> create a single self-looping node.
  Case 1: `prev.val <= insert_val <= curr.val` -> normal middle insertion between
          two sorted adjacent nodes.
  Case 2: `prev.val > curr.val` (the wrap-around cliff from maximum tail back to
          minimum head) AND (`insert_val >= prev.val` OR `insert_val <= curr.val`)
          -> `insert_val` is a new global maximum or new global minimum!
  Case 3: All nodes in the ring have identical values (e.g., `3 -> 3 -> 3 -> (back)`)
          and we complete a full 360-degree revolution back to `entry` without
          triggering Case 1 or Case 2 -> insert anywhere (right after `prev`).

Time Complexity:  O(n)
Space Complexity: O(1)
"""

from typing import List, Optional


class Node:
    """A node in a sorted circular singly linked list."""

    def __init__(self, val: int, next_node: Optional["Node"] = None) -> None:
        self.val: int = val
        self.next: Optional["Node"] = next_node


def insert_into_sorted_circular_list(entry: Optional[Node], insert_val: int) -> Node:
    """
    Inserts `insert_val` into a sorted circular linked list given an arbitrary
    node `entry`, returning the `entry` node (or the new node if `entry` was None).
    """
    new_node = Node(insert_val)

    # Case 0: Empty list -> create a 1-node ring pointing to itself
    if entry is None:
        new_node.next = new_node
        return new_node

    prev: Node = entry
    curr: Node = entry.next  # type: ignore[assignment]

    while True:
        # Case 1: Normal sorted interval where prev.val <= insert_val <= curr.val
        if prev.val <= insert_val <= curr.val:
            break

        # Case 2: At the wrap-around cliff where max tail (prev) meets min head (curr)
        if prev.val > curr.val:
            if insert_val >= prev.val or insert_val <= curr.val:
                break

        prev = curr
        curr = curr.next  # type: ignore[assignment]

        # Case 3: Completed a full revolution (all nodes are uniform values)
        if prev is entry:
            break

    # Splice `new_node` between `prev` and `curr`
    prev.next = new_node
    new_node.next = curr
    return entry


def circular_to_list_from(entry: Optional[Node]) -> List[int]:
    """Returns values starting from `entry` around the ring once."""
    if entry is None:
        return []
    result: List[int] = []
    curr: Node = entry
    while True:
        result.append(curr.val)
        curr = curr.next  # type: ignore[assignment]
        if curr is entry:
            break
    return result


if __name__ == "__main__":
    print("=" * 72)
    print("Insert into a Sorted Circular Linked List (All 4 Edge Cases)")
    print("=" * 72)

    # Case 0: Insert into empty list
    entry_node: Optional[Node] = None
    entry_node = insert_into_sorted_circular_list(entry_node, 10)
    print(f"Case 0 (Empty List -> insert 10)        : {circular_to_list_from(entry_node)}")

    # Add 20 and 30 so our sorted ring is [10 -> 20 -> 30 -> (back to 10)]
    insert_into_sorted_circular_list(entry_node, 20)
    insert_into_sorted_circular_list(entry_node, 30)
    # Move entry_node to 20 (an arbitrary middle node, not the minimum!)
    entry_node = entry_node.next
    print(f"Initial Ring (anchored at arbitrary 20) : {circular_to_list_from(entry_node)}")

    # Case 1: Normal middle insertion (25 fits between 20 and 30)
    insert_into_sorted_circular_list(entry_node, 25)
    print(f"Case 1 (Middle insert 25)               : {circular_to_list_from(entry_node)}")

    # Case 2a: New global minimum (5 fits at the cliff 30 -> 10)
    insert_into_sorted_circular_list(entry_node, 5)
    print(f"Case 2a (New global minimum 5)          : {circular_to_list_from(entry_node)}")

    # Case 2b: New global maximum (40 fits at the cliff 30 -> 5)
    insert_into_sorted_circular_list(entry_node, 40)
    print(f"Case 2b (New global maximum 40)         : {circular_to_list_from(entry_node)}")

    # Case 3: Uniform ring [7 -> 7 -> 7] where we insert 9
    uniform_entry: Optional[Node] = None
    for _ in range(3):
        uniform_entry = insert_into_sorted_circular_list(uniform_entry, 7)
    print(f"\nUniform Ring before insert              : {circular_to_list_from(uniform_entry)}")
    insert_into_sorted_circular_list(uniform_entry, 9)
    print(f"Case 3 (Uniform ring -> insert 9)       : {circular_to_list_from(uniform_entry)}")

