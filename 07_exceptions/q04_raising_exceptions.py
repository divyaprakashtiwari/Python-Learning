"""
Topic 07: Exceptions - Question 04: Raising Exceptions

A comprehensive collection of 10 standalone, runnable exercises exploring
explicit exception generation with `raise`, parameterizing error instances,
bare re-raises, NotImplementedError contracts, and schema validation engines.

Questions Covered:
 1. raise Syntax Fundamentals: Generating ValueError and TypeError with actionable messages.
 2. Multi-Argument Exceptions: Attaching error codes, timestamps, and metadata to err.args.
 3. Bare raise: Preserving original stack trace and re-throwing active exceptions.
 4. Precondition Validation: Defensive guard clauses asserting parameter validity.
 5. NotImplementedError: Enforcing interface method implementation in abstract base classes.
 6. StopIteration in Custom Iterators: Signaling termination in generator/iterator protocols.
 7. Error-Code to Exception Adapter: Transforming legacy C-style return codes into Pythonic exceptions.
 8. Context-Enriched Re-raising: Appending diagnostic metadata to an active exception before re-raising.
 9. Raising from Conditions: Constructing dynamic domain failure exceptions.
10. Advanced Project: Declarative Entity Contract & Field Validator Engine.
"""

from typing import Any, Callable


# ==============================================================================
# Question 1: raise Syntax Fundamentals
# ==============================================================================
def validate_age(age: int) -> int:
    """
    Demonstrate raising standard built-in exceptions for invalid argument values and types.
    """
    if not isinstance(age, int):
        raise TypeError(f"Age must be an integer, got {type(age).__name__}")
    if age < 0 or age > 150:
        raise ValueError(f"Age {age} is out of allowable range (0-150)")
    return age


def exercise_q1_raise_syntax() -> None:
    """
    Demonstrate raising and catching TypeError and ValueError.
    """
    print("=== Q1: raise Syntax Fundamentals ===")

    assert validate_age(25) == 25

    # Check TypeError
    caught_type = False
    try:
        validate_age("25")  # type: ignore
    except TypeError as err:
        caught_type = True
        assert "must be an integer" in str(err)

    # Check ValueError
    caught_val = False
    try:
        validate_age(-5)
    except ValueError as err:
        caught_val = True
        assert "out of allowable range" in str(err)

    assert caught_type is True
    assert caught_val is True
    print("  Validated normal age: 25")
    print("  Successfully trapped expected TypeError and ValueError.")


# ==============================================================================
# Question 2: Multi-Argument Exceptions
# ==============================================================================
def exercise_q2_multi_argument_exceptions() -> None:
    """
    Demonstrate passing multiple arguments to an exception constructor,
    which are automatically accessible via `err.args`.
    """
    print("\n=== Q2: Multi-Argument Exceptions ===")

    def query_service(endpoint: str) -> None:
        if endpoint == "/unauthorized":
            raise RuntimeError("Access Denied", 403, "ERR_REVOKED_TOKEN")

    try:
        query_service("/unauthorized")
        assert False, "Should have raised RuntimeError"
    except RuntimeError as exc:
        msg, code, err_id = exc.args
        assert msg == "Access Denied"
        assert code == 403
        assert err_id == "ERR_REVOKED_TOKEN"

        print(f"  Caught RuntimeError with args: msg='{msg}', code={code}, id='{err_id}'")


# ==============================================================================
# Question 3: Bare raise (Preserving Stack Trace)
# ==============================================================================
def exercise_q3_bare_raise() -> None:
    """
    Demonstrate that a bare `raise` statement with no arguments re-throws the
    currently active exception while preserving its original traceback and instance.
    """
    print("\n=== Q3: Bare raise ===")

    logged_errors: list[str] = []

    def intermediate_worker() -> None:
        try:
            # Generate original error
            raise KeyError("missing_session_key")
        except KeyError as exc:
            # Audit/log locally
            logged_errors.append(f"Audit log: {exc}")
            # Re-raise the active exception to caller
            raise

    caught_re_raised = False
    try:
        intermediate_worker()
    except KeyError as exc:
        caught_re_raised = True
        assert "missing_session_key" in str(exc)

    assert caught_re_raised is True
    assert len(logged_errors) == 1
    print(f"  Locally audited: {logged_errors[0]}")
    print("  Bare raise successfully propagated original exception to caller.")


