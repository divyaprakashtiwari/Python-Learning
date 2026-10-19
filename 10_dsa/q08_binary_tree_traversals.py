"""
Topic: Data Structures and Algorithms (DSA) - Binary Tree and Traversals
------------------------------------------------------------------------
Questions Covered:
1. Depth-First Search (DFS) Traversals: Inorder, Preorder, Postorder (iterative & recursive).
2. Tree Depth Metrics: Maximum and minimum depth via recursive DFS and BFS queue.
3. Invert / Mirror Binary Tree: Swapping subtrees recursively in-place.
4. Symmetric Mirror Tree: Verifying mirror reflection equality across left/right branches.
5. Diameter of Binary Tree: Calculating longest path between any two tree nodes.
6. Binary Search Tree (BST) Validation: Enforcing strict (min_bound, max_bound) invariant.
7. Lowest Common Ancestor (LCA): Efficient LCA in BSTs vs general binary trees.
8. Root-to-Leaf Path Sums: Finding valid paths summing to target value.
9. Tree Serialization & Deserialization: Encoding binary tree into compact stream & decoding.
10. Architectural System: AST Expression Evaluation Tree & Rule Engine with Constant Folding.
"""

from typing import List, Tuple, Optional, Any, Dict


# ==============================================================================
# Question 1: DFS Traversals (Inorder, Preorder, Postorder) Iterative & Recursive
# ==============================================================================
class TreeNode:
    def __init__(self, val: Any = 0, left: Optional["TreeNode"] = None, right: Optional["TreeNode"] = None):
        self.val = val
        self.left = left
        self.right = right


def inorder_traversal_recursive(root: Optional[TreeNode]) -> List[Any]:
    if not root:
        return []
    return inorder_traversal_recursive(root.left) + [root.val] + inorder_traversal_recursive(root.right)


def inorder_traversal_iterative(root: Optional[TreeNode]) -> List[Any]:
    result: List[Any] = []
    stack: List[TreeNode] = []
    curr = root

    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        result.append(curr.val)
        curr = curr.right

    return result


def preorder_traversal_iterative(root: Optional[TreeNode]) -> List[Any]:
    if not root:
        return []
    result: List[Any] = []
    stack: List[TreeNode] = [root]

    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return result


def postorder_traversal_iterative(root: Optional[TreeNode]) -> List[Any]:
    if not root:
        return []
    # Postorder is reverse of (Root -> Right -> Left)
    result: List[Any] = []
    stack: List[TreeNode] = [root]

    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)

    return result[::-1]


def test_q1_dfs_traversals():
    # Tree:
    #       1
    #      / \
    #     2   3
    #    / \
    #   4   5
    tree = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))

    assert inorder_traversal_recursive(tree) == [4, 2, 5, 1, 3]
    assert inorder_traversal_iterative(tree) == [4, 2, 5, 1, 3]
    assert preorder_traversal_iterative(tree) == [1, 2, 4, 5, 3]
    assert postorder_traversal_iterative(tree) == [4, 5, 2, 3, 1]
    print("=== Q1: DFS Traversals (Recursive & Iterative) Verified ===")


# ==============================================================================
# Question 2: Maximum and Minimum Depth of Binary Tree
# ==============================================================================
def max_depth(root: Optional[TreeNode]) -> int:
    """Returns the maximum depth (number of nodes along longest root-to-leaf path)."""
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def min_depth(root: Optional[TreeNode]) -> int:
    """Returns minimum depth to the nearest leaf node using BFS queue."""
    if not root:
        return 0
    queue: List[Tuple[TreeNode, int]] = [(root, 1)]
    while queue:
        node, depth = queue.pop(0)
        # First leaf encountered gives minimum depth
        if not node.left and not node.right:
            return depth
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    return 0


def test_q2_tree_depths():
    tree = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    assert max_depth(tree) == 3
    assert min_depth(tree) == 2  # leaf 9 is at depth 2
    assert max_depth(None) == 0
    print("=== Q2: Maximum and Minimum Tree Depth Verified ===")


# ==============================================================================
# Question 3: Invert / Mirror a Binary Tree
# ==============================================================================
def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """Inverts binary tree in-place by swapping left and right subtrees."""
    if not root:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root


