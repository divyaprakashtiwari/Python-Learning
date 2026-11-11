# Section D: Arrays and Strings — Topic 05: Kadane's Algorithm

## 1. Introduction

**Kadane's Algorithm** (proposed by Jay Kadane at Carnegie Mellon University in 1984) is an elegant **Dynamic Programming / Greedy** algorithm that finds the **Maximum Sum Contiguous Subarray** inside a 1D array of numbers (containing both positive and negative values) in **$O(N)$ linear time and strictly $O(1)$ auxiliary space**.

At every index `i` as we scan from left to right, we face a binary choice for the best subarray **ending at index `i`**:
1. **Extend** the best subarray ending at `i - 1` by adding `nums[i]` (`curr_sum + nums[i]`), OR
2. **Start fresh** at index `i` (`nums[i]`) because `curr_sum < 0` is negative baggage that can only reduce our sum!
$$\text{curr\_sum} = \max(\text{nums}[i],\; \text{curr\_sum} + \text{nums}[i])$$
$$\text{max\_sum} = \max(\text{max\_sum},\; \text{curr\_sum})$$

---

## 2. Why is it used?

1. **Reduces $O(N^2)$ Brute-Force Subarray Search to $O(N)$ Time and $O(1)$ Space:**
   An array of length $N = 100,000$ has $\frac{N(N+1)}{2} \approx 5 \times 10^9$ contiguous subarrays. Checking all of them takes seconds; Kadane's Algorithm finishes in a few milliseconds using two scalar registers (`curr_sum`, `max_sum`).
2. **Generalizes to Circular Arrays, Maximum Product Subarrays, and 2D Matrices:**
   - **Maximum Sum Circular Subarray (LeetCode 918):** Solved in 1 pass via $\max(\text{max\_kadane},\; \text{total\_sum} - \text{min\_kadane})$.
   - **Maximum Product Subarray (LeetCode 152):** Solved by tracking both `curr_max` and `curr_min` (since multiplying two negatives produces a positive).
   - **Maximum Sum Rectangle in a 2D Matrix (LeetCode 363 variant):** Compresses rows between columns `(c1, c2)` and runs 1D Kadane in $O(C^2 \cdot R)$ time.

---

## 3. Syntax & Core Blueprints

### Blueprint 1: Classic Kadane's Algorithm ($O(N)$ Time, $O(1)$ Space)
```python
def max_subarray_sum(nums: list[int]) -> int:
    curr_sum = nums[0]
    max_sum = nums[0]

    for i in range(1, len(nums)):
        curr_sum = max(nums[i], curr_sum + nums[i])
        max_sum = max(max_sum, curr_sum)

    return max_sum
```

### Blueprint 2: Maximum Product Subarray (Dual `curr_max` / `curr_min` State)
```python
def max_product_subarray(nums: list[int]) -> int:
    curr_max = curr_min = best = nums[0]
    for x in nums[1:]:
        if x < 0:
            curr_max, curr_min = curr_min, curr_max  # Negative flips sign!
        curr_max = max(x, curr_max * x)
        curr_min = min(x, curr_min * x)
        best = max(best, curr_max)
    return best
```

---

## 4. Step-by-Step Explanation & Complexity Analysis

### Tracing Kadane's Algorithm on `[-2, 1, -3, 4, -1, 2, 1, -5, 4]`

| Index `i` | `nums[i]` | `curr_sum = max(nums[i], curr_sum + nums[i])` | Active Subarray | `max_sum` |
| :---: | :---: | :--- | :--- | :---: |
| `0` | `-2` | `-2` (init) | `[-2]` | `-2` |
| `1` | `1` | `max(1, -2 + 1) = 1` *(reset!)* | `[1]` | `1` |
| `2` | `-3` | `max(-3, 1 - 3) = -2` *(extend)* | `[1, -3]` | `1` |
| `3` | `4` | `max(4, -2 + 4) = 4` *(reset!)* | `[4]` | `4` |
| `4` | `-1` | `max(-1, 4 - 1) = 3` *(extend)* | `[4, -1]` | `4` |
| `5` | `2` | `max(2, 3 + 2) = 5` *(extend)* | `[4, -1, 2]` | `5` |
| `6` | `1` | `max(1, 5 + 1) = 6` *(extend)* | `[4, -1, 2, 1]` | **`6`** |
| `7` | `-5` | `max(-5, 6 - 5) = 1` *(extend)* | `[4, -1, 2, 1, -5]` | `6` |
| `8` | `4` | `max(4, 1 + 4) = 5` *(extend)* | `[4, -1, 2, 1, -5, 4]` | `6` |

