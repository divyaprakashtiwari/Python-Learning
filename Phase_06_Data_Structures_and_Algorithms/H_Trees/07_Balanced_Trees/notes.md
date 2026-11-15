# Balanced Trees

## 1. Introduction

A **Balanced Tree** is a tree data structure designed to maintain a logarithmic height **$O(\log n)$** even under dynamic insertions and deletions.

In a standard Binary Search Tree (BST), inserting elements in sorted or nearly-sorted order degenerates the tree into a linked list with $O(n)$ height, rendering search, insertion, and deletion linear. Self-balancing binary search trees (such as **AVL Trees** and **Red-Black Trees**) continuously perform local pointer rewirings called **tree rotations** to guarantee that the height remains strictly bounded by $O(\log n)$.

---

## 2. Why Use Balanced Trees?

| Tree Structure | Search Time | Insert Time | Delete Time | Max Height Bound |
|---|---|---|---|---|
| **Unbalanced BST (Worst Case)** | $O(n)$ | $O(n)$ | $O(n)$ | $n$ |
| **AVL Tree** | **$O(\log n)$** | **$O(\log n)$** | **$O(\log n)$** | $\approx 1.44 \log_2 n$ (Strictly balanced) |
| **Red-Black Tree** | **$O(\log n)$** | **$O(\log n)$** | **$O(\log n)$** | $\le 2 \log_2(n+1)$ (Faster insertions) |
| **B-Tree / B+ Tree** | **$O(\log n)$** | **$O(\log n)$** | **$O(\log n)$** | Disk-page optimized multi-way balance |

---

## 3. Definition of Height-Balanced

A binary tree is defined as **height-balanced** if, for every node in the tree:
$$\text{Balance Factor } BF = \text{height}(Left) - \text{height}(Right)$$
$$BF \in \{-1, 0, 1\}$$

If $|BF| > 1$ at any node, the tree is considered unbalanced and requires rebalancing.

---

## 4. Key Algorithmic Mechanics: The 4 AVL Rotations

When an insertion causes an imbalance ($|BF| > 1$), exactly one of 4 rotation configurations applies:

### 1. Left-Left (LL) Case $\implies$ Single Right Rotation
The inserted key is smaller than the left child's key ($BF > 1$ and $key < left.key$).
```
    z                                y
   / \      Right Rotate(z)        /   \
  y   T4    --------------->      x     z
 / \                             / \   / \
x   T3                          T1 T2 T3 T4
```

### 2. Right-Right (RR) Case $\implies$ Single Left Rotation
The inserted key is greater than the right child's key ($BF < -1$ and $key > right.key$).
```
  z                                  y
 / \        Left Rotate(z)         /   \
T1  y       ------------->        z     x
   / \                           / \   / \
  T2  x                         T1 T2 T3 T4
```

### 3. Left-Right (LR) Case $\implies$ Left Rotate child, then Right Rotate root
The inserted key is in the right subtree of the left child.

### 4. Right-Left (RL) Case $\implies$ Right Rotate child, then Left Rotate root
The inserted key is in the left subtree of the right child.

---

## 5. Examples

### Example 1: Checking Balance in $O(n)$ Time
```python
def is_balanced(root):
    def check(node):
        if not node:
            return 0
        left_h = check(node.left)
        if left_h == -1: return -1
        right_h = check(node.right)
        if right_h == -1: return -1
        if abs(left_h - right_h) > 1:
            return -1
        return 1 + max(left_h, right_h)
    return check(root) != -1
```

### Example 2: Sorted Array to Balanced BST
```python
def sorted_array_to_bst(nums):
    def build(l, r):
        if l > r: return None
        mid = (l + r) // 2
        root = TreeNode(nums[mid])
        root.left = build(l, mid - 1)
        root.right = build(mid + 1, r)
        return root
    return build(0, len(nums) - 1)
```

### Example 3: AVL Tree Right Rotation
```python
def right_rotate(y):
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    x.height = 1 + max(get_height(x.left), get_height(x.right))
    return x
```

---

## 6. Output

