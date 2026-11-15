# Height and Depth of Binary Trees

## 1. Introduction

**Height** and **Depth** are fundamental vertical metrics that quantify the scale, balance, and complexity of a binary tree:
- **Depth of a Node:** The number of edges (or nodes) on the unique path from the tree's root down to that specific node. (The root is at depth 0).
- **Height of a Node:** The number of edges (or nodes) on the longest downward path from that node to a leaf. (A leaf node has height 0).
- **Height of a Tree:** The height of its root node, which is identical to the maximum depth among all nodes in the tree.

---

## 2. Why Understand Height and Depth?

| Concept / Metric | Algorithmic Consequence | Key Application |
|---|---|---|
| **Tree Height $h$** | Governs worst-case runtime $O(h)$ for search, insertion, and deletion | Proving operational bounds of BSTs |
| **Diameter** | Longest path between any two nodes ($left\_h + right\_h$) | Network routing latency & graph eccentricity |
| **Minimum Depth** | Shortest path from root to true leaf | BFS early-exit optimization |
| **Balanced Tree Check** | $|height(left) - height(right)| \le 1$ | AVL and Red-Black tree rebalancing |
| **Maximum Path Sum** | Subtree gain propagation with dynamic programming | Divide-and-conquer optimization |

---

## 3. Syntax / Core Formulations

```python
# Recursive Maximum Depth (Node Count Definition)
def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

# Edge Count Definition
def height_edges(root):
    if not root or (not root.left and not root.right):
        return 0
    return 1 + max(height_edges(root.left), height_edges(root.right))
```

---

## 4. Key Algorithmic Mechanics

### 1. The Minimum Depth Trap
In minimum depth, the goal is reaching a **true leaf** (both left and right children are `None`).
If a node has only one child, we cannot simply take `min(depth(left), depth(right))` because `depth(None)` is 0, which would falsely declare the current non-leaf node as a leaf! We must explore down the non-empty child branch.

### 2. Tree Diameter via Bottom-Up Post-Order
The longest path passing through any node $u$ has length `height(u.left) + height(u.right)` (in edges).
By calculating subtree heights bottom-up, we compute the height in $O(1)$ per node while maintaining a global `max_diameter = max(max_diameter, left_h + right_h)`.

### 3. Maximum Path Sum with Negative Truncation
Any subtree returning a negative contribution can be dropped (`max(gain, 0)`). The maximum path price through node $u$ is `u.val + left_gain + right_gain`. The value returned to the parent is `u.val + max(left_gain, right_gain)`.

---

## 5. Examples

### Example 1: Maximum Depth & Minimum Depth (BFS Early Exit)
```python
def min_depth(root):
    if not root:
        return 0
    q = deque([(root, 1)])
    while q:
        node, depth = q.popleft()
        if not node.left and not node.right:
            return depth
        if node.left: q.append((node.left, depth + 1))
        if node.right: q.append((node.right, depth + 1))
    return 0
```

### Example 2: Diameter of Binary Tree
```python
class Solution:
    def diameterOfBinaryTree(self, root):
        self.diameter = 0
        def height(node):
            if not node:
                return 0
            left = height(node.left)
            right = height(node.right)
            self.diameter = max(self.diameter, left + right)
            return 1 + max(left, right)
        height(root)
        return self.diameter
```

### Example 3: Deepest Leaves Sum
```python
def deepest_leaves_sum(root):
    q = deque([root])
    while q:
        level_sum = 0
        for _ in range(len(q)):
            node = q.popleft()
            level_sum += node.val
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
    return level_sum
```

---

## 6. Output

```
Tree 1:
        3
       / \
      9  20
         / \
        15  7

1. Max Depth (DFS): 3
2. Max Depth (BFS): 3
3. Min Depth (BFS): 2 (path: 3 -> 9)

Skewed Tree (2 -> 3 -> 4 -> 5 -> 6):
Max Depth: 5
Min Depth: 5 (correctly bypassed single-child nodes)

Tree Diameter (Edges): 3
Maximum Path Sum     : 42
Deepest Leaves Sum   : 15
```

---

## 7. Code Explanation

| Component | Responsibility |
|---|---|
| `1 + max(left, right)` | Standard bottom-up height aggregation formula |
| `if not node.left and not node.right:` | Identifies terminal leaf node to trigger immediate BFS exit |
| `max_diameter = max(d, left_h + right_h)` | Tracks global diameter without re-traversing subtrees |
| `max(gain, 0)` | Clamps negative subtree branches to avoid reducing total path sum |
| `level_sum` overwritten in BFS | Automatically retains sum of nodes in the final deepest level |

---

## 8. Common Mistakes

1. **Incorrect Min Depth Base Case**:
   Writing `min(min_depth(left), min_depth(right))` on a skewed tree yields `0` instead of traversing down the real leaf path.
2. **Confusing Node Counts vs Edge Counts**:
   Some problems measure height/diameter by number of **edges** (paths of length $N-1$), while others measure by number of **nodes** ($N$). Always confirm problem convention.
3. **$O(n^2)$ Naive Diameter Calculation**:
   Calling a separate `height()` function inside each node traversal results in $O(n^2)$ runtime. Both height and diameter must be calculated together in a single $O(n)$ post-order pass.
4. **Returning Split Path to Parent in Max Path Sum**:
   A path cannot branch both ways once handed to a parent node. The parent can only receive `node.val + max(left_gain, right_gain)`.
5. **Call Stack Overflow on Degenerate Trees**:
   Recursive height functions on linked-list style trees with $n = 10^5$ nodes exhaust Python's recursion limit.

---

## 9. Practice Questions

1. Implement **Balanced Binary Tree Check** in $O(n)$ time using $-1$ height sentinel on imbalance.
2. Calculate the maximum width of a binary tree (using heap/level index subtraction).
3. Find the length of the longest univalue path in a binary tree.
4. Count the number of complete tree nodes in less than $O(n)$ time using binary search and height comparison ($O(\log^2 n)$).
5. Find the sum of distances from the root to all leaf nodes in a binary tree.

---

## 10. Interview Questions

**Q1: What is the difference between node depth and node height?**
Depth measures distance from the root downward to the node. Height measures distance from the node downward to its deepest leaf. The root has depth 0 and maximum height; a leaf has height 0 and maximum depth.

**Q2: How does computing diameter in $O(n)$ differ from $O(n^2)$?**
The naive $O(n^2)$ approach calculates `height(left)` and `height(right)` independently at each node by re-traversing subtrees. The $O(n)$ approach computes heights bottom-up during post-order traversal and updates the global diameter variable simultaneously.

**Q3: Why is BFS superior for finding Minimum Depth?**
Because BFS visits nodes in increasing order of depth, the first leaf node dequeued is guaranteed to be at the minimum depth, allowing immediate termination without visiting the remainder of the tree.

**Q4: Can the diameter of a binary tree not pass through the root node?**
Yes. If one of the subtrees (e.g., left subtree) is exceptionally deep and wide, the longest path between two leaves may be entirely contained within that left subtree without touching the root.

**Q5: How do negative numbers alter the Maximum Path Sum problem?**
If a subtree path yields a sum $< 0$, including it will only decrease the overall path sum. Hence, negative gains are clamped to `0`, effectively treating those subtrees as empty.
