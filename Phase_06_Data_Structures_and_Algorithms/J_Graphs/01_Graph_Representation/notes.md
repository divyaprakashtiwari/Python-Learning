# Graph Representation

## 1. Introduction

A **Graph** $G = (V, E)$ is a non-linear data structure consisting of a set of **vertices (nodes)** $V$ connected by a set of **edges (links)** $E$.

Graphs model interconnected relationships across networks, social connections, computer networks, dependency build systems, road navigation maps, and state spaces. Choosing the appropriate representation format directly dictates the time complexity and memory overhead of all subsequent graph algorithms (BFS, DFS, Dijkstra, TopoSort, MST).

---

## 2. Representation Formats Comparison

| Representation | Space Complexity | Add Edge | Check Edge $(u, v)$ | Iterate Neighbors of $u$ | Best Suited For |
|---|---|---|---|---|---|
| **Adjacency Matrix** | $O(V^2)$ | $O(1)$ | **$O(1)$** | $O(V)$ | Dense graphs ($E \approx V^2$), constant-time edge checks, Floyd-Warshall |
| **Adjacency List** | **$O(V + E)$** | $O(1)$ | $O(\text{deg}(u))$ | **$O(\text{deg}(u))$** | Sparse graphs ($E \ll V^2$), BFS/DFS traversals, Dijkstra, standard library |
| **Edge List** | **$O(E)$** | $O(1)$ | $O(E)$ | $O(E)$ | Kruskal's MST algorithm, Bellman-Ford algorithm |
| **Implicit Matrix/Grid** | $O(1)$ auxiliary | Implicit | $O(1)$ | $O(1)$ (up to 4 or 8) | Maze problems, image flood fill, 2D grid pathfinding |

---

## 3. Syntax / Common Python Implementations

### Adjacency List with `collections.defaultdict`
```python
from collections import defaultdict
adj = defaultdict(list)
adj[u].append((v, weight))
if not directed:
    adj[v].append((u, weight))
```

### Adjacency Matrix with 2D List
```python
matrix = [[0] * V for _ in range(V)]
matrix[u][v] = weight
if not directed:
    matrix[v][u] = weight
```

---

## 4. Key Graph Concepts

### 1. Directed vs Undirected
- **Undirected Graph:** Edges are bidirectional ($(u, v) \equiv (v, u)$). The adjacency matrix is symmetric along the main diagonal ($M[u][v] = M[v][u]$).
- **Directed Graph (Digraph):** Edges have direction ($u \to v$). The matrix is generally asymmetric.

### 2. Weighted vs Unweighted
- Unweighted edges store boolean connectivity (`1` or `0`).
- Weighted edges store numeric weights (distance, latency, cost) instead of `1`.

### 3. Degree of Vertices
- **Undirected Degree:** Total edges incident on vertex $u$. Sum of degrees $\sum \text{deg}(v) = 2|E|$ (Handshaking Lemma).
- **In-Degree:** Number of incoming directed edges to $u$.
- **Out-Degree:** Number of outgoing directed edges from $u$.

### 4. Graph Transpose / Reversal ($G^T$)
In a directed graph, reversing the direction of every edge ($u \to v$ becomes $v \to u$) yields the transposed graph $G^T$. This is essential for Kosaraju's Strongly Connected Components (SCC) algorithm.

---

## 5. Examples

### Example 1: Adjacency Matrix vs Adjacency List
```python
class GraphAdjMatrix:
    def __init__(self, V):
        self.matrix = [[0] * V for _ in range(V)]
    def add_edge(self, u, v, w=1):
        self.matrix[u][v] = w
        self.matrix[v][u] = w

class GraphAdjList:
    def __init__(self):
        self.adj = defaultdict(list)
    def add_edge(self, u, v, w=1):
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))
```

### Example 2: Directed Graph In-Degree and Transpose
```python
def transpose_graph(adj):
    rev = defaultdict(list)
    for u in adj:
        for v, w in adj[u]:
            rev[v].append((u, w))
    return rev
```

### Example 3: Implicit 2D Grid Graph (4-Way Directions)
```python
def get_neighbors(r, c, rows, cols):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return [(r + dr, c + dc) for dr, dc in directions
            if 0 <= r + dr < rows and 0 <= c + dc < cols]
```

---

## 6. Output

