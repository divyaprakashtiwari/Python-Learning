"""
Topic 08 - Modules and Packages: Question 8
Problem: Functional Toolbox using functools (lru_cache, partial, reduce, wraps, singledispatch).
"""

from functools import lru_cache, partial, reduce, singledispatch, wraps
from typing import Any, Callable, Dict, List


# 1. Memoized Lucas Number Generator
@lru_cache(maxsize=128)
def compute_lucas_number(n: int) -> int:
    """Computes n-th Lucas number recursively with LRU caching."""
    if n == 0:
        return 2
    if n == 1:
        return 1
    return compute_lucas_number(n - 1) + compute_lucas_number(n - 2)


# 2. General Billing Calculator & Partials
def calculate_final_bill(
    amount: float,
    discount_ratio: float,
    tax_ratio: float,
    currency_symbol: str = "$"
) -> str:
    """Computes final billing amount after discount and applicable tax."""
    discounted = amount * (1.0 - discount_ratio)
    total = discounted * (1.0 + tax_ratio)
    return f"{currency_symbol}{total:.2f}"


# Frozen partials
standard_us_retail_bill = partial(
    calculate_final_bill,
    discount_ratio=0.10,
    tax_ratio=0.08,
    currency_symbol="$"
)
black_friday_vip_bill = partial(
    calculate_final_bill,
    discount_ratio=0.40,
    tax_ratio=0.08,
    currency_symbol="$"
)


# 3. Compound Growth via reduce
def aggregate_compound_growth(rates: List[float], starting_principal: float = 1.0) -> float:
    """Computes compounded yield using functools.reduce."""
    return reduce(lambda acc, r: acc * (1.0 + r), rates, starting_principal)


# 4. Custom Decorator preserving metadata via @wraps
def audit_execution(action_name: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)
        return wrapper
    return decorator


# 5. Polymorphic Function Overloading via @singledispatch
@singledispatch
def serialize_payload(data: Any) -> str:
    """Default fallback serializer."""
    return f"UNKNOWN_TYPE<{type(data).__name__}>: {data}"


@serialize_payload.register(int)
def _(data: int) -> str:
    return f"INT[{data}] (Hex: {hex(data)} | Bin: {bin(data)})"


@serialize_payload.register(list)
def _(data: list) -> str:
    elements = ", ".join(str(x) for x in data)
    return f"LIST[{elements}]"


@serialize_payload.register(dict)
def _(data: dict) -> str:
    pairs = ", ".join(f"{k}={v}" for k, v in sorted(data.items()))
    return f"DICT[{pairs}]"


# Verification & Execution
l10 = compute_lucas_number(10)
l10_cached = compute_lucas_number(10)  # Cache hit
cache_stats = compute_lucas_number.cache_info()

print(f"Lucas(10): {l10}")
print(f"Cache Info: {cache_stats}")

bill1 = standard_us_retail_bill(100.0)
bill2 = black_friday_vip_bill(100.0)
print(f"Standard Bill ($100.00 base): {bill1}")
print(f"Black Friday Bill ($100.00 base): {bill2}")

s_int = serialize_payload(42)
s_list = serialize_payload(["alpha", "beta"])
s_dict = serialize_payload({"env": "prod", "retries": 3})

print("\nSingleDispatch Outputs:")
print(f"- Int: {s_int}")
print(f"- List: {s_list}")
print(f"- Dict: {s_dict}")
