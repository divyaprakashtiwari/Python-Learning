"""
Phase 3 - Topic 06: *args and **kwargs
Example 03: Transparent Argument Forwarding (`*args, **kwargs`) in Wrapper Functions

Demonstrates:
  - Writing a generic telemetry/retry/logging wrapper that accepts `(*args, **kwargs)`
  - Forwarding all positional and keyword arguments unchanged to the target function
"""

from typing import Any, Callable


def call_with_telemetry(
    func: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Log the function call signature, forward `*args, **kwargs`, and return result."""
    pos_repr = [repr(a) for a in args]
    kw_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
    all_args_str = ", ".join(pos_repr + kw_repr)

    print(f"  [TELEMETRY] Calling {func.__name__}({all_args_str})")
    result = func(*args, **kwargs)
    print(f"  [TELEMETRY] {func.__name__} returned -> {result!r}")
    return result


def compute_shipping(weight_kg: float, zone: str, *, express: bool = False) -> float:
    """Target business function with positional and keyword-only parameters."""
    base = weight_kg * (120.0 if zone == "INTL" else 45.0)
    return base * (1.5 if express else 1.0)


def main() -> None:
    print("=== Forwarding `*args` and `**kwargs` Through a Generic Wrapper ===")
    cost_std = call_with_telemetry(compute_shipping, 2.5, "DOMESTIC")
    print(f"  Final Standard Cost : INR {cost_std:.2f}\n")

    cost_exp = call_with_telemetry(compute_shipping, 4.0, zone="INTL", express=True)
    print(f"  Final Express Cost  : INR {cost_exp:.2f}")


if __name__ == "__main__":
    main()