def test_q3_invert_tree():
    #      4                  4
    #    /   \      ->      /   \
    #   2     7            7     2
    #  / \   / \          / \   / \
    # 1   3 6   9        9   6 3   1
    tree = TreeNode(
        4,
        TreeNode(2, TreeNode(1), TreeNode(3)),
        TreeNode(7, TreeNode(6), TreeNode(9)),
    )
    inverted = invert_tree(tree)
    assert inorder_traversal_iterative(inverted) == [9, 7, 6, 4, 3, 2, 1]
    print("=== Q3: Invert Binary Tree Verified ===")


# ==============================================================================
# Question 4: Symmetric Tree (Mirror Reflection)
# ==============================================================================
def is_symmetric_tree(root: Optional[TreeNode]) -> bool:
    """Determines whether a tree is a symmetric mirror of itself around its center."""
    if not root:
        return True

    def is_mirror(t1: Optional[TreeNode], t2: Optional[TreeNode]) -> bool:
        if not t1 and not t2:
            return True
        if not t1 or not t2:
            return False
        return (
            t1.val == t2.val
            and is_mirror(t1.left, t2.right)
            and is_mirror(t1.right, t2.left)
        )

    return is_mirror(root.left, root.right)


def test_q4_symmetric_tree():
    # Symmetric:
    #      1
    #    /   \
    #   2     2
    #  / \   / \
    # 3   4 4   3
    sym_tree = TreeNode(
        1,
        TreeNode(2, TreeNode(3), TreeNode(4)),
        TreeNode(2, TreeNode(4), TreeNode(3)),
    )
    assert is_symmetric_tree(sym_tree) is True

    asym_tree = TreeNode(
        1,
        TreeNode(2, None, TreeNode(3)),
        TreeNode(2, None, TreeNode(3)),
    )
    assert is_symmetric_tree(asym_tree) is False
    print("=== Q4: Symmetric Tree Verification Verified ===")


# ==============================================================================
# Question 5: Diameter of Binary Tree
# ==============================================================================
def diameter_of_binary_tree(root: Optional[TreeNode]) -> int:
    """
    Computes diameter of a binary tree (length of longest path between any two nodes).
    Length is measured by number of edges.
    """
    max_diameter = 0

    def depth(node: Optional[TreeNode]) -> int:
        nonlocal max_diameter
        if not node:
            return 0
        left_d = depth(node.left)
        right_d = depth(node.right)
        max_diameter = max(max_diameter, left_d + right_d)
        return 1 + max(left_d, right_d)

    depth(root)
    return max_diameter


def test_q5_diameter_of_binary_tree():
    # Tree: 1 -> 2 (children 4, 5) and 3
    # Longest path: 4 -> 2 -> 1 -> 3 (3 edges)
    tree = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
    assert diameter_of_binary_tree(tree) == 3

    linear = TreeNode(1, TreeNode(2))
    assert diameter_of_binary_tree(linear) == 1
    print("=== Q5: Diameter of Binary Tree Verified ===")


# ==============================================================================
# Question 6: Validate Binary Search Tree (BST)
# ==============================================================================
def is_valid_bst(
    root: Optional[TreeNode],
    min_val: float = float("-inf"),
    max_val: float = float("inf"),
) -> bool:
    """
    Validates that a binary tree satisfies the BST property:
    Every node in left subtree must be < node.val,
    every node in right subtree must be > node.val.
    """
    if not root:
        return True

    if not (min_val < root.val < max_val):
        return False

    return is_valid_bst(root.left, min_val, root.val) and is_valid_bst(
        root.right, root.val, max_val
    )


def test_q6_validate_bst():
    valid_bst = TreeNode(2, TreeNode(1), TreeNode(3))
    assert is_valid_bst(valid_bst) is True

    # Invalid: 5 -> right is 4 (which is < 5)
    invalid_bst = TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6)))
    assert is_valid_bst(invalid_bst) is False

    # Invalid: right child of left branch is greater than root
    subtle_invalid = TreeNode(10, TreeNode(5, None, TreeNode(15)), TreeNode(20))
    assert is_valid_bst(subtle_invalid) is False
    print("=== Q6: Validate Binary Search Tree (BST) Verified ===")


