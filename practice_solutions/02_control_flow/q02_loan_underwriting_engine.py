"""
Topic 02 - Control Flow
Practice Question 2 Solution: Loan Underwriting Decision Engine

Problem Statement:
Implements loan underwriting decision logic using nested conditional structures:
1. Age Check: 18 <= age <= 65.
2. Credit Score: <580 reject; 580-669 fair credit (requires co-signer >= 700); >=670 prime.
3. Debt-to-Income (DTI): monthly_debt / (annual_income / 12) * 100. Must be <= 43.0%.
Assigns approved interest rates (Prime: 5.25%, Fair: 7.15%).
"""

from typing import Any


def evaluate_loan_application(applicant: dict[str, Any]) -> dict[str, Any]:
    """Evaluates loan eligibility through multi-tier nested underwriting checks."""
    age = applicant.get("age", 0)
    annual_income = applicant.get("annual_income", 0.0)
    monthly_debt = applicant.get("monthly_debt", 0.0)
    credit_score = applicant.get("credit_score", 0)
    has_cosigner = applicant.get("has_cosigner", False)
    cosigner_score = applicant.get("cosigner_credit_score", 0)

    # 1. Age Verification
    if age < 18 or age > 65:
        return {
            "decision": "REJECTED",
            "reason": "Age requirement not met",
            "tier": None,
            "dti": None,
            "rate": None,
        }

    # Validate inputs
    if annual_income <= 0:
        raise ValueError("Annual income must be strictly positive.")
    if monthly_debt < 0:
        raise ValueError("Monthly debt cannot be negative.")
    if not (300 <= credit_score <= 850):
        raise ValueError("Credit score must be between 300 and 850.")

    # 2. Credit Tier & Co-signer Verification
    if credit_score < 580:
        return {
            "decision": "REJECTED",
            "reason": "Poor credit rating",
            "tier": "Subprime",
            "dti": None,
            "rate": None,
        }
    elif 580 <= credit_score <= 669:
        if has_cosigner and cosigner_score >= 700:
            credit_tier = "Fair Credit (Co-signer Qualified)"
            approved_rate = 7.15
        else:
            return {
                "decision": "REJECTED",
                "reason": "Qualified co-signer required",
                "tier": "Fair Credit (Unqualified)",
                "dti": None,
                "rate": None,
            }
    else:
        credit_tier = "Prime Credit"
        approved_rate = 5.25

    # 3. Debt-to-Income (DTI) Check
    monthly_income = annual_income / 12.0
    dti_pct = (monthly_debt / monthly_income) * 100.0

    if dti_pct > 43.0:
        return {
            "decision": "REJECTED",
            "reason": "Debt-to-Income ratio exceeds limit",
            "tier": credit_tier,
            "dti": dti_pct,
            "rate": None,
        }

    return {
        "decision": "APPROVED",
        "reason": "Meets all underwriting criteria",
        "tier": credit_tier,
        "dti": dti_pct,
        "rate": approved_rate,
    }


def main() -> None:
    applicant_data = {
        "age": 29,
        "annual_income": 72000.0,
        "monthly_debt": 1800.0,
        "credit_score": 640,
        "has_cosigner": True,
        "cosigner_credit_score": 745,
    }

    result = evaluate_loan_application(applicant_data)

    print(f"Underwriting Decision: {result['decision']}")
    print(f"Credit Tier: {result['tier']}")
    print(f"Calculated DTI: {result['dti']:.2f}%")
    print(f"Approved Base Interest Rate: {result['rate']:.2f}%")


if __name__ == "__main__":
    main()
