# Topic 08: Nested Data Structures

---

## 1. Introduction

A **Nested Data Structure** is a collection (`list`, `dict`, `tuple`, `set`) whose elements are themselves other collections. Real-world data is almost never a flat 1D array:
- A **2D Matrix / Grid** is a `list` of `list`s (`list[list[int]]`).
- A **JSON API Response** is typically a `list` of `dict`s (`list[dict[str, Any]]`) or a deeply nested `dict` of `dict`s.
- A **Weighted Graph Adjacency List** in DSA is a `dict` mapping each node to a `list` of `(neighbor, weight)` tuples (`dict[str, list[tuple[str, int]]]`).

---

## 2. Why is it used?

1. **Grid & Matrix Algorithms:** Number of Islands, Rotting Oranges, Dynamic Programming 2D tables (`dp[r][c]`), and Sudoku boards all operate on `list[list[...]]`.
2. **Backend & Full-Stack Data Modeling:** Representing users with nested lists of roles, orders, and shipping addresses.
3. **Graph & Tree Representations:** Representing networks of cities, social connections, and course prerequisites.

---

## 3. Syntax

```python
# 1. 2D Matrix (List of Lists): grid[row][col]
grid = [
    [1, 2, 3],
    [4, 5, 6],
]
center_right = grid[1][2]  # Row 1, Column 2 -> 6

# 2. List of Dictionaries (JSON Table)
users = [
    {"id": 1, "tags": ["python", "dsa"]},
    {"id": 2, "tags": ["sql"]},
]
first_tag_of_first_user = users[0]["tags"][0]  # 'python'

# 3. Safe Chained .get() on Nested Dictionaries
port = config.get("server", {}).get("database", {}).get("port", 5432)
```

---

## 4. Explanation (Navigating & Copying Nested Structures)

1. **Chained Indexing Reads Left-to-Right:**
   - In `students[0]["scores"]["coding"]`:
     - `students[0]` retrieves the first student dictionary.
     - `["scores"]` retrieves the inner scores dictionary.
     - `["coding"]` retrieves the integer `95`.
2. **4-Directional Grid Neighbor Pattern (Crucial for DSA):**
   - To check Up, Down, Left, and Right from cell `(r, c)` in an `R x C` grid:
     ```python
     for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
         nr, nc = r + dr, c + dc
         if 0 <= nr < R and 0 <= nc < C:
             # (nr, nc) is a valid in-bounds neighbor!
     ```
3. **Shallow Copy vs Deep Copy Warning:**
   - Calling `matrix.copy()` or `matrix[:]` on a 2D list only copies the **outer list**; the inner row lists are still shared! To clone a nested structure completely, use `copy.deepcopy(matrix)` or `[row[:] for row in matrix]`.

---

## 5. Examples

All three runnable examples are located in this folder:
- [`example_01_2d_matrices_and_diagonals.py`](example_01_2d_matrices_and_diagonals.py)
- [`example_02_list_of_dicts_analytics.py`](example_02_list_of_dicts_analytics.py)
- [`example_03_nested_dicts_and_graph_adjacency.py`](example_03_nested_dicts_and_graph_adjacency.py)

### Example 1: 2D Matrices — Diagonals, Sums & 4-Directional Neighbors (`example_01_2d_matrices_and_diagonals.py`)

```python
def get_valid_neighbors(grid: list[list[int]], r: int, c: int) -> list[tuple[int, int, int]]:
    """Return (row, col, value) for Up, Down, Left, Right neighbors within bounds."""
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    neighbors = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc, grid[nr][nc]))
    return neighbors


def main() -> None:
    matrix = [
        [10, 20, 30],
        [40, 50, 60],
        [70, 80, 90],
    ]
    n = len(matrix)

    primary_diag = [matrix[i][i] for i in range(n)]
    secondary_diag = [matrix[i][n - 1 - i] for i in range(n)]

    print("=== 1. 2D Matrix Diagonals & Row/Column Sums ===")
    print(f"Primary Diagonal   : {primary_diag} (Sum={sum(primary_diag)})")
    print(f"Secondary Diagonal : {secondary_diag} (Sum={sum(secondary_diag)})")
    print(f"Row Sums           : {[sum(row) for row in matrix]}")
    print(f"Column Sums        : {[sum(matrix[r][c] for r in range(n)) for c in range(n)]}")

    print("\n=== 2. 4-Directional Neighbors of Center Cell (1, 1) and Corner (0, 0) ===")
    print(f"Neighbors of (1, 1): {get_valid_neighbors(matrix, 1, 1)}")
    print(f"Neighbors of (0, 0): {get_valid_neighbors(matrix, 0, 0)}")


if __name__ == "__main__":
    main()
```