# ==============================================================================
# Question 7: Lowest Common Ancestor (LCA) in BST and General Binary Tree
# ==============================================================================
def lca_bst(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    """Finds lowest common ancestor in a BST in O(h) time."""
    curr = root
    while curr:
        if p.val < curr.val and q.val < curr.val:
            curr = curr.left
        elif p.val > curr.val and q.val > curr.val:
            curr = curr.right
        else:
            return curr
    return None


def lca_general_tree(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    """Finds lowest common ancestor in an arbitrary binary tree."""
    if not root or root is p or root is q:
        return root

    left = lca_general_tree(root.left, p, q)
    right = lca_general_tree(root.right, p, q)

    if left and right:
        return root  # p and q split across left and right subtrees
    return left if left else right


def test_q7_lowest_common_ancestor():
    # BST:
    #         6
    #       /   \
    #      2     8
    #     / \   / \
    #    0   4 7   9
    n0 = TreeNode(0)
    n4 = TreeNode(4)
    n2 = TreeNode(2, n0, n4)
    n7 = TreeNode(7)
    n9 = TreeNode(9)
    n8 = TreeNode(8, n7, n9)
    root = TreeNode(6, n2, n8)

    assert lca_bst(root, n2, n8) is root
    assert lca_bst(root, n0, n4) is n2
    assert lca_general_tree(root, n0, n4) is n2
    print("=== Q7: Lowest Common Ancestor (BST & General Tree) Verified ===")


# ==============================================================================
# Question 8: Path Sum & Root-to-Leaf Path Accumulation
# ==============================================================================
def has_path_sum(root: Optional[TreeNode], target_sum: int) -> bool:
    """Checks if tree has a root-to-leaf path summing to target_sum."""
    if not root:
        return False
    if not root.left and not root.right:
        return root.val == target_sum
    rem = target_sum - root.val
    return has_path_sum(root.left, rem) or has_path_sum(root.right, rem)


def all_path_sums(root: Optional[TreeNode], target_sum: int) -> List[List[int]]:
    """Returns all root-to-leaf paths that sum to target_sum."""
    results: List[List[int]] = []

    def dfs(node: Optional[TreeNode], current_sum: int, path: List[int]):
        if not node:
            return
        path.append(node.val)
        if not node.left and not node.right and current_sum + node.val == target_sum:
            results.append(list(path))
        dfs(node.left, current_sum + node.val, path)
        dfs(node.right, current_sum + node.val, path)
        path.pop()

    dfs(root, 0, [])
    return results


def test_q8_path_sums():
    # Tree: 5 -> left(4 -> 11 -> 7, 2), right(8 -> 13, 4 -> 5, 1)
    tree = TreeNode(
        5,
        TreeNode(4, TreeNode(11, TreeNode(7), TreeNode(2))),
        TreeNode(8, TreeNode(13), TreeNode(4, TreeNode(5), TreeNode(1))),
    )
    # Path: 5 -> 4 -> 11 -> 2 sums to 22
    assert has_path_sum(tree, 22) is True
    paths = all_path_sums(tree, 22)
    assert [5, 4, 11, 2] in paths
    assert [5, 8, 4, 5] in paths
    assert len(paths) == 2
    print("=== Q8: Root-to-Leaf Path Sums Verified ===")


# ==============================================================================
# Question 9: Binary Tree Serialization and Deserialization
# ==============================================================================
class Codec:
    """Encodes a binary tree to a single string and decodes it back."""
    @staticmethod
    def serialize(root: Optional[TreeNode]) -> str:
        vals = []

        def preorder(node):
            if not node:
                vals.append("#")
                return
            vals.append(str(node.val))
            preorder(node.left)
            preorder(node.right)

        preorder(root)
        return ",".join(vals)

    @staticmethod
    def deserialize(data: str) -> Optional[TreeNode]:
        tokens = data.split(",")
        pos = 0

        def build():
            nonlocal pos
            if pos >= len(tokens) or tokens[pos] == "#":
                pos += 1
                return None
            val = int(tokens[pos])
            pos += 1
            node = TreeNode(val)
            node.left = build()
            node.right = build()
            return node

        return build()


def test_q9_serialization():
    tree = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))
    serialized = Codec.serialize(tree)
    deserialized = Codec.deserialize(serialized)

    assert inorder_traversal_iterative(deserialized) == [2, 1, 4, 3, 5]
    assert Codec.serialize(None) == "#"
    assert Codec.deserialize("#") is None
    print("=== Q9: Tree Serialization and Deserialization Verified ===")


