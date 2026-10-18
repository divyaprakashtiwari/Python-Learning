"""
Topic 07: Exceptions - Question 02: Multiple Exception Types

A comprehensive collection of 10 standalone, runnable exercises exploring
strategies for handling multiple exception types in Python, exception hierarchies,
LookupError/ArithmeticError bases, re-raising, and resilient failover pipelines.

Questions Covered:
 1. Grouped Exceptions in Single Tuple: except (ValueError, TypeError) syntax.
 2. Sequential Exception Handlers: Distinct recovery logic per exception type.
 3. Exception Hierarchy Ordering: Subclass-first ordering rule (Child before Parent).
 4. Polymorphic Base Exceptions: LookupError catching both IndexError and KeyError.
 5. ArithmeticError Family: Handling ZeroDivisionError, OverflowError, and FloatingPointError.
 6. Dynamic Exception Tuples: Parameterizing handled exceptions via tuple constants.
 7. Selective Re-raising: Handling known exceptions and re-raising unexpected ones.
 8. Multi-Layer Nested Try/Except: Inner operational errors vs outer boundary failures.
 9. Exception Inspection & Type Dispatch: Branching based on concrete exception type.
10. Advanced Project: Multi-Driver Resilient Payment Failover Engine with granular error policies.
"""

from typing import Any


# ==============================================================================
# Question 1: Grouped Exceptions in a Single Tuple
# ==============================================================================
def parse_and_index(items: list[str], index_str: str) -> tuple[str | None, str | None]:
    """
    Demonstrate catching both ValueError (invalid int) and IndexError (out of bounds)
    in a single grouped `except (ValueError, IndexError) as err` block.
    """
    try:
        idx = int(index_str)
        return items[idx], None
    except (ValueError, IndexError) as err:
        return None, f"Input error ({type(err).__name__}): {err}"


def exercise_q1_grouped_tuple_exceptions() -> None:
    """
    Demonstrate grouped exception tuple handling.
    """
    print("=== Q1: Grouped Exceptions in a Single Tuple ===")

    fruits = ["apple", "banana", "cherry"]

    # Valid
    val1, err1 = parse_and_index(fruits, "1")
    assert val1 == "banana"
    assert err1 is None

    # ValueError case
    val2, err2 = parse_and_index(fruits, "not_a_number")
    assert val2 is None
    assert err2 is not None
    assert "ValueError" in err2

    # IndexError case
    val3, err3 = parse_and_index(fruits, "99")
    assert val3 is None
    assert err3 is not None
    assert "IndexError" in err3

    print(f"  Valid index '1' returned: {val1}")
    print(f"  Grouped caught error 1: {err2}")
    print(f"  Grouped caught error 2: {err3}")


# ==============================================================================
# Question 2: Sequential Exception Handlers
# ==============================================================================
def execute_database_query(record_id: Any, records: dict[int, str]) -> str:
    """
    Demonstrate multiple sequential except blocks where each exception triggers
    a completely different recovery pathway.
    """
    try:
        int_id = int(record_id)
        return f"RECORD_FOUND: {records[int_id]}"
    except TypeError:
        return "ERROR_RECOVERY: Provided ID object is not convertible to int"
    except ValueError:
        return "ERROR_RECOVERY: Provided ID string contains non-numeric characters"
    except KeyError:
        return f"ERROR_RECOVERY: ID {record_id} does not exist in records"


def exercise_q2_sequential_handlers() -> None:
    """
    Demonstrate sequential distinct handlers for TypeError, ValueError, and KeyError.
    """
    print("\n=== Q2: Sequential Exception Handlers ===")

    db = {101: "Alice", 102: "Bob"}

    res_ok = execute_database_query("101", db)
    res_val = execute_database_query("abc", db)
    res_type = execute_database_query([1, 2], db)
    res_key = execute_database_query(999, db)

    assert "Alice" in res_ok
    assert "non-numeric" in res_val
    assert "not convertible" in res_type
    assert "does not exist" in res_key

    print(f"  Normal response: {res_ok}")
    print(f"  ValueError handler: {res_val}")
    print(f"  TypeError handler: {res_type}")
    print(f"  KeyError handler: {res_key}")


