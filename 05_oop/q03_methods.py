"""
Topic 05: Object-Oriented Programming (OOP)
Question 03: Methods: Instance, Class, and Static (Deep Dive)

Master Python method types and dispatch mechanics:
- Tripartite method comparison: instance method (self) vs @classmethod (cls) vs @staticmethod
- Alternative constructors and factory patterns with @classmethod
- Utility functions and logical grouping with @staticmethod
- Subclass polymorphism preservation in @classmethod factory methods (cls vs Class)
- Runtime method binding introspection: bound methods vs unbound functions (__self__, __func__)
- Dynamic method injection: class-wide vs single-instance binding (types.MethodType)
- Calling parent class methods with super()
- Method chaining via fluent 'return self' (Builder pattern)
- Method overriding and parameter compatibility
- Production-grade domain entity: TimestampedEvent with diverse serialization factories
"""

import datetime
import types
from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar


# ============================================================
# Q1: Tripartite Method Comparison (Instance vs Class vs Static)
# ============================================================
# Question: Define a class illustrating all three method types in Python:
# 1) Instance method: takes `self`, accesses/modifies instance state
# 2) Class method: takes `cls` via `@classmethod`, accesses/modifies class state
# 3) Static method: takes no implicit first argument via `@staticmethod`, self-contained logic

print("=== Q1: Method Types Comparison ===")

class TemperatureSensor:
    sensor_model = "TempGuard-v3"
    total_readings_taken = 0

    def __init__(self, sensor_id: str, current_celsius: float):
        self.sensor_id = sensor_id
        self.celsius = current_celsius

    # 1. Instance Method: binds to 'self'
    def read_temperature(self) -> float:
        TemperatureSensor.total_readings_taken += 1
        return self.celsius

    # 2. Class Method: binds to 'cls'
    @classmethod
    def get_model_info(cls) -> str:
        return f"Model: {cls.sensor_model} (Total readings across fleet: {cls.total_readings_taken})"

    # 3. Static Method: no implicit self/cls parameter
    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        return round((celsius * 9.0 / 5.0) + 32.0, 2)

sensor = TemperatureSensor("SENSOR_01", 25.0)

# 1. Call instance method
curr_temp = sensor.read_temperature()
print(f"  Instance method read: {curr_temp} deg C")
assert curr_temp == 25.0
assert TemperatureSensor.total_readings_taken == 1

# 2. Call class method via class and instance
cls_info = TemperatureSensor.get_model_info()
print(f"  Class method info:   {cls_info}")
assert "TempGuard-v3" in cls_info

# 3. Call static method via class and instance
f_temp = TemperatureSensor.celsius_to_fahrenheit(25.0)
f_temp_inst = sensor.celsius_to_fahrenheit(25.0)
print(f"  Static conversion:   25 deg C = {f_temp} deg F")
assert f_temp == f_temp_inst == 77.0

# Explanation:
# - Instance methods require an instance (`self`) to operate on object state.
# - Class methods receive the class (`cls`) and are often used as factories or class mutators.
# - Static methods receive no implicit receiver, acting as plain functions namespaced in the class.


# ============================================================
# Q2: Alternative Constructors with @classmethod
# ============================================================
# Question: Build a `DateRecord` class with standard `__init__(year, month, day)`.
# Provide alternative constructors: `from_iso_string("2026-10-17")` and `from_timestamp(epoch)`.

print("\n=== Q2: Alternative Constructors with @classmethod ===")

class DateRecord:
    def __init__(self, year: int, month: int, day: int):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def from_iso_string(cls, date_str: str) -> "DateRecord":
        """Factory: parse YYYY-MM-DD string into an instance of cls."""
        parts = [int(p) for p in date_str.strip().split("-")]
        if len(parts) != 3:
            raise ValueError(f"Invalid ISO format: '{date_str}'")
        return cls(parts[0], parts[1], parts[2])

    @classmethod
    def from_timestamp(cls, epoch_seconds: float) -> "DateRecord":
        """Factory: convert epoch seconds into an instance of cls."""
        dt = datetime.datetime.fromtimestamp(epoch_seconds)
        return cls(dt.year, dt.month, dt.day)

    def to_iso(self) -> str:
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d}"

d1 = DateRecord(2026, 10, 17)
d2 = DateRecord.from_iso_string("2026-12-25")
d3 = DateRecord.from_timestamp(1792213200)

print(f"  Standard init:   {d1.to_iso()}")
print(f"  from_iso_string: {d2.to_iso()}")
print(f"  from_timestamp:  {d3.to_iso()}")

