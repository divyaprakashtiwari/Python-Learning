"""
Phase 6 - Section J.01: Graph Representation
Example 01: Adjacency Matrix vs Adjacency List

Demonstrating:
1. Adjacency Matrix representation (2D V x V array).
2. Adjacency List representation (dict of lists / collections.defaultdict).
3. Tradeoffs in edge existence check vs neighbor enumeration.
"""

from collections import defaultdict


class GraphAdjMatrix:
    """Graph represented by a 2D V x V Adjacency Matrix."""
    def __init__(self, num_vertices, directed=False):
        self.v = num_vertices
        self.directed = directed
        self.matrix = [[0] * num_vertices for _ in range(num_vertices)]

    def add_edge(self, u, v, weight=1):
        self.matrix[u][v] = weight
        if not self.directed:
            self.matrix[v][u] = weight

    def has_edge(self, u, v):
        """O(1) time complexity."""
        return self.matrix[u][v] != 0

    def get_neighbors(self, u):
        """O(V) time complexity."""
        return [v for v in range(self.v) if self.matrix[u][v] != 0]

    def display(self):
        for row in self.matrix:
            print("  ", row)


class GraphAdjList:
    """Graph represented by an Adjacency List."""
    def __init__(self, directed=False):
        self.directed = directed
        self.adj = defaultdict(list)

    def add_edge(self, u, v, weight=1):
        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))

    def has_edge(self, u, v):
        """O(deg(u)) time complexity."""
        return any(neighbor == v for neighbor, _ in self.adj[u])

    def get_neighbors(self, u):
        """O(deg(u)) time complexity."""
        return [v for v, _ in self.adj[u]]

    def display(self):
        for u in sorted(self.adj.keys()):
            neighbors_str = ", ".join(f"{v}(w={w})" for v, w in self.adj[u])
            print(f"   Vertex {u} -> [{neighbors_str}]")


def main():
    print("=" * 60)
    print("1. Adjacency Matrix (Dense / Direct Lookup)")
    print("=" * 60)
    matrix_graph = GraphAdjMatrix(4, directed=False)
    # Edges: 0-1, 0-2, 1-2, 2-3
    matrix_graph.add_edge(0, 1)
    matrix_graph.add_edge(0, 2)
    matrix_graph.add_edge(1, 2)
    matrix_graph.add_edge(2, 3)

    print("Matrix View (4x4):")
    matrix_graph.display()
    print("has_edge(0, 1):", matrix_graph.has_edge(0, 1))
    print("has_edge(0, 3):", matrix_graph.has_edge(0, 3))
    print("Neighbors of vertex 2:", matrix_graph.get_neighbors(2))

    print("\n" + "=" * 60)
    print("2. Adjacency List (Sparse / Space-Optimal)")
    print("=" * 60)
    list_graph = GraphAdjList(directed=False)
    list_graph.add_edge(0, 1, weight=10)
    list_graph.add_edge(0, 2, weight=15)
    list_graph.add_edge(1, 2, weight=20)
    list_graph.add_edge(2, 3, weight=30)

    print("Adjacency List View:")
    list_graph.display()
    print("has_edge(0, 1):", list_graph.has_edge(0, 1))
    print("has_edge(0, 3):", list_graph.has_edge(0, 3))
    print("Neighbors of vertex 2:", list_graph.get_neighbors(2))


if __name__ == "__main__":
    main()
