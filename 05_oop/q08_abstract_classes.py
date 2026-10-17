"""
Topic 05: Object-Oriented Programming (OOP)
Question 08: Abstract Base Classes (Deep Dive)

Master Python's abc module and contract-driven design:
- Defining abstract base classes with abc.ABC and @abstractmethod
- Abstract property getters and setters (@property + @abstractmethod)
- Providing default/fallback implementations inside @abstractmethod
- Abstract class methods and static methods decorator ordering
- Virtual subclasses via abc.ABCMeta.register() (structural inheritance)
- Dynamic interface recognition using __subclasshook__
- The Template Method design pattern with abstract invariant algorithms
- Combining Abstract Base Classes with orthogonal Mixins
- Multi-tier abstract hierarchies with partial implementation
- Production-grade Generic CRUD Repository ABC with active In-Memory store
"""

from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar


# ============================================================
# Q1: Defining Abstract Base Classes with abc.ABC & @abstractmethod
# ============================================================
# Question: Define an abstract `PaymentGateway` class. Prove that attempting to instantiate
# an incomplete subclass raises `TypeError: Can't instantiate abstract class ... with abstract method`.

print("=== Q1: Abstract Base Classes & Instantiation Guard ===")

class PaymentGateway(ABC):
    @abstractmethod
    def process_charge(self, amount: float, currency: str) -> Dict[str, Any]:
        """Contract: concrete gateways must process charges."""
        pass

# Incomplete subclass: fails to implement process_charge
class IncompleteGateway(PaymentGateway):
    pass

# Complete subclass: satisfies the contract
class StripeGateway(PaymentGateway):
    def process_charge(self, amount: float, currency: str) -> Dict[str, Any]:
        return {"gateway": "Stripe", "amount": amount, "currency": currency, "status": "CONFIRMED"}

# 1. Instantiating incomplete class raises TypeError
caught_instantiation_error = False
try:
    IncompleteGateway()  # type: ignore
except TypeError as err:
    caught_instantiation_error = True
    print(f"  Caught expected TypeError on incomplete subclass: {err}")

assert caught_instantiation_error

# 2. Complete subclass instantiates cleanly
gateway = StripeGateway()
res = gateway.process_charge(99.0, "USD")
print(f"  Stripe charge processed: {res}")

assert res["status"] == "CONFIRMED"
assert isinstance(gateway, PaymentGateway)

# Explanation: `abc.ABC` and `@abstractmethod` enforce interface contracts at instantiation time.
# Subclasses cannot be instantiated unless all abstract methods are overridden.


# ============================================================
# Q2: Abstract Properties and Setters
# ============================================================
# Question: Define an abstract class with an abstract `@property` and `@prop.setter`.
# Enforce that concrete subclasses must provide getter and setter implementations.

print("\n=== Q2: Abstract Properties and Setters ===")

class ConfigurationSource(ABC):
    @property
    @abstractmethod
    def environment(self) -> str:
        """Abstract getter: concrete class must declare environment."""
        pass

    @environment.setter
    @abstractmethod
    def environment(self, value: str) -> None:
        """Abstract setter: concrete class must handle setting environment."""
        pass

class AppConfig(ConfigurationSource):
    def __init__(self, initial_env: str = "development"):
        self._env = initial_env

    @property
    def environment(self) -> str:
        return self._env

    @environment.setter
    def environment(self, value: str) -> None:
        allowed = {"development", "staging", "production"}
        if value not in allowed:
            raise ValueError(f"Invalid environment '{value}'. Allowed: {allowed}")
        self._env = value

cfg = AppConfig("development")
print(f"  Initial environment: {cfg.environment}")
assert cfg.environment == "development"

cfg.environment = "production"
print(f"  Updated environment: {cfg.environment}")
assert cfg.environment == "production"

# Explanation: Decorator order is critical: `@property` must be the outer decorator
# and `@abstractmethod` must be the inner decorator.


# ============================================================
# Q3: Default Implementation inside @abstractmethod
# ============================================================
# Question: Demonstrate that `@abstractmethod` can contain working code, which concrete
# subclasses can invoke via `super().method()` to reuse base logic.

print("\n=== Q3: Default Code inside Abstract Methods ===")

