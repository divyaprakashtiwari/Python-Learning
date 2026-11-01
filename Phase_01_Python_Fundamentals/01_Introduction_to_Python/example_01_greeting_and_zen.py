"""
Topic 01: Introduction to Python
Example 01: Greeting, Basic Calculation, and Core Principles of Python

Demonstrates how clean and readable Python code is compared to traditional
languages, without requiring semicolons, curly braces, or boilerplate class wrappers.
"""


def main() -> None:
    # 1. Printing a welcome message to the console
    learner_name = "Divya Prakash"
    course_title = "Complete Python Notes: Beginner to Advanced DSA"
    print(f"Welcome, {learner_name}!")
    print(f"Course: {course_title}")
    print("-" * 55)

    # 2. Expressive one-line calculation
    daily_study_hours = 2.5
    days_in_month = 30
    monthly_hours = daily_study_hours * days_in_month
    print(f"Studying {daily_study_hours} hrs/day = {monthly_hours} hrs/month")

    # 3. Core aphorisms from The Zen of Python (PEP 20)
    zen_highlights = [
        "Beautiful is better than ugly.",
        "Explicit is better than implicit.",
        "Simple is better than complex.",
        "Readability counts.",
    ]
    print("\nKey Principles of Python (PEP 20):")
    for index, principle in enumerate(zen_highlights, start=1):
        print(f"  {index}. {principle}")


if __name__ == "__main__":
    main()
