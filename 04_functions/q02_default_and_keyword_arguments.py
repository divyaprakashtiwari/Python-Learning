"""
Topic 04: Functions
Question 02: Default and Keyword Arguments (Deep Dive)

Master Python function argument semantics:
- The mutable default argument trap (def f(items=[])) & __defaults__ tuple
- Dynamic defaults (callables, timestamps, and None sentinels)
- Positional-only parameters syntax (/) introduced in PEP 570
- Keyword-only parameters syntax (*) introduced in PEP 3102
- The full parameter syntax signature: def f(pos_only, /, standard, *, kw_only)
- Safe keyword argument forwarding and config dictionary merging
- Runtime signature inspection using inspect.signature (Parameter kinds)
- Parameter default inheritance and LSP in class hierarchies
- Partial function application with functools.partial
- Production-grade HTTP Request Client with strict argument constraints
"""

import functools
import inspect
import time
from typing import Any, Callable, Dict, List, Optional, Tuple


# ============================================================
# Q1: The Mutable Default Argument Trap & __defaults__ Tuple
# ============================================================
# Question: Demonstrate the infamous mutable default argument trap (`def add_item(val, bucket=[])`).
# Inspect `__defaults__` to explain why state persists across calls, and demonstrate the idiomatic fix.

print("=== Q1: The Mutable Default Argument Trap ===")

# THE TRAP: Default values are evaluated ONCE when the `def` statement executes,
# NOT each time the function is called!
def buggy_append(val: int, target_list: List[int] = []) -> List[int]:
    target_list.append(val)
    return target_list

call1 = buggy_append(1)
call2 = buggy_append(2)
call3 = buggy_append(3)

print(f"  Buggy calls 1, 2, 3: {call3}")
print(f"  Underlying __defaults__: {buggy_append.__defaults__}")
assert call1 is call2 is call3
assert buggy_append.__defaults__[0] == [1, 2, 3]

# THE IDIOMATIC FIX: Default to None and initialize inside function body
def clean_append(val: int, target_list: Optional[List[int]] = None) -> List[int]:
    if target_list is None:
        target_list = []
    target_list.append(val)
    return target_list

clean1 = clean_append(1)
clean2 = clean_append(2)
clean3 = clean_append(3)

print(f"  Clean call 1: {clean1}")
print(f"  Clean call 2: {clean2}")
print(f"  Clean call 3: {clean3}")

assert clean1 == [1] and clean2 == [2] and clean3 == [3]
assert clean1 is not clean2

# Explanation: In Python, `def` is an executable statement. Default argument objects
# are stored in the function's `__defaults__` attribute upon definition and reused.


# ============================================================
# Q2: Dynamic Default Values via Callables & Timestamps
# ============================================================
# Question: Demonstrate why setting a default to `time.time()` or `datetime.now()`
# fails to record the time of invocation, and how to implement dynamic defaults.

print("\n=== Q2: Dynamic Defaults & Timestamp Sentinels ===")

# Buggy timestamp default: records definition time forever!
DEF_TIMESTAMP = time.time()
def buggy_log(msg: str, timestamp: float = DEF_TIMESTAMP) -> Tuple[str, float]:
    return msg, timestamp

# Correct dynamic timestamp pattern
def dynamic_log(msg: str, timestamp: Optional[float] = None) -> Tuple[str, float]:
    if timestamp is None:
        timestamp = time.time()
    return msg, timestamp

time.sleep(0.01)
_, t_buggy = buggy_log("Event A")
_, t_dynamic1 = dynamic_log("Event 1")
time.sleep(0.02)
_, t_dynamic2 = dynamic_log("Event 2")

print(f"  Buggy logged timestamp:     {t_buggy:.4f}")
print(f"  Dynamic event 1 timestamp:  {t_dynamic1:.4f}")
print(f"  Dynamic event 2 timestamp:  {t_dynamic2:.4f}")

assert t_buggy == DEF_TIMESTAMP
assert t_dynamic2 > t_dynamic1

# Explanation: Non-constant expressions used as default arguments are evaluated
# immediately when module loads. Always use `None` and compute dynamic values inside the body.


