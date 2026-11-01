"""
Topic 07: Operators
Example 02: Chained Comparisons and Logical Short-Circuit Evaluation

Demonstrates Python's mathematical chained comparison syntax (`low <= x <= high`),
short-circuit guard expressions (`den != 0 and num / den > 2`), and fallback defaults.
"""


def is_safe_ratio(numerator: int, denominator: int) -> bool:
    """Safely check if numerator / denominator >= 2 without ZeroDivisionError."""
    # Because `and` short-circuits, `numerator / denominator` is NEVER evaluated when denominator == 0
    return denominator != 0 and (numerator / denominator) >= 2.0


def main() -> None:
    print("=== 1. Mathematical Chained Comparisons ===")
    for exam_score in [45, 78, 95]:
        is_distinction = 75 <= exam_score <= 100
        print(f"Score {exam_score}: 75 <= score <= 100 -> {is_distinction}")

    print("\n=== 2. Short-Circuit Evaluation Guard ===")
    print(f"is_safe_ratio(10, 2) : {is_safe_ratio(10, 2)}")
    print(f"is_safe_ratio(10, 0) : {is_safe_ratio(10, 0)} (No ZeroDivisionError!)")

    print("\n=== 3. Value Return Behavior of `or` and `and` ===")
    configured_host = ""
    effective_host = configured_host or "localhost"
    print(f"Fallback host via `or`: {effective_host!r}")


if __name__ == "__main__":
    main()
