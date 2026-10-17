"""
Topic 05: Object-Oriented Programming (OOP)
Question 04: Inheritance (Deep Dive)

Master class inheritance and hierarchy architecture in Python:
- Single inheritance and constructor chaining with super().__init__()
- Multiple inheritance and the Diamond Problem resolved via C3 Linearization (MRO)
- Cooperative multiple inheritance: proving super() follows MRO, not direct parent
- Mixin classes: composing reusable orthogonal behaviors (JsonMixin, LoggingMixin)
- Hierarchy queries with issubclass() and isinstance()
- Preventing subclassing and method overriding with typing.final
- Attribute resolution conflict order across multiple base classes
- The Liskov Substitution Principle (LSP) in practice
- Automatic subclass discovery and registration via __init_subclass__ (PEP 487)
- Production-grade Message Broker Event Handler Hierarchy
"""

from typing import Any, Dict, List, Optional, Type, final


# ============================================================
# Q1: Single Inheritance & Constructor Chaining with super()
# ============================================================
# Question: Build an inheritance relationship between `Employee` and `Manager`.
# Forward constructor parameters to `super().__init__()`, extend with new attributes,
# and extend base class methods.

print("=== Q1: Single Inheritance & super().__init__() ===")

class Employee:
    def __init__(self, emp_id: str, name: str, salary: float):
        self.emp_id = emp_id
        self.name = name
        self.salary = salary

    def get_details(self) -> str:
        return f"[{self.emp_id}] {self.name} (Salary: ${self.salary:,.2f})"

class Manager(Employee):
    def __init__(self, emp_id: str, name: str, salary: float, department: str):
        # Forward base parameters to parent constructor
        super().__init__(emp_id, name, salary)
        self.department = department
        self.direct_reports: List[Employee] = []

    def add_report(self, employee: Employee) -> None:
        self.direct_reports.append(employee)

    # Extend base method
    def get_details(self) -> str:
        base_info = super().get_details()
        return f"{base_info} | Dept: {self.department} (Reports: {len(self.direct_reports)})"

emp1 = Employee("E101", "Alice", 95000.0)
mgr = Manager("M201", "Bob", 140000.0, "Engineering")
mgr.add_report(emp1)

print(f"  Employee: {emp1.get_details()}")
print(f"  Manager:  {mgr.get_details()}")

assert emp1.get_details() == "[E101] Alice (Salary: $95,000.00)"
assert mgr.get_details() == "[M201] Bob (Salary: $140,000.00) | Dept: Engineering (Reports: 1)"
assert isinstance(mgr, Employee)

# Explanation: `super().__init__(...)` delegates constructor initialization to the parent
# class, ensuring DRY compliance while letting the subclass add specialized attributes.


# ============================================================
# Q2: The Diamond Problem & C3 Linearization (MRO)
# ============================================================
# Question: Construct the classic Diamond inheritance pattern: `A -> B, C -> D`.
# Inspect `D.mro()` and `D.__mro__` to explain Python's C3 Linearization order.

print("\n=== Q2: The Diamond Problem & C3 Linearization ===")

class A:
    def ping(self) -> str:
        return "A"

class B(A):
    def ping(self) -> str:
        return "B"

class C(A):
    def ping(self) -> str:
        return "C"

class D(B, C):
    pass

d_inst = D()
ping_result = d_inst.ping()
mro_names = [cls.__name__ for cls in D.mro()]

print(f"  D().ping() returned: '{ping_result}'")
print(f"  D Method Resolution Order (MRO): {mro_names}")

# B comes before C in the inheritance list `class D(B, C)`, so B.ping() is called!
assert ping_result == "B"
assert mro_names == ["D", "B", "C", "A", "object"]

# Explanation: Python uses the C3 Linearization algorithm to calculate the Method Resolution
# Order (MRO). In Diamond inheritance, depth-first search would reach A before C;
# C3 ensures that subclasses appear before their parents, guaranteeing `C` is visited before `A`.


# ============================================================
# Q3: Cooperative Multiple Inheritance (super() Follows MRO!)
# ============================================================
# Question: Prove that `super()` in multiple inheritance calls the NEXT class in the MRO,
# which is NOT necessarily the direct syntactic parent class!

print("\n=== Q3: Cooperative Multiple Inheritance ===")

call_trace: List[str] = []

class Root:
    def execute(self) -> None:
        call_trace.append("Root.execute")

