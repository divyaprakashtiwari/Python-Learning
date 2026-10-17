"""
Topic 04: Functions
Question 05: Lambda Functions (Deep Dive)

Master anonymous functions (lambdas) in Python:
- Syntax restrictions: single expressions only (no statements, no loops)
- Custom sorting key functions with tie-breaking
- The infamous late-binding closure pitfall in loops & default arg fix (lambda i=i: i)
- Ternary conditional expressions inside lambdas
- Multi-argument and variadic (*args, **kwargs) lambdas
- Higher-order functional composition (compose(f, g))
- Immediately Invoked Function Expressions (IIFE)
- Integration with built-ins: map, filter, min, max, sorted
- Performance and clarity: lambda vs operator module (itemgetter, attrgetter)
- Real-world dynamic business rules and discount calculation engine
"""

import operator
import time
from typing import Any, Callable, Dict, List, Tuple


# ============================================================
# Q1: Lambda Syntax & Single-Expression Constraints
# ============================================================
# Question: Demonstrate the syntax of a lambda function. Explain why lambdas cannot
# contain statements (e.g. `pass`, `return`, `assert`, assignment) and implicitly return their expression.

print("=== Q1: Lambda Syntax & Expression Mechanics ===")

# Standard def function
def def_square(x: float) -> float:
    return x * x

# Equivalent lambda function: `lambda <params>: <single_expression>`
lambda_square: Callable[[float], float] = lambda x: x * x

res_def = def_square(7.0)
res_lam = lambda_square(7.0)

print(f"  def_square(7):    {res_def}")
print(f"  lambda_square(7): {res_lam}")
print(f"  Lambda __name__:  '{lambda_square.__name__}' (Always '<lambda>')")

assert res_def == res_lam == 49.0
assert lambda_square.__name__ == "<lambda>"

# Explanation: Lambdas are syntactically restricted to a single expression.
# The result of that expression is implicitly returned. They cannot contain statements
# or multi-line blocks.


# ============================================================
# Q2: Custom Multi-Criteria Sorting with Lambdas
# ============================================================
# Question: Sort a list of student records:
# 1) Primary: Grade level descending
# 2) Secondary: GPA descending
# 3) Tertiary: Name ascending

print("\n=== Q2: Custom Sorting Key Functions ===")

students = [
    {"name": "Alice",   "grade": 12, "gpa": 3.85},
    {"name": "Bob",     "grade": 11, "gpa": 3.90},
    {"name": "Charlie", "grade": 12, "gpa": 3.95},
    {"name": "Diana",   "grade": 12, "gpa": 3.85},  # Tied with Alice on grade & gpa
    {"name": "Evan",    "grade": 11, "gpa": 3.70},
]

# Sort key returns a tuple: (-grade, -gpa, name)
students.sort(key=lambda s: (-s["grade"], -s["gpa"], s["name"]))

print("  Sorted Student Roster:")
for s in students:
    print(f"    Grade {s['grade']} | GPA {s['gpa']:.2f} | {s['name']}")

assert students[0]["name"] == "Charlie"  # Grade 12, GPA 3.95
assert students[1]["name"] == "Alice"    # Grade 12, GPA 3.85 (Alice < Diana)
assert students[2]["name"] == "Diana"    # Grade 12, GPA 3.85
assert students[3]["name"] == "Bob"      # Grade 11, GPA 3.90
assert students[4]["name"] == "Evan"     # Grade 11, GPA 3.70

# Explanation: Passing a lambda as `key=` allows concise tuple projection for multi-key
# lexicographical sorting without writing standalone helper functions.


# ============================================================
# Q3: The Late-Binding Closure Pitfall & Default Arg Fix
# ============================================================
# Question: Demonstrate the infamous closure bug where a list of lambdas created in a loop
# all evaluate to the loop's final value, and show the idiomatic default-argument fix (`i=i`).

print("\n=== Q3: Late-Binding Closure Pitfall & Fix ===")

# THE PITFALL: Lambdas look up variable `i` in the surrounding scope at CALL time, NOT definition time!
buggy_funcs = [lambda: i for i in range(5)]
buggy_outputs = [f() for f in buggy_funcs]
print(f"  Buggy lambda outputs: {buggy_outputs} (All evaluated to 4!)")
assert buggy_outputs == [4, 4, 4, 4, 4]

# THE FIX: Bind current loop value to a default parameter at definition time!
fixed_funcs = [lambda i=i: i for i in range(5)]
fixed_outputs = [f() for f in fixed_funcs]
print(f"  Fixed lambda outputs: {fixed_outputs} (Correctly evaluated 0..4)")
assert fixed_outputs == [0, 1, 2, 3, 4]

# Explanation: Python functions bind free variables by reference (lexical scope).
# When the lambdas execute later, the loop has already completed and `i` equals 4.
# Using a default argument `i=i` forces evaluation and creates a local snapshot.


# ============================================================
# Q4: Conditional Expressions inside Lambdas
# ============================================================
# Question: Implement a piecewise calculation (e.g. shipping fee calculation)
# using chained conditional ternary expressions inside a lambda.

