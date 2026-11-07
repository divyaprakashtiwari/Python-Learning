# Section B: Searching — Topic 03: Variations of Binary Search

## 1. Introduction

In coding interviews and competitive programming, fewer than 10% of Binary Search problems ask you to find an exact value in a plain, distinct sorted array. The remaining 90% are **Variations of Binary Search** where you apply the halving invariant (`low`, `mid`, `high`) to:
1. **Boundary Finding in Arrays with Duplicates:** Locating the **First (Leftmost)** or **Last (Rightmost)** occurrence of a target, or counting its frequency in $O(\log N)$ time.
2. **Piecewise-Sorted or Bitonic Arrays:** Searching in a **Rotated Sorted Array** (`[45, 60, 75, 90, 10, 20, 30]`), finding the rotation pivot (minimum element), or finding a **Peak Element** (`arr[i] > neighbors`).
3. **Binary Search on the Answer Space (Parametric Search):** Solving optimization problems (*"Find the minimum ship capacity / koko eating speed / maximum minimum distance"*) where a boolean feasibility predicate `is_feasible(x)` transitions monotonically from `False` to `True`.

---

## 2. Why is it used?

1. **Handling Duplicates Without Degrading to $O(N)$:** If a sorted array of $10^7$ elements contains $5 \times 10^6$ copies of `20`, finding `20` with standard binary search and then scanning left and right linearly to count them degrades to $O(N)$ time! Two boundary binary searches (`last_occurrence - first_occurrence + 1`) solve it in guaranteed $O(\log N)$ time.
2. **Recovering Order After Cyclic Shifts:** Log files, circular ring buffers, and consistent-hashing rings are often sorted but rotated around a pivot index. Rotated Binary Search locates keys in $O(\log N)$ without un-rotating the buffer.
3. **Solving NP-Style Min-Max / Max-Min Optimization in Polynomial Time:** Whenever a question asks for the *"minimum possible maximum"* (e.g., Split Array Largest Sum, Capacity to Ship Packages, Aggressive Cows, Book Allocation), **Binary Search on the Answer Space** reduces an exponential partition search to $O(N \log(\text{Range}))$.

---

## 3. Syntax & Core Blueprints

### Blueprint 1: First & Last Occurrence in $O(\log N)$
```python
def find_boundary(arr: list[int], target: int, find_first: bool) -> int:
    low, high = 0, len(arr) - 1
    result = -1

    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            result = mid
            if find_first:
                high = mid - 1  # Keep searching LEFT for an earlier copy
            else:
                low = mid + 1   # Keep searching RIGHT for a later copy
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return result
```

### Blueprint 2: Universal "Binary Search on Answer" Template
```python
def binary_search_on_answer(low: int, high: int) -> int:
    best_ans = high
    while low <= high:
        mid = low + (high - low) // 2
        if is_feasible(mid):    # Monotonic predicate: False, False, ..., True, True
            best_ans = mid
            high = mid - 1      # Try to find an even smaller valid answer
        else:
            low = mid + 1       # Mid is too small; must increase
    return best_ans
```

---

## 4. Step-by-Step Explanation & Complexity Analysis

### 1. How Rotated Sorted Array Search Works in $O(\log N)$
Consider `arr = [45, 60, 75, 90, 10, 20, 30]`. Even though the whole array is not globally sorted, **splitting a rotated sorted array at any midpoint `mid` guarantees that AT LEAST ONE half (`[low .. mid]` or `[mid .. high]`) is strictly sorted!**
- Check if `arr[low] <= arr[mid]`:
  - If **True**, the left half `[low .. mid]` is contiguous and sorted. We can immediately check whether `arr[low] <= target < arr[mid]`. If yes, go left (`high = mid - 1`); otherwise, go right (`low = mid + 1`).
  - If **False**, the cliff drop lies in the left half, so the right half `[mid .. high]` **must** be strictly sorted! We check if `arr[mid] < target <= arr[high]`. If yes, go right (`low = mid + 1`); otherwise, go left (`high = mid - 1`).

### 2. Why Peak Element Works in $O(\log N)$ on an Unsorted Array
In `find_peak_element`, we compare `arr[mid]` with its right neighbor `arr[mid + 1]`:
- If `arr[mid] < arr[mid + 1]`, we are on a **rising slope** heading right. Since the right boundary of the array acts as $-\infty$, the numbers must eventually fall — guaranteeing at least one peak in `[mid + 1 .. high]`.
- If `arr[mid] > arr[mid + 1]`, we are on a **falling slope**, guaranteeing a peak in `[low .. mid]`.

### Complexity Summary

