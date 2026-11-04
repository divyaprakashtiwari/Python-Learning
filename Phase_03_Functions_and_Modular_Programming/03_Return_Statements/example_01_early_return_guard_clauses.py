"""
Phase 3 - Topic 03: Return Statements
Example 01: Early Return Guard Clauses vs Deeply Nested Conditionals

Demonstrates:
  - How `return` immediately terminates function execution and pops the stack frame
  - Refactoring "Arrow Anti-Pattern" nested `if/else` blocks into flat Guard Clauses
  - Implicit `None` return when execution reaches the end of a function without `return`
"""


def approve_loan_nested(age: int, credit_score: int, annual_income: float) -> str:
    """Deeply nested validation (harder to read and maintain)."""
    if age >= 21:
        if credit_score >= 700:
            if annual_income >= 300000.0:
                return "APPROVED: Eligible for Prime Rate Loan"
            else:
                return "REJECTED: Annual income below INR 3,00,000"
        else:
            return "REJECTED: Credit score below 700"
    else:
        return "REJECTED: Applicant must be at least 21 years old"


def approve_loan_guard_clauses(
    age: int,
    credit_score: int,
    annual_income: float,
) -> str:
    """Flat, readable validation using Early Return Guard Clauses."""
    if age < 21:
        return "REJECTED: Applicant must be at least 21 years old"
    if credit_score < 700:
        return "REJECTED: Credit score below 700"
    if annual_income < 300000.0:
        return "REJECTED: Annual income below INR 3,00,000"

    # Happy path is completely unindented at the bottom
    return "APPROVED: Eligible for Prime Rate Loan"


def log_audit_event(event: str) -> None:
    """Function with no explicit return statement returns `None`."""
    print(f"  [AUDIT LOG] {event}")


def main() -> None:
    print("=== 1. Comparing Nested vs Early Return Guard Clauses ===")
    test_applicants = [
        (19, 750, 500000.0),
        (28, 640, 500000.0),
        (28, 760, 220000.0),
        (30, 780, 850000.0),
    ]
    for age, score, income in test_applicants:
        res_nested = approve_loan_nested(age, score, income)
        res_guards = approve_loan_guard_clauses(age, score, income)
        assert res_nested == res_guards
        print(f"  Applicant (age={age}, score={score}, income={income:,.0f}) -> {res_guards}")

    print("\n=== 2. Implicit `None` Return When No `return` Is Reached ===")
    return_val = log_audit_event("Loan batch processing completed")
    print(f"  Return value of `log_audit_event` : {return_val!r} (type: {type(return_val).__name__})")


if __name__ == "__main__":
    main()
