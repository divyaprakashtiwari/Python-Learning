"""
Phase 3 - Topic 03: Return Statements
Example 02: Returning Multiple Values (Tuple Packing, Unpacking & NamedTuple)

Demonstrates:
  - How `return a, b, c` packs values into a single `tuple` object
  - Destructuring/unpacking multiple returned values at the call site
  - Returning a `typing.NamedTuple` for self-documenting multi-value returns
"""

from typing import NamedTuple


class DescriptiveStats(NamedTuple):
    """Self-documenting container for summary statistics."""

    minimum: float
    maximum: float
    mean: float
    count: int


def divmod_with_status(dividend: int, divisor: int) -> tuple[bool, int, int]:
    """Return (is_valid, quotient, remainder) as a packed 3-tuple."""
    if divisor == 0:
        return False, 0, 0
    return True, dividend // divisor, dividend % divisor


def compute_stats(values: list[float]) -> DescriptiveStats:
    """Return multiple named statistics that support both indexing and `.attribute` access."""
    if not values:
        return DescriptiveStats(0.0, 0.0, 0.0, 0)
    return DescriptiveStats(
        minimum=min(values),
        maximum=max(values),
        mean=round(sum(values) / len(values), 2),
        count=len(values),
    )


def main() -> None:
    print("=== 1. Returning Multiple Values via Tuple Packing ===")
    raw_return = divmod_with_status(29, 5)
    print(f"  Raw return object : {raw_return} (type: {type(raw_return).__name__})")

    # Unpacking directly into 3 variables
    ok, quotient, remainder = divmod_with_status(29, 5)
    print(f"  Unpacked values   : ok={ok}, quotient={quotient}, remainder={remainder}")

    ok_zero, _, _ = divmod_with_status(29, 0)
    print(f"  Divide by zero    : ok={ok_zero}")

    print("\n=== 2. Returning `NamedTuple` for Readable Multi-Value Returns ===")
    latencies_ms = [12.4, 18.9, 9.2, 24.5, 15.0]
    stats = compute_stats(latencies_ms)
    print(f"  NamedTuple repr   : {stats}")
    print(f"  Attribute access  : min={stats.minimum}ms, max={stats.maximum}ms, mean={stats.mean}ms")

    # Still supports tuple unpacking!
    lo, hi, avg, n = stats
    print(f"  Tuple unpacking   : lo={lo}, hi={hi}, avg={avg}, n={n}")


if __name__ == "__main__":
    main()
