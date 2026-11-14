"""
Phase 6 - Section H.04: Level Order Traversal
Example 01: Standard BFS and Zigzag (Spiral) Level Order Traversal

Demonstrating:
1. Standard Level Order Traversal grouping nodes level-by-level using deque.
2. Zigzag / Spiral Level Order Traversal alternating direction per level.
"""

from collections import deque


class TreeNode:
    """Standard Binary Tree Node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def level_order(root):
    """
    Standard Level Order Traversal (BFS).
    Time Complexity: O(n)
    Space Complexity: O(w) where w is max width of tree (up to n/2)
    """
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        current_level = []

        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(current_level)

    return result


def zigzag_level_order(root):
    """
    Zigzag / Spiral Level Order Traversal.
    Level 0: Left to Right
    Level 1: Right to Left
    Level 2: Left to Right, etc.
    Time Complexity: O(n)
    Space Complexity: O(w)
    """
    if not root:
        return []

    result = []
    queue = deque([root])
    left_to_right = True

    while queue:
        level_size = len(queue)
        current_level = deque()

        for _ in range(level_size):
            node = queue.popleft()
            if left_to_right:
                current_level.append(node.val)
            else:
                current_level.appendleft(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(list(current_level))
        left_to_right = not left_to_right

    return result


def main():
    print("=" * 60)
    print("Level Order & Zigzag Traversal")
    print("=" * 60)
    # Tree:
    #         3
    #        / \
    #       9   20
    #          /  \
    #         15   7
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20, TreeNode(15), TreeNode(7))

    standard = level_order(root)
    zigzag = zigzag_level_order(root)

    print("Standard Level Order:", standard)
    print("Zigzag Level Order  :", zigzag)


if __name__ == "__main__":
    main()
