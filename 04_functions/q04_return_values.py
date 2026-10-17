"""
Topic 04: Functions
Question 04: Return Values and Multiple Returns (Deep Dive)

Master return semantics in Python functions:
- Explicit return vs Bare return vs Implicit None
- Multiple return values (tuple packing and call-site unpacking)
- Self-documenting return types: NamedTuple and dataclass
- Result / Either pattern (graceful success/failure handling without uncaught exceptions)
- Returning dictionaries vs tuples for API contracts
- Returning functions from functions (Higher-Order Factory pattern)
- Fluent interfaces and method chaining (return self)
- Early returns vs Single Return Principle (cyclomatic complexity analysis)
- Generator returns: StopIteration value vs yield
- Real-world HTTP Gateway Response Builder with serialization and status codes
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, Generator, List, NamedTuple, Optional, Tuple, Union


# ============================================================
# Q1: Explicit Return vs Bare Return vs Implicit None
# ============================================================
# Question: Demonstrate the difference between returning an explicit value,
# a bare `return` (early exit), and dropping off the end of a function (implicit return).

print("=== Q1: Return Value Variations ===")

def calculate_square(x: int) -> int:
    return x * x  # Explicit return value

def early_exit_check(flag: bool) -> Optional[str]:
    if not flag:
        return  # Bare return: equivalent to 'return None'
    return "Flag was True"

def no_return_block() -> None:
    # Drops off the end without any return statement
    pass

val_sq = calculate_square(5)
val_bare = early_exit_check(False)
val_implicit = no_return_block()

print(f"  Explicit return: {val_sq} (type: {type(val_sq).__name__})")
print(f"  Bare return:     {val_bare} (type: {type(val_bare).__name__})")
print(f"  Implicit return: {val_implicit} (type: {type(val_implicit).__name__})")

assert val_sq == 25
assert val_bare is None
assert val_implicit is None

# Explanation: A bare `return` statement immediately terminates function execution
# and returns `None`. If execution falls off the end of a function suite, `None` is returned.


# ============================================================
# Q2: Multiple Returns via Automatic Tuple Packing
# ============================================================
# Question: Show that returning comma-separated values in Python implicitly packs them
# into an immutable tuple, and demonstrate positional unpacking with discard (_).

print("\n=== Q2: Multiple Returns & Tuple Packing ===")

def calculate_summary_stats(numbers: List[float]) -> Tuple[float, float, float, int]:
    """Returns minimum, maximum, mean average, and count."""
    if not numbers:
        raise ValueError("Cannot calculate stats on empty list")
    
    total = sum(numbers)
    count = len(numbers)
    # Comma-separated return automatically packs into a 4-element tuple
    return min(numbers), max(numbers), round(total / count, 2), count

data = [12.5, 45.0, 78.2, 99.0, 34.1]

# 1. Capture as a single packed tuple
stats_tuple = calculate_summary_stats(data)
print(f"  Packed return tuple: {stats_tuple} (type: {type(stats_tuple).__name__})")
assert isinstance(stats_tuple, tuple)
assert len(stats_tuple) == 4

# 2. Unpack into individual variables at call site
min_val, max_val, mean_val, n = calculate_summary_stats(data)
print(f"  Unpacked: min={min_val}, max={max_val}, mean={mean_val}, count={n}")
assert min_val == 12.5
assert max_val == 99.0
assert mean_val == 53.76
assert n == 5

# 3. Discard unneeded return values with underscore (_)
_, max_only, _, _ = calculate_summary_stats(data)
assert max_only == 99.0

# Explanation: In Python, `return a, b, c` creates a 3-element tuple `(a, b, c)`.
# The caller can unpack it directly into `x, y, z = func()`.


# ============================================================
# Q3: NamedTuple & Dataclass for Self-Documenting Returns
# ============================================================
# Question: Compare raw tuple returns against `NamedTuple` and `@dataclass` returns.
# Show how named fields eliminate index-ordering bugs and enable IDE auto-completion.

print("\n=== Q3: NamedTuple and Dataclass Return Types ===")

# 1. NamedTuple return type
class GeoCoordinate(NamedTuple):
    latitude: float
    longitude: float
    altitude_meters: float = 0.0

def get_facility_coordinates() -> GeoCoordinate:
    return GeoCoordinate(37.7749, -122.4194, 15.5)

geo = get_facility_coordinates()
print(f"  NamedTuple coordinate: lat={geo.latitude}, lon={geo.longitude}, alt={geo.altitude_meters}")
# NamedTuple supports both attribute access and tuple indexing/unpacking
assert geo.latitude == 37.7749
assert geo[0] == 37.7749
lat, lon, _ = geo
assert lat == 37.7749

# 2. Dataclass return type (mutable or frozen)
@dataclass(frozen=True)
class AuthenticationToken:
    access_token: str
    token_type: str
    expires_in_seconds: int

def issue_token(user_id: str) -> AuthenticationToken:
    return AuthenticationToken(
        access_token=f"jwt_{user_id}_secret_xyz",
        token_type="Bearer",
        expires_in_seconds=3600
    )

token_info = issue_token("usr_99")
print(f"  Dataclass token: {token_info.token_type} {token_info.access_token} (expires: {token_info.expires_in_seconds}s)")
assert token_info.token_type == "Bearer"
assert token_info.expires_in_seconds == 3600

# Explanation: While raw tuples rely on fragile positional indexes `result[2]`,
# `NamedTuple` and `dataclass` provide clear semantic property names with zero performance penalty.


# ============================================================
# Q4: Result / Either Pattern (Error Handling without Exceptions)
# ============================================================
# Question: Implement a functional `Result` class representing either `Ok(value)` or `Err(error)`.
# Use it to parse user integer input without crashing or throwing unhandled exceptions.

print("\n=== Q4: Result Monad Pattern (Ok / Err) ===")

class Result:
    def __init__(self, is_ok: bool, value: Any = None, error: Optional[str] = None):
        self.is_ok = is_ok
        self.value = value
        self.error = error

    @classmethod
    def ok(cls, value: Any) -> "Result":
        return cls(is_ok=True, value=value, error=None)

    @classmethod
    def err(cls, message: str) -> "Result":
        return cls(is_ok=False, value=None, error=message)

    def unwrap_or(self, default: Any) -> Any:
        return self.value if self.is_ok else default

    def __repr__(self) -> str:
        return f"Ok({self.value})" if self.is_ok else f"Err('{self.error}')"

def safe_parse_positive_int(raw: str) -> Result:
    """Safely converts string to positive int, returning Result instead of raising."""
    try:
        val = int(raw.strip())
        if val <= 0:
            return Result.err(f"Number must be strictly positive (got {val})")
        return Result.ok(val)
    except ValueError:
        return Result.err(f"Invalid integer string: '{raw}'")

res1 = safe_parse_positive_int("42")
res2 = safe_parse_positive_int("-5")
res3 = safe_parse_positive_int("not_a_number")

print(f"  Parse '42':           {res1} -> unwrap: {res1.unwrap_or(0)}")
print(f"  Parse '-5':           {res2} -> unwrap: {res2.unwrap_or(0)}")
print(f"  Parse 'not_a_number': {res3} -> unwrap: {res3.unwrap_or(0)}")

assert res1.is_ok and res1.value == 42
assert not res2.is_ok and "strictly positive" in str(res2.error)
assert not res3.is_ok and "Invalid integer" in str(res3.error)

# Explanation: The Result pattern makes error states explicit in the return signature,
# forcing callers to check `.is_ok` and preventing unexpected runtime crashes.


# ============================================================
# Q5: Returning Dictionaries for Extensible API Schemas
# ============================================================
# Question: Return structured dictionaries from business logic functions.
# Show how dictionaries allow backwards-compatible additions of fields without
# breaking callers who unpack variables.

print("\n=== Q5: Returning Dictionaries for API Contracts ===")

def calculate_invoice_breakdown(subtotal: float, discount_rate: float = 0.0, tax_rate: float = 0.08) -> Dict[str, float]:
    discount_amount = round(subtotal * discount_rate, 2)
    taxable_amount = subtotal - discount_amount
    tax_amount = round(taxable_amount * tax_rate, 2)
    grand_total = round(taxable_amount + tax_amount, 2)

    return {
        "subtotal": subtotal,
        "discount_amount": discount_amount,
        "taxable_amount": taxable_amount,
        "tax_amount": tax_amount,
        "grand_total": grand_total
    }

invoice = calculate_invoice_breakdown(200.0, discount_rate=0.10, tax_rate=0.08)
print(f"  Subtotal:   ${invoice['subtotal']:.2f}")
print(f"  Discount:   -${invoice['discount_amount']:.2f}")
print(f"  Tax (8%):   ${invoice['tax_amount']:.2f}")
print(f"  Grand Total:${invoice['grand_total']:.2f}")

assert invoice["subtotal"] == 200.0
assert invoice["discount_amount"] == 20.0
assert invoice["tax_amount"] == 14.40
assert invoice["grand_total"] == 194.40

# Explanation: Returning a dictionary or dataclass is far more maintainable than
# tuples when returning 4+ values, as new fields can be added without breaking unpack assignments.


# ============================================================
# Q6: Returning Functions from Functions (Factory Pattern)
# ============================================================
# Question: Implement a mathematical power factory `make_power_function(exponent)`
# and an authentication validator factory that returns specialized verification functions.

print("\n=== Q6: Returning Functions (Factory Pattern) ===")

def make_multiplier(factor: float) -> Callable[[float], float]:
    """Returns a newly configured multiplier function."""
    def multiplier(x: float) -> float:
        return x * factor
    return multiplier

double = make_multiplier(2.0)
triple = make_multiplier(3.0)
decuple = make_multiplier(10.0)

print(f"  double(15):  {double(15.0)}")
print(f"  triple(15):  {triple(15.0)}")
print(f"  decuple(15): {decuple(15.0)}")

assert double(15.0) == 30.0
assert triple(15.0) == 45.0
assert decuple(15.0) == 150.0

# Explanation: Functions are first-class values in Python. A function can construct
# and return an inner function that retains access to outer arguments via closures.


# ============================================================
# Q7: Fluent Interface / Method Chaining (return self)
# ============================================================
# Question: Implement a string query builder class where each mutation method
# returns `self` to allow continuous fluent method chaining.

print("\n=== Q7: Fluent Interface via 'return self' ===")

class TextQueryBuilder:
    def __init__(self, initial_text: str = ""):
        self._text = initial_text

    def append(self, text: str) -> "TextQueryBuilder":
        self._text += text
        return self  # Return self for chaining

    def strip_whitespace(self) -> "TextQueryBuilder":
        self._text = self._text.strip()
        return self

    def to_uppercase(self) -> "TextQueryBuilder":
        self._text = self._text.upper()
        return self

    def replace(self, old: str, new: str) -> "TextQueryBuilder":
        self._text = self._text.replace(old, new)
        return self

    def build(self) -> str:
        return self._text

# Fluent chained invocation
result_text = (
    TextQueryBuilder("   hello world   ")
    .strip_whitespace()
    .replace("world", "python")
    .to_uppercase()
    .append(" 2026")
    .build()
)

print(f"  Chained result: '{result_text}'")
assert result_text == "HELLO PYTHON 2026"

# Explanation: Returning `self` from mutator methods allows sequential dot-syntax
# chaining, creating expressive domain-specific languages (DSLs) like in SQLAlchemy or jQuery.


# ============================================================
# Q8: Early Return vs Single Exit Point Tradeoffs
# ============================================================
# Question: Contrast the traditional Single Entry Single Exit (SESE) style against
# modern Guard Clause Early Returns, demonstrating cyclomatic complexity differences.

print("\n=== Q8: Early Return vs Single Exit Point ===")

# Modern Early Return: low indentation, guards upfront
def validate_registration(username: str, age: int, has_accepted_terms: bool) -> Tuple[bool, str]:
    if len(username) < 3:
        return False, "Username too short"
    if age < 18:
        return False, "Must be at least 18 years old"
    if not has_accepted_terms:
        return False, "Terms and conditions must be accepted"
    
    return True, "Registration valid"

# Test cases
assert validate_registration("al", 25, True) == (False, "Username too short")
assert validate_registration("alice", 16, True) == (False, "Must be at least 18 years old")
assert validate_registration("alice", 25, False) == (False, "Terms and conditions must be accepted")
assert validate_registration("alice", 25, True) == (True, "Registration valid")

print("  Early return validation passed all assertion branches cleanly.")

# Explanation: Guard clauses with early returns avoid deep nested if/else pyramids,
# drastically reducing mental overhead and cognitive complexity.


# ============================================================
# Q9: Generator Returns & StopIteration Value
# ============================================================
# Question: Demonstrate that a generator function can use `return <value>`, and show
# how that return value is encapsulated inside `StopIteration.value`.

print("\n=== Q9: Generator Return & StopIteration.value ===")

def count_and_summarize(items: List[str]) -> Generator[str, None, int]:
    """Yields each item, and returns total count upon completion."""
    count = 0
    for item in items:
        yield item.upper()
        count += 1
    return count  # Attached to StopIteration.value!

gen = count_and_summarize(["apple", "banana", "cherry"])

# 1. Iterate through yielded values
yielded_items = []
return_value = None

while True:
    try:
        val = next(gen)
        yielded_items.append(val)
    except StopIteration as stop_err:
        return_value = stop_err.value
        break

print(f"  Yielded items: {yielded_items}")
print(f"  Generator return value (from StopIteration.value): {return_value}")

assert yielded_items == ["APPLE", "BANANA", "CHERRY"]
assert return_value == 3

# Explanation: In Python generators, `yield` outputs stream elements, while `return <val>`
# terminates the generator and attaches `<val>` to the `StopIteration.value` attribute.


# ============================================================
# Q10: Real-World HTTP Gateway Response Builder
# ============================================================
# Question: Implement a production-grade API gateway response serializer that produces
# standardized JSON-ready responses with HTTP status code, headers, payload, and error details.

print("\n=== Q10: HTTP Gateway Response Builder ===")

class ApiResponse:
    def __init__(self, status_code: int, data: Any = None, error: Optional[str] = None):
        self.status_code = status_code
        self.data = data
        self.error = error
        self.headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "X-Content-Type-Options": "nosniff"
        }

    def with_header(self, key: str, value: str) -> "ApiResponse":
        self.headers[key] = value
        return self

    def to_dict(self) -> Dict[str, Any]:
        """Serializes response into a canonical REST envelope."""
        is_success = 200 <= self.status_code < 300
        return {
            "status": self.status_code,
            "success": is_success,
            "data": self.data if is_success else None,
            "error": self.error if not is_success else None,
            "headers": self.headers
        }

def handle_user_lookup(user_id: int) -> ApiResponse:
    """Mock controller function returning standardized ApiResponse."""
    database = {
        1: {"id": 1, "name": "Alice Johnson", "role": "Engineer"},
        2: {"id": 2, "name": "Bob Smith", "role": "Designer"}
    }

    if user_id <= 0:
        return ApiResponse(400, error="Invalid user_id: ID must be positive").with_header("X-Error-Code", "ERR_INVALID_ID")

    user = database.get(user_id)
    if not user:
        return ApiResponse(404, error=f"User with ID {user_id} not found").with_header("X-Error-Code", "ERR_NOT_FOUND")

    return ApiResponse(200, data=user).with_header("Cache-Control", "max-age=3600")

# 1. Successful lookup
resp_ok = handle_user_lookup(1).to_dict()
print(f"  OK (200) Response:   success={resp_ok['success']}, user={resp_ok['data']['name']}")
assert resp_ok["status"] == 200
assert resp_ok["success"] is True
assert resp_ok["data"]["name"] == "Alice Johnson"
assert resp_ok["headers"]["Cache-Control"] == "max-age=3600"

# 2. Not Found lookup
resp_404 = handle_user_lookup(99).to_dict()
print(f"  404 Response:        success={resp_404['success']}, error={resp_404['error']}")
assert resp_404["status"] == 404
assert resp_404["success"] is False
assert resp_404["data"] is None
assert resp_404["headers"]["X-Error-Code"] == "ERR_NOT_FOUND"

# 3. Bad Request lookup
resp_400 = handle_user_lookup(-1).to_dict()
print(f"  400 Response:        success={resp_400['success']}, error={resp_400['error']}")
assert resp_400["status"] == 400
assert resp_400["success"] is False

print("\nAll 10 return values questions executed and asserted successfully!")
