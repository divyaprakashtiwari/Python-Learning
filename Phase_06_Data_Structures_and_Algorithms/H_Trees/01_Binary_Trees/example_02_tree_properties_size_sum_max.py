"""
Phase 6 - Section H.01: Binary Trees
Example 02: Recursive Tree Properties (Size, Sum, Max, Leaf Count)

Demonstrating:
1. Tree size (total number of nodes).
2. Sum of all node values.
3. Maximum value in a binary tree.
4. Count of leaf nodes (nodes with 0 children).
"""


class TreeNode:
    """Standard Binary Tree Node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def tree_size(root):
    """
    Count total number of nodes in the binary tree.
    Time Complexity: O(n)
    Space Complexity: O(h) call stack
    """
    if root is None:
        return 0
    return 1 + tree_size(root.left) + tree_size(root.right)


def tree_sum(root):
    """
    Calculate the sum of all node values.
    Time Complexity: O(n)
    """
    if root is None:
        return 0
    return root.val + tree_sum(root.left) + tree_sum(root.right)


def tree_max(root):
    """
    Find maximum value in the binary tree.
    Time Complexity: O(n)
    """
    if root is None:
        return float("-inf")
    return max(root.val, tree_max(root.left), tree_max(root.right))


def count_leaves(root):
    """
    Count the number of leaf nodes (nodes without left or right children).
    Time Complexity: O(n)
    """
    if root is None:
        return 0
    if root.left is None and root.right is None:
        return 1
    return count_leaves(root.left) + count_leaves(root.right)


def main():
    print("=" * 60)
    print("Recursive Tree Metrics")
    print("=" * 60)
    # Tree:
    #         10
    #        /  \
    #       5    15
    #      / \     \
    #     2   7     20
    root = TreeNode(10)
    root.left = TreeNode(5, TreeNode(2), TreeNode(7))
    root.right = TreeNode(15, None, TreeNode(20))

    total_nodes = tree_size(root)
    sum_vals = tree_sum(root)
    maximum = tree_max(root)
    num_leaves = count_leaves(root)

    print("Nodes:", [10, 5, 15, 2, 7, 20])
    print("Total Nodes (Size) :", total_nodes)
    print("Sum of All Values  :", sum_vals)
    print("Maximum Value      :", maximum)
    print("Number of Leaves   :", num_leaves)


if __name__ == "__main__":
    main()

