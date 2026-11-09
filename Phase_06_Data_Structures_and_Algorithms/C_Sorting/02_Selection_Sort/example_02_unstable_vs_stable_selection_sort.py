"""
Phase 6 - Data Structures and Algorithms
Section C: Sorting - Topic 02: Selection Sort
Example 02: Why Standard Selection Sort Is Unstable & How Stable Selection Sort Works

Demonstrates:
1. Concrete proof of why standard Swap-Based Selection Sort is UNSTABLE:
   In `[4_A, 4_B, 1]`, selecting the minimum (`1`) and swapping it with index 0 (`4_A`)
   teleports `4_A` to the end (`[1, 4_B, 4_A]`), reversing the relative order of `4_A` and `4_B`!
2. Stable Selection Sort: instead of swapping `a[i]` and `a[min_idx]` across a long distance,
   extract `a[min_idx]` and shift `a[i .. min_idx - 1]` right by 1 position!
"""


def unstable_selection_sort_tagged(
    items: list[tuple[int, str]]
) -> list[tuple[int, str]]:
    """Standard swap-based Selection Sort comparing only the numeric key `item[0]`."""
    a = items.copy()
    n = len(a)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if a[j][0] < a[min_idx][0]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
    return a


def stable_selection_sort_tagged(
    items: list[tuple[int, str]]
) -> list[tuple[int, str]]:
    """
    Stable Selection Sort:
    Instead of a long-distance swap between `a[i]` and `a[min_idx]`, saves `key_item = a[min_idx]`
    and shifts `a[i .. min_idx - 1]` one slot to the right before placing `key_item` at `a[i]`.
    """
    a = items.copy()
    n = len(a)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if a[j][0] < a[min_idx][0]:
                min_idx = j

        # Shift elements [i .. min_idx - 1] right by 1 instead of swapping!
        min_item = a[min_idx]
        while min_idx > i:
            a[min_idx] = a[min_idx - 1]
            min_idx -= 1
        a[i] = min_item

    return a


if __name__ == "__main__":
    print("=" * 72)
    print("1. WHY STANDARD SELECTION SORT IS UNSTABLE (LONG-DISTANCE SWAP)")
    print("=" * 72)

    # Two equal keys '4' tagged as (4, 'First_4') and (4, 'Second_4'), followed by (1, 'Min_1')
    tagged_records = [(4, "First_4"), (4, "Second_4"), (1, "Min_1"), (5, "Five")]
    print(f"Original Input            : {tagged_records}\n")

    unstable_res = unstable_selection_sort_tagged(tagged_records)
    stable_res = stable_selection_sort_tagged(tagged_records)

    print(f"Standard (Swap) Selection : {unstable_res}")
    print("  -> Notice (4, 'Second_4') now appears BEFORE (4, 'First_4')! (UNSTABLE)\n")

    print(f"Stable (Shift) Selection  : {stable_res}")
    print("  -> Notice (4, 'First_4') remains BEFORE (4, 'Second_4')! (STABLE)")
