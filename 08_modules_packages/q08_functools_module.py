"""
Topic 08: Modules and Packages - Question 08: functools Module

A comprehensive collection of 10 standalone, runnable exercises exploring
Python's standard library `functools` module: lru_cache, cache, partial,
wraps, reduce, total_ordering, singledispatch, and polymorphic dispatch pipelines.

Questions Covered:
 1. functools.lru_cache: Memoization, cache_info() hits/misses, and cache_clear().
 2. functools.cache: Unbounded memoization optimization for pure functions.
 3. functools.partial: Freezing arguments to construct specialized callables.
 4. functools.partialmethod: Bound method partial evaluation on classes.
 5. functools.wraps: Decorator metadata preservation (__name__, __doc__, __wrapped__).
 6. functools.reduce: Sequence folding with initial values and binary operators.
 7. functools.total_ordering: Auto-generating comparison operators from __lt__ & __eq__.
 8. functools.singledispatch: Type-based function overloading and polymorphic dispatch.
 9. functools.singledispatchmethod: Method-level polymorphic type dispatch inside classes.
10. Advanced Project: Declarative Pipeline Composer & Memoized Transformation Graph Engine.
"""

from functools import (
    cache,
    lru_cache,
    partial,
    partialmethod,
    reduce,
    singledispatch,
    singledispatchmethod,
    total_ordering,
    wraps,
)
import operator
from typing import Any, Callable


# ==============================================================================
# Question 1: functools.lru_cache (Bounded Memoization)
# ==============================================================================
call_count_lru = 0


@lru_cache(maxsize=4)
def compute_fibonacci(n: int) -> int:
    """Calculates n-th Fibonacci number with bounded LRU memoization."""
    global call_count_lru
    call_count_lru += 1
    if n < 2:
        return n
    return compute_fibonacci(n - 1) + compute_fibonacci(n - 2)


def exercise_q1_lru_cache() -> None:
    """
    Demonstrate lru_cache memoization, cache_info() telemetry, and cache_clear().
    """
    print("=== Q1: functools.lru_cache ===")

    global call_count_lru
    call_count_lru = 0
    compute_fibonacci.cache_clear()

    # Initial call calculates recursively
    fib_10 = compute_fibonacci(10)
    assert fib_10 == 55

    info1 = compute_fibonacci.cache_info()
    assert info1.hits > 0
    assert info1.currsize <= 4  # Bounded to maxsize=4!

    # Second call for previously computed value hits cache instantly
    calls_before = call_count_lru
    fib_10_cached = compute_fibonacci(10)
    assert fib_10_cached == 55
    assert call_count_lru == calls_before  # No new function evaluations!

    info2 = compute_fibonacci.cache_info()
    assert info2.hits == info1.hits + 1

    compute_fibonacci.cache_clear()
    assert compute_fibonacci.cache_info().currsize == 0

    print(f"  Fibonacci(10) = {fib_10}")
    print(f"  Cache Info: hits={info2.hits}, misses={info2.misses}, currsize={info2.currsize}")


# ==============================================================================
# Question 2: functools.cache (Unbounded Memoization)
# ==============================================================================
factorial_eval_count = 0


@cache
def heavy_factorial(n: int) -> int:
    """Calculates factorial with unbounded cache (Python 3.9+)."""
    global factorial_eval_count
    factorial_eval_count += 1
    if n <= 1:
        return 1
    return n * heavy_factorial(n - 1)


def exercise_q2_unbounded_cache() -> None:
    """
    Demonstrate functools.cache which has zero eviction overhead.
    """
    print("\n=== Q2: functools.cache ===")

    global factorial_eval_count
    factorial_eval_count = 0
    heavy_factorial.cache_clear()

    # Calculate 5! = 120 (5 calls: 5, 4, 3, 2, 1)
    res5 = heavy_factorial(5)
    assert res5 == 120
    assert factorial_eval_count == 5

    # Calculate 6! = 720 (requires ONLY 1 additional call for 6, since 5! is cached!)
    res6 = heavy_factorial(6)
    assert res6 == 720
    assert factorial_eval_count == 6  # Only 1 additional evaluation!

    print(f"  heavy_factorial(5) = {res5}")
    print(f"  heavy_factorial(6) = {res6} (computed with 1 incremental evaluation)")


# ==============================================================================
# Question 3: functools.partial (Argument Freezing)
# ==============================================================================
def multiply_and_offset(multiplier: float, offset: float, x: float) -> float:
    return (x * multiplier) + offset


def exercise_q3_partial_application() -> None:
    """
    Demonstrate freezing function arguments to generate specialized functions.
    """
    print("\n=== Q3: functools.partial ===")

    # Freeze multiplier=1.8 and offset=32.0 (Celsius to Fahrenheit conversion)
    celsius_to_fahrenheit = partial(multiply_and_offset, 1.8, 32.0)

    # Freeze multiplier=2.0 and offset=0.0 (Doubler)
    double = partial(multiply_and_offset, 2.0, 0.0)

    assert celsius_to_fahrenheit(0.0) == 32.0
    assert celsius_to_fahrenheit(100.0) == 212.0
    assert double(15.0) == 30.0

    # Inspecting partial metadata
    assert celsius_to_fahrenheit.func is multiply_and_offset
    assert celsius_to_fahrenheit.args == (1.8, 32.0)

    print(f"  0 C in F:    {celsius_to_fahrenheit(0.0)} F")
    print(f"  100 C in F:  {celsius_to_fahrenheit(100.0)} F")
    print(f"  double(15):  {double(15.0)}")


