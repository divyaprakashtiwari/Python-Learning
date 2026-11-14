"""
Phase 6 - Section H.04: Level Order Traversal
Example 03: Level Averages and Connecting Next Right Pointers

Demonstrating:
1. Calculating the average value of nodes at each level.
2. Connecting Next Right Pointers in Each Node (Perfect Binary Tree) in O(1) space.
3. Connecting Next Right Pointers for arbitrary General Binary Trees.
"""

from collections import deque


class Node:
    """Tree node with left, right, and next right pointer."""
    def __init__(self, val=0, left=None, right=None, next=None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next


def average_of_levels(root):
    """
    Compute arithmetic average of values on each tree level.
    Time Complexity: O(n)
    Space Complexity: O(w)
    """
    if not root:
        return []

    averages = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        level_sum = 0

        for _ in range(level_size):
            node = queue.popleft()
            level_sum += node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        averages.append(level_sum / level_size)

    return averages


def connect_next_pointers_constant_space(root):
    """
    Populate each next pointer to point to its next right node.
    Works on arbitrary trees in O(n) time and O(1) auxiliary space using a dummy head.
    """
    if not root:
        return None

    curr = root

    while curr:
        dummy = Node(0)
        tail = dummy

        while curr:
            if curr.left:
                tail.next = curr.left
                tail = tail.next
            if curr.right:
                tail.next = curr.right
                tail = tail.next
            curr = curr.next

        # Advance to next level
        curr = dummy.next

    return root


def print_level_next_chains(root):
    """Print each level followed by its next pointers."""
    level_head = root
    level_idx = 0
    while level_head:
        curr = level_head
        vals = []
        while curr:
            vals.append(str(curr.val))
            curr = curr.next
        print(f"Level {level_idx}: {' -> '.join(vals)} -> None")

        # Find first non-null child for next level
        curr = level_head
        level_head = None
        while curr:
            if curr.left:
                level_head = curr.left
                break
            if curr.right:
                level_head = curr.right
                break
            curr = curr.next
        level_idx += 1


def main():
    print("=" * 60)
    print("1. Average of Levels")
    print("=" * 60)
    # Tree:
    #         3
    #        / \
    #       9   20
    #          /  \
    #         15   7
    root = Node(3)
    root.left = Node(9)
    root.right = Node(20, Node(15), Node(7))

    avg = average_of_levels(root)
    print("Averages per level:", avg)

    print("\n" + "=" * 60)
    print("2. Connect Next Right Pointers (O(1) Space)")
    print("=" * 60)
    connected_root = connect_next_pointers_constant_space(root)
    print_level_next_chains(connected_root)


if __name__ == "__main__":
    main()
