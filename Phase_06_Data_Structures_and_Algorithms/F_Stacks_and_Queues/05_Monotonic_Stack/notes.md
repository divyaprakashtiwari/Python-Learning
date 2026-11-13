# Monotonic Stack (Next Greater/Smaller Elements, Histogram Area & Rain Water)

---

## 1. Introduction

A **Monotonic Stack** is a stack whose elements (or the array values at the indices stored in the stack) are maintained in **monotonic order** from bottom to top — either:
1. **Monotonic Decreasing Stack** (`bottom -> [9, 7, 4, 2] <- top`):
   Whenever a new element $x$ is **greater** than the top of the stack, we pop all smaller elements. For every popped element, **$x$ is its exact Next Greater Element to the right!**
2. **Monotonic Increasing Stack** (`bottom -> [1, 3, 5, 8] <- top`):
   Whenever a new element $x$ is **smaller** than the top of the stack, we pop all larger elements. For every popped element, **$x$ is its exact Next Smaller Element to the right**, and the new top of the stack after popping is its **Previous Smaller Element to the left!**

Despite having a `while` loop nested inside a `for` loop, a Monotonic Stack runs in **strict $O(n)$ total time** because each of the $n$ indices is pushed onto the stack **once** and popped at most **once** ($\le 2n$ operations total).

---

## 2. Why is it used?

1. **Replaces $O(n^2)$ Lookahead Scans with $O(n)$ Single-Pass Resolution:** Finding the next warmer day (LeetCode 739), next greater element (LeetCode 496/503), or stock price span (LeetCode 901) naively takes $O(n^2)$ nested loops; a monotonic stack resolves all $n$ elements in a single linear pass.
2. **Simultaneous Left & Right Boundary Discovery:** In **Largest Rectangle in Histogram** (LeetCode 84) and **Sum of Subarray Minimums** (LeetCode 907), a single monotonic increasing stack identifies both the first smaller element to the left and the first smaller element to the right for every index $i$.
3. **Greedy Lexicographical / Numeric Minimization:** In **Remove K Digits** (LeetCode 402) and **Remove Duplicate Letters** (LeetCode 316), maintaining a monotonic increasing stack greedily discards larger high-significance digits whenever a smaller digit arrives.

---

## 3. Syntax

### Universal 4-Mode Monotonic Stack Reference Table

| Goal for Each Index `i` | Stack Order (Bottom $\to$ Top) | `while` Pop Condition | Updated When? |
| :--- | :--- | :--- | :--- |
| **Next Greater Element** (to the right) | **Decreasing** | `nums[stack[-1]] < nums[i]` | Inside `while` (on pop) |
| **Previous Greater Element** (to the left) | **Decreasing** | `nums[stack[-1]] <= nums[i]` | After `while` (`stack[-1]`) |
| **Next Smaller Element** (to the right) | **Increasing** | `nums[stack[-1]] > nums[i]` | Inside `while` (on pop) |
| **Previous Smaller Element** (to the left) | **Increasing** | `nums[stack[-1]] >= nums[i]` | After `while` (`stack[-1]`) |

### Template: Next Greater Element (Store **Indices**, Not Values!)
```python
def next_greater_elements(nums: list[int]) -> list[int]:
    res = [-1] * len(nums)
    stack: list[int] = []  # Stores indices with decreasing values

    for i, val in enumerate(nums):
        while stack and nums[stack[-1]] < val:
            prev_idx = stack.pop()
            res[prev_idx] = val
        stack.append(i)

    return res
```

---

## 4. Explanation (Step-by-Step)

### 1. Why You Should Almost Always Push **Indices** Instead of Raw Values
If `stack` stores index `idx`, you automatically have **both** the position (`idx`, needed to compute distances/widths like `curr_day - prev_day` or `right - left - 1`) **and** the value (`nums[idx]`)!

### 2. How Largest Rectangle in Histogram (LeetCode 84) Works in One Pass
For each bar `mid` of height $H = \text{heights}[mid]$, what is the widest rectangle of full height $H$ that includes bar `mid`?
- It extends left until the first bar `left_bound` with $\text{heights}[left\_bound] < H$.
- It extends right until the first bar `right_bound` with $\text{heights}[right\_bound] < H$.
- When we maintain a **monotonic increasing stack** and encounter `heights[i] < heights[stack[-1]]`:
  - Let `mid = stack.pop()`.
  - The bar that caused `mid` to be popped (`right_bound = i`) is guaranteed to be the **first bar smaller than `heights[mid]` to the right**!
  - Because the stack is monotonically increasing, the bar sitting immediately below `mid` in the stack (`left_bound = stack[-1]`) is the **first bar smaller than `heights[mid]` to the left**!
  - Therefore, the width is `right_bound - left_bound - 1`, and we compute `heights[mid] * width` immediately on pop! Appending a trailing `0` sentinel height at the end flushes all remaining bars from the stack cleanly.

---

