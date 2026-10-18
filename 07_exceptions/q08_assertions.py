"""
Topic 07: Exceptions - Question 08: Assertions

A comprehensive collection of 10 standalone, runnable exercises exploring
Python's `assert` statement, AssertionError, optimization flags (-O),
invariants, the tuple assertion trap, and Design-by-Contract decorators.

Questions Covered:
 1. assert Syntax Fundamentals: Condition evaluation and custom error message payloads.
 2. Internal Invariants vs Input Validation: When to use assert vs explicit ValueError.
 3. The -O (Optimization) Hazard: Understanding how python -O strips assertions (__debug__).
 4. Precondition Assertions: Verifying internal invariants before operation execution.
 5. Postcondition Verification: Guaranteeing that output invariants are strictly satisfied.
 6. Class Invariant Verification: Ensuring object state consistency before and after mutations.
 7. Defensive Unreachable Code Traps: assert False in non-executable branches.
 8. The Tuple Assertion Trap: Why assert (condition, "msg") is always True and broken.
 9. Diagnostic Custom Assertion Helpers: Building detailed diff-producing assertion utilities.
10. Advanced Project: Design-by-Contract (DbC) Contract Decorator Engine (@requires, @ensures).
"""

import functools
from typing import Any, Callable


# ==============================================================================
# Question 1: assert Syntax Fundamentals
# ==============================================================================
def exercise_q1_assert_syntax() -> None:
    """
    Demonstrate basic assert syntax, checking truthiness and generating AssertionError
    with a custom error message.
    """
    print("=== Q1: assert Syntax Fundamentals ===")

    # Passing assertion
    x = 10
    assert x > 0, "x must be positive"

    captured_exc = None
    try:
        assert x < 0, f"Expected x to be negative, got {x}"
    except AssertionError as exc:
        captured_exc = exc
        assert "Expected x to be negative, got 10" in str(exc)

    assert captured_exc is not None
    print(f"  Failing assertion generated AssertionError: '{captured_exc}'")


# ==============================================================================
# Question 2: Internal Invariants vs Input Validation
# ==============================================================================
def exercise_q2_invariants_vs_input_validation() -> None:
    """
    Contrast internal invariants (appropriate for assert) against external
    user/API input validation (which MUST use explicit exceptions like ValueError).
    """
    print("\n=== Q2: Internal Invariants vs Input Validation ===")

    # Public API function: External input MUST raise ValueError, NOT AssertionError!
    def transfer_funds(account_id: str, amount: float) -> None:
        if amount <= 0:
            raise ValueError(f"Transfer amount must be positive, got {amount}")

        # Internal invariant: by this point, amount must be positive
        assert amount > 0, "Internal invariant violated: amount is non-positive"

    # 1. Invalid external input raises ValueError
    try:
        transfer_funds("acc_1", -50.0)
        assert False
    except ValueError as err:
        assert "Transfer amount must be positive" in str(err)

    print("  External user input correctly raised ValueError instead of AssertionError.")


# ==============================================================================
# Question 3: The -O (Optimization) Hazard & __debug__
# ==============================================================================
def exercise_q3_optimization_hazard() -> None:
    """
    Demonstrate that assertions are tied to the built-in constant `__debug__`.
    When Python is run with `-O` or `-OO`, `__debug__` is False, and ALL assert
    statements are completely stripped from bytecode!
    """
    print("\n=== Q3: The -O (Optimization) Hazard & __debug__ ===")

    # Under standard execution, __debug__ is True
    assert isinstance(__debug__, bool)

    print(f"  Current __debug__ state: {__debug__}")
    print("  Notice: Never use assert for security checks or business logic,")
    print("  because running 'python -O' disables all assert statements globally!")


# ==============================================================================
# Question 4: Precondition Assertions
# ==============================================================================
def internal_calculate_average(scores: list[float]) -> float:
    """
    Internal calculation helper with precondition assertion.
    """
    assert len(scores) > 0, "Precondition violated: scores list cannot be empty"
    return sum(scores) / len(scores)


def exercise_q4_precondition_assertions() -> None:
    """
    Demonstrate verifying internal preconditions with assertions.
    """
    print("\n=== Q4: Precondition Assertions ===")

    assert internal_calculate_average([10.0, 20.0, 30.0]) == 20.0

    caught_precondition = False
    try:
        internal_calculate_average([])
    except AssertionError as exc:
        caught_precondition = True
        assert "scores list cannot be empty" in str(exc)

    assert caught_precondition is True
    print("  Precondition assertion successfully trapped empty sequence.")


