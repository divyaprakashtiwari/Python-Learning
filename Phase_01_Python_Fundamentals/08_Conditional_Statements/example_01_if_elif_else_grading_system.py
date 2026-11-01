"""
Topic 08: Conditional Statements (if, elif, else)
Example 01: Multi-Way Branching — University Grading & Scholarship System

Demonstrates how `if`, `elif`, and `else` evaluate mutually exclusive conditions
top-to-bottom, executing only the first matching branch.
"""


def evaluate_student_performance(marks: int) -> tuple[str, str]:
    """Return (grade, scholarship_status) for a given score out of 100."""
    if not (0 <= marks <= 100):
        return ("INVALID", "Score must be between 0 and 100")

    if marks >= 90:
        return ("O (Outstanding)", "100% Tuition Waiver")
    elif marks >= 80:
        return ("A+ (Excellent)", "50% Tuition Waiver")
    elif marks >= 70:
        return ("A (Very Good)", "25% Book Grant")
    elif marks >= 50:
        return ("B (Pass)", "Standard Enrollment")
    else:
        return ("F (Reappear)", "Mandatory Remedial Coaching")


def main() -> None:
    test_scores = [94, 83, 72, 58, 35, 105]
    print("=== University Grading & Scholarship Evaluator ===")
    for score in test_scores:
        grade, remark = evaluate_student_performance(score)
        print(f"Marks: {score:>3} -> Grade: {grade:<17} | Benefit: {remark}")


if __name__ == "__main__":
    main()