## 5. Minimum 3 Examples

### Example 1: Next/Previous Greater Element, Daily Temperatures & Circular Array NGE
File: [`example_01_next_greater_element_and_daily_temperatures.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/F_Stacks_and_Queues/05_Monotonic_Stack/example_01_next_greater_element_and_daily_temperatures.py)

```python
def daily_temperatures(temperatures: List[int]) -> List[int]:
    n = len(temperatures)
    wait_days = [0] * n
    stack: List[int] = []  # Monotonic decreasing stack of day indices

    for curr_day, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            prev_day = stack.pop()
            wait_days[prev_day] = curr_day - prev_day
        stack.append(curr_day)

    return wait_days


def next_greater_elements_circular(nums: List[int]) -> List[int]:
    n = len(nums)
    res = [-1] * n
    stack: List[int] = []

    for step in range(2 * n):
        idx = step % n
        while stack and nums[stack[-1]] < nums[idx]:
            res[stack.pop()] = nums[idx]
        if step < n:
            stack.append(idx)

    return res
```

---

### Example 2: Largest Rectangle in Histogram (LeetCode 84) & Trapping Rain Water (LeetCode 42)
File: [`example_02_largest_rectangle_in_histogram_and_trapping_rain_water.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/F_Stacks_and_Queues/05_Monotonic_Stack/example_02_largest_rectangle_in_histogram_and_trapping_rain_water.py)

```python
def largest_rectangle_in_histogram(heights: List[int]) -> Tuple[int, Tuple[int, int, int]]:
    max_area = 0
    best_rect = (0, 0, -1)
    stack: List[int] = []  # Monotonic increasing stack of bar indices
    extended = heights + [0]  # Trailing 0 flushes all remaining bars at the end

    for right_bound, h in enumerate(extended):
        while stack and extended[stack[-1]] > h:
            mid = stack.pop()
            rect_height = extended[mid]
            left_bound = stack[-1] if stack else -1
            width = right_bound - left_bound - 1
            area = rect_height * width
            if area > max_area:
                max_area = area
                best_rect = (rect_height, left_bound + 1, right_bound - 1)
        stack.append(right_bound)

    return max_area, best_rect
```

---

