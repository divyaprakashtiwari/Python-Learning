"""
Topic 01 - Python Basics & Variables
Practice Question 3 Solution: Compound Interest & Bill Denomination Breakdown

Problem Statement:
1. Given Principal (P), annual interest rate (r in percent), compounding frequency (n),
   and time period in years (t), calculate total accrued amount:
       A = P * (1 + r / (100 * n)) ** (n * t)
2. Determine total interest earned (A - P).
3. Using integer division (//) and modulo (%), break down whole-dollar interest into
   minimum count of currency bills ($100, $50, $20, $10, $5, $1).
"""


def calculate_compound_interest(principal: float, rate_pct: float, freq: int, years: float) -> dict[str, object]:
    """Computes compound interest and decomposes whole dollars into denominations."""
    if principal < 0:
        raise ValueError("Principal must be non-negative.")
    if rate_pct < 0:
        raise ValueError("Rate must be non-negative.")
    if freq <= 0:
        raise ValueError("Compounding frequency must be strictly positive.")
    if years <= 0:
        raise ValueError("Time in years must be strictly positive.")

    # Compound Interest Formula
    accrued = principal * ((1 + (rate_pct / (100.0 * freq))) ** (freq * years))
    interest = accrued - principal
    whole_dollars = int(interest)

    # Bill breakdown using integer division and modulo
    denominations = [100, 50, 20, 10, 5, 1]
    breakdown: dict[int, int] = {}
    remaining = whole_dollars

    for bill in denominations:
        count = remaining // bill
        breakdown[bill] = count
        remaining = remaining % bill

    return {
        "accrued": accrued,
        "interest": interest,
        "whole_dollars": whole_dollars,
        "breakdown": breakdown,
    }


def main() -> None:
    p = 5000.00
    r = 6.5
    n = 4
    t = 3

    res = calculate_compound_interest(p, r, n, t)

    print(f"Total Accrued Amount: ${res['accrued']:,.2f}")
    print(f"Total Interest Earned: ${res['interest']:,.2f}")
    print(f"Whole Dollar Interest: ${res['whole_dollars']}")
    print("Currency Breakdown:")
    for bill, count in res["breakdown"].items():
        print(f"- ${bill} bills: {count}")


if __name__ == "__main__":
    main()