# ==============================================================================
# Question 4: Precondition Validation Guard Clauses
# ==============================================================================
def create_user_account(username: str, email: str, role: str) -> dict[str, str]:
    """
    Demonstrate defensive guard clauses that raise exceptions at the entry point.
    """
    if not username or not username.strip():
        raise ValueError("Username cannot be empty or whitespace")
    if "@" not in email:
        raise ValueError(f"Invalid email address: '{email}'")
    if role not in ("admin", "member", "guest"):
        raise ValueError(f"Unknown role '{role}'; allowed: admin, member, guest")

    return {"username": username.strip(), "email": email, "role": role}


def exercise_q4_precondition_guard_clauses() -> None:
    """
    Test guard clauses against diverse invalid arguments.
    """
    print("\n=== Q4: Precondition Validation Guard Clauses ===")

    # Valid
    user = create_user_account("alice", "alice@example.com", "admin")
    assert user["username"] == "alice"

    # Empty username
    try:
        create_user_account("   ", "a@a.com", "guest")
        assert False
    except ValueError as exc:
        assert "Username cannot be empty" in str(exc)

    # Invalid email
    try:
        create_user_account("bob", "bob_at_example.com", "guest")
        assert False
    except ValueError as exc:
        assert "Invalid email address" in str(exc)

    # Invalid role
    try:
        create_user_account("carol", "c@c.com", "superadmin")
        assert False
    except ValueError as exc:
        assert "Unknown role" in str(exc)

    print(f"  Successfully guarded account creation with descriptive exceptions.")


# ==============================================================================
# Question 5: NotImplementedError in Interface Contracts
# ==============================================================================
class CacheBackend:
    """Abstract caching interface raising NotImplementedError on un-implemented methods."""

    def get(self, key: str) -> str:
        raise NotImplementedError("Subclasses must implement get()")

    def set(self, key: str, value: str) -> None:
        raise NotImplementedError("Subclasses must implement set()")


class MemoryCacheBackend(CacheBackend):
    def __init__(self) -> None:
        self._store: dict[str, str] = {}

    def get(self, key: str) -> str:
        return self._store.get(key, "")

    def set(self, key: str, value: str) -> None:
        self._store[key] = value


def exercise_q5_not_implemented_error() -> None:
    """
    Demonstrate raising NotImplementedError to enforce interface compliance.
    """
    print("\n=== Q5: NotImplementedError in Interface Contracts ===")

    abstract_backend = CacheBackend()
    try:
        abstract_backend.get("user:1")
        assert False, "Should raise NotImplementedError"
    except NotImplementedError as exc:
        assert "Subclasses must implement get()" in str(exc)

    concrete_backend = MemoryCacheBackend()
    concrete_backend.set("user:1", "Alice")
    assert concrete_backend.get("user:1") == "Alice"

    print("  Abstract base successfully enforced method contracts via NotImplementedError.")


# ==============================================================================
# Question 6: StopIteration in Custom Iterators
# ==============================================================================
class CountdownIterator:
    """
    Iterator that counts down from N to 1, raising StopIteration when exhausted.
    """

    def __init__(self, start: int) -> None:
        self.current = start

    def __iter__(self) -> "CountdownIterator":
        return self

    def __next__(self) -> int:
        if self.current <= 0:
            raise StopIteration
        val = self.current
        self.current -= 1
        return val


