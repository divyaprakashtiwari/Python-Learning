"""
Topic 04 - Functions: Question 8
Problem: API Token Bucket Rate Limiter using Closures, nonlocal, and cell introspection.
"""

from typing import Callable, Tuple


def create_rate_limiter(max_tokens: int, refill_rate_per_sec: float) -> Callable[..., Tuple[bool, float]]:
    """Factory creating an in-memory token bucket rate limiter via lexical closure."""
    current_tokens: float = float(max_tokens)
    last_update_ts: float = 0.0
    max_capacity: int = max_tokens
    refill_rate: float = refill_rate_per_sec

    def consume(cost: int = 1, current_ts: float = 0.0) -> Tuple[bool, float]:
        nonlocal current_tokens, last_update_ts

        elapsed = max(0.0, current_ts - last_update_ts)
        current_tokens = min(float(max_capacity), current_tokens + elapsed * refill_rate)
        last_update_ts = current_ts

        if current_tokens >= cost:
            current_tokens -= cost
            return True, current_tokens
        else:
            return False, current_tokens

    return consume


# Verification & Timeline Simulation
free_tier = create_rate_limiter(max_tokens=2, refill_rate_per_sec=1.0)
premium_tier = create_rate_limiter(max_tokens=5, refill_rate_per_sec=5.0)

# T=0.0s
allowed1, rem1 = free_tier(1, current_ts=0.0)
print(f"Free Tier T=0.0s (Req 1): Allowed={allowed1} (Tokens Remaining: {rem1:.1f})")

allowed2, rem2 = free_tier(1, current_ts=0.0)
print(f"Free Tier T=0.0s (Req 2): Allowed={allowed2} (Tokens Remaining: {rem2:.1f})")

allowed3, rem3 = free_tier(1, current_ts=0.0)
print(f"Free Tier T=0.0s (Req 3): Allowed={allowed3} (Rate Limit Exceeded)")

# T=1.5s (Refills 1.5 tokens)
allowed4, rem4 = free_tier(1, current_ts=1.5)
print(f"Free Tier T=1.5s (Req 4): Allowed={allowed4} (Refilled and Granted)")

# Premium tier remains isolated
prem_allowed, prem_rem = premium_tier(1, current_ts=1.5)
print(f"Premium Tier T=1.5s: Allowed={prem_allowed} (Unimpacted, Remaining: {prem_rem:.1f})")

# 2. Closure Introspection via __closure__
print("\nClosure Cells Introspected:")
free_vars = free_tier.__code__.co_freevars
closure_cells = free_tier.__closure__
if closure_cells:
    for var_name, cell in zip(free_vars, closure_cells):
        val = cell.cell_contents
        if isinstance(val, float):
            print(f"- Bound {var_name}: ~{val:.1f}")
        else:
            print(f"- Bound {var_name}: {val}")
