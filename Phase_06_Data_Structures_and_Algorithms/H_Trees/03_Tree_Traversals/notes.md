# Tree Traversals

## 1. Introduction

A **Tree Traversal** is the systematic process of visiting (evaluating, modifying, or retrieving) each node in a tree data structure exactly once.

Unlike linear data structures (arrays, linked lists) which have an inherent sequential ordering, hierarchical trees can be traversed in several distinct ways depending on the relative order in which the root node and its children are processed. The primary Depth-First Search (DFS) traversals are:
1. **Pre-order:** $Root \to Left \to Right$
2. **In-order:** $Left \to Root \to Right$
3. **Post-order:** $Left \to Right \to Root$

---

## 2. Why Use Tree Traversals?

| Traversal Strategy | Visiting Order | Primary Practical Applications |
|---|---|---|
| **Pre-order DFS** | $Root \to L \to R$ | Tree cloning/copying, serialization, prefix expression evaluation (Polish notation) |
| **In-order DFS** | $L \to Root \to R$ | Sorted sequence generation in BSTs, tree validation, kth smallest element |
| **Post-order DFS** | $L \to R \to Root$ | Bottom-up calculations (height, subtree size), node deletion/garbage collection |
| **Morris Traversal** | Threaded in-place | Traversing trees in strictly **$O(1)$ auxiliary space** without recursion or stacks |

---

## 3. Syntax / Algorithmic Formats

### Recursive Form
```python
def preorder(node):
    if node:
        visit(node.val)
        preorder(node.left)
        preorder(node.right)
```

### Iterative Form (Stack-based)
```python
def iterative_inorder(root):
    stack, curr, res = [], root, []
    while stack or curr:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        res.append(curr.val)
        curr = curr.right
    return res
```

---

## 4. Key Traversal Mechanics

### 1. The Call Stack vs Explicit Stack
Every recursive tree traversal implicitly consumes $O(h)$ space on the runtime call stack, where $h$ is tree height. For deep or skewed trees ($h \approx n$), recursive solutions risk `RecursionError: maximum recursion depth exceeded`. Iterative approaches with an explicit heap-allocated `list` stack prevent call stack overflow.

### 2. Morris Traversal ($O(1)$ Space via Threaded Pointers)
Morris traversal achieves $O(1)$ auxiliary space by leveraging unused `None` right-child pointers of leaf nodes:
1. For current node `curr`, if `curr.left` exists, find its **inorder predecessor** (rightmost node in `curr.left`).
2. If `pred.right` is `None`: set `pred.right = curr` (create thread link), then advance `curr = curr.left`.
3. If `pred.right` is `curr`: thread already exists! Sever thread `pred.right = None`, visit `curr.val`, then advance `curr = curr.right`.

---

## 5. Examples

### Example 1: Recursive Pre-order, In-order, and Post-order
```python
def dfs_traversals(root):
    pre, ino, post = [], [], []
    def dfs(node):
        if not node:
            return
        pre.append(node.val)
        dfs(node.left)
        ino.append(node.val)
        dfs(node.right)
        post.append(node.val)
    dfs(root)
    return pre, ino, post
```

### Example 2: Iterative Pre-order & In-order
```python
def preorder_iterative(root):
    if not root:
        return []
    stack, res = [root], []
    while stack:
        node = stack.pop()
        res.append(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return res
```

### Example 3: Morris In-order Traversal ($O(1)$ Space)
```python
def morris_inorder(root):
    res, curr = [], root
    while curr:
        if not curr.left:
            res.append(curr.val)
            curr = curr.right
        else:
            pred = curr.left
            while pred.right and pred.right is not curr:
                pred = pred.right
            if not pred.right:
                pred.right = curr
                curr = curr.left
            else:
                pred.right = None
                res.append(curr.val)
                curr = curr.right
    return res
```

---

## 6. Output

```
Tree:
      1
     / \
    2   3
   / \
  4   5

Pre-order  : [1, 2, 4, 5, 3]
In-order   : [4, 2, 5, 1, 3]
Post-order : [4, 5, 2, 3, 1]

Morris In-order  : [4, 2, 5, 1, 3]
Morris Pre-order : [1, 2, 4, 5, 3]
Tree Structure Restored: True
```

---

## 7. Code Explanation

| Mechanism | Purpose |
|---|---|
| `stack.append(node.right)` before `node.left` | LIFO stack ensures left child is popped and processed first in preorder |
| `while curr: stack.append(curr); curr = curr.left` | Traverses down the left boundary until the smallest in-order node is reached |
| `pred.right = curr` | Establishes a temporary return pointer without allocating memory |
| `pred.right = None` | Restores original tree structure, clearing temporary thread pointers |
| `s2[::-1]` in postorder | Inverts $(Root \to Right \to Left)$ sequence into postorder $(Left \to Right \to Root)$ |

---

## 8. Common Mistakes

1. **Pushing Left before Right in Iterative Preorder**:
   Pushing left first causes the right child to be popped and visited before the left child.
2. **Infinite Loops in Morris Traversal**:
   Failing to check `pred.right is not curr` while locating the predecessor causes an infinite loop around the thread cycle.
3. **Failing to Revert Threaded Pointers**:
   Terminating early from Morris traversal leaves threaded links in the tree, permanently corrupting its structure.
4. **Stack Overflow on Large Skewed Trees**:
   Relying on default Python recursion limit (1000) for deep trees causes crash without `sys.setrecursionlimit` or iterative rewrites.
5. **Double Visiting Nodes in Iterative Inorder**:
   Popping from stack and immediately re-descending left causes duplicate node processing.

---

## 9. Practice Questions

1. Construct a Binary Tree from **Inorder and Preorder Traversal** arrays in $O(n)$ time.
2. Construct a Binary Tree from **Inorder and Postorder Traversal** arrays in $O(n)$ time.
3. Implement iterative Post-order Traversal using a single stack and a `prev` node pointer.
4. Verify if a given sequence can represent the preorder traversal of a Binary Search Tree.
5. Implement Boundary Traversal of a Binary Tree (Left boundary, Leaf nodes, Right boundary).

---

## 10. Interview Questions

**Q1: What is the time complexity of Morris Traversal?**
The time complexity is $O(n)$. Although each edge is traversed multiple times (once to build the thread, once to traverse, once to remove the thread), no edge is visited more than 3 times, giving $O(3n) = O(n)$ overall runtime.

**Q2: Why does Inorder traversal on a BST produce sorted order?**
Because the BST property guarantees that all values in the left subtree are smaller than the node, and all values in the right subtree are larger. Inorder recursively processes $Left \to Node \to Right$, directly following this ascending mathematical order.

**Q3: Which traversal is best suited for deleting a tree, and why?**
Post-order traversal ($Left \to Right \to Root$). Subtrees and children must be processed and deallocated before the parent node is deleted, ensuring parent references remain valid during child deletion.

**Q4: How can post-order traversal be derived from a modified pre-order traversal?**
Standard preorder is $Root \to Left \to Right$. If modified to $Root \to Right \to Left$ and the entire visited result list is reversed at the end, it yields $Left \to Right \to Root$, which is exactly post-order traversal.

**Q5: Can you reconstruct a tree with only Preorder and Postorder traversals?**
Only if the tree is a **Full Binary Tree** (every node has either 0 or 2 children). For general trees, Inorder traversal is mandatory to resolve left vs right subtree boundaries.
