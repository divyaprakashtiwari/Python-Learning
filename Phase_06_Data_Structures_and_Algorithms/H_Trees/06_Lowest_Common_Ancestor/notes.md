# Lowest Common Ancestor (LCA)

## 1. Introduction

The **Lowest Common Ancestor (LCA)** of two nodes $p$ and $q$ in a tree is defined as the deepest node $T$ that has both $p$ and $q$ as descendants (where a node is allowed to be a descendant of itself).

LCA is one of the foundational graph and tree queries in computer science, used extensively in phylogenetic tree analysis, network multicast routing, object-oriented class hierarchy resolution, and computing shortest paths on trees.

---

## 2. Why Use Lowest Common Ancestor?

| Tree Type | LCA Technique | Time Complexity | Space Complexity |
|---|---|---|---|
| **General Binary Tree (Pointer)** | Post-order DFS Divide-and-Conquer | $O(n)$ | $O(h)$ |
| **Binary Search Tree (BST)** | Range Split Comparison | **$O(h)$** | **$O(1)$** iterative |
| **Nodes with Parent Pointers** | Two-Pointer List Intersection | $O(h)$ | **$O(1)$** |
| **Tree with Distance Queries** | Binary Lifting (Euler Tour) | $O(\log n)$ query ($O(n \log n)$ prep) | $O(n \log n)$ table |
| **LCA of Deepest Leaves** | Equal-Depth Subtree Matching | $O(n)$ | $O(h)$ |

---

## 3. Syntax / API Reference

### Recursive General Binary Tree LCA
```python
def lowestCommonAncestor(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    if left and right:
        return root
    return left or right
```

### Iterative BST LCA
```python
def lowestCommonAncestorBST(root, p, q):
    curr = root
    while curr:
        if p.val < curr.val and q.val < curr.val:
            curr = curr.left
        elif p.val > curr.val and q.val > curr.val:
            curr = curr.right
        else:
            return curr
    return None
```

---

## 4. Key Algorithmic Mechanics

### 1. General Binary Tree (Post-Order Split-Point Detection)
- Traverse left and right subtrees recursively.
- If both subtrees return non-null, the current node is the convergence split-point where $p$ and $q$ reside in different branches $\implies$ current node is the LCA.
- If only one subtree returns non-null, propagate that non-null node upward.
- If current node is $p$ or $q$, immediately return current node (handles case where $p$ is an ancestor of $q$).

### 2. Binary Search Tree (O(h) Value Steering)
We do not need to search both subtrees in a BST:
- If both $p.val$ and $q.val$ are smaller than `root.val`, LCA must lie strictly in the left subtree.
- If both are greater, LCA must lie strictly in the right subtree.
- The very first node where $p$ and $q$ split into different branches (or one equals `root.val`) is the unique LCA.

### 3. Tree with Parent Pointers as Linked List Intersection
If each node has a `.parent` reference, the path from $p$ to the root and $q$ to the root are two converging singly linked lists. Using the standard two-pointer list intersection algorithm (`a = a.parent if a else q`) finds their meeting point in $O(1)$ space.

---

## 5. Examples

### Example 1: General Binary Tree LCA (Recursive & Iterative)
```python
def lca_iterative(root, p, q):
    parent = {root: None}
    stack = [root]
    while p not in parent or q not in parent:
        node = stack.pop()
        if node.left:
            parent[node.left] = node
            stack.append(node.left)
        if node.right:
            parent[node.right] = node
            stack.append(node.right)
    ancestors = set()
    while p:
        ancestors.add(p)
        p = parent[p]
    while q not in ancestors:
        q = parent[q]
    return q
```

### Example 2: LCA in a Binary Search Tree
```python
def lca_bst(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
    return None
```

### Example 3: LCA of Deepest Leaves
```python
def lca_deepest_leaves(root):
    def dfs(node):
        if not node:
            return None, 0
        l_node, l_depth = dfs(node.left)
        r_node, r_depth = dfs(node.right)
        if l_depth == r_depth:
            return node, l_depth + 1
        return (l_node, l_depth + 1) if l_depth > r_depth else (r_node, r_depth + 1)
    return dfs(root)[0]
```