# ==============================================================================
# Question 5: Postcondition Verification
# ==============================================================================
def binary_search_index(sorted_arr: list[int], target: int) -> int:
    """
    Performs binary search and asserts postconditions before returning.
    """
    low, high = 0, len(sorted_arr) - 1
    found_idx = -1

    while low <= high:
        mid = (low + high) // 2
        if sorted_arr[mid] == target:
            found_idx = mid
            break
        elif sorted_arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    # Postcondition: If index returned != -1, value at index MUST equal target
    if found_idx != -1:
        assert sorted_arr[found_idx] == target, "Postcondition failed: index value != target"
    else:
        assert target not in sorted_arr, "Postcondition failed: target existed in array"

    return found_idx


def exercise_q5_postcondition_verification() -> None:
    """
    Demonstrate postcondition verification asserting algorithmic correctness.
    """
    print("\n=== Q5: Postcondition Verification ===")

    arr = [10, 20, 30, 40, 50]
    assert binary_search_index(arr, 30) == 2
    assert binary_search_index(arr, 99) == -1

    print("  Binary search executed with postconditions verified.")


# ==============================================================================
# Question 6: Class Invariant Verification
# ==============================================================================
class BankAccount:
    """
    Maintains the class invariant that balance >= overdraft_limit at all times.
    """

    def __init__(self, initial_deposit: float, overdraft_limit: float = 0.0) -> None:
        self.balance = initial_deposit
        self.overdraft_limit = overdraft_limit
        self._check_invariants()

    def _check_invariants(self) -> None:
        assert self.balance >= -self.overdraft_limit, (
            f"Invariant broken: balance {self.balance} breaches overdraft -{self.overdraft_limit}"
        )

    def deposit(self, amount: float) -> None:
        assert amount > 0, "Deposit must be positive"
        self.balance += amount
        self._check_invariants()

    def withdraw(self, amount: float) -> None:
        assert amount > 0, "Withdrawal must be positive"
        self.balance -= amount
        self._check_invariants()


def exercise_q6_class_invariant_verification() -> None:
    """
    Demonstrate class invariant checks before and after mutation.
    """
    print("\n=== Q6: Class Invariant Verification ===")

    acc = BankAccount(100.0, overdraft_limit=50.0)
    acc.deposit(50.0)
    assert acc.balance == 150.0

    acc.withdraw(180.0)  # Balance is now -30.0 >= -50.0 overdraft limit
    assert acc.balance == -30.0

    # Withdrawing past overdraft breaches invariant
    caught_invariant = False
    try:
        acc.withdraw(30.0)  # Would make balance -60.0 < -50.0
    except AssertionError as exc:
        caught_invariant = True
        assert "Invariant broken" in str(exc)

    assert caught_invariant is True
    print("  Class invariant successfully prevented illegal state mutation.")


# ==============================================================================
# Question 7: Defensive Unreachable Code Traps
# ==============================================================================
def map_traffic_light_action(light_color: str) -> str:
    """
    Demonstrate assert False in exhaustive pattern / branch matching.
    """
    if light_color == "RED":
        return "STOP"
    elif light_color == "YELLOW":
        return "CAUTION"
    elif light_color == "GREEN":
        return "GO"
    else:
        # Unreachable if caller provides valid enumerated color
        assert False, f"Unreachable branch reached! Invalid light color: '{light_color}'"


def exercise_q7_unreachable_code_traps() -> None:
    """
    Demonstrate assert False acting as an unreachable code sentinel.
    """
    print("\n=== Q7: Defensive Unreachable Code Traps ===")

    assert map_traffic_light_action("RED") == "STOP"
    assert map_traffic_light_action("GREEN") == "GO"

    caught_unreachable = False
    try:
        map_traffic_light_action("PURPLE")
    except AssertionError as exc:
        caught_unreachable = True
        assert "Unreachable branch reached" in str(exc)

    assert caught_unreachable is True
    print("  Unreachable branch sentinel triggered AssertionError as expected.")


# ==============================================================================
# Question 8: The Tuple Assertion Trap
# ==============================================================================
def exercise_q8_tuple_assertion_trap() -> None:
    """
    Demonstrate the notorious Python assertion anti-pattern:
        assert (condition, "message")
    In Python, non-empty tuples evaluate to True! Thus:
        assert (False, "Failure message")
    evaluates to assert (True) and NEVER fails!
    """
    print("\n=== Q8: The Tuple Assertion Trap ===")

    # Non-empty tuple is always truthy in Python!
    assert bool((False, "this is a tuple")) is True

    # WRONG: assert (1 == 2, "1 does not equal 2")
    # This evaluates as `assert (<tuple of 2 items>)` which NEVER raises AssertionError!
    # We test that a non-empty tuple evaluates as truthy:
    tuple_trap = (False, "Error message")
    assert tuple_trap  # Does NOT raise AssertionError because tuple is non-empty!

    # CORRECT: assert 1 == 2, "1 does not equal 2" (no parentheses around statement)
    correct_failure = False
    try:
        assert 1 == 2, "1 does not equal 2"
    except AssertionError:
        correct_failure = True

    assert correct_failure is True
    print("  Demonstrated tuple trap: non-empty tuple evaluates to True.")
    print("  Corrected syntax without parentheses raised AssertionError cleanly.")


