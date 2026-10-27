"""
Topic 04 - Functions: Question 6
Problem: Divide-and-Conquer Logarithmic Exponentiation and Nested Tree Recursion.
"""

from typing import Any, Union


# 1. Logarithmic Exponentiation via Divide-and-Conquer
def power_recursive(base: float, exponent: int, depth: int = 0, max_depth: int = 50) -> float:
    """Computes base^exponent in O(log N) recursive steps with call-stack depth guard."""
    if depth > max_depth:
        raise RecursionError(f"Call-stack budget breached: exceeded max depth {max_depth}")

    if base == 0.0 and exponent < 0:
        raise ZeroDivisionError("Cannot raise zero to a negative power")

    if exponent == 0:
        return 1.0
    if exponent < 0:
        return 1.0 / power_recursive(base, -exponent, depth + 1, max_depth)

    if exponent % 2 == 0:
        half = power_recursive(base, exponent // 2, depth + 1, max_depth)
        return half * half
    else:
        return base * power_recursive(base, exponent - 1, depth + 1, max_depth)


# 2. Recursive Nested List Leaf Summation
def recursive_leaf_sum(data: Union[list, int, float], depth: int = 0, max_depth: int = 50) -> float:
    """Recursively traverses irregularly nested lists to sum numeric leaf values."""
    if depth > max_depth:
        raise RecursionError(f"Maximum traversal depth {max_depth} exceeded")

    if isinstance(data, (int, float)):
        return float(data)
    elif isinstance(data, list):
        return sum(recursive_leaf_sum(item, depth + 1, max_depth) for item in data)
    else:
        raise TypeError(f"Unsupported node type: {type(data).__name__}")


# Verification and Execution
base_val = 2.0
exp_val = 10
res_pow = power_recursive(base_val, exp_val)
print(f"{base_val}^{exp_val} via Logarithmic Recursion: {res_pow} (Computed in ~4 recursive subdivisions)")

neg_exp = -3
res_neg = power_recursive(base_val, neg_exp)
print(f"{base_val}^{neg_exp} via Logarithmic Recursion: {res_neg}")

nested_tree = [1, [2, [3, 4], 5], [[6, 7], 8], 9]
leaf_sum = int(recursive_leaf_sum(nested_tree))
print(f"Recursive Leaf Sum of Nested Tree: {leaf_sum}")

# 3. Recursion Safety Guard Test
try:
    # Trigger recursion guard with tight max_depth limit
    power_recursive(2.0, 1024, max_depth=5)
except RecursionError:
    print("Recursion Depth Guard: Handled safely within stack budget.")
