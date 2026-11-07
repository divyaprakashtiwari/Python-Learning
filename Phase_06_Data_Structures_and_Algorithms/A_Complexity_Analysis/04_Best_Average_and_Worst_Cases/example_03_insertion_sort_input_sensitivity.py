"""
Phase 6 - Section A (Complexity Analysis) - Topic 04: Best, Average and Worst Cases
Example 03: Input-Distribution Sensitivity — Insertion Sort Best Case O(n) vs Worst Case O(n^2)

Demonstrates:
  - How the exact same algorithm runs in O(n) on already-sorted input (Best Case)
    and O(n^2) on reverse-sorted input (Worst Case)
"""


def insertion_sort_shift_count(arr: list[int]) -> int:
    """Sort `arr` copy via Insertion Sort and return total inner-loop element shifts."""
    a = list(arr)
    shifts = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            shifts += 1
            j -= 1
        a[j + 1] = key
    return shifts


def main() -> None:
    n = 20
    already_sorted = list(range(n))
    reverse_sorted = list(range(n - 1, -1, -1))

    best_shifts = insertion_sort_shift_count(already_sorted)
    worst_shifts = insertion_sort_shift_count(reverse_sorted)
    theoretical_worst = (n * (n - 1)) // 2

    print(f"=== Insertion Sort Shift Counts (N = {n}) ===")
    print(f"  Best Case  (already sorted) : {best_shifts:>3} shifts (O(n) total comparisons, 0 shifts)")
    print(f"  Worst Case (reverse sorted) : {worst_shifts:>3} shifts (matches n*(n-1)/2 = {theoretical_worst} -> O(n^2))")


if __name__ == "__main__":
    main()
