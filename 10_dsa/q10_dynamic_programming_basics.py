"""
Topic: Data Structures and Algorithms (DSA) - Dynamic Programming Basics
-----------------------------------------------------------------------
Questions Covered:
1. Climbing Stairs / Fibonacci: Memoization (top-down), Tabulation (bottom-up), and O(1) space.
2. 0/1 Knapsack Problem: Classical 2D and 1D space-optimized bounded knapsack value maximization.
3. Coin Change (Fewest Coins): Unbounded knapsack finding minimum coin count to form amount.
4. Longest Increasing Subsequence (LIS): O(n^2) DP and O(n log n) patience sorting via binary search.
5. Longest Common Subsequence (LCS): 2D grid DP with full string subsequence reconstruction.
6. Edit Distance (Levenshtein Distance): String transformation via insert, delete, and replace.
7. House Robber (Maximum Non-Adjacent Sum): Optimization under adjacency constraints.
8. Unique Paths in Grid with Obstacles: 2D dynamic grid paths under blockage constraints.
9. Maximum Subarray Sum (Kadane's Algorithm): Local vs global maximum tracking with indices.
10. Architectural System: Bounded Resource Allocation & Multi-Project Portfolio Optimizer.
"""

import bisect
from typing import List, Tuple, Optional, Any, Dict


# ==============================================================================
# Question 1: Climbing Stairs / Fibonacci (Top-Down, Bottom-Up, O(1) Space)
# ==============================================================================
def climb_stairs_memo(n: int, memo: Optional[Dict[int, int]] = None) -> int:
    """Top-down recursive memoization for number of distinct ways to climb n steps (1 or 2 steps)."""
    if memo is None:
        memo = {}
    if n <= 2:
        return max(1, n)
    if n in memo:
        return memo[n]
    memo[n] = climb_stairs_memo(n - 1, memo) + climb_stairs_memo(n - 2, memo)
    return memo[n]


def climb_stairs_tabulation(n: int) -> int:
    """Bottom-up 1D DP table."""
    if n <= 2:
        return max(1, n)
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


def climb_stairs_optimized(n: int) -> int:
    """Space-optimized O(1) memory two-variable accumulator."""
    if n <= 2:
        return max(1, n)
    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr
    return prev1


def test_q1_climbing_stairs():
    for steps in [1, 2, 3, 5, 10]:
        r_memo = climb_stairs_memo(steps)
        r_tab = climb_stairs_tabulation(steps)
        r_opt = climb_stairs_optimized(steps)
        assert r_memo == r_tab == r_opt

    # For n=5: ways = 8 (11111, 1112, 1121, 1211, 2111, 122, 212, 221)
    assert climb_stairs_optimized(5) == 8
    print("=== Q1: Climbing Stairs (Memo, Tabulation, O(1) Space) Verified ===")


# ==============================================================================
# Question 2: 0/1 Knapsack Problem (2D DP and 1D Space Optimization)
# ==============================================================================
def knapsack_01(weights: List[int], values: List[int], capacity: int) -> Tuple[int, List[int]]:
    """
    Solves 0/1 Knapsack problem.
    Returns (max_value, list_of_selected_item_indices).
    """
    n = len(weights)
    # dp[i][w]: max value considering first i items with weight capacity w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        wt = weights[i - 1]
        val = values[i - 1]
        for w in range(capacity + 1):
            # Exclude item i - 1
            dp[i][w] = dp[i - 1][w]
            # Include item i - 1 if capacity permits
            if w >= wt:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - wt] + val)

    # Reconstruct selected item indices
    selected_indices = []
    rem_capacity = capacity
    for i in range(n, 0, -1):
        if dp[i][rem_capacity] != dp[i - 1][rem_capacity]:
            selected_indices.append(i - 1)
            rem_capacity -= weights[i - 1]

    return dp[n][capacity], selected_indices[::-1]


def test_q2_knapsack_01():
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 5
    # Best choice: items 0 (wt 2, val 3) + item 1 (wt 3, val 4) -> total wt 5, total val 7
    max_val, items = knapsack_01(weights, values, capacity)
    assert max_val == 7
    assert items == [0, 1]
    print("=== Q2: 0/1 Knapsack Problem with Item Reconstruction Verified ===")


# ==============================================================================
# Question 3: Coin Change Problem (Fewest Coins)
# ==============================================================================
def coin_change(coins: List[int], amount: int) -> int:
    """
    Computes fewest number of coins needed to make up amount (unbounded coin usage).
    Returns -1 if amount cannot be made.
    """
    if amount == 0:
        return 0

    # dp[i] represents minimum coins needed for amount i
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for c in coins:
            if i >= c and dp[i - c] != float("inf"):
                dp[i] = min(dp[i], dp[i - c] + 1)

    return int(dp[amount]) if dp[amount] != float("inf") else -1


