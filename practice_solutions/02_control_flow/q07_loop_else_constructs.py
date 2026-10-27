"""
Topic 02 - Control Flow
Practice Question 7 Solution: Clean Search & Validation using for...else and while...else

Problem Statement:
Utilizes Python's for...else and while...else constructs without boolean flags:
1. Database Record Lookup (for...else): break if found; else prints not found message.
2. Prime Number Validator without Flags (for...else): break on factor; else confirms prime.
3. Queue Drain Validation (while...else): break on poison pill; else confirms completion.
"""

from typing import Any


def lookup_employee(employees: list[dict[str, Any]], target_id: int) -> str:
    """Performs record search using for...else without boolean flag variables."""
    for emp in employees:
        if emp.get("id") == target_id:
            msg = f"Found {emp.get('name')} ({emp.get('department')})"
            break
    else:
        msg = f"Employee ID {target_id} not found in registry."
    return msg


def check_prime_with_loop_else(n: int) -> str:
    """Verifies primality using for...else without boolean flags."""
    if n < 2:
        return f"{n} is not a prime number (must be >= 2)."

    limit = int(n**0.5) + 1
    for d in range(2, limit):
        if n % d == 0:
            result = f"{n} is composite (first factor found: {d})."
            break
    else:
        result = f"{n} is a prime number (no factors found in range 2 to {limit - 1})."
    return result


def drain_queue_with_while_else(queue: list[str]) -> tuple[bool, str]:
    """Drains a task queue using while...else, breaking on 'POISON_PILL'."""
    tasks = list(queue)
    processed = 0

    while tasks:
        task = tasks.pop(0)
        if task == "POISON_PILL":
            return False, f"Halted prematurely due to poison pill at task #{processed + 1}"
        processed += 1
    else:
        return True, f"All {processed} tasks drained and processed successfully."


def main() -> None:
    employees = [
        {"id": 101, "name": "Sarah Connor", "department": "Cyberdyne"},
        {"id": 102, "name": "John Doe", "department": "Logistics"},
    ]

    print(f"Lookup 101: {lookup_employee(employees, 101)}")
    print(f"Lookup 999: {lookup_employee(employees, 999)}")
    print(f"Prime Check 97: {check_prime_with_loop_else(97)}")

    # Test Queue Drain
    clean_queue = ["task_a", "task_b", "task_c"]
    status, report = drain_queue_with_while_else(clean_queue)
    print(f"Queue Drain: {report}")


if __name__ == "__main__":
    main()
