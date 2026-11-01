# DSA Problem-Solving Pattern Guide (`DSA_PATTERN_GUIDE.md`)

Instead of memorizing hundreds of isolated problems, master these **14 core algorithmic patterns** to recognize and solve unseen coding interview questions systematically.

---

## Pattern Recognition Decision Table

| If the problem asks for... | Clues in Problem Statement | Primary Pattern | Time Complexity Target |
| :--- | :--- | :--- | :--- |
| Pair/Triplet sum or palindrome in sorted array | "Sorted array", "pair with target sum", "in-place" | **Two Pointers** | `O(n)` |
| Longest/shortest contiguous subarray or substring | "Contiguous subarray", "window of size k", "at most k distinct" | **Sliding Window** | `O(n)` |
| Range sum queries or subarray sum equals `K` | "Sum from index `L` to `R`", "number of subarrays with sum `K`" | **Prefix Sum + Hash Map** | `O(n)` |
| Search in sorted/rotated array or min-max optimization | "Sorted", "rotated", "minimize the maximum" | **Binary Search** | `O(log n)` |
| Linked list middle, cycle detection, or `k`-th from end | "Linked list", "O(1) space", "cycle" | **Fast & Slow Pointers** | `O(n)` |
| Next greater/smaller element or histogram area | "Next greater element", "daily temperatures", "span" | **Monotonic Stack** | `O(n)` |
| Top `K` frequent/largest/smallest or streaming median | "K largest", "k-th smallest", "merge K sorted" | **Heap / Priority Queue** | `O(n log k)` |
| Shortest path in unweighted graph or level-by-level tree | "Minimum steps", "level order", "grid shortest path" | **Breadth-First Search (BFS)** | `O(V + E)` |
| Connected components, maze exploration, or cycle check | "Number of islands", "path exists", "all paths" | **Depth-First Search (DFS)** | `O(V + E)` |
| Course prerequisites or task ordering with dependencies | "Prerequisites", "directed acyclic graph", "build order" | **Topological Sort** | `O(V + E)` |
| Generate all subsets, permutations, or constraint boards | "All possible combinations", "Sudoku", "N-Queens" | **Backtracking** | Exponential |
| Merging overlapping intervals or meeting rooms | "Intervals `[start, end]`", "overlap", "minimum rooms" | **Greedy + Interval Sorting** | `O(n log n)` |
| Count ways, min/max cost with overlapping subproblems | "Maximum profit", "minimum coins", "longest subsequence" | **Dynamic Programming** | `O(n * m)` or `O(n)` |
| Single non-repeating number or subset bitmasks | "Every element appears twice except one", `O(1)` space | **Bit Manipulation (XOR)** | `O(n)` |

---

## Core Pattern Templates

### 1. Two Pointers (Opposite Ends)
```python
def two_sum_sorted(nums: list[int], target: int) -> tuple[int, int] | None:
    left, right = 0, len(nums) - 1
    while left < right:
        current_sum = nums[left] + nums[right]
        if current_sum == target:
            return (left, right)
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return None
```

### 2. Variable-Size Sliding Window
```python
def longest_unique_substring(s: str) -> int:
    seen: dict[str, int] = {}
    left = 0
    max_len = 0
    for right, char in enumerate(s):
        if char in seen and seen[char] >= left:
            left = seen[char] + 1
        seen[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len
```

### 3. Binary Search on Answer
```python
def binary_search_on_answer(low: int, high: int, is_feasible) -> int:
    ans = high
    while low <= high:
        mid = low + (high - low) // 2
        if is_feasible(mid):
            ans = mid
            high = mid - 1  # Try to find a smaller valid answer
        else:
            low = mid + 1
    return ans
```

### 4. Monotonic Stack (Next Greater Element)
```python
def next_greater_elements(nums: list[int]) -> list[int]:
    result = [-1] * len(nums)
    stack: list[int] = []  # Stores indices whose next greater element isn't found yet
    for i, val in enumerate(nums):
        while stack and nums[stack[-1]] < val:
            prev_index = stack.pop()
            result[prev_index] = val
        stack.append(i)
    return result
```
