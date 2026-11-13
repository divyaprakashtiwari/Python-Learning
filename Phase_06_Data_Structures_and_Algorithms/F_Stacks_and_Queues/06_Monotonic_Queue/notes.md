# Monotonic Queue (Sliding Window Maximum/Minimum, Bounded Diff & DP Optimization)

---

## 1. Introduction

A **Monotonic Queue** (also called a **Monotonic Deque**) is a Double-Ended Queue (`collections.deque`) that maintains its elements in strictly/weakly monotonic order from front to back while supporting **both** back-end dominance pruning and front-end window expiration:

1. **Back-End Dominance Pruning (`dq.pop()`):** Before inserting a new index `i` at the rear, pop all indices `j` at the rear whose values are **dominated** by `nums[i]` (for a maximum queue, `nums[j] <= nums[i]`). Why? Because `i` is **both newer** (stays in the sliding window longer than `j`) **and larger** (`nums[i] >= nums[j]`), so `j` can **never** be the maximum of the current or any future window!
2. **Front-End Expiration (`dq.popleft()`):** Remove the front index `dq[0]` whenever it slides out of the current window (`dq[0] <= i - k`).
3. **$O(1)$ Window Extreme Query (`nums[dq[0]]`):** Because the deque is monotonically ordered from front to back, the **front element `dq[0]` is always the exact maximum (or minimum) of the active window in $O(1)$ time!**

---

## 2. Why is it used?

1. **$O(n)$ Sliding Window Maximum / Minimum (LeetCode 239):** A naive sliding window maximum scans $k$ elements per window in $O(n \cdot k)$ time, and a Binary Heap / BST takes $O(n \log k)$ time. A Monotonic Queue solves it in **strict $O(n)$ linear time**!
2. **Variable-Size Sliding Windows Bounded by $\max - \min \le \text{limit}$ (LeetCode 1438):** Maintaining both a monotonic decreasing deque (`max_dq`) and a monotonic increasing deque (`min_dq`) tracks the window range `max - min` in $O(1)$ time per step.
3. **Subarray Sum Problems With Negative Numbers (LeetCode 862 Hard):** When negative numbers break prefix-sum monotonicity, a monotonic increasing deque over prefix sums restores $O(n)$ sliding-window behavior.
4. **1D Dynamic Programming Range-Max Optimization (LeetCode 1696 / 1425):** Reduces transitions of the form $dp[i] = \text{nums}[i] + \max_{i - k \le j < i} dp[j]$ from $O(n \cdot k)$ to $O(n)$!

---

## 3. Syntax

### Sliding Window Maximum Template ($O(n)$ Time, $O(k)$ Space)
```python
from collections import deque

def max_sliding_window(nums: list[int], k: int) -> list[int]:
    dq: deque[int] = deque()  # Stores indices with decreasing values
    out: list[int] = []

    for i, val in enumerate(nums):
        # 1. Evict expired front index outside window [i - k + 1 .. i]
        if dq and dq[0] <= i - k:
            dq.popleft()

        # 2. Pop smaller/equal dominated indices from the rear
        while dq and nums[dq[-1]] <= val:
            dq.pop()

        # 3. Append current index
        dq.append(i)

        # 4. Record window maximum at `dq[0]` once window reaches size k
        if i >= k - 1:
            out.append(nums[dq[0]])

    return out
```

---

## 4. Explanation (Step-by-Step)

### Step-by-Step Trace on `nums = [1, 3, -1, -3, 5]`, `k = 3`

