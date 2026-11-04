"""
Phase 4 - Topic 04: Instance, Class and Static Methods
Example 01: Side-by-Side Comparison (`self` vs `@classmethod cls` vs `@staticmethod`)

Demonstrates:
  - Instance method (`def method(self)`): accesses/mutates instance state (`self`) and class state
  - Class method (`@classmethod def method(cls)`): receives `cls`, accesses/mutates class-level state
    or constructs instances without needing an existing object
  - Static method (`@staticmethod def method()`): receives neither `self` nor `cls`; a pure utility
    function namespaced inside the class
"""


class PaymentGateway:
    """Demonstrates all three method types in a payment processing service."""

    platform_fee_pct: float = 2.0

    def __init__(self, merchant_id: str, settlement_currency: str = "INR") -> None:
        self.merchant_id = merchant_id
        self.settlement_currency = settlement_currency

    # 1. INSTANCE METHOD: receives `self` (bound to a specific merchant instance)
    def process_charge(self, amount: float) -> str:
        if not self.is_valid_card_amount(amount):
            raise ValueError(f"Invalid charge amount: {amount}")
        fee = round(amount * (self.platform_fee_pct / 100.0), 2)
        net = round(amount - fee, 2)
        return (
            f"[{self.merchant_id}] Gross={self.settlement_currency} {amount:,.2f} | "
            f"Fee={fee:,.2f} ({self.platform_fee_pct}%) | Net={net:,.2f}"
        )

    # 2. CLASS METHOD: receives `cls` (the `PaymentGateway` class itself)
    @classmethod
    def update_platform_fee(cls, new_fee_pct: float) -> None:
        if new_fee_pct < 0 or new_fee_pct > 20:
            raise ValueError("Platform fee must be between 0% and 20%")
        cls.platform_fee_pct = new_fee_pct

    # 3. STATIC METHOD: receives neither `self` nor `cls` (pure validation helper)
    @staticmethod
    def is_valid_card_amount(amount: float) -> bool:
        return 1.0 <= amount <= 500_000.0


def main() -> None:
    print("=== 1. Calling `@staticmethod` Without Creating an Instance ===")
    print(f"  is_valid_card_amount(500.0) : {PaymentGateway.is_valid_card_amount(500.0)}")
    print(f"  is_valid_card_amount(0.25)  : {PaymentGateway.is_valid_card_amount(0.25)}")

    print("\n=== 2. Calling Instance Method (`process_charge`) ===")
    merchant = PaymentGateway("MERCH-88", "INR")
    print(f"  {merchant.process_charge(10000.0)}")

    print("\n=== 3. Calling `@classmethod` (`update_platform_fee`) ===")
    PaymentGateway.update_platform_fee(1.5)
    print(f"  After class-wide fee cut -> {merchant.process_charge(10000.0)}")


if __name__ == "__main__":
    main()