class FirstBranch(Root):
    def execute(self) -> None:
        call_trace.append("FirstBranch.execute (START)")
        super().execute()  # Calls SecondBranch.execute, NOT Root.execute!
        call_trace.append("FirstBranch.execute (END)")

class SecondBranch(Root):
    def execute(self) -> None:
        call_trace.append("SecondBranch.execute (START)")
        super().execute()  # Calls Root.execute
        call_trace.append("SecondBranch.execute (END)")

class CombinedChild(FirstBranch, SecondBranch):
    def execute(self) -> None:
        call_trace.append("CombinedChild.execute (START)")
        super().execute()
        call_trace.append("CombinedChild.execute (END)")

c_inst = CombinedChild()
c_inst.execute()

print(f"  CombinedChild MRO: {[cls.__name__ for cls in CombinedChild.mro()]}")
print("  Actual execution trace sequence:")
for step in call_trace:
    print(f"    {step}")

assert CombinedChild.mro() == [CombinedChild, FirstBranch, SecondBranch, Root, object]
# FirstBranch's super() called SecondBranch!
assert call_trace[0] == "CombinedChild.execute (START)"
assert call_trace[1] == "FirstBranch.execute (START)"
assert call_trace[2] == "SecondBranch.execute (START)"
assert call_trace[3] == "Root.execute"

# Explanation: `super()` does NOT mean "call parent". It means "call next class in MRO".
# When all classes cooperate by calling `super().method()`, every class in the diamond
# executes exactly once.


# ============================================================
# Q4: Mixin Classes for Reusable Orthogonal Capabilities
# ============================================================
# Question: Implement a `JsonSerializableMixin` and `AuditLoggerMixin`. Compose them onto
# domain classes without deep hierarchical coupling.

print("\n=== Q4: Mixin Classes ===")

import json

class JsonSerializableMixin:
    """Mixin: provides standardized JSON serialization for any class with __dict__."""
    def to_json(self) -> str:
        # Convert dictionary to JSON string
        return json.dumps(self.__dict__, sort_keys=True)

class AuditLoggerMixin:
    """Mixin: provides logging capabilities to any entity."""
    def log_event(self, action: str) -> str:
        class_name = self.__class__.__name__
        entity_id = getattr(self, "id", "NO_ID")
        return f"[{class_name} #{entity_id}] Action performed: {action}"

class Product(JsonSerializableMixin, AuditLoggerMixin):
    def __init__(self, product_id: str, name: str, price: float):
        self.id = product_id
        self.name = name
        self.price = price

p = Product("P-8821", "Mechanical Keyboard", 129.99)

json_str = p.to_json()
log_msg = p.log_event("PRICE_UPDATED")

print(f"  JSON from Mixin: {json_str}")
print(f"  Log from Mixin:  {log_msg}")

assert '"id": "P-8821"' in json_str
assert '"price": 129.99' in json_str
assert log_msg == "[Product #P-8821] Action performed: PRICE_UPDATED"

# Explanation: Mixins are small, standalone classes designed to add modular functionality
# to other classes through multiple inheritance, without forming a parent-child 'is-a' relationship.


# ============================================================
# Q5: Hierarchy Introspection: issubclass() & isinstance()
# ============================================================
# Question: Query complex class relationships across multiple tiers using `issubclass()`
# and `isinstance()`, including tuples of candidate classes.

print("\n=== Q5: Hierarchy Introspection ===")

class Vehicle: pass
class GroundVehicle(Vehicle): pass
class Car(GroundVehicle): pass
class ElectricCar(Car): pass
class Aircraft(Vehicle): pass

tesla = ElectricCar()

# 1. isinstance checks
assert isinstance(tesla, ElectricCar)
assert isinstance(tesla, Car)
assert isinstance(tesla, Vehicle)
assert not isinstance(tesla, Aircraft)

# 2. Check against tuple of candidates (any match returns True)
assert isinstance(tesla, (Aircraft, Car))  # True because it is a Car

# 3. issubclass checks
assert issubclass(ElectricCar, Vehicle)
assert issubclass(GroundVehicle, Vehicle)
assert not issubclass(Vehicle, ElectricCar)
assert issubclass(Car, (Aircraft, GroundVehicle))

print("  All hierarchy issubclass and isinstance assertions passed.")

# Explanation: Passing a tuple of classes to `isinstance(x, (A, B))` or `issubclass(X, (A, B))`
# returns True if the target matches ANY of the types in the tuple.