```
1. Adjacency Matrix (4x4):
   [0, 1, 1, 0]
   [1, 0, 1, 0]
   [1, 1, 0, 1]
   [0, 0, 1, 0]
   has_edge(0, 1): True
   has_edge(0, 3): False

2. Adjacency List:
   Vertex 0 -> [1(w=10), 2(w=15)]
   Vertex 2 -> [0(w=15), 1(w=20), 3(w=30)]
   Neighbors of vertex 2: [0, 1, 3]

3. Graph Transpose:
   Original : Node A (in=1, out=2) -> [B, C]
   Transposed: Node A (in=2, out=1) -> [D]
```

---

## 7. Code Explanation

| Component | Responsibility |
|---|---|
| `matrix[u][v] = weight` | Direct 2D array lookup providing $O(1)$ edge existence checks |
| `adj[u].append((v, weight))` | Dynamically stores only actual edges, saving memory on sparse graphs |
| `is_valid(r, c)` | Bounds check ensuring grid coordinate stays inside matrix boundaries |
| `rev.add_edge(v, u, w)` | Inverts edge orientation to construct the dual transposed digraph $G^T$ |
| `Handshaking Lemma` | Guarantees that the sum of degrees across all vertices is strictly even ($2|E|$) |

---

## 8. Common Mistakes

1. **Allocating Matrix for Sparse Graphs**:
   Creating an adjacency matrix for $V = 10^5$ vertices requires a $(10^5)^2$ array ($\approx 10$ billion entries), resulting in an immediate `MemoryError`. Always use Adjacency Lists for sparse graphs.
2. **Missing Reverse Edge in Undirected Graphs**:
   Adding `adj[u].append(v)` without adding `adj[v].append(u)` mistakenly converts an undirected edge into a one-way directed edge.
3. **Linear Scan in `has_edge()` for Adjacency Lists**:
   Checking if edge $(u, v)$ exists in an adjacency list takes $O(\text{deg}(u))$. If frequent edge checks are required, store neighbors in a set (`defaultdict(set)`) for $O(1)$ checks.
4. **Modifying In-Degree During Iteration**:
   Altering graph structures during degree calculations causes off-by-one errors in topological sorting.
5. **Ignoring Isolated Vertices**:
   Using `defaultdict(list)` means nodes without outgoing edges might not appear as keys in `adj.keys()`. Maintain a dedicated `nodes = set()` to track isolated vertices.

---

## 9. Practice Questions

1. Implement a method to compute the **density** of a directed graph ($D = |E| / (|V|(|V| - 1))$).
2. Given an adjacency matrix, convert it to an adjacency list in $O(V^2)$ time.
3. Determine whether an undirected graph is **Bipartite** (2-colorable) using BFS/DFS.
4. Count the number of triangles ($K_3$ cliques) in an undirected graph using the adjacency matrix ($A^3$ trace).
5. Implement a graph builder that parses edge string tokens like `"A->B:5, B->C:10"` into a weighted digraph.

---

## 10. Interview Questions

**Q1: When would you strictly prefer an Adjacency Matrix over an Adjacency List?**
When the graph is **dense** ($E \approx V^2$), when constant-time $O(1)$ edge existence verification is required, or when running algorithms that naturally operate on matrices such as the **Floyd-Warshall All-Pairs Shortest Path** algorithm ($O(V^3)$).

**Q2: What is the Handshaking Lemma?**
In any undirected graph, the sum of degrees of all vertices equals twice the number of edges: $\sum_{v \in V} \text{deg}(v) = 2|E|$. An immediate corollary is that any undirected graph must contain an even number of vertices with odd degrees.

**Q3: How much memory does an Adjacency List save compared to a Matrix on a road network with 1 million vertices and 3 million edges?**
An Adjacency Matrix requires $10^6 \times 10^6 = 10^{12}$ entries ($\approx 1$ Terabyte of RAM). An Adjacency List requires $V + E = 10^6 + 3 \times 10^6 = 4 \times 10^6$ pointers/integers ($\approx 32$ Megabytes of RAM), representing a 30,000x memory saving.

**Q4: How do you represent a multigraph (graph with multiple parallel edges between the same two nodes)?**
An Adjacency Matrix cannot store multiple edges in a single scalar cell without using sub-lists. An Adjacency List naturally supports multigraphs by allowing duplicate entries in `adj[u]`.

**Q5: What is an Implicit Graph?**
An implicit graph is one where vertices and edges are not explicitly stored in memory beforehand (like a matrix or list), but are generated dynamically on demand via state transition rules (e.g., 2D grid coordinates, chess game trees, or Rubik's cube states).
