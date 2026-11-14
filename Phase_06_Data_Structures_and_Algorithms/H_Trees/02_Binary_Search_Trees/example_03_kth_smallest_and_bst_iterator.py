"""
Phase 6 - Section H.02: Binary Search Trees
Example 03: Kth Smallest Element and BST Iterator

Demonstrating:
1. Kth Smallest Element in BST via early-exit Inorder Traversal in O(h + k) time.
2. BST Iterator class supporting next() and hasNext() with O(h) memory.
"""


class TreeNode:
    """Binary Search Tree Node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def kth_smallest(root, k):
    """
    Find kth smallest element in BST (1-indexed).
    Time Complexity: O(h + k)
    Space Complexity: O(h)
    """
    stack = []
    curr = root

    while stack or curr:
        while curr:
            stack.append(curr)
            curr = curr.left

        curr = stack.pop()
        k -= 1
        if k == 0:
            return curr.val

        curr = curr.right

    return None


class BSTIterator:
    """
    Iterator over a binary search tree (BST) initialized with root.
    Provides in-order traversal with O(h) memory and O(1) amortized time.
    """
    def __init__(self, root: TreeNode):
        self.stack = []
        self._push_left_chain(root)

    def _push_left_chain(self, node: TreeNode):
        while node:
            self.stack.append(node)
            node = node.left

    def next(self) -> int:
        """Returns the next smallest number."""
        top_node = self.stack.pop()
        if top_node.right:
            self._push_left_chain(top_node.right)
        return top_node.val

    def hasNext(self) -> bool:
        """Returns whether we have a next smallest number."""
        return len(self.stack) > 0


def main():
    print("=" * 60)
    print("1. Kth Smallest Element in BST")
    print("=" * 60)
    # BST:
    #        5
    #       / \
    #      3   6
    #     / \
    #    2   4
    #   /
    #  1
    root = TreeNode(5)
    root.left = TreeNode(3, TreeNode(2, TreeNode(1)), TreeNode(4))
    root.right = TreeNode(6)

    for k in [1, 3, 5]:
        val = kth_smallest(root, k)
        print(f"k = {k} -> Smallest Element: {val}")

    print("\n" + "=" * 60)
    print("2. BST Iterator (Controlled Stack Inorder)")
    print("=" * 60)
    iterator = BSTIterator(root)
    result = []
    while iterator.hasNext():
        result.append(iterator.next())
    print("Iterated sequence (strictly sorted):", result)


if __name__ == "__main__":
    main()
