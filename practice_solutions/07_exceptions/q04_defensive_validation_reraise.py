"""
Topic 07 - Exception Handling: Question 4
Problem: Defensive Input Validation, Explicit Raising, and Bare Re-Raise Auditing Middleware.
"""

from typing import Any, Dict, List


def register_account(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Validates user account registration criteria with specific built-in exception raising."""
    required_keys = ["username", "email", "age", "role"]
    for key in required_keys:
        if key not in profile:
            raise KeyError(f"Missing mandatory registration field: '{key}'")

    if not isinstance(profile["age"], int) or isinstance(profile["age"], bool):
        raise TypeError("Age must be an integer")

    age = profile["age"]
    if age < 18 or age > 120:
        raise ValueError(f"Age {age} is outside permitted registration bounds (18-120)")

    email = str(profile["email"])
    if "@" not in email or "." not in email:
        raise ValueError("Invalid email format")

    role = profile["role"]
    permitted_roles = {"STANDARD", "OPERATOR", "ADMIN"}
    if role not in permitted_roles:
        raise ValueError(f"Unauthorized role: '{role}'")

    account_id = f"ACC-{abs(hash(profile['username'])) % 10000:04d}"
    return {
        "account_id": account_id,
        "status": "REGISTERED"
    }


def audit_registration_wrapper(profile: Dict[str, Any], audit_log: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Middleware auditing failure events before bare re-raising the active exception upstream."""
    try:
        return register_account(profile)
    except Exception as err:
        audit_log.append({
            "event": "REGISTRATION_FAILED",
            "error": type(err).__name__,
            "message": str(err)
        })
        # Bare raise preserves original stack frame and exception context
        raise


# Verification & Execution
audit_trail: List[Dict[str, Any]] = []

# Test A: Valid User
valid_user = {"username": "jdoe", "email": "jdoe@company.org", "age": 28, "role": "STANDARD"}
acc = audit_registration_wrapper(valid_user, audit_trail)
print(f"Registration Success: Account Created {acc['account_id']}")

# Test B: Underage User (raises ValueError)
underage_user = {"username": "kid99", "email": "kid@fun.org", "age": 16, "role": "STANDARD"}
try:
    audit_registration_wrapper(underage_user, audit_trail)
except ValueError as exc:
    print("Caught Upstream Error:", exc)

# Test C: Missing Key (raises KeyError)
missing_key_user = {"username": "anon", "email": "anon@test.io", "age": 30}
try:
    audit_registration_wrapper(missing_key_user, audit_trail)
except KeyError as exc:
    print("Caught Upstream Error:", exc)

# Inspect recorded audit trail
print(f"\nAudit Trail Entries ({len(audit_trail)} logged failures):")
for idx, entry in enumerate(audit_trail, 1):
    print(f"{idx}. Event: {entry['event']} | Error: {entry['error']} | Message: {entry['message']}")
