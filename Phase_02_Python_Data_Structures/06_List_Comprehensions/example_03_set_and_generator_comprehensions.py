"""
Topic 06: List Comprehensions
Example 03: List Comprehension `[...]` vs Set Comprehension `{...}` vs Generator `(...)`

Demonstrates when to use a Set Comprehension for automatic deduplication and when
to use a lazy Generator Expression inside `sum()`, `any()`, or `all()` for O(1) memory.
"""

import sys


def main() -> None:
    words = ["apple", "Banana", "APPLE", "cherry", "banana", "Date"]

    # 1. List Comprehension vs Set Comprehension
    lower_list = [w.lower() for w in words]
    unique_lower_set = {w.lower() for w in words}
    print("=== 1. List Comprehension vs Set Comprehension ===")
    print(f"List Comprehension (keeps duplicates) : {lower_list}")
    print(f"Set Comprehension (unique sorted)     : {sorted(unique_lower_set)}")

    # 2. Memory comparison: List Comprehension vs Generator Expression
    list_comp = [x * x for x in range(10_000)]
    gen_expr = (x * x for x in range(10_000))

    print("\n=== 2. Memory Efficiency: [List Comp] vs (Generator Expr) ===")
    print(f"List Comprehension size (10,000 items): {sys.getsizeof(list_comp)} bytes")
    print(f"Generator Expression size (lazy O(1)) : {sys.getsizeof(gen_expr)} bytes")
    print(f"Sum via Generator Expression          : {sum(x * x for x in range(1, 6))}")


if __name__ == "__main__":
    main()
