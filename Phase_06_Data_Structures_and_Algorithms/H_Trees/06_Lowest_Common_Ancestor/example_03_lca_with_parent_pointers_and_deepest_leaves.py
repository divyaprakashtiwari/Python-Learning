"""
Phase 6 - Section H.06: Lowest Common Ancestor
Example 03: LCA with Parent Pointers and LCA of Deepest Leaves

Demonstrating:
1. LCA in a binary tree where nodes have a `parent` pointer in O(1) auxiliary space (two-pointer technique).
2. LCA of the deepest leaves in a binary tree.
"""


class NodeWithParent:
    """Tree node with left, right, and parent pointer."""
    def __init__(self, val=0, left=None, right=None, parent=None):
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent


def lca_with_parent_pointers(p, q):
    """
    Find LCA when nodes have parent pointers.
    Analogy: Intersection of Two Singly Linked Lists.
    When a pointer reaches the root (None), wrap around to the other start node.
    Time Complexity: O(h)
    Space Complexity: O(1) auxiliary space
    """
    a, b = p, q
    while a is not b:
        a = a.parent if a else q
        b = b.parent if b else p
    return a


class TreeNode:
    """Standard Binary Tree Node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def lca_deepest_leaves(root):
    """
    Find the smallest subtree containing all deepest leaves.
    Returns (LCA_node, depth).
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    def dfs(node):
        if not node:
            return None, 0

        left_node, left_depth = dfs(node.left)
        right_node, right_depth = dfs(node.right)

        if left_depth == right_depth:
            # Both sides have equal max depth; current node is their LCA
            return node, left_depth + 1
        elif left_depth > right_depth:
            return left_node, left_depth + 1
        else:
            return right_node, right_depth + 1

    lca_node, _ = dfs(root)
    return lca_node


def main():
    print("=" * 60)
    print("1. LCA with Parent Pointers (O(1) Space Two-Pointer)")
    print("=" * 60)
    # Tree:
    #         3
    #        / \
    #       5   1
    #      / \
    #     6   2
    n3 = NodeWithParent(3)
    n5 = NodeWithParent(5, parent=n3)
    n1 = NodeWithParent(1, parent=n3)
    n3.left, n3.right = n5, n1

    n6 = NodeWithParent(6, parent=n5)
    n2 = NodeWithParent(2, parent=n5)
    n5.left, n5.right = n6, n2

    lca_node = lca_with_parent_pointers(n6, n2)
    print(f"LCA of {n6.val} and {n2.val}: {lca_node.val}")

    lca_node_cross = lca_with_parent_pointers(n6, n1)
    print(f"LCA of {n6.val} and {n1.val}: {lca_node_cross.val}")

    print("\n" + "=" * 60)
    print("2. LCA of Deepest Leaves")
    print("=" * 60)
    # Tree:
    #         3
    #        / \
    #       5   1
    #      / \   \
    #     6   2   8
    #        / \
    #       7   4
    # Deepest leaves are 7 and 4 at depth 4. Their LCA is 2.
    root = TreeNode(3)
    root.left = TreeNode(5, TreeNode(6), TreeNode(2, TreeNode(7), TreeNode(4)))
    root.right = TreeNode(1, None, TreeNode(8))

    lca_deep = lca_deepest_leaves(root)
    print(f"LCA of deepest leaves: {lca_deep.val}")


if __name__ == "__main__":
    main()
