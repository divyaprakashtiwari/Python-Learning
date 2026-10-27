"""
Topic 07 - Exception Handling: Question 3
Problem: Simulated Transactional Database Executor demonstrating try, except, else, and finally lifecycle.
"""

from typing import Any, Dict, List


def execute_transaction(
    conn_pool: Dict[str, Any],
    queries: List[str],
    fail_on_query_index: int = -1
) -> Dict[str, Any]:
    """Executes a list of queries demonstrating the complete try-except-else-finally contract."""
    response: Dict[str, Any] = {}
    staged: List[str] = []

    try:
        conn_pool["status"] = "BUSY"
        for idx, q in enumerate(queries):
            if idx == fail_on_query_index:
                raise RuntimeError(f"Query '{q}' execution failed")
            staged.append(q)

    except RuntimeError as err:
        # Executes ONLY when an exception occurs in try
        conn_pool["rollbacks"] += 1
        response = {
            "status": "ROLLED_BACK",
            "failed_query": queries[fail_on_query_index],
            "error": str(err)
        }

    else:
        # Executes ONLY when the try block finishes with zero exceptions
        conn_pool["commits"] += 1
        response = {
            "status": "COMMITTED",
            "queries_run": len(staged)
        }

    finally:
        # ALWAYS executes regardless of success, failure, or unhandled exceptions
        conn_pool["status"] = "IDLE"
        conn_pool["total_transactions"] += 1

    return response


def demonstrate_finally_return_hazard() -> str:
    """Demonstrates why returning or breaking inside finally is dangerous (silences active exceptions)."""
    try:
        raise ValueError("Critical database connection error!")
    finally:
        # Warning: returning inside finally suppresses the active ValueError exception!
        return "OVERRIDDEN_SUPPRESSED_ERROR"


# Verification & Execution
pool = {"status": "IDLE", "commits": 0, "rollbacks": 0, "total_transactions": 0}
queries_batch = [
    "SELECT * FROM users",
    "UPDATE users SET active=1",
    "INSERT INTO audit_log VALUES (1)"
]

# Case A: Successful Execution (try -> else -> finally)
res_success = execute_transaction(pool, queries_batch, fail_on_query_index=-1)
print("Case A (Success):")
print(f"- Result: {res_success}")
print(f"- Pool State: {pool}")

# Case B: Execution with Failure (try -> except -> finally)
res_failure = execute_transaction(pool, queries_batch, fail_on_query_index=1)
print("\nCase B (Failure on query index 1):")
print(f"- Result: {res_failure}")
print(f"- Pool State: {pool}")

print("\nLifecycle Verification:")
print("In Case A: `else` ran (commit executed), `except` was bypassed, `finally` released connection.")
print("In Case B: `except` ran (rollback executed), `else` was bypassed, `finally` released connection.")

hazard_result = demonstrate_finally_return_hazard()
print(f"\nFinally Return Hazard Demonstration: Suppressed exception returned: '{hazard_result}'")