### Why Circular Maximum Subarray Equals $\max(\text{MaxKadane},\; \text{TotalSum} - \text{MinKadane})$
Any subarray in a circular array either:
1. Does **not** wrap around the boundary (standard Kadane `max_so_far`), OR
2. **Wraps around** both ends (takes a prefix `nums[0..i]` + a suffix `nums[j..n-1]`). The elements **excluded** in the middle (`nums[i+1 .. j-1]`) form a normal non-wrapping subarray! Maximizing the wrapped sum is equivalent to **minimizing the excluded middle subarray** (`total_sum - min_so_far`).

| Variant | Time Complexity | Auxiliary Space | Handles All-Negative? |
| :--- | :--- | :--- | :--- |
| **Standard Kadane (LC 53)** | $\Theta(N)$ | $O(1)$ | Yes (init `max_sum = nums[0]`) |
| **Circular Subarray (LC 918)** | $\Theta(N)$ | $O(1)$ | Yes (guard `if max_so_far < 0`) |
| **Maximum Product (LC 152)** | $\Theta(N)$ | $O(1)$ | Yes |

---

## 5. Practical Examples (3 Complete Programs)

### Example 1: Classic Kadane's Algorithm with Exact Subarray Indices (`example_01_classic_kadane_max_subarray_with_indices.py`)
```python
def kadane_max_subarray_with_indices(
    nums: list[int],
) -> tuple[int, int, int, list[int]]:
    if not nums:
        raise ValueError("Input array must be non-empty")

    curr_sum = nums[0]
    max_sum = nums[0]
    curr_start = 0
    best_start = 0
    best_end = 0

    for i in range(1, len(nums)):
        val = nums[i]
        if curr_sum < 0:
            curr_sum = val
            curr_start = i
        else:
            curr_sum += val

        if curr_sum > max_sum:
            max_sum = curr_sum
            best_start = curr_start
            best_end = i

    return max_sum, best_start, best_end, nums[best_start : best_end + 1]
```

### Example 2: Maximum Sum Circular Subarray (`example_02_maximum_sum_circular_subarray.py`)
```python
def max_subarray_sum_circular(nums: list[int]) -> tuple[int, int, int]:
    total_sum = 0
    curr_max = 0
    max_so_far = nums[0]
    curr_min = 0
    min_so_far = nums[0]

    for x in nums:
        total_sum += x
        curr_max = max(x, curr_max + x)
        max_so_far = max(max_so_far, curr_max)
        curr_min = min(x, curr_min + x)
        min_so_far = min(min_so_far, curr_min)

    if max_so_far < 0:
        return max_so_far, max_so_far, min_so_far

    circular_best = max(max_so_far, total_sum - min_so_far)
    return circular_best, max_so_far, min_so_far
```

### Example 3: Maximum Product Subarray & Best Time to Buy/Sell Stock (`example_03_max_product_subarray_and_stock_profit.py`)
```python
def max_product_subarray(nums: list[int]) -> int:
    curr_max = nums[0]
    curr_min = nums[0]
    best_prod = nums[0]

    for i in range(1, len(nums)):
        x = nums[i]
        if x < 0:
            curr_max, curr_min = curr_min, curr_max

        curr_max = max(x, curr_max * x)
        curr_min = min(x, curr_min * x)
        best_prod = max(best_prod, curr_max)

    return best_prod
```

---

## 6. Verified Console Output

### Output of `example_01_classic_kadane_max_subarray_with_indices.py`
```text
========================================================================
1. KADANE'S ALGORITHM: MAXIMUM SUBARRAY SUM & EXACT INDICES
========================================================================

[Classic LeetCode 53] Input: [-2, 1, -3, 4, -1, 2, 1, -5, 4]
  Max Sum =   6 | Range: [3 .. 6] -> Subarray: [4, -1, 2, 1]

[All Negative Numbers] Input: [-8, -3, -6, -2, -5, -4]
  Max Sum =  -2 | Range: [3 .. 3] -> Subarray: [-2]

[Profit/Loss Swing] Input: [15, -20, 12, 18, -5, 25, -40, 10]
  Max Sum =  50 | Range: [2 .. 5] -> Subarray: [12, 18, -5, 25]
```

### Output of `example_02_maximum_sum_circular_subarray.py`
```text
========================================================================
1. MAXIMUM SUM CIRCULAR SUBARRAY (LEETCODE 918) IN 1 PASS
========================================================================
  Wrapping Wins [5, -3, 5]             | Total=  7, MaxKadane= 7, MinKadane= -3 -> Circular Max: 10
  Non-Wrapping Wins [1, -2, 3, -2]     | Total=  0, MaxKadane= 3, MinKadane= -2 -> Circular Max: 3
  Heavy Wrap [8, -1, -3, 8]            | Total= 12, MaxKadane=12, MinKadane= -4 -> Circular Max: 16
  All Negative Edge Case [-3, -2, -5]  | Total=-10, MaxKadane=-2, MinKadane=-10 -> Circular Max: -2
```

