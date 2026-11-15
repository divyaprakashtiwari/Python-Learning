"""
Phase 6 - Section I.01: Min Heap
Example 02: Floyd's Linear Time Heapify Algorithm

Demonstrating:
1. Bottom-up Floyd's Heapify converting an arbitrary array into a valid Min Heap in O(n) time.
2. Comparison with naive sequential insertions (O(n log n)).
3. Operation/swap count verification showing linear growth.
"""


def floyd_heapify(arr):
    """
    Transform array into a min heap in-place in O(n) time.
    Starts at the last non-leaf parent: (n // 2) - 1 down to 0.
    """
    n = len(arr)
    swaps = 0

    def sift_down(i):
        nonlocal swaps
        smallest = i
        while True:
            left = 2 * i + 1
            right = 2 * i + 2

            if left < n and arr[left] < arr[smallest]:
                smallest = left
            if right < n and arr[right] < arr[smallest]:
                smallest = right

            if smallest != i:
                arr[i], arr[smallest] = arr[smallest], arr[i]
                swaps += 1
                i = smallest
            else:
                break

    for i in range(n // 2 - 1, -1, -1):
        sift_down(i)

    return swaps


def naive_heap_build(arr):
    """Build heap via sequential sift-up pushes in O(n log n) time."""
    heap = []
    swaps = 0

    for val in arr:
        heap.append(val)
        i = len(heap) - 1
        while i > 0:
            parent = (i - 1) // 2
            if heap[i] < heap[parent]:
                heap[i], heap[parent] = heap[parent], heap[i]
                swaps += 1
                i = parent
            else:
                break

    return heap, swaps


def main():
    print("=" * 60)
    print("Floyd's O(n) Heapify vs Naive O(n log n) Build")
    print("=" * 60)
    raw_array = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    print("Original Array:", raw_array)

    # 1. Floyd's Build
    floyd_copy = list(raw_array)
    floyd_swaps = floyd_heapify(floyd_copy)
    print("\nFloyd Heap Array (O(n))     :", floyd_copy)
    print("Total Swaps (Floyd)         :", floyd_swaps)

    # 2. Naive Sequential Build
    naive_copy = list(raw_array)
    naive_heap, naive_swaps = naive_heap_build(naive_copy)
    print("\nNaive Heap Array (O(n log n)):", naive_heap)
    print("Total Swaps (Naive)         :", naive_swaps)

    print(f"\nEfficiency ratio (Naive / Floyd swaps): {naive_swaps / floyd_swaps:.2f}x")


if __name__ == "__main__":
    main()