# ==============================================================================
# Question 3: Exception Hierarchy Ordering (Subclass-First Rule)
# ==============================================================================
def exercise_q3_hierarchy_ordering() -> None:
    """
    Demonstrate that specific exceptions MUST precede general parent exceptions.
    If a parent exception (e.g. OSError) is placed before its child (e.g. FileNotFoundError),
    the child block will be shadowed and never executed.
    """
    print("\n=== Q3: Exception Hierarchy Ordering ===")

    # FileNotFoundError inherits from OSError
    assert issubclass(FileNotFoundError, OSError)

    caught_as = None

    # Correct ordering: FileNotFoundError first, then general OSError
    try:
        with open("non_existent_path_xyz.tmp", "r") as f:
            pass
    except FileNotFoundError:
        caught_as = "SPECIFIC_CHILD: FileNotFoundError"
    except OSError:
        caught_as = "GENERAL_PARENT: OSError"

    assert caught_as == "SPECIFIC_CHILD: FileNotFoundError"

    # Illustrate shadowing if parent is placed first
    shadowed_res = None
    try:
        with open("non_existent_path_xyz.tmp", "r") as f:
            pass
    except OSError:
        shadowed_res = "SHADOWED_BY_PARENT: OSError"
    except FileNotFoundError:
        shadowed_res = "UNREACHABLE_CHILD"

    assert shadowed_res == "SHADOWED_BY_PARENT: OSError"

    print(f"  Proper order caught:   {caught_as}")
    print(f"  Shadowed order caught: {shadowed_res} (demonstrating why order matters!)")


# ==============================================================================
# Question 4: Polymorphic Base Exceptions (LookupError)
# ==============================================================================
def exercise_q4_lookup_error_base() -> None:
    """
    Demonstrate LookupError as the common standard library ancestor for both
    IndexError (sequences) and KeyError (mappings).
    """
    print("\n=== Q4: Polymorphic Base Exceptions (LookupError) ===")

    assert issubclass(IndexError, LookupError)
    assert issubclass(KeyError, LookupError)

    def extract_item(container: Any, index_or_key: Any) -> tuple[Any, str | None]:
        try:
            return container[index_or_key], None
        except LookupError as err:
            return None, f"Caught via LookupError base: {type(err).__name__}"

    # Catching IndexError via LookupError
    val_list, err_list = extract_item(["a", "b"], 10)
    assert val_list is None
    assert "IndexError" in (err_list or "")

    # Catching KeyError via LookupError
    val_dict, err_dict = extract_item({"k1": "v1"}, "missing_key")
    assert val_dict is None
    assert "KeyError" in (err_dict or "")

    print(f"  IndexError handled by LookupError: {err_list}")
    print(f"  KeyError handled by LookupError:   {err_dict}")


# ==============================================================================
# Question 5: ArithmeticError Family
# ==============================================================================
def exercise_q5_arithmetic_error_family() -> None:
    """
    Demonstrate ArithmeticError as the unified base class for ZeroDivisionError,
    OverflowError, and FloatingPointError.
    """
    print("\n=== Q5: ArithmeticError Family ===")

    assert issubclass(ZeroDivisionError, ArithmeticError)
    assert issubclass(OverflowError, ArithmeticError)
    assert issubclass(FloatingPointError, ArithmeticError)

    def safe_arithmetic(op_type: str, *args: Any) -> tuple[Any, str | None]:
        try:
            if op_type == "div":
                return args[0] / args[1], None
            elif op_type == "exp":
                # Exponentiation with floats exceeding float max range raises OverflowError
                return 2.0 ** args[0], None
            return None, "Unknown op"
        except ArithmeticError as exc:
            return None, f"ArithmeticError caught: {type(exc).__name__}"

    # ZeroDivisionError
    res1, err1 = safe_arithmetic("div", 10, 0)
    assert res1 is None
    assert "ZeroDivisionError" in (err1 or "")

    # OverflowError (float power overflow)
    res2, err2 = safe_arithmetic("exp", 1024)
    assert res2 is None
    assert "OverflowError" in (err2 or "")

    print(f"  {err1}")
    print(f"  {err2}")


# ==============================================================================
# Question 6: Dynamic Exception Tuples
# ==============================================================================
def exercise_q6_dynamic_exception_tuples() -> None:
    """
    Demonstrate parameterizing handled exception types using a tuple variable.
    Allows reusable, configurable exception interceptors across functions.
    """
    print("\n=== Q6: Dynamic Exception Tuples ===")

    # Configurable tuple of exceptions
    VALIDATION_EXCEPTIONS: tuple[type[Exception], ...] = (ValueError, TypeError, KeyError)

    def execute_with_guard(func: Any, *args: Any) -> tuple[Any, bool]:
        try:
            return func(*args), True
        except VALIDATION_EXCEPTIONS:
            return None, False

    # Test with ValueError
    val1, ok1 = execute_with_guard(int, "bad_int")
    assert val1 is None
    assert ok1 is False

    # Test with TypeError
    val2, ok2 = execute_with_guard(len, 12345)
    assert val2 is None
    assert ok2 is False

    # Test with success
    val3, ok3 = execute_with_guard(int, "100")
    assert val3 == 100
    assert ok3 is True

    print(f"  Guarded execution with dynamic tuple: OK={ok1}, OK={ok2}, OK={ok3}")


