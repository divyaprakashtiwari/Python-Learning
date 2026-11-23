# Breadth-First Search (BFS) on Graphs

## 1. Introduction

**Breadth-First Search (BFS)** is a fundamental graph traversal and search algorithm that systematically explores vertices in concentric layers or horizons. Starting from a source vertex, BFS explores all immediate neighbors (distance 1) before exploring vertices at distance 2, distance 3, and so on.

BFS is driven by a **FIFO Queue** (`collections.deque`) and a `visited` set. It guarantees finding the **shortest path (minimum number of edges)** between two vertices in any unweighted graph.

---

## 2. Why Use BFS on Graphs?

| Problem Type | DFS Approach | BFS Approach | Advantage of BFS |
|---|---|---|---|
| **Shortest Path (Unweighted)** | Explores deep non-optimal paths | Level-by-level wavefront | **Guaranteed minimum edges** |
| **Connected Components** | Visits deep component paths | Traverses each component horizon | Clear level partitioning |
| **Bipartite Graph Check** | 2-coloring recursion | 2-coloring level parity | Odd/even level parity matches color |
| **Multi-Source Spread** | Inefficient backtracking | Enqueue all sources initially | Simultaneous parallel wave propagation |
| **Minimum Moves / State Space** | Deep exploration / stack overflow | First state reached is shortest | Optimal for puzzle solving (Word Ladder, 15-puzzle) |

---

## 3. Syntax / Core BFS Template

```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])

    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if v not in visited:
                visited.add(v)  # Mark visited immediately upon enqueue!
                queue.append(v)
```

---

## 4. Key Algorithmic Mechanics

### 1. Marking Visited Immediately Upon Enqueue
A classic and critical BFS rule: **mark a node as visited at the moment it is pushed into the queue**, NOT when it is popped.
Failing to do so allows multiple currently-queued neighbors to enqueue the same vertex redundantly, leading to an exponential explosion in queue size and TLE / memory exhaustion.

### 2. Multi-Source BFS
When a phenomenon expands simultaneously from multiple locations (e.g., rotting oranges, wildfire spreading, distance to nearest 0 in a binary matrix), initialize the queue with **all initial source nodes** at time 0.
The BFS queue naturally interleaves their expansions, producing the exact Voronoi-like wavefront in a single $O(V + E)$ pass.

### 3. Parent Map Path Reconstruction
To recover the actual sequence of vertices in the shortest path, maintain a `parent` dictionary mapping `parent[v] = u` whenever edge $(u, v)$ is traversed. Once the target is reached, trace backwards from `target` up to `start` and reverse the list.

---

## 5. Examples

### Example 1: BFS Traversal & Disconnected Components
```python
def find_components(adj, nodes):
    visited = set()
    components = []
    for node in nodes:
        if node not in visited:
            comp, q = [], deque([node])
            visited.add(node)
            while q:
                u = q.popleft()
                comp.append(u)
                for v in adj[u]:
                    if v not in visited:
                        visited.add(v)
                        q.append(v)
            components.append(comp)
    return components
```

### Example 2: Shortest Path with Reconstruction
```python
def shortest_path(adj, start, target):
    visited, parent = {start}, {start: None}
    q = deque([start])
    while q:
        u = q.popleft()
        if u == target: break
        for v in adj[u]:
            if v not in visited:
                visited.add(v)
                parent[v] = u
                q.append(v)
    if target not in parent: return []
    path, curr = [], target
    while curr:
        path.append(curr)
        curr = parent[curr]
    return path[::-1]
```

### Example 3: Multi-Source BFS (Rotting Oranges)
```python
def oranges_rotting(grid):
    rows, cols = len(grid), len(grid[0])
    q = deque([(r, c, 0) for r in range(rows) for c in range(cols) if grid[r][c] == 2])
    fresh = sum(grid[r][c] == 1 for r in range(rows) for c in range(cols))
    time = 0
    while q:
        r, c, t = q.popleft()
        time = t
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                q.append((nr, nc, t + 1))
    return time if fresh == 0 else -1
```

---

## 6. Output

