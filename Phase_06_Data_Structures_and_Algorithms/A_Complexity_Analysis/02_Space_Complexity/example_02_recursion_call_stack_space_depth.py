"""
Phase 6 - Section A (Complexity Analysis) - Topic 02: Space Complexity
Example 02: Recursion Call-Stack Space — O(n) Linear Recursion vs O(1) Iterative Loop

Demonstrates:
  - Why recursive functions without extra arrays still consume O(depth) auxiliary space
    on the Python call stack
  - Measuring peak recursion frame depth explicitly
"""


def factorial_recursive(n: int, current_depth: int = 1) -> tuple[int, int]:
    """Return `(n!, max_stack_depth_reached)` -> O(n) call-stack space."""
    if n <= 1:
        return 1, current_depth
    sub_fact, max_depth = factorial_recursive(n - 1, current_depth + 1)
    return n * sub_fact, max_depth


def factorial_iterative(n: int) -> tuple[int, int]:
    """Return `(n!, stack_frames_used)` -> O(1) auxiliary space."""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result, 1


def main() -> None:
    print("=== Comparing Call-Stack Frame Depth: Recursive O(n) vs Iterative O(1) ===")
    for n in [5, 10]:
        rec_val, rec_depth = factorial_recursive(n)
        iter_val, iter_depth = factorial_iterative(n)
        print(
            f"  n={n:>2}: value={rec_val:>7} | "
            f"Recursive stack frames={rec_depth:>2} (O(n)) | Iterative frames={iter_depth} (O(1))"
        )


if __name__ == "__main__":
    main()
