"""
Example 03: All Paths Source to Target and Path Sum Problems using DFS Backtracking

Demonstrates:
1. Finding all paths from source node (0) to destination node (n - 1) in a DAG (LeetCode 797).
2. Path sum in a directed weighted graph (all paths matching target cost).
3. Finding paths in a general graph with cycles using explicit backtracking (visiting and unvisiting).

Time Complexity: O(2^V * V) worst case for all paths in DAG (or O(V! * V) in dense general graphs).
Space Complexity: O(V) stack space and path tracking.
"""

from typing import Dict, List, Tuple


class PathFinderDFS:
    @staticmethod
    def all_paths_dag(graph: List[List[int]]) -> List[List[int]]:
        """Finds all paths from node 0 to node n-1 in a Directed Acyclic Graph (DAG).

        LeetCode 797.
        """
        target = len(graph) - 1
        results: List[List[int]] = []

        def _dfs(node: int, current_path: List[int]) -> None:
            if node == target:
                results.append(list(current_path))
                return

            for neighbor in graph[node]:
                current_path.append(neighbor)
                _dfs(neighbor, current_path)
                current_path.pop()  # Backtrack

        _dfs(0, [0])
        return results

    @staticmethod
    def all_paths_cyclic_graph(
        adj: Dict[int, List[int]], start: int, target: int
    ) -> List[List[int]]:
        """Finds all simple paths from start to target in a graph that may contain cycles."""
        results: List[List[int]] = []
        visited = set()

        def _backtrack(node: int, path: List[int]) -> None:
            if node == target:
                results.append(list(path))
                return

            visited.add(node)
            for neighbor in adj.get(node, []):
                if neighbor not in visited:
                    path.append(neighbor)
                    _backtrack(neighbor, path)
                    path.pop()  # Backtrack path
            visited.remove(node)  # Backtrack visited state

        path = [start]
        _backtrack(start, path)
        return results

    @staticmethod
    def path_with_target_sum(
        adj: Dict[int, List[Tuple[int, int]]], start: int, target: int, target_sum: int
    ) -> List[Tuple[List[int], int]]:
        """Finds all paths from start to target whose sum of edge weights equals target_sum."""
        valid_paths: List[Tuple[List[int], int]] = []
        visited = set()

        def _dfs(u: int, curr_sum: int, path: List[int]) -> None:
            if u == target and curr_sum == target_sum:
                valid_paths.append((list(path), curr_sum))
                return

            visited.add(u)
            for v, weight in adj.get(u, []):
                if v not in visited and curr_sum + weight <= target_sum:
                    path.append(v)
                    _dfs(v, curr_sum + weight, path)
                    path.pop()
            visited.remove(u)

        _dfs(start, 0, [start])
        return valid_paths


def main() -> None:
    print("=" * 60)
    print("1. All Paths from Source to Target in DAG (LeetCode 797)")
    print("=" * 60)

    # DAG where node 0 connects to 1 and 2, 1 -> 3, 2 -> 3
    dag_graph = [[1, 2], [3], [3], []]
    paths = PathFinderDFS.all_paths_dag(dag_graph)
    print("Graph Adjacency List :", dag_graph)
    print("Paths from 0 to 3    :", paths)

    # More complex DAG
    complex_dag = [[4, 3, 1], [3, 2, 4], [3], [4], []]
    print("\nComplex DAG Paths from 0 to 4:")
    for p in PathFinderDFS.all_paths_dag(complex_dag):
        print(f"  Path: {' -> '.join(map(str, p))}")

    print("\n" + "=" * 60)
    print("2. Simple Paths in Cyclic Graph (Backtracking Visited)")
    print("=" * 60)

    cyclic_adj = {
        0: [1, 2, 3],
        1: [0, 3],
        2: [0, 3],
        3: [0, 1, 2, 4],
        4: [3],
    }
    cyclic_paths = PathFinderDFS.all_paths_cyclic_graph(cyclic_adj, start=0, target=4)
    print("Cyclic Graph Paths from 0 to 4:")
    for p in sorted(cyclic_paths):
        print(f"  {' -> '.join(map(str, p))}")

    print("\n" + "=" * 60)
    print("3. Target Path Sum in Weighted Graph")
    print("=" * 60)

    weighted_graph = {
        1: [(2, 5), (3, 3)],
        2: [(4, 5), (5, 7)],
        3: [(2, 2), (5, 7)],
        4: [(5, 2)],
        5: [],
    }
    target_sum = 12
    matching_paths = PathFinderDFS.path_with_target_sum(
        weighted_graph, start=1, target=5, target_sum=target_sum
    )

    print(f"Paths from 1 to 5 with exact edge weight sum = {target_sum}:")
    for path, weight in matching_paths:
        print(f"  Path: {' -> '.join(map(str, path))} | Total Weight: {weight}")


if __name__ == "__main__":
    main()