| Variation | Time Complexity | Auxiliary Space | Key Invariant |
| :--- | :--- | :--- | :--- |
| **First / Last Occurrence** | $O(\log N)$ | $O(1)$ | Record `result = mid` on match and continue halving |
| **Search in Rotated Array (Distinct)** | $O(\log N)$ | $O(1)$ | At least one half `[low..mid]` or `[mid..high]` is sorted |
| **Find Peak Element** | $O(\log N)$ | $O(1)$ | Move toward the higher neighbor (`arr[mid] < arr[mid+1]`) |
| **Binary Search on Answer Space** | $O(N \log(\text{High} - \text{Low}))$ | $O(1)$ | `is_feasible(x)` is monotonic (`FFF...TTT`) |
| **Exponential (Galloping) Search** | $O(\log i)$ ($i =$ target index) | $O(1)$ | Double `bound = 1, 2, 4, 8...` until `arr[bound] >= target` |

---

## 5. Practical Examples (3 Complete Programs)

### Example 1: First Occurrence, Last Occurrence, and $O(\log N)$ Frequency Count (`example_01_first_last_occurrence_and_count.py`)
```python
def find_first_occurrence(arr: list[int], target: int) -> int:
    low = 0
    high = len(arr) - 1
    first_idx = -1

    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            first_idx = mid
            high = mid - 1  # Continue searching left!
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return first_idx


def find_last_occurrence(arr: list[int], target: int) -> int:
    low = 0
    high = len(arr) - 1
    last_idx = -1

    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            last_idx = mid
            low = mid + 1  # Continue searching right!
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return last_idx
```

### Example 2: Rotated Sorted Array Search, Pivot Minimum, and Peak Element (`example_02_rotated_sorted_array_and_peak_element.py`)
```python
def search_rotated_sorted_array(arr: list[int], target: int) -> int:
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            return mid

        if arr[low] <= arr[mid]:
            if arr[low] <= target < arr[mid]:
                high = mid - 1
            else:
                low = mid + 1
        else:
            if arr[mid] < target <= arr[high]:
                low = mid + 1
            else:
                high = mid - 1

    return -1
```

### Example 3: Binary Search on the Answer Space & Exponential Search (`example_03_binary_search_on_answer_space.py`)
```python
def min_ship_capacity(weights: list[int], max_days: int) -> int:
    low = max(weights)
    high = sum(weights)
    best_capacity = high

    while low <= high:
        mid_cap = low + (high - low) // 2
        feasible, _ = can_ship_within_days(weights, max_days, mid_cap)

        if feasible:
            best_capacity = mid_cap
            high = mid_cap - 1
        else:
            low = mid_cap + 1

    return best_capacity
```

---

## 6. Verified Console Output

### Output of `example_01_first_last_occurrence_and_count.py`
```text
========================================================================
1. FIRST & LAST OCCURRENCE + O(log N) FREQUENCY COUNT
========================================================================
Sorted Array (n=11): [10, 15, 20, 20, 20, 20, 20, 35, 35, 50, 80]
Indices                 : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

  Target 20 -> First Idx:  2 | Last Idx:  6 | Total Count: 5
  Target 35 -> First Idx:  7 | Last Idx:  8 | Total Count: 2
  Target 10 -> First Idx:  0 | Last Idx:  0 | Total Count: 1
  Target 99 -> First Idx: -1 | Last Idx: -1 | Total Count: 0
```

### Output of `example_02_rotated_sorted_array_and_peak_element.py`
```text
========================================================================
1. SEARCH IN A ROTATED SORTED ARRAY O(log N)
========================================================================
Rotated Array: [45, 60, 75, 90, 10, 20, 30]
  Search 75 -> Index: 2
  Search 10 -> Index: 4
  Search 30 -> Index: 6
  Search 50 -> Index: -1
  Minimum Element: 10 at index 4 (Rotated by 4 positions)

========================================================================
2. FIND PEAK ELEMENT IN AN UNSORTED / BITONIC ARRAY O(log N)
========================================================================
Elevation Profile: [12, 28, 45, 82, 64, 51, 30, 15]
Peak Element     : 82 at index 3
```

### Output of `example_03_binary_search_on_answer_space.py`
```text
========================================================================
1. BINARY SEARCH ON THE ANSWER SPACE (MINIMUM SHIP CAPACITY IN D DAYS)
========================================================================
Package Weights : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] (Total = 55, Max = 10)
Deadline        : 5 days

Monotonic Feasibility Table across candidate capacities [10 .. 20]:
  Capacity = 10 -> Days Required = 7 -> Feasible (<=5 days)? False
  Capacity = 12 -> Days Required = 6 -> Feasible (<=5 days)? False
  Capacity = 14 -> Days Required = 6 -> Feasible (<=5 days)? False
  Capacity = 16 -> Days Required = 5 -> Feasible (<=5 days)? True
  Capacity = 18 -> Days Required = 4 -> Feasible (<=5 days)? True
  Capacity = 20 -> Days Required = 4 -> Feasible (<=5 days)? True

-> Optimal Minimum Capacity via Binary Search on Answer: 15

========================================================================
2. EXPONENTIAL (GALLOPING) SEARCH O(log i)
========================================================================
  Exponential Search for  10 -> Index: 0
  Exponential Search for  70 -> Index: 6
  Exponential Search for 640 -> Index: 63
  Exponential Search for 995 -> Index: -1
```

---

## 7. Code Explanation