def test_q3_coin_change():
    # 11 with [1, 2, 5]: 5 + 5 + 1 -> 3 coins
    assert coin_change([1, 2, 5], 11) == 3
    # 3 with [2]: impossible -> -1
    assert coin_change([2], 3) == -1
    assert coin_change([1], 0) == 0
    print("=== Q3: Coin Change Problem (Fewest Coins) Verified ===")


# ==============================================================================
# Question 4: Longest Increasing Subsequence (LIS) in O(n^2) and O(n log n)
# ==============================================================================
def length_of_lis_dp(nums: List[int]) -> int:
    """O(n^2) Dynamic Programming formulation."""
    if not nums:
        return 0
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


def length_of_lis_binary_search(nums: List[int]) -> int:
    """O(n log n) Patience Sorting binary search formulation."""
    tails: List[int] = []
    for num in nums:
        idx = bisect.bisect_left(tails, num)
        if idx == len(tails):
            tails.append(num)
        else:
            tails[idx] = num
    return len(tails)


def test_q4_longest_increasing_subsequence():
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    # LIS is [2, 3, 7, 101] or [2, 5, 7, 18] -> length 4
    assert length_of_lis_dp(nums) == 4
    assert length_of_lis_binary_search(nums) == 4

    all_same = [7, 7, 7, 7]
    assert length_of_lis_binary_search(all_same) == 1
    print("=== Q4: Longest Increasing Subsequence (LIS) in O(n log n) Verified ===")


# ==============================================================================
# Question 5: Longest Common Subsequence (LCS) with Full String Reconstruction
# ==============================================================================
def longest_common_subsequence(text1: str, text2: str) -> Tuple[int, str]:
    """
    Computes length and full string of the Longest Common Subsequence.
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Reconstruct string
    lcs_chars = []
    i, j = m, n
    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            lcs_chars.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return dp[m][n], "".join(lcs_chars[::-1])


def test_q5_longest_common_subsequence():
    l_len, l_str = longest_common_subsequence("abcde", "ace")
    assert l_len == 3
    assert l_str == "ace"

    l_len2, l_str2 = longest_common_subsequence("abc", "def")
    assert l_len2 == 0
    assert l_str2 == ""
    print("=== Q5: Longest Common Subsequence (LCS) Verified ===")


# ==============================================================================
# Question 6: Edit Distance (Levenshtein Distance)
# ==============================================================================
def min_edit_distance(word1: str, word2: str) -> int:
    """
    Computes minimum operations (insert, delete, replace) to convert word1 to word2.
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Deletion
                    dp[i][j - 1],      # Insertion
                    dp[i - 1][j - 1],  # Replacement
                )

    return dp[m][n]


def test_q6_edit_distance():
    # horse -> rorse (replace h->r) -> rose (remove r) -> ros (remove e) = 3 ops
    assert min_edit_distance("horse", "ros") == 3
    # intention -> execution = 5 ops
    assert min_edit_distance("intention", "execution") == 5
    assert min_edit_distance("", "hello") == 5
    print("=== Q6: Edit Distance (Levenshtein Distance) Verified ===")


# ==============================================================================
# Question 7: House Robber (Maximum Non-Adjacent Sum)
# ==============================================================================
def house_robber(nums: List[int]) -> int:
    """
    Computes max loot possible without robbing two adjacent houses.
    Runs in O(n) time and O(1) space.
    """
    if not nums:
        return 0
    rob_prev = 0
    not_rob_prev = 0

    for n in nums:
        new_rob = not_rob_prev + n
        new_not_rob = max(rob_prev, not_rob_prev)
        rob_prev, not_rob_prev = new_rob, new_not_rob

    return max(rob_prev, not_rob_prev)


def test_q7_house_robber():
    # [1, 2, 3, 1] -> rob house 1 (val 1) + house 3 (val 3) = 4
    assert house_robber([1, 2, 3, 1]) == 4
    # [2, 7, 9, 3, 1] -> 2 + 9 + 1 = 12
    assert house_robber([2, 7, 9, 3, 1]) == 12
    assert house_robber([]) == 0
    print("=== Q7: House Robber (Maximum Non-Adjacent Sum) Verified ===")


# ==============================================================================
# Question 8: Unique Paths in Grid with Obstacles
# ==============================================================================
def unique_paths_with_obstacles(obstacle_grid: List[List[int]]) -> int:
    """
    Calculates unique paths from top-left to bottom-right moving only right or down.
    1 represents an obstacle, 0 represents open path.
    """
    if not obstacle_grid or obstacle_grid[0][0] == 1:
        return 0

    m = len(obstacle_grid)
    n = len(obstacle_grid[0])
    dp = [0] * n
    dp[0] = 1

    for r in range(m):
        for c in range(n):
            if obstacle_grid[r][c] == 1:
                dp[c] = 0
            elif c > 0:
                dp[c] += dp[c - 1]

    return dp[n - 1]


