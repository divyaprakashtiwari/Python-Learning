"""
Topic 03: Variables and Constants
Example 01: Variable Assignment, Dynamic Typing, and Rebinding

Demonstrates how Python variables act as labels bound to objects in memory,
and how a variable can be rebound to a new value or even a new data type.
"""


def main() -> None:
    # 1. Standard variable assignment (snake_case per PEP 8)
    student_name = "Divya Prakash"
    completed_topics = 2
    completion_rate = 16.67
    is_active_learner = True

    print("=== Initial Variable Bindings ===")
    print(f"Student Name      : {student_name} (type: {type(student_name).__name__})")
    print(f"Completed Topics  : {completed_topics} (type: {type(completed_topics).__name__})")
    print(f"Completion Rate   : {completion_rate}% (type: {type(completion_rate).__name__})")
    print(f"Active Learner    : {is_active_learner} (type: {type(is_active_learner).__name__})")

    # 2. Updating (rebinding) an existing variable
    completed_topics = completed_topics + 1
    print(f"\nAfter completing Topic 03, completed_topics = {completed_topics}")

    # 3. Dynamic typing: rebinding a variable to a different type
    status_indicator: int | str = 200
    print(f"Status Indicator (as int) : {status_indicator} ({type(status_indicator).__name__})")
    status_indicator = "OK - All Checks Passed"
    print(f"Status Indicator (as str) : {status_indicator} ({type(status_indicator).__name__})")


if __name__ == "__main__":
    main()
