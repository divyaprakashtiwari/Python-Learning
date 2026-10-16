"""
Topic 02: Control Flow
Question 10: Structural Pattern Matching (match-case)

Master Python 3.10+ structural pattern matching: literal patterns, wildcard (_),
or-patterns (|), sequence unpacking, guard clauses (if), mapping/dict patterns,
class/dataclass patterns, starred rest patterns (*rest), expression evaluators,
and event-driven webhook dispatchers.
"""

from dataclasses import dataclass
from typing import Any

# ============================================================
# Q1: Literal Patterns, Value Matching, and Wildcards (_)
# ============================================================
# Question: Build an HTTP response handler that matches numeric status codes
# to descriptive responses using `match-case` and a wildcard default handler.

print("=== Q1: Literal Patterns & Wildcard ===")

def describe_http_status(status_code: int) -> str:
    """Matches HTTP status codes using literal patterns."""
    match status_code:
        case 200:
            return "200 OK: Request succeeded"
        case 201:
            return "201 Created: Resource created"
        case 400:
            return "400 Bad Request: Malformed syntax"
        case 401:
            return "401 Unauthorized: Authentication required"
        case 403:
            return "403 Forbidden: Insufficient permissions"
        case 404:
            return "404 Not Found: Resource does not exist"
        case 500:
            return "500 Internal Server Error: Server failure"
        case _:
            # Wildcard (_) matches any unmatched value
            return f"{status_code} Unknown Status Code"

test_codes = [200, 404, 500, 418]
for code in test_codes:
    print(f"  Status {code} -> {describe_http_status(code)}")

# Explanation: `match-case` replaces long `if-elif-else` chains.
# The `case _:` pattern is a wildcard that acts as the universal fallback catch-all.


# ============================================================
# Q2: Combined Alternatives with Or-Patterns (|)
# ============================================================
# Question: Classify file extensions into categories (Image, Audio, Code, Document)
# using or-patterns (`|`) to match multiple alternative values in a single case.

print("\n=== Q2: Or-Patterns with Pipe (|) ===")

def categorize_file(filename: str) -> str:
    """Categorizes file type based on extension using or-patterns."""
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    
    match ext:
        case "png" | "jpg" | "jpeg" | "gif" | "webp" | "svg":
            return "Raster / Vector Image Asset"
        case "mp3" | "wav" | "flac" | "aac" | "ogg":
            return "Digital Audio File"
        case "py" | "rs" | "go" | "js" | "ts" | "cpp":
            return "Source Code File"
        case "pdf" | "docx" | "md" | "txt":
            return "Document / Text Format"
        case _:
            return f"Unrecognized Extension (.{ext})"

test_files = ["main.py", "banner.webp", "track.flac", "notes.md", "archive.tar.gz"]
for f in test_files:
    print(f"  {f:<18} -> {categorize_file(f)}")

# Explanation: The pipe `|` in a case statement defines an or-pattern, matching
# any one of the listed alternatives without having to duplicate case bodies.


# ============================================================
# Q3: Sequence Matching and Variable Capture
# ============================================================
# Question: Parse 2D and 3D navigation commands using sequence pattern matching:
# `("move", x, y)`, `("move", x, y, z)`, and `("jump", height)`. Capture the coordinates.

print("\n=== Q3: Sequence Matching and Variable Capture ===")

def execute_command(command: tuple) -> str:
    """Unpacks command tuples and binds positional coordinates."""
    match command:
        case ("move", x, y):
            # 2D movement
            return f"Moved 2D: X={x:+d}, Y={y:+d}"
        case ("move", x, y, z):
            # 3D movement
            return f"Moved 3D: X={x:+d}, Y={y:+d}, Z={z:+d}"
        case ("jump", height):
            return f"Jumped vertically: Height={height}"
        case ("stop",):
            return "Halted movement"
        case _:
            return f"Invalid command signature: {command}"

actions = [
    ("move", 10, -5),
    ("move", 5, 20, 15),
    ("jump", 12),
    ("stop",),
    ("fly", 100),
]

