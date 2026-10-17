"""
Topic 04: Functions
Question 01: Function Basics (Deep Dive)

Master the fundamentals of Python functions:
- Definition, invocation, and the implicit None return
- Positional vs keyword arguments
- Pure functions vs side effects (mutability risks)
- Docstrings and function introspection (__name__, __doc__)
- Pass-by-object-reference (mutable vs immutable parameter behavior)
- Guard clauses and early returns for cyclomatic complexity reduction
- Functions as first-class citizens (variables, lists, dictionaries)
- Higher-order callbacks
- Custom function attributes for metadata tracking
- Real-world command dispatcher table
"""

from typing import Any, Callable, Dict, List, Optional, Tuple


# ============================================================
# Q1: Definition, Invocation, and Implicit None Return
# ============================================================
# Question: Define a function with and without an explicit return statement.
# Demonstrate that Python functions without a return statement implicitly return `None`.

print("=== Q1: Function Definition & Implicit None Return ===")

def greet(name: str) -> str:
    """Explicitly returns a formatted greeting string."""
    return f"Hello, {name}!"

def log_message(msg: str) -> None:
    """Prints a message but has NO return statement."""
    print(f"  [LOG]: {msg}")

greeting_result = greet("Developer")
log_result = log_message("System initialized")

print(f"  greet() returned:      '{greeting_result}'")
print(f"  log_message() returned: {log_result} (type: {type(log_result).__name__})")

assert greeting_result == "Hello, Developer!"
assert log_result is None
assert greet.__name__ == "greet"

# Explanation: Every Python function returns a value. If control reaches the end
# without an explicit `return <expr>`, the Python interpreter returns `None`.


# ============================================================
# Q2: Positional vs Keyword Arguments
# ============================================================
# Question: Demonstrate calling a function using positional arguments, keyword arguments,
# and mixed arguments. Show why positional arguments cannot follow keyword arguments.

print("\n=== Q2: Positional vs Keyword Arguments ===")

def create_user_profile(username: str, role: str, status: str = "active") -> Dict[str, str]:
    return {"username": username, "role": role, "status": status}

# 1. Purely positional
p1 = create_user_profile("alice", "admin", "pending")

# 2. Purely keyword (order does not matter!)
p2 = create_user_profile(status="inactive", role="viewer", username="bob")

# 3. Mixed: positional must precede keyword arguments
p3 = create_user_profile("charlie", role="moderator")

print(f"  Positional: {p1}")
print(f"  Keyword:    {p2}")
print(f"  Mixed:      {p3}")

assert p1 == {"username": "alice", "role": "admin", "status": "pending"}
assert p2 == {"username": "bob", "role": "viewer", "status": "inactive"}
assert p3 == {"username": "charlie", "role": "moderator", "status": "active"}

# Explanation: Positional arguments map by index order. Keyword arguments map by name,
# allowing arbitrary ordering. Positional arguments must always precede keyword arguments.


# ============================================================
# Q3: Pure Functions vs Impure Functions (Side Effects)
# ============================================================
# Question: Demonstrate the difference between a pure function (deterministic, no side effects)
# and an impure function (mutates external state or incoming mutable arguments).

print("\n=== Q3: Pure Functions vs Side Effects ===")

# Impure function: mutates caller's list directly (side effect)
def impure_add_tax(prices: List[float], tax_rate: float) -> List[float]:
    for i in range(len(prices)):
        prices[i] = round(prices[i] * (1.0 + tax_rate), 2)
    return prices

# Pure function: creates and returns a brand-new list, leaving original intact
def pure_add_tax(prices: List[float], tax_rate: float) -> List[float]:
    return [round(p * (1.0 + tax_rate), 2) for p in prices]

raw_prices_1 = [100.0, 50.0, 20.0]
pure_result = pure_add_tax(raw_prices_1, 0.08)
print(f"  Pure call result:     {pure_result}")
print(f"  Original list intact: {raw_prices_1}")
assert raw_prices_1 == [100.0, 50.0, 20.0]  # Unmutated!

raw_prices_2 = [100.0, 50.0, 20.0]
impure_result = impure_add_tax(raw_prices_2, 0.08)
print(f"  Impure call result:   {impure_result}")
print(f"  Original list mutated:{raw_prices_2}")
assert raw_prices_2 == [108.0, 54.0, 21.6]  # Mutated in place!

# Explanation: Pure functions promote testability and concurrency safety by avoiding
# shared mutable state and unexpected side effects across call sites.


# ============================================================
# Q4: Docstrings & Function Introspection
# ============================================================
# Question: Inspect a function's runtime metadata: `__name__`, `__doc__`,
# `__code__.co_argcount`, and `__code__.co_varnames`.

print("\n=== Q4: Function Introspection & Docstrings ===")

def calculate_compound_interest(principal: float, rate: float, periods: int) -> float:
    """
    Computes total accrued compound interest.
    
    Formula: A = P * (1 + r)^n
    :param principal: Starting capital
    :param rate: Annual interest rate (0.05 = 5%)
    :param periods: Compounding periods (years)
    :return: Accrued total amount
    """
    multiplier = (1.0 + rate) ** periods
    return round(principal * multiplier, 2)

