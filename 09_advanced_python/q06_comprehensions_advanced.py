"""
Topic: Advanced Python - Advanced Comprehensions
-----------------------------------------------
Questions Covered:
1. Multi-Level Nested List Comprehensions: Flattening 3D matrices, Cartesian products, and filter chains.
2. Advanced Dict Comprehensions: Inverted mappings, multi-value aggregation, and nested transformations.
3. Set Comprehensions: Normalization, unique token extraction, and set operations.
4. Walrus Operator (:=) in Comprehensions: Eliminating duplicate expensive evaluations in filtering.
5. Pure Comprehension Matrix Algebra: Transposition, scalar multiplication, and inner dot products.
6. Grouping and Bucketing via Comprehensions: Building category histograms and inverted indices.
7. Nested Generator Expressions: Memory-bounded lazy streaming pipelines without intermediate lists.
8. Tree and Graph Traversal Comprehensions: Extracting leaf nodes and recursive path evaluations.
9. Tabular Data Pivoting: Reshaping normalized relation rows into multi-dimensional pivoted records.
10. Architectural System: Declarative SQL-like In-Memory ETL Query Engine using advanced comprehensions.
"""

from typing import List, Dict, Any, Tuple, Set, Iterable, Callable, Optional


# ==============================================================================
# Question 1: Multi-Level Nested List Comprehensions
# ==============================================================================
def flatten_3d_cube(cube: List[List[List[int]]], min_threshold: int) -> List[int]:
    """
    Flattens a 3D matrix into a 1D list containing only elements >= min_threshold.
    Demonstrates nested 'for' order: outer to inner.
    """
    return [
        val
        for matrix in cube
        for row in matrix
        for val in row
        if val >= min_threshold
    ]


def test_q1_nested_list_comprehension():
    cube = [
        [[1, 2], [3, 4]],
        [[5, 6], [7, 8]],
    ]
    flattened = flatten_3d_cube(cube, min_threshold=4)
    assert flattened == [4, 5, 6, 7, 8]

    # Cartesian product with filter
    suits = ["C", "D", "H", "S"]
    ranks = ["A", "K", "Q"]
    cards = [f"{r}{s}" for s in suits for r in ranks if s in ("H", "S")]
    assert len(cards) == 6
    assert cards[:3] == ["AH", "KH", "QH"]
    print("=== Q1: Multi-Level Nested List Comprehension Verified ===")


# ==============================================================================
# Question 2: Advanced Dict Comprehensions
# ==============================================================================
def invert_and_group(source_dict: Dict[str, str]) -> Dict[str, List[str]]:
    """
    Inverts a dictionary where values become keys and original keys are grouped
    into sorted lists of keys sharing that value.
    """
    unique_vals = {v for v in source_dict.values()}
    return {
        val: sorted([k for k, v in source_dict.items() if v == val])
        for val in unique_vals
    }


def test_q2_dict_comprehensions():
    dept_map = {
        "alice": "Engineering",
        "bob": "Marketing",
        "charlie": "Engineering",
        "dave": "Finance",
        "eve": "Marketing",
    }
    grouped = invert_and_group(dept_map)
    assert grouped == {
        "Engineering": ["alice", "charlie"],
        "Marketing": ["bob", "eve"],
        "Finance": ["dave"],
    }

    # Nested dictionary comprehension: multiplication table
    table = {i: {j: i * j for j in range(1, 4)} for i in range(1, 4)}
    assert table[2][3] == 6
    assert table[3][2] == 6
    print("=== Q2: Advanced Dict Comprehensions Verified ===")


# ==============================================================================
# Question 3: Set Comprehensions
# ==============================================================================
def extract_unique_domain_extensions(urls: List[str]) -> Set[str]:
    """
    Extracts unique lowercase domain extensions (e.g. 'com', 'org', 'io') from URLs.
    """
    return {
        url.split("/")[-1].split(".")[-1].lower()
        for url in urls
        if "." in url.split("/")[-1]
    }


