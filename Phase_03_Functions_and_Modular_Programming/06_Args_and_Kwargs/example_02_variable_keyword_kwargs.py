"""
Phase 3 - Topic 06: *args and **kwargs
Example 02: Variable Keyword Arguments (`**kwargs` Dict Packing) & Canonical Order

Demonstrates:
  - How `**kwargs` collects arbitrary keyword arguments into a `dict[str, Any]`
  - The strict 5-part parameter ordering rule in Python function signatures:
    (1) positional-only `/` -> (2) standard -> (3) `*args` -> (4) keyword-only -> (5) `**kwargs`
"""


def build_sql_insert(
    table_name: str,
    /,
    *tags: str,
    ignore_duplicates: bool = False,
    **columns: object,
) -> str:
    """
    Demonstrate all 5 parameter categories in a single signature:
      1. `table_name`        : Positional-only (before `/`)
      2. `*tags`             : Variable positional tuple
      3. `ignore_duplicates` : Keyword-only with default (after `*tags`)
      4. `**columns`         : Variable keyword dictionary
    """
    verb = "INSERT OR IGNORE INTO" if ignore_duplicates else "INSERT INTO"
    col_names = ", ".join(columns.keys())
    col_vals = ", ".join(repr(v) for v in columns.values())
    comment = f"/* tags: {', '.join(tags)} */ " if tags else ""
    return f"{comment}{verb} {table_name} ({col_names}) VALUES ({col_vals});"


def main() -> None:
    print("=== 1. Inspecting `**columns` Packing & Full Signature Order ===")
    query_1 = build_sql_insert(
        "users",
        "audit",
        "v2",
        ignore_duplicates=True,
        id=101,
        username="aarav_dev",
        active=True,
    )
    print(f"  Generated SQL 1 :\n    {query_1}")

    query_2 = build_sql_insert(
        "products",
        sku="LAP-900",
        price=74999.50,
        in_stock=15,
    )
    print(f"  Generated SQL 2 :\n    {query_2}")


if __name__ == "__main__":
    main()
