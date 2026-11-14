# Level Order Traversal (BFS)

## 1. Introduction

**Level Order Traversal** (also known as Breadth-First Search on Trees) visits tree nodes horizon-by-horizon, starting from the root node at depth 0 and proceeding downward level by level, processing nodes on each level strictly from left to right.

Unlike Depth-First Search (DFS) which relies on a LIFO stack to explore along deep branch paths, Level Order Traversal relies on a **FIFO Queue** (`collections.deque`) to guarantee that nodes at shallower depths are processed before any node at a deeper level.

---

## 2. Why Use Level Order Traversal?

| Problem Type | Standard DFS Time/Space | BFS Level Order Time/Space | Core Advantage |
|---|---|---|---|
| **Shortest Path to Leaf / Min Depth** | $O(n)$ time (full traversal) | $O(\text{min\_depth})$ time | Stops immediately upon finding the first leaf |
| **Tree Side Views (Right/Left)** | $O(n)$ time & $O(h)$ space | $O(n)$ time & $O(w)$ space | Directly extracts boundary items per level size |
| **Zigzag / Spiral Traversal** | Reversing subtrees | Double-ended level deque | Alternates insertion end at each level boundary |
| **Level-wise Aggregations** | Grouping array indices | Direct per-level loop | Calculates level averages/sums in one clean pass |
| **Connecting Next Right Pointers** | Complex pointer tracking | Natural level queue / $O(1)$ dummy | Links horizontal siblings directly |

---

## 3. Syntax / BFS Template

```python
from collections import deque

def level_order_template(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level_size = len(queue)
        current_level = []
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(current_level)
    return result
```

---

## 4. Key Algorithmic Mechanics

### 1. Snapshotting Level Size
The defining pattern of multi-level BFS is capturing `level_size = len(queue)` at the start of each while iteration. Because child nodes are enqueued inside the loop, using a fixed `for _ in range(level_size)` loop isolates the current horizontal level cleanly from newly discovered children.

### 2. Side Views of Binary Tree
- **Right Side View:** The last element (`i == level_size - 1`) processed in each level loop.
- **Left Side View:** The first element (`i == 0`) processed in each level loop.

### 3. $O(1)$ Space Pointer Connection via Dummy Sentinel
To populate horizontal `next` pointers without a queue:
Use the already-established `next` pointers on the parent level like a linked list, using a dummy node (`dummy = Node(0); tail = dummy`) to stitch together the child level below.

---

## 5. Examples

### Example 1: Standard & Zigzag Level Order Traversal
```python
def zigzag_level_order(root):
    if not root:
        return []
    res, q, l2r = [], deque([root]), True
    while q:
        level = deque()
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val) if l2r else level.appendleft(node.val)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
        res.append(list(level))
        l2r = not l2r
    return res
```

### Example 2: Binary Tree Right Side View
```python
def right_side_view(root):
    if not root:
        return []
    view, q = [], deque([root])
    while q:
        size = len(q)
        for i in range(size):
            node = q.popleft()
            if i == size - 1:
                view.append(node.val)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
    return view
```

### Example 3: Populating Next Right Pointers in $O(1)$ Space
```python
def connect(root):
    curr = root
    while curr:
        dummy = Node(0)
        tail = dummy
        while curr:
            if curr.left:
                tail.next = curr.left
                tail = tail.next
            if curr.right:
                tail.next = curr.right
                tail = tail.next
            curr = curr.next
        curr = dummy.next
    return root
```

---

## 6. Output

```
Tree:
        3
       / \
      9   20
         /  \
        15   7

1. Standard Level Order : [[3], [9, 20], [15, 7]]
2. Zigzag Level Order   : [[3], [20, 9], [15, 7]]
3. Right Side View      : [3, 20, 7]
4. Level Averages       : [3.0, 14.5, 11.0]
5. Connected Next Nodes :
   Level 0: 3 -> None
   Level 1: 9 -> 20 -> None
   Level 2: 15 -> 7 -> None
```

---

## 7. Code Explanation

| Mechanism | Purpose |
|---|---|
| `collections.deque` | Provides $O(1)$ amortized `popleft()` and `append()`, unlike $O(n)$ `list.pop(0)` |
| `level_size = len(queue)` | Freezes count of nodes at current depth before any children are added |
| `current_level.appendleft(val)` | Inverts ordering for odd-indexed levels in Zigzag traversal |
| `col - 1` and `col + 1` | Assigns horizontal x-coordinates for vertical/top tree view projections |
| `dummy.next` | Tracks the start of the next level without allocating auxiliary queue storage |

---

## 8. Common Mistakes

1. **Using `list.pop(0)` Instead of `collections.deque`**:
   `list.pop(0)` requires $O(n)$ time to shift remaining elements, degrading total BFS runtime to $O(n^2)$.
2. **Dynamic Queue Length Evaluation**:
   Iterating directly over `range(len(queue))` without snapshotting causes newly appended children to be processed within the same level loop.
3. **Queueing `None` Children Blindly**:
   Pushing `node.left` without checking if it is `None` pollutes the queue with `None` values and requires defensive `if node:` checks.
4. **Incorrect Level Flips in Zigzag**:
   Reversing after pushing children into the main queue instead of buffering within the level container corrupts child exploration order.
5. **Memory Constraints on Wide Trees**:
   A perfect binary tree of $n$ nodes has $n / 2$ leaves at its bottom level. The queue reaches $O(n)$ space complexity at its widest point.

---

## 9. Practice Questions

1. Find the **Minimum Depth of a Binary Tree** using BFS to terminate at the very first leaf encountered.
2. Implement **Vertical Order Traversal** of a Binary Tree using BFS with row/column coordinate sorting.
3. Find the largest value in each tree row using level order traversal.
4. Check if a binary tree is **Cousins** (nodes at the same depth with different parents).
5. Implement Deepest Leaves Sum in a single BFS pass.

---

## 10. Interview Questions

**Q1: What is the space complexity of Level Order Traversal on a binary tree?**
$O(w)$ where $w$ is the maximum width of the tree. In a balanced or perfect tree, the last level has $\lceil n / 2 \rceil$ nodes, requiring $O(n)$ auxiliary space in the worst case.

**Q2: Why is BFS preferred over DFS for finding the minimum depth of a tree?**
BFS explores nodes level-by-level. As soon as it encounters the first leaf node, it can immediately terminate and return its depth. DFS must explore all paths to all leaves before confirming the minimum, taking $O(n)$ time in all cases.

**Q3: How can we connect next right pointers in $O(1)$ space without a queue?**
By treating each already-connected level as a singly linked list and using a dummy head to weave together the children of the current level into a linked list for the next iteration.

**Q4: How does Top View differ from Vertical Order Traversal?**
Vertical order returns all nodes grouped by vertical column, whereas Top View returns only the single earliest-visited (topmost) node visible from each column.

**Q5: Can level order traversal be implemented recursively?**
Yes, by passing the current `level` index as a parameter in a DFS traversal and appending `node.val` to `result[level]`, creating new sublists as depth increases.
