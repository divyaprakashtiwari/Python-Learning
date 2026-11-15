"""
Phase 6 - Section H.06: Lowest Common Ancestor
Example 01: LCA in a General Binary Tree

Demonstrating:
1. Recursive DFS divide-and-conquer LCA in O(n) time.
2. Iterative LCA using a parent pointer dictionary and ancestor set.
"""


class TreeNode:
    """Standard Binary Tree Node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def lowest_common_ancestor_recursive(root, p, q):
    """
    Find LCA of nodes p and q in general binary tree.
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    # Base case: if root is null or matches either target, return root
    if root is None or root is p or root is q:
        return root

    left = lowest_common_ancestor_recursive(root.left, p, q)
    right = lowest_common_ancestor_recursive(root.right, p, q)

    # If both left and right return non-null, root is the LCA split point
    if left and right:
        return root

    # Otherwise return whichever subtree found a target
    return left if left else right


def lowest_common_ancestor_iterative(root, p, q):
    """
    Find LCA iteratively using parent pointers and a visited ancestor set.
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    parent = {root: None}
    stack = [root]

    # Traverse until both p and q have known parents
    while p not in parent or q not in parent:
        node = stack.pop()
        if node.left:
            parent[node.left] = node
            stack.append(node.left)
        if node.right:
            parent[node.right] = node
            stack.append(node.right)

    # Collect all ancestors of p
    ancestors = set()
    curr = p
    while curr:
        ancestors.add(curr)
        curr = parent[curr]

    # Walk up from q until meeting first shared ancestor
    curr = q
    while curr not in ancestors:
        curr = parent[curr]

    return curr


def main():
    print("=" * 60)
    print("Lowest Common Ancestor in General Binary Tree")
    print("=" * 60)
    # Tree:
    #         3
    #        / \
    #       5   1
    #      / \  / \
    #     6  2 0   8
    #       / \
    #      7   4
    root = TreeNode(3)
    p = TreeNode(5)
    q = TreeNode(1)
    n6 = TreeNode(6)
    n2 = TreeNode(2, TreeNode(7), TreeNode(4))

    root.left = p
    root.right = q
    p.left = n6
    p.right = n2
    q.left = TreeNode(0)
    q.right = TreeNode(8)

    # LCA of 5 and 1 -> 3
    lca_rec1 = lowest_common_ancestor_recursive(root, p, q)
    lca_iter1 = lowest_common_ancestor_iterative(root, p, q)
    print(f"LCA of {p.val} and {q.val} (Recursive): {lca_rec1.val}")
    print(f"LCA of {p.val} and {q.val} (Iterative): {lca_iter1.val}")

    # LCA of 5 and 4 -> 5 (ancestor can be itself)
    n4 = n2.right
    lca_rec2 = lowest_common_ancestor_recursive(root, p, n4)
    lca_iter2 = lowest_common_ancestor_iterative(root, p, n4)
    print(f"\nLCA of {p.val} and {n4.val} (Recursive): {lca_rec2.val}")
    print(f"LCA of {p.val} and {n4.val} (Iterative): {lca_iter2.val}")


if __name__ == "__main__":
    main()
