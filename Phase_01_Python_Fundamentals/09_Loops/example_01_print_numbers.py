"""
Topic 09: Loops (for, while)
Example 01: Printing Number Sequences with `for`, `range()`, and `enumerate()`

Demonstrates how `range(start, stop, step)` generates lazy integer sequences
for forward counting, even numbers, reverse countdowns, and indexed iteration.
"""


def main() -> None:
    # 1. Basic range(start, stop) -> stop is exclusive
    print("=== 1. Numbers 1 to 10 using range(1, 11) ===")
    for num in range(1, 11):
        print(num, end=" ")
    print()

    # 2. Stepping by 2: Even numbers from 2 to 20
    print("\n=== 2. Even Numbers 2 to 20 using range(2, 21, 2) ===")
    evens = [n for n in range(2, 21, 2)]
    print(evens)

    # 3. Reverse countdown using a negative step: range(5, 0, -1)
    print("\n=== 3. Countdown using range(5, 0, -1) ===")
    for sec in range(5, 0, -1):
        print(f"T-minus {sec}...", end=" ")
    print("Liftoff!")

    # 4. Iterating over a sequence with enumerate(seq, start=1)
    print("\n=== 4. Indexed Iteration with enumerate() ===")
    milestones = ["Variables", "Data Types", "Conditionals", "Loops"]
    for step_no, topic in enumerate(milestones, start=1):
        print(f"  Milestone #{step_no}: {topic}")


if __name__ == "__main__":
    main()