# ==============================================================================
# Question 10: Architectural System: AST Expression Evaluation Tree & Rule Engine
# ==============================================================================
class ASTNode:
    def __init__(self, token: str, left: Optional["ASTNode"] = None, right: Optional["ASTNode"] = None):
        self.token = token
        self.left = left
        self.right = right

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


class ExpressionRuleEngine:
    """
    Production-grade Abstract Syntax Tree (AST) evaluator and rule engine.
    Supports arithmetic operators (+, -, *, /), comparison operators (>, <, ==),
    logical operators (AND, OR), variable substitution, and constant folding optimization.
    """
    @classmethod
    def evaluate(cls, node: Optional[ASTNode], context: Dict[str, Any]) -> Any:
        if not node:
            return None

        # Leaf node: literal number or context variable
        if node.is_leaf():
            if node.token in context:
                return context[node.token]
            try:
                if "." in node.token:
                    return float(node.token)
                return int(node.token)
            except ValueError:
                return node.token

        left_val = cls.evaluate(node.left, context)
        right_val = cls.evaluate(node.right, context)

        # Dispatch operator evaluation
        op = node.token
        if op == "+":
            return left_val + right_val
        elif op == "-":
            return left_val - right_val
        elif op == "*":
            return left_val * right_val
        elif op == "/":
            return left_val / right_val
        elif op == ">":
            return left_val > right_val
        elif op == "<":
            return left_val < right_val
        elif op == "==":
            return left_val == right_val
        elif op == "AND":
            return bool(left_val and right_val)
        elif op == "OR":
            return bool(left_val or right_val)
        else:
            raise ValueError(f"Unknown operator: {op}")

    @classmethod
    def constant_fold(cls, node: Optional[ASTNode]) -> Optional[ASTNode]:
        """Optimizes tree by pre-evaluating subtrees containing only literal constants."""
        if not node or node.is_leaf():
            return node

        node.left = cls.constant_fold(node.left)
        node.right = cls.constant_fold(node.right)

        # If both children are constant literals, evaluate now
        if node.left and node.left.is_leaf() and node.right and node.right.is_leaf():
            try:
                # Test if children are literal numbers
                val = cls.evaluate(node, context={})
                return ASTNode(str(val))
            except Exception:
                pass  # Contains variable, keep dynamic

        return node


def test_q10_ast_rule_engine():
    # Expression: (credit_score > 700) AND (age >= 21)
    # Tree:
    #             AND
    #           /     \
    #          >       >
    #        /   \   /   \
    #    score  700 age   20
    rule = ASTNode(
        "AND",
        ASTNode(">", ASTNode("score"), ASTNode("700")),
        ASTNode(">", ASTNode("age"), ASTNode("20")),
    )

    ctx1 = {"score": 750, "age": 25}
    assert ExpressionRuleEngine.evaluate(rule, ctx1) is True

    ctx2 = {"score": 680, "age": 30}
    assert ExpressionRuleEngine.evaluate(rule, ctx2) is False

    # Constant folding optimization: (x + (10 * 5)) -> (x + 50)
    calc_tree = ASTNode("+", ASTNode("x"), ASTNode("*", ASTNode("10"), ASTNode("5")))
    optimized = ExpressionRuleEngine.constant_fold(calc_tree)
    assert optimized.token == "+"
    assert optimized.left.token == "x"
    assert optimized.right.token == "50"
    assert ExpressionRuleEngine.evaluate(optimized, {"x": 20}) == 70
    print("=== Q10: Architectural AST Expression Tree & Rule Engine Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_dfs_traversals()
    test_q2_tree_depths()
    test_q3_invert_tree()
    test_q4_symmetric_tree()
    test_q5_diameter_of_binary_tree()
    test_q6_validate_bst()
    test_q7_lowest_common_ancestor()
    test_q8_path_sums()
    test_q9_serialization()
    test_q10_ast_rule_engine()
    print("\nAll 10 binary tree traversal DSA questions passed successfully!")
