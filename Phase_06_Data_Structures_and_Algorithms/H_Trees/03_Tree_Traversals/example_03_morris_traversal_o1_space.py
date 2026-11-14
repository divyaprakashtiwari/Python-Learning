"""
Phase 6 - Section H.03: Tree Traversals
Example 03: Morris Traversal (Inorder & Preorder in O(1) Auxiliary Space)

Demonstrating:
1. Morris Inorder Traversal using temporary threaded predecessor right pointers.
2. Morris Preorder Traversal.
3. Tree restoration guarantees (leaving the tree completely restored to its original structure).
"""


class TreeNode:
    """Standard Binary Tree Node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def morris_inorder_traversal(root):
    """
    Inorder traversal in O(n) time and O(1) auxiliary space (no stack/recursion).
    Creates temporary right links from inorder predecessor to current node.
    """
    result = []
    curr = root

    while curr:
        if curr.left is None:
            # No left subtree -> visit current and go right
            result.append(curr.val)
            curr = curr.right
        else:
            # Find inorder predecessor (rightmost node in left subtree)
            pred = curr.left
            while pred.right is not None and pred.right is not curr:
                pred = pred.right

            if pred.right is None:
                # Thread creation: link predecessor to current
                pred.right = curr
                curr = curr.left
            else:
                # Thread deletion: already visited left subtree, restore tree
                pred.right = None
                result.append(curr.val)
                curr = curr.right

    return result


def morris_preorder_traversal(root):
    """
    Preorder traversal in O(n) time and O(1) auxiliary space.
    Visits current node immediately upon first encountering and threading predecessor.
    """
    result = []
    curr = root

    while curr:
        if curr.left is None:
            result.append(curr.val)
            curr = curr.right
        else:
            pred = curr.left
            while pred.right is not None and pred.right is not curr:
                pred = pred.right

            if pred.right is None:
                # Visit root on first encounter
                result.append(curr.val)
                pred.right = curr
                curr = curr.left
            else:
                pred.right = None
                curr = curr.right

    return result


def main():
    print("=" * 60)
    print("Morris Traversal (O(1) Space Threaded Inorder & Preorder)")
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

    morris_in = morris_inorder_traversal(root)
    morris_pre = morris_preorder_traversal(root)

    print("Morris In-order  :", morris_in)
    print("Morris Pre-order :", morris_pre)

    # Verification: check that the tree structure remained intact
    print("Tree root.left.left still 4:", root.left.left.val == 4)
    print("Tree root.left.right.right is None (thread restored):", root.left.right.right is None)


if __name__ == "__main__":
    main()