### Example 2: List of Dictionaries — JSON-Style Analytics (`example_02_list_of_dicts_analytics.py`)

```python
def main() -> None:
    students = [
        {
            "id": 101,
            "name": "Divya Prakash",
            "skills": ["Python", "DSA", "SQL"],
            "scores": {"coding": 95, "system_design": 88},
        },
        {
            "id": 102,
            "name": "Aarav Sharma",
            "skills": ["Java", "Spring", "SQL"],
            "scores": {"coding": 84, "system_design": 91},
        },
        {
            "id": 103,
            "name": "Sneha Verma",
            "skills": ["Python", "PyTorch", "DSA"],
            "scores": {"coding": 92, "system_design": 85},
        },
    ]

    print("=== 1. Filtering Nested Records (Python + DSA Skills) ===")
    python_dsa_candidates = [
        s["name"]
        for s in students
        if "Python" in s["skills"] and "DSA" in s["skills"]
    ]
    print(f"Python + DSA Candidates : {python_dsa_candidates}")

    print("\n=== 2. Ranking by Nested Total Score ===")
    ranked = sorted(
        students,
        key=lambda s: s["scores"]["coding"] + s["scores"]["system_design"],
        reverse=True,
    )
    for rank, s in enumerate(ranked, start=1):
        total = s["scores"]["coding"] + s["scores"]["system_design"]
        print(f"  #{rank}: {s['name']:<15} | Total: {total} (Coding: {s['scores']['coding']})")


if __name__ == "__main__":
    main()
```

### Example 3: Safe Deep Dict Lookup & Weighted Graph Adjacency List (`example_03_nested_dicts_and_graph_adjacency.py`)

```python
from typing import Any


def deep_get(data: dict, path: list[str], default: Any = None) -> Any:
    """Safely navigate a nested dictionary along `path` keys."""
    current: Any = data
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def main() -> None:
    app_config = {
        "server": {
            "database": {
                "host": "db.internal.local",
                "port": 5432,
            }
        }
    }

    print("=== 1. Safe Deep Dictionary Navigation ===")
    db_host = deep_get(app_config, ["server", "database", "host"], default="localhost")
    redis_host = deep_get(app_config, ["server", "cache", "host"], default="127.0.0.1")
    print(f"Resolved DB Host    : {db_host}")
    print(f"Resolved Cache Host : {redis_host} (Fallback default)")

    print("\n=== 2. Weighted Graph Adjacency List (dict of list of tuples) ===")
    flight_graph: dict[str, list[tuple[str, int]]] = {
        "DEL": [("BOM", 1150), ("BLR", 1740)],
        "BOM": [("BLR", 840), ("HYD", 620)],
        "BLR": [("HYD", 500)],
    }
    for origin, edges in flight_graph.items():
        formatted_edges = ", ".join(f"{dest} ({km} km)" for dest, km in edges)
        print(f"  {origin} -> {formatted_edges}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output for Example 1:
```text
=== 1. 2D Matrix Diagonals & Row/Column Sums ===
Primary Diagonal   : [10, 50, 90] (Sum=150)
Secondary Diagonal : [30, 50, 70] (Sum=150)
Row Sums           : [60, 150, 240]
Column Sums        : [120, 150, 180]

=== 2. 4-Directional Neighbors of Center Cell (1, 1) and Corner (0, 0) ===
Neighbors of (1, 1): [(0, 1, 20), (2, 1, 80), (1, 0, 40), (1, 2, 60)]
Neighbors of (0, 0): [(1, 0, 40), (0, 1, 20)]
```

### Output for Example 2:
```text
=== 1. Filtering Nested Records (Python + DSA Skills) ===
Python + DSA Candidates : ['Divya Prakash', 'Sneha Verma']

=== 2. Ranking by Nested Total Score ===
  #1: Divya Prakash   | Total: 183 (Coding: 95)
  #2: Sneha Verma     | Total: 177 (Coding: 92)
  #3: Aarav Sharma    | Total: 175 (Coding: 84)
