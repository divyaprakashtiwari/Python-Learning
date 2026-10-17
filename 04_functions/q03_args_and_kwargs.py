"""
Topic 04: Functions
Question 03: *args and **kwargs (Deep Dive)

Master variable positional and keyword argument packing/unpacking in Python:
- *args tuple packing mechanics and iteration
- **kwargs dictionary packing mechanics
- Call-site unpacking with * (iterables) and ** (mappings)
- Universal wrapper function pattern (def wrapper(*args, **kwargs))
- Signature ordering: mandatory, *args, keyword-only, **kwargs
- Starred extended unpacking in expressions (PEP 3132)
- Multi-dictionary keyword collision and precedence merging
- Transparent function decorator with *args, **kwargs and functools.wraps
- Dynamic event emitter supporting heterogeneous subscriber signatures
- Production-grade dynamic SQL Query Builder utilizing *cols and **filters
"""

import functools
import time
from typing import Any, Callable, Dict, List, Optional, Tuple


# ============================================================
# Q1: *args Tuple Packing Mechanics
# ============================================================
# Question: Demonstrate how `*args` packs an arbitrary number of positional arguments
# into an immutable tuple. Show that args is an empty tuple `()` when no arguments are passed.

print("=== Q1: *args Tuple Packing ===")

def multiply_all(initial_factor: float, *numbers: float) -> float:
    """Multiplies initial_factor by all passed variable positional numbers."""
    print(f"  initial_factor: {initial_factor}, numbers type: {type(numbers).__name__}, value: {numbers}")
    result = initial_factor
    for n in numbers:
        result *= n
    return result

# Calling with multiple numbers
prod1 = multiply_all(2.0, 3.0, 4.0, 5.0)
print(f"  multiply_all(2, 3, 4, 5) -> {prod1}")
assert prod1 == 120.0

# Calling with NO additional numbers: *args is an empty tuple ()
prod2 = multiply_all(42.0)
print(f"  multiply_all(42) -> {prod2}")
assert prod2 == 42.0

# Explanation: The single asterisk `*` before a parameter name captures all excess
# positional arguments into an immutable `tuple`.


# ============================================================
# Q2: **kwargs Dictionary Packing Mechanics
# ============================================================
# Question: Demonstrate how `**kwargs` captures arbitrary named arguments into a standard
# dictionary. Show key lookup, iteration, and default retrieval.

print("\n=== Q2: **kwargs Dictionary Packing ===")

def build_html_tag(tag_name: str, content: str, **attributes: Any) -> str:
    """Constructs an HTML tag with arbitrary dynamic attributes."""
    attr_parts = []
    for key, value in sorted(attributes.items()):
        # Handle python reserved keywords (e.g., class_ -> class)
        clean_key = "class" if key == "class_" else key
        attr_parts.append(f'{clean_key}="{value}"')

    attr_str = f" {' '.join(attr_parts)}" if attr_parts else ""
    return f"<{tag_name}{attr_str}>{content}</{tag_name}>"

tag_simple = build_html_tag("p", "Hello world")
tag_complex = build_html_tag("a", "Click Here", href="https://python.org", id="main-link", class_="btn-primary")

print(f"  Simple tag:  {tag_simple}")
print(f"  Complex tag: {tag_complex}")

assert tag_simple == "<p>Hello world</p>"
assert tag_complex == '<a class="btn-primary" href="https://python.org" id="main-link">Click Here</a>'

# Explanation: Two asterisks `**` collect all unmatched keyword arguments into a standard
# Python `dict`. Iterating through `kwargs.items()` provides key-value pairs.


# ============================================================
# Q3: Call-Site Argument Unpacking (* and **)
# ============================================================
# Question: Demonstrate unpacking lists, tuples, sets, and dictionaries at the call site
# using `*` (iterable unpacking) and `**` (mapping unpacking).

print("\n=== Q3: Call-Site Unpacking (* and **) ===")

def create_box(width: float, height: float, depth: float, label: str = "Package") -> str:
    volume = width * height * depth
    return f"{label} (Vol: {volume:.1f} m^3)"

# Unpacking a list / tuple into positional arguments
dimensions_list = [2.0, 3.5, 4.0]
box_from_list = create_box(*dimensions_list)
print(f"  Unpacked from list: {box_from_list}")
assert box_from_list == "Package (Vol: 28.0 m^3)"