def test_q3_set_comprehensions():
    urls = [
        "https://example.com",
        "http://openai.COM",
        "https://github.io",
        "http://python.ORG",
        "https://sub.test.io",
    ]
    extensions = extract_unique_domain_extensions(urls)
    assert extensions == {"com", "io", "org"}
    print("=== Q3: Set Comprehensions Verified ===")


# ==============================================================================
# Question 4: Walrus Operator (:=) in Comprehensions
# ==============================================================================
expensive_call_count = 0


def expensive_square_root_approx(n: int) -> float:
    """Simulates an expensive calculation."""
    global expensive_call_count
    expensive_call_count += 1
    return n ** 0.5


def filter_and_format_roots(numbers: List[int], threshold: float) -> List[str]:
    """
    Computes expensive square root once per element using the walrus operator (:=)
    in the filter clause, reusing the bound variable in the output expression.
    """
    return [
        f"root({n})={root:.2f}"
        for n in numbers
        if (root := expensive_square_root_approx(n)) >= threshold
    ]


def test_q4_walrus_in_comprehensions():
    global expensive_call_count
    expensive_call_count = 0

    nums = [4, 9, 16, 25, 36]  # roots: 2, 3, 4, 5, 6
    formatted = filter_and_format_roots(nums, threshold=4.0)

    # Elements >= 4.0 are 16 (4.00), 25 (5.00), 36 (6.00)
    assert formatted == ["root(16)=4.00", "root(25)=5.00", "root(36)=6.00"]
    # Exactly 5 calls made (one per number in nums), never duplicated
    assert expensive_call_count == 5
    print("=== Q4: Walrus Operator (:=) in Comprehensions Verified ===")


# ==============================================================================
# Question 5: Pure Comprehension Matrix Algebra
# ==============================================================================
def transpose_matrix(matrix: List[List[float]]) -> List[List[float]]:
    """Transposes an M x N matrix into an N x M matrix using list comprehension."""
    cols = len(matrix[0])
    return [[matrix[row_idx][col_idx] for row_idx in range(len(matrix))] for col_idx in range(cols)]


def matrix_vector_dot(matrix: List[List[float]], vector: List[float]) -> List[float]:
    """Computes M x N matrix multiplied by N x 1 vector using list comprehensions."""
    return [sum(row[i] * vector[i] for i in range(len(vector))) for row in matrix]


def test_q5_matrix_algebra():
    m = [
        [1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0],
    ]
    t = transpose_matrix(m)
    assert t == [
        [1.0, 4.0],
        [2.0, 5.0],
        [3.0, 6.0],
    ]

    v = [2.0, 3.0, 4.0]
    # [1*2 + 2*3 + 3*4, 4*2 + 5*3 + 6*4] = [2 + 6 + 12, 8 + 15 + 24] = [20.0, 47.0]
    prod = matrix_vector_dot(m, v)
    assert prod == [20.0, 47.0]
    print("=== Q5: Pure Comprehension Matrix Algebra Verified ===")


# ==============================================================================
# Question 6: Grouping and Bucketing via Comprehensions
# ==============================================================================
def build_score_grade_buckets(scores: Dict[str, int]) -> Dict[str, List[str]]:
    """
    Groups students into grade bands (A: 90+, B: 80-89, C: 70-79, F: <70)
    using pure dictionary and list comprehensions.
    """
    bands = {
        "A": lambda s: s >= 90,
        "B": lambda s: 80 <= s < 90,
        "C": lambda s: 70 <= s < 80,
        "F": lambda s: s < 70,
    }
    return {
        band: sorted([student for student, score in scores.items() if predicate(score)])
        for band, predicate in bands.items()
    }


def test_q6_grouping_and_bucketing():
    scores = {
        "Alice": 95,
        "Bob": 82,
        "Charlie": 78,
        "David": 65,
        "Eve": 91,
        "Frank": 88,
    }
    buckets = build_score_grade_buckets(scores)
    assert buckets["A"] == ["Alice", "Eve"]
    assert buckets["B"] == ["Bob", "Frank"]
    assert buckets["C"] == ["Charlie"]
    assert buckets["F"] == ["David"]
    print("=== Q6: Grouping and Bucketing via Comprehensions Verified ===")