```

### Output for Example 3:
```text
=== 1. Safe Deep Dictionary Navigation ===
Resolved DB Host    : db.internal.local
Resolved Cache Host : 127.0.0.1 (Fallback default)

=== 2. Weighted Graph Adjacency List (dict of list of tuples) ===
  DEL -> BOM (1150 km), BLR (1740 km)
  BOM -> BLR (840 km), HYD (620 km)
  BLR -> HYD (500 km)
```

---

## 7. Code Explanation

- **`primary_diag = [matrix[i][i] for i in range(n)]` and `secondary_diag = [matrix[i][n - 1 - i] for i in range(n)]`:** Extracts both diagonals of an $N \times N$ matrix in **`O(N)`** time (no nested loop required!).
- **`directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]`:** Standard DSA offset table for moving Up, Down, Left, and Right from `(r, c)` without writing 4 repetitive `if` blocks.
- **`deep_get(data, path, default)`:** Safely walks down arbitrary key paths without crashing when an intermediate dictionary is missing or `None`.

---

## 8. Common Mistakes

1. **Confusing `grid[x][y]` with Cartesian `(x, y)` Coordinates:**
   In 2D arrays, the **first** index is the vertical **Row (`r`)** (top-to-bottom) and the **second** index is the horizontal **Column (`c`)** (left-to-right): `grid[row][col]`.
2. **Shallow Copying a 2D Matrix (`copy_grid = grid.copy()`):**
   Mutating `copy_grid[0][0] = 99` also mutates `grid[0][0]` because both outer lists point to the same inner row objects! Use `[row[:] for row in grid]` for a 2D list of primitives, or `copy.deepcopy(grid)` for arbitrary nesting.
3. **Chaining `.get()` When a Key Exists with Value `None`:**
   If `config = {"server": None}`, calling `config.get("server", {}).get("host")` raises `AttributeError: 'NoneType' object has no attribute 'get'` because `"server"` exists and returns `None`! Use `(config.get("server") or {}).get("host")` or `deep_get()`.

---

## 9. Practice Questions

1. **Easy:** Write a function `matrix_diagonal_sum(mat: list[list[int]]) -> int` (LeetCode 1572) that returns the sum of the primary and secondary diagonals of an $N \times N$ matrix without double-counting the center element when $N$ is odd.
2. **Medium:** Write a function `rotate_matrix_90_clockwise(matrix: list[list[int]]) -> None` (LeetCode 48) that rotates an $N \times N$ 2D matrix by 90 degrees clockwise **in-place** (`O(1)` extra space) by first transposing across the main diagonal and then reversing each row.
3. **Hard:** Write a recursive function `flatten_json(nested: dict[str, Any], parent_key: str = "", sep: str = ".") -> dict[str, Any]` that flattens a deeply nested dictionary into a single-level dictionary with dot-separated keys (e.g., `{"a": {"b": 1}} -> {"a.b": 1}`).

---

## 10. Interview Questions

### Q1: How do you rotate an $N \times N$ matrix 90 degrees clockwise in-place (`O(1)` auxiliary space)?
**Answer:** Perform two `O(N^2)` in-place passes:
1. **Transpose the matrix across the main diagonal:** For `r` in `0..N-1` and `c` in `r+1..N-1`, swap `matrix[r][c]` and `matrix[c][r]`.
2. **Reverse each row:** For each `row` in `matrix`, call `row.reverse()`.

### Q2: Why is an Adjacency List (`dict[int, list[int]]`) usually preferred over an Adjacency Matrix (`list[list[int]]`) for graphs?
**Answer:** Real-world graphs (road networks, social graphs, web links) are **sparse** ($E \ll V^2$). An Adjacency Matrix always consumes `O(V^2)` memory and takes `O(V)` time just to iterate over a node's neighbors. An Adjacency List consumes only **`O(V + E)`** memory and iterates over a node's actual neighbors in `O(degree(u))` time.

### Q3: How can you transpose a 2D matrix `grid` in a single Python expression using `zip`?
**Answer:** `[list(col) for col in zip(*grid)]`. The unpacking operator `*grid` passes each row of `grid` as a separate argument to `zip()`, which pairs up elements column-by-column!
