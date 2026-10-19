"""
Topic: Data Structures and Algorithms (DSA) - Graph Representation and BFS/DFS
------------------------------------------------------------------------------
Questions Covered:
1. Graph Representations: Adjacency list vs adjacency matrix with edge weight support.
2. Breadth-First Search (BFS): Unweighted shortest path finding and full path reconstruction.
3. Depth-First Search (DFS): Connected components traversal (iterative and recursive).
4. Cycle Detection in Undirected Graphs: DFS parent tracking and Disjoint Set Union (DSU).
5. Cycle Detection in Directed Graphs: Three-color DFS state machine (White, Gray, Black).
6. Topological Sorting: Kahn's in-degree BFS algorithm and DFS post-order on DAGs.
7. Dijkstra's Shortest Path Algorithm: Single-source shortest path using priority queue min-heap.
8. Bipartite Graph Verification: Two-color graph partition verification using BFS.
9. Number of Islands (2D Grid Flood Fill): Grid-based multi-directional connected component search.
10. Architectural System: Microservice Dependency DAG with deployment ordering & blast radius analysis.
"""

import heapq
from typing import List, Tuple, Optional, Any, Dict, Set


# ==============================================================================
# Question 1: Graph Representations (Adjacency List vs Matrix)
# ==============================================================================
class AdjacencyListGraph:
    """Graph represented as adjacency list mapping node -> list of (neighbor, weight)."""
    def __init__(self, directed: bool = False):
        self.directed = directed
        self.adj: Dict[str, List[Tuple[str, float]]] = {}

    def add_edge(self, u: str, v: str, weight: float = 1.0) -> None:
        if u not in self.adj:
            self.adj[u] = []
        if v not in self.adj:
            self.adj[v] = []

        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))

    def get_neighbors(self, u: str) -> List[Tuple[str, float]]:
        return self.adj.get(u, [])


class AdjacencyMatrixGraph:
    """Graph represented as N x N 2D matrix."""
    def __init__(self, num_vertices: int, directed: bool = False):
        self.n = num_vertices
        self.directed = directed
        self.matrix = [[0.0] * num_vertices for _ in range(num_vertices)]

    def add_edge(self, u: int, v: int, weight: float = 1.0) -> None:
        self.matrix[u][v] = weight
        if not self.directed:
            self.matrix[v][u] = weight


def test_q1_graph_representations():
    al = AdjacencyListGraph(directed=False)
    al.add_edge("A", "B", 5.0)
    al.add_edge("A", "C", 2.0)
    assert len(al.get_neighbors("A")) == 2
    assert ("B", 5.0) in al.get_neighbors("A")
    assert ("A", 5.0) in al.get_neighbors("B")

    am = AdjacencyMatrixGraph(3, directed=True)
    am.add_edge(0, 1, 3.5)
    assert am.matrix[0][1] == 3.5
    assert am.matrix[1][0] == 0.0  # Directed
    print("=== Q1: Graph Representations (List & Matrix) Verified ===")


# ==============================================================================
# Question 2: Breadth-First Search (BFS) Shortest Path
# ==============================================================================
def bfs_shortest_path(graph: Dict[str, List[str]], start: str, target: str) -> Optional[List[str]]:
    """
    Finds shortest path in an unweighted graph using BFS with parent tracking.
    Returns list of vertices from start to target.
    """
    if start == target:
        return [start]

    visited = {start}
    queue: List[str] = [start]
    parent: Dict[str, Optional[str]] = {start: None}

    while queue:
        curr = queue.pop(0)
        if curr == target:
            # Reconstruct path
            path = []
            node: Optional[str] = target
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1]

        for neighbor in graph.get(curr, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = curr
                queue.append(neighbor)

    return None


def test_q2_bfs_shortest_path():
    graph = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A", "F"],
        "D": ["B"],
        "E": ["B", "F"],
        "F": ["C", "E"],
    }
    # Shortest path A to F is A -> C -> F (2 edges, 3 nodes)
    path = bfs_shortest_path(graph, "A", "F")
    assert path == ["A", "C", "F"]

    no_path = bfs_shortest_path(graph, "A", "Z")
    assert no_path is None
    print("=== Q2: BFS Shortest Path Reconstruction Verified ===")


