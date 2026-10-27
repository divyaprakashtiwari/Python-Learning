"""
Topic 03 - Data Structures: Question 10
Problem: Financial Trading Order Book Engine using Multi-key Timsort & Bisect module.
"""

import bisect
from typing import List, Tuple

# Orders: (order_id, client_id, side, price, timestamp_ms)
OrderTuple = Tuple[str, str, str, float, int]

orders: List[OrderTuple] = [
    ("ord_1", "client_A", "BID", 150.25, 1002),
    ("ord_2", "client_B", "BID", 151.00, 1000),
    ("ord_3", "client_C", "BID", 150.25, 1001),
    ("ord_4", "client_D", "ASK", 151.50, 1005),
    ("ord_5", "client_E", "ASK", 151.20, 1003),
    ("ord_6", "client_F", "ASK", 151.20, 1001)
]

# 1. Multi-Criteria Order Book Priority Sorting
# Separate into BIDs and ASKs
bids = [o for o in orders if o[2] == "BID"]
asks = [o for o in orders if o[2] == "ASK"]

# BIDs: Highest Price first (-price), Earliest timestamp (+time)
sorted_bids = sorted(bids, key=lambda x: (-x[3], x[4]))

# ASKs: Lowest Price first (+price), Earliest timestamp (+time)
sorted_asks = sorted(asks, key=lambda x: (x[3], x[4]))

print("Prioritized BID Book (Price DESC, Time ASC):")
for idx, o in enumerate(sorted_bids, 1):
    print(f"{idx}. {o[0]}: ${o[3]:.2f} (Time: {o[4]})")

print("\nPrioritized ASK Book (Price ASC, Time ASC):")
for idx, o in enumerate(sorted_asks, 1):
    print(f"{idx}. {o[0]}: ${o[3]:.2f} (Time: {o[4]})")

# 2. Efficient Real-Time Order Insertion with bisect
# Extract sorted ascending unique price levels
bid_price_levels = sorted(list({o[3] for o in bids}))
new_bid_quote = 150.75

idx_insert = bisect.bisect_left(bid_price_levels, new_bid_quote)
bisect.insort(bid_price_levels, new_bid_quote)

print("\nBinary Search Insertion:")
print(f"- Inserting Quote {new_bid_quote:.2f} into BIDs: Inserted at index {idx_insert}")
print(f"- Updated Price Levels: {[round(p, 2) for p in bid_price_levels]}")


# 3. Nearest Price Level Query in O(log N)
def find_closest_level(sorted_levels: List[float], target_price: float) -> float:
    """Finds the price level closest to target_price in logarithmic time."""
    if not sorted_levels:
        raise ValueError("Price levels list cannot be empty")
    idx = bisect.bisect_left(sorted_levels, target_price)
    if idx == 0:
        return sorted_levels[0]
    if idx == len(sorted_levels):
        return sorted_levels[-1]
    before = sorted_levels[idx - 1]
    after = sorted_levels[idx]
    return after if (after - target_price) < (target_price - before) else before


query_target = 150.80
closest = find_closest_level(bid_price_levels, query_target)
print(f"Nearest Price Level to {query_target:.2f}: {closest:.2f}")