def exercise_q6_stop_iteration() -> None:
    """
    Demonstrate raising StopIteration to terminate iteration protocols.
    """
    print("\n=== Q6: StopIteration in Custom Iterators ===")

    countdown = CountdownIterator(3)
    items = list(countdown)
    assert items == [3, 2, 1]

    # Explicit next() on exhausted iterator
    try:
        next(countdown)
        assert False, "Should raise StopIteration"
    except StopIteration:
        pass

    print(f"  Countdown items collected: {items}")
    print("  StopIteration cleanly terminated iterator loop.")


# ==============================================================================
# Question 7: Error-Code to Exception Adapter
# ==============================================================================
def exercise_q7_error_code_to_exception_adapter() -> None:
    """
    Convert legacy C-style integer return codes into Pythonic exception raises.
    """
    print("\n=== Q7: Error-Code to Exception Adapter ===")

    # Simulated legacy API returning tuple (status_code, payload)
    def legacy_system_call(cmd: str) -> tuple[int, str]:
        if cmd == "DISK_READ":
            return 0, "DATA_BLOCK_OK"
        elif cmd == "DISK_IO_ERR":
            return 5, "I/O Hardware failure"
        elif cmd == "DISK_FULL":
            return 28, "No space left on device"
        return -1, "Unknown command"

    def pythonic_system_call(cmd: str) -> str:
        code, message = legacy_system_call(cmd)
        if code == 0:
            return message
        elif code == 5:
            raise IOError(f"Hardware failure (Code {code}): {message}")
        elif code == 28:
            raise OSError(f"Disk full error (Code {code}): {message}")
        else:
            raise RuntimeError(f"System call failed with code {code}: {message}")

    # Success case
    assert pythonic_system_call("DISK_READ") == "DATA_BLOCK_OK"

    # Code 5 -> IOError
    try:
        pythonic_system_call("DISK_IO_ERR")
        assert False
    except IOError as err:
        assert "Hardware failure" in str(err)

    # Code 28 -> OSError
    try:
        pythonic_system_call("DISK_FULL")
        assert False
    except OSError as err:
        assert "Disk full error" in str(err)

    print("  Successfully adapted return codes into IOError and OSError.")


# ==============================================================================
# Question 8: Context-Enriched Re-raising
# ==============================================================================
def exercise_q8_context_enriched_reraising() -> None:
    """
    Demonstrate mutating or enriching an exception's args with additional diagnostic
    context before re-raising with bare `raise`.
    """
    print("\n=== Q8: Context-Enriched Re-raising ===")

    def load_subcomponent(component_id: str) -> None:
        try:
            # Inner operation raises KeyError
            raise KeyError("missing_driver_manifest")
        except KeyError as exc:
            # Enrich exception with component_id context
            exc.args = (*exc.args, f"Failed while initializing component '{component_id}'")
            raise

    try:
        load_subcomponent("GRAPHICS_ACCELERATOR_0")
        assert False
    except KeyError as exc:
        assert len(exc.args) == 2
        assert "GRAPHICS_ACCELERATOR_0" in exc.args[1]
        print(f"  Enriched exception args caught: {exc.args}")


# ==============================================================================
# Question 9: Raising from Conditions
# ==============================================================================
def process_withdrawal(current_balance: float, withdrawal_amount: float) -> float:
    """
    Raise specific domain exceptions based on logical conditions.
    """
    if withdrawal_amount <= 0:
        raise ValueError("Withdrawal amount must be strictly positive")
    if withdrawal_amount > current_balance:
        raise PermissionError(
            f"Overdraft rejected: requested {withdrawal_amount}, balance is only {current_balance}"
        )
    return current_balance - withdrawal_amount


def exercise_q9_raising_from_conditions() -> None:
    """
    Demonstrate raising ValueError for invalid input and PermissionError for insufficient funds.
    """
    print("\n=== Q9: Raising from Conditions ===")

    balance = 500.0
    new_balance = process_withdrawal(balance, 200.0)
    assert new_balance == 300.0

    # Negative amount
    try:
        process_withdrawal(balance, -50.0)
        assert False
    except ValueError as exc:
        assert "must be strictly positive" in str(exc)

    # Overdraft
    try:
        process_withdrawal(balance, 1000.0)
        assert False
    except PermissionError as exc:
        assert "Overdraft rejected" in str(exc)

    print(f"  Clean balance update: {new_balance}")
    print("  Validated condition-based exception generation.")