for act in actions:
    print(f"  Action {str(act):<18} -> {execute_command(act)}")

# Explanation: Sequence patterns match lists and tuples. Variables in the pattern
# (e.g., `x`, `y`, `z`) automatically bind to the values at those exact positions.


# ============================================================
# Q4: Guard Clauses on Cases (`if condition`)
# ============================================================
# Question: Match 2D coordinates `(x, y)` and use guard clauses (`if`)
# to detect points along diagonal lines, axes, and quadrant signs.

print("\n=== Q4: Guard Clauses on Cases ===")

def analyze_point(point: tuple[int, int]) -> str:
    """Matches 2D points using structural decomposition and guard conditions."""
    match point:
        case (0, 0):
            return "Point at Origin"
        case (x, y) if x == y:
            return f"Point on Main Diagonal (y = x = {x})"
        case (x, y) if x == -y:
            return f"Point on Anti-Diagonal (y = -x = {y})"
        case (x, 0):
            return f"Point on X-Axis at {x}"
        case (0, y):
            return f"Point on Y-Axis at {y}"
        case (x, y) if x > 0 and y > 0:
            return f"Quadrant I ({x}, {y})"
        case (x, y) if x < 0 and y > 0:
            return f"Quadrant II ({x}, {y})"
        case (x, y) if x < 0 and y < 0:
            return f"Quadrant III ({x}, {y})"
        case (x, y) if x > 0 and y < 0:
            return f"Quadrant IV ({x}, {y})"
        case _:
            return "Invalid coordinate"

point_samples = [(0, 0), (5, 5), (-4, 4), (0, 8), (-3, -7)]
for pt in point_samples:
    print(f"  Point {str(pt):<10} -> {analyze_point(pt)}")

# Explanation: A guard `case pattern if condition:` evaluates the condition ONLY
# if the structural pattern matches. If the condition is False, matching falls through.


# ============================================================
# Q5: Dictionary and Mapping Pattern Matching
# ============================================================
# Question: Parse heterogeneous user event dictionaries:
# Extract specified keys while allowing extra arbitrary keys in the payload.

print("\n=== Q5: Dictionary / Mapping Patterns ===")

def process_event(event: dict) -> str:
    """Matches dictionary schemas and binds key values."""
    match event:
        case {"type": "login", "user": str(user), "ip": str(ip)}:
            return f"User '{user}' logged in from IP {ip}"
        case {"type": "purchase", "user": str(user), "amount": float(amt) | int(amt)}:
            return f"Purchase: '{user}' bought items totaling ${amt:.2f}"
        case {"type": "logout", "user": str(user)}:
            return f"User '{user}' logged out"
        case {"type": unknown_type, **extra}:
            return f"Unhandled event '{unknown_type}' with metadata keys: {list(extra.keys())}"
        case _:
            return "Malformed event packet (missing 'type' key)"

events_stream = [
    {"type": "login", "user": "alice_dev", "ip": "192.168.1.1", "device": "MacBook"},
    {"type": "purchase", "user": "bob_99", "amount": 89.50, "currency": "USD"},
    {"type": "logout", "user": "alice_dev"},
    {"type": "custom_metric", "cpu": 82.5, "ram": 45.1},
]

for ev in events_stream:
    print(f"  Event -> {process_event(ev)}")

# Explanation: Mapping patterns `{"key": pattern}` match dictionaries.
# Unlike sequences, mapping patterns do NOT require exhaustive matching: extra keys
# in the input dictionary are ignored unless captured with `**rest`.


# ============================================================
# Q6: Object and Dataclass Pattern Matching
# ============================================================
# Question: Define geometric shapes as dataclasses (Circle, Rectangle, Triangle)
# and compute their areas using class pattern matching.

print("\n=== Q6: Dataclass Pattern Matching ===")

import math

@dataclass
class Circle:
    radius: float

@dataclass
class Rectangle:
    width: float
    height: float

@dataclass
class Triangle:
    base: float
    height: float

