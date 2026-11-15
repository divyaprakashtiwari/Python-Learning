"""
Phase 6 - Section H.07: Balanced Trees
Example 01: Check if Binary Tree is Height-Balanced

Demonstrating:
1. Naive O(n^2) top-down height comparison.
2. Optimal O(n) bottom-up post-order check using -1 sentinel on imbalance.
"""


class TreeNode:
    """Standard Binary Tree Node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def is_balanced_naive(root):
    """
    Naive top-down check: calculates height at every node.
    Time Complexity: O(n^2) worst case on skewed trees, O(n log n) balanced.
    """
    def height(node):
        if not node:
            return 0
        return 1 + max(height(node.left), height(node.right))

    if not root:
        return True

    left_h = height(root.left)
    right_h = height(root.right)

    return (abs(left_h - right_h) <= 1 and
            is_balanced_naive(root.left) and
            is_balanced_naive(root.right))


def is_balanced_optimal(root):
    """
    Optimal bottom-up post-order check:
    Returns actual height if balanced; returns -1 immediately if any subtree is unbalanced.
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    def check_height(node):
        if not node:
            return 0

        left_h = check_height(node.left)
        if left_h == -1:
            return -1

        right_h = check_height(node.right)
        if right_h == -1:
            return -1

        if abs(left_h - right_h) > 1:
            return -1

        return 1 + max(left_h, right_h)

    return check_height(root) != -1


def main():
    print("=" * 60)
    print("Balanced Binary Tree Verification")
    print("=" * 60)
    # Balanced tree:
    #         3
    #        / \
    #       9  20
    #          / \
    #         15  7
    root_balanced = TreeNode(3)
    root_balanced.left = TreeNode(9)
    root_balanced.right = TreeNode(20, TreeNode(15), TreeNode(7))

    print("Tree 1 (Balanced):")
    print("  Naive check   :", is_balanced_naive(root_balanced))
    print("  Optimal check :", is_balanced_optimal(root_balanced))

    # Unbalanced tree:
    #         1
    #        / \
    #       2   2
    #      / \
    #     3   3
    #    / \
    #   4   4
    root_unbalanced = TreeNode(1)
    n3 = TreeNode(3, TreeNode(4), TreeNode(4))
    root_unbalanced.left = TreeNode(2, n3, TreeNode(3))
    root_unbalanced.right = TreeNode(2)

    print("\nTree 2 (Unbalanced):")
    print("  Naive check   :", is_balanced_naive(root_unbalanced))
    print("  Optimal check :", is_balanced_optimal(root_unbalanced))


if __name__ == "__main__":
    main()