doc = calculate_compound_interest.__doc__
name = calculate_compound_interest.__name__
arg_count = calculate_compound_interest.__code__.co_argcount
var_names = calculate_compound_interest.__code__.co_varnames

print(f"  Function Name: {name}")
print(f"  Arg count:     {arg_count}")
print(f"  All vars:      {var_names}")
print(f"  Has docstring: {doc is not None and 'Formula: A = P' in doc}")

assert name == "calculate_compound_interest"
assert arg_count == 3
assert "principal" in var_names and "multiplier" in var_names
assert calculate_compound_interest(1000.0, 0.05, 3) == 1157.63

# Explanation: Functions in Python are full objects with accessible bytecode metadata
# via `__code__` and documentation accessible via `__doc__`.


# ============================================================
# Q5: Pass-by-Object-Reference Mechanics
# ============================================================
# Question: Demonstrate how Python's parameter passing ("call by object reference")
# behaves when reassigning vs mutating parameters.

print("\n=== Q5: Pass-by-Object-Reference Mechanics ===")

def reassign_parameter(x: int, items: List[int]) -> None:
    # Rebinding local variable name to a new object (does NOT affect caller)
    x = 999
    items = [999, 999]

def mutate_parameter(items: List[int]) -> None:
    # Mutating the underlying object referenced by both caller and callee
    items.append(42)

orig_num = 10
orig_list = [1, 2, 3]

# Test 1: Rebinding has zero effect on caller
reassign_parameter(orig_num, orig_list)
print(f"  After reassign -> num: {orig_num}, list: {orig_list}")
assert orig_num == 10
assert orig_list == [1, 2, 3]

# Test 2: In-place mutation affects caller
mutate_parameter(orig_list)
print(f"  After mutation -> list: {orig_list}")
assert orig_list == [1, 2, 3, 42]

# Explanation: Python passes object references by value. Rebinding a parameter name
# only changes the local pointer. Mutating the object alters the shared heap instance.


# ============================================================
# Q6: Guard Clauses (Early Return) Pattern
# ============================================================
# Question: Refactor a deeply nested conditional function into a clean, flat function
# using early returns (guard clauses) to validate inputs.

print("\n=== Q6: Guard Clauses & Early Returns ===")

# Refactored clean version with guard clauses
def process_refund(user_id: Optional[str], amount: float, account_balance: float) -> Tuple[bool, str]:
    # Guard 1: Validate user ID
    if not user_id:
        return False, "Error: Invalid user ID"

    # Guard 2: Validate positive amount
    if amount <= 0:
        return False, "Error: Amount must be greater than zero"

    # Guard 3: Validate sufficient funds
    if amount > account_balance:
        return False, "Error: Insufficient funds for refund"

    # Happy path executes at root indentation level
    return True, f"Success: Refunded ${amount:.2f} to user {user_id}"

r1_ok, r1_msg = process_refund(None, 50.0, 100.0)
r2_ok, r2_msg = process_refund("USR_01", -10.0, 100.0)
r3_ok, r3_msg = process_refund("USR_01", 150.0, 100.0)
r4_ok, r4_msg = process_refund("USR_01", 50.0, 100.0)

print(f"  Case 1: {r1_msg}")
print(f"  Case 2: {r2_msg}")
print(f"  Case 3: {r3_msg}")
print(f"  Case 4: {r4_msg}")

assert not r1_ok and "Invalid user" in r1_msg
assert not r2_ok and "greater than zero" in r2_msg
assert not r3_ok and "Insufficient" in r3_msg
assert r4_ok and "Refunded $50.00" in r4_msg

# Explanation: Guard clauses check error conditions upfront and exit immediately,
# avoiding deep 'arrow anti-pattern' nesting and keeping the happy path prominent.


# ============================================================
# Q7: Functions as First-Class Citizens
# ============================================================
# Question: Demonstrate that Python functions can be assigned to variables, passed as
# arguments, stored in data structures (lists, dicts), and returned from other functions.

print("\n=== Q7: First-Class Citizen Functions ===")

def square(x: float) -> float:
    return x * x

def cube(x: float) -> float:
    return x * x * x

def sqrt(x: float) -> float:
    return x ** 0.5

# 1. Assign to variable
op_alias = square
print(f"  Alias call op_alias(4): {op_alias(4)}")
assert op_alias(4) == 16

# 2. Store pipeline of functions in a list
math_pipeline: List[Callable[[float], float]] = [square, cube]
val = 2.0
for func in math_pipeline:
    val = func(val)  # 2.0 -> 4.0 -> 64.0
print(f"  Pipeline output on 2.0: {val}")
assert val == 64.0

# 3. Store in dictionary for lookup
operations_map: Dict[str, Callable[[float], float]] = {
    "sqr": square,
    "cube": cube,
    "sqrt": sqrt
}
assert operations_map["sqrt"](16.0) == 4.0