### Output of `example_03_max_product_subarray_and_stock_profit.py`
```text
========================================================================
1. MAXIMUM PRODUCT SUBARRAY (TRACKING MAX & MIN FOR SIGN FLIPS)
========================================================================
  Array: [2, 3, -2, 4]          -> Max Product Subarray: 6
  Array: [-2, 0, -1]            -> Max Product Subarray: 0
  Array: [-2, 3, -4]            -> Max Product Subarray: 24
  Array: [2, -5, -2, -4, 3]     -> Max Product Subarray: 24

========================================================================
2. BEST TIME TO BUY & SELL STOCK (KADANE ON PRICE DELTAS)
========================================================================
Stock Prices : [7, 1, 5, 3, 6, 4]
Max Profit   : 5 (Buy on Day 1 at 1, Sell on Day 4 at 6)
```

---

## 7. Code Explanation

1. **Why Initializing `max_sum = 0` Fails on All-Negative Arrays:**
   In LeetCode 53, the problem requires a **non-empty** subarray. If `nums = [-8, -3, -6, -2]` and you initialize `max_sum = 0` (or reset `if curr_sum < 0: curr_sum = 0` before updating `max_sum`), your function returns `0` instead of `-2`! Initializing `curr_sum = max_sum = nums[0]` (or `max_sum = -math.inf`) guarantees the correct negative answer.
2. **Why `if max_so_far < 0: return max_so_far` Is Mandatory in Circular Kadane:**
   When every element is negative (`[-3, -2, -5]`), the minimum subarray is the **entire array** (`min_so_far = -10 = total_sum`). Computing `total_sum - min_so_far` subtracts all elements and leaves an **empty** subarray with sum `0`, which is illegal. Checking `if max_so_far < 0:` catches this immediately!

---

## 8. Common Mistakes

1. **Updating `curr_min` Using the Already-Updated `curr_max` in `max_product_subarray`:**
   If you don't swap `curr_max, curr_min = curr_min, curr_max` when `x < 0` (or if you write `curr_max = max(x, curr_max * x, curr_min * x)` and then use that new `curr_max` on the next line to compute `curr_min`), you corrupt `curr_min`! Either swap `curr_max` and `curr_min` when `x < 0`, or use tuple simultaneous assignment:
   `curr_max, curr_min = max(x, curr_max * x, curr_min * x), min(x, curr_max * x, curr_min * x)`.

---

## 9. Practice Questions

1. **Easy — Maximum Ascending Subarray Sum (LeetCode 1800):** Given an array of positive integers `nums`, return the maximum possible sum of an strictly ascending contiguous subarray in $O(N)$ time and $O(1)$ space.
2. **Medium — Maximum Absolute Sum of Any Subarray (LeetCode 1749):** Find the maximum of `abs(sum(subarray))` in a single $O(N)$ pass by computing `max(abs(max_kadane), abs(min_kadane))` (or `max_prefix_sum - min_prefix_sum`)!
3. **Hard — Maximum Subarray Sum with One Deletion (LeetCode 1186):** Given an array of integers, return the maximum sum for a non-empty subarray where you may optionally delete at most **one** element from the subarray in $O(N)$ time and $O(1)$ space using two DP states (`no_delete`, `one_delete`).

---

## 10. Interview Questions

### Q1: How can you solve Maximum Subarray Sum using Divide and Conquer, and how does its complexity compare to Kadane's Algorithm?
**Answer:**
Divide the array at `mid`: the maximum subarray lies either (1) entirely in the left half, (2) entirely in the right half, or (3) **crosses the midpoint** (found in $O(N)$ by scanning outward left from `mid` and right from `mid + 1`). By Master Theorem $T(N) = 2T(N/2) + \Theta(N) = \Theta(N \log N)$ time and $O(\log N)$ stack space. While asymptotically slower than Kadane's $O(N)$ time / $O(1)$ space on a single thread, the Divide-and-Conquer state `(total_sum, max_prefix, max_suffix, max_subarray)` can be stored in a **Segment Tree** to answer dynamic range maximum subarray queries in $O(\log N)$ time!

### Q2: How does Kadane's Algorithm connect to Prefix Sums?
**Answer:**
Since $\text{sum}(i..j) = \text{prefix}[j + 1] - \text{prefix}[i]$, maximizing $\text{sum}(i..j)$ over all $i \le j$ is equivalent to tracking the **minimum prefix sum seen so far** (`min_prefix`) and maximizing `current_prefix - min_prefix` at each step `j` — which is the exact same recurrence as Best Time to Buy and Sell Stock!