# Unpacking a dictionary into keyword arguments
box_kwargs = {"width": 1.5, "height": 2.0, "depth": 3.0, "label": "Container"}
box_from_dict = create_box(**box_kwargs)
print(f"  Unpacked from dict: {box_from_dict}")
assert box_from_dict == "Container (Vol: 9.0 m^3)"

# Mixed unpacking: 1 positional, rest unpacked from tuple, label overridden via kwargs
rem_dims = (5.0, 6.0)
box_mixed = create_box(2.0, *rem_dims, **{"label": "Cargo"})
print(f"  Mixed unpacking:    {box_mixed}")
assert box_mixed == "Cargo (Vol: 60.0 m^3)"

# Explanation: At invocation time, `*iterable` spreads elements into individual positional arguments,
# and `**mapping` spreads key-value pairs into individual keyword arguments.


# ============================================================
# Q4: The Universal Wrapper Pattern
# ============================================================
# Question: Implement a universal wrapper function that intercepts any function invocation,
# logs call arguments, executes the original function, and returns its result without modification.

print("\n=== Q4: Universal Wrapper Pattern ===")

call_audit_log: List[str] = []

def universal_audit_wrapper(target_fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Interception wrapper accepting arbitrary inputs for any target callable."""
    args_repr = ", ".join(repr(a) for a in args)
    kwargs_repr = ", ".join(f"{k}={repr(v)}" for k, v in sorted(kwargs.items()))
    all_params = ", ".join(filter(None, [args_repr, kwargs_repr]))

    call_audit_log.append(f"CALLED {target_fn.__name__}({all_params})")
    return target_fn(*args, **kwargs)

def add(a: int, b: int) -> int:
    return a + b

def format_greeting(first: str, last: str, title: str = "Mr.") -> str:
    return f"{title} {first} {last}"

r_add = universal_audit_wrapper(add, 15, 27)
r_greet = universal_audit_wrapper(format_greeting, "Guido", "van Rossum", title="Benevolent Dictator")

print(f"  Audit log entry 1: {call_audit_log[0]}")
print(f"  Audit log entry 2: {call_audit_log[1]}")

assert r_add == 42
assert r_greet == "Benevolent Dictator Guido van Rossum"
assert len(call_audit_log) == 2

# Explanation: The pattern `def f(*args, **kwargs): return target(*args, **kwargs)`
# provides 100% transparent forwarding for any Python signature.


# ============================================================
# Q5: Full Signature Ordering Spectrum
# ============================================================
# Question: Define a function illustrating the canonical ordering of parameter types:
# 1) Standard positional
# 2) *args
# 3) Keyword-only parameters (with and without defaults)
# 4) **kwargs

print("\n=== Q5: Parameter Ordering Rules ===")

def complex_signature(
    req_a: int,
    req_b: str,
    *extra_positional: float,
    mode: str = "standard",
    flag: bool,
    **extra_keywords: Any
) -> Dict[str, Any]:
    return {
        "req_a": req_a,
        "req_b": req_b,
        "extra_positional": extra_positional,
        "mode": mode,
        "flag": flag,
        "extra_keywords": extra_keywords
    }

res = complex_signature(
    100, "Core",
    1.1, 2.2, 3.3,           # Captured into *extra_positional
    mode="turbo",
    flag=True,               # Mandatory keyword-only
    ip="192.168.1.1",        # Captured into **extra_keywords
    timeout=60
)

print(f"  Complex invocation parsed:")
print(f"    req_a:            {res['req_a']}")
print(f"    extra_positional: {res['extra_positional']}")
print(f"    mode:             {res['mode']}")
print(f"    flag:             {res['flag']}")
print(f"    extra_keywords:   {res['extra_keywords']}")

assert res["req_a"] == 100
assert res["extra_positional"] == (1.1, 2.2, 3.3)
assert res["mode"] == "turbo"
assert res["flag"] is True
assert res["extra_keywords"] == {"ip": "192.168.1.1", "timeout": 60}

# Explanation: Python requires strict declaration order:
# positional parameters -> *args -> keyword-only parameters -> **kwargs.


# ============================================================
# Q6: Extended Starred Unpacking in Expressions (PEP 3132)
# ============================================================
# Question: Use starred expressions in assignment statements to unpack the head,
# tail, and variable middle segments of sequences, and merge multiple dictionaries.

print("\n=== Q6: Extended Starred Unpacking (PEP 3132) ===")

numbers_seq = [10, 20, 30, 40, 50, 60]

# 1. Unpack first, middle items, and last
first_item, *middle_items, last_item = numbers_seq
print(f"  First: {first_item}, Middle: {middle_items}, Last: {last_item}")
assert first_item == 10
assert middle_items == [20, 30, 40, 50]
assert last_item == 60

# 2. Unpack prefix and rest
head, *tail = [1, 2, 3]
assert head == 1 and tail == [2, 3]

# 3. Unpacking into lists and sets
combined_list = [0, *numbers_seq, 70, 80]
print(f"  Combined list: {combined_list}")
assert combined_list == [0, 10, 20, 30, 40, 50, 60, 70, 80]

# 4. Dictionary unpacking merge
defaults = {"theme": "light", "fontSize": 12, "showSidebar": True}
user_prefs = {"theme": "dark", "fontSize": 14}
final_prefs = {**defaults, **user_prefs}
print(f"  Merged dictionary preferences: {final_prefs}")
assert final_prefs == {"theme": "dark", "fontSize": 14, "showSidebar": True}

# Explanation: `*` unpacks any iterable into sequence literals. `**` unpacks mappings
# into dictionary literals, where later keys overwrite earlier keys.


# ============================================================
# Q7: Multi-Dictionary Keyword Collision & Precedence Merging
# ============================================================
# Question: Build a layered configuration resolver that accepts a base config and
# arbitrary keyword overrides from environment, files, and CLI flags with strict precedence.

print("\n=== Q7: Keyword Collision & Precedence Merging ===")

def resolve_layered_config(base_defaults: Dict[str, Any], *override_sources: Dict[str, Any], **cli_overrides: Any) -> Dict[str, Any]:
    """
    Layers configs in order of increasing precedence:
    base_defaults < override_sources[0] < override_sources[1] < ... < cli_overrides
    """
    resolved: Dict[str, Any] = dict(base_defaults)
    
    for src in override_sources:
        resolved.update(src)
        
    resolved.update(cli_overrides)
    return resolved

app_defaults = {"host": "localhost", "port": 8000, "log_level": "INFO", "cache": False}
file_config  = {"port": 8080, "log_level": "DEBUG"}
env_config   = {"port": 9000, "cache": True}

# CLI override has highest priority
active_config = resolve_layered_config(
    app_defaults,
    file_config,
    env_config,
    log_level="CRITICAL"  # CLI flag
)

print(f"  Resolved layered config: {active_config}")
assert active_config["host"] == "localhost"  # From base_defaults
assert active_config["port"] == 9000         # From env_config (beat file_config 8080)
assert active_config["cache"] is True        # From env_config
assert active_config["log_level"] == "CRITICAL"  # From CLI keyword override

# Explanation: Dict updates and keyword unpacking evaluate left-to-right, granting
# precedence to later arguments in the invocation chain.


# ============================================================
# Q8: Transparent Decorator with *args, **kwargs & functools.wraps
# ============================================================
# Question: Implement a performance benchmark decorator `time_it` that works on any
# function with arbitrary arguments, preserving docstrings and metadata.

print("\n=== Q8: Transparent Function Decorator ===")

def time_it(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start_time
        print(f"  [BENCHMARK] '{func.__name__}' executed in {elapsed * 1000:.3f} ms")
        return result
    return wrapper

@time_it
def compute_sum_of_squares(limit: int, step: int = 1) -> int:
    """Computes sum of squares up to limit."""
    return sum(x * x for x in range(0, limit, step))

res_sum = compute_sum_of_squares(50_000, step=2)
print(f"  Result of sum of squares: {res_sum}")
print(f"  Preserved function name:  {compute_sum_of_squares.__name__}")
print(f"  Preserved docstring:      '{compute_sum_of_squares.__doc__}'")

assert compute_sum_of_squares.__name__ == "compute_sum_of_squares"
assert compute_sum_of_squares.__doc__ == "Computes sum of squares up to limit."

# Explanation: `functools.wraps` copies `__name__`, `__doc__`, and `__annotations__`
# from target function to the wrapper, while `*args, **kwargs` ensures zero parameter distortion.


# ============================================================
# Q9: Dynamic Event Emitter with Heterogeneous Handler Signatures
# ============================================================
# Question: Implement an EventEmitter that safely invokes registered subscriber callbacks
# with `*args` and `**kwargs`, discarding unsupported keyword arguments using introspection.

print("\n=== Q9: Dynamic Event Emitter ===")

import inspect

class SafeEventEmitter:
    def __init__(self):
        self._listeners: Dict[str, List[Callable[..., Any]]] = {}

    def on(self, event_name: str, handler: Callable[..., Any]) -> None:
        self._listeners.setdefault(event_name, []).append(handler)

    def emit(self, event_name: str, *args: Any, **kwargs: Any) -> List[Any]:
        results = []
        handlers = self._listeners.get(event_name, [])
        for handler in handlers:
            sig = inspect.signature(handler)
            # If handler has **kwargs, pass everything
            has_var_kw = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
            if has_var_kw:
                call_kwargs = kwargs
            else:
                # Filter kwargs to only those accepted by handler
                call_kwargs = {k: v for k, v in kwargs.items() if k in sig.parameters}
            results.append(handler(*args, **call_kwargs))
        return results

emitter = SafeEventEmitter()

# Listener 1: accepts user and timestamp
def on_login_audit(user: str, timestamp: float) -> str:
    return f"AUDIT: {user} logged in at {timestamp:.0f}"

# Listener 2: accepts only user (ignores timestamp and extra fields!)
def on_login_notify(user: str) -> str:
    return f"NOTIFY: Welcome back, {user}!"

emitter.on("user_login", on_login_audit)
emitter.on("user_login", on_login_notify)

now = time.time()
dispatched = emitter.emit("user_login", user="alice", timestamp=now, ip="10.0.0.1")
print(f"  Listener 1 result: {dispatched[0]}")
print(f"  Listener 2 result: {dispatched[1]}")

assert dispatched[0].startswith("AUDIT: alice logged in")
assert dispatched[1] == "NOTIFY: Welcome back, alice!"

# Explanation: Inspecting subscriber signatures allows safely dispatching broad payloads
# with `**kwargs` without triggering `TypeError: unexpected keyword argument`.


# ============================================================
# Q10: Production-Grade Dynamic SQL Query Builder
# ============================================================
# Question: Implement a dynamic SQL query builder function `build_sql_query(table, *columns, **filters)`
# that converts variable columns and filters into parameterized SQL and parameter tuples.

print("\n=== Q10: Dynamic SQL Query Builder ===")

def build_sql_query(
    table_name: str,
    *columns: str,
    limit: Optional[int] = None,
    order_by: Optional[str] = None,
    **filters: Any
) -> Tuple[str, Tuple[Any, ...]]:
    """
    Builds a secure parameterized SQL query string and parameter tuple.
    Columns are passed via *columns; filtering criteria are passed via **filters.
    """
    # 1. Columns clause
    cols_clause = ", ".join(columns) if columns else "*"

    # 2. WHERE clause with parameterized '?' placeholders
    where_parts = []
    params = []
    for col, val in sorted(filters.items()):
        if val is None:
            where_parts.append(f"{col} IS NULL")
        else:
            where_parts.append(f"{col} = ?")
            params.append(val)

    where_clause = f" WHERE {' AND '.join(where_parts)}" if where_parts else ""

    # 3. ORDER BY clause
    order_clause = f" ORDER BY {order_by}" if order_by else ""

    # 4. LIMIT clause
    limit_clause = f" LIMIT {limit}" if limit is not None else ""

    query_str = f"SELECT {cols_clause} FROM {table_name}{where_clause}{order_clause}{limit_clause};"
    return query_str, tuple(params)

# Build a targeted query
sql, params = build_sql_query(
    "users",
    "id", "username", "email",
    role="admin",
    is_active=True,
    order_by="id ASC",
    limit=10
)

print(f"  Generated SQL: {sql}")
print(f"  Query Params:  {params}")

assert sql == "SELECT id, username, email FROM users WHERE is_active = ? AND role = ? ORDER BY id ASC LIMIT 10;"
assert params == (True, "admin")

# Build a fallback wildcard query
sql_all, params_all = build_sql_query("products")
print(f"  Wildcard SQL:  {sql_all}")
assert sql_all == "SELECT * FROM products;"
assert params_all == ()

print("\nAll 10 *args and **kwargs questions executed and asserted successfully!")