# ==============================================================================
# Question 9: Diagnostic Custom Assertion Helpers
# ==============================================================================
def assert_dicts_equal(actual: dict[str, Any], expected: dict[str, Any]) -> None:
    """
    Custom assertion helper that computes and reports precise key-by-key differences.
    """
    missing_keys = set(expected.keys()) - set(actual.keys())
    extra_keys = set(actual.keys()) - set(expected.keys())
    value_mismatches = {
        k: (actual[k], expected[k])
        for k in expected.keys() & actual.keys()
        if actual[k] != expected[k]
    }

    if missing_keys or extra_keys or value_mismatches:
        diff_lines = ["Dictionary assertion mismatch:"]
        if missing_keys:
            diff_lines.append(f"  Missing keys:  {missing_keys}")
        if extra_keys:
            diff_lines.append(f"  Extra keys:    {extra_keys}")
        if value_mismatches:
            diff_lines.append(f"  Value diffs:   {value_mismatches}")
        raise AssertionError("\n".join(diff_lines))


def exercise_q9_custom_assertion_helpers() -> None:
    """
    Test assert_dicts_equal helper.
    """
    print("\n=== Q9: Diagnostic Custom Assertion Helpers ===")

    d1 = {"a": 1, "b": 2}
    d2 = {"a": 1, "b": 2}
    assert_dicts_equal(d1, d2)  # Passes cleanly

    d3 = {"a": 1, "b": 99, "c": 3}
    caught_diff = False
    try:
        assert_dicts_equal(d3, d1)
    except AssertionError as exc:
        caught_diff = True
        err_msg = str(exc)
        assert "Extra keys" in err_msg
        assert "Value diffs" in err_msg

    assert caught_diff is True
    print("  Custom assertion helper generated structured diff diagnostics.")


# ==============================================================================
# Question 10: Advanced Project - Design-by-Contract (DbC) Decorator Engine
# ==============================================================================
def requires(predicate: Callable[..., bool], error_msg: str) -> Callable:
    """Decorator asserting preconditions before function execution."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            assert predicate(*args, **kwargs), f"Precondition failed for {func.__name__}: {error_msg}"
            return func(*args, **kwargs)
        return wrapper
    return decorator


def ensures(predicate: Callable[[Any], bool], error_msg: str) -> Callable:
    """Decorator asserting postconditions on function return values."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            assert predicate(result), f"Postcondition failed for {func.__name__}: {error_msg}"
            return result
        return wrapper
    return decorator


# Contract-annotated business functions
@requires(lambda n: n >= 0, "n must be non-negative")
@ensures(lambda res: res >= 1, "Factorial result must be >= 1")
def contract_factorial(n: int) -> int:
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def exercise_q10_design_by_contract_decorators() -> None:
    """
    Verify @requires and @ensures decorators enforce contracts using assertions.
    """
    print("\n=== Q10: Design-by-Contract (DbC) Decorator Engine ===")

    # Valid execution
    assert contract_factorial(5) == 120
    assert contract_factorial(0) == 1

    # Precondition failure: negative argument
    caught_precondition = False
    try:
        contract_factorial(-3)
    except AssertionError as err:
        caught_precondition = True
        assert "Precondition failed" in str(err)
        assert "n must be non-negative" in str(err)

    assert caught_precondition is True
    print(f"  contract_factorial(5) = {contract_factorial(5)}")
    print("  DbC @requires decorator intercepted invalid precondition with AssertionError.")


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_assert_syntax()
    exercise_q2_invariants_vs_input_validation()
    exercise_q3_optimization_hazard()
    exercise_q4_precondition_assertions()
    exercise_q5_postcondition_verification()
    exercise_q6_class_invariant_verification()
    exercise_q7_unreachable_code_traps()
    exercise_q8_tuple_assertion_trap()
    exercise_q9_custom_assertion_helpers()
    exercise_q10_design_by_contract_decorators()

    print("\nAll 10 assertions questions executed and asserted successfully!")
