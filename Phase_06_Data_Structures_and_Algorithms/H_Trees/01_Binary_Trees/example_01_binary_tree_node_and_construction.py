"""
Phase 6 - Section H.01: Binary Trees
Example 01: Binary Tree Node Representation and Construction

Demonstrating:
1. TreeNode definition with left and right child pointers.
2. Manual tree construction and basic visualization.
3. Verification of tree properties: Full, Degenerate (Skewed), and Perfect binary trees.
"""


class TreeNode:
    """Standard Binary Tree Node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def is_full_binary_tree(root):
    """
    Check if tree is full (every node has either 0 or 2 children).
    """
    if root is None:
        return True
    if root.left is None and root.right is None:
        return True
    if root.left is not None and root.right is not None:
        return is_full_binary_tree(root.left) and is_full_binary_tree(root.right)
    return False


def is_degenerate(root):
    """
    Check if tree is degenerate/skewed (every parent node has exactly 1 child).
    """
    if root is None or (root.left is None and root.right is None):
        return True
    if root.left is not None and root.right is not None:
        return False
    return is_degenerate(root.left if root.left else root.right)


def print_tree_structure(root, prefix="", is_left=True):
    """Pretty-print a binary tree visually in text."""
    if root is not None:
        print(prefix + ("|-- " if is_left else "\\-- ") + str(root.val))
        next_prefix = prefix + ("|   " if is_left else "    ")
        if root.left or root.right:
            if root.left:
                print_tree_structure(root.left, next_prefix, True)
            else:
                print(next_prefix + "|-- None")
            if root.right:
                print_tree_structure(root.right, next_prefix, False)
            else:
                print(next_prefix + "\\-- None")


def main():
    print("=" * 60)
    print("1. Manual Binary Tree Construction")
    print("=" * 60)
    # Constructing:
    #        1
    #       / \
    #      2   3
    #     / \
    #    4   5
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)

    print("Tree Hierarchy:")
    print_tree_structure(root)

    print("\n" + "=" * 60)
    print("2. Tree Classifications")
    print("=" * 60)
    print("Is Full Binary Tree:", is_full_binary_tree(root))
    print("Is Degenerate Tree :", is_degenerate(root))

    # Skewed tree: 1 -> 2 -> 3 -> 4
    skewed = TreeNode(1, right=TreeNode(2, right=TreeNode(3, right=TreeNode(4))))
    print("\nSkewed Tree Hierarchy:")
    print_tree_structure(skewed)
    print("Is Skewed Degenerate Tree:", is_degenerate(skewed))


if __name__ == "__main__":
    main()