# ==============================================================================
# Question 7: Nested Generator Expressions for Lazy Streaming
# ==============================================================================
def lazy_streaming_stats(data_stream: Iterable[str]) -> Tuple[int, float]:
    """
    Consumes a stream of raw delimited data without building in-memory intermediate lists.
    Returns (count, average_val).
    """
    # Generator pipeline stages
    stripped = (line.strip() for line in data_stream if line.strip())
    non_comments = (line for line in stripped if not line.startswith("#"))
    numbers = (float(line.split(",")[1]) for line in non_comments)

    total = 0.0
    count = 0
    for num in numbers:
        total += num
        count += 1

    return count, (total / count if count else 0.0)


def test_q7_nested_generator_expressions():
    raw_lines = [
        "id1, 10.5\n",
        "# header/comment",
        "id2, 20.5\n",
        "  \n",
        "id3, 30.0\n",
    ]
    count, avg = lazy_streaming_stats(raw_lines)
    assert count == 3
    assert avg == (10.5 + 20.5 + 30.0) / 3
    print("=== Q7: Nested Generator Expressions Verified ===")


# ==============================================================================
# Question 8: Tree Traversal and Path Extractions with Comprehensions
# ==============================================================================
def collect_all_leaf_values(node: Dict[str, Any]) -> List[Any]:
    """
    Recursively collects all leaf node values from a hierarchical dictionary tree.
    """
    if "children" not in node or not node["children"]:
        return [node.get("value")]

    return [
        leaf
        for child in node["children"]
        for leaf in collect_all_leaf_values(child)
    ]


def test_q8_tree_comprehension():
    tree = {
        "name": "root",
        "children": [
            {
                "name": "branch1",
                "children": [
                    {"name": "leaf1", "value": 10},
                    {"name": "leaf2", "value": 20},
                ],
            },
            {
                "name": "branch2",
                "children": [
                    {"name": "leaf3", "value": 30},
                ],
            },
        ],
    }
    leaves = collect_all_leaf_values(tree)
    assert leaves == [10, 20, 30]
    print("=== Q8: Tree Traversal Comprehension Verified ===")


# ==============================================================================
# Question 9: Tabular Data Pivoting
# ==============================================================================
def pivot_tabular_data(
    records: List[Dict[str, Any]], row_key: str, col_key: str, val_key: str, default: Any = 0
) -> Dict[str, Dict[str, Any]]:
    """
    Pivots flat tabular records into a nested dict: {row_value: {col_value: val_value}}.
    Missing values filled with default.
    """
    unique_rows = sorted({r[row_key] for r in records})
    unique_cols = sorted({r[col_key] for r in records})

    # Build lookup map
    lookup = {(r[row_key], r[col_key]): r[val_key] for r in records}

    return {
        row: {col: lookup.get((row, col), default) for col in unique_cols}
        for row in unique_rows
    }


def test_q9_tabular_pivoting():
    flat_grades = [
        {"student": "Alice", "subject": "Math", "score": 90},
        {"student": "Alice", "subject": "Physics", "score": 85},
        {"student": "Bob", "subject": "Math", "score": 78},
        {"student": "Bob", "subject": "Chemistry", "score": 92},
    ]
    pivoted = pivot_tabular_data(flat_grades, row_key="student", col_key="subject", val_key="score", default=0)

    assert pivoted["Alice"] == {"Chemistry": 0, "Math": 90, "Physics": 85}
    assert pivoted["Bob"] == {"Chemistry": 92, "Math": 78, "Physics": 0}
    print("=== Q9: Tabular Data Pivoting Verified ===")


