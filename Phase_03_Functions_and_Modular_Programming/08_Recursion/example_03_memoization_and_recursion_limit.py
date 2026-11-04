"""
Phase 3 - Topic 08: Recursion
Example 03: Tree Recursion, Memoization (`@lru_cache`), and `RecursionError`

Demonstrates:
  - Why naive tree recursion (`fib_naive`) explodes in O(2^n) calls
  - How `@functools.lru_cache` turns O(2^n) recursion into O(n) via memoization
  - Solving the classic Tower of Hanoi puzzle recursively
  - Inspecting `sys.getrecursionlimit()` and catching `RecursionError`
"""

from functools import lru_cache
import sys

naive_call_count = 0
memo_call_count = 0


def fib_naive(n: int) -> int:
    """O(2^n) naive tree recursion - recomputes overlapping subproblems."""
    global naive_call_count
    naive_call_count += 1
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


@lru_cache(maxsize=None)
def fib_memoized(n: int) -> int:
    """O(n) memoized recursion - each state `n` is computed only ONCE."""
    global memo_call_count
    memo_call_count += 1
    if n <= 1:
        return n
    return fib_memoized(n - 1) + fib_memoized(n - 2)


def tower_of_hanoi(
    n_disks: int,
    source: str,
    auxiliary: str,
    target: str,
    moves: list[str],
) -> None:
    """Record the sequence of moves to transfer `n_disks` from `source` to `target`."""
    if n_disks == 1:
        moves.append(f"Disk 1: {source} -> {target}")
        return
    tower_of_hanoi(n_disks - 1, source, target, auxiliary, moves)
    moves.append(f"Disk {n_disks}: {source} -> {target}")
    tower_of_hanoi(n_disks - 1, auxiliary, source, target, moves)


def main() -> None:
    print("=== 1. Naive O(2^n) vs Memoized O(n) Fibonacci (n=20) ===")
    ans_naive = fib_naive(20)
    ans_memo = fib_memoized(20)
    print(f"  fib(20) = {ans_naive} (matches memoized: {ans_naive == ans_memo})")
    print(f"  Naive recursive calls made    : {naive_call_count:,}")
    print(f"  Memoized recursive calls made : {memo_call_count:,}")

    print("\n=== 2. Tower of Hanoi (3 Disks) ===")
    hanoi_moves: list[str] = []
    tower_of_hanoi(3, "A", "B", "C", hanoi_moves)
    for step_no, move in enumerate(hanoi_moves, start=1):
        print(f"  Step {step_no}: {move}")

    print("\n=== 3. Recursion Depth Limit & `RecursionError` ===")
    print(f"  Default sys.getrecursionlimit() = {sys.getrecursionlimit()}")

    def infinite_recurse(x: int) -> int:
        return infinite_recurse(x + 1)

    try:
        infinite_recurse(0)
    except RecursionError as err:
        print(f"  Caught expected RecursionError  : {err}")


if __name__ == "__main__":
    main()
