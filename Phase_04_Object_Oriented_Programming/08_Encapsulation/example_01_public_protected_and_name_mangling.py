"""
Phase 4 - Topic 08: Encapsulation
Example 01: Access Conventions (`public`, `_protected`, and `__private` Name Mangling)

Demonstrates:
  - Public attributes (`account_id`): part of the public API
  - Protected convention (`_audit_trail`): internal to class & subclasses (single underscore)
  - Private name mangling (`__pin_hash`): transformed by Python into `_ClassName__pin_hash`
    to prevent accidental attribute collisions in subclasses
"""


class SmartCardWallet:
    """Demonstrates Python's 3-tier attribute visibility conventions."""

    def __init__(self, card_id: str, pin_code: str) -> None:
        self.card_id = card_id  # 1. Public attribute
        self._failed_attempts = 0  # 2. Protected attribute (convention)
        self.__pin_code = pin_code  # 3. Private attribute (name-mangled)

    def verify_pin(self, entered_pin: str) -> bool:
        """Public method providing controlled access to `__pin_code`."""
        if self._failed_attempts >= 3:
            return False
        if entered_pin == self.__pin_code:
            self._failed_attempts = 0
            return True
        self._failed_attempts += 1
        return False


def main() -> None:
    wallet = SmartCardWallet("CARD-7700", "4829")

    print("=== 1. Public and Protected Access ===")
    print(f"  Public `wallet.card_id`           : {wallet.card_id}")
    print(f"  Protected `wallet._failed_attempts`: {wallet._failed_attempts}")
    print(f"  verify_pin('0000') (wrong)        : {wallet.verify_pin('0000')}")
    print(f"  verify_pin('4829') (correct)      : {wallet.verify_pin('4829')}")

    print("\n=== 2. Direct Access to `__pin_code` Fails Due to Name Mangling ===")
    try:
        print(wallet.__pin_code)  # type: ignore[attr-defined]
    except AttributeError as err:
        print(f"  Caught expected AttributeError: {err}")

    print("\n=== 3. Inspecting Mangled Name in `wallet.__dict__` ===")
    print(f"  wallet.__dict__ keys : {list(wallet.__dict__.keys())}")
    # Name mangling prevents accidental collisions; it is not cryptographic security:
    print(f"  Mangled `_SmartCardWallet__pin_code` : {wallet._SmartCardWallet__pin_code!r}")  # type: ignore[attr-defined]


if __name__ == "__main__":
    main()
