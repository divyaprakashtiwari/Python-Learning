"""
Question 10: Dynamic Programming Suite (Stairs, 0/1 Knapsack & Coin Change)
Topic: Data Structures & Algorithms (DSA)

Key Concepts Tested:
- Variable step climbing stairs via 1D tabulation
- 0/1 Knapsack with 2D DP table and item selection backtracking
- Coin Change: Minimum coin count (fewest coins) and total distinct combinations
- Boundary conditions and invalid input validation
"""

from typing import List, Tuple


def count_stair_ways(total_steps: int, allowed_steps: List[int]) -> int:
    """
    Computes distinct ways to climb total_steps using allowed_steps increments.
    Operates via 1D bottom-up tabulation.
    """
    if total_steps < 0:
        raise ValueError("Total steps cannot be negative")
    if total_steps == 0:
        return 1

    dp = [0] * (total_steps + 1)
    dp[0] = 1

    for i in range(1, total_steps + 1):
        dp[i] = sum(dp[i - step] for step in allowed_steps if i >= step)

    return dp[total_steps]


def knapsack_01(weights: List[int], values: List[int], max_weight: int) -> Tuple[int, List[int]]:
    """
    Solves the 0/1 Knapsack problem using a 2D dynamic programming table.
    Backtracks through the table to reconstruct the indices of selected items.
    Returns (maximum_value, selected_indices).
    """
    if max_weight < 0:
        raise ValueError("Capacity cannot be negative")

    n = len(weights)
    if n == 0 or max_weight == 0:
        return (0, [])

    # dp[i][w] stores maximum value achievable using a subset of the first i items with capacity w
    dp = [[0] * (max_weight + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w_i = weights[i - 1]
        v_i = values[i - 1]
        for w in range(max_weight + 1):
            if w_i <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - w_i] + v_i)
            else:
                dp[i][w] = dp[i - 1][w]

    # Backtracking to reconstruct selected items
    selected_indices: List[int] = []
    w_remaining = max_weight
    for i in range(n, 0, -1):
        if dp[i][w_remaining] != dp[i - 1][w_remaining]:
            selected_indices.append(i - 1)
            w_remaining -= weights[i - 1]

    selected_indices.reverse()
    return (dp[n][max_weight], selected_indices)


def coin_change_min(coins: List[int], target_amount: int) -> int:
    """
    Calculates the minimum number of coins needed to make target_amount.
    Returns -1 if the amount cannot be formed.
    """
    if target_amount < 0:
        raise ValueError("Target amount cannot be negative")
    if target_amount == 0:
        return 0

    dp = [float("inf")] * (target_amount + 1)
    dp[0] = 0

    for i in range(1, target_amount + 1):
        for coin in coins:
            if i >= coin and dp[i - coin] != float("inf"):
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return int(dp[target_amount]) if dp[target_amount] != float("inf") else -1


def coin_change_ways(coins: List[int], target_amount: int) -> int:
    """
    Calculates the number of distinct combinations of coins that sum to target_amount.
    Outer-loops over coin denominations to ensure combinations (not permutations) are counted.
    """
    if target_amount < 0:
        raise ValueError("Target amount cannot be negative")
    if target_amount == 0:
        return 1

    dp = [0] * (target_amount + 1)
    dp[0] = 1

    for coin in coins:
        for amount in range(coin, target_amount + 1):
            dp[amount] += dp[amount - coin]

    return dp[target_amount]


if __name__ == "__main__":
    print("=== 1. Variable Step Climbing Stairs ===")
    ways = count_stair_ways(total_steps=5, allowed_steps=[1, 2, 3])
    print(f"Climbing Stairs Ways to reach 5 steps: {ways}")

    print("\n=== 2. 0/1 Knapsack with Backtracking ===")
    item_weights = [2, 3, 4, 5]
    item_values = [3, 4, 5, 8]

    # For capacity 8: optimal items are [1, 3] (weight 3 + 5 = 8, value 4 + 8 = 12)
    max_val_8, selected_8 = knapsack_01(item_weights, item_values, max_weight=8)
    print(f"Knapsack Maximum Value for Capacity 8: {max_val_8}")
    print(f"Knapsack Selected Item Indices: {selected_8} (Item 1: weight {item_weights[1]} val {item_values[1]}; Item 3: weight {item_weights[3]} val {item_values[3]})")

    # For capacity 7: optimal items are [0, 3] (weight 2 + 5 = 7, value 3 + 8 = 11)
    max_val_7, selected_7 = knapsack_01(item_weights, item_values, max_weight=7)
    print(f"Knapsack Maximum Value for Capacity 7: {max_val_7} with items: {selected_7}")

    print("\n=== 3. Coin Change Problems ===")
    coins = [1, 2, 5]
    min_coins_res = coin_change_min(coins, target_amount=11)
    ways_res = coin_change_ways(coins, target_amount=5)

    print(f"Minimum Coins to Make 11: {min_coins_res} (5 + 5 + 1)")
    print(f"Total Distinct Ways to Make 5 with {coins}: {ways_res} ([5], [2, 2, 1], [2, 1, 1, 1], [1, 1, 1, 1, 1])")

    print("\n=== 4. Edge Cases ===")
    print(f"Zero coins needed for amount 0: {coin_change_min(coins, 0)}")
    print(f"1 way to make amount 0: {coin_change_ways(coins, 0)}")
    print(f"Unreachable coin amount: {coin_change_min([2, 4], 7)}")

    try:
        coin_change_min(coins, -5)
    except ValueError as err:
        print(f"Caught negative amount validation: {err}")