| Index `i` | `val` | Front Eviction (`<= i - 3`) | Back Dominance Pop (`nums[dq[-1]] <= val`) | `dq` Indices (`Values`) | Window Max (`i >= 2`) |
| :---: | :---: | :--- | :--- | :--- | :---: |
| `0` | `1` | None | None | `[0]` (`[1]`) | — |
| `1` | `3` | None | Pop `0` (`1 <= 3`) | `[1]` (`[3]`) | — |
| `2` | `-1` | None | None (`3 > -1`) | `[1, 2]` (`[3, -1]`) | `nums[1] = 3` |
| `3` | `-3` | None (`1 > 0`) | None (`-1 > -3`) | `[1, 2, 3]` (`[3, -1, -3]`) | `nums[1] = 3` |
| `4` | `5` | Pop `1` (`1 <= 1`) | Pop `3` (`-3 <= 5`), Pop `2` (`-1 <= 5`) | `[4]` (`[5]`) | `nums[4] = 5` |

### Why LeetCode 862 (Shortest Subarray With Sum $\ge K$ with Negatives) Needs a Monotonic Deque
Let $P[idx] = \sum_{m=0}^{idx-1} \text{nums}[m]$ be the prefix sum array. We want the shortest subarray $[i \dots j-1]$, i.e., minimum $j - i$ such that $P[j] - P[i] \ge K$:
1. **Why pop from the front when $P[j] - P[dq[0]] \ge K$?**
   Once index $i = dq[0]$ forms a valid sum $\ge K$ with $j$, no future right endpoint $j' > j$ can ever give a **shorter** subarray with $i$ (since $j' - i > j - i$). So we record $j - i$ and `dq.popleft()`!
2. **Why pop from the rear when $P[j] \le P[dq[-1]]$?**
   If a later index $j$ has a smaller or equal prefix sum than an earlier index $i' = dq[-1]$, then for any future right endpoint $r > j$, $P[r] - P[j] \ge P[r] - P[i']$ **and** $r - j < r - i'$. Thus $j$ is strictly better than $i'$ in both sum and length, so $i'$ is popped from the rear!

---

## 5. Minimum 3 Examples

### Example 1: Sliding Window Maximum & Minimum in One $O(n)$ Pass (LeetCode 239)
File: [`example_01_sliding_window_maximum_and_minimum.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/F_Stacks_and_Queues/06_Monotonic_Queue/example_01_sliding_window_maximum_and_minimum.py)

```python
def sliding_window_max_and_min(nums: List[int], k: int) -> Tuple[List[int], List[int]]:
    if not nums or k <= 0 or k > len(nums):
        return [], []

    max_dq: Deque[int] = deque()  # Monotonic decreasing deque of indices
    min_dq: Deque[int] = deque()  # Monotonic increasing deque of indices
    max_results: List[int] = []
    min_results: List[int] = []

    for i, val in enumerate(nums):
        if max_dq and max_dq[0] <= i - k:
            max_dq.popleft()
        if min_dq and min_dq[0] <= i - k:
            min_dq.popleft()

        while max_dq and nums[max_dq[-1]] <= val:
            max_dq.pop()
        while min_dq and nums[min_dq[-1]] >= val:
            min_dq.pop()

        max_dq.append(i)
        min_dq.append(i)

        if i >= k - 1:
            max_results.append(nums[max_dq[0]])
            min_results.append(nums[min_dq[0]])

    return max_results, min_results
```

---

### Example 2: Longest Subarray With Absolute Diff $\le$ Limit (LeetCode 1438) & `MaxQueue`
File: [`example_02_longest_subarray_within_limit_and_max_queue.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/F_Stacks_and_Queues/06_Monotonic_Queue/example_02_longest_subarray_within_limit_and_max_queue.py)

```python
def longest_subarray_abs_diff_limit(nums: List[int], limit: int) -> Tuple[int, List[int]]:
    max_dq: Deque[int] = deque()
    min_dq: Deque[int] = deque()
    left = 0
    best_len = 0
    best_start = 0

    for right, val in enumerate(nums):
        while max_dq and nums[max_dq[-1]] < val:
            max_dq.pop()
        while min_dq and nums[min_dq[-1]] > val:
            min_dq.pop()
        max_dq.append(right)
        min_dq.append(right)

        while nums[max_dq[0]] - nums[min_dq[0]] > limit:
            if max_dq[0] == left:
                max_dq.popleft()
            if min_dq[0] == left:
                min_dq.popleft()
            left += 1

        curr_len = right - left + 1
        if curr_len > best_len:
            best_len = curr_len
            best_start = left

    return best_len, nums[best_start : best_start + best_len]
```

