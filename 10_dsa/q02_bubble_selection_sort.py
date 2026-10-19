"""
Topic: Data Structures and Algorithms (DSA) - Bubble Sort and Selection Sort
----------------------------------------------------------------------------
Questions Covered:
1. Optimized Bubble Sort: Early termination with swapped flag achieving O(n) best-case time.
2. Selection Sort: Minimum index selection with comparison and swap metrics tracking.
3. Stability Analysis: Proving Bubble Sort stability vs Selection Sort instability with keyed records.
4. Bidirectional Bubble Sort (Cocktail Shaker Sort): Dual-direction passes eliminating "turtles".
5. Stable Selection Sort: Shifting instead of swapping to preserve relative order of duplicates.
6. Generic Key and Reverse Sorting: Higher-order sorting with custom key extraction and reverse order.
7. K-Pass Bubble Sort for K-Largest Elements: Efficient partial sorting in O(k * n) time.
8. Recursive Bubble and Selection Sorts: Pure recursive formulation without iterative loops.
9. Inversion Counting via Bubble Swaps: Tracking inversion pairs through adjacent swap counts.
10. Architectural System: Multi-Metric Product Ranking Engine with tie-breaking and telemetry.
"""

from typing import List, Tuple, Any, Callable, Optional, Dict


# ==============================================================================
# Question 1: Optimized Bubble Sort (Early Exit Flag)
# ==============================================================================
def bubble_sort_optimized(arr: List[int]) -> Tuple[List[int], int, int]:
    """
    Sorts a copy of arr using bubble sort with an early termination flag.
    Returns (sorted_arr, comparisons, swaps).
    Best-case: O(n) when already sorted. Worst-case: O(n^2).
    """
    res = list(arr)
    n = len(res)
    comparisons = 0
    swaps = 0

    for i in range(n):
        swapped = False
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            comparisons += 1
            if res[j] > res[j + 1]:
                res[j], res[j + 1] = res[j + 1], res[j]
                swaps += 1
                swapped = True
        if not swapped:
            break

    return res, comparisons, swaps


def test_q1_bubble_sort_optimized():
    nums = [64, 34, 25, 12, 22, 11, 90]
    sorted_arr, comps, swaps = bubble_sort_optimized(nums)
    assert sorted_arr == [11, 12, 22, 25, 34, 64, 90]
    assert swaps > 0

    # Best-case sorted array: exactly n - 1 comparisons, 0 swaps, 1 pass
    already_sorted = [1, 2, 3, 4, 5]
    res_sorted, comps_sorted, swaps_sorted = bubble_sort_optimized(already_sorted)
    assert res_sorted == [1, 2, 3, 4, 5]
    assert comps_sorted == 4  # 5 - 1
    assert swaps_sorted == 0
    print("=== Q1: Optimized Bubble Sort Verified ===")


# ==============================================================================
# Question 2: Selection Sort with Telemetry Tracking
# ==============================================================================
def selection_sort(arr: List[int]) -> Tuple[List[int], int, int]:
    """
    Sorts a copy of arr using selection sort.
    Returns (sorted_arr, comparisons, swaps).
    Comparisons are always n*(n-1)/2, swaps are at most n-1.
    """
    res = list(arr)
    n = len(res)
    comparisons = 0
    swaps = 0

    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if res[j] < res[min_idx]:
                min_idx = j

        if min_idx != i:
            res[i], res[min_idx] = res[min_idx], res[i]
            swaps += 1

    return res, comparisons, swaps


def test_q2_selection_sort():
    nums = [29, 10, 14, 37, 13]
    sorted_arr, comps, swaps = selection_sort(nums)
    assert sorted_arr == [10, 13, 14, 29, 37]
    # For n=5: comps = 4 + 3 + 2 + 1 = 10
    assert comps == 10
    assert swaps <= 4
    print("=== Q2: Selection Sort with Telemetry Tracking Verified ===")


# ==============================================================================
# Question 3: Stability Analysis: Bubble Sort vs Standard Selection Sort
# ==============================================================================
def bubble_sort_keyed(records: List[Tuple[int, str]]) -> List[Tuple[int, str]]:
    """Stable bubble sort on (key, id) tuples."""
    res = list(records)
    n = len(res)
    for i in range(n):
        for j in range(0, n - i - 1):
            if res[j][0] > res[j + 1][0]:
                res[j], res[j + 1] = res[j + 1], res[j]
    return res