assert d1.to_iso() == "2026-10-17"
assert d2.to_iso() == "2026-12-25"
assert d3.year == 2026

# Explanation: In Python, you cannot overload `__init__` with multiple signatures.
# `@classmethod` alternative constructors provide idiomatic, descriptive factory methods.


# ============================================================
# Q3: Utility Helpers with @staticmethod
# ============================================================
# Question: Implement a `ValidationUtils` class containing `@staticmethod` methods
# for email format validation, password strength checking, and sanitization.

print("\n=== Q3: Utility Helpers with @staticmethod ===")

class Validator:
    @staticmethod
    def is_valid_email(email: str) -> bool:
        email = email.strip()
        if "@" not in email or "." not in email:
            return False
        user, domain = email.split("@", 1)
        return bool(user) and "." in domain and not domain.startswith(".") and not domain.endswith(".")

    @staticmethod
    def sanitize_phone(phone: str) -> str:
        # Strip all non-digit characters
        return "".join(c for c in phone if c.isdigit())

v_ok = Validator.is_valid_email("dev@python.org")
v_bad = Validator.is_valid_email("not-an-email")
phone_clean = Validator.sanitize_phone("+1 (555) 234-5678")

print(f"  'dev@python.org' valid: {v_ok}")
print(f"  'not-an-email' valid:   {v_bad}")
print(f"  Sanitized phone:        '{phone_clean}'")

assert v_ok is True
assert v_bad is False
assert phone_clean == "15552345678"

# Explanation: Use `@staticmethod` when a function logically belongs to a class's
# namespace, but does not read or modify instance (`self`) or class (`cls`) state.


# ============================================================
# Q4: Subclass Polymorphism in @classmethod Factories (cls vs Class)
# ============================================================
# Question: Demonstrate why using `cls(...)` inside a classmethod is essential for
# inheritance polymorphism, whereas hardcoding `BaseClass(...)` breaks subclass factory instantiation.

print("\n=== Q4: Subclass Polymorphism in @classmethod ===")

class Document:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    @classmethod
    def from_text(cls, raw_text: str):
        # Uses cls(...) dynamically!
        first_line, *rest = raw_text.strip().split("\n")
        body = "\n".join(rest)
        return cls(first_line, body)

class LegalContract(Document):
    def __init__(self, title: str, content: str, jurisdiction: str = "US"):
        super().__init__(title, content)
        self.jurisdiction = jurisdiction

raw_doc = "NDA Agreement\nParty A and Party B agree to..."

# Call from_text on base Document
doc_base = Document.from_text(raw_doc)
print(f"  Document.from_text type:     {type(doc_base).__name__}")
assert type(doc_base) is Document

# Call from_text on subclass LegalContract: cls is dynamically LegalContract!
contract = LegalContract.from_text(raw_doc)
print(f"  LegalContract.from_text type:{type(contract).__name__}")
assert type(contract) is LegalContract
assert isinstance(contract, Document)
assert contract.jurisdiction == "US"

# Explanation: Because `from_text` called `cls(...)` instead of `Document(...)`,
# subclasses automatically inherit the factory and instantiate instances of their own class.


# ============================================================
# Q5: Inspecting Method Binding at Runtime (__self__, __func__)
# ============================================================
# Question: Inspect bound methods vs unbound functions at runtime.
# Access the underlying raw function via `__func__` and the bound instance via `__self__`.

print("\n=== Q5: Runtime Method Binding Introspection ===")

class Greeter:
    def greet(self, target: str) -> str:
        return f"Hello, {target}"

g = Greeter()

# Accessing via class yields an unbound function in Python 3
unbound_fn = Greeter.greet
# Accessing via instance yields a BOUND METHOD
bound_method = g.greet

print(f"  Greeter.greet type:  {type(unbound_fn).__name__}")
print(f"  g.greet type:        {type(bound_method).__name__}")

assert type(unbound_fn) is types.FunctionType
assert type(bound_method) is types.MethodType

# Inspect bound method descriptors
print(f"  bound_method.__self__: {bound_method.__self__} (Matches instance g: {bound_method.__self__ is g})")
print(f"  bound_method.__func__: {bound_method.__func__} (Matches Greeter.greet: {bound_method.__func__ is unbound_fn})")

assert bound_method.__self__ is g
assert bound_method.__func__ is unbound_fn

# Explanation: In Python, retrieving a function through an instance triggers the descriptor
# protocol (`function.__get__(instance, owner)`), binding `instance` to `self`.


