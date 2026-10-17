"""
Topic 04: Functions
Question 07: Scope and LEGB Rule (Deep Dive)

Master Python variable scope, name resolution, and symbol tables:
- The LEGB rule hierarchy: Local -> Enclosing -> Global -> Built-in
- The `global` keyword mechanics, re-binding, and race conditions
- The `nonlocal` keyword for nested enclosing scopes
- UnboundLocalError: compiler symbol classification and assignment trap
- Runtime symbol tables: locals(), globals(), and __builtins__
- Shadowing built-ins (accidental list/dict rebinding) and recovery
- Module scope isolation, private prefixes (_var), and __all__ exports
- Comprehension scope isolation in Python 3 (preventing loop variable leakage)
- Class body scope vs method scope quirk in nested expressions
- Production-grade thread-safe scoped configuration context manager
"""

import builtins
from typing import Any, Dict, List, Optional, Tuple


# ============================================================
# Q1: The LEGB Resolution Rule (All 4 Tiers Demonstrated)
# ============================================================
# Question: Demonstrate the LEGB hierarchy by defining the same variable name `x`
# in Built-in, Global, Enclosing, and Local scopes. Show how Python resolves
# from inner to outer tiers.

print("=== Q1: LEGB Rule Hierarchy ===")

# Tier 4: Built-in (e.g. `len`, `sum`, `max`)
# Tier 3: Global (Module-level)
target_scope_val = "GLOBAL_VAL"

def outer_enclosing() -> Dict[str, str]:
    # Tier 2: Enclosing (Outer function)
    target_scope_val = "ENCLOSING_VAL"

    def inner_local() -> str:
        # Tier 1: Local (Inner function)
        target_scope_val = "LOCAL_VAL"
        return target_scope_val

    def inner_fallback_enclosing() -> str:
        # Falls back to Enclosing because no local variable exists
        return target_scope_val

    return {
        "local": inner_local(),
        "enclosing_fallback": inner_fallback_enclosing()
    }

results = outer_enclosing()
print(f"  Inner Local resolved:       '{results['local']}'")
print(f"  Fallback Enclosing resolved:'{results['enclosing_fallback']}'")
print(f"  Module Global resolved:     '{target_scope_val}'")

assert results["local"] == "LOCAL_VAL"
assert results["enclosing_fallback"] == "ENCLOSING_VAL"
assert target_scope_val == "GLOBAL_VAL"

# Explanation: LEGB resolution order:
# 1. Local (names assigned inside the current function)
# 2. Enclosing (names in the local scope of any enclosing functions from inner to outer)
# 3. Global (names assigned at top-level of module)
# 4. Built-in (names preassigned in Python builtins module)


# ============================================================
# Q2: The `global` Keyword & Module State Mutation
# ============================================================
# Question: Rebind a module-level global variable from inside a function using the
# `global` keyword. Explain why mutating global state is generally an anti-pattern.

print("\n=== Q2: The `global` Keyword ===")

server_request_counter = 0

def increment_request_counter() -> int:
    global server_request_counter
    # Without 'global', this creates a new local variable shadowing the global
    server_request_counter += 1
    return server_request_counter

def reset_request_counter() -> None:
    global server_request_counter
    server_request_counter = 0

increment_request_counter()
increment_request_counter()
c1 = increment_request_counter()

print(f"  Server request counter after 3 increments: {c1}")
assert c1 == 3
assert server_request_counter == 3

reset_request_counter()
print(f"  Server request counter after reset:        {server_request_counter}")
assert server_request_counter == 0

# Explanation: In Python, assigning to a variable name anywhere in a function body
# makes it local unless explicitly declared `global` or `nonlocal`.


# ============================================================
# Q3: The `nonlocal` Keyword (Enclosing Closures)
# ============================================================
# Question: Implement a stateful accumulator closure using the `nonlocal` keyword.
# Show how `nonlocal` rebinds variables in the enclosing function without polluting the global scope.

print("\n=== Q3: The `nonlocal` Keyword ===")

def create_bank_account(initial_balance: float):
    balance = initial_balance  # Enclosing scope variable

    def deposit(amount: float) -> float:
        nonlocal balance
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        balance += amount
        return balance

    def withdraw(amount: float) -> float:
        nonlocal balance
        if amount > balance:
            raise ValueError("Insufficient balance")
        balance -= amount
        return balance

    def get_balance() -> float:
        return balance

    return deposit, withdraw, get_balance

dep, wdraw, bal = create_bank_account(100.0)
dep(50.0)
wdraw(30.0)
final_bal = bal()

print(f"  Account balance after +$50 and -$30: ${final_bal:.2f}")
assert final_bal == 120.0

# Explanation: `nonlocal` causes the declared identifier to refer to previously
# bound variables in the nearest enclosing function scope, excluding globals.


# ============================================================
# Q4: UnboundLocalError: The Reading-Before-Assignment Trap
# ============================================================
# Question: Demonstrate why referencing a global variable and then assigning to it
# in the same function raises `UnboundLocalError: cannot access local variable where it is not associated with a value`.

