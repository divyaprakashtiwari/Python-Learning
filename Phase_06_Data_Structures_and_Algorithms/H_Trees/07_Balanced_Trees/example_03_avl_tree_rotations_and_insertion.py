"""
Phase 6 - Section H.07: Balanced Trees
Example 03: AVL Tree Rotations and Self-Balancing Insertion

Demonstrating:
1. AVL Tree Node with explicit height metadata.
2. Single Rotations: Right Rotation (LL Case), Left Rotation (RR Case).
3. Double Rotations: Left-Right Rotation (LR Case), Right-Left Rotation (RL Case).
4. Insertion maintaining AVL Balance Factor condition: |height(L) - height(R)| <= 1.
"""


class AVLNode:
    """Node in an AVL Tree storing key, child links, and subtree height."""
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    """Self-balancing AVL Tree implementation."""

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        """Balance Factor = height(left) - height(right)"""
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, y):
        r"""
        Perform Right Rotation (LL Imbalance Fix):
             y                               x
            / \     Right Rotate(y)         / \
           x   T3   --------------->       T1  y
          / \                                 / \
         T1  T2                              T2  T3
        """
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights (y first because it is now child of x)
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        return x

    def left_rotate(self, x):
        r"""
        Perform Left Rotation (RR Imbalance Fix):
           x                                   y
          / \       Left Rotate(x)            / \
         T1  y      -------------->          x   T3
            / \                             / \
           T2  T3                          T1  T2
        """
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights (x first because it is now child of y)
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def insert(self, root, key):
        """
        Insert key into AVL tree and restore balance factor through rotations.
        Time Complexity: O(log n)
        Space Complexity: O(log n) call stack
        """
        # 1. Standard BST insertion
        if not root:
            return AVLNode(key)

        if key < root.key:
            root.left = self.insert(root.left, key)
        elif key > root.key:
            root.right = self.insert(root.right, key)
        else:
            return root  # Duplicate keys not allowed

        # 2. Update height of ancestor node
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # 3. Check balance factor to identify imbalance
        balance = self.get_balance(root)

        # Case 1: Left-Left (LL) -> Single Right Rotation
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)

        # Case 2: Right-Right (RR) -> Single Left Rotation
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

        # Case 3: Left-Right (LR) -> Double Rotation (Left Rotate child, Right Rotate root)
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Case 4: Right-Left (RL) -> Double Rotation (Right Rotate child, Left Rotate root)
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def inorder(self, root):
        res = []
        def dfs(node):
            if node:
                dfs(node.left)
                res.append(node.key)
                dfs(node.right)
        dfs(root)
        return res


def main():
    print("=" * 60)
    print("AVL Tree Self-Balancing Insertion")
    print("=" * 60)
    avl = AVLTree()
    root = None

    # Insert strictly ascending numbers: [10, 20, 30, 40, 50, 25]
    # In an unbalance BST this would form a skewed linked list of height 6.
    # In an AVL tree, self-balancing rotations keep height <= 3.
    keys = [10, 20, 30, 40, 50, 25]
    for k in keys:
        root = avl.insert(root, k)
        print(f"Inserted {k:2d} -> Root: {root.key:2d}, Height: {root.height}, Balance: {avl.get_balance(root)}")

    print("\nFinal Inorder Traversal (Sorted):", avl.inorder(root))
    print("Final Tree Height               :", root.height)
    print("Final Root Key                  :", root.key)


if __name__ == "__main__":
    main()