def selection_sort_keyed_unstable(records: List[Tuple[int, str]]) -> List[Tuple[int, str]]:
    """Standard selection sort: UNSTABLE because long-distance swaps jump equal elements."""
    res = list(records)
    n = len(res)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if res[j][0] < res[min_idx][0]:
                min_idx = j
        if min_idx != i:
            res[i], res[min_idx] = res[min_idx], res[i]
    return res


def test_q3_stability_analysis():
    # Input with equal keys: 4a, 5, 4b, 3
    # 4a appears before 4b initially
    items = [(4, "a"), (5, "first"), (4, "b"), (3, "solo")]

    # Bubble sort preserves relative order of 4a and 4b
    bubble_sorted = bubble_sort_keyed(items)
    assert bubble_sorted == [(3, "solo"), (4, "a"), (4, "b"), (5, "first")]

    # Standard Selection sort swaps index 0 (4a) with index 3 (3), inverting order of 4a and 4b!
    selection_sorted = selection_sort_keyed_unstable(items)
    assert selection_sorted == [(3, "solo"), (4, "b"), (4, "a"), (5, "first")]
    print("=== Q3: Stability Analysis (Bubble Stable vs Selection Unstable) Verified ===")


# ==============================================================================
# Question 4: Bidirectional Bubble Sort (Cocktail Shaker Sort)
# ==============================================================================
def cocktail_shaker_sort(arr: List[int]) -> Tuple[List[int], int]:
    """
    Alternating forward and backward passes.
    Handles small elements at end ("turtles") much faster than standard bubble sort.
    Returns (sorted_arr, total_passes).
    """
    res = list(arr)
    n = len(res)
    start = 0
    end = n - 1
    swapped = True
    passes = 0

    while swapped:
        swapped = False
        passes += 1

        # Forward pass: moves largest to end
        for i in range(start, end):
            if res[i] > res[i + 1]:
                res[i], res[i + 1] = res[i + 1], res[i]
                swapped = True
        end -= 1

        if not swapped:
            break

        swapped = False
        # Backward pass: moves smallest to start
        for i in range(end - 1, start - 1, -1):
            if res[i] > res[i + 1]:
                res[i], res[i + 1] = res[i + 1], res[i]
                swapped = True
        start += 1

    return res, passes


def test_q4_cocktail_shaker_sort():
    nums = [5, 1, 4, 2, 8, 0, 2]
    sorted_arr, passes = cocktail_shaker_sort(nums)
    assert sorted_arr == [0, 1, 2, 2, 4, 5, 8]
    assert passes > 0

    turtle_arr = [2, 3, 4, 5, 6, 1]  # 1 is a turtle at the end
    sorted_turtle, passes_turtle = cocktail_shaker_sort(turtle_arr)
    assert sorted_turtle == [1, 2, 3, 4, 5, 6]
    # Shaker sort moves 1 to front on the very first backward pass!
    assert passes_turtle == 2
    print("=== Q4: Bidirectional Bubble Sort (Cocktail Shaker Sort) Verified ===")


# ==============================================================================
# Question 5: Stable Selection Sort (Element Shifting)
# ==============================================================================
def stable_selection_sort(records: List[Tuple[int, str]]) -> List[Tuple[int, str]]:
    """
    Selection sort made stable by shifting intermediate elements right
    and placing min element into index i instead of swapping.
    """
    res = list(records)
    n = len(res)

    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if res[j][0] < res[min_idx][0]:
                min_idx = j

        # Shift elements right between i and min_idx
        min_elem = res[min_idx]
        for k in range(min_idx, i, -1):
            res[k] = res[k - 1]
        res[i] = min_elem

    return res


def test_q5_stable_selection_sort():
    items = [(4, "a"), (5, "first"), (4, "b"), (3, "solo")]
    sorted_items = stable_selection_sort(items)
    # 4a must precede 4b
    assert sorted_items == [(3, "solo"), (4, "a"), (4, "b"), (5, "first")]
    print("=== Q5: Stable Selection Sort (Shift Instead of Swap) Verified ===")