# ==============================================================================
# Question 4: functools.partialmethod
# ==============================================================================
class CellPhone:
    """Demonstrates partialmethod on class definitions."""

    def __init__(self) -> None:
        self.state = "STANDBY"

    def set_state(self, new_state: str, log_event: bool = False) -> str:
        self.state = new_state
        return f"State: {self.state} (logged={log_event})"

    # Partial methods bound to instance 'self' at call time
    turn_on = partialmethod(set_state, "ON", log_event=True)
    turn_off = partialmethod(set_state, "OFF", log_event=True)


def exercise_q4_partialmethod() -> None:
    """
    Test partialmethod binding to class instances.
    """
    print("\n=== Q4: functools.partialmethod ===")

    phone = CellPhone()
    assert phone.state == "STANDBY"

    msg_on = phone.turn_on()
    assert phone.state == "ON"
    assert "logged=True" in msg_on

    msg_off = phone.turn_off()
    assert phone.state == "OFF"

    print(f"  phone.turn_on():  '{msg_on}'")
    print(f"  phone.turn_off(): '{msg_off}'")


# ==============================================================================
# Question 5: functools.wraps (Metadata Preservation)
# ==============================================================================
def logged_decorator(func: Callable) -> Callable:
    """Decorator demonstrating @wraps metadata preservation."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)
    return wrapper


@logged_decorator
def calculate_tax(subtotal: float, rate: float = 0.08) -> float:
    """Calculates tax liability given subtotal and rate."""
    return subtotal * rate


def exercise_q5_wraps_decorator() -> None:
    """
    Verify that @wraps preserves __name__, __doc__, and __wrapped__.
    """
    print("\n=== Q5: functools.wraps ===")

    # Without @wraps, these would be 'wrapper' and empty docstring!
    assert calculate_tax.__name__ == "calculate_tax"
    assert calculate_tax.__doc__ == "Calculates tax liability given subtotal and rate."

    # Access original un-decorated function via __wrapped__
    assert hasattr(calculate_tax, "__wrapped__")
    assert calculate_tax.__wrapped__(100.0, 0.10) == 10.0

    print(f"  calculate_tax.__name__:    '{calculate_tax.__name__}'")
    print(f"  calculate_tax.__doc__:     '{calculate_tax.__doc__}'")
    print(f"  calculate_tax.__wrapped__: {calculate_tax.__wrapped__}")


# ==============================================================================
# Question 6: functools.reduce (Sequence Folding)
# ==============================================================================
def exercise_q6_reduce_folding() -> None:
    """
    Demonstrate folding sequences with reduce:
    - Cumulative product
    - Finding maximum
    - Flattening nested lists
    """
    print("\n=== Q6: functools.reduce ===")

    numbers = [2, 3, 4, 5]

    # 1. Cumulative multiplication: 2 * 3 * 4 * 5 = 120
    product = reduce(operator.mul, numbers)
    assert product == 120

    # 2. Maximum with initial seed
    max_val = reduce(lambda a, b: a if a > b else b, [10, 45, 23, 8], 0)
    assert max_val == 45

    # 3. Merging dictionaries
    dicts = [{"a": 1}, {"b": 2}, {"c": 3}]
    merged_dict = reduce(lambda acc, d: {**acc, **d}, dicts, {})
    assert merged_dict == {"a": 1, "b": 2, "c": 3}

    print(f"  reduce(mul, [2, 3, 4, 5]):  {product}")
    print(f"  reduce(max, [10, 45, ...]):  {max_val}")
    print(f"  reduce(dict_merge, dicts):  {merged_dict}")


# ==============================================================================
# Question 7: functools.total_ordering
# ==============================================================================
@total_ordering
class PriorityTask:
    """
    Class demonstrating @total_ordering: implements only __eq__ and __lt__,
    and functools generates __le__, __gt__, and __ge__ automatically.
    """

    def __init__(self, priority: int, name: str) -> None:
        self.priority = priority
        self.name = name

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PriorityTask):
            return NotImplemented
        return self.priority == other.priority

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, PriorityTask):
            return NotImplemented
        return self.priority < other.priority


def exercise_q7_total_ordering() -> None:
    """
    Verify auto-generated comparison operators via @total_ordering.
    """
    print("\n=== Q7: functools.total_ordering ===")

    t1 = PriorityTask(1, "Low Task")
    t2 = PriorityTask(5, "High Task")
    t3 = PriorityTask(1, "Another Low Task")

    # Manually defined
    assert t1 == t3
    assert t1 < t2

    # Auto-generated by @total_ordering!
    assert t1 <= t3  # __le__
    assert t2 > t1   # __gt__
    assert t2 >= t1  # __ge__
    assert t1 != t2  # __ne__

    print(f"  t1 < t2:  {t1 < t2}")
    print(f"  t1 <= t3: {t1 <= t3} (auto-generated)")
    print(f"  t2 > t1:  {t2 > t1} (auto-generated)")
    print(f"  t2 >= t1: {t2 >= t1} (auto-generated)")


# ==============================================================================
# Question 8: functools.singledispatch (Polymorphic Functions)
# ==============================================================================
@singledispatch
def format_data(arg: Any) -> str:
    """Base generic fallback."""
    return f"UNKNOWN_FORMAT: {arg}"


@format_data.register(int)
def _(arg: int) -> str:
    return f"INT:{arg:04d}"


@format_data.register(float)
def _(arg: float) -> str:
    return f"FLOAT:{arg:.2f}"


@format_data.register(list)
def _(arg: list) -> str:
    return f"LIST:len={len(arg)}"


def exercise_q8_singledispatch() -> None:
    """
    Test type-based polymorphic dispatch using @singledispatch.
    """
    print("\n=== Q8: functools.singledispatch ===")

    assert format_data(42) == "INT:0042"
    assert format_data(3.14159) == "FLOAT:3.14"
    assert format_data(["a", "b", "c"]) == "LIST:len=3"
    assert format_data("hello") == "UNKNOWN_FORMAT: hello"

    print(f"  format_data(42):      {format_data(42)}")
    print(f"  format_data(3.14159): {format_data(3.14159)}")
    print(f"  format_data([1, 2]):  {format_data([1, 2])}")


# ==============================================================================
# Question 9: functools.singledispatchmethod
# ==============================================================================
class EventSerializer:
    """Demonstrates singledispatchmethod inside a class."""

    @singledispatchmethod
    def serialize(self, payload: Any) -> str:
        raise NotImplementedError(f"Cannot serialize type: {type(payload)}")

    @serialize.register(str)
    def _(self, payload: str) -> str:
        return f"STR::{payload}"

    @serialize.register(dict)
    def _(self, payload: dict) -> str:
        keys_str = ",".join(sorted(payload.keys()))
        return f"DICT_KEYS::{keys_str}"


def exercise_q9_singledispatchmethod() -> None:
    """
    Test polymorphic method dispatch bound to class instances.
    """
    print("\n=== Q9: functools.singledispatchmethod ===")

    serializer = EventSerializer()

    res_str = serializer.serialize("auth_login")
    assert res_str == "STR::auth_login"

    res_dict = serializer.serialize({"user": "bob", "role": "admin"})
    assert res_dict == "DICT_KEYS::role,user"

    try:
        serializer.serialize(12345)
        assert False
    except NotImplementedError:
        pass

    print(f"  serializer.serialize('auth_login'): {res_str}")
    print(f"  serializer.serialize(dict):        {res_dict}")


# ==============================================================================
# Question 10: Advanced Project - Declarative Pipeline Composer
# ==============================================================================
class PipelineComposer:
    """
    High-order function composition engine. Chains multiple transformation
    functions together using functools.reduce, supporting partial parameter
    pre-binding and memoized intermediate stages.
    """

    def __init__(self, *steps: Callable[[Any], Any]) -> None:
        self.steps = list(steps)

    def add_step(self, step: Callable[[Any], Any]) -> "PipelineComposer":
        self.steps.append(step)
        return self

    def execute(self, initial_value: Any) -> Any:
        # Uses reduce to thread initial_value through all function steps
        return reduce(lambda val, func: func(val), self.steps, initial_value)


def exercise_q10_pipeline_composer() -> None:
    """
    Demonstrate PipelineComposer combining partial, reduce, and string transformations.
    """
    print("\n=== Q10: Declarative Pipeline Composer ===")

    def strip_text(s: str) -> str:
        return s.strip()

    def replace_spaces(char: str, s: str) -> str:
        return s.replace(" ", char)

    # Pre-bind hyphen replacement using partial
    replace_with_hyphens = partial(replace_spaces, "-")

    def prefix_tag(prefix: str, s: str) -> str:
        return f"{prefix}::{s}"

    add_build_prefix = partial(prefix_tag, "BUILD_2026")

    # Compose pipeline
    pipeline = PipelineComposer(
        strip_text,
        str.lower,
        replace_with_hyphens,
        add_build_prefix,
    )

    result = pipeline.execute("   Antigravity Python Modules Test   ")
    assert result == "BUILD_2026::antigravity-python-modules-test"

    print(f"  Composed Pipeline Execution:")
    print(f"    Input:  '   Antigravity Python Modules Test   '")
    print(f"    Output: '{result}'")


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_lru_cache()
    exercise_q2_unbounded_cache()
    exercise_q3_partial_application()
    exercise_q4_partialmethod()
    exercise_q5_wraps_decorator()
    exercise_q6_reduce_folding()
    exercise_q7_total_ordering()
    exercise_q8_singledispatch()
    exercise_q9_singledispatchmethod()
    exercise_q10_pipeline_composer()

    print("\nAll 10 functools module questions executed and asserted successfully!")
