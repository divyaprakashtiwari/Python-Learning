"""
Topic 03: Tuples
Example 01: Tuple Creation, Single-Element Trailing Comma, and Extended Unpacking

Demonstrates how to create tuples, why `(42,)` requires a trailing comma,
extended star unpacking (`first, *middle, last`), and returning multiple values.
"""


def compute_min_max_avg(numbers: list[float]) -> tuple[float, float, float]:
    """Return (minimum, maximum, average) packaged as a 3-element tuple."""
    return (min(numbers), max(numbers), sum(numbers) / len(numbers))


def main() -> None:
    print("=== 1. Single-Element Tuple vs Parenthesized Integer ===")
    not_a_tuple = (42)
    single_tuple = (42,)
    print(f"(42)  -> value={not_a_tuple}, type={type(not_a_tuple).__name__}")
    print(f"(42,) -> value={single_tuple}, type={type(single_tuple).__name__}")

    print("\n=== 2. Extended Iterable Unpacking (first, *middle, last) ===")
    lap_times = (58.2, 57.9, 59.1, 58.4, 56.8)
    opening_lap, *middle_laps, final_lap = lap_times
    print(f"Opening Lap : {opening_lap}s")
    print(f"Middle Laps : {middle_laps}")
    print(f"Final Lap   : {final_lap}s")

    print("\n=== 3. Unpacking Multi-Value Function Return ===")
    lowest, highest, mean = compute_min_max_avg([82.0, 91.5, 76.0, 94.5])
    print(f"Min: {lowest:.1f} | Max: {highest:.1f} | Avg: {mean:.2f}")


if __name__ == "__main__":
    main()