# ==============================================================================
# Question 6: Generic Key and Reverse Sorting
# ==============================================================================
def bubble_sort_generic(
    arr: List[Any],
    *,
    key: Optional[Callable[[Any], Any]] = None,
    reverse: bool = False,
) -> List[Any]:
    """Bubble sort supporting arbitrary key extractor and reverse order."""
    res = list(arr)
    n = len(res)
    key_fn = key if key is not None else lambda x: x

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            val_a = key_fn(res[j])
            val_b = key_fn(res[j + 1])
            should_swap = (val_a < val_b) if reverse else (val_a > val_b)
            if should_swap:
                res[j], res[j + 1] = res[j + 1], res[j]
                swapped = True
        if not swapped:
            break

    return res


def test_q6_generic_sorting():
    words = ["banana", "pie", "apple", "kiwi", "elderberry"]
    # Sort by length ascending
    by_len = bubble_sort_generic(words, key=len)
    assert by_len == ["pie", "kiwi", "apple", "banana", "elderberry"]

    # Sort descending
    by_len_desc = bubble_sort_generic(words, key=len, reverse=True)
    assert by_len_desc == ["elderberry", "banana", "apple", "kiwi", "pie"]
    print("=== Q6: Generic Key and Reverse Sorting Verified ===")


# ==============================================================================
# Question 7: Partial Passes / K-Largest Elements in O(k * n)
# ==============================================================================
def find_k_largest_bubble(arr: List[int], k: int) -> List[int]:
    """
    Runs exactly k outer passes of Bubble Sort.
    After k passes, the last k elements are guaranteed to be the k largest in sorted order.
    Returns the k largest elements in ascending order in O(k * n) time without full sorting.
    """
    if k <= 0:
        return []
    if k > len(arr):
        k = len(arr)

    res = list(arr)
    n = len(res)

    for i in range(k):
        for j in range(0, n - i - 1):
            if res[j] > res[j + 1]:
                res[j], res[j + 1] = res[j + 1], res[j]

    return res[n - k : n]


def test_q7_k_largest_partial_passes():
    nums = [19, 1, 10, 45, 23, 78, 4, 90, 2]
    top_3 = find_k_largest_bubble(nums, k=3)
    # The 3 largest are 45, 78, 90
    assert top_3 == [45, 78, 90]

    top_1 = find_k_largest_bubble(nums, k=1)
    assert top_1 == [90]
    print("=== Q7: Partial Passes for K-Largest Elements Verified ===")


# ==============================================================================
# Question 8: Recursive Formulations of Bubble and Selection Sort
# ==============================================================================
def recursive_bubble_sort(arr: List[int], n: Optional[int] = None) -> List[int]:
    """Recursive Bubble Sort: Each recursive call bubbles largest element to index n-1."""
    if n is None:
        arr = list(arr)
        n = len(arr)

    if n <= 1:
        return arr

    for i in range(n - 1):
        if arr[i] > arr[i + 1]:
            arr[i], arr[i + 1] = arr[i + 1], arr[i]

    return recursive_bubble_sort(arr, n - 1)


def recursive_selection_sort(arr: List[int], start_idx: int = 0) -> List[int]:
    """Recursive Selection Sort: Each recursive call locates min in arr[start_idx:] and swaps."""
    if start_idx == 0:
        arr = list(arr)

    if start_idx >= len(arr) - 1:
        return arr

    min_idx = start_idx
    for j in range(start_idx + 1, len(arr)):
        if arr[j] < arr[min_idx]:
            min_idx = j

    if min_idx != start_idx:
        arr[start_idx], arr[min_idx] = arr[min_idx], arr[start_idx]

    return recursive_selection_sort(arr, start_idx + 1)


def test_q8_recursive_sorts():
    nums = [38, 27, 43, 3, 9, 82, 10]
    expected = sorted(nums)

    res_bubble = recursive_bubble_sort(nums)
    assert res_bubble == expected

    res_selection = recursive_selection_sort(nums)
    assert res_selection == expected
    print("=== Q8: Recursive Bubble and Selection Sorts Verified ===")


# ==============================================================================
# Question 9: Counting Inversions via Bubble Swaps
# ==============================================================================
def count_inversions_bubble(arr: List[int]) -> Tuple[int, List[Tuple[int, int]]]:
    """
    An inversion is a pair (i, j) such that i < j and arr[i] > arr[j].
    The number of adjacent swaps performed by standard Bubble Sort exactly equals
    the total number of inversions in the array.
    """
    res = list(arr)
    n = len(res)
    inversion_pairs: List[Tuple[int, int]] = []
    total_swaps = 0

    for i in range(n):
        for j in range(0, n - i - 1):
            if res[j] > res[j + 1]:
                inversion_pairs.append((res[j], res[j + 1]))
                res[j], res[j + 1] = res[j + 1], res[j]
                total_swaps += 1

    return total_swaps, inversion_pairs