# ============================================================
# Q6: Preventing Subclassing & Overriding with typing.final
# ============================================================
# Question: Use `@final` from the `typing` module to indicate that a security-critical
# class must not be subclassed and a method must not be overridden.

print("\n=== Q6: Preventing Subclassing with @final ===")

@final
class SecureEncryptionEngine:
    """Security engine marked @final to prevent tampering via inheritance."""
    def encrypt(self, data: str) -> str:
        return f"ENCRYPTED_{hash(data)}"

class BaseAuth:
    @final
    def verify_token(self, token: str) -> bool:
        """Core security verification method that must not be overridden."""
        return token == "SECRET_TOKEN_XYZ"

    def authenticate_user(self, user: str) -> bool:
        return True

engine = SecureEncryptionEngine()
ciphertext = engine.encrypt("password123")
print(f"  Final engine ciphertext: {ciphertext}")
assert ciphertext.startswith("ENCRYPTED_")

# Explanation: `@final` signals to static analysis tools (mypy, Pyright) and IDEs
# that subclassing the decorated class or overriding the decorated method is prohibited.


# ============================================================
# Q7: Attribute Resolution Conflict Order in Multiple Bases
# ============================================================
# Question: Given two base classes defining identical method and attribute names,
# prove how Python determines which implementation wins based on inheritance declaration order.

print("\n=== Q7: Attribute Resolution Conflict Order ===")

class SQLiteBackend:
    backend_name = "SQLite"
    def execute_query(self) -> str:
        return "Executing on SQLite local storage"

class PostgresBackend:
    backend_name = "Postgres"
    def execute_query(self) -> str:
        return "Executing on PostgreSQL distributed cluster"

# Class 1: SQLite declared first
class DualClientA(SQLiteBackend, PostgresBackend):
    pass

# Class 2: Postgres declared first
class DualClientB(PostgresBackend, SQLiteBackend):
    pass

client_a = DualClientA()
client_b = DualClientB()

print(f"  DualClientA (SQLite first) -> backend: {client_a.backend_name}, query: '{client_a.execute_query()}'")
print(f"  DualClientB (PG first)     -> backend: {client_b.backend_name}, query: '{client_b.execute_query()}'")

assert client_a.backend_name == "SQLite"
assert "SQLite local" in client_a.execute_query()

assert client_b.backend_name == "Postgres"
assert "PostgreSQL distributed" in client_b.execute_query()

# Explanation: Python searches base classes from left to right as listed in the class header.
# The leftmost parent class has higher precedence in the MRO for conflicting attributes.


# ============================================================
# Q8: The Liskov Substitution Principle (LSP) in Practice
# ============================================================
# Question: Demonstrate the classic Circle-Ellipse / Square-Rectangle LSP violation,
# and refactor it into a proper immutable/interface hierarchy that respects LSP.

print("\n=== Q8: Liskov Substitution Principle (LSP) ===")

# THE VIOLATION: Making Square a subclass of mutable Rectangle breaks LSP!
# If caller resizes width, a Rectangle expects height to stay unchanged, but a Square mutates both!

# THE SOLUTION: An abstract Shape interface with read-only area calculation
class Shape:
    def get_area(self) -> float:
        raise NotImplementedError

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def get_area(self) -> float:
        return self.width * self.height

class Square(Shape):
    def __init__(self, side: float):
        self.side = side

    def get_area(self) -> float:
        return self.side * self.side

def compute_total_area(shapes: List[Shape]) -> float:
    """LSP compliant: accepts any Shape subclass and computes area reliably."""
    return sum(s.get_area() for s in shapes)

shapes_list = [Rectangle(4.0, 5.0), Square(3.0), Rectangle(2.0, 6.0)]
total_area = compute_total_area(shapes_list)

print(f"  Total area of [Rect(4,5), Sq(3), Rect(2,6)]: {total_area}")
assert total_area == (20.0 + 9.0 + 12.0)  # 41.0

# Explanation: Subclasses must be substitutable for their base types without altering
# program correctness. Modeling 'Square IS-A Rectangle' fails when rectangles are mutable.


# ============================================================
# Q9: Automatic Subclass Registration via __init_subclass__ (PEP 487)
# ============================================================
# Question: Implement a plugin registry using `__init_subclass__` (Python 3.6+).
# Automatically register any newly defined subclass into a class dictionary without metaclasses.

