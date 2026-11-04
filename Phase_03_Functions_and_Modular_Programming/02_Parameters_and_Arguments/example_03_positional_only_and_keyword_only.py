"""
Phase 3 - Topic 02: Parameters and Arguments
Example 03: Positional-Only (`/`) and Keyword-Only (`*`) Parameter Dividers

Demonstrates:
  - Enforcing positional-only parameters before `/` (PEP 570, Python 3.8+)
  - Allowing standard positional-or-keyword parameters between `/` and `*`
  - Enforcing keyword-only parameters after `*` (PEP 3102)
  - Handling `TypeError` when callers violate parameter passing rules
"""


def transfer_funds(
    sender_acct: str,
    receiver_acct: str,
    /,  # Everything to the LEFT of `/` is POSITIONAL-ONLY
    amount: float,  # Between `/` and `*` is POSITIONAL-OR-KEYWORD
    *,  # Everything to the RIGHT of `*` is KEYWORD-ONLY
    currency: str = "INR",
    instant_settlement: bool = False,
) -> str:
    """Execute a bank transfer with strict parameter passing boundaries."""
    mode = "IMPS-Instant" if instant_settlement else "NEFT-Standard"
    return (
        f"[{mode}] {sender_acct} -> {receiver_acct} : "
        f"{currency} {amount:,.2f}"
    )


def main() -> None:
    print("=== 1. Valid Calls Respecting `/` and `*` Boundaries ===")
    # `amount` passed positionally
    receipt_1 = transfer_funds("ACCT-101", "ACCT-202", 15000.0)
    print(f"  Valid Call 1 : {receipt_1}")

    # `amount` passed by keyword, plus keyword-only arguments
    receipt_2 = transfer_funds(
        "ACCT-101",
        "ACCT-202",
        amount=42500.50,
        currency="USD",
        instant_settlement=True,
    )
    print(f"  Valid Call 2 : {receipt_2}")

    print("\n=== 2. Violating Positional-Only (`/`) Rule ===")
    try:
        # Passing `sender_acct` by keyword is forbidden because it is before `/`
        transfer_funds(sender_acct="ACCT-101", receiver_acct="ACCT-202", amount=500.0)  # type: ignore[misc]
    except TypeError as err:
        print(f"  Caught expected TypeError: {err}")

    print("\n=== 3. Violating Keyword-Only (`*`) Rule ===")
    try:
        # Passing `currency` positionally is forbidden because it is after `*`
        transfer_funds("ACCT-101", "ACCT-202", 500.0, "EUR")  # type: ignore[misc]
    except TypeError as err:
        print(f"  Caught expected TypeError: {err}")


if __name__ == "__main__":
    main()