---

### Example 3: Shortest Subarray With Sum $\ge K$ (LeetCode 862 Hard) & Jump Game VI DP (LeetCode 1696)
File: [`example_03_shortest_subarray_at_least_k_and_dp_optimization.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/F_Stacks_and_Queues/06_Monotonic_Queue/example_03_shortest_subarray_at_least_k_and_dp_optimization.py)

```python
def shortest_subarray_at_least_k(nums: List[int], k: int) -> int:
    n = len(nums)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]

    best_len = n + 1
    dq: Deque[int] = deque()

    for j in range(n + 1):
        while dq and prefix[j] - prefix[dq[0]] >= k:
            best_len = min(best_len, j - dq.popleft())

        while dq and prefix[j] <= prefix[dq[-1]]:
            dq.pop()

        dq.append(j)

    return best_len if best_len <= n else -1
```

---

## 6. Output

### Output — Example 1 (`example_01_sliding_window_maximum_and_minimum.py`)
```text
========================================================================
Sliding Window Maximum & Minimum in O(n) Time (LeetCode 239)
========================================================================
Input Array : [1, 3, -1, -3, 5, 3, 6, 7], Window Size k = 3

  Window [0..2] = [1, 3, -1]      -> Max =  3, Min = -1
  Window [1..3] = [3, -1, -3]     -> Max =  3, Min = -3
  Window [2..4] = [-1, -3, 5]     -> Max =  5, Min = -3
  Window [3..5] = [-3, 5, 3]      -> Max =  5, Min = -3
  Window [4..6] = [5, 3, 6]       -> Max =  6, Min =  3
  Window [5..7] = [3, 6, 7]       -> Max =  7, Min =  3
```

### Output — Example 2 (`example_02_longest_subarray_within_limit_and_max_queue.py`)
```text
========================================================================
1. Longest Subarray With Absolute Diff <= Limit in O(n) (LeetCode 1438)
========================================================================
  nums=[8, 2, 4, 7]                , limit=4 -> max_len=2, subarray=[2, 4]
  nums=[10, 1, 2, 4, 7, 2]         , limit=5 -> max_len=4, subarray=[2, 4, 7, 2]
  nums=[4, 2, 2, 2, 4, 4, 2, 2]    , limit=0 -> max_len=3, subarray=[2, 2, 2]

========================================================================
2. MaxQueue — Amortized O(1) Enqueue, Dequeue, and GetMax
========================================================================
  enqueue(4) -> items=[4], get_max()=4
  enqueue(7) -> items=[4, 7], get_max()=7
  enqueue(2) -> items=[4, 7, 2], get_max()=7
  enqueue(7) -> items=[4, 7, 2, 7], get_max()=7
  enqueue(5) -> items=[4, 7, 2, 7, 5], get_max()=7
  dequeue() -> 4 | items=[7, 2, 7, 5], get_max()=7
  dequeue() -> 7 | items=[2, 7, 5], get_max()=7
  dequeue() -> 2 | items=[7, 5], get_max()=7
  dequeue() -> 7 | items=[5], get_max()=5
```

### Output — Example 3 (`example_03_shortest_subarray_at_least_k_and_dp_optimization.py`)
```text
========================================================================
1. Shortest Subarray With Sum >= K (with Negatives — LeetCode 862 Hard)
========================================================================
  nums=[2, -1, 2]                , k=3   -> Shortest Length = 3
  nums=[84, -37, 32, 40, 95]     , k=167 -> Shortest Length = 3
  nums=[1, 2]                    , k=4   -> Shortest Length = -1

========================================================================
2. Jump Game VI — Monotonic Queue DP Optimization in O(n) (LeetCode 1696)
========================================================================
  nums=[1, -1, -2, 4, -7, 3]     , k=2 -> Max DP Score = 7
  nums=[10, -5, -2, 4, 0, 3]     , k=3 -> Max DP Score = 17
