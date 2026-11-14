"""
Phase 6 - Section H.03: Tree Traversals
Example 01: Recursive Depth-First Search (DFS) Traversals

Demonstrating:
1. Pre-order Traversal  (Root -> Left -> Right): used for tree duplication / serialization.
2. In-order Traversal   (Left -> Root -> Right): used for BST sorted order retrieval.
3. Post-order Traversal (Left -> Right -> Root): used for bottom-up cleanup / deletion / height computation.
"""


class TreeNode:
    """Standard Binary Tree Node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def preorder_recursive(root):
    """Root -> Left -> Right"""
    res = []
    def dfs(node):
        if node:
            res.append(node.val)
            dfs(node.left)
            dfs(node.right)
    dfs(root)
    return res


def inorder_recursive(root):
    """Left -> Root -> Right"""
    res = []
    def dfs(node):
        if node:
            dfs(node.left)
            res.append(node.val)
            dfs(node.right)
    dfs(root)
    return res


def postorder_recursive(root):
    """Left -> Right -> Root"""
    res = []
    def dfs(node):
        if node:
            dfs(node.left)
            dfs(node.right)
            res.append(node.val)
    dfs(root)
    return res


def main():
    print("=" * 60)
    print("Recursive DFS Tree Traversals")
    print("=" * 60)
    # Tree:
    #         1
    #        / \
    #       2   3
    #      / \
    #     4   5
    root = TreeNode(1)
    root.left = TreeNode(2, TreeNode(4), TreeNode(5))
    root.right = TreeNode(3)

    pre = preorder_recursive(root)
    ino = inorder_recursive(root)
    post = postorder_recursive(root)

    print("Pre-order  (Root, Left, Right):", pre)
    print("In-order   (Left, Root, Right):", ino)
    print("Post-order (Left, Right, Root):", post)


if __name__ == "__main__":
    main()
