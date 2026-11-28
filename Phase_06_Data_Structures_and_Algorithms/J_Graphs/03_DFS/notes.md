# Topic 03: Depth-First Search (DFS)

Depth-First Search (DFS) is a fundamental graph and tree traversal algorithm that explores as deep as possible along each branch before backtracking. It operates under a **Last-In, First-Out (LIFO)** strategy, either implicitly through the system recursion call stack or explicitly via a stack data structure.

---

## 1. Introduction to Depth-First Search

Unlike Breadth-First Search (BFS), which explores nodes layer-by-layer like ripples in a pond, DFS dives straight down a path until it reaches a dead end (a node with no unvisited neighbors). It then backtracks to the previous node and continues exploring remaining unexplored branches.

### Core Properties
- **Exploration Order:** Depth-oriented (follows a branch until exhaustion before backtracking).
- **Underlying Mechanism:** LIFO (Call Stack or Explicit `list` stack).
- **Time Complexity:** $O(V + E)$ where $V$ is vertices and $E$ is edges (for adjacency lists).
- **Space Complexity:** $O(V)$ in the worst case (e.g., skewed chain-like graph or recursion call stack).

---

## 2. Why Use DFS & Real-World Applications

DFS is the primary algorithmic engine behind many complex graph and tree problems:
1. **Topological Sorting:** Ordering dependencies (e.g., build systems, course prerequisites) using post-order DFS timestamps.
2. **Cycle Detection:** Detecting back-edges in directed and undirected graphs.
3. **Connected Components & Flood Fill:** Identifying clusters of connected nodes (e.g., islands in a 2D grid, image editing paint bucket tools).
4. **Pathfinding & Backtracking:** Finding all paths from a source to a target (e.g., maze solving, N-Queens, Sudoku).
5. **Biconnectivity & Bridges (Tarjan's / Kosaraju's):** Finding critical connections and articulation points in computer networks.

---

## 3. Syntax and Core Mechanics

### Recursive Template
```python
def dfs(node: int, visited: set) -> None:
    visited.add(node)
    # Process current node (pre-order)
    for neighbor in adj[node]:
        if neighbor not in visited:
            dfs(neighbor, visited)
    # Post-order processing (backtracking hook)
```

### Iterative Template (Explicit Stack)
```python
def dfs_iterative(start_node: int) -> List[int]:
    visited = set()
    stack = [start_node]
    order = []

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        for neighbor in reversed(adj[node]):
            if neighbor not in visited:
                stack.append(neighbor)
    return order
```

---

## 4. DFS Edge Classification

When running DFS on a directed graph, edges can be classified into four distinct types:
1. **Tree Edges:** Edges pointing to newly discovered nodes in the DFS tree.
2. **Back Edges:** Edges pointing to an active ancestor in the current recursion stack (indicates a **cycle**).
3. **Forward Edges:** Non-tree edges pointing from an ancestor to an already visited descendant.
4. **Cross Edges:** Edges pointing from one subtree to another already visited branch without ancestor-descendant relation.

---

## 5. Practical Examples

### Example 1: Recursive vs Iterative DFS & Disconnected Forest
- File: `example_01_dfs_recursive_and_iterative.py`
- Implements both recursive DFS and explicit-stack iterative DFS.
- Shows discovery (pre-order) and finish (post-order) orderings.
- Traverses a disconnected graph with multiple independent components.

### Example 2: 2D Grid DFS (Islands, Max Area, and Flood Fill)
- File: `example_02_number_of_islands_and_flood_fill.py`
- Implements LeetCode 200 (Number of Islands) via 4-directional grid exploration.
- Implements LeetCode 695 (Max Area of Island) computing area by summing recursive branches.
- Implements LeetCode 733 (Flood Fill) performing in-place replacement of matching colors.

### Example 3: Path Finding and DFS Backtracking
- File: `example_03_path_sum_and_all_paths_source_to_target.py`
- Implements LeetCode 797 (All Paths from Source to Target in a DAG).
- Demonstrates backtracking in cyclic graphs by adding and removing visited nodes.
- Evaluates path weights to find all simple paths matching a target weight sum.

---

## 6. Output & Verification Walkthrough