```
1. Balance Verification:
   Tree 1 (Balanced)   -> True
   Tree 2 (Unbalanced) -> False

2. Sorted Array to Balanced BST:
   Input Array: [-10, -3, 0, 5, 9]
   Root Value : 0
   Height     : 3 (Strictly O(log n))

3. AVL Insertion (10, 20, 30, 40, 50, 25):
   Inserted 10 -> Root: 10, Height: 1
   Inserted 20 -> Root: 10, Height: 2
   Inserted 30 -> Root: 20, Height: 2 (Rotated RR -> balanced)
   Inserted 40 -> Root: 20, Height: 3
   Inserted 50 -> Root: 20, Height: 3 (Rotated RR -> balanced)
   Inserted 25 -> Root: 30, Height: 3 (Rotated RL -> balanced)
   Final Height: 3 (vs 6 in unbalanced BST)
```

---

## 7. Code Explanation

| Mechanism | Purpose |
|---|---|
| Return `-1` Sentinel | Prunes recursion as soon as an imbalance is discovered anywhere in the tree |
| `mid = (left + right) // 2` | Ensures equal node distribution across left and right subtrees in divide-and-conquer |
| `x.right = y; y.left = T2` | Re-links child pointers in $O(1)$ time without modifying underlying data values |
| Height recalculation `y` before `x` | Rotated child `y` must have its height updated before parent `x` reads it |
| `balance = height(L) - height(R)` | Identifies direction of subtree skewness to trigger correct rotation |

---

## 8. Common Mistakes

1. **Naive $O(n^2)$ Balance Checking**:
   Calling a separate `height()` helper at each node recomputes heights repeatedly. Use a bottom-up post-order check that returns $-1$ on imbalance.
2. **Updating Rotated Parent Height before Child**:
   In a rotation, $y$ becomes the child of $x$. Calculating $x$'s height before updating $y$'s height produces stale height values.
3. **Missing Double Rotations (LR and RL)**:
   Attempting a single right rotation on a Left-Right zigzag imbalance fails to balance the tree; it must be converted to Left-Left first.
4. **Modifying Inorder Keys During Rotation**:
   Rotations must preserve the BST ordering invariant. Only tree pointers change, never node values.
5. **Overhead of AVL vs Red-Black Trees**:
   AVL trees are more rigidly balanced (maximum height $1.44 \log_2 n$), making them faster for lookups but slower on frequent inserts/deletes compared to Red-Black trees.

---

## 9. Practice Questions

1. Implement `balanceBST(root)` to balance an arbitrary unbalanced Binary Search Tree in $O(n)$ time.
2. Convert a Sorted Singly Linked List to Balanced BST in $O(n)$ time using inorder simulation.
3. Implement node deletion in an AVL Tree with balance factor restoration.
4. Check whether a binary tree satisfies the Complete Binary Tree property in $O(n)$ time.
5. Implement a Treap (Cartesian Tree combining BST key property and Heap priority property).

---

## 10. Interview Questions

**Q1: What is the difference between an AVL Tree and a Red-Black Tree?**
AVL trees enforce a strict balance condition ($|BF| \le 1$), resulting in shorter heights ($\approx 1.44 \log_2 n$) and faster lookups. Red-Black trees allow slightly looser balance (height up to $2 \log_2(n+1)$), requiring fewer rotations on insertions and deletions ($O(1)$ rotations).

**Q2: What is the time complexity of an AVL tree rotation?**
$O(1)$ time. A rotation involves updating a constant number of node pointers (`left`, `right`) and recalculating node heights for the two rotated nodes.

**Q3: How many rotations are required after an insertion into an AVL tree?**
At most **one** single or double rotation is required along the path to the root. Once the lowest unbalanced ancestor is rotated, its height is restored to its pre-insertion value, restoring balance to all higher ancestors.

**Q4: How many rotations are required after a deletion in an AVL tree?**
Up to $O(\log n)$ rotations. Unlike insertion, rebalancing a subtree after deletion can reduce its height, potentially propagating imbalances up to the root.

**Q5: Why is Red-Black tree preferred over AVL tree in standard libraries (like C++ `std::map` or Java `TreeMap`)?**
Because real-world applications typically have mixed workloads of inserts, deletes, and lookups. The looser balance of Red-Black trees reduces the overhead of constant rebalancing during writes while still guaranteeing $O(\log n)$ lookup bounds.
