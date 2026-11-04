"""
Phase 5 - Topic 07: Closures
Example 02: Stateful Closures with `nonlocal` vs Late-Binding Loop Pitfall

Demonstrates:
  - Mutating enclosing state across calls using the `nonlocal` keyword
  - The classic late-binding closure trap in loops (`[lambda x: x + i for i in range(3)]`)
    and how to fix it with a default parameter (`i=i`)
"""

from typing import Callable


def make_moving_average() -> Callable[[float], float]:
    """Stateful closure tracking running total and count via `nonlocal`."""
    total = 0.0
    count = 0

    def add_sample(value: float) -> float:
        nonlocal total, count
        total += value
        count += 1
        return round(total / count, 2)

    return add_sample


def main() -> None:
    print("=== 1. Stateful Closure with `nonlocal` (Moving Average) ===")
    avg = make_moving_average()
    for reading in [10.0, 20.0, 45.0]:
        print(f"  Added {reading:>4.1f} -> running average = {avg(reading)}")

    print("\n=== 2. Classic Late-Binding Loop Trap vs Early-Binding Fix ===")
    # Buggy: all lambdas share the SAME cell for `i`, which ends at 2 after the loop!
    buggy_Adders = [lambda x: x + i for i in range(3)]
    # Fixed: `i=i` binds the current value of `i` as a default argument at creation time
    fixed_adders = [lambda x, i=i: x + i for i in range(3)]

    print(f"  Buggy [fn(10) for fn in buggy_Adders] : {[fn(10) for fn in buggy_Adders]} (all used i=2!)")
    print(f"  Fixed [fn(10) for fn in fixed_adders] : {[fn(10) for fn in fixed_adders]} (used i=0, 1, 2)")


if __name__ == "__main__":
    main()