# ============================================================
# Q6: Dynamic Method Injection (Class-Wide vs Single Instance)
# ============================================================
# Question: Demonstrate attaching a new method dynamically at runtime:
# 1) To the class: affects ALL current and future instances
# 2) To a single specific instance using `types.MethodType`

print("\n=== Q6: Dynamic Method Injection ===")

class Robot:
    def __init__(self, name: str):
        self.name = name

bot1 = Robot("Atlas")
bot2 = Robot("Titan")

# 1. Attach method to the class (affects ALL instances)
def class_speak(self) -> str:
    return f"{self.name} says beep boop!"

Robot.speak = class_speak  # Injected into class dictionary

print(f"  Class injection -> bot1: '{bot1.speak()}', bot2: '{bot2.speak()}'")
assert bot1.speak() == "Atlas says beep boop!"
assert bot2.speak() == "Titan says beep boop!"

# 2. Attach specialized method to a single specific instance only!
def fly(self) -> str:
    return f"{self.name} is flying through the air!"

# Use types.MethodType to bind function to bot1
bot1.fly = types.MethodType(fly, bot1)

print(f"  Instance injection -> bot1.fly(): '{bot1.fly()}'")
assert bot1.fly() == "Atlas is flying through the air!"

# bot2 does NOT have the fly method
assert not hasattr(bot2, "fly")

# Explanation: Setting an attribute on a class injects a function into `Class.__dict__`.
# To attach a method to a single instance without affecting other instances, bind it with `types.MethodType(func, instance)`.


# ============================================================
# Q7: Cooperative Method Extension with super()
# ============================================================
# Question: Implement a multi-stage logging notifier using `super()` to extend
# base class behavior before and after the super call.

print("\n=== Q7: Method Extension with super() ===")

class BaseLogger:
    def log(self, message: str) -> List[str]:
        return [f"[BASE] {message}"]

class TimestampLogger(BaseLogger):
    def log(self, message: str) -> List[str]:
        # Extend parent method
        history = super().log(message)
        history.append(f"[TIMESTAMPED] {message} at 2026-10-17")
        return history

class EncryptedLogger(TimestampLogger):
    def log(self, message: str) -> List[str]:
        history = super().log(message)
        history.append(f"[ENCRYPTED] SHA256_{hash(message)}")
        return history

enc_logger = EncryptedLogger()
log_entries = enc_logger.log("Transaction #991")

print("  Cooperative log entries sequence:")
for entry in log_entries:
    print(f"    {entry}")

assert len(log_entries) == 3
assert log_entries[0] == "[BASE] Transaction #991"
assert "[TIMESTAMPED]" in log_entries[1]
assert "[ENCRYPTED]" in log_entries[2]

# Explanation: `super().method(*args)` delegates call execution up the Method Resolution
# Order (MRO), allowing layers of subclass functionality to compose cooperatively.


# ============================================================
# Q8: Fluent Interface & Method Chaining (Builder Pattern)
# ============================================================
# Question: Implement an SQL Query Builder class using instance methods that return
# `self` to enable fluent method chaining.

print("\n=== Q8: Fluent Interface via Method Chaining ===")

class SqlSelectBuilder:
    def __init__(self, table: str):
        self.table = table
        self._columns: List[str] = ["*"]
        self._where_conditions: List[str] = []
        self._limit_count: Optional[int] = None

    def columns(self, *cols: str) -> "SqlSelectBuilder":
        self._columns = list(cols)
        return self  # Return self for chaining

    def where(self, condition: str) -> "SqlSelectBuilder":
        self._where_conditions.append(condition)
        return self

    def limit(self, count: int) -> "SqlSelectBuilder":
        self._limit_count = count
        return self

    def build(self) -> str:
        cols_str = ", ".join(self._columns)
        query = f"SELECT {cols_str} FROM {self.table}"
        if self._where_conditions:
            query += f" WHERE {' AND '.join(self._where_conditions)}"
        if self._limit_count is not None:
            query += f" LIMIT {self._limit_count}"
        return query + ";"

sql_query = (
    SqlSelectBuilder("users")
    .columns("id", "username", "email")
    .where("active = 1")
    .where("role = 'admin'")
    .limit(25)
    .build()
)

print(f"  Fluent SQL Query: {sql_query}")
assert sql_query == "SELECT id, username, email FROM users WHERE active = 1 AND role = 'admin' LIMIT 25;"

# Explanation: Methods that return `self` create fluent APIs, allowing clean, readable
# multi-step object configuration without intermediate temporary variables.


