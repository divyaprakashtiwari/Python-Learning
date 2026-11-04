# Phase 4 — Topic 07: Polymorphism

## 1. Introduction

**Polymorphism** (from Greek *poly* = "many" and *morph* = "form") is the ability of different object types to respond to the **exact same method call, function, or operator** in their own type-specific way.

In Python, polymorphism appears in three major forms:
1. **Subtype Polymorphism:** Subclasses (`EmailNotifier`, `SMSNotifier`, `SlackWebhookNotifier`) override a shared base method (`.send_alert()`) so callers can treat all subclasses uniformly.
2. **Duck Typing & Structural Polymorphism (`typing.Protocol`):** Any object that implements the required methods (`.read()`) works—even without inheriting from a shared base class!
3. **Ad-Hoc Polymorphism (Operator Overloading & `@singledispatch`):** Operators (`+`, `*`, `len()`) and `@functools.singledispatch` functions adapt their behavior based on input types.

---

## 2. Why is it used?

- **Eliminating Fragile `if isinstance(...) elif isinstance(...)` Chains:** Instead of writing a giant `if/elif` block checking every notification type, polymorphic code simply calls `channel.send_alert(msg)`.
- **Open/Closed Principle (OCP):** Software becomes **open for extension, closed for modification**—you can add a new `PagerDutyNotifier` tomorrow without modifying a single line of `broadcast_incident()`.
- **Easy Unit Testing & Mocking (Duck Typing):** A test can pass an `InMemoryBuffer` into a function expecting a file stream without touching the real disk or network.

---

## 3. Syntax

```python
from typing import Protocol


# 1. Structural Polymorphism (Duck Typing with `typing.Protocol`)
class Renderable(Protocol):
    def render(self) -> str:
        ...


# 2. Polymorphic consumer function (works with ANY class implementing `.render()`)
def display_all(widgets: list[Renderable]) -> None:
    for w in widgets:
        print(w.render())
```

---

## 4. Explanation (Step-by-Step)

### Step 1: Subtype Polymorphism vs `if/elif` Type Switching
Compare these two designs:
```python
# ANTI-PATTERN: Must edit this function every time a new channel is added!
def send_bad(channel, msg):
    if isinstance(channel, EmailNotifier):
        channel.send_email(msg)
    elif isinstance(channel, SMSNotifier):
        channel.send_sms(msg)

# POLYMORPHIC PATTERN: Zero `if/elif` checks; extensible forever!
def send_good(channel: Notifier, msg: str) -> None:
    channel.send_alert(msg)
```

### Step 2: Duck Typing & `typing.Protocol` (PEP 544)
Python is dynamically typed and embraces **Duck Typing**: *"If it walks like a duck and quacks like a duck, it is a duck."*
- At runtime, `count_words_from_stream(stream)` only cares whether `stream.read()` exists and returns a `str`.
- To get static type checking (`mypy`/`pyright`) **without** forcing classes to inherit from a common base class, Python 3.8+ introduced **`typing.Protocol`** (Structural Subtyping). Adding `@runtime_checkable` even allows `isinstance(obj, ReadableStream)` at runtime!

### Step 3: `@functools.singledispatch` (Function Overloading by Type)
Because defining two functions with the same name in Python overwrites the first one, the standard library provides **`@functools.singledispatch`** to dispatch a function call to different registered implementations based on the runtime type of its first argument.

---

## 5. Minimum 3 Examples

### Example 1: Subtype Polymorphism (Uniform Interface Across a Class Hierarchy)
File: `example_01_subtype_polymorphism_hierarchy.py`

```python
class Notifier:
    """Base notification channel contract."""

    def send_alert(self, message: str) -> str:
        raise NotImplementedError("Subclasses must implement send_alert()")


class EmailNotifier(Notifier):
    def __init__(self, recipient_email: str) -> None:
        self.recipient_email = recipient_email

    def send_alert(self, message: str) -> str:
        return f"[EMAIL -> {self.recipient_email}] Subject: ALERT | Body: {message}"


class SMSNotifier(Notifier):
    def __init__(self, phone_number: str) -> None:
        self.phone_number = phone_number

    def send_alert(self, message: str) -> str:
        return f"[SMS   -> {self.phone_number}] {message[:60]}"


class SlackWebhookNotifier(Notifier):
    def __init__(self, channel: str) -> None:
        self.channel = channel

    def send_alert(self, message: str) -> str:
        return f"[SLACK -> #{self.channel}] :rotating_light: {message}"


def broadcast_incident(channels: list[Notifier], incident_msg: str) -> None:
    """
    Polymorphic dispatcher: knows NOTHING about Email, SMS, or Slack specifics!
    Simply invokes `channel.send_alert(incident_msg)` on every object.
    """
    for channel in channels:
        print(f"  {channel.send_alert(incident_msg)}")


def main() -> None:
    print("=== Subtype Polymorphism: Broadcasting Across Heterogeneous Channels ===")
    on_call_channels: list[Notifier] = [
        EmailNotifier("sre-team@techcorp.in"),
        SMSNotifier("+91-9876543210"),
        SlackWebhookNotifier("prod-incidents"),
    ]
    broadcast_incident(on_call_channels, "Database replica lag exceeded 30 seconds")


if __name__ == "__main__":
    main()
```

