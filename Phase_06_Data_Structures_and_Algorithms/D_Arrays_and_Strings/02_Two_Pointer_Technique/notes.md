# Section D: Arrays and Strings — Topic 02: Two Pointer Technique

## 1. Introduction

The **Two Pointer Technique** is one of the highest-yield algorithmic patterns in coding interviews. Instead of using nested `for` loops ($O(N^2)$ time) or allocating an auxiliary Hash Map ($O(N)$ memory) to search for pairs, triplets, or in-place array compactions, we coordinate **two index pointers** that traverse the data structure in a single coordinated $O(N)$ pass using strictly **$O(1)$ auxiliary space**.

There are two fundamental flavors of Two Pointers:
1. **Opposite-Direction (Converging) Two Pointers (`left = 0`, `right = n - 1`):**
   Start at both ends of a **sorted** (or geometric) array and step inward (`left += 1` or `right -= 1`) based on a monotonic comparison until `left >= right`.
2. **Same-Direction (Reader / Writer or Slow / Fast) Two Pointers (`writer = 0`, `reader = 0..n-1`):**
   Both pointers start at index `0` and move left-to-right. `reader` scouts ahead through every element, while `writer` advances only when a valid element is kept/compacted in-place.

---

## 2. Why is it used?

1. **Reduces $O(N^2)$ Brute-Force Pair Searches to $O(N)$ Linear Time:**
   In a sorted array, checking `arr[left] + arr[right]` against `target` eliminates an entire row or column of the $N \times N$ pair matrix on every single comparison!
2. **Eliminates $O(N)$ Hash Table Memory:**
   While a Hash Set can solve unsorted Two Sum in $O(N)$ time, it requires $O(N)$ heap memory. If the array is already sorted (or if sorting in $O(N \log N)$ is needed anyway, as in **3Sum** or **4Sum**), Two Pointers uses **$O(1)$ extra space**.
3. **Avoids $O(N^2)$ Shifting During In-Place Array Filtering:**
   Calling `arr.pop(i)` inside a loop to remove duplicates or zeroes takes $O(N^2)$ time. Reader/Writer two pointers compact the array in a single $O(N)$ pass.

---

## 3. Syntax & Core Blueprints

### Blueprint 1: Converging Two Pointers (`left = 0, right = n - 1`)
```python
def two_sum_sorted(arr: list[int], target: int) -> tuple[int, int] | None:
    left, right = 0, len(arr) - 1
    while left < right:
        curr = arr[left] + arr[right]
        if curr == target:
            return left, right
        elif curr < target:
            left += 1   # Sum too small -> need larger number
        else:
            right -= 1  # Sum too large -> need smaller number
    return None
```

### Blueprint 2: Reader / Writer In-Place Compaction (`writer = 0`)
```python
def filter_in_place(arr: list[int]) -> int:
    writer = 0
    for reader in range(len(arr)):
        if should_keep(arr[reader]):
            arr[writer] = arr[reader]
            writer += 1
    return writer  # New valid length of compacted prefix arr[:writer]
```

---

## 4. Step-by-Step Explanation & Complexity Analysis

### 1. Why Converging Two Pointers Never Misses the Optimal Pair
In **Container With Most Water** (`area = (right - left) * min(h[left], h[right])`), suppose `h[left] < h[right]`:
- The current height is bottlenecked by the shorter wall `h[left]`.
- If we moved the taller wall `right -= 1`, the width `(right - left)` would **shrink**, and the new height `min(h[left], h[right - 1])` could **never exceed `h[left]`**!
- Thus, every other container pairing `left` with any index `< right` is provably smaller. We can safely discard `left` and advance `left += 1`!

### 2. Why Trapping Rain Water Works in $O(1)$ Space with Two Pointers
Water trapped above bar `i` equals $\min(\text{max\_left}[i], \text{max\_right}[i]) - \text{height}[i]$.
When `left_max <= right_max`, we already know that **even if there is a gigantic wall somewhere between `left` and `right`**, the water level at `left` is bottlenecked by `left_max` (since `left_max <= right_max <= true_max_to_the_right_of_left`)! Thus we can immediately compute `left_max - heights[left]` in $O(1)$ space!