print("\n=== Q4: Conditional Ternary Expressions in Lambdas ===")

# Free shipping over $100; $5 fee for $50-$100; $12 fee under $50
calc_shipping = lambda order_total: 0.0 if order_total >= 100.0 else (5.0 if order_total >= 50.0 else 12.0)

s1 = calc_shipping(120.0)
s2 = calc_shipping(75.0)
s3 = calc_shipping(30.0)

print(f"  Shipping on $120: ${s1:.2f}")
print(f"  Shipping on $75:  ${s2:.2f}")
print(f"  Shipping on $30:  ${s3:.2f}")

assert s1 == 0.0
assert s2 == 5.0
assert s3 == 12.0

# Explanation: Python allows the ternary conditional `A if condition else B` inside
# expressions, enabling branching logic inside single-expression lambdas.


# ============================================================
# Q5: Multi-Argument & Variadic Lambdas (*args, **kwargs)
# ============================================================
# Question: Define lambdas that accept variable positional arguments `*args` and
# keyword arguments `**kwargs`. Demonstrate defaults and keyword lookups.

print("\n=== Q5: Multi-Argument and Variadic Lambdas ===")

# Variadic arithmetic mean lambda
calc_average: Callable[..., float] = lambda *args: sum(args) / len(args) if args else 0.0

avg_vals = calc_average(10, 20, 30, 40)
avg_empty = calc_average()

print(f"  calc_average(10, 20, 30, 40) = {avg_vals}")
print(f"  calc_average()               = {avg_empty}")

assert avg_vals == 25.0
assert avg_empty == 0.0

# Lambda accepting **kwargs
formatter: Callable[..., str] = lambda prefix="INFO", **kwargs: f"[{prefix}] " + ", ".join(f"{k}={v}" for k, v in sorted(kwargs.items()))

log_str = formatter(prefix="DB_QUERY", table="orders", latency_ms=42)
print(f"  Kwargs formatted log: {log_str}")
assert log_str == "[DB_QUERY] latency_ms=42, table=orders"

# Explanation: Lambdas support identical parameter syntax to `def` functions:
# positional, defaults, `*args`, and `**kwargs`.


# ============================================================
# Q6: Functional Composition with Lambdas
# ============================================================
# Question: Implement a higher-order `compose` lambda that takes two functions `f` and `g`
# and returns a new composite function `h(x) = f(g(x))`. Pipe multiple operations.

print("\n=== Q6: Functional Composition ===")

# compose(f, g) returns x -> f(g(x))
compose = lambda f, g: lambda x: f(g(x))

strip_str = lambda s: s.strip()
uppercase_str = lambda s: s.upper()
add_brackets = lambda s: f"[{s}]"

# Compose: clean -> uppercase -> bracket
clean_and_upper = compose(uppercase_str, strip_str)
full_transform = compose(add_brackets, clean_and_upper)

raw_input = "   python learning repository   "
transformed = full_transform(raw_input)

print(f"  Raw:         '{raw_input}'")
print(f"  Transformed: '{transformed}'")

assert transformed == "[PYTHON LEARNING REPOSITORY]"

# Explanation: Composing unary lambdas allows building expressive data transformation
# pipelines without intermediate state variables.


# ============================================================
# Q7: Immediately Invoked Function Expressions (IIFE)
# ============================================================
# Question: Demonstrate an Immediately Invoked Function Expression (IIFE) in Python
# `(lambda ...: ...)(...)` to compute an isolated value without leaking temporary variable names.

print("\n=== Q7: Immediately Invoked Function Expressions (IIFE) ===")

# Compute Euclidean distance using an IIFE
distance = (lambda x1, y1, x2, y2: ((x2 - x1)**2 + (y2 - y1)**2)**0.5)(0, 0, 3, 4)

print(f"  Calculated distance via IIFE: {distance}")
assert distance == 5.0

# Initialize a config dictionary with computed constants without leaking scratch names
database_timeout = (lambda base_timeout, load_factor: base_timeout * (2 if load_factor > 0.8 else 1))(30, 0.95)
print(f"  Computed timeout: {database_timeout}s")
assert database_timeout == 60

# Explanation: Surrounding a lambda in parentheses followed immediately by arguments
# executes it in-place, scoping local parameters without polluting module scope.


# ============================================================
# Q8: Lambdas with Built-in Functional Utilities
# ============================================================
# Question: Demonstrate using lambdas with `map`, `filter`, `min`, `max`, and `sorted`.
# Extract the oldest active user from a list of user profiles.

print("\n=== Q8: Lambdas with Functional Built-ins ===")

user_accounts = [
    {"user": "Alice", "age": 28, "active": True},
    {"user": "Bob",   "age": 45, "active": False},
    {"user": "Carol", "age": 34, "active": True},
    {"user": "Dave",  "age": 19, "active": True},
]

# 1. filter() active users
active_users = list(filter(lambda u: u["active"], user_accounts))
assert len(active_users) == 3