---

### Example 2: Duck Typing & Structural Polymorphism (`typing.Protocol`)
File: `example_02_duck_typing_and_protocols.py`

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class ReadableStream(Protocol):
    """Structural Protocol: ANY object with `read() -> str` satisfies this interface!"""

    def read(self) -> str:
        ...


class InMemoryBuffer:
    """Does NOT inherit from `ReadableStream`, yet implements `.read() -> str`."""

    def __init__(self, text: str) -> None:
        self.text = text

    def read(self) -> str:
        return self.text


class MockNetworkSocket:
    """Completely unrelated class that also implements `.read() -> str`."""

    def __init__(self, packet_payload: str) -> None:
        self.packet_payload = packet_payload

    def read(self) -> str:
        return f"SOCKET_DATA:{self.packet_payload}"


def count_words_from_stream(stream: ReadableStream) -> int:
    """Accepts ANY object that quacks like a `ReadableStream` (has `.read()`)."""
    content = stream.read()
    return len(content.split())


def main() -> None:
    print("=== Duck Typing & `typing.Protocol` Without Shared Inheritance ===")
    mem_buf = InMemoryBuffer("Python duck typing enables flexible polymorphism")
    net_sock = MockNetworkSocket("SYN ACK payload received from peer")

    for source in (mem_buf, net_sock):
        is_stream = isinstance(source, ReadableStream)
        words = count_words_from_stream(source)
        print(
            f"  {type(source).__name__:<18} | "
            f"satisfies Protocol={is_stream} | word_count={words}"
        )


if __name__ == "__main__":
    main()
```

---

### Example 3: Ad-Hoc Polymorphism (Operator Overloading & `@functools.singledispatch`)
File: `example_03_operator_and_builtin_polymorphism.py`

```python
from functools import singledispatch


class Money:
    """Supports polymorphic `+` operator via `__add__`."""

    def __init__(self, amount: float, currency: str = "INR") -> None:
        self.amount = round(amount, 2)
        self.currency = currency

    def __add__(self, other: "Money") -> "Money":
        if not isinstance(other, Money) or self.currency != other.currency:
            raise TypeError("Can only add Money instances of the same currency")
        return Money(self.amount + other.amount, self.currency)

    def __repr__(self) -> str:
        return f"Money({self.amount:.2f}, {self.currency!r})"


@singledispatch
def format_for_audit(value: object) -> str:
    """Default fallback implementation for arbitrary objects."""
    return f"OBJECT({value!r})"


@format_for_audit.register
def _(value: int) -> str:
    return f"INT({value:,})"


@format_for_audit.register
def _(value: list) -> str:
    return f"LIST(len={len(value)}, items={value})"


