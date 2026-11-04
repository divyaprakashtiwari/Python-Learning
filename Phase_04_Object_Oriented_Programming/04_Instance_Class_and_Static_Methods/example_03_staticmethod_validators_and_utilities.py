"""
Phase 4 - Topic 04: Instance, Class and Static Methods
Example 03: `@staticmethod` Validators/Checksums & Calling Them Polymorphically via `self`

Demonstrates:
  - Grouping pure domain algorithms (like Luhn checksum or IFSC validation) as `@staticmethod`
  - Calling a `@staticmethod` via `self.validate(...)` so subclasses can override it if needed
"""


class BankTransferValidator:
    """Groups stateless banking format & checksum algorithms with stateful transfer rules."""

    def __init__(self, daily_limit: float) -> None:
        self.daily_limit = daily_limit

    @staticmethod
    def is_valid_ifsc(code: str) -> bool:
        """
        Standard Indian IFSC format:
          - Exactly 11 characters
          - First 4 chars: uppercase letters (bank code)
          - 5th char: always '0'
          - Last 6 chars: alphanumeric (branch code)
        """
        return (
            len(code) == 11
            and code[:4].isalpha()
            and code[:4].isupper()
            and code[4] == "0"
            and code[5:].isalnum()
        )

    def validate_transfer(self, ifsc: str, amount: float) -> tuple[bool, str]:
        """Instance method combining `@staticmethod` format check + instance `daily_limit`."""
        if not self.is_valid_ifsc(ifsc):
            return False, f"Invalid IFSC format: {ifsc!r}"
        if amount <= 0 or amount > self.daily_limit:
            return False, f"Amount {amount:,.2f} exceeds daily limit {self.daily_limit:,.2f}"
        return True, f"Valid transfer of INR {amount:,.2f} to {ifsc}"


def main() -> None:
    print("=== 1. Direct Call on Class (`BankTransferValidator.is_valid_ifsc`) ===")
    for sample in ("SBIN0001234", "HDFC0123456", "sbin0001234", "SBIN1001234"):
        print(f"  IFSC {sample!r:<14} -> valid={BankTransferValidator.is_valid_ifsc(sample)}")

    print("\n=== 2. Instance Method Calling `@staticmethod` via `self` ===")
    validator = BankTransferValidator(daily_limit=100_000.0)
    for ifsc, amt in (("SBIN0001234", 45000.0), ("SBIN0001234", 250000.0), ("BADIFSC", 500.0)):
        ok, msg = validator.validate_transfer(ifsc, amt)
        print(f"  [{ 'OK' if ok else 'ERR':<3}] {msg}")


if __name__ == "__main__":
    main()
