"""
Phase 6 - Section J.02: BFS (Breadth-First Search)
Example 01: BFS Traversal and Connected Components

Demonstrating:
1. Standard Breadth-First Search on graphs using a FIFO queue (collections.deque).
2. Finding all connected components in disconnected undirected graphs.
3. Tracking BFS levels (distance from source in edge count).
"""

from collections import defaultdict, deque


class Graph:
    def __init__(self):
        self.adj = defaultdict(list)
        self.nodes = set()

    def add_edge(self, u, v):
        self.nodes.add(u)
        self.nodes.add(v)
        self.adj[u].append(v)
        self.adj[v].append(u)


def bfs_traversal(graph, start_node):
    """
    Traverse graph using BFS starting from start_node.
    Returns: (traversal_order, distances_from_start)
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    visited = set([start_node])
    queue = deque([(start_node, 0)])
    order = []
    distances = {start_node: 0}

    while queue:
        u, dist = queue.popleft()
        order.append(u)

        for v in sorted(graph.adj[u]):
            if v not in visited:
                visited.add(v)
                distances[v] = dist + 1
                queue.append((v, dist + 1))

    return order, distances


def find_connected_components(graph):
    """
    Find all disconnected subgraphs (components) using BFS.
    Time Complexity: O(V + E)
    """
    visited = set()
    components = []

    for node in sorted(graph.nodes):
        if node not in visited:
            component = []
            queue = deque([node])
            visited.add(node)

            while queue:
                u = queue.popleft()
                component.append(u)
                for v in sorted(graph.adj[u]):
                    if v not in visited:
                        visited.add(v)
                        queue.append(v)

            components.append(component)

    return components


def main():
    print("=" * 60)
    print("1. Breadth-First Search (BFS) Traversal")
    print("=" * 60)
    g = Graph()
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (4, 5)]
    for u, v in edges:
        g.add_edge(u, v)

    order, dists = bfs_traversal(g, start_node=0)
    print("Graph Edges     :", edges)
    print("BFS Visit Order :", order)
    print("Distances from 0:", dists)

    print("\n" + "=" * 60)
    print("2. Connected Components in Disconnected Graph")
    print("=" * 60)
    g_disc = Graph()
    # Component 1: 1-2-3
    g_disc.add_edge(1, 2)
    g_disc.add_edge(2, 3)
    # Component 2: 4-5
    g_disc.add_edge(4, 5)
    # Component 3: 6 (isolated)
    g_disc.nodes.add(6)

    comp_list = find_connected_components(g_disc)
    print(f"Total Components Found: {len(comp_list)}")
    for i, comp in enumerate(comp_list, 1):
        print(f"  Component {i}: {comp}")


if __name__ == "__main__":
    main()
