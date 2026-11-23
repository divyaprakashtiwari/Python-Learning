"""
Phase 6 - Section J.01: Graph Representation
Example 02: General Weighted Graph Class & Degree Analysis

Demonstrating:
1. Complete OOP Weighted Directed Graph class.
2. In-degree and Out-degree calculations.
3. Graph Transpose / Reversal (flipping all directed edges).
"""

from collections import defaultdict


class DirectedWeightedGraph:
    """Directed graph with weighted edges."""

    def __init__(self):
        self.adj = defaultdict(dict)  # u -> {v: weight}
        self.nodes = set()

    def add_node(self, node):
        self.nodes.add(node)
        if node not in self.adj:
            self.adj[node] = {}

    def add_edge(self, u, v, weight=1):
        self.add_node(u)
        self.add_node(v)
        self.adj[u][v] = weight

    def out_degree(self, u):
        return len(self.adj[u])

    def in_degree(self, u):
        return sum(1 for src in self.adj if u in self.adj[src])

    def transpose(self):
        """
        Reverse direction of all edges.
        Time Complexity: O(V + E)
        """
        rev = DirectedWeightedGraph()
        for node in self.nodes:
            rev.add_node(node)
        for u in self.adj:
            for v, w in self.adj[u].items():
                rev.add_edge(v, u, w)
        return rev

    def display(self):
        for u in sorted(self.nodes):
            edges_str = ", ".join(f"{v}(w={w})" for v, w in self.adj[u].items())
            print(f"  Node {u} (in={self.in_degree(u)}, out={self.out_degree(u)}) -> [{edges_str}]")


def main():
    print("=" * 60)
    print("Directed Weighted Graph with Degree Metrics")
    print("=" * 60)
    g = DirectedWeightedGraph()
    # Edges: A->B(5), A->C(3), B->C(2), C->D(7), D->A(4)
    g.add_edge("A", "B", 5)
    g.add_edge("A", "C", 3)
    g.add_edge("B", "C", 2)
    g.add_edge("C", "D", 7)
    g.add_edge("D", "A", 4)
    g.add_node("E")  # Isolated vertex

    print("Original Graph:")
    g.display()

    print("\n" + "=" * 60)
    print("Reversed / Transposed Graph (G^T)")
    print("=" * 60)
    g_rev = g.transpose()
    g_rev.display()


if __name__ == "__main__":
    main()