def main() -> None:
    print("=== 1. Operator Polymorphism (`+` on `int`, `str`, `list`, and `Money`) ===")
    print(f"  10 + 25                      = {10 + 25}")
    print(f"  'Py' + 'thon'                = {'Py' + 'thon'!r}")
    print(f"  Money(450) + Money(550)      = {Money(450) + Money(550)}")

    print("\n=== 2. Type-Based Function Dispatch (`@functools.singledispatch`) ===")
    for sample in (1250000, ["read", "write"], Money(99.50)):
        print(f"  {format_for_audit(sample)}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 1 (`example_01_subtype_polymorphism_hierarchy.py`)
```text
=== Subtype Polymorphism: Broadcasting Across Heterogeneous Channels ===
  [EMAIL -> sre-team@techcorp.in] Subject: ALERT | Body: Database replica lag exceeded 30 seconds
  [SMS   -> +91-9876543210] Database replica lag exceeded 30 seconds
  [SLACK -> #prod-incidents] :rotating_light: Database replica lag exceeded 30 seconds
```

### Output — Example 2 (`example_02_duck_typing_and_protocols.py`)
```text
=== Duck Typing & `typing.Protocol` Without Shared Inheritance ===
  InMemoryBuffer     | satisfies Protocol=True | word_count=6
  MockNetworkSocket  | satisfies Protocol=True | word_count=6
```

### Output — Example 3 (`example_03_operator_and_builtin_polymorphism.py`)
```text
=== 1. Operator Polymorphism (`+` on `int`, `str`, `list`, and `Money`) ===
  10 + 25                      = 35
  'Py' + 'thon'                = 'Python'
  Money(450) + Money(550)      = Money(1000.00, 'INR')

=== 2. Type-Based Function Dispatch (`@functools.singledispatch`) ===
  INT(1,250,000)
  LIST(len=2, items=['read', 'write'])
  OBJECT(Money(99.50, 'INR'))
```

---

## 7. Code Explanation

1. **Dynamic Dispatch (`example_01`):** Inside `broadcast_incident`, Python resolves `channel.send_alert` at runtime on each element of `on_call_channels` using `type(channel).__mro__`.
2. **`@runtime_checkable` `Protocol` (`example_02`):** Neither `InMemoryBuffer` nor `MockNetworkSocket` inherits from `ReadableStream`, yet `isinstance(source, ReadableStream)` returns `True` because both define a `.read()` method.
3. **`@singledispatch` (`example_03`):** `@format_for_audit.register` reads the type annotation `value: int` or `value: list` and registers type-specific overloads without touching the `int` or `list` classes.

---

## 8. Common Mistakes

1. **Checking `if type(x) == list:` before iterating instead of relying on Duck Typing / `Iterable`:**
   - Checking `type(x) == list` unnecessarily rejects tuples, sets, generators, and custom sequences. Accept any `Iterable` (or simply iterate in a `for` loop).
2. **Expecting C++/Java compile-time method overloading by parameter count inside a class:**
   - Defining `def pay(self, amount):` followed by `def pay(self, amount, currency):` in the same class overwrites the first `pay` method! Use default parameters (`def pay(self, amount: float, currency: str = "INR"):`) or `@functools.singledispatchmethod`.
3. **Breaking the Liskov Substitution Principle (LSP) by changing return types or raising unexpected errors in an overridden method:**
   - If `Notifier.send_alert()` is documented to return a `str`, a subclass whose `send_alert()` returns `None` or a `dict` will break polymorphic callers.

---

## 9. Practice Questions

1. **Easy — Polymorphic Shape Area Calculator:**
   Create `Circle(radius)`, `Rectangle(width, height)`, and `RightTriangle(base, height)` classes, each implementing `.area() -> float`. Write `total_canvas_area(shapes) -> float` that sums `.area()` across a mixed list of shapes.

2. **Medium — ` ClosableResource` Protocol:**
   Define a `@runtime_checkable class Closable(Protocol): def close(self) -> None: ...` and write `close_all(resources: list[Closable])` that safely closes three unrelated classes (`TempFile`, `DBCursor`, `AudioChannel`).

3. **Hard — JSON Serializer Using `@functools.singledispatch`:**
   Write a `@singledispatch` function `to_serializable(val)` with registered handlers for `set` (converts to sorted `list`), `datetime` (converts to `.isoformat()`), and `bytes` (converts via `.decode("utf-8")`).

---

## 10. Interview Questions

### Q1: What is the difference between Nominal Subtyping (`abc.ABC`) and Structural Subtyping (`typing.Protocol`) in Python?
**Answer:**
- **Nominal Subtyping (`abc.ABC`):** A class is considered a subtype **only if it explicitly declares inheritance** (`class MyStream(BaseStream):` or `BaseStream.register(MyStream)`).
- **Structural Subtyping (`typing.Protocol` / Duck Typing):** A class is considered a subtype **automatically if its structure (methods and attributes) matches the protocol**, even if it never imports or inherits from the `Protocol` class.

### Q2: Does Python support method overloading vs method overriding?
**Answer:**
- **Method Overriding (Runtime Polymorphism):** Fully supported—a subclass defines a method with the same name as a parent class method.
- **Method Overloading (Compile-Time Polymorphism):** Python does **not** support defining multiple methods with the same name and different parameter lists in the same class namespace (the last definition wins). Instead, Python achieves the same goal via **default arguments**, **`*args`/`**kwargs`**, **`@typing.overload`** (for static type checkers), and **`@functools.singledispatchmethod`** (for runtime dispatch by first-argument type).

### Q3: How does `len(obj)` work polymorphically on `str`, `list`, `dict`, and custom objects?
**Answer:**
Calling the built-in `len(obj)` invokes the object's **`obj.__len__()`** dunder method under the hood. Any custom class that implements `def __len__(self) -> int:` automatically works with `len(obj)` (and `bool(obj)` if `__bool__` is not defined).