---

## 6. Output

```
Tree:
        3
       / \
      5   1
     / \  / \
    6  2 0   8
      / \
     7   4

1. LCA of 5 and 1: 3
2. LCA of 5 and 4: 5 (5 is ancestor of 4)
3. BST LCA of 2 and 8 in BST: 6
4. LCA with parent pointers (6 and 2): 5
5. LCA of deepest leaves (7 and 4): 2
```

---

## 7. Code Explanation

| Logic | Function |
|---|---|
| `if root in (None, p, q): return root` | Immediate short-circuit returning target reference up call stack |
| `if left and right: return root` | Signals that $p$ and $q$ were found in opposite subtrees of `root` |
| `return left or right` | Passes single detected descendant up to ancestors |
| `p.val < root.val and q.val < root.val` | Directs search into left BST subtree without exploring right |
| `a = a.parent if a else q` | Equilibrates length differences in parent paths to meet at LCA |

---

## 8. Common Mistakes

1. **Assuming $p$ and $q$ are Always in the Tree**:
   The classic recursive algorithm assumes both nodes exist. If one node is missing, it may return the single node found rather than `None`. A boolean presence check is needed if existence is not guaranteed.
2. **Missing Ancestor Self-Inclusion**:
   Forgetting that a node can be its own ancestor ($p$ is ancestor of $q$).
3. **Searching Both Subtrees in BST**:
   Treating a BST like a general tree and searching both branches loses the $O(h)$ advantage.
4. **Extra Space with Parent Dictionaries**:
   Allocating an $O(n)$ hash map when a simple $O(h)$ recursive DFS or $O(1)$ space BST traversal suffices.
5. **Node Identity vs Value Comparison**:
   Comparing `node.val == p.val` instead of object reference `node is p` when trees may contain duplicate values.

---

## 9. Practice Questions

1. Implement **LCA III** (nodes have parent pointers, no root provided) in $O(1)$ space.
2. Implement **LCA IV** (finding LCA of a list of $k$ nodes).
3. Compute distance between any two nodes in a tree using `dist(p, q) = depth(p) + depth(q) - 2 * depth(LCA(p, q))`.
4. Solve LCA when target nodes might not exist in the tree (`lowestCommonAncestorExtended`).
5. Implement Tarjan's Off-line LCA algorithm using Disjoint Set Union (DSU) in $O(n + q \cdot \alpha(n))$ time.

---

## 10. Interview Questions

**Q1: What is the time and space complexity of finding LCA in a General Binary Tree?**
Time complexity is $O(n)$ because in the worst case we must visit all $n$ nodes. Auxiliary space is $O(h)$ on the recursion call stack ($O(\log n)$ balanced, $O(n)$ skewed).

**Q2: How does LCA simplify in a BST?**
In a BST, values guide traversal. If both targets are less than root, go left; if both are greater, go right. The first node where values branch is the LCA, taking $O(h)$ time and $O(1)$ space without visiting both subtrees.

**Q3: How do you find distance between two nodes using LCA?**
Let $L = \text{LCA}(p, q)$. Then:
$\text{distance}(p, q) = \text{depth}(p) + \text{depth}(q) - 2 \cdot \text{depth}(L)$.

**Q4: What if node $p$ exists in the tree but node $q$ does not?**
The standard LeetCode 236 algorithm will return $p$ because it sees $p$ and bubbles it up. To handle missing nodes, we must either run a second search to verify $q$'s existence or use a bottom-up counter that returns the LCA only when both targets are confirmed visited.

**Q5: What is Binary Lifting for LCA?**
Binary Lifting is an $O(\log n)$ query method used on large trees ($10^5$ queries). It precomputes an `up[node][i]` table storing the $2^i$-th ancestor of each node in $O(n \log n)$ time, allowing LCA to be located in $O(\log n)$ by jumping powers of 2.
