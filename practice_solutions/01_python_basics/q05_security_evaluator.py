"""
Topic 01 - Python Basics & Variables
Practice Question 5 Solution: Multi-Tier Security Authorization Evaluator

Problem Statement:
Implements a multi-tier security authorization evaluator using logical and comparison
operators (and, or, not, is, ==):
1. User session: role ("admin", "auditor", "viewer"), is_active, mfa_verified,
   failed_attempts, is_internal_ip.
2. Access is GRANTED iff:
   - is_active is True, AND
   - failed_attempts < 3, AND
   - EITHER (role == "admin" and mfa_verified) OR
            (role in ("auditor", "viewer") and (is_internal_ip or mfa_verified)).
3. Short-circuit evaluation ordering.
4. Identity ('is True') vs equality distinction.
"""

from typing import Any


def evaluate_access(session: dict[str, Any]) -> tuple[bool, str]:
    """Evaluates user session access permissions using short-circuit logic."""
    # 1. Active Account Check (short-circuit: reject immediately if not active)
    if session.get("is_active") is not True:
        return False, "Account is inactive"

    # 2. Lockout Check (short-circuit: reject if excessive failures)
    failed_attempts = session.get("failed_attempts", 0)
    if failed_attempts >= 3:
        return False, "Account locked due to excessive failed attempts"

    # 3. Role and Security Verification
    role = session.get("role", "")
    mfa = session.get("mfa_verified") is True
    internal_ip = session.get("is_internal_ip") is True

    if role == "admin":
        if mfa:
            return True, "Admin with verified MFA"
        return False, "Admin requires mandatory MFA"

    elif role in ("auditor", "viewer"):
        if internal_ip:
            return True, f"{role.capitalize()} from trusted internal IP"
        elif mfa:
            return True, f"{role.capitalize()} with verified MFA"
        return False, f"{role.capitalize()} requires internal IP or MFA"

    return False, f"Unknown or unauthorized role: '{role}'"


def main() -> None:
    session_1 = {
        "role": "admin",
        "is_active": True,
        "mfa_verified": True,
        "failed_attempts": 0,
        "is_internal_ip": False,
    }
    session_2 = {
        "role": "auditor",
        "is_active": True,
        "mfa_verified": False,
        "failed_attempts": 4,
        "is_internal_ip": True,
    }
    session_3 = {
        "role": "viewer",
        "is_active": True,
        "mfa_verified": False,
        "failed_attempts": 1,
        "is_internal_ip": True,
    }

    sessions = [("Session 1", session_1), ("Session 2", session_2), ("Session 3", session_3)]

    for label, sess in sessions:
        allowed, reason = evaluate_access(sess)
        status = "GRANTED" if allowed else "DENIED"
        print(f"{label} Access: {status} (Reason: {reason})")


if __name__ == "__main__":
    main()