# ==============================================================================
# Question 7: Selective Re-raising
# ==============================================================================
def exercise_q7_selective_reraising() -> None:
    """
    Catch a broad exception type, inspect its details or properties, handle
    anticipated cases, and re-raise (`raise`) unexpected cases.
    """
    print("\n=== Q7: Selective Re-raising ===")

    def handle_known_codes(code: int) -> str:
        try:
            if code == 404:
                raise ValueError("NOT_FOUND: Resource missing")
            elif code == 500:
                raise ValueError("SERVER_CRASH: Fatal database down")
            return "SUCCESS"
        except ValueError as err:
            if "NOT_FOUND" in str(err):
                return "HANDLED_SOFTLY: 404 ignored"
            # Re-raise server crashes
            raise

    # 404 handled cleanly
    res_404 = handle_known_codes(404)
    assert res_404 == "HANDLED_SOFTLY: 404 ignored"

    # 500 re-raised
    caught_server_crash = False
    try:
        handle_known_codes(500)
    except ValueError as exc:
        if "SERVER_CRASH" in str(exc):
            caught_server_crash = True

    assert caught_server_crash is True
    print(f"  Selective handle result: {res_404}")
    print("  Unexpected condition properly re-raised and caught at caller level.")


# ==============================================================================
# Question 8: Multi-Layer Nested Try/Except
# ==============================================================================
def exercise_q8_nested_try_except() -> None:
    """
    Demonstrate fine-grained multi-layer try/except where inner exceptions
    provide local defaults, allowing outer logic to proceed uninterrupted.
    """
    print("\n=== Q8: Multi-Layer Nested Try/Except ===")

    raw_user_records = [
        {"name": "Alice", "score": "95"},
        {"name": "Bob", "score": "corrupted"},
        "NOT_A_DICT",
        {"name": "Charlie", "score": "88"},
    ]

    clean_data: list[dict[str, Any]] = []

    for entry in raw_user_records:
        try:
            # Outer layer: Type validation
            user_name = entry["name"]  # type: ignore

            # Inner layer: Score parsing with local fallback
            try:
                score = int(entry["score"])  # type: ignore
            except (ValueError, TypeError):
                score = 0  # Fallback score on parse failure

            clean_data.append({"name": user_name, "score": score})

        except (TypeError, KeyError):
            # Outer layer catches non-dict entries or missing name
            continue

    assert len(clean_data) == 3
    assert clean_data[0] == {"name": "Alice", "score": 95}
    assert clean_data[1] == {"name": "Bob", "score": 0}  # Inner recovery
    assert clean_data[2] == {"name": "Charlie", "score": 88}

    print(f"  Processed {len(clean_data)} valid records with inner & outer recovery:")
    for rec in clean_data:
        print(f"    - {rec['name']}: {rec['score']}")


# ==============================================================================
# Question 9: Exception Inspection & Type Dispatch
# ==============================================================================
def exercise_q9_type_dispatch() -> None:
    """
    Demonstrate catching Exception once and programmatically dispatching
    to different handlers using isinstance() or a type-to-handler dispatch table.
    """
    print("\n=== Q9: Exception Inspection & Type Dispatch ===")

    def dispatch_handler(exc: Exception) -> str:
        if isinstance(exc, (ValueError, TypeError)):
            return f"CLIENT_INPUT_FAULT: {exc}"
        elif isinstance(exc, LookupError):
            return f"DATA_MISSING_FAULT: {exc}"
        else:
            return f"UNEXPECTED_SYSTEM_FAULT: {exc}"

    res_val = dispatch_handler(ValueError("bad string"))
    res_type = dispatch_handler(TypeError("int + str"))
    res_key = dispatch_handler(KeyError("missing_id"))
    res_unexp = dispatch_handler(RuntimeError("thread deadlock"))

    assert "CLIENT_INPUT_FAULT" in res_val
    assert "CLIENT_INPUT_FAULT" in res_type
    assert "DATA_MISSING_FAULT" in res_key
    assert "UNEXPECTED_SYSTEM_FAULT" in res_unexp

    print("  Dispatch table classifications:")
    print(f"    {res_val}")
    print(f"    {res_key}")
    print(f"    {res_unexp}")


