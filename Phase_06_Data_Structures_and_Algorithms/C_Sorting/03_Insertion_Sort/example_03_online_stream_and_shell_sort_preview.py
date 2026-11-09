"""
Phase 6 - Data Structures and Algorithms
Section C: Sorting - Topic 03: Insertion Sort
Example 03: Online Stream Insertion Sort & Shell Sort (Diminishing Increment Sort)

Demonstrates:
1. Why Insertion Sort is an ONLINE algorithm: it can maintain a sorted list incrementally
   as elements arrive one by one from a real-time network stream without knowing N upfront!
2. Shell Sort (Donald Shell, 1959): generalizes Insertion Sort by pre-sorting elements separated
   by `gap` indices (`gap = n//2, n//4, ..., 1`) so elements leap across long distances before
   the final `gap = 1` standard Insertion Sort pass finishes in near-linear time!
"""


class OnlineSortedStream:
    """Maintains a live sorted buffer using online insertion as items arrive."""

    def __init__(self) -> None:
        self._buffer: list[int] = []

    def push(self, value: int) -> int:
        """Insert `value` into its sorted position and return number of shifts performed."""
        self._buffer.append(value)
        j = len(self._buffer) - 2
        shifts = 0
        while j >= 0 and self._buffer[j] > value:
            self._buffer[j + 1] = self._buffer[j]
            shifts += 1
            j -= 1
        self._buffer[j + 1] = value
        return shifts

    @property
    def items(self) -> list[int]:
        return self._buffer


def shell_sort(arr: list[int]) -> tuple[list[int], int]:
    """
    Shell Sort (Gapped Insertion Sort):
    Starts with large gaps (`n // 2`) to eliminate large numbers of inversions in a single
    move, shrinking down to `gap = 1` (standard Insertion Sort on a nearly sorted array!).
    Returns (sorted_list, total_shifts).
    """
    a = arr.copy()
    n = len(a)
    gap = n // 2
    shifts = 0

    while gap > 0:
        # Perform gapped insertion sort for this gap size
        for i in range(gap, n):
            key = a[i]
            j = i
            while j >= gap and a[j - gap] > key:
                a[j] = a[j - gap]
                shifts += 1
                j -= gap
            a[j] = key
        gap //= 2

    return a, shifts


if __name__ == "__main__":
    from example_01_shift_based_insertion_sort_and_adaptivity import insertion_sort

    print("=" * 72)
    print("1. ONLINE STREAM INSERTION SORT (REAL-TIME LEADERBOARD)")
    print("=" * 72)
    stream = OnlineSortedStream()
    incoming_scores = [450, 820, 610, 900, 520, 750]
    for score in incoming_scores:
        shifts = stream.push(score)
        print(f"  Arrived {score} ({shifts} shifts) -> Live Sorted Stream: {stream.items}")

    print("\n" + "=" * 72)
    print("2. SHELL SORT (GAPPED INSERTION SORT) vs STANDARD INSERTION SORT")
    print("=" * 72)
    reverse_16 = list(range(160, 0, -10))
    _, _, ins_shifts = insertion_sort(reverse_16)
    shell_out, sh_shifts = shell_sort(reverse_16)
    assert shell_out == sorted(reverse_16)
    print(f"Reverse-Sorted Array (N=16): {reverse_16}")
    print(f"  Standard Insertion Sort Shifts : {ins_shifts}")
    print(f"  Shell Sort (Gapped) Shifts     : {sh_shifts} (nearly 4x fewer moves!)")

