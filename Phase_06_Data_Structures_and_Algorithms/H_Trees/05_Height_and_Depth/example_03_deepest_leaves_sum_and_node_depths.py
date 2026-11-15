"""
Phase 6 - Section H.05: Height and Depth
Example 03: Deepest Leaves Sum and Total Node Depths

Demonstrating:
1. Deepest Leaves Sum using BFS level-order accumulation.
2. Deepest Leaves Sum using single-pass DFS with max-depth tracking.
3. Total Node Depths sum (sum of depths of all nodes in tree).
"""

from collections import deque


class TreeNode:
    """Standard Binary Tree Node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def deepest_leaves_sum_bfs(root):
    """
    Sum of values of deepest leaves via BFS.
    Overwrites level_sum with each new level; the last level processed holds the answer.
    Time Complexity: O(n)
    Space Complexity: O(w)
    """
    if not root:
        return 0

    queue = deque([root])
    level_sum = 0

    while queue:
        level_sum = 0
        for _ in range(len(queue)):
            node = queue.popleft()
            level_sum += node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return level_sum


def deepest_leaves_sum_dfs(root):
    """
    Sum of deepest leaves via DFS tracking (max_depth, total_sum).
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    max_depth = -1
    total_sum = 0

    def dfs(node, depth):
        nonlocal max_depth, total_sum
        if not node:
            return

        if not node.left and not node.right:
            if depth > max_depth:
                max_depth = depth
                total_sum = node.val
            elif depth == max_depth:
                total_sum += node.val
            return

        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)
    return total_sum


def sum_of_all_node_depths(root, depth=0):
    """
    Calculate the sum of all node depths relative to the root (depth 0).
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    if not root:
        return 0
    return depth + sum_of_all_node_depths(root.left, depth + 1) + sum_of_all_node_depths(root.right, depth + 1)


def main():
    print("=" * 60)
    print("Deepest Leaves Sum & Node Depths Sum")
    print("=" * 60)
    # Tree:
    #            1
    #          /   \
    #         2     3
    #        / \     \
    #       4   5     6
    #      /           \
    #     7             8
    # Deepest leaves are 7 and 8 at depth 3. Sum = 7 + 8 = 15.
    root = TreeNode(1)
    root.left = TreeNode(2, TreeNode(4, TreeNode(7)), TreeNode(5))
    root.right = TreeNode(3, None, TreeNode(6, None, TreeNode(8)))

    sum_bfs = deepest_leaves_sum_bfs(root)
    sum_dfs = deepest_leaves_sum_dfs(root)
    total_depths = sum_of_all_node_depths(root)

    print("Deepest Leaves Sum (BFS):", sum_bfs)
    print("Deepest Leaves Sum (DFS):", sum_dfs)
    print("Total Sum of All Node Depths:", total_depths)


if __name__ == "__main__":
    main()