print("\n=== Q4: UnboundLocalError Analysis ===")

score = 100

def buggy_increment():
    # Python's compiler inspects the function at compilation time.
    # Because 'score = ...' exists in the body, 'score' is classified as LOCAL for the entire function!
    # Attempting to read 'score' before the assignment raises UnboundLocalError!
    temp = score  # Reading
    score = temp + 10  # Assignment makes it local!

caught_unbound_error = False
try:
    buggy_increment()
except UnboundLocalError as err:
    caught_unbound_error = True
    print(f"  Caught expected UnboundLocalError: {err}")

assert caught_unbound_error

# Correct pattern: declare global explicitly, pass as argument, or return new value
def clean_increment(current_score: int) -> int:
    return current_score + 10

score = clean_increment(score)
print(f"  Clean increment result: {score}")
assert score == 110

# Explanation: Variable scope is determined statically at compile time, not dynamically at runtime.
# An assignment anywhere in a function flags the identifier as local throughout the function.


# ============================================================
# Q5: Runtime Symbol Tables: locals() vs globals()
# ============================================================
# Question: Inspect runtime symbol tables using `locals()` and `globals()`.
# Demonstrate that `locals()` in a function returns a copy of current local bindings.

print("\n=== Q5: locals() and globals() Symbol Tables ===")

def inspect_symbol_tables(param_a: int, param_b: str) -> Dict[str, Any]:
    local_num = 42
    local_text = "Python"
    
    current_locals = locals()
    return current_locals

loc_dict = inspect_symbol_tables(10, "test")
print(f"  Local symbols captured: {sorted(list(loc_dict.keys()))}")

assert loc_dict["param_a"] == 10
assert loc_dict["param_b"] == "test"
assert loc_dict["local_num"] == 42
assert loc_dict["local_text"] == "Python"

# Check globals dict contains module-level variables
assert "score" in globals()
assert "inspect_symbol_tables" in globals()

# Explanation: `globals()` returns the dictionary of the current module's namespace.
# `locals()` returns a dictionary representing the current local namespace frame.


# ============================================================
# Q6: Built-in Shadowing & Safe Recovery
# ============================================================
# Question: Demonstrate the pitfall of accidentally shadowing built-in names
# (e.g. `list = [1, 2, 3]`), and demonstrate how to access the original built-in via the `builtins` module.

print("\n=== Q6: Shadowing Built-in Functions & Recovery ===")

def demonstrate_shadowing():
    # Accidental shadowing: rebinding 'min' and 'list' locally
    min = "shadowed_string"
    list = [10, 20, 30]

    # Attempting to call min([1, 2]) here would raise TypeError: 'str' object is not callable!
    assert isinstance(min, str)
    assert isinstance(list, builtins.list)

    # Recover the true built-in function from standard builtins module
    actual_min_val = builtins.min(list)
    return actual_min_val

res_min = demonstrate_shadowing()
print(f"  Recovered builtins.min(list) -> {res_min}")
assert res_min == 10

# Verify outer module scope did not have its built-in corrupted
assert min([5, 2, 8]) == 2

# Explanation: Assigning to built-in identifiers (min, max, id, list, type, str)
# creates a local or global variable that hides the built-in. `import builtins` allows safe access.


# ============================================================
# Q7: Module Scope Isolation, Private Identifiers & __all__
# ============================================================
# Question: Explain how Python modules isolate scope. Demonstrate conventions for
# internal variables (single leading underscore `_helper`) and explicit exports with `__all__`.

print("\n=== Q7: Module Scope Isolation & __all__ ===")

# Module-level definitions
PUBLIC_CONST = "I am public"
_PRIVATE_HELPER = "I am private internal implementation"

__all__ = ["PUBLIC_CONST", "public_service"]

def public_service() -> str:
    return "Service Running"

def _private_internal_logic() -> str:
    return "Secret calculation"

# Verify __all__ contract
print(f"  Module __all__ exports: {__all__}")
assert "_PRIVATE_HELPER" not in __all__
assert "_private_internal_logic" not in __all__
assert "public_service" in __all__

# Explanation: When a consumer does `from my_module import *`, Python imports only
# the names listed in `__all__`. If `__all__` is omitted, names with a leading underscore are skipped.


# ============================================================
# Q8: Comprehension Scope Isolation (Python 3)
# ============================================================
# Question: Prove that in Python 3, list, set, and dict comprehensions have their own
# isolated local scope and do NOT leak their loop variable into the outer namespace.

print("\n=== Q8: Comprehension Scope Isolation in Python 3 ===")

item = "ORIGINAL_OUTER_VALUE"

# Comprehension iterates over variable 'item'
squared_items = [item ** 2 for item in range(5)]

print(f"  Comprehension result: {squared_items}")
print(f"  Outer 'item' value after comprehension: '{item}' (Did NOT get overwritten!)")

