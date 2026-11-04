"""
Phase 4 - Topic 02: Constructors
Example 01: `__init__` Initializer with Validation, Defaults, and Derived Attributes

Demonstrates:
  - Setting up default, validated, and derived attributes inside `__init__`
  - Raising `ValueError` in `__init__` so an invalid object can never be constructed
  - Why `__init__` must always return `None`
"""


class BankVaultAccount:
    """Represents a validated bank account whose invariants are enforced at construction."""

    def __init__(
        self,
        account_number: str,
        holder_name: str,
        opening_balance: float = 0.0,
        currency: str = "INR",
    ) -> None:
        # 1. Fail-fast invariant validation inside `__init__`
        if not account_number.strip():
            raise ValueError("account_number cannot be empty")
        if opening_balance < 0:
            raise ValueError(f"opening_balance cannot be negative (got {opening_balance})")

        # 2. Normalized & direct attributes
        self.account_number = account_number.strip().upper()
        self.holder_name = holder_name.strip().title()
        self.balance = round(opening_balance, 2)
        self.currency = currency.upper()

        # 3. Derived attribute computed automatically during initialization
        self.is_high_net_worth = self.balance >= 1_000_000.0

    def summary(self) -> str:
        tier = "HNW-Priority" if self.is_high_net_worth else "Standard"
        return (
            f"[{self.account_number}] {self.holder_name:<15} | "
            f"{self.currency} {self.balance:>12,.2f} ({tier})"
        )


def main() -> None:
    print("=== 1. Valid Construction (With Defaults and Overrides) ===")
    acct_1 = BankVaultAccount(" sbi-1001 ", "aarav sharma")
    acct_2 = BankVaultAccount("hdfc-2040", "priya patel", 2_500_000.0)
    print(f"  {acct_1.summary()}")
    print(f"  {acct_2.summary()}")

    print("\n=== 2. Rejecting Invalid State in `__init__` ===")
    try:
        BankVaultAccount("ICICI-999", "Rohan", opening_balance=-500.0)
    except ValueError as err:
        print(f"  Caught expected ValueError: {err}")


if __name__ == "__main__":
    main()