# ==============================================================================
# Question 10: Advanced Project - Declarative Contract & Schema Validator
# ==============================================================================
class ValidationError(ValueError):
    """Base exception for schema validation failures."""
    pass


class SchemaValidator:
    """
    Declarative schema validator that tests a dictionary against rules
    (type, presence, range, custom predicates) and raises detailed ValidationError
    with line numbers or field paths.
    """

    def __init__(self, rules: dict[str, dict[str, Any]]) -> None:
        self.rules = rules

    def validate(self, record: dict[str, Any]) -> dict[str, Any]:
        for field, spec in self.rules.items():
            # 1. Required check
            if spec.get("required", False) and field not in record:
                raise ValidationError(f"Field '{field}' is mandatory but missing")

            if field not in record:
                continue

            val = record[field]

            # 2. Type check
            expected_type = spec.get("type")
            if expected_type and not isinstance(val, expected_type):
                raise ValidationError(
                    f"Field '{field}' expected type {expected_type.__name__}, got {type(val).__name__}"
                )

            # 3. Numeric range check
            if "min" in spec and val < spec["min"]:
                raise ValidationError(f"Field '{field}' ({val}) below minimum {spec['min']}")
            if "max" in spec and val > spec["max"]:
                raise ValidationError(f"Field '{field}' ({val}) above maximum {spec['max']}")

            # 4. Custom predicate check
            predicate: Callable[[Any], bool] | None = spec.get("predicate")
            if predicate and not predicate(val):
                raise ValidationError(f"Field '{field}' failed custom constraint: {spec.get('error_msg')}")

        return record


def exercise_q10_schema_validator() -> None:
    """
    Test declarative SchemaValidator against valid and invalid payloads.
    """
    print("\n=== Q10: Declarative Contract & Schema Validator ===")

    rules = {
        "username": {
            "type": str,
            "required": True,
            "predicate": lambda s: len(s) >= 3,
            "error_msg": "Username must have at least 3 characters",
        },
        "level": {
            "type": int,
            "required": True,
            "min": 1,
            "max": 100,
        },
        "score": {
            "type": float,
            "required": False,
            "min": 0.0,
        },
    }

    validator = SchemaValidator(rules)

    # Valid record
    valid_payload = {"username": "admin_bob", "level": 42, "score": 98.5}
    res = validator.validate(valid_payload)
    assert res == valid_payload

    # Missing required field
    try:
        validator.validate({"level": 10})
        assert False
    except ValidationError as err:
        assert "Field 'username' is mandatory" in str(err)

    # Type error
    try:
        validator.validate({"username": "alice", "level": "one"})  # type: ignore
        assert False
    except ValidationError as err:
        assert "expected type int, got str" in str(err)

    # Out of range
    try:
        validator.validate({"username": "alice", "level": 150})
        assert False
    except ValidationError as err:
        assert "above maximum 100" in str(err)

    # Predicate failure
    try:
        validator.validate({"username": "ab", "level": 10})
        assert False
    except ValidationError as err:
        assert "at least 3 characters" in str(err)

    print(f"  Valid record passed schema.")
    print("  SchemaValidator caught all 4 distinct constraint violations with ValidationError.")


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_raise_syntax()
    exercise_q2_multi_argument_exceptions()
    exercise_q3_bare_raise()
    exercise_q4_precondition_guard_clauses()
    exercise_q5_not_implemented_error()
    exercise_q6_stop_iteration()
    exercise_q7_error_code_to_exception_adapter()
    exercise_q8_context_enriched_reraising()
    exercise_q9_raising_from_conditions()
    exercise_q10_schema_validator()

    print("\nAll 10 raising exceptions questions executed and asserted successfully!")