def test_q9_inversion_counting():
    # Inversions in [2, 4, 1, 3, 5]: (2, 1), (4, 1), (4, 3) -> 3 inversions
    arr = [2, 4, 1, 3, 5]
    swaps, _ = count_inversions_bubble(arr)
    assert swaps == 3

    # Reverse sorted array [5, 4, 3, 2, 1] has n*(n-1)/2 = 10 inversions
    rev = [5, 4, 3, 2, 1]
    rev_swaps, _ = count_inversions_bubble(rev)
    assert rev_swaps == 10
    print("=== Q9: Inversion Counting via Bubble Swaps Verified ===")


# ==============================================================================
# Question 10: Architectural System: Multi-Metric E-Commerce Product Ranking Engine
# ==============================================================================
class ProductRecord:
    def __init__(self, sku: str, name: str, price: float, rating: float, sales_rank: int):
        self.sku = sku
        self.name = name
        self.price = price
        self.rating = rating
        self.sales_rank = sales_rank

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sku": self.sku,
            "name": self.name,
            "price": self.price,
            "rating": self.rating,
            "sales_rank": self.sales_rank,
        }


class RankedSortEngine:
    """
    Production-grade ranking engine utilizing stable sorting principles to perform
    multi-tier criteria ordering (e.g. Primary: Rating DESC, Secondary: Price ASC).
    """
    @staticmethod
    def multi_tier_stable_sort(
        products: List[ProductRecord],
        criteria: List[Tuple[str, bool]],  # List of (attribute_name, reverse_flag)
    ) -> List[ProductRecord]:
        """
        Sorts products across multiple criteria from lowest priority to highest priority
        using a stable sort, guaranteeing proper tie-breaking.
        """
        result = list(products)

        # Apply stable sort in reverse order of criteria (least significant first)
        for attr, reverse in reversed(criteria):
            n = len(result)
            for i in range(n):
                swapped = False
                for j in range(0, n - i - 1):
                    val_a = getattr(result[j], attr)
                    val_b = getattr(result[j + 1], attr)
                    should_swap = (val_a < val_b) if reverse else (val_a > val_b)
                    if should_swap:
                        result[j], result[j + 1] = result[j + 1], result[j]
                        swapped = True
                if not swapped:
                    break

        return result


def test_q10_ranked_sort_engine():
    catalog = [
        ProductRecord("SKU1", "Standard Mouse", price=25.0, rating=4.5, sales_rank=10),
        ProductRecord("SKU2", "Pro Gaming Mouse", price=80.0, rating=4.8, sales_rank=5),
        ProductRecord("SKU3", "Budget Mouse", price=15.0, rating=4.5, sales_rank=20),
        ProductRecord("SKU4", "Ergonomic Mouse", price=45.0, rating=4.5, sales_rank=8),
        ProductRecord("SKU5", "Ultra Mouse", price=120.0, rating=4.8, sales_rank=2),
    ]

    # Rank by:
    # 1. rating DESC (highest rating first)
    # 2. price ASC (cheaper price first for equal rating)
    criteria = [("rating", True), ("price", False)]
    sorted_catalog = RankedSortEngine.multi_tier_stable_sort(catalog, criteria)

    # Expected order:
    # 4.8 rating: SKU2 ($80), SKU5 ($120) -> SKU2 precedes SKU5
    # 4.5 rating: SKU3 ($15), SKU1 ($25), SKU4 ($45) -> SKU3, SKU1, SKU4
    skus = [p.sku for p in sorted_catalog]
    assert skus == ["SKU2", "SKU5", "SKU3", "SKU1", "SKU4"]
    print("=== Q10: Architectural Multi-Metric Product Ranking Engine Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_bubble_sort_optimized()
    test_q2_selection_sort()
    test_q3_stability_analysis()
    test_q4_cocktail_shaker_sort()
    test_q5_stable_selection_sort()
    test_q6_generic_sorting()
    test_q7_k_largest_partial_passes()
    test_q8_recursive_sorts()
    test_q9_inversion_counting()
    test_q10_ranked_sort_engine()
    print("\nAll 10 bubble sort and selection sort DSA questions passed successfully!")