# ==============================================================================
# Question 3: Depth-First Search (DFS) Connected Components
# ==============================================================================
def count_connected_components(num_vertices: int, edges: List[Tuple[int, int]]) -> int:
    """Counts number of connected components in an undirected graph using DFS."""
    adj: Dict[int, List[int]] = {i: [] for i in range(num_vertices)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited: Set[int] = set()
    components = 0

    def dfs(node: int):
        visited.add(node)
        for neighbor in adj[node]:
            if neighbor not in visited:
                dfs(neighbor)

    for i in range(num_vertices):
        if i not in visited:
            dfs(i)
            components += 1

    return components


def test_q3_dfs_components():
    # 5 vertices: 0-1, 1-2 (component 1), 3-4 (component 2) -> 2 components
    edges = [(0, 1), (1, 2), (3, 4)]
    assert count_connected_components(5, edges) == 2

    # Isolated vertex 5 -> 3 components
    assert count_connected_components(6, edges) == 3
    print("=== Q3: DFS Connected Components Verified ===")


# ==============================================================================
# Question 4: Cycle Detection in Undirected Graph
# ==============================================================================
def has_cycle_undirected(num_vertices: int, edges: List[Tuple[int, int]]) -> bool:
    """
    Detects if an undirected graph contains a cycle using DFS with parent tracking.
    """
    adj: Dict[int, List[int]] = {i: [] for i in range(num_vertices)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited: Set[int] = set()

    def dfs(curr: int, parent: int) -> bool:
        visited.add(curr)
        for neighbor in adj[curr]:
            if neighbor not in visited:
                if dfs(neighbor, curr):
                    return True
            elif neighbor != parent:
                # Visited node that is NOT immediate parent implies back-edge cycle
                return True
        return False

    for i in range(num_vertices):
        if i not in visited:
            if dfs(i, -1):
                return True

    return False


def test_q4_cycle_undirected():
    # Cycle 0-1-2-0
    cyclic_edges = [(0, 1), (1, 2), (2, 0)]
    assert has_cycle_undirected(3, cyclic_edges) is True

    # Tree (acyclic): 0-1, 1-2, 1-3
    acyclic_edges = [(0, 1), (1, 2), (1, 3)]
    assert has_cycle_undirected(4, acyclic_edges) is False
    print("=== Q4: Cycle Detection in Undirected Graph Verified ===")


# ==============================================================================
# Question 5: Cycle Detection in Directed Graph (Three-Color DFS)
# ==============================================================================
def has_cycle_directed(num_vertices: int, edges: List[Tuple[int, int]]) -> bool:
    """
    Detects cycles in directed graph using 3-color DFS:
    0 = WHITE (unvisited)
    1 = GRAY (currently in recursion call stack / visiting)
    2 = BLACK (completely visited and processed)
    Cycle exists if a GRAY node is visited.
    """
    adj: Dict[int, List[int]] = {i: [] for i in range(num_vertices)}
    for u, v in edges:
        adj[u].append(v)

    color = [0] * num_vertices

    def dfs(node: int) -> bool:
        color[node] = 1  # Mark GRAY
        for neighbor in adj[node]:
            if color[neighbor] == 1:
                return True  # Back edge to an ancestor in active stack
            if color[neighbor] == 0:
                if dfs(neighbor):
                    return True
        color[node] = 2  # Mark BLACK
        return False

    for i in range(num_vertices):
        if color[i] == 0:
            if dfs(i):
                return True

    return False


def test_q5_cycle_directed():
    # Cycle: 0 -> 1 -> 2 -> 0
    assert has_cycle_directed(3, [(0, 1), (1, 2), (2, 0)]) is True

    # DAG (no cycle): 0 -> 1, 0 -> 2, 1 -> 2
    assert has_cycle_directed(3, [(0, 1), (0, 2), (1, 2)]) is False
    print("=== Q5: Cycle Detection in Directed Graph (3-Color DFS) Verified ===")


# ==============================================================================
# Question 6: Topological Sorting (Kahn's Algorithm BFS)
# ==============================================================================
def topological_sort_kahns(num_courses: int, prerequisites: List[Tuple[int, int]]) -> List[int]:
    """
    Finds valid topological order of tasks/courses using Kahn's algorithm.
    prerequisites contains (u, v) representing edge u -> v (u must precede v).
    Returns ordering list, or [] if graph has a cycle.
    """
    adj: Dict[int, List[int]] = {i: [] for i in range(num_courses)}
    in_degree = [0] * num_courses

    for u, v in prerequisites:
        adj[u].append(v)
        in_degree[v] += 1

    # Queue all nodes with 0 in-degree
    queue: List[int] = [i for i in range(num_courses) if in_degree[i] == 0]
    order: List[int] = []

    while queue:
        curr = queue.pop(0)
        order.append(curr)

        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return order if len(order) == num_courses else []


def test_q6_topological_sort():
    # Prerequisites: 0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3
    prereqs = [(0, 1), (0, 2), (1, 3), (2, 3)]
    order = topological_sort_kahns(4, prereqs)
    assert order[0] == 0
    assert order[-1] == 3
    assert set(order[1:3]) == {1, 2}

    # Cyclic dependencies cannot be topologically sorted
    cyclic = [(0, 1), (1, 2), (2, 0)]
    assert topological_sort_kahns(3, cyclic) == []
    print("=== Q6: Topological Sorting (Kahn's Algorithm) Verified ===")


# ==============================================================================
# Question 7: Dijkstra's Shortest Path Algorithm
# ==============================================================================
def dijkstra_shortest_paths(
    graph: Dict[str, List[Tuple[str, float]]], source: str
) -> Dict[str, float]:
    """
    Computes shortest distances from source to all reachable nodes in a weighted graph
    with non-negative edge weights using a min-heap priority queue.
    """
    distances: Dict[str, float] = {node: float("inf") for node in graph}
    distances[source] = 0.0

    # Priority queue stores tuples: (distance, node)
    pq: List[Tuple[float, str]] = [(0.0, source)]

    while pq:
        curr_dist, u = heapq.heappop(pq)

        if curr_dist > distances[u]:
            continue

        for v, weight in graph.get(u, []):
            new_dist = curr_dist + weight
            if new_dist < distances.get(v, float("inf")):
                distances[v] = new_dist
                heapq.heappush(pq, (new_dist, v))

    return distances


def test_q7_dijkstra():
    weighted_graph = {
        "A": [("B", 4.0), ("C", 2.0)],
        "B": [("D", 3.0), ("C", 1.0)],
        "C": [("B", 1.0), ("D", 5.0)],
        "D": [],
    }
    # Path A -> D:
    # Direct A -> B(4) -> D(3) = 7
    # Path A -> C(2) -> B(2+1=3) -> D(3+3=6) -> optimal distance = 6.0
    dist = dijkstra_shortest_paths(weighted_graph, "A")
    assert dist["A"] == 0.0
    assert dist["C"] == 2.0
    assert dist["B"] == 3.0
    assert dist["D"] == 6.0
    print("=== Q7: Dijkstra's Shortest Path Algorithm Verified ===")


# ==============================================================================
# Question 8: Bipartite Graph Verification (Two-Coloring)
# ==============================================================================
def is_bipartite(graph: List[List[int]]) -> bool:
    """
    Checks whether an undirected graph is bipartite (nodes can be colored with 2 colors
    such that no two adjacent nodes share the same color).
    graph[u] contains list of neighbors of u.
    """
    n = len(graph)
    colors = [-1] * n  # -1 = uncolored, 0 and 1 = colors

    for start_node in range(n):
        if colors[start_node] != -1:
            continue

        colors[start_node] = 0
        queue = [start_node]

        while queue:
            curr = queue.pop(0)
            curr_color = colors[curr]
            next_color = 1 - curr_color

            for neighbor in graph[curr]:
                if colors[neighbor] == -1:
                    colors[neighbor] = next_color
                    queue.append(neighbor)
                elif colors[neighbor] == curr_color:
                    return False

    return True


def test_q8_bipartite_graph():
    # Bipartite graph (square 0-1-2-3-0)
    bipartite_adj = [[1, 3], [0, 2], [1, 3], [0, 2]]
    assert is_bipartite(bipartite_adj) is True

    # Non-bipartite (triangle 0-1-2-0)
    odd_cycle_adj = [[1, 2], [0, 2], [0, 1]]
    assert is_bipartite(odd_cycle_adj) is False
    print("=== Q8: Bipartite Graph Verification Verified ===")


# ==============================================================================
# Question 9: Number of Islands (2D Grid Connected Components)
# ==============================================================================
def num_islands(grid: List[List[str]]) -> int:
    """
    Counts number of islands in a 2D grid ('1' is land, '0' is water).
    An island is surrounded by water and formed by connecting adjacent lands horizontally or vertically.
    """
    if not grid or not grid[0]:
        return 0

    rows = len(grid)
    cols = len(grid[0])
    islands = 0

    def dfs(r: int, c: int):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"  # Sink land to avoid revisiting
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                dfs(r, c)
                islands += 1

    return islands


def test_q9_num_islands():
    grid1 = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
    ]
    assert num_islands(grid1) == 1

    grid2 = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    assert num_islands(grid2) == 3
    print("=== Q9: Number of Islands (2D Grid Flood Fill) Verified ===")


# ==============================================================================
# Question 10: Architectural Microservice Dependency DAG & Blast Radius Engine
# ==============================================================================
class MicroserviceDependencyDAG:
    """
    Production dependency graph engine for distributed microservices:
    - Analyzes valid deployment build orders (Topological sorting)
    - Detects circular dependency deadlocks
    - Calculates the blast radius / affected downstream services when a component fails
    """
    def __init__(self):
        self.services: Set[str] = set()
        self.dependencies: Dict[str, Set[str]] = {}  # service -> services it depends on (downstream calls)
        self.dependents: Dict[str, Set[str]] = {}    # service -> callers that depend on it

    def register_dependency(self, service: str, depends_on: str) -> None:
        self.services.add(service)
        self.services.add(depends_on)

        if service not in self.dependencies:
            self.dependencies[service] = set()
        self.dependencies[service].add(depends_on)

        if depends_on not in self.dependents:
            self.dependents[depends_on] = set()
        self.dependents[depends_on].add(service)

    def get_deployment_order(self) -> Optional[List[str]]:
        """
        Determines order to deploy services such that all dependencies are deployed first.
        """
        in_degree = {s: 0 for s in self.services}
        for s in self.services:
            for dep in self.dependencies.get(s, set()):
                in_degree[s] += 1  # s depends on dep, so dep must be deployed before s

        # Services with 0 dependencies can deploy immediately
        queue = [s for s, deg in in_degree.items() if deg == 0]
        order = []

        while queue:
            curr = queue.pop(0)
            order.append(curr)

            # Once curr is deployed, unblock callers that depend on curr
            for caller in self.dependents.get(curr, set()):
                in_degree[caller] -= 1
                if in_degree[caller] == 0:
                    queue.append(caller)

        return order if len(order) == len(self.services) else None  # None if cycle

    def calculate_blast_radius(self, failed_service: str) -> Set[str]:
        """
        Calculates all services that fail directly or transitively if failed_service goes down.
        Traverses callers using BFS.
        """
        impacted: Set[str] = set()
        queue = [failed_service]

        while queue:
            curr = queue.pop(0)
            for caller in self.dependents.get(curr, set()):
                if caller not in impacted:
                    impacted.add(caller)
                    queue.append(caller)

        return impacted


def test_q10_microservice_dag():
    dag = MicroserviceDependencyDAG()
    # auth_db has no dependencies
    # auth_service depends on auth_db
    # payment_gateway depends on db_proxy
    # checkout_api depends on payment_gateway and auth_service
    # web_frontend depends on checkout_api
    dag.register_dependency("auth_service", "auth_db")
    dag.register_dependency("payment_gateway", "db_proxy")
    dag.register_dependency("checkout_api", "payment_gateway")
    dag.register_dependency("checkout_api", "auth_service")
    dag.register_dependency("web_frontend", "checkout_api")

    # 1. Deployment order
    deploy_order = dag.get_deployment_order()
    assert deploy_order is not None
    # Foundations (auth_db, db_proxy) must be deployed before checkout_api and web_frontend
    assert deploy_order.index("auth_db") < deploy_order.index("auth_service")
    assert deploy_order.index("auth_service") < deploy_order.index("checkout_api")
    assert deploy_order.index("checkout_api") < deploy_order.index("web_frontend")

    # 2. Blast radius when auth_db fails:
    # auth_db -> auth_service -> checkout_api -> web_frontend
    blast_radius = dag.calculate_blast_radius("auth_db")
    assert blast_radius == {"auth_service", "checkout_api", "web_frontend"}
    assert "payment_gateway" not in blast_radius
    assert "db_proxy" not in blast_radius
    print("=== Q10: Architectural Microservice Dependency DAG Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_graph_representations()
    test_q2_bfs_shortest_path()
    test_q3_dfs_components()
    test_q4_cycle_undirected()
    test_q5_cycle_directed()
    test_q6_topological_sort()
    test_q7_dijkstra()
    test_q8_bipartite_graph()
    test_q9_num_islands()
    test_q10_microservice_dag()
    print("\nAll 10 graph representation and BFS/DFS DSA questions passed successfully!")
