"""
Topic 02 - Control Flow
Practice Question 1 Solution: Progressive Marginal Tax Bracket Calculator

Problem Statement:
Determines annual tax liability and effective tax rate based on progressive
marginal tax brackets using if/elif/else statements:
- Income <= 10,000: 0%
- 10,001 to 40,000: 10% on amount over 10,000
- 40,001 to 85,000: $3,000 + 20% on amount over 40,000
- Above 85,000: $12,000 + 30% on amount over 85,000
Computes exact tax owed, net post-tax income, and effective tax rate.
"""


def calculate_tax(gross_income: float) -> dict[str, object]:
    """Calculates progressive tax, net income, and effective rate."""
    if gross_income < 0:
        raise ValueError("Gross income cannot be negative.")

    if gross_income <= 10000:
        bracket = "0% Marginal Bracket"
        tax_owed = 0.0
    elif gross_income <= 40000:
        bracket = "10% Marginal Bracket"
        tax_owed = 0.10 * (gross_income - 10000)
    elif gross_income <= 85000:
        bracket = "20% Marginal Bracket"
        tax_owed = 3000.0 + (0.20 * (gross_income - 40000))
    else:
        bracket = "30% Marginal Bracket"
        tax_owed = 12000.0 + (0.30 * (gross_income - 85000))

    net_income = gross_income - tax_owed
    effective_rate = (tax_owed / gross_income * 100.0) if gross_income > 0 else 0.0

    return {
        "gross_income": gross_income,
        "bracket": bracket,
        "tax_owed": tax_owed,
        "net_income": net_income,
        "effective_rate": effective_rate,
    }


def main() -> None:
    income = 65000.00
    res = calculate_tax(income)

    print(f"Gross Income: ${res['gross_income']:,.2f}")
    print(f"Tax Bracket: {res['bracket']}")
    print(f"Total Tax Owed: ${res['tax_owed']:,.2f}")
    print(f"Net Income: ${res['net_income']:,.2f}")
    print(f"Effective Tax Rate: {res['effective_rate']:.2f}%")


if __name__ == "__main__":
    main()
