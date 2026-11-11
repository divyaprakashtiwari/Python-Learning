# Section D: Arrays and Strings — Topic 04: Prefix Sum

## 1. Introduction

A **Prefix Sum Array** (also called a **Cumulative Sum Array**) is a precomputation technique that transforms **$O(N)$ range-sum queries into $O(1)$ constant-time lookups**.

Given an array `nums` of length $N$, we construct a padded array `prefix` of length $N + 1$ where:
- `prefix[0] = 0`
- `prefix[i + 1] = prefix[i] + nums[i]` *(i.e., `prefix[k]` holds the sum of the first `k` elements `nums[0 .. k - 1]`)*

Then, the sum of **any** contiguous subarray `nums[L .. R]` (inclusive) is computed in **$O(1)$ time** via a single subtraction:
$$\sum_{k=L}^{R} \text{nums}[k] = \text{prefix}[R + 1] - \text{prefix}[L]$$

---

## 2. Why is it used?

1. **Instant $O(1)$ Range Sum Queries ($M$ Queries Drop from $O(M \cdot N)$ to $O(N + M)$):**
   In analytics dashboards, financial ledgers, and image processing (Integral Images / Summed-Area Tables), an array is queried thousands of times for different `[L, R]` intervals. Building `prefix` once in $O(N)$ makes every subsequent query $O(1)$.
2. **Solves Subarray Sum Problems WITH Negative Numbers (`Prefix Sum + Hash Map`):**
   When an array contains **negative numbers**, the Sliding Window Technique breaks down (because expanding `right` can decrease the sum). However, the algebraic identity:
   $$\text{sum}(i..j) = K \iff \text{prefix}[j] - \text{prefix}[i - 1] = K \iff \text{prefix}[i - 1] = \text{prefix}[j] - K$$
   holds for **all** real numbers (positive, zero, and negative)! Storing seen prefix sums in a Hash Map solves **Subarray Sum Equals $K$ (LeetCode 560)** in $O(N)$ time.
3. **2D Rectangular Subgrid Sums & 1D Difference Arrays:**
   - **2D Prefix Sums** compute the sum of any $H \times W$ sub-rectangle of a matrix in **$O(1)$ time** using Inclusion-Exclusion.
   - **Difference Arrays** (the mathematical inverse of Prefix Sums) apply batch range additions `add(L, R, delta)` in **$O(1)$ time per update**!

---

## 3. Syntax & Core Blueprints

### Blueprint 1: 1D Padded Prefix Sum ($O(N)$ Build, $O(1)$ Query)
```python
prefix = [0] * (len(nums) + 1)
for i, x in enumerate(nums):
    prefix[i + 1] = prefix[i] + x

# Sum of nums[L .. R] inclusive (no `if L == 0` branch needed!)
range_sum = prefix[R + 1] - prefix[L]
```

### Blueprint 2: Prefix Sum + Hash Map (`Subarray Sum Equals K`, LeetCode 560)
```python
def subarray_sum_k(nums: list[int], k: int) -> int:
    prefix_counts = {0: 1}  # Base case: empty prefix has sum 0
    curr_sum = 0
    count = 0
    for x in nums:
        curr_sum += x
        count += prefix_counts.get(curr_sum - k, 0)
        prefix_counts[curr_sum] = prefix_counts.get(curr_sum, 0) + 1
    return count
```

### Blueprint 3: Difference Array for $O(1)$ Range Updates
```python
diff = [0] * (n + 1)
for L, R, delta in updates:
    diff[L] += delta
    diff[R + 1] -= delta
# Final array is the prefix sum of diff[:n]
```

---

## 4. Step-by-Step Explanation & Complexity Analysis

### 1. Why Padded `prefix` of Size $N + 1$ Beats Unpadded Size $N$
If you define `P[i] = sum(nums[0..i])` (length $N$), every query has to write a branch: `P[R] if L == 0 else P[R] - P[L - 1]`. By prepending `prefix[0] = 0` (length $N + 1$), `L = 0` automatically subtracts `prefix[0] = 0` (`prefix[R + 1] - prefix[0]`), eliminating off-by-one bugs and branching in both 1D and 2D prefix sums!

### 2. 2D Prefix Sum Inclusion-Exclusion Formula
To compute the sum of rectangle `(r1, c1)` to `(r2, c2)` in $O(1)$ time:
$$\text{Sum} = P[r_2+1][c_2+1] - P[r_1][c_2+1] - P[r_2+1][c_1] + P[r_1][c_1]$$
Why `+ P[r1][c1]` at the end? Because the top-left corner `P[r1][c1]` was subtracted **twice** (once inside the top strip `P[r1][c2+1]` and once inside the left strip `P[r2+1][c1]`), so we add it back once!

