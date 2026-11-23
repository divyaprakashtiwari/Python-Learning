"""
Phase 6 - Section J.02: BFS (Breadth-First Search)
Example 02: Shortest Path in Unweighted Graph & Word Ladder

Demonstrating:
1. Shortest path finding in an unweighted graph with full path reconstruction.
2. Word Ladder I (shortest transformation sequence between words).
"""

from collections import defaultdict, deque


def shortest_path_unweighted(adj, start, target):
    """
    Find shortest path (minimum edge count) between start and target in unweighted graph.
    Returns: (path_length, full_path_list)
    Time Complexity: O(V + E)
    """
    if start == target:
        return 0, [start]

    visited = {start}
    parent = {start: None}
    queue = deque([start])

    found = False
    while queue:
        curr = queue.popleft()
        if curr == target:
            found = True
            break

        for neighbor in adj.get(curr, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = curr
                queue.append(neighbor)

    if not found:
        return -1, []

    # Reconstruct path backwards from target to start
    path = []
    curr = target
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()

    return len(path) - 1, path


def word_ladder_length(begin_word, end_word, word_list):
    """
    Shortest transformation sequence from begin_word to end_word.
    Only one letter can be changed at a time; each transformed word must exist in word_list.
    Time Complexity: O(M^2 * N) where M is word length, N is number of words.
    """
    words = set(word_list)
    if end_word not in words:
        return 0

    queue = deque([(begin_word, 1)])
    visited = {begin_word}

    while queue:
        word, steps = queue.popleft()
        if word == end_word:
            return steps

        # Try mutating each character from 'a' to 'z'
        for i in range(len(word)):
            for c in "abcdefghijklmnopqrstuvwxyz":
                next_word = word[:i] + c + word[i + 1:]
                if next_word in words and next_word not in visited:
                    visited.add(next_word)
                    queue.append((next_word, steps + 1))

    return 0


def main():
    print("=" * 60)
    print("1. Shortest Path in Unweighted Graph with Reconstruction")
    print("=" * 60)
    # Subway network:
    #   A - B - C - D
    #   |       |   |
    #   E - - - F - G
    network = {
        "A": ["B", "E"],
        "B": ["A", "C"],
        "C": ["B", "D", "F"],
        "D": ["C", "G"],
        "E": ["A", "F"],
        "F": ["E", "C", "G"],
        "G": ["D", "F"]
    }
    start_v, target_v = "A", "G"
    dist, path = shortest_path_unweighted(network, start_v, target_v)
    print(f"Shortest path from {start_v} to {target_v}:")
    print(f"  Distance: {dist} edges")
    print(f"  Path    : {' -> '.join(path)}")

    print("\n" + "=" * 60)
    print("2. Word Ladder Problem")
    print("=" * 60)
    begin = "hit"
    end = "cog"
    w_list = ["hot", "dot", "dog", "lot", "log", "cog"]
    min_steps = word_ladder_length(begin, end, w_list)
    print(f"Begin: '{begin}', End: '{end}'")
    print(f"Dictionary: {w_list}")
    print(f"Shortest Transformation Length: {min_steps} words (hit -> hot -> dot -> dog -> cog)")


if __name__ == "__main__":
    main()
