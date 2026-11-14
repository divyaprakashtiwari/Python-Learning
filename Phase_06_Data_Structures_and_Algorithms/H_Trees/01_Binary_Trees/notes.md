# Binary Trees

## 1. Introduction

A **Binary Tree** is a hierarchical, non-linear data structure in which each node has at most two children, referred to as the **left child** and the **right child**.

Unlike linear data structures (arrays, linked lists) where elements are arranged sequentially, binary trees organize data in parent-child relationships. Trees serve as the foundation for Binary Search Trees (BST), AVL trees, Red-Black trees, Heaps, Tries, and syntax parsing engines in compilers.

---

## 2. Why Use Binary Trees?

| Property / Feature | Array / Linked List | Binary Tree |
|---|---|---|
| **Hierarchical Representation** | Difficult (flat index structure) | Natural recursive tree structure |
| **Search Space Division** | $O(n)$ in linked list | $O(\log n)$ when balanced |
| **Dynamic Insertion/Deletion** | $O(n)$ shifts in array | $O(1)$ pointer adjustments at leaf |
| **Recursive Decomposition** | Iterative / 1D divide-and-conquer | Divide into independent Left & Right subtrees |
| **Expression Evaluation** | Complex parsing stacks | Abstract Syntax Trees (AST) |

---

## 3. Syntax / Node Definition

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

---

## 4. Classifications of Binary Trees

1. **Full Binary Tree (Strict Binary Tree):**
   Every node has either 0 or 2 children (no node has exactly 1 child).
2. **Complete Binary Tree:**
   All levels are completely filled except possibly the last level, and all nodes in the last level are as far left as possible (used in Binary Heaps).
3. **Perfect Binary Tree:**
   All internal nodes have 2 children, and all leaf nodes are at the exact same depth. Total nodes $n = 2^{h+1} - 1$.
4. **Balanced Binary Tree:**
   The height difference between the left and right subtrees of any node is at most 1 (e.g., AVL tree). Height is bounded by $O(\log n)$.
5. **Degenerate / Skewed Tree:**
   Every parent node has only one child. The tree essentially degenerates into a singly linked list with $O(n)$ height.

---

## 5. Examples

### Example 1: Tree Construction & Full Tree Verification
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def is_full(root):
    if not root:
        return True
    if not root.left and not root.right:
        return True
    if root.left and root.right:
        return is_full(root.left) and is_full(root.right)
    return False
```

### Example 2: Recursive Size, Sum, Max, and Leaf Counting
```python
def tree_size(root):
    if not root:
        return 0
    return 1 + tree_size(root.left) + tree_size(root.right)

def count_leaves(root):
    if not root:
        return 0
    if not root.left and not root.right:
        return 1
    return count_leaves(root.left) + count_leaves(root.right)
```

### Example 3: Serialization & Deserialization via BFS
```python
from collections import deque

def serialize(root):
    if not root:
        return ""
    q, res = deque([root]), []
    while q:
        node = q.popleft()
        if node:
            res.append(str(node.val))
            q.append(node.left)
            q.append(node.right)
        else:
            res.append("#")
    while res and res[-1] == "#":
        res.pop()
    return ",".join(res)
```

---

## 6. Output

```
1. Full Tree Verification:
   Tree with root=1, left=2(4,5), right=3 -> Full: True

2. Tree Metrics:
   Total Nodes (Size) : 6
   Sum of All Values  : 59
   Maximum Value      : 20
   Number of Leaves   : 3

3. Serialization:
   Serialized String   : 1,2,3,#,#,4,5
   Reserialized Tree   : Identical (True)
```

---

## 7. Code Explanation

| Function / Logic | Explanation |
|---|---|
| `1 + size(left) + size(right)` | Standard bottom-up post-order reduction aggregating subtree counts |
| `not left and not right` | Identifies a terminal leaf node (base case for depth and leaf counts) |
| `deque([root])` in BFS | Level-by-level queue processing preserving topological parent-child ordering |
| Sentinel `"#"` | Encodes absent children so structural topology is unambiguous during deserialization |
| `is_same_tree(p, q)` | Recursively validates value and subtree isomorphism |

---

## 8. Common Mistakes

1. **Forgetting Null Base Cases**:
   Accessing `root.left` when `root` is `None` raises an immediate `AttributeError: 'NoneType' object has no attribute 'left'`.
2. **Assuming Tree is Balanced**:
   Assuming tree height is always $O(\log n)$ leads to unexpected $O(n)$ recursion stack overflow on skewed trees.
3. **Ambiguous Serialization**:
   Serializing node values without null sentinels makes it impossible to reconstruct an arbitrary binary tree uniquely from a single traversal.
4. **Confusing Full and Complete Trees**:
   A full tree does not require leaves to be on the same level; a complete tree requires all leaves to be packed tightly to the left.
5. **Global State in Recursive Traversal**:
   Using mutable global variables across recursive tree calls causes race conditions and incorrect results on repeated runs.

---

## 9. Practice Questions

1. Implement a function to check if two binary trees are identical (`is_same_tree`).
2. Write a function to check if a binary tree is symmetric (mirror image of itself).
3. Invert/flip a binary tree left-to-right in $O(n)$ time.
4. Construct a binary tree from preorder and inorder traversal arrays.
5. Find the maximum path sum between any two nodes in a binary tree.

---

## 10. Interview Questions

**Q1: What is the maximum number of nodes in a binary tree of height $h$?**
The maximum number of nodes occurs in a perfect binary tree, which contains $2^{h+1} - 1$ nodes (assuming root is at height 0).

**Q2: What is the minimum possible height of a binary tree with $n$ nodes?**
The minimum height is $\lfloor \log_2(n) \rfloor$, achieved when the tree is complete and balanced.

**Q3: Can a binary tree be uniquely reconstructed from its preorder and postorder traversals?**
Not in general. Preorder and postorder can only reconstruct a tree uniquely if the tree is a **full binary tree** (every internal node has 2 children). Otherwise, preorder + inorder or postorder + inorder is required.

**Q4: What is the recursion call stack space complexity for binary tree operations?**
The auxiliary call stack space is $O(h)$ where $h$ is the height of the tree. For a balanced tree, $h = O(\log n)$; in the worst case (skewed tree), $h = O(n)$.

**Q5: How can a complete binary tree be represented without node pointers?**
Using a 1D array where for any node at index $i$ (0-indexed):
- Left child is at `2 * i + 1`
- Right child is at `2 * i + 2`
- Parent is at `(i - 1) // 2`
(This is the exact representation used in Binary Heaps).