# 2. max() by age among active users
oldest_active = max(active_users, key=lambda u: u["age"])
print(f"  Oldest active user: {oldest_active['user']} (Age: {oldest_active['age']})")
assert oldest_active["user"] == "Carol"
assert oldest_active["age"] == 34

# 3. min() by age among active users
youngest_active = min(active_users, key=lambda u: u["age"])
print(f"  Youngest active user: {youngest_active['user']} (Age: {youngest_active['age']})")
assert youngest_active["user"] == "Dave"

# Explanation: Combining lambdas with built-in functions like `min()` and `max()`
# with `key=` parameters avoids full list sorting when only extreme values are needed.


# ============================================================
# Q9: Lambdas vs operator Module (Performance Benchmark)
# ============================================================
# Question: Compare `lambda x: x['key']` against `operator.itemgetter('key')` in terms
# of syntax, readability, and execution speed in sorting.

print("\n=== Q9: Lambda vs operator.itemgetter Benchmark ===")

SAMPLE_SIZE = 50_000
records = [{"id": i, "val": -i} for i in range(SAMPLE_SIZE)]

# 1. Sorting using lambda key
rec_copy1 = list(records)
t0 = time.perf_counter()
rec_copy1.sort(key=lambda item: item["val"])
t_lambda = time.perf_counter() - t0

# 2. Sorting using operator.itemgetter
rec_copy2 = list(records)
t0 = time.perf_counter()
rec_copy2.sort(key=operator.itemgetter("val"))
t_operator = time.perf_counter() - t0

print(f"  Sort {SAMPLE_SIZE:,} items with lambda key:      {t_lambda * 1000:.3f} ms")
print(f"  Sort {SAMPLE_SIZE:,} items with operator module: {t_operator * 1000:.3f} ms")
print(f"  operator.itemgetter was {t_lambda / max(t_operator, 1e-9):.2f}x faster!")

assert rec_copy1 == rec_copy2
assert t_operator < t_lambda

# Explanation: `operator.itemgetter` is implemented directly in C, bypassing the
# Python bytecode evaluation loop and Python call stack frames used by lambdas.


# ============================================================
# Q10: Real-World Business Rules & Pricing Engine
# ============================================================
# Question: Implement a dynamic discount pricing engine driven by a collection of
# predicate-action lambda rules (e.g. VIP discount, bulk volume discount, holiday coupon).

print("\n=== Q10: Dynamic Pricing Discount Rule Engine ===")

class PricingEngine:
    def __init__(self):
        # List of rules: (rule_name, predicate_lambda, discount_action_lambda)
        self._rules: List[Tuple[str, Callable[[Dict[str, Any]], bool], Callable[[float], float]]] = []

    def add_rule(self, name: str,
                 predicate: Callable[[Dict[str, Any]], bool],
                 discount_fn: Callable[[float], float]) -> None:
        self._rules.append((name, predicate, discount_fn))

    def calculate_final_price(self, order: Dict[str, Any]) -> Tuple[float, List[str]]:
        current_price: float = float(order["base_price"])
        applied_rules: List[str] = []

        for name, predicate, discount_fn in self._rules:
            if predicate(order):
                current_price = discount_fn(current_price)
                applied_rules.append(name)

        return round(current_price, 2), applied_rules

engine = PricingEngine()

# Rule 1: VIP members get 15% off
engine.add_rule(
    "VIP_MEMBER_15%",
    lambda ord: ord.get("user_tier") == "VIP",
    lambda price: price * 0.85
)

# Rule 2: Bulk order (> 10 items) gets flat $20 discount
engine.add_rule(
    "BULK_ORDER_FLAT_20",
    lambda ord: ord.get("item_count", 0) >= 10,
    lambda price: max(0.0, price - 20.0)
)

# Rule 3: Black Friday promo code gives additional 10% off
engine.add_rule(
    "BLACK_FRIDAY_10%",
    lambda ord: ord.get("promo_code") == "BF2026",
    lambda price: price * 0.90
)

# Test Order 1: VIP user purchasing 12 items with promo code
order_1 = {"base_price": 200.0, "user_tier": "VIP", "item_count": 12, "promo_code": "BF2026"}
final_p1, applied_1 = engine.calculate_final_price(order_1)

# Math: 200 * 0.85 = 170.0 -> 170 - 20 = 150.0 -> 150 * 0.90 = 135.0
print(f"  Order 1 Final Price: ${final_p1:.2f} (Rules: {applied_1})")
assert final_p1 == 135.0
assert len(applied_1) == 3

# Test Order 2: Regular user with 3 items and no promo code
order_2 = {"base_price": 50.0, "user_tier": "STANDARD", "item_count": 3}
final_p2, applied_2 = engine.calculate_final_price(order_2)

print(f"  Order 2 Final Price: ${final_p2:.2f} (Rules: {applied_2})")
assert final_p2 == 50.0
assert len(applied_2) == 0

print("\nAll 10 lambda function questions executed and asserted successfully!")
