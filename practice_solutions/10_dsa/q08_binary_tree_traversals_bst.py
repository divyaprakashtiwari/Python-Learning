"""
Question 8: Binary Tree Traversals, Structural Inversion & BST Validation
Topic: Data Structures & Algorithms (DSA)

Key Concepts Tested:
- Node-based Binary Tree data representation
- Depth-First Traversals: Inorder (recursive & iterative), Preorder, Postorder
- Breadth-First Search (Level-Order) using deque
- Maximum tree depth computation
- In-place tree inversion / mirroring
- Strict Binary Search Tree (BST) validity checking with boundary ranges
"""

from collections import deque
from typing import TypeVar, Generic, Optional, List

T = TypeVar("T")


class TreeNode(Generic[T]):
    """Binary tree node structure."""

    def __init__(
        self,
        val: T,
        left: Optional["TreeNode[T]"] = None,
        right: Optional["TreeNode[T]"] = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"TreeNode({self.val})"


def inorder_traversal(root: Optional[TreeNode[T]]) -> List[T]:
    """Inorder traversal: Left -> Node -> Right (Recursive)."""
    if not root:
        return []
    return inorder_traversal(root.left) + [root.val] + inorder_traversal(root.right)


def inorder_iterative(root: Optional[TreeNode[T]]) -> List[T]:
    """Inorder traversal using an explicit stack."""
    result: List[T] = []
    stack: List[TreeNode[T]] = []
    curr = root

    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        result.append(curr.val)
        curr = curr.right

    return result


def preorder_traversal(root: Optional[TreeNode[T]]) -> List[T]:
    """Preorder traversal: Node -> Left -> Right."""
    if not root:
        return []
    return [root.val] + preorder_traversal(root.left) + preorder_traversal(root.right)


def postorder_traversal(root: Optional[TreeNode[T]]) -> List[T]:
    """Postorder traversal: Left -> Right -> Node."""
    if not root:
        return []
    return postorder_traversal(root.left) + postorder_traversal(root.right) + [root.val]


def level_order_traversal(root: Optional[TreeNode[T]]) -> List[List[T]]:
    """Breadth-first level order traversal returning nodes grouped by tree depth."""
    if not root:
        return []

    levels: List[List[T]] = []
    queue: deque[TreeNode[T]] = deque([root])

    while queue:
        level_size = len(queue)
        current_level: List[T] = []

        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        levels.append(current_level)

    return levels


def max_depth(root: Optional[TreeNode[T]]) -> int:
    """Computes the maximum height (root-to-leaf node count) of the binary tree."""
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def invert_tree(root: Optional[TreeNode[T]]) -> Optional[TreeNode[T]]:
    """Inverts / mirrors the binary tree in-place by swapping left and right subtrees."""
    if not root:
        return None

    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root


def is_valid_bst(
    root: Optional[TreeNode[int]],
    min_val: float = float("-inf"),
    max_val: float = float("inf"),
) -> bool:
    """
    Validates if a binary tree satisfies BST invariants:
    every left descendant < node.val and every right descendant > node.val.
    """
    if not root:
        return True

    if not (min_val < root.val < max_val):
        return False

    return is_valid_bst(root.left, min_val, root.val) and is_valid_bst(root.right, root.val, max_val)


if __name__ == "__main__":
    # Construct sample binary tree:
    #        4
    #       / \
    #      2   7
    #     / \
    #    1   3
    root = TreeNode(4)
    root.left = TreeNode(2, TreeNode(1), TreeNode(3))
    root.right = TreeNode(7)

    print("=== 1. Tree Traversals ===")
    in_res = inorder_traversal(root)
    in_iter = inorder_iterative(root)
    pre_res = preorder_traversal(root)
    post_res = postorder_traversal(root)
    levels = level_order_traversal(root)

    print(f"Inorder Traversal: {in_res}")
    print(f"Inorder Iterative: {in_iter} (Matches recursive: {in_res == in_iter})")
    print(f"Preorder Traversal: {pre_res}")
    print(f"Postorder Traversal: {post_res}")
    print(f"Level Order Traversal: {levels}")

    print("\n=== 2. Structural Properties & BST Validation ===")
    tree_depth = max_depth(root)
    valid_bst = is_valid_bst(root)
    print(f"Tree Max Depth: {tree_depth}")
    print(f"Is Valid BST: {valid_bst}")

    # Invalid BST test
    bad_bst = TreeNode(5, TreeNode(6), TreeNode(8))  # 6 on left of 5 violates BST
    print(f"Invalid Tree BST check: {is_valid_bst(bad_bst)}")

    print("\n=== 3. In-Place Tree Inversion ===")
    inverted_root = invert_tree(root)
    in_res_inverted = inorder_traversal(inverted_root)
    print(f"Inverted Tree Inorder: {in_res_inverted}")

    print("\n=== 4. Edge Cases: Empty Trees ===")
    print(f"Empty tree max depth: {max_depth(None)}")
    print(f"Empty tree level order: {level_order_traversal(None)}")
    print(f"Empty tree is BST: {is_valid_bst(None)}")
