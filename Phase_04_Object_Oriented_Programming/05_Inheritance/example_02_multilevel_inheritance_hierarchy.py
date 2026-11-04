"""
Phase 4 - Topic 05: Inheritance
Example 02: Multilevel Inheritance (`Grandparent -> Parent -> Child`) & Custom Exceptions

Demonstrates:
  - Chaining `super().__init__()` across a 3-level hierarchy
  - Real-world Python standard practice: building a domain exception hierarchy
    inheriting from Python's built-in `Exception` class
"""


class PaymentError(Exception):
    """Base domain exception for all payment failures (Level 1)."""

    def __init__(self, transaction_id: str, message: str) -> None:
        super().__init__(f"[{transaction_id}] {message}")
        self.transaction_id = transaction_id


class CardDeclinedError(PaymentError):
    """Specialized payment error for bank card declines (Level 2)."""

    def __init__(self, transaction_id: str, decline_code: str, message: str) -> None:
        super().__init__(transaction_id, f"Declined ({decline_code}): {message}")
        self.decline_code = decline_code


class InsufficientFundsError(CardDeclinedError):
    """Specific decline reason with shortfall calculation (Level 3)."""

    def __init__(self, transaction_id: str, required: float, available: float) -> None:
        shortfall = round(required - available, 2)
        super().__init__(
            transaction_id,
            decline_code="INSUFFICIENT_FUNDS",
            message=f"Shortfall of INR {shortfall:,.2f}",
        )
        self.shortfall = shortfall


def main() -> None:
    print("=== 1. Raising and Catching a 3-Level Exception Hierarchy ===")
    try:
        raise InsufficientFundsError("TXN-9081", required=5000.0, available=3200.0)
    except PaymentError as err:
        # Caught by the base `PaymentError` handler!
        print(f"  Caught as `PaymentError` : {err}")
        print(f"  Actual runtime class     : {type(err).__name__}")
        if isinstance(err, InsufficientFundsError):
            print(f"  Shortfall attribute      : INR {err.shortfall:,.2f}")

    print("\n=== 2. Inspecting the Method Resolution Order (`__mro__`) ===")
    mro_names = [cls.__name__ for cls in InsufficientFundsError.__mro__]
    print(f"  MRO chain : {' -> '.join(mro_names)}")


if __name__ == "__main__":
    main()