# Explanation: In Python, functions are instances of `types.FunctionType`.
# They enjoy identical status to integers, strings, and lists.


# ============================================================
# Q8: Higher-Order Callback Functions
# ============================================================
# Question: Implement an asynchronous-style event filter/transformer that accepts
# user-defined callback functions for processing events.

print("\n=== Q8: Higher-Order Callbacks ===")

def process_records(records: List[Dict[str, Any]],
                    filter_fn: Callable[[Dict[str, Any]], bool],
                    transform_fn: Callable[[Dict[str, Any]], Any]) -> List[Any]:
    """Applies filter callback and transformation callback to records."""
    results = []
    for rec in records:
        if filter_fn(rec):
            results.append(transform_fn(rec))
    return results

events = [
    {"type": "click", "user": "alice", "page": "/home"},
    {"type": "scroll", "user": "bob", "page": "/feed"},
    {"type": "click", "user": "charlie", "page": "/checkout"},
    {"type": "view", "user": "diana", "page": "/pricing"}
]

# Callback 1: Filter only 'click' events
def is_click_event(e: Dict[str, Any]) -> bool:
    return e["type"] == "click"

# Callback 2: Transform into user -> page string
def format_event(e: Dict[str, Any]) -> str:
    return f"{e['user']} clicked {e['page']}"

click_summaries = process_records(events, is_click_event, format_event)
print(f"  Extracted click events: {click_summaries}")

assert len(click_summaries) == 2
assert click_summaries == ["alice clicked /home", "charlie clicked /checkout"]

# Explanation: Higher-order functions accept functions as arguments, decoupling
# control flow / traversal from domain-specific filtering and transformation logic.


# ============================================================
# Q9: Custom Function Attributes (Metadata & State Tracking)
# ============================================================
# Question: Attach arbitrary attributes to a function object to track its execution
# call count and cache the most recent calculation without global variables.

print("\n=== Q9: Custom Function Attributes ===")

def fibonacci_tracked(n: int) -> int:
    """Calculates n-th Fibonacci number while tracking total recursive calls."""
    fibonacci_tracked.call_count += 1

    if n <= 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci_tracked(n - 1) + fibonacci_tracked(n - 2)

# Initialize function attribute
fibonacci_tracked.call_count = 0

fib_6 = fibonacci_tracked(6)
total_calls = fibonacci_tracked.call_count

print(f"  fib(6) = {fib_6}")
print(f"  Total recursive invocations: {total_calls}")

assert fib_6 == 8
assert total_calls == 25  # Standard naive tree recursion calls for n=6

# Explanation: Functions are objects whose `__dict__` is writeable. We can attach
# metadata, configuration flags, or call counters directly to the function object.


# ============================================================
# Q10: Real-World Command Dispatcher Table
# ============================================================
# Question: Implement an extensible CLI command dispatcher using a dictionary dispatch
# table, fallback handling, and argument routing instead of if/elif chains.

print("\n=== Q10: Command Dispatcher Pattern ===")

class CommandDispatcher:
    def __init__(self):
        self._handlers: Dict[str, Callable[[List[str]], str]] = {}

    def register(self, command: str, handler: Callable[[List[str]], str]) -> None:
        """Registers a command handler function."""
        self._handlers[command.lower()] = handler

    def dispatch(self, cmd_line: str) -> str:
        """Parses command line string and routes to appropriate handler."""
        parts = cmd_line.strip().split()
        if not parts:
            return "Error: Empty command"

        cmd, *args = parts
        cmd_key = cmd.lower()

        handler = self._handlers.get(cmd_key)
        if not handler:
            return f"Error: Unknown command '{cmd}'. Available: {list(self._handlers.keys())}"

        return handler(args)

dispatcher = CommandDispatcher()

# Register command handlers
def handle_ping(args: List[str]) -> str:
    target = args[0] if args else "localhost"
    return f"PONG: {target} is reachable"

def handle_sum(args: List[str]) -> str:
    if not args:
        return "SUM: 0"
    total = sum(float(x) for x in args)
    return f"SUM: {total}"

def handle_echo(args: List[str]) -> str:
    return " ".join(args)

dispatcher.register("ping", handle_ping)
dispatcher.register("sum", handle_sum)
dispatcher.register("echo", handle_echo)

r_ping = dispatcher.dispatch("ping server.internal")
r_sum = dispatcher.dispatch("sum 10 25.5 4.5")
r_echo = dispatcher.dispatch("echo Hello Python World")
r_err = dispatcher.dispatch("reboot now")

print(f"  Dispatch 'ping':   {r_ping}")
print(f"  Dispatch 'sum':    {r_sum}")
print(f"  Dispatch 'echo':   {r_echo}")
print(f"  Dispatch 'reboot': {r_err}")

assert r_ping == "PONG: server.internal is reachable"
assert r_sum == "SUM: 40.0"
assert r_echo == "Hello Python World"
assert "Unknown command" in r_err

print("\nAll 10 function basics questions executed and asserted successfully!")