### Example 3: Remove K Digits (LeetCode 402), Online Stock Span (LeetCode 901) & Subarray Minimums (LeetCode 907)
File: [`example_03_remove_k_digits_and_subarray_minimum_contributions.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/F_Stacks_and_Queues/05_Monotonic_Stack/example_03_remove_k_digits_and_subarray_minimum_contributions.py)

```python
def remove_k_digits(num: str, k: int) -> str:
    stack: List[str] = []
    for digit in num:
        while k > 0 and stack and stack[-1] > digit:
            stack.pop()
            k -= 1
        stack.append(digit)

    if k > 0:
        stack = stack[:-k]

    result = "".join(stack).lstrip("0")
    return result if result else "0"
```

---

## 6. Output

### Output — Example 1 (`example_01_next_greater_element_and_daily_temperatures.py`)
```text
========================================================================
1. Next Greater & Previous Greater Elements in One O(n) Pass
========================================================================
Input Array      : [2, 7, 4, 3, 5, 1, 9]
Next Greater     : [7, 9, 5, 5, 9, 9, -1]
Previous Greater : [-1, -1, 7, 4, 7, 5, -1]

========================================================================
2. Daily Temperatures — Days Until Warmer Weather (LeetCode 739)
========================================================================
Temperatures : [73, 74, 75, 71, 69, 72, 76, 73]
Wait Days    : [1, 1, 4, 2, 1, 1, 0, 0]

========================================================================
3. Circular Array Next Greater Element II (LeetCode 503)
========================================================================
Circular Array : [1, 2, 1, 4, 3]
Next Greater   : [2, 4, 4, -1, 4]
```

### Output — Example 2 (`example_02_largest_rectangle_in_histogram_and_trapping_rain_water.py`)
```text
========================================================================
1. Largest Rectangle in Histogram in O(n) Time (LeetCode 84 Hard)
========================================================================
  Heights: [2, 1, 5, 6, 2, 3]       -> Max Area = 10 (height=5 across indices [2..3])
  Heights: [2, 4]                   -> Max Area =  4 (height=4 across indices [1..1])
  Heights: [6, 2, 5, 4, 5, 1, 6]    -> Max Area = 12 (height=4 across indices [2..4])

========================================================================
2. Trapping Rain Water via Horizontal Valley Layers (LeetCode 42 Hard)
========================================================================
  Elevation Map: [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]   -> Trapped Water = 6
  Elevation Map: [4, 2, 0, 3, 2, 5]                     -> Trapped Water = 9
```

### Output — Example 3 (`example_03_remove_k_digits_and_subarray_minimum_contributions.py`)
```text
========================================================================
1. Remove K Digits for Smallest Number (LeetCode 402)
========================================================================
  num = '1432219', k = 3 -> smallest = '1219'
  num = '10200', k = 1 -> smallest = '200'
  num = '10', k = 2 -> smallest = '0'
  num = '12345', k = 2 -> smallest = '123'

========================================================================
2. Online Stock Span (LeetCode 901)
========================================================================
  Daily Prices : [100, 80, 60, 70, 60, 75, 85]
  Stock Spans  : [1, 1, 1, 2, 1, 4, 6]

========================================================================
3. Sum of Subarray Minimums via Monotonic Contribution (LeetCode 907)
========================================================================
  Array: [3, 1, 2, 4]           -> Sum of Subarray Mins = 17
  Array: [11, 81, 94, 43, 3]    -> Sum of Subarray Mins = 444
```

---

## 7. Code Explanation

1. **Handling Duplicate Minimums in `sum_of_subarray_minimums` (Asymmetric `<` vs `<=`):**
   Suppose an array is `[2, 1, 1, 2]`. Both index `1` and index `2` have value `1`. If both indices extended past equal values on both sides, the subarray `[2, 1, 1, 2]` would be counted **twice**! By making the left boundary stop at **strictly smaller (`<`)** elements (`while arr[stack[-1]] >= arr[i]: pop()`) and the right boundary stop at **smaller or equal (`<=`)** elements (`while arr[stack[-1]] > arr[i]: pop()`), every subarray with duplicate minimums is attributed uniquely to its **leftmost** minimum!
2. **Why `next_greater_elements_circular` Only Pushes When `step < n`:**
   During the second lap (`n <= step < 2*n`), we only want to **resolve** indices from the first lap that are still waiting in `stack`; pushing indices again on the second lap is redundant work.

---

## 8. Common Mistakes

1. **Forgetting to Flush Remaining Stack Elements in `largest_rectangle_in_histogram` or `remove_k_digits`:**
   - In `largest_rectangle_in_histogram`, if the input is strictly increasing (e.g., `[2, 4, 6]`), no bar ever pops during the loop unless you append a `0` sentinel height at the end!
   - In `remove_k_digits`, if the digits are already non-decreasing (`"12345"`, `k=2`), `k` is still `2` after the loop, so you must slice `stack = stack[:-k]`.
2. **Computing Histogram Width as `right_bound - mid` Instead of `right_bound - stack[-1] - 1`:**
   Bar `mid` can also extend **leftward** across any taller bars that were already popped before `mid`! The true left boundary is `stack[-1]` (the bar sitting below `mid` in the stack after `mid` is popped).

---

## 9. Practice Questions

1. **Easy — Final Prices With a Special Discount in a Shop (LeetCode 1475):**
   For each item `prices[i]`, you receive a discount equal to `prices[j]` where `j > i` is the **first** index with `prices[j] <= prices[i]`. Compute final prices in $O(n)$ time using a monotonic increasing stack.
2. **Medium — Car Fleet (LeetCode 853) & Asteroid Collision (LeetCode 735):**
   Simulate right-moving (`+`) and left-moving (`-`) asteroids on a 1D line where smaller asteroids explode on collision using a stack.
3. **Hard — Maximal Rectangle of `1`s in a 2D Binary Matrix (LeetCode 85):**
   Given an $R \times C$ binary matrix of `'0'` and `'1'`, maintain a running histogram of consecutive `'1'` heights for each row and invoke `largest_rectangle_in_histogram` on each row to find the largest rectangle of `'1'`s in $O(R \cdot C)$ time!

---

## 10. Interview Questions

### Q1: How does the Monotonic Stack solution for Trapping Rain Water (LeetCode 42) differ geometrically from the Two-Pointer solution?
**Answer:**
- The **Two-Pointer** solution computes trapped water **vertically column-by-column** (`min(left_max, right_max) - height[i]`).
- The **Monotonic Stack** solution computes trapped water **horizontally layer-by-layer** (`bounded_height * width`) whenever a rising right wall closes a valley floor. Both run in $O(n)$ time.

### Q2: How do you compute the **Sum of Subarray Ranges** ($\sum (\max(B) - \min(B))$ over all subarrays $B$, LeetCode 2104) in $O(n)$ time?
**Answer:** By linearity of summation:
$$\sum_{B} (\max(B) - \min(B)) = \sum_{B} \max(B) - \sum_{B} \min(B)$$
Compute $\sum \min(B)$ in $O(n)$ using a monotonic increasing stack (as in LeetCode 907) and $\sum \max(B)$ in $O(n)$ using a monotonic decreasing stack, then subtract!

### Q3: Why is the time complexity of `StockSpanner.next(price)` amortized $O(1)$ even though a single call can pop $n - 1$ elements?
**Answer:** Every daily price is pushed onto `self._stack` **once** and popped at most **once** when a future higher or equal price absorbs its span. Across $n$ calls to `.next()`, at most $n$ pops can ever occur, averaging $\le 1$ pop per call ($O(1)$ amortized).

