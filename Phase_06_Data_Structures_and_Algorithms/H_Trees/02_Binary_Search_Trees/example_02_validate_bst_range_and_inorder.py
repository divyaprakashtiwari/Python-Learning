"""
Phase 6 - Section H.02: Binary Search Trees
Example 02: Validate Binary Search Tree

Demonstrating:
1. Validating BST using recursive bounding range (low, high).
2. Validating BST using iterative inorder traversal monotonicity.
3. Demonstration of common pitfalls (local checks vs global subtree bounds).
"""


class TreeNode:
    """Binary Search Tree Node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def is_valid_bst_range(root, low=float("-inf"), high=float("inf")):
    """
    Validate BST recursively using bounding intervals.
    Every node in left subtree must be < node.val.
    Every node in right subtree must be > node.val.
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    if root is None:
        return True

    if not (low < root.val < high):
        return False

    return (is_valid_bst_range(root.left, low, root.val) and
            is_valid_bst_range(root.right, root.val, high))


def is_valid_bst_inorder(root):
    """
    Validate BST using iterative inorder traversal.
    Elements must be strictly monotonically increasing.
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    stack = []
    curr = root
    prev_val = float("-inf")

    while stack or curr:
        while curr:
            stack.append(curr)
            curr = curr.left

        curr = stack.pop()
        if curr.val <= prev_val:
            return False
        prev_val = curr.val

        curr = curr.right

    return True


def main():
    print("=" * 60)
    print("1. Valid BST Verification")
    print("=" * 60)
    # Valid BST:
    #       5
    #      / \
    #     3   7
    #    / \   \
    #   2   4   8
    valid_tree = TreeNode(5)
    valid_tree.left = TreeNode(3, TreeNode(2), TreeNode(4))
    valid_tree.right = TreeNode(7, None, TreeNode(8))

    print("Valid Tree via Range Check  :", is_valid_bst_range(valid_tree))
    print("Valid Tree via Inorder Check:", is_valid_bst_inorder(valid_tree))

    print("\n" + "=" * 60)
    print("2. Invalid BST (The Local-Check Trap)")
    print("=" * 60)
    # Invalid BST where each node locally satisfies child check,
    # but global subtree property is violated (3 in right subtree of 5):
    #       5
    #      / \
    #     1   6
    #        / \
    #       3   7   <-- 3 < 5! Invalid right subtree of 5.
    invalid_tree = TreeNode(5)
    invalid_tree.left = TreeNode(1)
    invalid_tree.right = TreeNode(6, TreeNode(3), TreeNode(7))

    print("Invalid Tree via Range Check  :", is_valid_bst_range(invalid_tree))
    print("Invalid Tree via Inorder Check:", is_valid_bst_inorder(invalid_tree))


if __name__ == "__main__":
    main()
