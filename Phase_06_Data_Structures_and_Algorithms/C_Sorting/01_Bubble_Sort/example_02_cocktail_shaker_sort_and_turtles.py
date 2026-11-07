"""
Phase 6 - Data Structures and Algorithms
Section C: Sorting - Topic 01: Bubble Sort
Example 02: Cocktail Shaker Sort (Bidirectional Bubble Sort) & "Turtles" Problem

Demonstrates:
1. The "Rabbits and Turtles" phenomenon in standard Bubble Sort:
   - Large elements near the front ("Rabbits", e.g., 99) bubble all the way to the right in 1 pass.
   - Small elements near the back ("Turtles", e.g., 1 at the very end) move left by only
     ONE position per pass, forcing N-1 passes even on `[2, 3, 4, 5, 6, 7, 8, 1]`!
2. Cocktail Shaker Sort (Bidirectional Bubble Sort): alternates left-to-right and
   right-to-left passes so Turtles reach the front in a single backward pass!
"""


def cocktail_shaker_sort(arr: list[int]) -> tuple[list[int], int, int]:
    """
    Bidirectional Bubble Sort (Cocktail Shaker Sort).
    Alternates forward passes (bubbling max right) and backward passes (bubbling min left).
    Returns (sorted_list, full_sweeps, comparisons).
    """
    a = arr.copy()
    start = 0
    end = len(a) - 1
    sweeps = 0
    comparisons = 0

    while start < end:
        swapped = False
        sweeps += 1

        # 1. Forward pass (left to right): bubble largest item to `end`
        for i in range(start, end):
            comparisons += 1
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True
        end -= 1

        if not swapped:
            break

        # 2. Backward pass (right to left): bubble smallest item ("turtle") to `start`
        swapped = False
        sweeps += 1
        for i in range(end, start, -1):
            comparisons += 1
            if a[i - 1] > a[i]:
                a[i - 1], a[i] = a[i], a[i - 1]
                swapped = True
        start += 1

        if not swapped:
            break

    return a, sweeps, comparisons


if __name__ == "__main__":
    from example_01_standard_vs_early_exit_bubble_sort import bubble_sort_optimized

    print("=" * 72)
    print("1. THE 'TURTLE' PROBLEM: SMALL ELEMENT AT THE END OF SORTED ARRAY")
    print("=" * 72)

    # '1' at the end is a "Turtle": standard Bubble Sort only moves it left by 1 slot per pass!
    turtle_array = [2, 3, 4, 5, 6, 7, 8, 9, 1]
    print(f"Turtle Array (n={len(turtle_array)}): {turtle_array}\n")

    res_b, passes_b, comps_b, swaps_b = bubble_sort_optimized(turtle_array)
    res_c, sweeps_c, comps_c = cocktail_shaker_sort(turtle_array)
    assert res_b == res_c

    print(
        f"Unidirectional Bubble Sort -> Passes: {passes_b} | Comparisons: {comps_b}"
    )
    print(
        f"Cocktail Shaker Sort       -> Sweeps: {sweeps_c} | Comparisons: {comps_c}"
    )
    print(f"Sorted Result              : {res_c}")
