"""
Phase 4 - Topic 05: Inheritance
Example 01: Single Inheritance (`Parent` -> `Child`) and Reusing Base Behavior

Demonstrates:
  - Defining a base class (`Employee`) and specialized subclasses (`FullTimeDeveloper`, `Contractor`)
  - Calling the parent initializer via `super().__init__(...)`
  - Checking inheritance relationships with `isinstance()` and `issubclass()`
"""


class Employee:
    """Base class sharing common identity and badge logic for all staff."""

    def __init__(self, emp_id: str, name: str) -> None:
        self.emp_id = emp_id
        self.name = name

    def badge_label(self) -> str:
        return f"[{self.emp_id}] {self.name}"


class FullTimeDeveloper(Employee):
    """Inherits from `Employee` and adds salary + tech stack."""

    def __init__(self, emp_id: str, name: str, monthly_salary: float, primary_lang: str) -> None:
        super().__init__(emp_id, name)  # Initialize `emp_id` and `name` in `Employee`
        self.monthly_salary = monthly_salary
        self.primary_lang = primary_lang

    def compute_monthly_payout(self) -> float:
        return self.monthly_salary


class HourlyContractor(Employee):
    """Inherits from `Employee` and computes payout from hourly rate * hours logged."""

    def __init__(self, emp_id: str, name: str, hourly_rate: float, hours_logged: float) -> None:
        super().__init__(emp_id, name)
        self.hourly_rate = hourly_rate
        self.hours_logged = hours_logged

    def compute_monthly_payout(self) -> float:
        return round(self.hourly_rate * self.hours_logged, 2)


def main() -> None:
    dev = FullTimeDeveloper("EMP-101", "Aarav", 140000.0, "Python")
    contractor = HourlyContractor("CNT-502", "Priya", 1800.0, 65.0)

    print("=== 1. Subclasses Inherit `badge_label()` and Add Specialized Payouts ===")
    print(f"  {dev.badge_label():<20} | Payout: INR {dev.compute_monthly_payout():,.2f} ({dev.primary_lang})")
    print(f"  {contractor.badge_label():<20} | Payout: INR {contractor.compute_monthly_payout():,.2f}")

    print("\n=== 2. Verifying `isinstance()` and `issubclass()` ===")
    print(f"  isinstance(dev, FullTimeDeveloper) : {isinstance(dev, FullTimeDeveloper)}")
    print(f"  isinstance(dev, Employee)          : {isinstance(dev, Employee)} (IS-A Employee!)")
    print(f"  issubclass(HourlyContractor, Employee) : {issubclass(HourlyContractor, Employee)}")


if __name__ == "__main__":
    main()