def compute_shape_area(shape: Any) -> float:
    """Computes area by matching object class type and unpacking attributes."""
    match shape:
        case Circle(radius=r):
            return math.pi * (r ** 2)
        case Rectangle(width=w, height=h):
            return w * h
        case Triangle(base=b, height=h):
            return 0.5 * b * h
        case _:
            raise TypeError(f"Unknown shape type: {type(shape)}")

shapes = [Circle(radius=5.0), Rectangle(width=4.0, height=6.0), Triangle(base=8.0, height=3.0)]
for s in shapes:
    area = compute_shape_area(s)
    print(f"  Shape {s.__class__.__name__:<9} -> Area: {area:.2f}")

# Explanation: Class patterns inspect `isinstance(obj, ClassName)` and match attributes
# by keyword (e.g. `Circle(radius=r)`) or positional arguments if `__match_args__` is defined.


# ============================================================
# Q7: Starred Rest Patterns in Sequences
# ============================================================
# Question: Build a CLI command parser matching commands with variable argument lists:
# `["git", "commit", "-m", msg]`, `["git", "push", *options]`, and `["git", "checkout", branch]`.

print("\n=== Q7: Starred Rest Patterns ===")

def parse_cli_command(tokens: list[str]) -> str:
    """Parses shell CLI tokens with starred expressions."""
    match tokens:
        case ["git", "commit", "-m", msg]:
            return f"Git Commit with message: \"{msg}\""
        case ["git", "checkout", "-b", new_branch]:
            return f"Git Create & Checkout new branch: '{new_branch}'"
        case ["git", "checkout", branch]:
            return f"Git Checkout existing branch: '{branch}'"
        case ["git", "push", remote, branch, *flags]:
            flag_str = f" with flags {flags}" if flags else ""
            return f"Git Push to remote '{remote}', branch '{branch}'{flag_str}"
        case ["git", *unknown_args]:
            return f"Unknown git subcommand: {' '.join(unknown_args)}"
        case _:
            return f"Non-git command: {' '.join(tokens)}"

cli_inputs = [
    ["git", "commit", "-m", "Initial commit"],
    ["git", "checkout", "-b", "feature/auth"],
    ["git", "push", "origin", "main", "--force", "--tags"],
    ["git", "rebase", "main"],
]

for cmd in cli_inputs:
    print(f"  CLI: {' '.join(cmd):<35} -> {parse_cli_command(cmd)}")

# Explanation: Starred patterns `*flags` capture 0 or more elements into a list,
# mimicking sequence unpacking in function parameter lists.


# ============================================================
# Q8: Sub-pattern Binding with `as`
# ============================================================
# Question: Match and bind both the composite whole and its inner parts
# using the `as` pattern keyword.

print("\n=== Q8: Sub-pattern Binding with as ===")

def inspect_person_record(record: dict) -> str:
    """Binds composite sub-structures with 'as'."""
    match record:
        case {"name": str(name), "address": {"city": str(city), "zip": int()} as full_addr}:
            # 'full_addr' binds to the entire inner address dictionary!
            return f"Person: {name} | City: {city} | Full Address Object: {full_addr}"
        case {"name": str(name)}:
            return f"Person: {name} (No detailed address)"
        case _:
            return "Invalid person schema"

person_data = {
    "name": "David Miller",
    "address": {"street": "100 Pine St", "city": "Seattle", "zip": 98101}
}

print(f"  {inspect_person_record(person_data)}")

# Explanation: `pattern as name` allows capturing intermediate or nested values
# without needing redundant secondary dictionary lookups.


# ============================================================
# Q9: Recursive AST / Arithmetic Expression Evaluator
# ============================================================
# Question: Build an expression evaluator using match-case over nested tuples
# representing an Abstract Syntax Tree (AST): operations (+, -, *, /) and numeric leaves.

print("\n=== Q9: Recursive AST Expression Evaluator ===")