class BaseSerializer(ABC):
    @abstractmethod
    def serialize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Provides standardized baseline normalization for all serializers."""
        # Baseline transformation logic
        cleaned = dict(data)
        cleaned["_version"] = "1.0"
        cleaned["_timestamp"] = "2026-10-17"
        return cleaned

class JsonHeaderSerializer(BaseSerializer):
    def serialize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Invoke abstract method's base implementation via super()!
        base_payload = super().serialize(data)
        base_payload["content_type"] = "application/json"
        return base_payload

ser = JsonHeaderSerializer()
out = ser.serialize({"user": "alice", "action": "login"})

print(f"  Serialized payload: {out}")
assert out["_version"] == "1.0"
assert out["_timestamp"] == "2026-10-17"
assert out["content_type"] == "application/json"

# Explanation: `@abstractmethod` does not forbid having a method body.
# It only mandates that subclasses override the method; the subclass may call `super()` to leverage common base logic.


# ============================================================
# Q4: Abstract Class Methods and Static Methods
# ============================================================
# Question: Define an ABC with an `@abstractmethod` classmethod and staticmethod.
# Illustrate proper decorator ordering.

print("\n=== Q4: Abstract Class & Static Methods ===")

class DatabaseDriver(ABC):
    @classmethod
    @abstractmethod
    def default_port(cls) -> int:
        """Must be overridden as a class method."""
        pass

    @staticmethod
    @abstractmethod
    def validate_connection_string(conn_str: str) -> bool:
        """Must be overridden as a static method."""
        pass

class PostgresDriver(DatabaseDriver):
    @classmethod
    def default_port(cls) -> int:
        return 5432

    @staticmethod
    def validate_connection_string(conn_str: str) -> bool:
        return conn_str.startswith("postgresql://")

port = PostgresDriver.default_port()
is_valid = PostgresDriver.validate_connection_string("postgresql://localhost:5432/db")

print(f"  Postgres default port: {port}")
print(f"  Connection string valid: {is_valid}")

assert port == 5432
assert is_valid is True

# Explanation: When combining with `@abstractmethod`, `@classmethod` or `@staticmethod`
# must be the OUTER decorator, and `@abstractmethod` must be the INNER decorator.


# ============================================================
# Q5: Virtual Subclasses via abc.ABCMeta.register()
# ============================================================
# Question: Register a completely independent class as a "virtual subclass" of an ABC
# using `.register()`. Prove that `isinstance()` and `issubclass()` return True
# without modifying the class's MRO.

print("\n=== Q5: Virtual Subclasses via .register() ===")

class CacheInterface(ABC):
    @abstractmethod
    def get(self, key: str) -> Any: pass
    @abstractmethod
    def set(self, key: str, value: Any) -> None: pass

# Standalone Third-Party Cache (does not inherit from CacheInterface)
class RedisThirdPartyClient:
    def __init__(self):
        self._data: Dict[str, Any] = {}
    def get(self, key: str) -> Any:
        return self._data.get(key)
    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

# Register as virtual subclass
CacheInterface.register(RedisThirdPartyClient)

client = RedisThirdPartyClient()

# isinstance and issubclass recognize the virtual relationship!
is_sub = issubclass(RedisThirdPartyClient, CacheInterface)
is_inst = isinstance(client, CacheInterface)

print(f"  issubclass(RedisThirdPartyClient, CacheInterface): {is_sub}")
print(f"  isinstance(client, CacheInterface):               {is_inst}")
print(f"  RedisThirdPartyClient MRO: {[c.__name__ for c in RedisThirdPartyClient.mro()]}")

assert is_sub is True
assert is_inst is True
# Crucial: CacheInterface is NOT in RedisThirdPartyClient's MRO!
assert CacheInterface not in RedisThirdPartyClient.mro()

# Explanation: `.register()` allows third-party classes to satisfy ABC type checks
# without invasive code modification or introducing fragile multiple inheritance trees.


# ============================================================
# Q6: Dynamic Subclass Detection with __subclasshook__
# ============================================================
# Question: Implement an ABC `Renderable` that automatically recognizes ANY class providing
# a `render() -> str` method as a subclass via `__subclasshook__`, without explicit registration.

print("\n=== Q6: Dynamic Interface Detection with __subclasshook__ ===")

class Renderable(ABC):
    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        # Check if 'render' is defined anywhere in subclass or its base classes
        if cls is Renderable:
            for base in subclass.__mro__:
                if "render" in base.__dict__ and callable(base.__dict__["render"]):
                    return True
        return NotImplemented

class CustomWidget:
    # Notice: zero inheritance or registration!
    def render(self) -> str:
        return "<div>CustomWidget</div>"

class PlainObject:
    pass

w = CustomWidget()
p = PlainObject()

print(f"  isinstance(CustomWidget, Renderable): {isinstance(w, Renderable)}")
print(f"  isinstance(PlainObject, Renderable):  {isinstance(p, Renderable)}")

assert isinstance(w, Renderable)
assert issubclass(CustomWidget, Renderable)
assert not isinstance(p, Renderable)

# Explanation: `__subclasshook__` allows an ABC to dynamically define structural subtyping,
# exactly how standard library `collections.abc` detects iterables, mappings, and sequences.


# ============================================================
# Q7: Template Method Design Pattern via ABC
# ============================================================
# Question: Implement the Template Method pattern: an invariant multi-step algorithm
# defined in a base ABC (`generate_report`), where specific processing hooks
# (`_fetch_data`, `_format_report`) are left abstract for subclasses.

print("\n=== Q7: Template Method Pattern ===")

class ReportGenerator(ABC):
    # Invariant template algorithm skeleton
    def generate_report(self) -> str:
        data = self._fetch_data()
        validated = self._validate_data(data)
        formatted = self._format_report(validated)
        return formatted

    # Hook 1: Mandatory abstract step
    @abstractmethod
    def _fetch_data(self) -> List[int]:
        pass

    # Hook 2: Concrete step with sensible default
    def _validate_data(self, data: List[int]) -> List[int]:
        return [x for x in data if x >= 0]  # Exclude negatives

    # Hook 3: Mandatory abstract step
    @abstractmethod
    def _format_report(self, data: List[int]) -> str:
        pass

class CsvReport(ReportGenerator):
    def _fetch_data(self) -> List[int]:
        return [10, -5, 20, 30]

    def _format_report(self, data: List[int]) -> str:
        return ",".join(str(x) for x in data)

class HtmlReport(ReportGenerator):
    def _fetch_data(self) -> List[int]:
        return [1, 2, 3]

    def _format_report(self, data: List[int]) -> str:
        items = "".join(f"<li>{x}</li>" for x in data)
        return f"<ul>{items}</ul>"

csv_out = CsvReport().generate_report()
html_out = HtmlReport().generate_report()

print(f"  CSV Report:  {csv_out}")
print(f"  HTML Report: {html_out}")

assert csv_out == "10,20,30"
assert html_out == "<ul><li>1</li><li>2</li><li>3</li></ul>"

# Explanation: The Template Method pattern defines the high-level workflow invariant
# in the abstract base class, delegating domain-specific steps to concrete subclasses.


# ============================================================
# Q8: Combining ABCs with Orthogonal Mixins
# ============================================================
# Question: Implement a base ABC for `DataStore` that integrates with a `MetricsMixin`
# to track execution times across all abstract storage operations.

print("\n=== Q8: Combining ABCs with Mixins ===")

class MetricsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.operation_counts: Dict[str, int] = {}

    def record_metric(self, op_name: str) -> None:
        self.operation_counts[op_name] = self.operation_counts.get(op_name, 0) + 1

class KeyValueStore(ABC):
    @abstractmethod
    def put(self, key: str, val: Any) -> None: pass
    @abstractmethod
    def get(self, key: str) -> Any: pass

class MonitoredMemoryStore(MetricsMixin, KeyValueStore):
    def __init__(self):
        super().__init__()
        self._table: Dict[str, Any] = {}

    def put(self, key: str, val: Any) -> None:
        self.record_metric("put")
        self._table[key] = val

    def get(self, key: str) -> Any:
        self.record_metric("get")
        return self._table.get(key)

store = MonitoredMemoryStore()
store.put("session_id", "abc-123")
val = store.get("session_id")
store.get("missing_key")

print(f"  Retrieved value: {val}")
print(f"  Metrics logged:  {store.operation_counts}")

assert val == "abc-123"
assert store.operation_counts == {"put": 1, "get": 2}

# Explanation: Python allows combining contract-enforcing ABCs with functional Mixins,
# ensuring both strict API contracts and reusable cross-cutting concerns.


# ============================================================
# Q9: Multi-Tier Abstract Hierarchies (Partial Implementation)
# ============================================================
# Question: Build a 3-tier hierarchy:
# 1) `StreamReader` (ABC: read, seek, close)
# 2) `BufferedStreamReader` (ABC: implements seek, leaves read/close abstract)
# 3) `FileStreamReader` (Concrete: implements read, close)

print("\n=== Q9: Multi-Tier Hierarchies (Partial Implementation) ===")

class StreamReader(ABC):
    @abstractmethod
    def read(self, bytes_count: int) -> bytes: pass
    @abstractmethod
    def seek(self, offset: int) -> int: pass
    @abstractmethod
    def close(self) -> None: pass

class BufferedStreamReader(StreamReader):
    """Intermediate ABC: implements seek, but remains abstract for read and close."""
    def __init__(self):
        self._cursor = 0

    def seek(self, offset: int) -> int:
        self._cursor = max(0, offset)
        return self._cursor

# Cannot instantiate intermediate class because read and close are still abstract!
caught_inter_err = False
try:
    BufferedStreamReader()  # type: ignore
except TypeError:
    caught_inter_err = True

assert caught_inter_err
print("  Intermediate abstract class successfully blocked from instantiation.")

class MemoryStreamReader(BufferedStreamReader):
    """Leaf concrete class: completes the contract."""
    def __init__(self, raw_buffer: bytes):
        super().__init__()
        self._buffer = raw_buffer
        self.is_closed = False

    def read(self, bytes_count: int) -> bytes:
        if self.is_closed:
            raise ValueError("Stream is closed")
        data = self._buffer[self._cursor:self._cursor + bytes_count]
        self._cursor += len(data)
        return data

    def close(self) -> None:
        self.is_closed = True

stream = MemoryStreamReader(b"ABCDEFGHIJ")
assert stream.seek(2) == 2
chunk = stream.read(4)
print(f"  Read after seek(2): {chunk}")
assert chunk == b"CDEF"
stream.close()
assert stream.is_closed is True

# Explanation: An intermediate subclass that does not implement all abstract methods
# remains abstract and cannot be instantiated until a leaf subclass fulfills all contracts.


# ============================================================
# Q10: Production-Grade CRUD Repository ABC & In-Memory Store
# ============================================================
# Question: Implement a production-grade Generic Repository pattern:
# - Abstract Base Class `CrudRepository[T]` with create, read, update, delete, find_all
# - Concrete `InMemoryCrudRepository` implementing thread-safe dictionary storage
# - Demonstrates enterprise contract design and separation of persistence concerns

print("\n=== Q10: Domain Entity: CrudRepository Pattern ===")

T = TypeVar("T", bound=Dict[str, Any])

class CrudRepository(ABC):
    @abstractmethod
    def save(self, entity: Dict[str, Any]) -> str:
        """Persists entity and returns generated/existing ID."""
        pass

    @abstractmethod
    def find_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves entity by unique ID."""
        pass

    @abstractmethod
    def delete_by_id(self, entity_id: str) -> bool:
        """Deletes entity by ID; returns True if deleted."""
        pass

    @abstractmethod
    def list_all(self) -> List[Dict[str, Any]]:
        """Returns all persisted entities."""
        pass

