"""
Phase 5 - Topic 01: Exception Handling
Example 01: The Complete `try / except / else / finally` Execution Lifecycle

Demonstrates:
  - Catching specific exceptions (`ValueError`, `ZeroDivisionError`) instead of bare `except:`
  - Why code that should only run when `try` succeeds belongs in `else:` (not inside `try:`)
  - Why cleanup logic belongs in `finally:` (runs whether an exception occurred or not)
"""


def parse_and_divide(raw_numerator: str, raw_denominator: str) -> float | None:
    """Parse two strings as floats and return their quotient, tracing all 4 blocks."""
    print(f"  --- Input: ({raw_numerator!r}, {raw_denominator!r}) ---")
    try:
        numerator = float(raw_numerator)
        denominator = float(raw_denominator)
        quotient = numerator / denominator
    except ValueError as err:
        print(f"    [except ValueError] Invalid number format: {err}")
        return None
    except ZeroDivisionError:
        print("    [except ZeroDivisionError] Denominator cannot be zero!")
        return None
    else:
        # Runs ONLY if the `try` block completed with ZERO exceptions
        rounded = round(quotient, 4)
        print(f"    [else] Division succeeded cleanly -> {rounded}")
        return rounded
    finally:
        # Runs ALWAYS (even when `except` or `else` executes a `return` statement!)
        print("    [finally] Releasing parser resources")


def main() -> None:
    print("=== Tracing `try / except / else / finally` Across 3 Scenarios ===")
    parse_and_divide("45", "6")
    parse_and_divide("forty-five", "6")
    parse_and_divide("45", "0")


if __name__ == "__main__":
    main()
