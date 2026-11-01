"""
Topic 06: Input and Output
Example 01: Mastering `print()` Parameters (`sep`, `end`) and f-String Formatting

Demonstrates custom separators, custom line endings, f-string self-documenting
expressions (`f"{var=}"`), decimal precision, and thousand separators.
"""


def main() -> None:
    # 1. Custom `sep` and `end` in print()
    print("=== 1. Custom sep and end in print() ===")
    print("2026", "11", "01", sep="-")
    print(" Phase_01", "06_Input_and_Output", "notes.md", sep="/")
    print("Loading modules", end="... ")
    print("Done!")

    # 2. f-String number formatting and debugging syntax (var=)
    population = 1_428_627_663
    accuracy = 0.987654
    items = 12
    unit_cost = 250

    print("\n=== 2. Modern f-String Formatting ===")
    print(f"Formatted Population : {population:,}")
    print(f"Accuracy (2 decimals): {accuracy:.2f}")
    print(f"Accuracy (percentage): {accuracy:.2%}")
    print(f"Debug Expression     : {items=}, {unit_cost=}, {items * unit_cost=}")


if __name__ == "__main__":
    main()
