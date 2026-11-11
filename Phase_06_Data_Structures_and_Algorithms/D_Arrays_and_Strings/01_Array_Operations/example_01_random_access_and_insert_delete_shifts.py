"""
Phase 6 - Data Structures and Algorithms
Section D: Arrays and Strings - Topic 01: Array Operations
Example 01: Contiguous Memory Layout, O(1) Random Access, and Insert/Delete Shifting Costs

Demonstrates:
1. Why contiguous arrays provide O(1) random index access (`base_address + index * item_size`).
2. Why inserting or deleting at the END (`append` / `pop()`) is O(1) amortized, whereas
   inserting or deleting at the FRONT or MIDDLE (`insert(i, x)` / `pop(i)`) requires
   shifting `N - i` elements in O(N) time!
3. Manual implementation of in-place deletion and insertion with explicit shift counting.
"""


def insert_at_index_with_shift_count(
    arr: list[int], index: int, value: int
) -> tuple[list[int], int]:
    """
    Insert `value` at `index` by appending a dummy slot and shifting elements
    `[index .. n - 1]` one position to the right.
    Returns (modified_copy, elements_shifted).
    Time Complexity: O(N - index) -> O(N) worst case at index 0, O(1) at index N.
    """
    a = arr.copy()
    n = len(a)
    if not (0 <= index <= n):
        raise IndexError("Insertion index out of bounds")

    a.append(0)  # Expand capacity by 1 slot at the tail
    shifts = 0

    for j in range(n - 1, index - 1, -1):
        a[j + 1] = a[j]
        shifts += 1

    a[index] = value
    return a, shifts


def delete_at_index_with_shift_count(
    arr: list[int], index: int
) -> tuple[list[int], int, int]:
    """
    Delete element at `index` by shifting elements `[index + 1 .. n - 1]` one position
    to the left and popping the duplicate tail slot.
    Returns (modified_copy, removed_value, elements_shifted).
    Time Complexity: O(N - 1 - index) -> O(N) worst case at index 0, O(1) at index N - 1.
    """
    a = arr.copy()
    n = len(a)
    if not (0 <= index < n):
        raise IndexError("Deletion index out of bounds")

    removed = a[index]
    shifts = 0

    for j in range(index, n - 1):
        a[j] = a[j + 1]
        shifts += 1

    a.pop()
    return a, removed, shifts


if __name__ == "__main__":
    print("=" * 72)
    print("1. ARRAY INSERTION SHIFT COST BY POSITION (N = 8)")
    print("=" * 72)
    base_arr = [10, 20, 30, 40, 50, 60, 70, 80]
    print(f"Original Array (N={len(base_arr)}): {base_arr}\n")

    for pos, label in [(0, "Front (Worst Case)"), (4, "Middle (Index 4)"), (8, "End / Append (Best Case)")]:
        new_arr, shifts = insert_at_index_with_shift_count(base_arr, pos, 99)
        print(f"  Insert 99 at idx {pos} ({label:<24}) -> Shifts: {shifts} | Result: {new_arr}")

    print("\n" + "=" * 72)
    print("2. ARRAY DELETION SHIFT COST BY POSITION (N = 8)")
    print("=" * 72)
    for pos, label in [(0, "Front pop(0) (Worst)"), (3, "Middle pop(3)"), (7, "Tail pop() (Best)")]:
        new_arr, rem, shifts = delete_at_index_with_shift_count(base_arr, pos)
        print(f"  Delete at idx {pos} ({label:<22}) -> Removed {rem}, Shifts: {shifts} | Result: {new_arr}")
