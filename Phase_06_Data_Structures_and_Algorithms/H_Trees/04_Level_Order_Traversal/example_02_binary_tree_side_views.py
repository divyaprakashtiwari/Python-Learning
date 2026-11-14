"""
Phase 6 - Section H.04: Level Order Traversal
Example 02: Binary Tree Side Views (Right View, Left View, Top View)

Demonstrating:
1. Right Side View of Binary Tree via BFS (last element in each level queue).
2. Left Side View of Binary Tree via BFS (first element in each level queue).
3. Top View of Binary Tree using vertical column coordinate mapping.
"""

from collections import deque


class TreeNode:
    """Standard Binary Tree Node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def right_side_view(root):
    """
    Return values of nodes visible from the right side.
    Time Complexity: O(n)
    Space Complexity: O(w)
    """
    if not root:
        return []

    view = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if i == level_size - 1:  # Last node of current level
                view.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return view


def left_side_view(root):
    """
    Return values of nodes visible from the left side.
    Time Complexity: O(n)
    Space Complexity: O(w)
    """
    if not root:
        return []

    view = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if i == 0:  # First node of current level
                view.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return view


def top_view(root):
    """
    Return values visible from top of the tree sorted by horizontal column distance.
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    if not root:
        return []

    col_map = {}  # col -> first seen val
    # Queue stores (node, col)
    queue = deque([(root, 0)])

    while queue:
        node, col = queue.popleft()
        if col not in col_map:
            col_map[col] = node.val

        if node.left:
            queue.append((node.left, col - 1))
        if node.right:
            queue.append((node.right, col + 1))

    # Sort columns from leftmost to rightmost
    return [col_map[c] for c in sorted(col_map.keys())]


def main():
    print("=" * 60)
    print("Binary Tree Views")
    print("=" * 60)
    # Tree:
    #         1
    #        / \
    #       2   3
    #        \   \
    #         5   4
    root = TreeNode(1)
    root.left = TreeNode(2, None, TreeNode(5))
    root.right = TreeNode(3, None, TreeNode(4))

    right_v = right_side_view(root)
    left_v = left_side_view(root)
    top_v = top_view(root)

    print("Right Side View :", right_v)
    print("Left Side View  :", left_v)
    print("Top View        :", top_v)


if __name__ == "__main__":
    main()