# ============================================================
# Q9: Method Overriding & Parameter Compatibility
# ============================================================
# Question: Demonstrate method overriding in a PaymentProcessor hierarchy.
# Show how subclasses override the parent method while maintaining parameter compatibility.

print("\n=== Q9: Method Overriding & Compatibility ===")

class PaymentProcessor:
    def process_payment(self, amount: float) -> Dict[str, Any]:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return {"status": "SUCCESS", "amount": amount, "fee": 0.0}

class CreditCardProcessor(PaymentProcessor):
    def __init__(self, fee_percentage: float = 0.029):
        self.fee_percentage = fee_percentage

    # Overrides base method, maintaining compatible signature
    def process_payment(self, amount: float) -> Dict[str, Any]:
        res = super().process_payment(amount)
        res["fee"] = round(amount * self.fee_percentage, 2)
        res["processor"] = "CreditCard"
        return res

base_proc = PaymentProcessor()
cc_proc = CreditCardProcessor(fee_percentage=0.03)

r_base = base_proc.process_payment(100.0)
r_cc = cc_proc.process_payment(100.0)

print(f"  Base processor output:       {r_base}")
print(f"  CreditCard processor output: {r_cc}")

assert r_base["fee"] == 0.0
assert r_cc["fee"] == 3.0
assert r_cc["processor"] == "CreditCard"

# Explanation: Method overriding replaces parent method behavior in the subclass.
# To preserve the Liskov Substitution Principle, the subclass method should accept
# at least the same arguments and return compatible data structures.


# ============================================================
# Q10: Production-Grade Domain Entity with Diverse Factories
# ============================================================
# Question: Implement an `AuditLogEvent` domain entity featuring:
# 1) Instance methods for serialization and hashing
# 2) Class method factories (`from_json`, `from_system_event`, `create_failure`)
# 3) Static methods for sanitization and event ID generation

print("\n=== Q10: Domain Entity: AuditLogEvent with Diverse Factories ===")

import json
import uuid

class AuditLogEvent:
    def __init__(self, event_id: str, action: str, actor: str, success: bool, payload: Dict[str, Any]):
        self.event_id = event_id
        self.action = action
        self.actor = actor
        self.success = success
        self.payload = payload

    # 1. Instance method: serialize to dictionary
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "action": self.action,
            "actor": self.actor,
            "success": self.success,
            "payload": self.payload
        }

    # 2. Static method: generate compliant UUID event ID
    @staticmethod
    def generate_event_id() -> str:
        return f"EVT_{uuid.uuid4().hex[:12].upper()}"

    # 3. Class method factory: create successful system event
    @classmethod
    def create_system_event(cls, action: str, details: Dict[str, Any]) -> "AuditLogEvent":
        return cls(
            event_id=cls.generate_event_id(),
            action=action,
            actor="SYSTEM_DAEMON",
            success=True,
            payload=details
        )

    # 4. Class method factory: create failure event
    @classmethod
    def create_failure_event(cls, action: str, actor: str, error_reason: str) -> "AuditLogEvent":
        return cls(
            event_id=cls.generate_event_id(),
            action=action,
            actor=actor,
            success=False,
            payload={"error": error_reason}
        )

    # 5. Class method factory: deserialize from JSON string
    @classmethod
    def from_json(cls, json_str: str) -> "AuditLogEvent":
        data = json.loads(json_str)
        return cls(
            event_id=data["event_id"],
            action=data["action"],
            actor=data["actor"],
            success=data["success"],
            payload=data.get("payload", {})
        )

# Create events using different methods
evt_sys = AuditLogEvent.create_system_event("CRON_BACKUP", {"backup_mb": 450})
evt_fail = AuditLogEvent.create_failure_event("LOGIN_ATTEMPT", "unknown_user", "Invalid password")

# JSON roundtrip
json_repr = json.dumps(evt_sys.to_dict())
evt_deserialized = AuditLogEvent.from_json(json_repr)

print(f"  System Event:       {evt_sys.action} by {evt_sys.actor} (id: {evt_sys.event_id})")
print(f"  Failure Event:      {evt_fail.action} success={evt_fail.success}")
print(f"  Deserialized Event: {evt_deserialized.action} (Matches: {evt_deserialized.event_id == evt_sys.event_id})")

assert evt_sys.actor == "SYSTEM_DAEMON"
assert evt_sys.success is True
assert evt_fail.success is False
assert evt_deserialized.event_id == evt_sys.event_id
assert evt_deserialized.payload["backup_mb"] == 450

print("\nAll 10 methods questions executed and asserted successfully!")