| Technique | Precomputation | Per-Operation Time | Space |
| :--- | :--- | :--- | :--- |
| **1D Prefix Sum** | $O(N)$ | $O(1)$ per range sum query | $O(N)$ |
| **Prefix Sum + Hash Map** | N/A (1 pass) | $O(N)$ total for all subarrays | $O(N)$ |
| **2D Matrix Prefix Sum** | $O(R \cdot C)$ | $O(1)$ per 2D rectangle query | $O(R \cdot C)$ |
| **1D Difference Array** | $O(N)$ | $O(1)$ per range update + $O(N)$ rebuild | $O(N)$ |

---

## 5. Practical Examples (3 Complete Programs)

### Example 1: 1D Prefix Sum Queries & Pivot Equilibrium Index (`example_01_1d_prefix_sum_range_queries_and_pivot_index.py`)
```python
class RangeSumQueryImmutable:
    def __init__(self, nums: list[int]) -> None:
        self.prefix = [0] * (len(nums) + 1)
        for i, val in enumerate(nums):
            self.prefix[i + 1] = self.prefix[i] + val

    def query(self, left: int, right: int) -> int:
        return self.prefix[right + 1] - self.prefix[left]
```

### Example 2: Prefix Sum + Hash Map (`Subarray Sum Equals K`, `example_02_prefix_sum_hashmap_subarray_sum_equals_k.py`)
```python
def count_subarrays_with_sum_k(nums: list[int], k: int) -> int:
    prefix_counts: dict[int, int] = {0: 1}
    current_sum = 0
    total_subarrays = 0

    for num in nums:
        current_sum += num
        needed_prior_prefix = current_sum - k
        if needed_prior_prefix in prefix_counts:
            total_subarrays += prefix_counts[needed_prior_prefix]

        prefix_counts[current_sum] = prefix_counts.get(current_sum, 0) + 1

    return total_subarrays
```

### Example 3: 2D Matrix Prefix Sum & 1D Difference Array (`example_03_2d_matrix_prefix_sum_and_difference_array.py`)
```python
class NumMatrix2DPrefixSum:
    def __init__(self, matrix: list[list[int]]) -> None:
        rows = len(matrix)
        cols = len(matrix[0]) if rows > 0 else 0
        self.pref = [[0] * (cols + 1) for _ in range(rows + 1)]

        for r in range(rows):
            for c in range(cols):
                self.pref[r + 1][c + 1] = (
                    matrix[r][c]
                    + self.pref[r][c + 1]
                    + self.pref[r + 1][c]
                    - self.pref[r][c]
                )

    def sum_region(self, r1: int, c1: int, r2: int, c2: int) -> int:
        return (
            self.pref[r2 + 1][c2 + 1]
            - self.pref[r1][c2 + 1]
            - self.pref[r2 + 1][c1]
            + self.pref[r1][c1]
        )
```

---

## 6. Verified Console Output

### Output of `example_01_1d_prefix_sum_range_queries_and_pivot_index.py`
```text
========================================================================
1. 1D PREFIX SUM ARRAY: O(N) BUILD, O(1) RANGE SUM QUERIES
========================================================================
Daily Revenue (N=8) : [120, 85, 200, 150, 95, 310, 140, 260]
Padded Prefix Array (N+1) : [0, 120, 205, 405, 555, 650, 960, 1100, 1360]

  query(0, 3) = prefix[4] (555) - prefix[0] (0) = 555
  query(2, 5) = prefix[6] (960) - prefix[2] (205) = 755
  query(0, 7) = prefix[8] (1360) - prefix[0] (0) = 1360
  query(4, 4) = prefix[5] (650) - prefix[4] (555) = 95

========================================================================
2. FIND PIVOT / EQUILIBRIUM INDEX IN O(N) TIME & O(1) SPACE
========================================================================
  Array: [1, 7, 3, 6, 5, 6]     -> Pivot Index: 3
  Array: [1, 2, 3]              -> Pivot Index: -1
  Array: [2, 1, -1]             -> Pivot Index: 0
```

### Output of `example_02_prefix_sum_hashmap_subarray_sum_equals_k.py`
```text
========================================================================
1. SUBARRAY SUM EQUALS K WITH NEGATIVE NUMBERS (LEETCODE 560)
========================================================================
Input Array (with negatives): [3, 4, -7, 1, 3, 3, 1, -4]
Total Subarrays Summing to 7: 4
  Matching Subarrays: [3, 4], [3, 4, -7, 1, 3, 3], [1, 3, 3], [3, 3, 1]

========================================================================
2. LONGEST SUBARRAY WITH SUM == K (FIRST-SEEN PREFIX INDEX MAP)
========================================================================
Longest Subarray Summing to 7: [3, 4, -7, 1, 3, 3] (Length = 6)
```