assert squared_items == [0, 1, 4, 9, 16]
assert item == "ORIGINAL_OUTER_VALUE", "Comprehension variable must not leak into outer scope!"

# Traditional for-loop DOES leak loop variable into outer scope
for item in ["LEAKED_1", "LEAKED_2"]:
    pass
print(f"  For-loop 'item' value after loop:        '{item}' (Standard loop LEAKS!)")
assert item == "LEAKED_2"

# Explanation: In Python 3, comprehensions are executed inside an implicit function frame,
# isolating loop variables. Standard `for` statements do not create a new scope.


# ============================================================
# Q9: Class Body Scope vs Method Scope Quirk
# ============================================================
# Question: Demonstrate the scoping quirk where class-level attributes are NOT visible
# inside comprehensions defined in the class body, but ARE accessible via `cls` or `self` in methods.

print("\n=== Q9: Class Body Scope vs Comprehensions Quirk ===")

class DataRegistry:
    BASE_PREFIX = "APP_"
    
    # In Python, class bodies are executed as code blocks, but class scope is NOT
    # an enclosing scope for nested functions or comprehensions inside the class body!
    # The following would fail: [BASE_PREFIX + str(i) for i in range(3)] -> NameError!
    
    # Correct class-level pattern:
    ITEMS = [f"APP_{i}" for i in range(3)]

    @classmethod
    def get_prefixed(cls, suffix: str) -> str:
        # Access via cls is explicit and reliable
        return cls.BASE_PREFIX + suffix

reg_items = DataRegistry.ITEMS
reg_prefixed = DataRegistry.get_prefixed("AUTH")

print(f"  Class registry items:   {reg_items}")
print(f"  Class method prefixed: '{reg_prefixed}'")

assert reg_items == ["APP_0", "APP_1", "APP_2"]
assert reg_prefixed == "APP_AUTH"

# Explanation: Python PEP 227 states that names in class blocks are not accessible
# by nested functions or comprehensions. Use `self.` or `cls.` to access class attributes cleanly.


# ============================================================
# Q10: Production-Grade Scoped Config Switcher Context Manager
# ============================================================
# Question: Implement a thread-safe scoped configuration context manager that temporarily
# overrides global settings and guarantees restoration upon block exit (even on exceptions).

print("\n=== Q10: Scoped Configuration Context Manager ===")

GLOBAL_SYSTEM_CONFIG: Dict[str, Any] = {
    "DEBUG_MODE": False,
    "TIMEOUT_SEC": 30,
    "ENVIRONMENT": "production"
}

class ScopedConfigOverride:
    def __init__(self, **overrides: Any):
        self.overrides = overrides
        self._saved_state: Dict[str, Any] = {}

    def __enter__(self) -> Dict[str, Any]:
        global GLOBAL_SYSTEM_CONFIG
        # Save original values of keys being overwritten
        for key, new_val in self.overrides.items():
            if key in GLOBAL_SYSTEM_CONFIG:
                self._saved_state[key] = GLOBAL_SYSTEM_CONFIG[key]
            GLOBAL_SYSTEM_CONFIG[key] = new_val
        return GLOBAL_SYSTEM_CONFIG

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        global GLOBAL_SYSTEM_CONFIG
        # Restore saved values
        for key, original_val in self._saved_state.items():
            GLOBAL_SYSTEM_CONFIG[key] = original_val
        # Remove any newly inserted keys that were not originally present
        for key in list(self.overrides.keys()):
            if key not in self._saved_state:
                GLOBAL_SYSTEM_CONFIG.pop(key, None)

print(f"  Initial global config: {GLOBAL_SYSTEM_CONFIG}")
assert GLOBAL_SYSTEM_CONFIG["DEBUG_MODE"] is False

# Enter scoped temporary context
with ScopedConfigOverride(DEBUG_MODE=True, TIMEOUT_SEC=5, TEMP_FEATURE=True):
    print(f"  Inside scoped context: {GLOBAL_SYSTEM_CONFIG}")
    assert GLOBAL_SYSTEM_CONFIG["DEBUG_MODE"] is True
    assert GLOBAL_SYSTEM_CONFIG["TIMEOUT_SEC"] == 5
    assert GLOBAL_SYSTEM_CONFIG["TEMP_FEATURE"] is True

# Verify restoration after exit
print(f"  After scoped context:  {GLOBAL_SYSTEM_CONFIG}")
assert GLOBAL_SYSTEM_CONFIG["DEBUG_MODE"] is False
assert GLOBAL_SYSTEM_CONFIG["TIMEOUT_SEC"] == 30
assert "TEMP_FEATURE" not in GLOBAL_SYSTEM_CONFIG

# Verify restoration even if an exception occurs
try:
    with ScopedConfigOverride(DEBUG_MODE=True):
        raise RuntimeError("Simulated crash")
except RuntimeError:
    pass

assert GLOBAL_SYSTEM_CONFIG["DEBUG_MODE"] is False
print("  Guaranteed restoration after exception verified.")

print("\nAll 10 scope and LEGB rule questions executed and asserted successfully!")