def test_q8_unique_paths_with_obstacles():
    grid = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0],
    ]
    # Paths around center obstacle = 2
    assert unique_paths_with_obstacles(grid) == 2

    blocked_start = [[1, 0]]
    assert unique_paths_with_obstacles(blocked_start) == 0
    print("=== Q8: Unique Paths in Grid with Obstacles Verified ===")


# ==============================================================================
# Question 9: Maximum Subarray Sum (Kadane's Algorithm)
# ==============================================================================
def max_subarray_kadane(nums: List[int]) -> Tuple[int, int, int]:
    """
    Finds contiguous subarray with the largest sum.
    Returns (max_sum, start_index, end_index).
    Time Complexity: O(n), Space Complexity: O(1).
    """
    if not nums:
        raise ValueError("nums cannot be empty")

    max_so_far = nums[0]
    curr_max = nums[0]
    start = end = 0
    temp_start = 0

    for i in range(1, len(nums)):
        if nums[i] > curr_max + nums[i]:
            curr_max = nums[i]
            temp_start = i
        else:
            curr_max += nums[i]

        if curr_max > max_so_far:
            max_so_far = curr_max
            start = temp_start
            end = i

    return max_so_far, start, end


def test_q9_kadane():
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    # Subarray [4, -1, 2, 1] has max sum = 6 from index 3 to 6
    max_sum, start, end = max_subarray_kadane(nums)
    assert max_sum == 6
    assert start == 3
    assert end == 6
    assert nums[start : end + 1] == [4, -1, 2, 1]
    print("=== Q9: Maximum Subarray Sum (Kadane's Algorithm) Verified ===")


# ==============================================================================
# Question 10: Architectural Multi-Project Resource Allocation Engine
# ==============================================================================
class ProjectProposal:
    def __init__(self, name: str, cost: int, expected_roi: float):
        self.name = name
        self.cost = cost
        self.expected_roi = expected_roi


class ResourceAllocationOptimizer:
    """
    Production portfolio optimizer allocating a discrete budget across projects
    to maximize overall ROI using bounded dynamic programming with full plan reconstruction.
    """
    @staticmethod
    def optimize_portfolio(
        proposals: List[ProjectProposal], total_budget: int
    ) -> Dict[str, Any]:
        n = len(proposals)
        # dp[i][b]: max ROI with first i proposals and b budget
        dp = [[0.0] * (total_budget + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            cost = proposals[i - 1].cost
            roi = proposals[i - 1].expected_roi
            for b in range(total_budget + 1):
                dp[i][b] = dp[i - 1][b]
                if b >= cost:
                    dp[i][b] = max(dp[i][b], dp[i - 1][b - cost] + roi)

        # Backtrack selections
        selected: List[ProjectProposal] = []
        rem_budget = total_budget
        for i in range(n, 0, -1):
            if dp[i][rem_budget] != dp[i - 1][rem_budget]:
                p = proposals[i - 1]
                selected.append(p)
                rem_budget -= p.cost

        selected_reversed = selected[::-1]
        used_budget = sum(p.cost for p in selected_reversed)
        total_roi = round(dp[n][total_budget], 2)

        return {
            "max_roi": total_roi,
            "budget_spent": used_budget,
            "budget_remaining": total_budget - used_budget,
            "selected_projects": [p.name for p in selected_reversed],
        }


def test_q10_resource_allocation_optimizer():
    portfolio = [
        ProjectProposal("Cloud Migration", cost=30, expected_roi=45.0),
        ProjectProposal("AI Analytics", cost=20, expected_roi=35.0),
        ProjectProposal("Security Hardening", cost=15, expected_roi=20.0),
        ProjectProposal("Mobile App", cost=25, expected_roi=30.0),
    ]
    # Total budget = 50
    # Optimal: Cloud Migration (30) + AI Analytics (20) -> cost 50, ROI 80.0
    res = ResourceAllocationOptimizer.optimize_portfolio(portfolio, total_budget=50)
    assert res["max_roi"] == 80.0
    assert res["budget_spent"] == 50
    assert res["budget_remaining"] == 0
    assert set(res["selected_projects"]) == {"Cloud Migration", "AI Analytics"}
    print("=== Q10: Architectural Resource Allocation Portfolio Optimizer Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_climbing_stairs()
    test_q2_knapsack_01()
    test_q3_coin_change()
    test_q4_longest_increasing_subsequence()
    test_q5_longest_common_subsequence()
    test_q6_edit_distance()
    test_q7_house_robber()
    test_q8_unique_paths_with_obstacles()
    test_q9_kadane()
    test_q10_resource_allocation_optimizer()
    print("\nAll 10 dynamic programming DSA questions passed successfully!")