Running each example yields clean, deterministic ASCII output:
```
============================================================
1. Recursive vs Iterative DFS Traversal
============================================================
Graph Nodes           : [0, 1, 2, 3, 4, 5, 6]
Recursive DFS Order   : [0, 1, 3, 4, 6, 5, 2]
Iterative DFS Order   : [0, 1, 3, 4, 6, 5, 2]
Pre-order (Discovery) : [0, 1, 3, 4, 6, 5, 2]
Post-order (Finish)   : [3, 6, 5, 2, 4, 1, 0]

============================================================
2. Disconnected Graph DFS (Forest Components)
============================================================
Total Disconnected Components: 3
  Component 1: [10, 20, 30]
  Component 2: [40, 50]
  Component 3: [60]
```

Grid operations:
```
Total Islands Count: 3
Maximum Connected Island Area: 4
```

---

## 7. In-Depth Code Explanation

### Backtracking Pattern in DFS
When finding *all* paths rather than just *any* path, state must be restored:
```python
path.append(node)
visited.add(node)
for neighbor in adj[node]:
    if neighbor not in visited:
        dfs(neighbor)
visited.remove(node)  # Un-mark node for alternative exploration branches
path.pop()            # Restore path state
```
Without `visited.remove(node)` and `path.pop()`, once a node is visited along one path, alternative valid paths through that node would be erroneously skipped.

---

## 8. Common Pitfalls & Mistakes

1. **Python Recursion Limit (`RecursionError`):**
   - Python defaults to a recursion depth limit of 1000 (`sys.getrecursionlimit()`).
   - For deep or linear graphs ($V = 10^5$), recursive DFS will throw `RecursionError: maximum recursion depth exceeded`.
   - **Fix:** Use `sys.setrecursionlimit(200000)` or prefer the explicit iterative stack DFS.

2. **Forgetting to Mark Visited Immediately:**
   - In graphs with cycles, failing to mark nodes as visited before recursing into neighbors leads to infinite recursion and stack overflow.

3. **In-place Grid Mutation Side Effects:**
   - Sinking islands in 2D grids (`grid[r][c] = '0'`) mutates caller input. Always make a shallow/deep copy or use a `visited` set if input preservation is required.

4. **Missing Disconnected Components:**
   - Starting DFS from only node `0` will miss any isolated subgraphs. Always loop through all vertices to check `if v not in visited`.

---

## 9. 5 Practice Questions

1. **Reconstruct Itinerary (LeetCode 332):** Given airline tickets `[from, to]`, reconstruct the itinerary in lexicographical order using Hierholzer's Eulerian path DFS.
2. **Surrounded Regions (LeetCode 130):** Capture regions surrounded by `'X'` on a 2D board by running DFS from the boundary `'O'` cells first.
3. **Pacific Atlantic Water Flow (LeetCode 417):** Run multi-source reverse DFS inward from ocean borders to find grid cells that can drain to both oceans.
4. **Evaluate Division (LeetCode 399):** Model equations `A / B = k` as a directed weighted graph and run DFS to evaluate query quotients.
5. **Path Sum II (LeetCode 113):** Find all root-to-leaf paths in a binary tree where path sum equals target sum.

---

## 10. 5 Real-World Interview Questions

1. **Q: When would you choose DFS over BFS for pathfinding?**
   - **A:** When we need to find *any* path rather than the *shortest* path, when memory is constrained on wide tree/graph structures ($O(h)$ vs $O(w)$), or when solving backtracking puzzles like mazes and Sudoku.

2. **Q: How does DFS detect cycles in a directed graph versus an undirected graph?**
   - **A:** In an undirected graph, encountering an already visited neighbor that is *not* the immediate parent node indicates a cycle. In a directed graph, we must track the current recursion stack (e.g. 3-state coloring: unvisited, visiting, visited); encountering a node currently in the `visiting` state (a back-edge) indicates a directed cycle.

3. **Q: What is the time complexity of finding all paths from source to target in a DAG?**
   - **A:** In the worst-case (a complete DAG where every node points to all higher-numbered nodes), there are $2^{V-2}$ distinct paths, each taking $O(V)$ time to construct, leading to $O(2^V \cdot V)$ time complexity.

4. **Q: Why does Kahn's algorithm use BFS while reverse post-order uses DFS for Topological Sort?**
   - **A:** Kahn's uses BFS with indegrees because nodes with 0 incoming edges are ready to be processed. DFS visits nodes deeply first; by appending nodes to a list upon finishing (post-order) and reversing it, every prerequisite comes before its dependents.

5. **Q: How do you prevent stack overflow in deep DFS in Python?**
   - **A:** Either rewrite the traversal using an explicit list as a stack (`while stack: node = stack.pop()`), or increase the recursion limit via `sys.setrecursionlimit()`, though the explicit stack is safer and portable across runtimes.
