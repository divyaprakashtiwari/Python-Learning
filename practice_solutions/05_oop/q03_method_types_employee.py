"""
Topic 05 - Object-Oriented Programming (OOP): Question 3
Problem: EmployeeRecord with instance methods, @classmethod factories, and @staticmethod utilities.
"""

from typing import Dict, Any


class EmployeeRecord:
    """Demonstrates instance methods, classmethod alternative constructors, and static utilities."""

    def __init__(self, emp_id: str, name: str, base_salary: float, department: str):
        if not self.is_valid_emp_id(emp_id):
            raise ValueError("Invalid employee ID format")
        self.emp_id = emp_id
        self.name = name
        self.base_salary = float(base_salary)
        self.department = department

    # 1. Instance Methods
    def calculate_annual_bonus(self, performance_multiplier: float) -> float:
        """Computes annual bonus based on salary and performance percentage."""
        return self.base_salary * (performance_multiplier / 100.0)

    def get_summary(self) -> str:
        """Returns human-readable employee summary."""
        return f"Employee[ID: {self.emp_id}, Name: {self.name}, Dept: {self.department}, Base: ${self.base_salary:.2f}]"

    # 2. Alternative Constructors with @classmethod
    @classmethod
    def from_csv_row(cls, csv_text: str) -> "EmployeeRecord":
        """Instantiates an EmployeeRecord from a comma-separated text string."""
        tokens = [t.strip() for t in csv_text.split(",")]
        if len(tokens) != 4:
            raise ValueError("Malformed CSV row")
        emp_id, name, salary_str, dept = tokens
        return cls(emp_id, name, float(salary_str), dept)

    @classmethod
    def from_dict(cls, data_dict: Dict[str, Any]) -> "EmployeeRecord":
        """Instantiates an EmployeeRecord from a dictionary."""
        return cls(
            emp_id=data_dict["emp_id"],
            name=data_dict["name"],
            base_salary=float(data_dict["base_salary"]),
            department=data_dict["department"]
        )

    # 3. Static Utilities with @staticmethod
    @staticmethod
    def is_valid_emp_id(emp_id: str) -> bool:
        """Validates EMP-XXXX format where XXXX are 4 numeric digits."""
        if not isinstance(emp_id, str):
            return False
        return emp_id.startswith("EMP-") and len(emp_id) == 8 and emp_id[4:].isdigit()

    @staticmethod
    def calculate_tax_bracket(annual_income: float) -> str:
        """Determines income tax tier without accessing class or instance state."""
        if annual_income <= 50000.0:
            return "TIER_1"
        elif annual_income <= 100000.0:
            return "TIER_2"
        else:
            return "TIER_3"


# Verification & Execution
emp1 = EmployeeRecord("EMP-1001", "Alice Vance", 72000.0, "Engineering")
emp2 = EmployeeRecord.from_csv_row("EMP-2002, Bob Martinez , 95000.0 , Data")
emp3 = EmployeeRecord.from_dict({
    "emp_id": "EMP-3003",
    "name": "Charlie King",
    "base_salary": 115000.0,
    "department": "Finance"
})

print(f"Employee 1 Summary: {emp1.get_summary()}")
print(f"Employee 1 Bonus (Rating 15%): ${emp1.calculate_annual_bonus(15.0):.2f}")
print(f"Employee 2 from CSV: {emp2.get_summary()}")
print(f"Employee 3 from Dict: {emp3.get_summary()}")

tier = EmployeeRecord.calculate_tax_bracket(115000.0)
print(f"Tax Bracket for $115000.00: {tier}")

print(f'ID Validation Test ("INVALID-99"): {EmployeeRecord.is_valid_emp_id("INVALID-99")}')
print(f'ID Validation Test ("EMP-4092"): {EmployeeRecord.is_valid_emp_id("EMP-4092")}')
