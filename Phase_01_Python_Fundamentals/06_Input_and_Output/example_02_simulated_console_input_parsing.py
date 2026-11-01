"""
Topic 06: Input and Output
Example 02: Reading Single and Space-Separated Inputs (`input()`, `split()`, `map()`)

Demonstrates how `input()` reads lines from standard input (`sys.stdin`), and how
competitive programmers parse space-separated integers on a single line.
Uses `io.StringIO` so this script executes deterministically without hanging for keyboard input.
"""

import io
import sys


def process_student_inputs() -> None:
    # 1. Read a single string line
    full_name = input().strip()

    # 2. Read two space-separated integers: age andgraduation_year
    age, grad_year = map(int, input().split())

    # 3. Read a list of space-separated test scores on a single line
    scores = list(map(float, input().split()))
    avg_score = sum(scores) / len(scores)

    print("=== Parsed Standard Input Summary ===")
    print(f"Student Name    : {full_name}")
    print(f"Age & Grad Year : {age} years old | Class of {grad_year}")
    print(f"Scores          : {scores}")
    print(f"Average Score   : {avg_score:.2f}")


def main() -> None:
    simulated_stdin = "Divya Prakash Tiwari\n21 2027\n88.5 92.0 95.5 89.0\n"
    original_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(simulated_stdin)
        process_student_inputs()
    finally:
        sys.stdin = original_stdin


if __name__ == "__main__":
    main()
