"""
Phase 6 - Section H.06: Lowest Common Ancestor
Example 02: LCA in a Binary Search Tree (BST)

Demonstrating:
1. Recursive LCA in BST exploiting BST ordering property in O(h) time.
2. Iterative LCA in BST in O(h) time and O(1) auxiliary space.
"""


class TreeNode:
    """Binary Search Tree Node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def lca_bst_recursive(root, p, q):
    """
    Find LCA in a BST using recursive split-point search.
    Time Complexity: O(h)
    Space Complexity: O(h)
    """
    if root is None:
        return None

    # Both nodes are in left subtree
    if p.val < root.val and q.val < root.val:
        return lca_bst_recursive(root.left, p, q)

    # Both nodes are in right subtree
    if p.val > root.val and q.val > root.val:
        return lca_bst_recursive(root.right, p, q)

    # Split point found (one node on left, one on right, or one is root)
    return root


def lca_bst_iterative(root, p, q):
    """
    Find LCA in a BST using iterative traversal.
    Time Complexity: O(h)
    Space Complexity: O(1) auxiliary space
    """
    curr = root
    while curr:
        if p.val < curr.val and q.val < curr.val:
            curr = curr.left
        elif p.val > curr.val and q.val > curr.val:
            curr = curr.right
        else:
            return curr
    return None


def main():
    print("=" * 60)
    print("Lowest Common Ancestor in a Binary Search Tree")
    print("=" * 60)
    # BST:
    #         6
    #        / \
    #       2   8
    #      / \  / \
    #     0  4 7   9
    #       / \
    #      3   5
    n0 = TreeNode(0)
    n3 = TreeNode(3)
    n5 = TreeNode(5)
    n4 = TreeNode(4, n3, n5)
    n2 = TreeNode(2, n0, n4)
    n7 = TreeNode(7)
    n9 = TreeNode(9)
    n8 = TreeNode(8, n7, n9)
    root = TreeNode(6, n2, n8)

    # Test 1: LCA of 2 and 8 -> 6
    ans1_rec = lca_bst_recursive(root, n2, n8)
    ans1_iter = lca_bst_iterative(root, n2, n8)
    print(f"LCA of {n2.val} and {n8.val} -> Recursive: {ans1_rec.val}, Iterative: {ans1_iter.val}")

    # Test 2: LCA of 2 and 4 -> 2
    ans2_rec = lca_bst_recursive(root, n2, n4)
    ans2_iter = lca_bst_iterative(root, n2, n4)
    print(f"LCA of {n2.val} and {n4.val} -> Recursive: {ans2_rec.val}, Iterative: {ans2_iter.val}")

    # Test 3: LCA of 3 and 5 -> 4
    ans3_rec = lca_bst_recursive(root, n3, n5)
    ans3_iter = lca_bst_iterative(root, n3, n5)
    print(f"LCA of {n3.val} and {n5.val} -> Recursive: {ans3_rec.val}, Iterative: {ans3_iter.val}")


if __name__ == "__main__":
    main()