def evaluate_ast(node: Any) -> float:
    """Recursively evaluates an arithmetic AST expression."""
    match node:
        # Numeric base case
        case int(val) | float(val):
            return float(val)
            
        # Unary operations
        case ("neg", expr):
            return -evaluate_ast(expr)
        case ("abs", expr):
            return abs(evaluate_ast(expr))
            
        # Binary operations
        case ("+", left, right):
            return evaluate_ast(left) + evaluate_ast(right)
        case ("-", left, right):
            return evaluate_ast(left) - evaluate_ast(right)
        case ("*", left, right):
            return evaluate_ast(left) * evaluate_ast(right)
        case ("/", left, right):
            denom = evaluate_ast(right)
            if denom == 0:
                raise ZeroDivisionError("Division by zero in AST evaluation")
            return evaluate_ast(left) / denom
            
        case _:
            raise ValueError(f"Invalid AST node syntax: {node}")

# Expression: (10 + 5) * (20 - 4) / 2
# AST: ("/", ("*", ("+", 10, 5), ("-", 20, 4)), 2)
sample_ast = ("/", ("*", ("+", 10, 5), ("-", 20, 4)), 2)
ast_result = evaluate_ast(sample_ast)
print(f"  AST Expression: (10 + 5) * (20 - 4) / 2")
print(f"  Evaluated Result: {ast_result}")

# Unary expression: -abs(10 - 25)
unary_ast = ("neg", ("abs", ("-", 10, 25)))
print(f"  Unary AST -abs(10 - 25) = {evaluate_ast(unary_ast)}")

# Explanation: Pattern matching is ideal for tree traversals, interpreters,
# compilers, and state machines where data structures are deeply nested and heterogeneous.


# ============================================================
# Q10: Event-Driven Webhook Dispatcher
# ============================================================
# Question: Implement a production-grade webhook dispatcher that validates
# and routes incoming payment and customer life-cycle events with strict type checks.

print("\n=== Q10: Event-Driven Webhook Dispatcher ===")

def dispatch_webhook(payload: dict) -> dict:
    """Dispatches webhook payloads to specific business domain handlers."""
    match payload:
        # Payment Succeeded event
        case {
            "event": "payment.succeeded",
            "data": {"invoice_id": str(inv), "amount": int(cents) | float(cents), "currency": str(curr)}
        } if cents > 0:
            return {
                "status": "PROCESSED",
                "action": "CREDIT_ACCOUNT",
                "details": f"Credited {inv} with {cents / 100:.2f} {curr.upper()}"
            }

        # Payment Failed event with error details
        case {
            "event": "payment.failed",
            "data": {"invoice_id": str(inv), "error_code": str(err)}
        }:
            return {
                "status": "ALERTED",
                "action": "NOTIFY_CUSTOMER",
                "details": f"Invoice {inv} failed with code: {err}"
            }

        # Customer Subscription Cancelled
        case {
            "event": "customer.subscription.deleted",
            "data": {"customer_id": str(cust), "reason": str(reason)}
        }:
            return {
                "status": "PROCESSED",
                "action": "REVOKE_ACCESS",
                "details": f"Deactivated access for customer {cust} ({reason})"
            }

        # Unrecognized event schema
        case {"event": str(unknown_event), **extra}:
            return {
                "status": "IGNORED",
                "action": "LOG_UNHANDLED",
                "details": f"Ignoring event '{unknown_event}'"
            }

        # Malformed root payload
        case _:
            return {
                "status": "REJECTED",
                "action": "BAD_REQUEST",
                "details": "Invalid webhook payload structure"
            }

incoming_webhooks = [
    {"event": "payment.succeeded", "data": {"invoice_id": "INV-5521", "amount": 4900, "currency": "usd"}},
    {"event": "payment.failed", "data": {"invoice_id": "INV-8890", "error_code": "card_declined"}},
    {"event": "customer.subscription.deleted", "data": {"customer_id": "CUST-104", "reason": "user_cancelled"}},
    {"event": "dispute.created", "data": {"dispute_id": "DSP-01"}},
    {"invalid_key": "junk_data"},
]

for wb in incoming_webhooks:
    res = dispatch_webhook(wb)
    print(f"  [{res['status']:<9}] Action: {res['action']:<15} | {res['details']}")

# Summary Output
print("\n" + "=" * 55)
print("  All 10 Questions for Topic 02 - Q10 executed successfully!")
print("=" * 55)
