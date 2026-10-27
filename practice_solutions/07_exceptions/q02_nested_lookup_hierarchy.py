"""
Topic 07 - Exception Handling: Question 2
Problem: Nested Data Lookup with Exception Grouping and Class Hierarchy Precedence.
"""

from typing import Any, Dict, List, Optional


def safe_nested_lookup(
    data_structure: Any,
    query_path: List[Any],
    fallback: Optional[Any] = None
) -> Dict[str, Any]:
    """Safely traverses nested dictionaries and sequences using ordered exception handlers."""
    if not query_path:
        return {"status": "SUCCESS", "value": data_structure, "depth": 0}

    current = data_structure
    for token in query_path:
        try:
            current = current[token]
        # Specific subclass handlers precede general superclass handlers
        except KeyError:
            return {
                "status": "FALLBACK",
                "value": fallback,
                "error_type": "KeyError",
                "failing_token": token,
                "diagnostic": f"Key '{token}' not found in mapping"
            }
        except IndexError:
            return {
                "status": "FALLBACK",
                "value": fallback,
                "error_type": "IndexError",
                "failing_token": token,
                "diagnostic": f"Index {token} out of range for sequence"
            }
        except LookupError as err:
            # General fallback for any other LookupError subclass
            return {
                "status": "FALLBACK",
                "value": fallback,
                "error_type": "LookupError",
                "failing_token": token,
                "diagnostic": str(err)
            }
        except (TypeError, AttributeError) as err:
            # Combined exception tuple group
            return {
                "status": "FALLBACK",
                "value": fallback,
                "error_type": err.__class__.__name__,
                "failing_token": token,
                "diagnostic": "Invalid subscript access on non-container or wrong key type"
            }

    return {
        "status": "SUCCESS",
        "value": current,
        "depth": len(query_path)
    }


# Verification & Execution
payload = {
    "users": [
        {"id": 101, "profile": {"name": "Alice", "tags": ["admin", "dev"]}},
        {"id": 102, "profile": {"name": "Bob", "tags": []}}
    ]
}

res1 = safe_nested_lookup(payload, ["users", 0, "profile", "name"])
res2 = safe_nested_lookup(payload, ["users", 0, "profile", "email"], fallback="no-email")
res3 = safe_nested_lookup(payload, ["users", 5, "profile"])
res4 = safe_nested_lookup(payload, ["users", 0, "profile", "name", 100])
res5 = safe_nested_lookup(None, ["users"])

print("Lookup 1 (Valid Path):")
print(res1)

print("\nLookup 2 (Missing Dict Key 'email'):")
print(res2)

print("\nLookup 3 (Out of Bounds Index 5):")
print(res3)

print("\nLookup 4 (String Indexing Out of Range):")
print(res4)

print("\nLookup 5 (Indexing into Non-Container None):")
print(f"safe_nested_lookup(None, ['users']) -> '{res5['error_type']}' caught by (TypeError, AttributeError) group.")
print(res5)
