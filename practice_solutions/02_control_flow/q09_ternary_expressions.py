"""
Topic 02 - Control Flow
Practice Question 9 Solution: Data Clamping, Severity Mapping & Resilient Fallbacks via Ternary Operators

Problem Statement:
Utilizes single-line conditional (ternary) expressions (x if cond else y):
1. Signal Clamping: bounds [min_bound, max_bound] via nested ternary.
2. Telemetry Severity: code < 0 -> CORRUPT, 0 -> NOMINAL, 1-99 -> INFO, 100-299 -> WARNING, >=300 -> CRITICAL.
3. Resilient Endpoint Resolver: selects first valid non-empty endpoint among primary, backup, default.
4. Short-circuit evaluation demonstration preventing ZeroDivisionError.
"""

from typing import Optional


def clamp_signal(voltage: float, min_val: float, max_val: float) -> float:
    """Clamps a voltage signal between min_val and max_val using inline ternary."""
    return min_val if voltage < min_val else (max_val if voltage > max_val else voltage)


def classify_error_code(code: int) -> str:
    """Classifies an error code using chained ternary expressions."""
    return (
        "CORRUPT_SIGNAL"
        if code < 0
        else (
            "NOMINAL"
            if code == 0
            else (
                "INFO"
                if code <= 99
                else ("WARNING" if code <= 299 else "CRITICAL")
            )
        )
    )


def resolve_endpoint(primary: Optional[str], backup: Optional[str], default: str) -> str:
    """Resolves highest-priority available endpoint via ternary chaining."""
    return primary if primary else (backup if backup else default)


def safe_divide_demonstration() -> float:
    """Demonstrates short-circuit behavior in ternary expressions."""
    # The condition is True, so the division by zero in the alternate branch is never evaluated.
    safe_result = 100.0 if True else (100.0 / 0.0)
    return safe_result


def main() -> None:
    signal_voltage = 14.85
    min_bound = 0.0
    max_bound = 12.0
    error_code = 142
    primary_endpoint = None
    backup_endpoint = "https://backup-api.internal"
    default_host = "https://fallback.internal"

    clamped = clamp_signal(signal_voltage, min_bound, max_bound)
    severity = classify_error_code(error_code)
    endpoint = resolve_endpoint(primary_endpoint, backup_endpoint, default_host)
    safe_val = safe_divide_demonstration()

    print(f"Raw Voltage: {signal_voltage:.2f} V -> Clamped Voltage: {clamped:.2f} V")
    print(f"Error Code: {error_code} -> Operational Status: \"{severity}\"")
    print(f"Resolved Endpoint: \"{endpoint}\"")
    print(f"Safe Division Evaluation: {safe_val} (Unreached division by zero avoided via short-circuit)")


if __name__ == "__main__":
    main()
