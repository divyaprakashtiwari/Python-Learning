"""
Topic 08: Conditional Statements (if, elif, else)
Example 02: Nested Conditionals vs Clean Guard Clauses (Placement Eligibility)

Demonstrates how early-return Guard Clauses flatten deeply nested `if` statements
and provide clear, specific rejection reasons.
"""


def check_placement_drive_eligibility(
    cgpa: float,
    active_backlogs: int,
    attendance_pct: float,
    graduation_year: int,
) -> str:
    """Validate whether a candidate can sit for the campus placement drive."""
    # Guard Clauses: fail fast on invalid preconditions
    if graduation_year != 2027:
        return "ineligible: Only Class of 2027 candidates are eligible."
    if active_backlogs > 0:
        return f"ineligible: {active_backlogs} active backlog(s) must be cleared first."
    if cgpa < 7.0:
        return f"ineligible: CGPA {cgpa:.2f} is below the 7.00 cutoff."
    if attendance_pct < 75.0:
        return f"ineligible: Attendance {attendance_pct:.1f}% is below 75.0%."

    # Tier classification once all base criteria pass
    if cgpa >= 8.5:
        return "ELIGIBLE: Super-Dream & Dream Companies"
    return "ELIGIBLE: Dream & Core Companies"


def main() -> None:
    candidates = [
        ("Divya", 8.9, 0, 91.0, 2027),
        ("Rohan", 7.6, 0, 82.5, 2027),
        ("Sneha", 8.2, 1, 88.0, 2027),
        ("Kabir", 6.5, 0, 80.0, 2027),
    ]

    print("=== Campus Placement Eligibility Audit ===")
    for name, cgpa, backlogs, attendance, batch in candidates:
        verdict = check_placement_drive_eligibility(cgpa, backlogs, attendance, batch)
        print(f"{name:<6} (CGPA={cgpa}, Backlogs={backlogs}) -> {verdict}")


if __name__ == "__main__":
    main()
