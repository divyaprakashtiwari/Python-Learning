"""
Phase 6 - Section H.05: Height and Depth
Example 01: Maximum Depth and Minimum Depth of Binary Tree

Demonstrating:
1. Maximum Depth of Binary Tree using recursive DFS in O(n) time.
2. Maximum Depth using iterative BFS level order.
3. Minimum Depth of Binary Tree (properly handling 1-child cases and BFS early exit).
"""

from collections import deque


class TreeNode:
    """Standard Binary Tree Node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_depth_recursive(root):
    """
    Max depth is the number of nodes along the longest path from root to leaf.
    Time Complexity: O(n)
    Space Complexity: O(h) call stack
    """
    if root is None:
        return 0
    return 1 + max(max_depth_recursive(root.left), max_depth_recursive(root.right))


def max_depth_bfs(root):
    """Max depth using BFS level order counting."""
    if root is None:
        return 0
    queue = deque([root])
    depth = 0
    while queue:
        depth += 1
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return depth


def min_depth(root):
    """
    Minimum depth is the number of nodes along shortest path from root to nearest leaf.
    Note: A node with only one child is NOT a leaf; we must continue down the non-empty child!
    Uses BFS for optimal early termination.
    Time Complexity: O(n) worst case, O(min_depth) best case
    Space Complexity: O(w)
    """
    if root is None:
        return 0

    queue = deque([(root, 1)])  # (node, current_depth)

    while queue:
        node, depth = queue.popleft()

        # If it is a leaf (both children None), we found the minimum depth
        if node.left is None and node.right is None:
            return depth

        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))

    return 0


def main():
    print("=" * 60)
    print("1. Maximum Depth")
    print("=" * 60)
    # Balanced tree:
    #       3
    #      / \
    #     9  20
    #        / \
    #       15  7
    root1 = TreeNode(3)
    root1.left = TreeNode(9)
    root1.right = TreeNode(20, TreeNode(15), TreeNode(7))

    print("Tree 1 Max Depth (DFS):", max_depth_recursive(root1))
    print("Tree 1 Max Depth (BFS):", max_depth_bfs(root1))
    print("Tree 1 Min Depth (BFS):", min_depth(root1))

    print("\n" + "=" * 60)
    print("2. Minimum Depth Skewed Edge Case")
    print("=" * 60)
    # Skewed tree:
    #   2
    #    \
    #     3
    #      \
    #       4
    #        \
    #         5
    #          \
    #           6
    # Note: 2 has no left child, but it is NOT a leaf! Shortest path to leaf is 5.
    root2 = TreeNode(2, right=TreeNode(3, right=TreeNode(4, right=TreeNode(5, right=TreeNode(6)))))
    print("Skewed Tree Max Depth:", max_depth_recursive(root2))
    print("Skewed Tree Min Depth:", min_depth(root2))


if __name__ == "__main__":
    main()
