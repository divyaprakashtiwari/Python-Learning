"""
Topic 04 - Functions: Question 2
Problem: Mutable Default Argument Trap and Keyword-Only Parameters (*).
"""

from typing import List, Optional


# 1. Demonstrating the Mutable Default Trap
def record_event_flawed(event_id: str, tags: list = []):  # noqa: B006
    tags.append(event_id)
    return tags


flawed_1 = record_event_flawed("login")
print(f"Flawed Call 1: {flawed_1}")

flawed_2 = record_event_flawed("logout")
print(f"Flawed Call 2: {flawed_2} (Leaked previous invocation state!)")


# 2. Idiomatic Safe Default Pattern with Keyword-Only Parameters
def record_event_safe(
    event_id: str,
    tags: Optional[List[str]] = None,
    *,
    log_level: str = "INFO",
    dry_run: bool = False
) -> List[str]:
    """Safely appends an event to tags using None sentinel to prevent state leakage."""
    if tags is None:
        tags = []

    if not dry_run:
        tags.append(event_id)

    # log_level can be used for logging/auditing
    _ = log_level
    return tags


# 3. Verification of State Isolation
safe_1 = record_event_safe("purchase", log_level="AUDIT")
print(f"\nSafe Call 1: {safe_1} (Tags isolated)")

safe_2 = record_event_safe("refund")
print(f"Safe Call 2: {safe_2} (Tags isolated)")

# Positional keyword-only enforcement verification
print("Positional Keyword-Only Test:")
try:
    # Attempting to supply log_level as 3rd positional argument
    record_event_safe("auth", None, "DEBUG")  # type: ignore
except TypeError as err:
    print(f"Caught Expected Error: TypeError('{err}')")
