"""
Phase 3 - Topic 07: Lambda Functions
Example 02: Custom Sorting Keys (`sorted`, `min`, `max` with Multi-Criteria Tuples)

Demonstrates:
  - Passing an inline `key=lambda item: ...` to `sorted()`, `min()`, and `max()`
  - Multi-level tie-breaking sort using a tuple key `lambda emp: (emp["dept"], -emp["salary"])`
"""


def main() -> None:
    employees = [
        {"name": "Rohan", "dept": "Engineering", "salary": 145000, "tenure_yrs": 3},
        {"name": "Ananya", "dept": "Design", "salary": 115000, "tenure_yrs": 4},
        {"name": "Vikram", "dept": "Engineering", "salary": 175000, "tenure_yrs": 6},
        {"name": "Meera", "dept": "Design", "salary": 115000, "tenure_yrs": 2},
        {"name": "Kabir", "dept": "Engineering", "salary": 145000, "tenure_yrs": 5},
    ]

    print("=== 1. `min()` and `max()` with `key=lambda` ===")
    highest_paid = max(employees, key=lambda emp: emp["salary"])
    newest_hire = min(employees, key=lambda emp: emp["tenure_yrs"])
    print(f"  Highest Paid : {highest_paid['name']} (INR {highest_paid['salary']:,})")
    print(f"  Newest Hire  : {newest_hire['name']} ({newest_hire['tenure_yrs']} yrs)")

    print("\n=== 2. Multi-Criteria `sorted()` with Tuple Key ===")
    # Sort by:
    #   1. Department alphabetically (ascending)
    #   2. Salary descending (`-emp["salary"]`)
    #   3. Tenure descending (`-emp["tenure_yrs"]`)
    ranked = sorted(
        employees,
        key=lambda emp: (emp["dept"], -emp["salary"], -emp["tenure_yrs"]),
    )
    for rank, emp in enumerate(ranked, start=1):
        print(
            f"  #{rank} [{emp['dept']:<11}] {emp['name']:<7} | "
            f"Salary: INR {emp['salary']:,} | Tenure: {emp['tenure_yrs']}y"
        )


if __name__ == "__main__":
    main()
