"""
Phase 6 - Section J.01: Graph Representation
Example 03: Edge List and Implicit Grid Graph

Demonstrating:
1. Edge List representation (used in Kruskal's algorithm and Bellman-Ford).
2. Implicit 2D Grid Graph: generating 4-directional and 8-directional neighbor transitions.
"""


class EdgeListGraph:
    """Graph stored as a list of edge tuples: (u, v, weight)."""

    def __init__(self, directed=False):
        self.edges = []
        self.directed = directed

    def add_edge(self, u, v, weight=1):
        self.edges.append((u, v, weight))
        if not self.directed:
            self.edges.append((v, u, weight))

    def sort_by_weight(self):
        """Essential for greedy MST algorithms like Kruskal's."""
        self.edges.sort(key=lambda edge: edge[2])


class GridGraph:
    """
    Implicit Graph on a 2D Matrix where each cell (r, c) is a vertex.
    Edges connect to adjacent valid cells.
    """

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # 4-Directional deltas: Up, Down, Left, Right
        self.directions_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        # 8-Directional deltas including diagonals
        self.directions_8 = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

    def is_valid(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def get_neighbors_4(self, r, c):
        neighbors = []
        for dr, dc in self.directions_4:
            nr, nc = r + dr, c + dc
            if self.is_valid(nr, nc):
                neighbors.append((nr, nc))
        return neighbors

    def get_neighbors_8(self, r, c):
        neighbors = []
        for dr, dc in self.directions_8:
            nr, nc = r + dr, c + dc
            if self.is_valid(nr, nc):
                neighbors.append((nr, nc))
        return neighbors


def main():
    print("=" * 60)
    print("1. Edge List Representation")
    print("=" * 60)
    el_graph = EdgeListGraph(directed=True)
    el_graph.add_edge("A", "B", 10)
    el_graph.add_edge("B", "C", 5)
    el_graph.add_edge("A", "C", 20)
    el_graph.add_edge("C", "D", 2)

    print("Unsorted Edge List:")
    for u, v, w in el_graph.edges:
        print(f"  ({u} -> {v}, weight={w})")

    el_graph.sort_by_weight()
    print("\nEdge List Sorted by Weight (Ascending):")
    for u, v, w in el_graph.edges:
        print(f"  ({u} -> {v}, weight={w})")

    print("\n" + "=" * 60)
    print("2. Implicit 2D Grid Graph (Neighbor Generation)")
    print("=" * 60)
    grid = GridGraph(rows=3, cols=3)
    corners = [(0, 0), (1, 1)]

    for r, c in corners:
        print(f"Cell ({r}, {c}) 4-way neighbors :", grid.get_neighbors_4(r, c))
        print(f"Cell ({r}, {c}) 8-way neighbors :", grid.get_neighbors_8(r, c))


if __name__ == "__main__":
    main()