class InMemoryCrudRepository(CrudRepository):
    def __init__(self):
        self._storage: Dict[str, Dict[str, Any]] = {}
        self._auto_id = 1000

    def save(self, entity: Dict[str, Any]) -> str:
        # Defensive copy
        record = dict(entity)
        if "id" not in record or not record["id"]:
            self._auto_id += 1
            record["id"] = f"REC_{self._auto_id}"
        entity_id = record["id"]
        self._storage[entity_id] = record
        return entity_id

    def find_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        item = self._storage.get(entity_id)
        return dict(item) if item else None

    def delete_by_id(self, entity_id: str) -> bool:
        return self._storage.pop(entity_id, None) is not None

    def list_all(self) -> List[Dict[str, Any]]:
        return [dict(item) for item in self._storage.values()]

repo = InMemoryCrudRepository()

# 1. Create records
id1 = repo.save({"name": "User Service", "port": 8081})
id2 = repo.save({"name": "Auth Service", "port": 8082})

print(f"  Created record 1 ID: {id1}")
print(f"  Created record 2 ID: {id2}")

# 2. Retrieve record
fetched = repo.find_by_id(id1)
print(f"  Fetched record 1:    {fetched}")
assert fetched is not None and fetched["name"] == "User Service"

# 3. Update record
repo.save({"id": id1, "name": "User Service v2", "port": 9000})
updated = repo.find_by_id(id1)
assert updated is not None and updated["port"] == 9000

# 4. List all
all_records = repo.list_all()
assert len(all_records) == 2

# 5. Delete record
assert repo.delete_by_id(id2) is True
assert repo.find_by_id(id2) is None
assert len(repo.list_all()) == 1

print("\nAll 10 abstract classes questions executed and asserted successfully!")
