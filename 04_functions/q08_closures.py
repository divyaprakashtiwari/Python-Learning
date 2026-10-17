"""
Topic 04: Functions
Question 08: Closures (Deep Dive)

Master Python closures and lexical state encapsulation:
- Anatomy of a closure: nested functions, free variables, and cell objects (__closure__)
- Stateful counter without classes or global variables
- Rolling average / statistical accumulator closure
- Explicit memoization cache closure (custom lru mechanics)
- Function factory for configurable text taggers
- Callback registration and listener notification via closures
- Sliding window / token bucket rate limiter closure
- Decorator mechanics: proving that decorators are closures
- Multi-variable closures and cell_contents introspection
- Production-grade Circuit Breaker pattern with error budgets and timeout resets
"""

import time
from typing import Any, Callable, Dict, List, Optional, Tuple


# ============================================================
# Q1: Anatomy of a Closure & `__closure__` Cell Objects
# ============================================================
# Question: Define a minimal closure. Inspect the inner function's `__closure__` attribute,
# `__code__.co_freevars`, and access the captured value via `.cell_contents`.

print("=== Q1: Anatomy of a Closure & Cell Objects ===")

def make_greeting_closure(greeting_prefix: str) -> Callable[[str], str]:
    # 'greeting_prefix' is a free variable captured in the inner function's closure
    def greeter(name: str) -> str:
        return f"{greeting_prefix}, {name}!"
    return greeter

hello_greeter = make_greeting_closure("Hello")
welcome_greeter = make_greeting_closure("Welcome to Python")

res_hello = hello_greeter("Alice")
res_welcome = welcome_greeter("Bob")

print(f"  hello_greeter('Alice'):  '{res_hello}'")
print(f"  welcome_greeter('Bob'):  '{res_welcome}'")

# Introspect the closure mechanics
free_vars = hello_greeter.__code__.co_freevars
closure_cells = hello_greeter.__closure__
captured_val = closure_cells[0].cell_contents if closure_cells else None

print(f"  Free variable names: {free_vars}")
print(f"  Closure cells count: {len(closure_cells) if closure_cells else 0}")
print(f"  Cell contents:       '{captured_val}'")

assert res_hello == "Hello, Alice!"
assert res_welcome == "Welcome to Python, Bob!"
assert free_vars == ("greeting_prefix",)
assert captured_val == "Hello"

# Explanation: A closure occurs when an inner function retains access to variables
# from its enclosing scope even after the outer function has finished executing.
# Python stores these in a tuple of `cell` objects on `__closure__`.


# ============================================================
# Q2: Stateful Counter Closure (Data Hiding without Classes)
# ============================================================
# Question: Implement an auto-incrementing ID generator closure. Demonstrate that multiple
# instances maintain completely isolated state and cannot be tampered with directly.

print("\n=== Q2: Stateful Auto-Increment Closure ===")

def create_counter(start: int = 1, step: int = 1) -> Callable[[], int]:
    current = start

    def counter() -> int:
        nonlocal current
        val = current
        current += step
        return val

    return counter

counter_a = create_counter(start=100, step=5)
counter_b = create_counter(start=1, step=1)

# Advance counter A
a1, a2, a3 = counter_a(), counter_a(), counter_a()
# Advance counter B
b1, b2 = counter_b(), counter_b()

print(f"  Counter A (starts 100, step 5): {a1}, {a2}, {a3}")
print(f"  Counter B (starts 1, step 1):   {b1}, {b2}")

assert (a1, a2, a3) == (100, 105, 110)
assert (b1, b2) == (1, 2)
# Counter A continues independently
assert counter_a() == 115

# Explanation: Closures provide true private encapsulation. External code cannot
# directly rebind or corrupt `current` without calling the returned function.


# ============================================================
# Q3: Rolling Average / Statistical Accumulator Closure
# ============================================================
# Question: Implement a rolling average tracker closure that updates its cumulative sum
# and element count in O(1) time without retaining all historical numbers in a list.

print("\n=== Q3: Rolling Average Accumulator Closure ===")

def make_averager() -> Callable[[float], float]:
    total: float = 0.0
    count: int = 0

    def averager(new_val: float) -> float:
        nonlocal total, count
        total += new_val
        count += 1
        return round(total / count, 3)

    return averager

avg = make_averager()
val1 = avg(10.0)
val2 = avg(20.0)
val3 = avg(30.0)
val4 = avg(5.0)

