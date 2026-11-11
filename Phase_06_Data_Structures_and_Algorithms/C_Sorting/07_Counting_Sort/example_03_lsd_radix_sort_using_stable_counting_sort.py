"""
Phase 6 - Data Structures and Algorithms
Section C: Sorting - Topic 07: Counting Sort
Example 03: LSD Radix Sort (Using Stable Counting Sort as Digit Subroutine)

Demonstrates:
1. What happens when K is huge (e.g., 32-bit integers up to 10^9) where standalone
   Counting Sort would run out of RAM?
2. LSD (Least Significant Digit) Radix Sort solves this in O(d * (N + b)) linear time
   by running Stable Counting Sort `d` times — once per digit from least-significant
   (1s place) to most-significant (1000s place)!
3. Why the inner Counting Sort MUST be STABLE for Radix Sort to work!
"""


def counting_sort_by_digit(arr: list[int], exp: int, base: int = 10) -> list[int]:
    """
    Stable Counting Sort on `arr` according to the digit at place value `exp` (1, 10, 100, ...).
    Digit extraction formula: `(num // exp) % base`.
    """
    n = len(arr)
    output = [0] * n
    counts = [0] * base

    for num in arr:
        digit = (num // exp) % base
        counts[digit] += 1

    # Cumulative prefix sums
    for d in range(1, base):
        counts[d] += counts[d - 1]

    # Backward pass is MANDATORY to preserve previous digits' sorted order!
    for i in range(n - 1, -1, -1):
        num = arr[i]
        digit = (num // exp) % base
        counts[digit] -= 1
        output[counts[digit]] = num

    return output


def lsd_radix_sort(arr: list[int], trace: bool = False) -> list[int]:
    """
    Least-Significant-Digit (LSD) Radix Sort for non-negative integers.
    Time Complexity : O(d * (N + base)) where d = number of digits of max(arr)
    Space Complexity: O(N + base)
    """
    if not arr:
        return []
    a = arr.copy()
    max_num = max(a)
    exp = 1
    pass_num = 0

    while max_num // exp > 0:
        pass_num += 1
        a = counting_sort_by_digit(a, exp, base=10)
        if trace:
            print(f"  Pass {pass_num} (place value {exp:>4}s): {a}")
        exp *= 10

    return a


if __name__ == "__main__":
    print("=" * 72)
    print("1. LSD RADIX SORT powered by STABLE COUNTING SORT SUBROUTINE")
    print("=" * 72)

    invoice_numbers = [170, 45, 75, 90, 802, 24, 2, 66, 519, 304]
    print(f"Unsorted Invoices (N={len(invoice_numbers)}): {invoice_numbers}\n")
    sorted_invoices = lsd_radix_sort(invoice_numbers, trace=True)
    assert sorted_invoices == sorted(invoice_numbers)
    print(f"\nFinal Sorted Invoices    : {sorted_invoices}")
