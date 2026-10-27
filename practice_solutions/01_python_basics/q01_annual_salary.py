"""
Topic 01 - Python Basics & Variables
Practice Question 1 Solution: Annual Salary Calculation

Problem Statement:
Accept three distinct values representing a person's first name, age, and
hourly wage. Store them in appropriately typed variables (string, integer, float).
Determine and print the data type of each variable, and compute their annual
salary assuming a standard 2080-hour work year.
"""


def calculate_annual_salary(first_name: str, age: int, hourly_wage: float) -> dict[str, object]:
    """Validates inputs, inspects types, and calculates annual salary."""
    if not isinstance(first_name, str) or not first_name.strip():
        raise ValueError("First name must be a non-empty string.")
    if not isinstance(age, int) or age <= 0:
        raise ValueError("Age must be a positive integer.")
    if not isinstance(hourly_wage, (int, float)) or hourly_wage < 0:
        raise ValueError("Hourly wage must be a non-negative number.")

    hourly_wage = float(hourly_wage)
    annual_salary = hourly_wage * 2080

    return {
        "first_name": first_name,
        "first_name_type": type(first_name),
        "age": age,
        "age_type": type(age),
        "hourly_wage": hourly_wage,
        "hourly_wage_type": type(hourly_wage),
        "annual_salary": annual_salary,
        "formatted_salary": f"${annual_salary:,.2f}",
    }


def main() -> None:
    # Sample Input
    name = "Elena"
    age = 28
    wage = 34.50

    result = calculate_annual_salary(name, age, wage)

    print(f"Variable 'first_name' has type {result['first_name_type']} with value '{result['first_name']}'")
    print(f"Variable 'age' has type {result['age_type']} with value {result['age']}")
    print(f"Variable 'hourly_wage' has type {result['hourly_wage_type']} with value {result['hourly_wage']}")
    print(f"Calculated Annual Salary for {result['first_name']}: {result['formatted_salary']}")


if __name__ == "__main__":
    main()
