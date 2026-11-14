"""
Phase 6 - Section H.02: Binary Search Trees
Example 01: BST Insert, Search, and Delete Operations

Demonstrating:
1. BST Insert operation maintaining ordering property.
2. Search (iterative and recursive) in O(h) time.
3. Three cases of BST Deletion:
   - Node with no children (leaf).
   - Node with 1 child.
   - Node with 2 children (replace with inorder successor).
"""


class TreeNode:
    """Binary Search Tree Node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def bst_insert(root, val):
    """
    Insert a value into the BST.
    Time Complexity: O(h) where h is tree height
    """
    if root is None:
        return TreeNode(val)
    if val < root.val:
        root.left = bst_insert(root.left, val)
    elif val > root.val:
        root.right = bst_insert(root.right, val)
    return root


def bst_search(root, target):
    """
    Search for target in BST. Returns TreeNode or None.
    Time Complexity: O(h)
    """
    curr = root
    while curr:
        if curr.val == target:
            return curr
        elif target < curr.val:
            curr = curr.left
        else:
            curr = curr.right
    return None


def find_min(node):
    """Find leftmost node in a subtree (inorder successor)."""
    curr = node
    while curr.left:
        curr = curr.left
    return curr


def bst_delete(root, key):
    """
    Delete a key from the BST.
    Handles 3 cases: 0 children, 1 child, 2 children.
    Time Complexity: O(h)
    """
    if root is None:
        return None

    if key < root.val:
        root.left = bst_delete(root.left, key)
    elif key > root.val:
        root.right = bst_delete(root.right, key)
    else:
        # Node to be deleted found

        # Case 1 & 2: 0 or 1 child
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left

        # Case 3: 2 children
        # Find inorder successor (smallest node in right subtree)
        successor = find_min(root.right)
        root.val = successor.val
        # Delete successor from right subtree
        root.right = bst_delete(root.right, successor.val)

    return root


def inorder_traversal(root):
    """Inorder traversal of BST yields sorted values."""
    res = []
    def dfs(node):
        if node:
            dfs(node.left)
            res.append(node.val)
            dfs(node.right)
    dfs(root)
    return res


def main():
    print("=" * 60)
    print("BST Construction and Inorder Verification")
    print("=" * 60)
    values = [50, 30, 70, 20, 40, 60, 80]
    root = None
    for v in values:
        root = bst_insert(root, v)

    print("Inserted values:", values)
    print("Inorder traversal (must be sorted):", inorder_traversal(root))

    print("\n" + "=" * 60)
    print("BST Search")
    print("=" * 60)
    for target in [40, 99]:
        found = bst_search(root, target)
        print(f"Search {target}: {'Found' if found else 'Not Found'}")

    print("\n" + "=" * 60)
    print("BST Deletion (3 Cases)")
    print("=" * 60)
    # Case 1: Delete leaf (20)
    root = bst_delete(root, 20)
    print("After deleting leaf (20)     :", inorder_traversal(root))

    # Case 2: Delete node with 1 child (30 has child 40)
    root = bst_delete(root, 30)
    print("After deleting 1-child node (30):", inorder_traversal(root))

    # Case 3: Delete node with 2 children (root 50)
    root = bst_delete(root, 50)
    print("After deleting 2-child root (50):", inorder_traversal(root))


if __name__ == "__main__":
    main()