1. **Why `if arr[low] <= arr[mid]:` Uses `<=` in Rotated Sorted Array Search:**
   When the remaining search window has only 2 elements (e.g., `low = 4, high = 5`), integer division gives `mid = 4 == low`. Thus `arr[low] == arr[mid]`, and the single-element left subarray `[low .. mid]` is trivially sorted! Using `<` instead of `<=` fails on 2-element windows.
2. **Why `find_min_in_rotated_sorted_array` Compares `arr[mid]` with `arr[high]` Instead of `arr[low]`:**
   In an unrotated sorted array `[10, 20, 30]` and a rotated array `[20, 30, 10]`, `arr[mid] > arr[low]` is True in **both** cases (`20 > 10` and `30 > 20`), so comparing against `arr[low]` cannot distinguish whether the minimum is to the left or right! Comparing `arr[mid]` against `arr[high]` uniquely determines which side holds the cliff drop.
3. **Choosing Tight Bounds (`low = max(weights)`, `high = sum(weights)`) in Answer-Space Binary Search:**
   In `min_ship_capacity`, no ship can have capacity less than `max(weights)` (otherwise the heaviest package could never board), and no ship ever needs capacity greater than `sum(weights)` (which ships everything in 1 day).

---

## 8. Common Mistakes

1. **Linearly Scanning Around `mid` to Count Duplicates:**
   Writing standard binary search and then `while left > 0 and arr[left-1] == target: left -= 1` takes **$O(N)$ worst-case time** when all elements in the array equal `target`! Always run two separate $O(\log N)$ boundary binary searches (`find_first_occurrence` and `find_last_occurrence`).
2. **Out-of-Bounds `arr[mid + 1]` in `find_peak_element`:**
   Because the loop condition is `while low < high:` (strict `<`), `mid = low + (high - low) // 2` is always strictly less than `high`, so `mid + 1 <= high < len(arr)` is **guaranteed** to be in bounds. If you mistakenly write `while low <= high:`, `mid + 1` will raise `IndexError` when `low == high == n - 1`.
3. **Forgetting Duplicate Edge Case in Rotated Sorted Array II (`arr[low] == arr[mid] == arr[high]`):**
   When a rotated sorted array contains duplicates (e.g., `[2, 2, 2, 0, 2]`), `arr[low] == arr[mid] == arr[high]` makes it impossible to tell which half contains `0`. You must shrink both ends (`low += 1; high -= 1`), which degrades worst-case time to $O(N)$.

---

## 9. Practice Questions

1. **Easy — First Bad Version (LeetCode 278):** You have $N$ versions `1..N` and an API `is_bad_version(v) -> bool`. Once a version is bad, all subsequent versions are bad (`False, False, ..., True, True`). Find the first bad version using the minimal number of API calls in $O(\log N)$ time.
2. **Medium — Koko Eating Bananas (LeetCode 875):** Given `piles` of bananas and `h` hours (`h >= len(piles)`), find the minimum integer eating speed `k` (bananas/hour) such that Koko can eat all piles within `h` hours (`sum(math.ceil(p / k) for p in piles) <= h`).
3. **Hard — Split Array Largest Sum / Book Allocation (LeetCode 410):** Given an integer array `nums` and an integer `k`, split `nums` into `k` non-empty contiguous subarrays such that the largest sum of any subarray is **minimized**. Solve in $O(N \log(\sum \text{nums}))$ time using Binary Search on Answer.

---

## 10. Interview Questions

### Q1: How do you recognize a "Binary Search on the Answer Space" problem in an interview when the input array isn't even sorted?
**Answer:**
Look for three telltale signs:
1. The problem asks for the **Minimum possible Maximum** (min-max) or **Maximum possible Minimum** (max-min), such as *"minimize the maximum subarray sum"* or *"maximize the minimum distance between cows"*.
2. The answer $X$ is bounded within a known numeric range `[low, high]`.
3. Given a candidate answer $X$, you can write a greedy $O(N)$ verification function `can_achieve(X)` that is **monotonic** (if $X$ works, then $X + 1$ also works).

### Q2: When is Exponential (Galloping) Search superior to standard Binary Search?
**Answer:**
1. When searching an **unbounded / infinite sorted stream** where `high` (`len(arr)`) is unknown.
2. When the target is known to be near the **beginning** of a massive sorted array (at index $i \ll N$): Exponential Search takes $O(\log i)$ time instead of $O(\log N)$ time. Python's **Timsort** uses Galloping Search when merging runs!

### Q3: What is the worst-case time complexity of searching in a Rotated Sorted Array WITH duplicates (`[1, 1, 1, 1, 0, 1]`), and why?
**Answer:**
**$O(N)$ in the worst case.** When `arr[low] == arr[mid] == arr[high]` (for example, `1 == 1 == 1`), the algorithm cannot determine whether the pivot (`0`) lies in the left half or the right half without inspecting both halves (or incrementing `low += 1` and decrementing `high -= 1`), which inspects up to $N$ elements when the array is nearly all identical values.
