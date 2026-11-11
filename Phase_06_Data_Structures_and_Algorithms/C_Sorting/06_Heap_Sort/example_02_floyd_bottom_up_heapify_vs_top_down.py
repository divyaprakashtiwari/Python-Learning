"""
Phase 6 - Data Structures and Algorithms
Section C: Sorting - Topic 06: Heap Sort
Example 02: Why Floyd's Bottom-Up `build_heap` Is O(N) vs Top-Down `sift_up` O(N log N)

Demonstrates:
1. Top-Down Heap Construction (`sift_up` each of the N elements one by one):
   - Half of the nodes (the leaves at depth log2(N)) travel all the way up to the root,
     costing O(N log N) work in the worst case.
2. Floyd's Bottom-Up Heap Construction (`sift_down` from `n // 2 - 1` down to `0`):
   - 50% of nodes (leaves) do 0 work!
   - 25% of nodes (height 1) sift down at most 1 level.
   - 12.5% of nodes (height 2) sift down at most 2 levels.
   - Sum of (N / 2^(h+1)) * h converges to <= 2N swaps (strictly O(N) linear time!).
"""


def build_max_heap_top_down_sift_up(arr: list[int]) -> tuple[list[int], int]:
    """
    Top-down heap construction by inserting elements one by one and sifting UP.
    Worst-case swaps on an ascending array: O(N log N).
    """
    a = arr.copy()
    swaps = 0
    for i in range(1, len(a)):
        curr = i
        while curr > 0:
            parent = (curr - 1) // 2
            if a[curr] > a[parent]:
                a[curr], a[parent] = a[parent], a[curr]
                swaps += 1
                curr = parent
            else:
                break
    return a, swaps


def build_max_heap_bottom_up_floyd(arr: list[int]) -> tuple[list[int], int]:
    """
    Floyd's Bottom-Up O(N) heap construction by sifting DOWN from `n // 2 - 1` to `0`.
    Guaranteed < N swaps for any array of size N!
    """
    a = arr.copy()
    n = len(a)
    swaps = 0

    for start in range(n // 2 - 1, -1, -1):
        root = start
        while True:
            left = 2 * root + 1
            if left >= n:
                break
            right = left + 1
            largest = root
            if a[left] > a[largest]:
                largest = left
            if right < n and a[right] > a[largest]:
                largest = right
            if largest == root:
                break
            a[root], a[largest] = a[largest], a[root]
            swaps += 1
            root = largest

    return a, swaps


if __name__ == "__main__":
    print("=" * 72)
    print("1. TOP-DOWN SIFT-UP O(N log N) vs FLOYD'S BOTTOM-UP SIFT-DOWN O(N)")
    print("=" * 72)

    for size in [31, 127, 511]:
        # Ascending array is the worst case for building a Max-Heap
        ascending_data = list(range(1, size + 1))
        _, swaps_up = build_max_heap_top_down_sift_up(ascending_data)
        _, swaps_down = build_max_heap_bottom_up_floyd(ascending_data)
        print(
            f"  N = {size:>3} | Top-Down Sift-Up Swaps: {swaps_up:>4} (O(N log N)) | "
            f"Floyd Bottom-Up Swaps: {swaps_down:>3} (< N, strictly O(N)!)"
        )