| Problem | Brute Force | Two-Pointer Time | Auxiliary Space |
| :--- | :--- | :--- | :--- |
| **Two Sum II (Sorted Array)** | $O(N^2)$ | $O(N)$ | $O(1)$ |
| **3Sum (Unique Zero Triplets)** | $O(N^3)$ | $O(N^2)$ (after $O(N \log N)$ sort) | $O(1)$ |
| **Container With Most Water** | $O(N^2)$ | $O(N)$ | $O(1)$ |
| **Remove Duplicates / Move Zeroes** | $O(N^2)$ (`pop`) | $O(N)$ | $O(1)$ |
| **Trapping Rain Water** | $O(N^2)$ | $O(N)$ | $O(1)$ |

---

## 5. Practical Examples (3 Complete Programs)

### Example 1: Converging Two Pointers — Two Sum II, Container With Most Water, and 3Sum (`example_01_converging_two_pointers_two_sum_and_3sum.py`)
```python
def three_sum_zero(nums: list[int]) -> list[tuple[int, int, int]]:
    a = sorted(nums)
    n = len(a)
    triplets: list[tuple[int, int, int]] = []

    for i in range(n - 2):
        if a[i] > 0:
            break
        if i > 0 and a[i] == a[i - 1]:
            continue

        left = i + 1
        right = n - 1
        while left < right:
            total = a[i] + a[left] + a[right]
            if total == 0:
                triplets.append((a[i], a[left], a[right]))
                left += 1
                right -= 1
                while left < right and a[left] == a[left - 1]:
                    left += 1
                while left < right and a[right] == a[right + 1]:
                    right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1

    return triplets
```

### Example 2: Reader / Writer Two Pointers — In-Place Deduplication & Move Zeroes (`example_02_reader_writer_in_place_deduplication_and_zeroes.py`)
```python
def remove_duplicates_sorted_in_place(arr: list[int], max_allowed_copies: int = 1) -> int:
    n = len(arr)
    if n <= max_allowed_copies:
        return n

    writer = max_allowed_copies
    for reader in range(max_allowed_copies, n):
        if arr[reader] != arr[writer - max_allowed_copies]:
            arr[writer] = arr[reader]
            writer += 1

    return writer
```

### Example 3: Trapping Rain Water ($O(1)$ Space) & Squares of a Sorted Array (`example_03_trapping_rain_water_and_sorted_squares.py`)
```python
def trap_rain_water_two_pointers(heights: list[int]) -> int:
    if not heights:
        return 0

    left = 0
    right = len(heights) - 1
    left_max = heights[left]
    right_max = heights[right]
    total_water = 0

    while left < right:
        if left_max <= right_max:
            left += 1
            left_max = max(left_max, heights[left])
            total_water += left_max - heights[left]
        else:
            right -= 1
            right_max = max(right_max, heights[right])
            total_water += right_max - heights[right]

    return total_water
```

---

## 6. Verified Console Output

### Output of `example_01_converging_two_pointers_two_sum_and_3sum.py`
```text
========================================================================
1. TWO SUM II ON SORTED ARRAY (O(N) TIME, O(1) SPACE)
========================================================================
Sorted Prices : [12, 25, 34, 48, 60, 75, 90]
Target = 85   -> Indices: (1, 4) (25 + 60 = 85)

========================================================================
2. CONTAINER WITH MOST WATER (O(N) TWO POINTERS)
========================================================================
Wall Heights  : [1, 8, 6, 2, 5, 4, 8, 3, 7]
Max Water Area: 49 between indices (1, 8) [heights 8 and 7]

========================================================================
3. 3SUM UNIQUE ZERO-SUM TRIPLETS (O(N^2) TWO POINTERS)
========================================================================
Input Array   : [-1, 0, 1, 2, -1, -4, -2, 3]
Zero Triplets : [(-4, 1, 3), (-2, -1, 3), (-2, 0, 2), (-1, -1, 2), (-1, 0, 1)]
```

### Output of `example_02_reader_writer_in_place_deduplication_and_zeroes.py`
```text
========================================================================
1. READER/WRITER IN-PLACE DEDUPLICATION ON SORTED ARRAY
========================================================================
Strict Unique (max 1 copy) -> Length=5, Prefix: [10, 20, 30, 40, 50]
At Most 2 Copies (LC 80)   -> Length=8, Prefix: [10, 10, 20, 30, 30, 40, 50, 50]

========================================================================
2. MOVE ZEROES TO END IN-PLACE (STABLE NON-ZERO ORDER)
========================================================================
Original Stream : [0, 42, 0, 19, 88, 0, 0, 73, 15]
Compacted Stream: [42, 19, 88, 73, 15, 0, 0, 0, 0]
```