# ============================================================
# Q3: Positional-Only Parameters (PEP 570 `/` Syntax)
# ============================================================
# Question: Define a function with positional-only arguments using `/`.
# Demonstrate that callers cannot pass them as keyword arguments, allowing parameter
# renaming in internal implementations without breaking client code.

print("\n=== Q3: Positional-Only Parameters (/) ===")

def calculate_volume(length: float, width: float, height: float, /) -> float:
    """All parameters before '/' are strictly positional-only."""
    return length * width * height

# Valid positional invocation
vol = calculate_volume(2.0, 3.0, 4.0)
print(f"  calculate_volume(2, 3, 4) = {vol}")
assert vol == 24.0

# Calling with keyword arguments raises TypeError
caught_kw_error = False
try:
    calculate_volume(length=2.0, width=3.0, height=4.0)  # type: ignore
except TypeError as e:
    caught_kw_error = True
    print(f"  Caught expected TypeError: {e}")

assert caught_kw_error

# Explanation: Syntax `def f(a, b, /)` was introduced in Python 3.8. It prevents
# callers from coupling to parameter names and aligns with built-in C-extensions (like pow(), len()).


# ============================================================
# Q4: Keyword-Only Parameters (PEP 3102 `*` Syntax)
# ============================================================
# Question: Define a function that enforces keyword-only arguments using bare `*`.
# Prevent the "boolean blindness" anti-pattern where naked True/False arguments obscure readability.

print("\n=== Q4: Keyword-Only Parameters (*) ===")

# Bare '*' specifies that all subsequent parameters MUST be passed by name
def connect_database(host: str, port: int, *, use_ssl: bool = True, timeout: int = 30) -> Dict[str, Any]:
    return {"host": host, "port": port, "ssl": use_ssl, "timeout": timeout}

# Valid call: positional for host & port, keyword for options
conn = connect_database("db.internal", 5432, use_ssl=False, timeout=10)
print(f"  Connection configuration: {conn}")
assert conn["ssl"] is False and conn["timeout"] == 10

# Calling with positional boolean flag raises TypeError!
caught_pos_error = False
try:
    # connect_database("db.internal", 5432, False, 10)  # Illegal!
    connect_database("db.internal", 5432, False)  # type: ignore
except TypeError as e:
    caught_pos_error = True
    print(f"  Caught expected positional TypeError: {e}")

assert caught_pos_error

# Explanation: Keyword-only arguments force clarity at call sites, making code self-documenting
# and preventing argument transposition bugs.


# ============================================================
# Q5: Full Parameter Spectrum: (pos_only, /, standard, *, kw_only)
# ============================================================
# Question: Implement a function demonstrating all four parameter classifications
# in a single signature: positional-only, standard positional-or-keyword, and keyword-only.

print("\n=== Q5: Full Parameter Spectrum ===")

def full_spectrum_function(
    p_only: int,            # Positional-only
    /,
    p_or_k: str,           # Positional OR Keyword
    *,
    kw_only: float = 3.14  # Keyword-only
) -> Tuple[int, str, float]:
    return p_only, p_or_k, kw_only

# Case A: p_or_k passed positionally
res_a = full_spectrum_function(10, "Hello", kw_only=9.99)
print(f"  Case A (p_or_k positional): {res_a}")
assert res_a == (10, "Hello", 9.99)

# Case B: p_or_k passed as keyword
res_b = full_spectrum_function(20, p_or_k="World", kw_only=1.23)
print(f"  Case B (p_or_k keyword):    {res_b}")
assert res_b == (20, "World", 1.23)

# Case C: using default for kw_only
res_c = full_spectrum_function(30, "DefaultTest")
assert res_c == (30, "DefaultTest", 3.14)

# Explanation:
# Before '/' -> Positional-only
# Between '/' and '*' -> Positional or Keyword
# After '*' -> Keyword-only


# ============================================================
# Q6: Safe Keyword Argument Forwarding & Dict Merging
# ============================================================
# Question: Implement an options merger function that accepts explicit keyword overrides,
# merges them with default application configurations, and rejects unsupported options.

