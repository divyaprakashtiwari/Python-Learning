"""
Helper Custom Module: `billing_utils.py`
Used by Phase 3 - Topic 10 (`10_Modules_and_Packages`) examples.
"""

DEFAULT_CURRENCY = "INR"
GST_RATE = 0.18


def apply_gst(amount: float, rate: float = GST_RATE) -> float:
    """Return `amount` including GST rounded to 2 decimal places."""
    return round(amount * (1.0 + rate), 2)


def format_currency(amount: float, currency: str = DEFAULT_CURRENCY) -> str:
    """Format a numeric amount with a currency code."""
    return f"{currency} {amount:,.2f}"


# Executed ONLY when `python billing_utils.py` is run directly,
# NEVER when imported by another script (`import billing_utils`).
if __name__ == "__main__":
    print("[billing_utils self-test] Running standalone diagnostics:")
    print(f"  __name__ = {__name__!r}")
    print(f"  Sample   = {format_currency(apply_gst(1000.0))}")