print(f"  After 10: {val1}")
print(f"  After 20: {val2}")
print(f"  After 30: {val3}")
print(f"  After 5:  {val4}")

assert val1 == 10.0
assert val2 == 15.0
assert val3 == 20.0
assert val4 == 16.25

# Explanation: By maintaining running scalars (`total`, `count`) inside the closure cell,
# the rolling average operates in O(1) time and O(1) auxiliary memory space.


# ============================================================
# Q4: Explicit Memoization Cache Closure
# ============================================================
# Question: Write a manual memoization closure `memoize(fn)` from scratch using a
# dictionary cell. Track cache hits and misses without external libraries.

print("\n=== Q4: Memoization Cache Closure ===")

def memoize(fn: Callable[..., Any]) -> Tuple[Callable[..., Any], Callable[[], Dict[str, int]]]:
    cache: Dict[Tuple[Any, ...], Any] = {}
    stats = {"hits": 0, "misses": 0}

    def memoized_fn(*args: Any) -> Any:
        if args in cache:
            stats["hits"] += 1
            return cache[args]
        
        stats["misses"] += 1
        result = fn(*args)
        cache[args] = result
        return result

    def get_stats() -> Dict[str, int]:
        return dict(stats)

    return memoized_fn, get_stats

def expensive_computation(x: int, y: int) -> int:
    return (x ** 3) + (y ** 3)

cached_comp, get_cache_stats = memoize(expensive_computation)

# First run: Cache misses
r1 = cached_comp(2, 3)
r2 = cached_comp(4, 5)

# Second run: Cache hits
r3 = cached_comp(2, 3)
r4 = cached_comp(4, 5)
r5 = cached_comp(2, 3)

print(f"  Computation (2, 3): {r1}")
print(f"  Cache Stats:        {get_cache_stats()}")

assert r1 == r3 == r5 == 35
assert r2 == r4 == 189
assert get_cache_stats() == {"hits": 3, "misses": 2}

# Explanation: The dictionary `cache` and dictionary `stats` persist in the closure cell,
# allowing transparent caching across invocations.


# ============================================================
# Q5: Configurable Function Factory (HTML Tag Generator)
# ============================================================
# Question: Build an HTML tag generator factory that produces specialized tag functions
# (e.g., `make_tag('h1')`, `make_tag('div')`) with custom CSS classes and attributes.

print("\n=== Q5: Configurable Function Factory ===")

def make_tag(tag_name: str, default_class: Optional[str] = None) -> Callable[[str], str]:
    def render(content: str, **attrs: Any) -> str:
        all_attrs = []
        if default_class and "class_" not in attrs:
            all_attrs.append(f'class="{default_class}"')

        for k, v in sorted(attrs.items()):
            attr_key = "class" if k == "class_" else k
            all_attrs.append(f'{attr_key}="{v}"')

        attr_str = f" {' '.join(all_attrs)}" if all_attrs else ""
        return f"<{tag_name}{attr_str}>{content}</{tag_name}>"

    return render

h1_tagger = make_tag("h1", default_class="page-title")
btn_tagger = make_tag("button", default_class="btn-primary")
div_tagger = make_tag("div")

out_h1 = h1_tagger("Welcome")
out_btn = btn_tagger("Submit", id="submit-btn")
out_div = div_tagger("Container content", id="main-wrap")

print(f"  H1:     {out_h1}")
print(f"  Button: {out_btn}")
print(f"  Div:    {out_div}")

assert out_h1 == '<h1 class="page-title">Welcome</h1>'
assert out_btn == '<button class="btn-primary" id="submit-btn">Submit</button>'
assert out_div == '<div id="main-wrap">Container content</div>'

# Explanation: Function factories parameterize behavior at creation time, yielding
# specialized, reusable functions without repetitive boilerplate.


# ============================================================
# Q6: Event Callback Registry via Closures
# ============================================================
# Question: Implement a lightweight pub-sub event registry closure that allows registering
# callbacks and dispatching events, keeping the subscriber list strictly private.

print("\n=== Q6: Event Callback Registry via Closures ===")