print("\n=== Q6: Safe Keyword Overrides & Merging ===")

DEFAULT_SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 8080,
    "debug": False,
    "workers": 4,
    "keepalive_sec": 60
}

def configure_server(**user_overrides: Any) -> Dict[str, Any]:
    # Check for invalid / unsupported keys
    invalid_keys = set(user_overrides.keys()) - set(DEFAULT_SERVER_CONFIG.keys())
    if invalid_keys:
        raise ValueError(f"Unsupported configuration options: {sorted(list(invalid_keys))}")

    # Merge defaults with user overrides using dictionary unpack operator
    merged_config = {**DEFAULT_SERVER_CONFIG, **user_overrides}
    return merged_config

custom_cfg = configure_server(port=9000, debug=True)
print(f"  Custom config: {custom_cfg}")
assert custom_cfg["port"] == 9000
assert custom_cfg["debug"] is True
assert custom_cfg["workers"] == 4  # Preserved from defaults

# Rejection test
caught_invalid = False
try:
    configure_server(unrecognized_opt="danger")
except ValueError as err:
    caught_invalid = True
    print(f"  Caught rejection: {err}")
assert caught_invalid

# Explanation: Combining `**kwargs` with whitelist validation allows flexible
# option passing while preventing silent typos in configuration keys.


# ============================================================
# Q7: Runtime Signature Introspection via inspect.signature
# ============================================================
# Question: Use Python's standard `inspect` module to analyze function parameters,
# default values, and parameter categories (POSITIONAL_ONLY, KEYWORD_ONLY, etc.).

print("\n=== Q7: Runtime Signature Introspection ===")

def sample_endpoint(entity_id: int, /, action: str, *, notify: bool = False, retries: int = 3) -> str:
    return f"{action} on {entity_id}"

sig = inspect.signature(sample_endpoint)
print(f"  Function signature: {sig}")

param_kinds = {}
for param_name, param in sig.parameters.items():
    default_val = "EMPTY" if param.default is inspect.Parameter.empty else param.default
    param_kinds[param_name] = (param.kind.name, default_val)
    print(f"    Parameter: {param_name:<10} | Kind: {param.kind.name:<25} | Default: {default_val}")

assert param_kinds["entity_id"][0] == "POSITIONAL_ONLY"
assert param_kinds["action"][0] == "POSITIONAL_OR_KEYWORD"
assert param_kinds["notify"][0] == "KEYWORD_ONLY"
assert param_kinds["notify"][1] is False
assert param_kinds["retries"][1] == 3

# Explanation: `inspect.signature` reveals the programmatic structure of functions,
# powering frameworks like FastAPI, Pydantic, and pytest dependency injection.


# ============================================================
# Q8: Default Arguments & Liskov Substitution Principle (LSP)
# ============================================================
# Question: Demonstrate how subclass method overrides must maintain compatible default
# arguments and parameter signatures to respect the Liskov Substitution Principle.

print("\n=== Q8: Default Arguments in Class Hierarchies ===")

class BaseNotifier:
    def send(self, message: str, priority: str = "NORMAL") -> str:
        return f"[BASE-{priority}] {message}"

class SlackNotifier(BaseNotifier):
    # Subclass can accept additional optional parameters with defaults,
    # but must NOT require additional mandatory parameters!
    def send(self, message: str, priority: str = "NORMAL", channel: str = "#general") -> str:
        return f"[SLACK-{channel}-{priority}] {message}"

def broadcast_alert(notifier: BaseNotifier, alert_text: str) -> str:
    # Caller only knows about BaseNotifier's interface!
    return notifier.send(alert_text)

base_res = broadcast_alert(BaseNotifier(), "System Alert")
slack_res = broadcast_alert(SlackNotifier(), "System Alert")

print(f"  Base output:  {base_res}")
print(f"  Slack output: {slack_res}")

assert base_res == "[BASE-NORMAL] System Alert"
assert slack_res == "[SLACK-#general-NORMAL] System Alert"

