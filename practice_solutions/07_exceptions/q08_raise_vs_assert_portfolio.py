"""
Topic 07 - Exception Handling: Question 8
Problem: PortfolioEngine demonstrating Runtime Validation (raise) vs Internal Invariants (assert).
"""

import math
from typing import List, Union


class PortfolioEngine:
    """Demonstrates strict distinction between input validation (raise) and state invariants (assert)."""

    def distribute_capital(
        self,
        asset_weights: List[float],
        total_capital: Union[int, float]
    ) -> List[float]:
        """Distributes capital proportionally based on weights."""
        # 1. Runtime Input Validation (Production gates must NEVER rely on assert)
        if not isinstance(total_capital, (int, float)) or total_capital <= 0:
            raise ValueError("Capital must be a strictly positive number")

        if not asset_weights or any(not isinstance(w, (int, float)) or w < 0 for w in asset_weights):
            raise ValueError("Asset weights must be a non-empty list of non-negative floats")

        total_weight = sum(asset_weights)
        if math.isclose(total_weight, 0.0):
            raise ValueError("Sum of asset weights cannot be zero")

        # 2. Internal State Invariant Verification (Legitimate use of assert for internal logic checks)
        norm_weights = [w / total_weight for w in asset_weights]
        # Invariant 1: normalized weights must sum to 1.0 within float tolerance
        assert math.isclose(sum(norm_weights), 1.0, rel_tol=1e-7), (
            "Algorithm Error: Normalized weights do not sum to 1.0"
        )

        allocations = [round(w * total_capital, 2) for w in norm_weights]

        # Invariant 2: total distributed capital must match original input within rounding tolerance
        assert math.isclose(sum(allocations), total_capital, abs_tol=0.05), (
            "Invariant Breach: Allocations sum does not match total capital"
        )

        return allocations

    def explain_assertion_flag_security(self) -> str:
        """Explains why assert is dangerous for authentication and authorization."""
        return (
            "Security Audit on Assertions:\n"
            "Rule: `assert` is exclusively for verifying developer assumptions and impossible internal state invariants.\n"
            "Security warning: Running `python -O script.py` strips all assertions; "
            "runtime data validation and security access guards must always use explicit `if ...: raise`."
        )


# Verification & Execution
engine = PortfolioEngine()
weights = [0.4, 0.4, 0.2]
capital = 10000.0

allocations = engine.distribute_capital(weights, capital)
print(f"Allocated Capital: {allocations}")
print(f"Total Sum Verified: {sum(allocations)}")

# Validation input checks:
try:
    engine.distribute_capital([-0.5, 0.5], 1000.0)
except ValueError as err:
    print("Caught Input Error (Valid raise):", err)

print(f"\n{engine.explain_assertion_flag_security()}")