```
1. BFS Traversal:
   Visit Order : [0, 1, 2, 3, 4, 5]
   Distances   : {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 2}

2. Connected Components:
   Component 1: [1, 2, 3]
   Component 2: [4, 5]
   Component 3: [6]

3. Shortest Path:
   Shortest Path from A to G: A -> E -> F -> G (Distance: 3)
   Word Ladder ('hit' -> 'cog'): 5 words

4. Rotting Oranges:
   Grid 1: All rotted in 4 minutes
   Grid 2: Impossible (-1)
```

---

## 7. Code Explanation

| Mechanism | Purpose |
|---|---|
| `collections.deque` | Guarantees strictly $O(1)$ pop from left; avoids $O(V)$ cost of list slicing |
| `visited.add(v)` before `q.append(v)` | Prevents duplicate instances of node $v$ from entering queue |
| `parent[v] = u` | Retains structural shortest-path tree edges for backward path extraction |
| Multi-source enqueue | Combines multiple origin points into a unified expanding wavefront |
| Level size snapshooting | Segregates discrete rounds of expansion (minutes, clock ticks) |

---

## 8. Common Mistakes

1. **Marking Visited on Pop Instead of Push**:
   The most common BFS bug. In dense graphs, multiple nodes discover the same unvisited neighbor before it is popped, causing the queue to swell to $O(E)$ redundant elements and timing out.
2. **Using BFS for Weighted Graphs**:
   BFS only finds the shortest path if all edges have equal (or unit) weight. On graphs with varying edge weights, BFS fails; use Dijkstra's Algorithm.
3. **Using `list.pop(0)`**:
   `list.pop(0)` is an $O(n)$ array shift. In BFS with $10^5$ nodes, it turns an $O(V + E)$ linear algorithm into an $O(V^2)$ algorithm. Always use `collections.deque.popleft()`.
4. **Missing Disconnected Components**:
   Calling BFS once from vertex 0 only explores the component containing vertex 0. An outer loop over all vertices is required to handle disconnected graphs.
5. **Memory Explosion in State Space Search**:
   In puzzle solving (like Word Ladder or Sliding Puzzle), failing to prune unviable states or forgetting the visited set exhausts memory rapidly.

---

## 9. Practice Questions

1. Implement **0-1 BFS** using a deque (push weight 0 to left, weight 1 to right) to find shortest path in $O(V + E)$.
2. Solve **Shortest Path in Binary Matrix** (8-directional grid with obstacles).
3. Implement **Bidirectional BFS** for Word Ladder and compare speedup over standard BFS.
4. Check if an undirected graph is **Bipartite** using 2-color BFS.
5. Solve **Open the Lock** (minimum wheel turns to reach target combo without hitting deadends).

---

## 10. Interview Questions

**Q1: What are the time and space complexities of BFS?**
Time complexity is $O(V + E)$ because every vertex is enqueued and dequeued at most once, and every edge is examined once (directed) or twice (undirected). Space complexity is $O(V)$ for the visited set and the FIFO queue.

**Q2: Why does BFS guarantee the shortest path in unweighted graphs?**
Because edges have uniform weight 1, the queue naturally maintains non-decreasing order of distances from the source. The first time a target vertex is dequeued, it is guaranteed to have been reached via the fewest possible edge transitions.

**Q3: How does Bidirectional BFS reduce the search space?**
Instead of expanding a single search tree of radius $d$ ($O(b^d)$ nodes where $b$ is branching factor), Bidirectional BFS grows two trees from both start and target of radius $d/2$. Total nodes explored decreases from $O(b^d)$ to $O(2 \cdot b^{d/2})$, yielding orders-of-magnitude speedup.

**Q4: Can BFS detect cycles in an undirected graph?**
Yes. If during BFS an edge points to an already-visited neighbor that is NOT the immediate parent of the current node, an undirected cycle exists.

**Q5: What is 0-1 BFS?**
A modified BFS for graphs where edge weights are either 0 or 1. Instead of a priority queue ($O((V + E) \log V)$), it uses a double-ended queue (`deque`). Edges of weight 0 are pushed to the front (`appendleft`), and edges of weight 1 are pushed to the back (`append`), running in strictly linear $O(V + E)$ time.
