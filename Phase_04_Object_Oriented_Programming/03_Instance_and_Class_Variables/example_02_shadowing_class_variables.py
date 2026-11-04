"""
Phase 4 - Topic 03: Instance and Class Variables
Example 02: Attribute Shadowing (`self.attr = ...` vs `Class.attr = ...`)

Demonstrates:
  - How assigning `self.gst_rate = 0.0` on one instance creates an instance variable
    in `self.__dict__` that SHADOWS the class variable for that instance only
  - How `del self.gst_rate` removes the shadow and restores fallback to the class variable
"""


class EmployeeBadge:
    """Demonstrates class attribute lookup and per-instance shadowing."""

    company_domain: str = "techcorp.in"
    default_access_level: int = 1

    def __init__(self, username: str) -> None:
        self.username = username

    def email(self) -> str:
        return f"{self.username}@{self.company_domain}"


def main() -> None:
    emp_1 = EmployeeBadge("aarav")
    emp_2 = EmployeeBadge("priya")

    print("=== 1. Before Shadowing: Both Read From `EmployeeBadge.__dict__` ===")
    print(f"  emp_1.__dict__ : {emp_1.__dict__}")
    print(f"  emp_1.email()  : {emp_1.email()} | level={emp_1.default_access_level}")
    print(f"  emp_2.email()  : {emp_2.email()} | level={emp_2.default_access_level}")

    print("\n=== 2. Shadowing `company_domain` on `emp_1` Only ===")
    # Creates `'company_domain'` inside `emp_1.__dict__`; does NOT touch `EmployeeBadge`!
    emp_1.company_domain = "contractor.techcorp.in"
    print(f"  emp_1.__dict__ : {emp_1.__dict__}")
    print(f"  emp_1.email()  : {emp_1.email()} (uses shadowed instance attribute)")
    print(f"  emp_2.email()  : {emp_2.email()} (still uses class attribute!)")

    print("\n=== 3. Deleting the Shadow Restores Fallback to Class Variable ===")
    del emp_1.company_domain
    print(f"  After `del emp_1.company_domain`, emp_1.email() : {emp_1.email()}")


if __name__ == "__main__":
    main()