print("\n=== Q9: Automatic Plugin Registration via __init_subclass__ ===")

class DataParserPlugin:
    # Class-level plugin registry
    _registry: Dict[str, Type["DataParserPlugin"]] = {}

    def __init_subclass__(cls, format_code: str, **kwargs: Any):
        super().__init_subclass__(**kwargs)
        # Register the subclass automatically when defined!
        cls._registry[format_code.lower()] = cls
        cls.format_code = format_code.lower()

    @classmethod
    def get_parser(cls, format_code: str) -> Optional[Type["DataParserPlugin"]]:
        return cls._registry.get(format_code.lower())

    def parse(self, raw: str) -> Dict[str, Any]:
        raise NotImplementedError

# Defining subclasses automatically triggers __init_subclass__!
class CsvParser(DataParserPlugin, format_code="csv"):
    def parse(self, raw: str) -> Dict[str, Any]:
        return {"type": "csv", "data": raw.split(",")}

class JsonParser(DataParserPlugin, format_code="json"):
    def parse(self, raw: str) -> Dict[str, Any]:
        return {"type": "json", "data": json.loads(raw)}

print(f"  Registered parsers: {list(DataParserPlugin._registry.keys())}")
assert "csv" in DataParserPlugin._registry
assert "json" in DataParserPlugin._registry

# Fetch and execute plugin dynamically
csv_parser_cls = DataParserPlugin.get_parser("csv")
assert csv_parser_cls is CsvParser
parsed_csv = csv_parser_cls().parse("a,b,c")
print(f"  Parsed CSV via registered plugin: {parsed_csv}")
assert parsed_csv["data"] == ["a", "b", "c"]

# Explanation: `__init_subclass__` is called on the parent class whenever a subclass
# is created. It replaces complex metaclass registration with a clean, readable hook.


# ============================================================
# Q10: Production-Grade Message Broker Consumer Hierarchy
# ============================================================
# Question: Build an extensible event consumer hierarchy:
# - BaseConsumer: handles connection lifecycle and dispatch routing
# - KafkaConsumer / RabbitMqConsumer: specialized implementations
# - DeadLetterQueueMixin: adds failed-message retry & DLQ forwarding

print("\n=== Q10: Message Broker Consumer Hierarchy ===")

class DeadLetterQueueMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dlq_messages: List[Dict[str, Any]] = []

    def route_to_dlq(self, message: Dict[str, Any], reason: str) -> None:
        self.dlq_messages.append({"message": message, "reason": reason, "timestamp": "2026-10-17"})

class BaseMessageConsumer:
    def __init__(self, topic: str, group_id: str):
        self.topic = topic
        self.group_id = group_id
        self.processed_messages: List[Dict[str, Any]] = []

    def consume(self, message: Dict[str, Any]) -> bool:
        if not message.get("payload"):
            return False
        self.processed_messages.append(message)
        return True

class KafkaReliableConsumer(DeadLetterQueueMixin, BaseMessageConsumer):
    def __init__(self, topic: str, group_id: str, bootstrap_servers: str):
        super().__init__(topic=topic, group_id=group_id)
        self.bootstrap_servers = bootstrap_servers

    def consume(self, message: Dict[str, Any]) -> bool:
        try:
            if message.get("corrupted"):
                raise ValueError("Corrupted message payload")
            return super().consume(message)
        except Exception as exc:
            # Route to DLQ via Mixin!
            self.route_to_dlq(message, str(exc))
            return False

consumer = KafkaReliableConsumer("orders.v1", "order_processors", "kafka:9092")

# Process valid message
msg_ok = {"id": 1, "payload": "Order created"}
res_ok = consumer.consume(msg_ok)

# Process corrupted message
msg_bad = {"id": 2, "payload": "Garbage", "corrupted": True}
res_bad = consumer.consume(msg_bad)

print(f"  Valid message processed:    {res_ok}")
print(f"  Corrupted message processed:{res_bad}")
print(f"  Processed messages count:   {len(consumer.processed_messages)}")
print(f"  DLQ redirected count:       {len(consumer.dlq_messages)}")

assert res_ok is True
assert res_bad is False
assert len(consumer.processed_messages) == 1
assert len(consumer.dlq_messages) == 1
assert consumer.dlq_messages[0]["reason"] == "Corrupted message payload"

print("\nAll 10 inheritance questions executed and asserted successfully!")
