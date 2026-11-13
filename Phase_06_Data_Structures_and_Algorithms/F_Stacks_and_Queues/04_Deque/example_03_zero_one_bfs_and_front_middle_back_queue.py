"""
Phase 6 - Data Structures and Algorithms
Section F: Stacks and Queues
Topic 04: Deque (Double-Ended Queue)
Example 03: 0-1 BFS Shortest Path on a Binary-Weight Graph &
            Design Front-Middle-Back Queue (LeetCode 1670)

Two high-impact algorithmic interview patterns powered by a Deque:

1. 0-1 Breadth-First Search (0-1 BFS) in O(V + E) Time:
   - Standard BFS finds shortest paths when all edge weights are 1.
   - Dijkstra's Algorithm takes O((V + E) log V) using a priority queue.
   - When every edge weight is strictly in `{0, 1}` (e.g., grid mazes where moving in
     the arrow's direction costs 0 and changing direction costs 1 — LeetCode 1368),
     a Deque solves shortest paths in linear **O(V + E)** time!
   - Rule: When relaxing an edge of weight `0`, push the neighbor to the **FRONT**
     (`appendleft`). When relaxing an edge of weight `1`, push to the **BACK** (`append`).

2. Design Front-Middle-Back Queue in O(1) Time Using Two Balanced Deques (LeetCode 1670):
   - Maintain `left_dq` and `right_dq` such that `len(left_dq) == len(right_dq)` or
     `len(left_dq) == len(right_dq) - 1`.
   - The middle of the entire queue is always at the boundary between `left_dq` and
     `right_dq`, making `pushMiddle` and `popMiddle` strict O(1)!
"""

from collections import deque
from typing import Deque, Dict, List, Tuple


def zero_one_bfs_shortest_path(
    num_nodes: int, adj: Dict[int, List[Tuple[int, int]]], src: int
) -> List[int]:
    """
    Computes shortest path distances from `src` to all nodes `0 .. num_nodes - 1`
    in a graph where every edge weight `w` is in `{0, 1}` in O(V + E) time.
    """
    INF = 10**9
    dist = [INF] * num_nodes
    dist[src] = 0
    dq: Deque[int] = deque([src])

    while dq:
        u = dq.popleft()
        for v, weight in adj.get(u, []):
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                if weight == 0:
                    # 0-cost transition stays in the current distance layer -> front!
                    dq.appendleft(v)
                else:
                    # 1-cost transition moves to next distance layer -> back!
                    dq.append(v)

    return dist


class FrontMiddleBackQueue:
    """
    Supports O(1) push/pop at Front, Middle, and Back (LeetCode 1670) by balancing
    two deques `left` and `right` where `0 <= len(right) - len(left) <= 1`.
    """

    def __init__(self) -> None:
        self.left: Deque[int] = deque()
        self.right: Deque[int] = deque()

    def _rebalance(self) -> None:
        """Maintains invariant: len(left) == len(right) or len(left) + 1 == len(right)."""
        if len(self.left) > len(self.right):
            self.right.appendleft(self.left.pop())
        elif len(self.right) > len(self.left) + 1:
            self.left.append(self.right.popleft())

    def pushFront(self, val: int) -> None:
        self.left.appendleft(val)
        self._rebalance()

    def pushMiddle(self, val: int) -> None:
        self.left.append(val)
        self._rebalance()

    def pushBack(self, val: int) -> None:
        self.right.append(val)
        self._rebalance()

    def popFront(self) -> int:
        if not self.left and not self.right:
            return -1
        val = self.left.popleft() if self.left else self.right.popleft()
        self._rebalance()
        return val

    def popMiddle(self) -> int:
        if not self.left and not self.right:
            return -1
        if len(self.left) == len(self.right):
            val = self.left.pop()
        else:
            val = self.right.popleft()
        self._rebalance()
        return val

    def popBack(self) -> int:
        if not self.left and not self.right:
            return -1
        val = self.right.pop()
        self._rebalance()
        return val

    def to_list(self) -> List[int]:
        return list(self.left) + list(self.right)


if __name__ == "__main__":
    print("=" * 72)
    print("1. 0-1 BFS Shortest Path on a Binary-Weight Graph in O(V + E) Time")
    print("=" * 72)
    # Graph: 0 --(1)--> 1, 0 --(1)--> 2, 2 --(0)--> 3, 3 --(0)--> 1, 1 --(1)--> 4
    # Shortest path 0 -> 1 is via 0 -> 2 -> 3 -> 1 with total weight 1 + 0 + 0 = 1,
    # and 0 -> 4 has weight 1 + 1 = 2 (whereas direct 0 -> 1 -> 4 also has weight 2,
    # let's make 0 -> 1 have weight 1 and 0 -> 2 have weight 0 so 0->2->3->1 costs 0!).
    graph = {
        0: [(1, 1), (2, 1)],
        2: [(3, 0)],
        3: [(1, 0), (4, 1)],
        1: [(4, 1)],
    }
    distances = zero_one_bfs_shortest_path(num_nodes=5, adj=graph, src=0)
    print(f"Graph edges (u -> (v, w in {{0,1}})): {graph}")
    print(f"Shortest distances from node 0     : {distances}")

    print("\n" + "=" * 72)
    print("2. Front-Middle-Back Queue in O(1) via Two Balanced Deques (LeetCode 1670)")
    print("=" * 72)
    fmb = FrontMiddleBackQueue()
    fmb.pushFront(1)
    fmb.pushBack(2)
    fmb.pushMiddle(3)
    fmb.pushMiddle(4)
    print(f"After pushFront(1), pushBack(2), pushMiddle(3), pushMiddle(4): {fmb.to_list()}")
    print(f"popFront()  -> {fmb.popFront()} | Queue: {fmb.to_list()}")
    print(f"popMiddle() -> {fmb.popMiddle()} | Queue: {fmb.to_list()}")
    print(f"popMiddle() -> {fmb.popMiddle()} | Queue: {fmb.to_list()}")
    print(f"popBack()   -> {fmb.popBack()} | Queue: {fmb.to_list()}")
