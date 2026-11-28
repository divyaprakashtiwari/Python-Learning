"""
Example 01: DFS Recursive and Iterative Implementations

Demonstrates:
1. Recursive DFS traversal on an adjacency list graph.
2. Iterative DFS using an explicit LIFO stack.
3. Pre-order and Post-order graph exploration orders.
4. Handling disconnected graphs (forest traversal).

Time Complexity: O(V + E)
Space Complexity: O(V) for visited set and call/explicit stack.
"""

from typing import Dict, List, Set


class GraphDFS:
    def __init__(self, adj_list: Dict[int, List[int]]) -> None:
        self.adj = adj_list

    def dfs_recursive(self, start_node: int) -> List[int]:
        """Performs depth-first search starting from start_node recursively."""
        visited: Set[int] = set()
        traversal_order: List[int] = []

        def _dfs(node: int) -> None:
            visited.add(node)
            traversal_order.append(node)
            for neighbor in sorted(self.adj.get(node, [])):
                if neighbor not in visited:
                    _dfs(neighbor)

        _dfs(start_node)
        return traversal_order

    def dfs_iterative(self, start_node: int) -> List[int]:
        """Performs DFS using an explicit LIFO stack."""
        visited: Set[int] = set()
        traversal_order: List[int] = []
        stack: List[int] = [start_node]

        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            traversal_order.append(node)
            # Push in reverse sorted order so smaller numbered neighbors pop first
            for neighbor in sorted(self.adj.get(node, []), reverse=True):
                if neighbor not in visited:
                    stack.append(neighbor)

        return traversal_order

    def pre_and_post_order(self, start_node: int) -> tuple[List[int], List[int]]:
        """Returns pre-order (entry) and post-order (exit) visit sequences."""
        visited: Set[int] = set()
        pre_order: List[int] = []
        post_order: List[int] = []

        def _dfs(u: int) -> None:
            visited.add(u)
            pre_order.append(u)
            for v in sorted(self.adj.get(u, [])):
                if v not in visited:
                    _dfs(v)
            post_order.append(u)

        _dfs(start_node)
        return pre_order, post_order

    def dfs_all_components(self, all_nodes: List[int]) -> List[List[int]]:
        """Traverses all connected components of a potentially disconnected graph."""
        visited: Set[int] = set()
        components: List[List[int]] = []

        for node in sorted(all_nodes):
            if node not in visited:
                component: List[int] = []

                def _dfs(curr: int) -> None:
                    visited.add(curr)
                    component.append(curr)
                    for nxt in sorted(self.adj.get(curr, [])):
                        if nxt not in visited:
                            _dfs(nxt)

                _dfs(node)
                components.append(component)

        return components


def main() -> None:
    print("=" * 60)
    print("1. Recursive vs Iterative DFS Traversal")
    print("=" * 60)

    # Graph representation:
    #      0
    #     / \
    #    1   2
    #   / \   \
    #  3   4   5
    #       \ /
    #        6
    adj_graph = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 5],
        3: [1],
        4: [1, 6],
        5: [2, 6],
        6: [4, 5],
    }

    g = GraphDFS(adj_graph)
    rec_result = g.dfs_recursive(0)
    iter_result = g.dfs_iterative(0)
    pre, post = g.pre_and_post_order(0)

    print(f"Graph Nodes           : {list(adj_graph.keys())}")
    print(f"Recursive DFS Order   : {rec_result}")
    print(f"Iterative DFS Order   : {iter_result}")
    print(f"Pre-order (Discovery) : {pre}")
    print(f"Post-order (Finish)   : {post}")

    print("\n" + "=" * 60)
    print("2. Disconnected Graph DFS (Forest Components)")
    print("=" * 60)

    # Component 1: {10, 20, 30}, Component 2: {40, 50}, Component 3: {60}
    forest = {
        10: [20],
        20: [10, 30],
        30: [20],
        40: [50],
        50: [40],
        60: [],
    }
    all_nodes = [10, 20, 30, 40, 50, 60]
    forest_g = GraphDFS(forest)
    components = forest_g.dfs_all_components(all_nodes)

    print(f"Total Disconnected Components: {len(components)}")
    for idx, comp in enumerate(components, start=1):
        print(f"  Component {idx}: {comp}")


if __name__ == "__main__":
    main()
