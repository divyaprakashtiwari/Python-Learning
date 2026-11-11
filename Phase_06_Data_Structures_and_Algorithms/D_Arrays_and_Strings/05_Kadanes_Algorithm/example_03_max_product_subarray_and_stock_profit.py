"""
Phase 6 - Data Structures and Algorithms
Section D: Arrays and Strings - Topic 05: Kadane's Algorithm
Example 03: Maximum Product Subarray (Tracking Max & Min for Negative Sign Flips) & Stock Profit

Demonstrates:
1. Maximum Product Subarray (LeetCode 152):
   Why standard Kadane fails on products: a huge NEGATIVE product multiplied by another
   NEGATIVE number suddenly flips into a huge POSITIVE product!
   Fix: Track BOTH `curr_max_prod` and `curr_min_prod` at every step, swapping them whenever
   `nums[i] < 0`!
2. Best Time to Buy and Sell Stock (LeetCode 121) as Kadane's Algorithm on daily price differences!
"""


def max_product_subarray(nums: list[int]) -> int:
    """
    Find the contiguous non-empty subarray with the largest product in O(N) time and O(1) space.
    Tracks both `curr_max` and `curr_min` because multiplying by a negative number flips
    the smallest negative product into the largest positive product!
    """
    if not nums:
        raise ValueError("Array must not be empty")

    curr_max = nums[0]
    curr_min = nums[0]
    best_prod = nums[0]

    for i in range(1, len(nums)):
        x = nums[i]
        # Multiplying by a negative number flips max and min!
        if x < 0:
            curr_max, curr_min = curr_min, curr_max

        curr_max = max(x, curr_max * x)
        curr_min = min(x, curr_min * x)
        best_prod = max(best_prod, curr_max)

    return best_prod


def max_stock_profit_kadane(prices: list[int]) -> tuple[int, int, int]:
    """
    Best Time to Buy and Sell Stock (Single Transaction, LeetCode 121):
    Notice that `prices[sell] - prices[buy]` equals the sum of daily price changes
    `diff[buy + 1] + diff[buy + 2] + ... + diff[sell]`, which is literally Kadane's Algorithm
    clamped at `0`!
    Returns (max_profit, buy_day, sell_day).
    """
    if len(prices) < 2:
        return 0, 0, 0

    min_price_day = 0
    max_profit = 0
    best_buy = 0
    best_sell = 0

    for day in range(1, len(prices)):
        if prices[day] < prices[min_price_day]:
            min_price_day = day
        else:
            profit = prices[day] - prices[min_price_day]
            if profit > max_profit:
                max_profit = profit
                best_buy = min_price_day
                best_sell = day

    return max_profit, best_buy, best_sell


if __name__ == "__main__":
    print("=" * 72)
    print("1. MAXIMUM PRODUCT SUBARRAY (TRACKING MAX & MIN FOR SIGN FLIPS)")
    print("=" * 72)
    for sample in [[2, 3, -2, 4], [-2, 0, -1], [-2, 3, -4], [2, -5, -2, -4, 3]]:
        print(f"  Array: {str(sample):<22} -> Max Product Subarray: {max_product_subarray(sample)}")

    print("\n" + "=" * 72)
    print("2. BEST TIME TO BUY & SELL STOCK (KADANE ON PRICE DELTAS)")
    print("=" * 72)
    stock_prices = [7, 1, 5, 3, 6, 4]
    profit, b_day, s_day = max_stock_profit_kadane(stock_prices)
    print(f"Stock Prices : {stock_prices}")
    print(
        f"Max Profit   : {profit} (Buy on Day {b_day} at {stock_prices[b_day]}, "
        f"Sell on Day {s_day} at {stock_prices[s_day]})"
    )
