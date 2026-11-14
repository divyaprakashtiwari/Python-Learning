"""
Phase 6 - Section H.03: Tree Traversals
Example 02: Iterative DFS Traversals (Pre-order, In-order, Post-order)

Demonstrating:
1. Iterative Pre-order using a single explicit stack.
2. Iterative In-order using stack and left-chain descending pointer.
3. Iterative Post-order using two stacks (or reverse modified pre-order).
"""


class TreeNode:
    """Standard Binary Tree Node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def preorder_iterative(root):
    """
    Iterative Pre-order Traversal (Root, Left, Right).
    Stack pushes right child first so left child is popped and processed first.
    """
    if not root:
        return []
    stack = [root]
    result = []
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return result


def inorder_iterative(root):
    """
    Iterative In-order Traversal (Left, Root, Right).
    Descends to leftmost child, then pops and visits right branch.
    """
    stack = []
    curr = root
    result = []
    while stack or curr:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        result.append(curr.val)
        curr = curr.right
    return result


def postorder_iterative_two_stacks(root):
    """
    Iterative Post-order Traversal (Left, Right, Root) using 2 Stacks.
    Emulates Root -> Right -> Left, which when reversed gives Left -> Right -> Root.
    """
    if not root:
        return []
    s1 = [root]
    s2 = []
    while s1:
        node = s1.pop()
        s2.append(node.val)
        if node.left:
            s1.append(node.left)
        if node.right:
            s1.append(node.right)
    return s2[::-1]


def main():
    print("=" * 60)
    print("Iterative DFS Tree Traversals")
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

    iter_pre = preorder_iterative(root)
    iter_in = inorder_iterative(root)
    iter_post = postorder_iterative_two_stacks(root)

    print("Iterative Pre-order :", iter_pre)
    print("Iterative In-order  :", iter_in)
    print("Iterative Post-order:", iter_post)


if __name__ == "__main__":
    main()
