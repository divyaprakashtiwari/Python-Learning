# Binary Search Trees (BST)

## 1. Introduction

A **Binary Search Tree (BST)** is a node-based binary tree data structure with the fundamental **ordering invariant**:
- The **left subtree** of a node contains only nodes with values strictly less than the node's value.
- The **right subtree** of a node contains only nodes with values strictly greater than the node's value.
- Both the left and right subtrees must also be binary search trees.

This property guarantees that an **inorder traversal** ($Left \to Node \to Right$) of a BST visits the values in strictly ascending sorted order.

---

## 2. Why Use Binary Search Trees?

| Operation | Array (Unsorted) | Sorted Array | Singly Linked List | Balanced BST (AVL/Red-Black) | Skewed BST |
|---|---|---|---|---|---|
| **Search** | $O(n)$ | $O(\log n)$ | $O(n)$ | **$O(\log n)$** | $O(n)$ |
| **Insert** | $O(1)$ | $O(n)$ | $O(1)$ | **$O(\log n)$** | $O(n)$ |
| **Delete** | $O(n)$ | $O(n)$ | $O(n)$ | **$O(\log n)$** | $O(n)$ |
| **Min / Max** | $O(n)$ | $O(1)$ | $O(n)$ | **$O(\log n)$** | $O(n)$ |
| **Predecessor / Successor** | $O(n)$ | $O(1)$ | $O(n)$ | **$O(\log n)$** | $O(n)$ |

---

## 3. Syntax / API Reference

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Search
def search(root, target):
    curr = root
    while curr and curr.val != target:
        curr = curr.left if target < curr.val else curr.right
    return curr

# Insert
def insert(root, val):
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    elif val > root.val:
        root.right = insert(root.right, val)
    return root
```

---

## 4. Key Algorithmic Mechanics

### BST Deletion Cases
Deleting node $Z$ from a BST falls into one of three structural cases:
1. **$Z$ is a leaf (no children):** Sever the link from $Z$'s parent by returning `None`.
2. **$Z$ has exactly one child:** Bypass $Z$ by returning its non-null child directly to $Z$'s parent.
3. **$Z$ has two children:**
   - Locate $Z$'s **inorder successor** (the minimum node in $Z$'s right subtree).
   - Copy the successor's value into $Z$.
   - Recursively delete the successor from $Z$'s right subtree (which is guaranteed to fall into Case 1 or 2).

### Validating BST Property: The Global Range Trap
Checking only `root.left.val < root.val < root.right.val` locally is **incorrect** because a node deep in the right subtree could be smaller than an ancestor higher up. Correct validation passes bounding intervals $(low, high)$ down the tree:
- Left child interval: $(low, root.val)$
- Right child interval: $(root.val, high)$

---

## 5. Examples

### Example 1: BST Insert, Search, and Delete
```python
def bst_delete(root, key):
    if not root:
        return None
    if key < root.val:
        root.left = bst_delete(root.left, key)
    elif key > root.val:
        root.right = bst_delete(root.right, key)
    else:
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        successor = root.right
        while successor.left:
            successor = successor.left
        root.val = successor.val
        root.right = bst_delete(root.right, successor.val)
    return root
```

### Example 2: Validating BST via Bounding Ranges
```python
def is_valid_bst(root, low=float("-inf"), high=float("inf")):
    if not root:
        return True
    if not (low < root.val < high):
        return False
    return (is_valid_bst(root.left, low, root.val) and
            is_valid_bst(root.right, root.val, high))
```

### Example 3: BST Iterator ($O(h)$ Memory)
```python
class BSTIterator:
    def __init__(self, root):
        self.stack = []
        self._push_left(root)

    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def next(self):
        node = self.stack.pop()
        if node.right:
            self._push_left(node.right)
        return node.val

    def hasNext(self):
        return len(self.stack) > 0
```

---

## 6. Output

```
1. Insertion & Inorder Traversal:
   Values: [50, 30, 70, 20, 40, 60, 80]
   Inorder: [20, 30, 40, 50, 60, 70, 80] (strictly sorted)

2. Search:
   Search 40 -> Found
   Search 99 -> Not Found

3. Deletions:
   After deleting leaf (20)        : [30, 40, 50, 60, 70, 80]
   After deleting 1-child node (30): [40, 50, 60, 70, 80]
   After deleting 2-child root (50): [40, 60, 70, 80]

4. Validation:
   Valid Tree   -> True
   Invalid Tree -> False
```

---

## 7. Code Explanation

| Component | Responsibility |
|---|---|
| `successor = find_min(root.right)` | Finds smallest node greater than current node to maintain BST ordering |
| `low < root.val < high` | Propagates ancestor boundaries downward to catch indirect subtree violations |
| `stack` in BSTIterator | Emulates runtime call stack for lazy traversal using only $O(h)$ memory |
| `curr = curr.left` loop | Traverses to the leftmost boundary to reach smallest available element |
| `root.val = successor.val` | Replaces value without unlinking complicated child subtrees |

---

## 8. Common Mistakes

1. **Local-Only BST Validation Trap**:
   Only comparing a node against its immediate children misses violations where a right-subtree grandchild is smaller than the parent.
2. **Duplicate Value Handling**:
   Standard BST definitions assume strictly unique keys ($< and >$). Allowing duplicates requires explicit conventions (e.g. $\le$ in left subtree).
3. **Memory Explosion in Inorder Traversal**:
   Storing full inorder traversal in a list to find the $K$-th element takes $O(n)$ space; using controlled stack or early exit takes $O(h)$.
4. **Deleting Successor Value Incorrectly**:
   Failing to recursively delete the successor from `root.right` leaves duplicate values in the tree.
5. **Degradation into Linked List**:
   Inserting already-sorted data into an unbalanced BST creates an $O(n)$ skewed tree, degrading search to linear scan.

---

## 9. Practice Questions

1. Implement **Lowest Common Ancestor (LCA) in a BST** in $O(h)$ time using the BST ordering property.
2. Convert a Sorted Array into a Height-Balanced Binary Search Tree.
3. Implement `trimBST(root, low, high)` to prune all nodes outside $[low, high]$.
4. Find the Inorder Successor and Predecessor for a given node in a BST.
5. Recover a Binary Search Tree where two nodes were swapped by mistake in $O(1)$ space.

---

## 10. Interview Questions

**Q1: What is the difference between Binary Tree and Binary Search Tree?**
A binary tree only requires that each node has at most two children. A binary search tree adds the ordering invariant: all left subtree keys $<$ node key $<$ all right subtree keys.

**Q2: What is the worst-case time complexity of BST operations, and how is it resolved?**
In the worst case (skewed tree caused by sorted inserts), operations take $O(n)$ time. Self-balancing binary search trees (AVL Trees, Red-Black Trees) resolve this by performing tree rotations to enforce $O(\log n)$ height.

**Q3: How does LCA in a BST differ from LCA in a general Binary Tree?**
In a general tree, both subtrees must be searched recursively ($O(n)$). In a BST, if both targets are smaller than root, go left; if both are larger, go right; the first node where paths diverge is the LCA ($O(h)$ time).

**Q4: Can we delete a 2-child node by replacing it with its inorder predecessor instead of successor?**
Yes. Both the inorder predecessor (maximum of left subtree) and inorder successor (minimum of right subtree) are valid replacements that preserve the BST ordering invariant.

**Q5: What is the amortized time complexity of `next()` in `BSTIterator`?**
$O(1)$ amortized time. Although an individual call to `next()` may push up to $h$ nodes onto the stack, each of the $n$ nodes in the tree is pushed and popped exactly once across the full iteration ($O(n) / n = O(1)$ per step).