# ==============================================================================
# Question 10: Architectural Declarative In-Memory Query Engine
# ==============================================================================
class ComprehensionQueryEngine:
    """
    Production declarative SQL-like query processor built entirely with advanced comprehensions:
    SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY.
    """
    def __init__(self, dataset: List[Dict[str, Any]]):
        self._dataset = dataset

    def query(
        self,
        select_fields: List[str],
        where_clause: Optional[Callable[[Dict[str, Any]], bool]] = None,
        group_by: Optional[str] = None,
        having_clause: Optional[Callable[[Dict[str, Any]], bool]] = None,
        order_by: Optional[str] = None,
        reverse: bool = False,
    ) -> List[Dict[str, Any]]:
        # 1. Filter with WHERE
        filtered = [
            row for row in self._dataset
            if where_clause is None or where_clause(row)
        ]

        # 2. GROUP BY and Aggregations if requested
        if group_by:
            groups = {row[group_by] for row in filtered}
            grouped_rows = [
                {
                    group_by: g,
                    "count": len([r for r in filtered if r[group_by] == g]),
                    "total_amount": sum(r.get("amount", 0) for r in filtered if r[group_by] == g),
                    "avg_amount": (
                        sum(r.get("amount", 0) for r in filtered if r[group_by] == g)
                        / len([r for r in filtered if r[group_by] == g])
                    ),
                }
                for g in groups
            ]
            # 3. HAVING filter on grouped results
            filtered = [
                g_row for g_row in grouped_rows
                if having_clause is None or having_clause(g_row)
            ]

        # 4. SELECT projection
        projected = [
            {field: row.get(field) for field in select_fields if field in row}
            for row in filtered
        ]

        # 5. ORDER BY sorting
        if order_by:
            projected = sorted(
                projected,
                key=lambda item: item.get(order_by, 0),
                reverse=reverse,
            )

        return projected


def test_q10_comprehension_query_engine():
    transactions = [
        {"txn_id": "T1", "category": "Electronics", "amount": 300, "status": "APPROVED"},
        {"txn_id": "T2", "category": "Books", "amount": 25, "status": "APPROVED"},
        {"txn_id": "T3", "category": "Electronics", "amount": 700, "status": "APPROVED"},
        {"txn_id": "T4", "category": "Books", "amount": 40, "status": "REJECTED"},
        {"txn_id": "T5", "category": "Clothing", "amount": 150, "status": "APPROVED"},
        {"txn_id": "T6", "category": "Books", "amount": 35, "status": "APPROVED"},
    ]

    engine = ComprehensionQueryEngine(transactions)

    # Query: SELECT category, count, total_amount
    #        WHERE status == 'APPROVED'
    #        GROUP BY category
    #        HAVING total_amount > 50
    #        ORDER BY total_amount DESC
    result = engine.query(
        select_fields=["category", "count", "total_amount"],
        where_clause=lambda r: r["status"] == "APPROVED",
        group_by="category",
        having_clause=lambda g: g["total_amount"] > 50,
        order_by="total_amount",
        reverse=True,
    )

    # Categories approved:
    # Electronics: T1 (300) + T3 (700) = 1000, count 2
    # Clothing: T5 (150) = 150, count 1
    # Books: T2 (25) + T6 (35) = 60, count 2
    assert len(result) == 3
    assert result[0] == {"category": "Electronics", "count": 2, "total_amount": 1000}
    assert result[1] == {"category": "Clothing", "count": 1, "total_amount": 150}
    assert result[2] == {"category": "Books", "count": 2, "total_amount": 60}
    print("=== Q10: Architectural Declarative In-Memory Query Engine Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_nested_list_comprehension()
    test_q2_dict_comprehensions()
    test_q3_set_comprehensions()
    test_q4_walrus_in_comprehensions()
    test_q5_matrix_algebra()
    test_q6_grouping_and_bucketing()
    test_q7_nested_generator_expressions()
    test_q8_tree_comprehension()
    test_q9_tabular_pivoting()
    test_q10_comprehension_query_engine()
    print("\nAll 10 advanced comprehension practice questions passed successfully!")