def create_event_bus():
    subscribers: Dict[str, List[Callable[[Any], None]]] = {}

    def subscribe(event_type: str, handler: Callable[[Any], None]) -> Callable[[], None]:
        subscribers.setdefault(event_type, []).append(handler)
        # Return an un-subscriber closure!
        def unsubscribe() -> None:
            if handler in subscribers.get(event_type, []):
                subscribers[event_type].remove(handler)
        return unsubscribe

    def publish(event_type: str, data: Any) -> int:
        handlers = subscribers.get(event_type, [])
        for h in list(handlers):
            h(data)
        return len(handlers)

    return subscribe, publish

subscribe, publish = create_event_bus()
audit_events: List[str] = []

unsub_1 = subscribe("ORDER_PLACED", lambda order_id: audit_events.append(f"Email sent for #{order_id}"))
unsub_2 = subscribe("ORDER_PLACED", lambda order_id: audit_events.append(f"Warehouse alerted for #{order_id}"))

# Publish first event (both handlers invoked)
publish("ORDER_PLACED", 1001)
print(f"  Audit events after 1st order: {audit_events}")
assert len(audit_events) == 2

# Unsubscribe email handler using returned closure
unsub_1()
publish("ORDER_PLACED", 1002)
print(f"  Audit events after 2nd order (email unsubscribed): {audit_events}")
assert len(audit_events) == 3
assert audit_events[-1] == "Warehouse alerted for #1002"

# Explanation: The returned un-subscriber closure captures its specific handler
# reference and outer subscribers list, cleanly implementing disposal mechanics.


# ============================================================
# Q7: Rate Limiter Closure (Token Bucket / Sliding Window)
# ============================================================
# Question: Implement an API rate-limiter closure that enforces a maximum of `max_calls`
# within a specified `window_seconds`. Fast-fail with `False` when the budget is exhausted.

print("\n=== Q7: Rate Limiter Closure ===")

def make_rate_limiter(max_calls: int, window_seconds: float) -> Callable[[], bool]:
    timestamps: List[float] = []

    def allow_request() -> bool:
        nonlocal timestamps
        now = time.time()
        # Evict timestamps older than the sliding window
        cutoff = now - window_seconds
        timestamps = [t for t in timestamps if t > cutoff]

        if len(timestamps) < max_calls:
            timestamps.append(now)
            return True
        return False

    return allow_request

# Allow at most 3 requests in a 1.0 second window
limiter = make_rate_limiter(max_calls=3, window_seconds=1.0)

# Make 3 fast requests: should all pass
call_1 = limiter()
call_2 = limiter()
call_3 = limiter()
# 4th request in the same window should be rejected
call_4 = limiter()

print(f"  Call 1 allowed: {call_1}")
print(f"  Call 2 allowed: {call_2}")
print(f"  Call 3 allowed: {call_3}")
print(f"  Call 4 allowed: {call_4} (Rate limit exceeded!)")

assert call_1 and call_2 and call_3
assert not call_4

# Explanation: State is retained in the `timestamps` closure cell across calls,
# enabling real-time throttling without external state databases.


# ============================================================
# Q8: Proving Decorators are Closures
# ============================================================
# Question: Demonstrate that a standard Python function decorator is literally a closure.
# Inspect the wrapper function's `__closure__` to confirm it holds the wrapped function.

print("\n=== Q8: Decorators as Closures ===")

def prefix_logger(prefix: str):
    # Outer factory closure
    def decorator(func: Callable[..., Any]):
        # Inner decorator closure
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            return f"{prefix} -> {result}"
        return wrapper
    return decorator

@prefix_logger("[AUDIT_LOG]")
def multiply(a: int, b: int) -> int:
    return a * b

output = multiply(6, 7)
print(f"  Decorated multiply(6, 7): '{output}'")
assert output == "[AUDIT_LOG] -> 42"

# Inspect the wrapper's closure cells
closure_objs = [cell.cell_contents for cell in multiply.__closure__]
print(f"  Captured objects in wrapper.__closure__: {closure_objs}")

# The closure holds both the original function object and the prefix string!
assert any(callable(obj) and obj.__name__ == "multiply" for obj in closure_objs)
assert "[AUDIT_LOG]" in closure_objs

# Explanation: Python's `@decorator` syntax is syntactic sugar for `fn = decorator(fn)`.
# The resulting `wrapper` is a closure retaining references to `fn` and configuration values.


# ============================================================
# Q9: Multi-Variable Closures & Cell Introspection
# ============================================================
# Question: Create a closure that binds multiple variables of different types (int, list, dict).
# Verify each variable is mapped to a distinct cell object with correct type.