```

---

## 7. Code Explanation

1. **Why Index Storage (`dq.append(i)`) vs Value Storage (`MaxQueue`) Matters:**
   - In index-based sliding windows (`sliding_window_max_and_min`), we store **indices** so we can check expiration via `dq[0] <= i - k`, and we can pop `<=` at the back because the newer index `i` outlives any older duplicate value.
   - In value-based `MaxQueue` (where `dequeue()` does not pass an index), we store **values** and must use strict `<` (`self._max_candidates[-1] < val`) so duplicate maximums (like the two `7`s in `[4, 7, 2, 7, 5]`) are both retained until each is dequeued!

---

## 8. Common Mistakes

1. **Recording `nums[dq[0]]` Before `i >= k - 1` in Fixed-Window Problems:**
   For the first $k - 1$ iterations ($i = 0 \dots k - 2$), the window has fewer than $k$ elements. Only append to the output list once $i \ge k - 1$.
2. **Storing Values Instead of Indices in Fixed-Size Sliding Window Maximum:**
   If you store values instead of indices and the array contains duplicates, it is easy to accidentally evict a newer duplicate when an older duplicate slides out of the window. Storing indices (`dq[0] <= i - k`) avoids all ambiguity.

---

## 9. Practice Questions

1. **Easy — Sliding Window Minimum:**
   Given an array `nums` and window size `k`, return the minimum of every contiguous subarray of size `k` in $O(n)$ time.
2. **Medium — Constrained Subsequence Sum (LeetCode 1425):**
   Given an integer array `nums` and an integer `k`, return the maximum sum of a non-empty subsequence of that array such that for every two consecutive integers in the subsequence `nums[i]` and `nums[j]` ($i < j$), $j - i \le k$ (note: if the best previous DP value is negative, you can start fresh at `nums[i]`, i.e., `dp[i] = nums[i] + max(0, dp[dq[0]])`).
3. **Hard — Maximum Number of Robots Within Budget (LeetCode 2398):**
   Combine a variable-size sliding window, running sum of `runningCosts`, and a Monotonic Decreasing Deque over `chargeTimes` to find the maximum number of consecutive robots whose total cost $\max(\text{chargeTimes}) + k \cdot \sum \text{runningCosts} \le \text{budget}$ in $O(n)$ time.

---

## 10. Interview Questions

### Q1: What is the difference between a Monotonic Stack and a Monotonic Queue?
**Answer:**
- A **Monotonic Stack** only adds and removes at the **top (rear)** — once an element enters the bottom of the stack, it stays until a future element dominates it. It solves unbounded lookahead/lookbehind problems (Next Greater Element, Histogram Area).
- A **Monotonic Queue** is a **Deque** that removes dominated elements from the **rear** AND evicts expired elements from the **front**. It solves **bounded-window** extremum problems (Sliding Window Maximum, Bounded-Range DP).

### Q2: How does a Monotonic Queue compare to a Max-Heap (`heapq`) for Sliding Window Maximum (LeetCode 239)?
**Answer:**
- A Max-Heap with lazy deletion takes **$O(n \log n)$** worst-case time and **$O(n)$** space (if the input is strictly increasing, expired elements accumulate inside the heap without ever reaching the top).
- A Monotonic Queue takes **strict $O(n)$ time** and **$O(k)$ space**!

### Q3: Why can't we use a standard two-pointer sliding window for Shortest Subarray With Sum $\ge K$ when negative numbers exist (LeetCode 862)?
**Answer:** A standard two-pointer window relies on the invariant that advancing `left` decreases the window sum and advancing `right` increases the window sum. When negative numbers exist, advancing `left` past a negative number actually **increases** the remaining subarray sum! Switching to prefix sums $P[j] - P[i] \ge K$ with a monotonic increasing deque restores $O(n)$ optimality.