### Output of `example_03_2d_matrix_prefix_sum_and_difference_array.py`
```text
========================================================================
1. 2D MATRIX PREFIX SUM (O(1) RECTANGULAR SUBGRID QUERIES)
========================================================================
Subgrid (1, 1) to (2, 2) [6+3+2+0]       -> Sum: 11
Subgrid (1, 2) to (3, 4) [3+2+1+0+1+5+0+1+7] -> Sum: 20

========================================================================
2. DIFFERENCE ARRAY: O(1) BATCH RANGE ADDITION UPDATES
========================================================================
Updates on N=5 zeros: [(1, 3, 2), (2, 4, 3), (0, 2, -2)]
Final Reconstructed : [-2, 0, 3, 5, 3]
```

---

## 7. Code Explanation

1. **Why `prefix_counts = {0: 1}` Is Initialized Before the Loop:**
   Suppose `nums = [3, 4]` and `k = 7`. At index `1`, `current_sum = 7`, which means the subarray `nums[0..1]` **starting from index 0** sums to `7`. We look up `needed = current_sum - k = 7 - 7 = 0`. Having `{0: 1}` (and `{0: -1}` in `longest_subarray_with_sum_k`) represents the empty prefix before index `0`!
2. **Why `longest_subarray_with_sum_k` Only Records `current_sum` If Not Already Present (`if current_sum not in first_seen_idx:`):**
   When negative and positive numbers cancel out (like `4` and `-4`), the same `current_sum` can occur at multiple indices $i_1 < i_2$. To **maximize** the subarray length `idx - i`, we must always keep the **earliest (smallest)** index $i_1$!

---

## 8. Common Mistakes

1. **Updating `prefix_counts[current_sum] += 1` BEFORE Checking `current_sum - k`:**
   If $k = 0$ and you increment `prefix_counts[current_sum]` before looking up `current_sum - 0`, you will match `current_sum` with **itself** (counting an empty 0-length subarray at every index!). Always query `current_sum - k` **first**, and update `prefix_counts[current_sum]` **second**.
2. **Using a Static Prefix Sum Array When Elements Are Frequently Mutated Interleaved With Queries:**
   Updating a single element `nums[i]` forces you to recompute `prefix[i+1 .. n]` in $O(N)$ time! When point updates and range sum queries are interleaved, use a **Fenwick Tree (Binary Indexed Tree)** or **Segment Tree** ($O(\log N)$ update and $O(\log N)$ query).

---

## 9. Practice Questions

1. **Easy — Contiguous Array with Equal 0s and 1s (LeetCode 525):** Given a binary array `nums`, find the maximum length of a contiguous subarray with an equal number of `0` and `1` by treating every `0` as `-1` and finding the longest subarray with sum `0` in $O(N)$ time!
2. **Medium — Subarray Sums Divisible by $K$ (LeetCode 974):** Given an integer array `nums` and an integer `k`, return the number of non-empty subarrays that have a sum divisible by `k` using modular prefix remainders `(curr_sum % k)` in a hash map!
3. **Hard — Corporate Flight Bookings / Car Pooling (LeetCode 1109 / 1094):** Use a 1D Difference Array to process $M$ overlapping interval bookings `[first, last, seats]` in $O(N + M)$ time.

---

## 10. Interview Questions

### Q1: Why does Python's `curr_sum % k` make "Subarray Sums Divisible by K" easier in Python than in C++ or Java?
**Answer:**
A subarray `nums[i..j]` has a sum divisible by $K$ if and only if `prefix[j] % K == prefix[i - 1] % K`. In C++ and Java, `-7 % 5` evaluates to `-2` (a negative remainder!), requiring `((curr_sum % k) + k) % k`. In Python, the `%` operator always returns a remainder with the same sign as the divisor (`-7 % 5 == 3`), so `curr_sum % k` is automatically normalized in `[0 .. k - 1]`!

### Q2: Can Prefix Sums be used for Range XOR Queries (`XOR(nums[L .. R])`)?
**Answer:**
**Yes!** Because XOR is its own inverse ($A \oplus A = 0$), precomputing `prefix_xor[i + 1] = prefix_xor[i] ^ nums[i]` answers any range XOR query in $O(1)$ time via `prefix_xor[R + 1] ^ prefix_xor[L]`! (However, Prefix Min/Max cannot be inverted to answer arbitrary `[L, R]` queries because `min` and `max` have no inverse operation — use a Sparse Table for $O(1)$ Range Minimum Queries.)
