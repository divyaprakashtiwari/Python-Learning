"""
Phase 3 - Topic 02: Parameters and Arguments
Example 01: Formal Parameters vs Actual Arguments & Binding Order

Demonstrates:
  - The difference between formal parameters (in `def`) and actual arguments (in calls)
  - Positional binding order and arity (argument count) matching
  - Inspecting a function's formal parameters programmatically via `inspect.signature`
"""

import inspect


def schedule_appointment(patient_name: str, doctor_name: str, time_slot: str) -> str:
    """Return a formatted appointment confirmation string."""
    # `patient_name`, `doctor_name`, and `time_slot` are FORMAL PARAMETERS
    return f"Confirmed: {patient_name} with Dr. {doctor_name} at {time_slot}"


def main() -> None:
    print("=== 1. Formal Parameters vs Actual Arguments ===")
    # "Aarav", "Mehta", and "10:30 AM" are ACTUAL ARGUMENTS
    confirmation_1 = schedule_appointment("Aarav", "Mehta", "10:30 AM")
    print(f"  Call 1 (Correct Order) : {confirmation_1}")

    # Swapping positional arguments changes which parameter receives which value
    confirmation_2 = schedule_appointment("Mehta", "Aarav", "10:30 AM")
    print(f"  Call 2 (Swapped Order) : {confirmation_2}")

    print("\n=== 2. Passing Variables and Expressions as Arguments ===")
    user = "Priya"
    specialist = "Sharma"
    hour = 14
    # Expressions are evaluated BEFORE being bound to formal parameters
    confirmation_3 = schedule_appointment(
        user.upper(),
        specialist,
        f"{hour}:00 HRS",
    )
    print(f"  Call 3 (Expressions)   : {confirmation_3}")

    print("\n=== 3. Inspecting Formal Parameters at Runtime ===")
    sig = inspect.signature(schedule_appointment)
    print(f"  Function Signature     : {sig}")
    for idx, (param_name, param_obj) in enumerate(sig.parameters.items(), start=1):
        print(
            f"  Param #{idx}: name={param_name!r:<14} | "
            f"annotation={param_obj.annotation.__name__:<4} | "
            f"kind={param_obj.kind.description}"
        )


if __name__ == "__main__":
    main()