print("\n=== Q9: Multi-Variable Closure Cells ===")

def complex_closure_factory(multiplier: int, tags: List[str], config: Dict[str, bool]):
    def worker(data: int) -> Tuple[int, List[str], Dict[str, bool]]:
        return data * multiplier, tags, config
    return worker

worker_fn = complex_closure_factory(10, ["prod", "us-east"], {"secure": True})
r_val, r_tags, r_cfg = worker_fn(5)

cells = worker_fn.__closure__
print(f"  Total captured cells: {len(cells)}")
cell_types = [type(c.cell_contents).__name__ for c in cells]
print(f"  Captured types:       {cell_types}")

assert len(cells) == 3
assert r_val == 50
assert r_tags == ["prod", "us-east"]
assert r_cfg == {"secure": True}

# Explanation: Each free variable in the enclosing scope gets its own independent
# `cell` in the closure's `__closure__` tuple.


# ============================================================
# Q10: Production-Grade Circuit Breaker Pattern via Closure
# ============================================================
# Question: Implement a production-grade Circuit Breaker using a closure.
# Support states: CLOSED (normal), OPEN (fast-failing after failure threshold),
# and recovery after a cooldown timeout.

print("\n=== Q10: Circuit Breaker Pattern via Closure ===")

def make_circuit_breaker(
    target_service: Callable[..., Any],
    failure_threshold: int = 3,
    recovery_timeout: float = 0.5
) -> Callable[..., Any]:
    """
    States:
      - CLOSED: requests pass through normally; failures increment failure_count.
      - OPEN: requests fast-fail immediately without calling target_service.
      - HALF-OPEN: after recovery_timeout, try a probe request.
    """
    failure_count = 0
    state = "CLOSED"
    last_failure_time = 0.0

    def call_service(*args: Any, **kwargs: Any) -> Dict[str, Any]:
        nonlocal failure_count, state, last_failure_time
        now = time.time()

        # Check if circuit should transition from OPEN to HALF-OPEN
        if state == "OPEN":
            if now - last_failure_time >= recovery_timeout:
                state = "HALF-OPEN"
            else:
                return {"success": False, "circuit_state": "OPEN", "error": "Circuit is OPEN: fast-failing"}

        try:
            result = target_service(*args, **kwargs)
            # Success in CLOSED or HALF-OPEN resets circuit to pristine CLOSED state
            failure_count = 0
            state = "CLOSED"
            return {"success": True, "circuit_state": state, "data": result}
        except Exception as exc:
            failure_count += 1
            last_failure_time = now
            if failure_count >= failure_threshold:
                state = "OPEN"
            return {"success": False, "circuit_state": state, "error": str(exc)}

    return call_service

# Mock flaky microservice
unstable_mode = True
def mock_payment_api(amount: float) -> str:
    if unstable_mode:
        raise ConnectionError("Payment gateway timed out")
    return f"Processed ${amount:.2f}"

breaker = make_circuit_breaker(mock_payment_api, failure_threshold=2, recovery_timeout=0.1)

# Call 1: First failure (CLOSED state, count=1)
r1 = breaker(100.0)
print(f"  Call 1: state={r1['circuit_state']}, success={r1['success']}")
assert r1["circuit_state"] == "CLOSED" and not r1["success"]

# Call 2: Second failure -> Trips circuit to OPEN!
r2 = breaker(100.0)
print(f"  Call 2: state={r2['circuit_state']}, success={r2['success']}")
assert r2["circuit_state"] == "OPEN" and not r2["success"]

# Call 3: Immediate call fast-fails without even calling service!
r3 = breaker(100.0)
print(f"  Call 3: state={r3['circuit_state']}, error='{r3['error']}'")
assert r3["circuit_state"] == "OPEN"
assert "fast-failing" in r3["error"]

# Sleep past recovery timeout and restore service stability
time.sleep(0.15)
unstable_mode = False

# Call 4: Probe succeeds, circuit transitions back to CLOSED!
r4 = breaker(100.0)
print(f"  Call 4: state={r4['circuit_state']}, data='{r4['data']}'")
assert r4["circuit_state"] == "CLOSED"
assert r4["success"] is True
assert r4["data"] == "Processed $100.00"

print("\nAll 10 closure questions executed and asserted successfully!")