### Output of `example_03_trapping_rain_water_and_sorted_squares.py`
```text
========================================================================
1. TRAPPING RAIN WATER IN O(N) TIME AND O(1) AUXILIARY SPACE
========================================================================
Elevation Map : [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
Trapped Water : 6 units

========================================================================
2. SQUARES OF A SORTED ARRAY WITH NEGATIVES IN O(N) TIME
========================================================================
Sorted Input  : [-7, -3, -1, 2, 4, 5, 11]
Sorted Squares: [1, 4, 9, 16, 25, 49, 121]
```

---

## 7. Code Explanation

1. **Why `arr[reader] != arr[writer - max_allowed_copies]` Generalizes Deduplication to Any $K$:**
   Because the valid compacted prefix `arr[0 .. writer - 1]` is sorted, if `arr[reader]` equals `arr[writer - K]`, then `arr[writer - K .. writer - 1]` already contains $K$ copies of that value! Comparing against `arr[writer - K]` (rather than `arr[reader - K]`, which could have been overwritten earlier) works for any $K \ge 1$.
2. **Why `sorted_squares_two_pointers` Fills the Result Array BACKWARD (`n - 1` down to `0`):**
   In a sorted array containing negative numbers (`[-7, -3, -1, 2, 4, 5, 11]`), the **largest** squares are guaranteed to sit at the two **outer extremes** (`left = 0` with $(-7)^2 = 49$, or `right = n - 1` with $11^2 = 121$), whereas the smallest squares sit somewhere in the middle near `0`. Therefore, converging pointers from the outside in naturally produce squares from **largest to smallest**!

---

## 8. Common Mistakes

1. **Running Converging Two-Sum on an UNSORTED Array Without Sorting First:**
   If the array is unsorted, knowing `arr[left] + arr[right] < target` does NOT tell you whether moving `left` right will increase or decrease the sum. Furthermore, if the problem asks for **original indices** of an unsorted array (LeetCode 1 Two Sum), sorting destroys the original indices unless you sort `(value, original_index)` pairs in $O(N \log N)$ time (or use an $O(N)$ Hash Map).
2. **Forgetting to Skip Duplicate Values in `3Sum`:**
   If you don't skip `if i > 0 and a[i] == a[i - 1]: continue` AND `while left < right and a[left] == a[left - 1]: left += 1`, inputs like `[-1, -1, 0, 1, 1]` will emit duplicate triplets `(-1, 0, 1)` multiple times.

---

## 9. Practice Questions

1. **Easy — Valid Palindrome Ignoring Non-Alphanumerics (LeetCode 125):** Use two converging pointers `left` and `right` that skip non-alphanumeric characters (`not s[left].isalnum()`) and compare `s[left].lower() == s[right].lower()` in $O(N)$ time and $O(1)$ space (without allocating a filtered string copy!).
2. **Medium — 3Sum Closest / 4Sum (LeetCode 16 / 18):** Given an integer array `nums` and an integer `target`, find three integers in `nums` such that the sum is closest to `target` in $O(N^2)$ time and $O(1)$ space.
3. **Hard — Boats to Save People / Minimize Maximum Pair Sum (LeetCode 881):** Given `people` weights and a boat `limit` (each boat carries at most 2 people), sort `people` and greedily pair the heaviest remaining person (`right`) with the lightest remaining person (`left`) if `people[left] + people[right] <= limit`.

---

## 10. Interview Questions

### Q1: When should you use Two Pointers vs a Hash Map for pair-sum problems?
**Answer:**
- **Use a Hash Map ($O(N)$ time, $O(N)$ space)** when the array is **unsorted** and you only need **1 pair** (or need original indices without sorting).
- **Use Converging Two Pointers ($O(N)$ time, $O(1)$ space)** when the input is **already sorted**, when memory is strictly constrained to $O(1)$, when finding **closest sum / count of pairs `< target`** (which a hash map cannot do in $O(1)$!), or inside **3Sum / 4Sum** where sorting once ($O(N \log N)$) is negligible compared to the $O(N^2)$ / $O(N^3)$ outer loops.

### Q2: How does the Dutch National Flag (3-Pointer) algorithm extend the Reader/Writer pattern?
**Answer:**
Instead of two zones (`[kept | uninspected]`), Dutch National Flag maintains **three zones** using three pointers (`low`, `mid`, `high`):
- `[0 .. low - 1]` = bottom bucket (`0`s)
- `[low .. mid - 1]` = middle bucket (`1`s)
- `[mid .. high]` = uninspected
- `[high + 1 .. n - 1]` = top bucket (`2`s)
It partitions 3 categories in a single $O(N)$ pass and $O(1)$ space.