# Explanation: Subclasses may add new keyword arguments as long as sensible defaults
# are provided, ensuring any code expecting the base class continues to function without errors.


# ============================================================
# Q9: Partial Application with functools.partial
# ============================================================
# Question: Freeze specific arguments and default values using `functools.partial`.
# Compare behavior against manual wrapper functions and inspect frozen keywords.

print("\n=== Q9: Partial Function Application ===")

def calculate_discounted_price(price: float, discount_pct: float, tax_pct: float) -> float:
    discounted = price * (1.0 - discount_pct)
    total = discounted * (1.0 + tax_pct)
    return round(total, 2)

# Create specialized preset functions by fixing discount and tax
black_friday_price = functools.partial(calculate_discounted_price, discount_pct=0.30, tax_pct=0.08)
employee_price = functools.partial(calculate_discounted_price, discount_pct=0.20, tax_pct=0.08)

item_price = 100.0
bf_cost = black_friday_price(item_price)
emp_cost = employee_price(item_price)

print(f"  Base Price: ${item_price:.2f}")
print(f"  Black Friday (30% off + 8% tax): ${bf_cost:.2f}")
print(f"  Employee (20% off + 8% tax):     ${emp_cost:.2f}")
print(f"  Frozen keywords in black_friday_price: {black_friday_price.keywords}")

assert bf_cost == 75.60
assert emp_cost == 86.40
assert black_friday_price.keywords == {"discount_pct": 0.30, "tax_pct": 0.08}

# Explanation: `functools.partial` produces a callable with pre-bound arguments,
# optimizing code reuse and functional composition pipelines.


# ============================================================
# Q10: Production-Grade Configurable HTTP Client Simulator
# ============================================================
# Question: Implement a production-grade HTTP client simulator that strictly enforces:
# 1) Method and URL as positional-only
# 2) Payload data as optional positional-or-keyword
# 3) Timeout, retries, headers, and follow_redirects as strictly keyword-only with defaults.

print("\n=== Q10: Configurable HTTP Client Simulator ===")

def http_request(
    method: str,
    url: str,
    /,
    data: Optional[Dict[str, Any]] = None,
    *,
    headers: Optional[Dict[str, str]] = None,
    timeout: float = 10.0,
    retries: int = 3,
    follow_redirects: bool = True
) -> Dict[str, Any]:
    """
    Robust HTTP request simulator enforcing clear signature boundaries.
    """
    # Normalize inputs
    norm_method = method.upper()
    req_headers = {"User-Agent": "PyPracticeClient/1.0"}
    if headers:
        req_headers.update(headers)

    return {
        "method": norm_method,
        "url": url,
        "data": data or {},
        "headers": req_headers,
        "timeout": timeout,
        "retries": retries,
        "follow_redirects": follow_redirects,
        "status": 200,
        "body": f"Mock response from {url}"
    }

# 1. Standard GET request
get_resp = http_request("get", "https://api.github.com/users", timeout=5.0)
print(f"  GET response status:  {get_resp['status']} (timeout: {get_resp['timeout']}s)")
assert get_resp["method"] == "GET"
assert get_resp["timeout"] == 5.0
assert get_resp["headers"]["User-Agent"] == "PyPracticeClient/1.0"

# 2. POST request with body and custom headers
post_resp = http_request(
    "post",
    "https://api.internal/v1/orders",
    {"item_id": 42, "qty": 2},
    headers={"Authorization": "Bearer sec_token_123"},
    retries=5
)
print(f"  POST response method: {post_resp['method']}, retries: {post_resp['retries']}")
assert post_resp["method"] == "POST"
assert post_resp["data"] == {"item_id": 42, "qty": 2}
assert post_resp["headers"]["Authorization"] == "Bearer sec_token_123"
assert post_resp["retries"] == 5

# 3. Verify positional enforcement: passing method as keyword must raise TypeError
caught_kw_method = False
try:
    http_request(method="GET", url="https://api.org")  # type: ignore
except TypeError:
    caught_kw_method = True
assert caught_kw_method

print("\nAll 10 default and keyword arguments questions executed and asserted successfully!")
