"""
Topic 04 - Functions: Question 3
Problem: Dynamic SQL Query String Builder using *args, **kwargs, and argument unpacking.
"""

from typing import Tuple, Any


def build_select_query(
    table_name: str,
    *columns: str,
    distinct: bool = False,
    **where_clauses: Any
) -> Tuple[str, Tuple[Any, ...]]:
    """Builds parameterized SELECT SQL statement and parameter tuple safely."""
    col_str = ", ".join(columns) if columns else "*"
    dist_prefix = "DISTINCT " if distinct else ""

    where_str = ""
    params: Tuple[Any, ...] = ()
    if where_clauses:
        where_parts = [f"{k} = ?" for k in where_clauses.keys()]
        where_str = " WHERE " + " AND ".join(where_parts)
        params = tuple(where_clauses.values())

    sql = f"SELECT {dist_prefix}{col_str} FROM {table_name}{where_str};"
    return sql, params


# Call 1: Default all columns, no filters
q1_sql, q1_params = build_select_query("users")
print("Query 1:")
print(f'SQL: "{q1_sql}"')
print(f"Params: {q1_params}")

# Call 2: Explicit columns, DISTINCT flag, and keyword criteria
q2_sql, q2_params = build_select_query(
    "orders",
    "order_id",
    "total_price",
    distinct=True,
    customer_id=42,
    status="SHIPPED"
)
print("\nQuery 2:")
print(f'SQL: "{q2_sql}"')
print(f"Params: {q2_params}")

# Call 3: Call-site unpacking with *list and **dict
cols = ["first_name", "last_name", "department"]
filters = {"active": True, "location": "NYC"}
q3_sql, q3_params = build_select_query("employees", *cols, **filters)
print("\nQuery 3 (Unpacked):")
print(f'SQL: "{q3_sql}"')
print(f"Params: {q3_params}")
