"""
Question 9: Adjacency-List Graph Representation, Pathfinding & Cycle Detection
Topic: Data Structures & Algorithms (DSA)

Key Concepts Tested:
- Graph representation with adjacency list (dict mapping vertices to neighbor lists)
- Breadth-First Search (BFS) and unweighted shortest path with parent backtracking
- Depth-First Search (DFS) and connected components discovery
- Directed cycle detection using 3-color DFS (WHITE, GRAY, BLACK)
- Handling disconnected components, self-paths, and directed/undirected edges
"""

from collections import deque
from typing import TypeVar, Generic, Dict, List, Optional, Set

T = TypeVar("T")


class Graph(Generic[T]):
    """
    Adjacency-list graph supporting directed/undirected edges,
    BFS/DFS traversals, shortest path calculation, and cycle detection.
    """

    def __init__(self) -> None:
        self.adj_list: Dict[T, List[T]] = {}

    def add_vertex(self, v: T) -> None:
        """Adds a vertex if not already present."""
        if v not in self.adj_list:
            self.adj_list[v] = []

    def add_edge(self, u: T, v: T, directed: bool = False) -> None:
        """Adds an edge between u and v."""
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj_list[u].append(v)
        if not directed:
            self.adj_list[v].append(u)

    def bfs(self, start: T) -> List[T]:
        """Layer-by-layer traversal using a FIFO queue."""
        if start not in self.adj_list:
            return []

        visited: Set[T] = {start}
        queue: deque[T] = deque([start])
        order: List[T] = []

        while queue:
            curr = queue.popleft()
            order.append(curr)
            for neighbor in self.adj_list.get(curr, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return order

    def shortest_path_bfs(self, start: T, target: T) -> Optional[List[T]]:
        """
        Computes the shortest path in an unweighted graph using BFS and parent backtracking.
        Returns the path as a list of vertices, or None if no path exists.
        """
        if start not in self.adj_list or target not in self.adj_list:
            return None

        if start == target:
            return [start]

        visited: Set[T] = {start}
        parent: Dict[T, Optional[T]] = {start: None}
        queue: deque[T] = deque([start])
        found = False

        while queue:
            curr = queue.popleft()
            if curr == target:
                found = True
                break

            for neighbor in self.adj_list.get(curr, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = curr
                    queue.append(neighbor)

        if not found and target not in parent:
            return None

        # Reconstruct path backwards
        path: List[T] = []
        step: Optional[T] = target
        while step is not None:
            path.append(step)
            step = parent.get(step)

        return path[::-1]

    def dfs(self, start: T) -> List[T]:
        """
        Depth-First Search traversal using an explicit stack.
        """
        if start not in self.adj_list:
            return []

        visited: Set[T] = set()
        order: List[T] = []
        stack: List[T] = [start]

        while stack:
            curr = stack.pop()
            if curr not in visited:
                visited.add(curr)
                order.append(curr)
                for neighbor in self.adj_list.get(curr, []):
                    if neighbor not in visited:
                        stack.append(neighbor)

        return order

    def connected_components(self) -> List[List[T]]:
        """
        Finds all connected subgraphs in an undirected graph.
        """
        visited: Set[T] = set()
        components: List[List[T]] = []

        for vertex in self.adj_list:
            if vertex not in visited:
                component = []
                queue: deque[T] = deque([vertex])
                visited.add(vertex)

                while queue:
                    curr = queue.popleft()
                    component.append(curr)
                    for neighbor in self.adj_list.get(curr, []):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)

                components.append(component)

        return components

    def has_cycle_directed(self) -> bool:
        """
        Detects directed cycles using 3-color DFS:
        WHITE = 0 (unvisited), GRAY = 1 (active in recursion stack), BLACK = 2 (fully explored).
        """
        WHITE, GRAY, BLACK = 0, 1, 2
        colors: Dict[T, int] = {v: WHITE for v in self.adj_list}

        def dfs_visit(u: T) -> bool:
            colors[u] = GRAY
            for neighbor in self.adj_list.get(u, []):
                if colors.get(neighbor, WHITE) == GRAY:
                    return True  # Back-edge detected
                if colors.get(neighbor, WHITE) == WHITE:
                    if dfs_visit(neighbor):
                        return True
            colors[u] = BLACK
            return False

        for node in list(self.adj_list.keys()):
            if colors.get(node, WHITE) == WHITE:
                if dfs_visit(node):
                    return True

        return False


if __name__ == "__main__":
    # 1. Undirected Graph
    # A --- B --- C
    # |     |
    # D --- E
    g = Graph[str]()
    edges = [("A", "B"), ("A", "D"), ("B", "C"), ("B", "E"), ("D", "E")]
    for u, v in edges:
        g.add_edge(u, v, directed=False)

    print("=== 1. Undirected Graph Traversals ===")
    bfs_order = g.bfs("A")
    dfs_order = g.dfs("A")
    path_a_to_c = g.shortest_path_bfs("A", "C")
    components = g.connected_components()

    print(f"BFS Traversal from 'A': {bfs_order}")
    print(f"DFS Traversal from 'A': {dfs_order}")
    print(f"Shortest Path from 'A' to 'C': {path_a_to_c} (Length: {len(path_a_to_c) - 1} edges)")
    print(f"Connected Components Count: {len(components)}")

    print("\n=== 2. Directed Graph Cycle Detection ===")
    # Directed cycle: 1 -> 2 -> 3 -> 1
    dg = Graph[int]()
    dg.add_edge(1, 2, directed=True)
    dg.add_edge(2, 3, directed=True)
    dg.add_edge(3, 1, directed=True)
    has_cycle = dg.has_cycle_directed()
    print(f"Directed Graph (1->2->3->1) Contains Cycle: {has_cycle}")

    # Directed Acyclic Graph (DAG): 10 -> 20, 10 -> 30, 20 -> 30
    dag = Graph[int]()
    dag.add_edge(10, 20, directed=True)
    dag.add_edge(10, 30, directed=True)
    dag.add_edge(20, 30, directed=True)
    print(f"Directed Graph (DAG) Contains Cycle: {dag.has_cycle_directed()}")

    print("\n=== 3. Edge Cases ===")
    print(f"Path to self: {g.shortest_path_bfs('A', 'A')}")
    print(f"Path to unreachable node: {g.shortest_path_bfs('A', 'Z')}")
