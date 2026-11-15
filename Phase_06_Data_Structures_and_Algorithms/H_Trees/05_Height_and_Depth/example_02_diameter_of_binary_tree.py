"""
Phase 6 - Section H.05: Height and Depth
Example 02: Diameter of Binary Tree and Maximum Path Sum

Demonstrating:
1. Diameter of Binary Tree (longest path between any two nodes, measured by number of edges).
2. Binary Tree Maximum Path Sum (nodes can have negative values; path can start and end anywhere).
"""


class TreeNode:
    """Standard Binary Tree Node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class TreeDiameter:
    """Computes diameter of binary tree using bottom-up height recursion."""

    def __init__(self):
        self.max_diameter = 0

    def diameter_of_binary_tree(self, root):
        """
        Calculates maximum path length (edges) between any two nodes.
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        self.max_diameter = 0

        def get_height(node):
            if not node:
                return 0
            left_h = get_height(node.left)
            right_h = get_height(node.right)

            # Longest path through this node has (left_h + right_h) edges
            self.max_diameter = max(self.max_diameter, left_h + right_h)

            return 1 + max(left_h, right_h)

        get_height(root)
        return self.max_diameter


class MaxPathSum:
    """Computes maximum path sum across any non-empty path."""

    def __init__(self):
        self.max_sum = float("-inf")

    def max_path_sum(self, root):
        """
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        self.max_sum = float("-inf")

        def gain_from_subtree(node):
            if not node:
                return 0

            # Ignore subtrees with negative gain by clamping to 0
            left_gain = max(gain_from_subtree(node.left), 0)
            right_gain = max(gain_from_subtree(node.right), 0)

            # Price of the new path where current node is the highest ancestor
            price_new_path = node.val + left_gain + right_gain
            self.max_sum = max(self.max_sum, price_new_path)

            # Return max gain the parent can obtain through this node
            return node.val + max(left_gain, right_gain)

        gain_from_subtree(root)
        return self.max_sum


def main():
    print("=" * 60)
    print("1. Diameter of Binary Tree")
    print("=" * 60)
    # Tree:
    #         1
    #        / \
    #       2   3
    #      / \
    #     4   5
    # Longest path: 4 -> 2 -> 1 -> 3 (3 edges) or 4 -> 2 -> 5 (2 edges) -> diameter = 3
    root = TreeNode(1)
    root.left = TreeNode(2, TreeNode(4), TreeNode(5))
    root.right = TreeNode(3)

    solver = TreeDiameter()
    print("Tree Diameter (Edges):", solver.diameter_of_binary_tree(root))

    print("\n" + "=" * 60)
    print("2. Binary Tree Maximum Path Sum")
    print("=" * 60)
    # Tree:
    #       -10
    #       /  \
    #      9   20
    #         /  \
    #        15   7
    # Max path: 15 -> 20 -> 7 = 42
    root_neg = TreeNode(-10)
    root_neg.left = TreeNode(9)
    root_neg.right = TreeNode(20, TreeNode(15), TreeNode(7))

    mps = MaxPathSum()
    print("Maximum Path Sum:", mps.max_path_sum(root_neg))


if __name__ == "__main__":
    main()