# ==============================================================================
# Question 10: Advanced Project - Multi-Driver Resilient Payment Gateway
# ==============================================================================
# Custom Gateway Exceptions
class PaymentNetworkTimeout(IOError):
    pass


class PaymentAuthenticationFailed(PermissionError):
    pass


class InsufficientAccountBalance(ValueError):
    pass


class PaymentGateway:
    """
    Enterprise-grade multi-gateway transaction processor that handles distinct
    failure domains with specialized retry, fallback, and abort policies.
    """

    def __init__(self) -> None:
        self.primary_attempts = 0
        self.backup_attempts = 0

    def process_charge(self, customer_id: str, amount: float, fail_mode: str | None = None) -> dict[str, Any]:
        """
        Attempts charge on primary gateway; if network timeout occurs, fails over
        to secondary gateway. If authentication fails or funds are insufficient,
        aborts immediately.
        """
        try:
            self.primary_attempts += 1
            if fail_mode == "timeout":
                raise PaymentNetworkTimeout("Primary Gateway connection timed out after 3000ms")
            elif fail_mode == "auth_failed":
                raise PaymentAuthenticationFailed("Primary Gateway API key revoked")
            elif fail_mode == "no_funds":
                raise InsufficientAccountBalance("Customer account has insufficient funds")

            return {"status": "SUCCESS", "gateway": "PRIMARY", "amount": amount}

        except PaymentNetworkTimeout as timeout_exc:
            # Policy: Transient network error -> Failover to Backup Gateway
            try:
                self.backup_attempts += 1
                return {
                    "status": "SUCCESS",
                    "gateway": "BACKUP",
                    "amount": amount,
                    "failover_reason": str(timeout_exc),
                }
            except Exception as backup_exc:
                return {"status": "FAILED", "reason": f"Backup failed: {backup_exc}"}

        except PaymentAuthenticationFailed as auth_exc:
            # Policy: Fatal security misconfiguration -> Abort immediately, alert ops
            return {"status": "ABORTED_AUTH", "reason": str(auth_exc)}

        except InsufficientAccountBalance as funds_exc:
            # Policy: User financial error -> Return clean user rejection without retry
            return {"status": "REJECTED_FUNDS", "reason": str(funds_exc)}


def exercise_q10_resilient_payment_gateway() -> None:
    """
    Test PaymentGateway under multiple failure scenarios.
    """
    print("\n=== Q10: Multi-Driver Resilient Payment Gateway ===")

    gw = PaymentGateway()

    # Scenario 1: Clean success
    tx1 = gw.process_charge("cust_1", 100.0)
    assert tx1["status"] == "SUCCESS"
    assert tx1["gateway"] == "PRIMARY"

    # Scenario 2: Timeout -> Automatic Failover to backup
    tx2 = gw.process_charge("cust_2", 250.0, fail_mode="timeout")
    assert tx2["status"] == "SUCCESS"
    assert tx2["gateway"] == "BACKUP"
    assert "timed out" in tx2["failover_reason"]

    # Scenario 3: Auth Failure -> Immediate abort without fallback
    tx3 = gw.process_charge("cust_3", 50.0, fail_mode="auth_failed")
    assert tx3["status"] == "ABORTED_AUTH"
    assert "API key revoked" in tx3["reason"]

    # Scenario 4: Insufficient Funds -> Clean user rejection
    tx4 = gw.process_charge("cust_4", 10000.0, fail_mode="no_funds")
    assert tx4["status"] == "REJECTED_FUNDS"
    assert "insufficient funds" in tx4["reason"]

    print(f"  Transaction 1 (Clean):     {tx1['gateway']} ({tx1['status']})")
    print(f"  Transaction 2 (Failover):  {tx2['gateway']} ({tx2['status']})")
    print(f"  Transaction 3 (Fatal):     {tx3['status']}")
    print(f"  Transaction 4 (Rejection): {tx4['status']}")


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_grouped_tuple_exceptions()
    exercise_q2_sequential_handlers()
    exercise_q3_hierarchy_ordering()
    exercise_q4_lookup_error_base()
    exercise_q5_arithmetic_error_family()
    exercise_q6_dynamic_exception_tuples()
    exercise_q7_selective_reraising()
    exercise_q8_nested_try_except()
    exercise_q9_type_dispatch()
    exercise_q10_resilient_payment_gateway()

    print("\nAll 10 multiple exception types questions executed and asserted successfully!")
