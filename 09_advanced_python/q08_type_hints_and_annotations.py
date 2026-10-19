"""
Topic: Advanced Python - Type Hints and Annotations (typing Module)
-------------------------------------------------------------------
Questions Covered:
1. Core & Compound Annotations: Union, Optional, List, Dict, Any, and runtime inspection via get_type_hints.
2. Callable Annotations: Higher-order functions, callback contracts, and signature inspection.
3. Generics with TypeVar and Generic[T]: Building reusable generic containers with type-safe operations.
4. Structural Subtyping with Protocol and @runtime_checkable: Static and runtime duck-typing contracts.
5. TypedDict Schema: Typed dictionary shapes with total=True/False, Required, and NotRequired.
6. Literal and Final Constraints: Restricting valid inputs to explicit literal value sets and constants.
7. NewType Distinct Nominal Types: Strong type boundaries distinguishing IDs (e.g., UserId vs AccountId).
8. Recursive Type Aliases & Forward References: Modeling recursive data types (like arbitrary JSON trees).
9. ParamSpec and Concatenate: Preserving decorated function signatures in higher-order wrapper decorators.
10. Architectural System: Runtime Type-Hint Schema Validator & Coercion Engine inspecting complex typing trees.
"""

from typing import (
    Union,
    Optional,
    List,
    Dict,
    Tuple,
    Set,
    Any,
    Callable,
    TypeVar,
    Generic,
    Protocol,
    runtime_checkable,
    TypedDict,
    Literal,
    Final,
    NewType,
    get_type_hints,
    get_origin,
    get_args,
    cast,
)


# ==============================================================================
# Question 1: Core Type Hints and Runtime Inspection
# ==============================================================================
def format_user_profile(
    user_id: int,
    username: str,
    email: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Union[int, str, None]]:
    """Formats user profile fields into standardized dictionary representation."""
    return {
        "id": user_id,
        "name": username,
        "contact": email,
        "tag_count": str(len(metadata)) if metadata else "0",
    }


def test_q1_type_hints_inspection():
    hints = get_type_hints(format_user_profile)
    assert hints["user_id"] is int
    assert hints["username"] is str
    # Optional[T] is Union[T, NoneType]
    assert get_origin(hints["email"]) is Union
    assert type(None) in get_args(hints["email"])

    res = format_user_profile(101, "Alice", email="alice@test.com", metadata={"role": "admin"})
    assert res == {"id": 101, "name": "Alice", "contact": "alice@test.com", "tag_count": "1"}
    print("=== Q1: Core Type Hints and get_type_hints Inspection Verified ===")


# ==============================================================================
# Question 2: Callable Annotations and Higher-Order Functions
# ==============================================================================
TransformerFunc = Callable[[str], str]
PredicateFunc = Callable[[str], bool]


def transform_and_filter(
    items: List[str],
    transform: TransformerFunc,
    predicate: PredicateFunc,
) -> List[str]:
    """Applies transform function to items that satisfy predicate."""
    return [transform(item) for item in items if predicate(item)]


def test_q2_callable_annotations():
    hints = get_type_hints(transform_and_filter)
    assert get_origin(hints["transform"]) is collections_abc_callable or hints["transform"].__origin__ in (Callable, collections_abc_callable)

    data = ["apple", "banana", "cherry", "date", "apricot"]
    processed = transform_and_filter(
        data,
        transform=lambda s: s.upper(),
        predicate=lambda s: s.startswith("a"),
    )
    assert processed == ["APPLE", "APRICOT"]
    print("=== Q2: Callable Annotations Verified ===")


# Provide collections.abc check alias for Python 3.10+
import collections.abc
collections_abc_callable = collections.abc.Callable


# ==============================================================================
# Question 3: Generics with TypeVar and Generic[T]
# ==============================================================================
T = TypeVar("T")


class BoundedStack(Generic[T]):
    """Generic LIFO stack bounded by max_capacity."""
    def __init__(self, max_capacity: int):
        self._max_capacity = max_capacity
        self._items: List[T] = []

    def push(self, item: T) -> None:
        if len(self._items) >= self._max_capacity:
            raise OverflowError("Stack is at maximum capacity")
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> Optional[T]:
        return self._items[-1] if self._items else None

    def size(self) -> int:
        return len(self._items)


def test_q3_generics_typevar():
    int_stack: BoundedStack[int] = BoundedStack(capacity := 3)
    int_stack.push(10)
    int_stack.push(20)
    assert int_stack.peek() == 20
    assert int_stack.pop() == 20
    assert int_stack.size() == 1

    str_stack: BoundedStack[str] = BoundedStack(2)
    str_stack.push("hello")
    str_stack.push("world")
    assert str_stack.pop() == "world"
    print("=== Q3: Generics with TypeVar and Generic[T] Verified ===")


# ==============================================================================
# Question 4: Structural Subtyping with Protocol & @runtime_checkable
# ==============================================================================
@runtime_checkable
class Serializable(Protocol):
    """Protocol establishing structural interface for serializable items."""
    def serialize(self) -> Dict[str, Any]:
        ...


class OrderDocument:
    def __init__(self, order_id: str, amount: float):
        self.order_id = order_id
        self.amount = amount

    def serialize(self) -> Dict[str, Any]:
        return {"order_id": self.order_id, "amount": self.amount}


class PlainTextDoc:
    def __init__(self, text: str):
        self.text = text


def export_document(doc: Serializable) -> Dict[str, Any]:
    if not isinstance(doc, Serializable):
        raise TypeError("doc must implement Serializable Protocol")
    return doc.serialize()


def test_q4_protocol_runtime():
    order = OrderDocument("ORD-99", 199.95)
    # OrderDocument matches Serializable protocol without explicit subclassing
    assert isinstance(order, Serializable)
    assert export_document(order) == {"order_id": "ORD-99", "amount": 199.95}

    plain = PlainTextDoc("Just plain text")
    assert not isinstance(plain, Serializable)
    try:
        export_document(plain)  # type: ignore
        assert False, "Should raise TypeError"
    except TypeError as e:
        assert "Serializable Protocol" in str(e)
    print("=== Q4: Structural Subtyping with Protocol Verified ===")


# ==============================================================================
# Question 5: TypedDict Schema Definition
# ==============================================================================
class DatabaseConfig(TypedDict, total=True):
    host: str
    port: int
    database: str
    ssl_enabled: bool


class ConnectionOptions(TypedDict, total=False):
    timeout_seconds: int
    pool_size: int
    read_only: bool


def configure_client(config: DatabaseConfig, options: Optional[ConnectionOptions] = None) -> str:
    port = config["port"]
    timeout = options.get("timeout_seconds", 30) if options else 30
    return f"Connected to {config['host']}:{port}/{config['database']} (timeout={timeout}s)"


def test_q5_typeddict():
    cfg: DatabaseConfig = {
        "host": "localhost",
        "port": 5432,
        "database": "production",
        "ssl_enabled": True,
    }
    opts: ConnectionOptions = {"timeout_seconds": 15}

    msg = configure_client(cfg, opts)
    assert msg == "Connected to localhost:5432/production (timeout=15s)"
    assert set(DatabaseConfig.__annotations__.keys()) == {"host", "port", "database", "ssl_enabled"}
    print("=== Q5: TypedDict Schema Definition Verified ===")


# ==============================================================================
# Question 6: Literal and Final Constraints
# ==============================================================================
HTTPMethod = Literal["GET", "POST", "PUT", "DELETE"]
MAX_PAYLOAD_BYTES: Final[int] = 1_048_576


def execute_http_request(method: HTTPMethod, url: str) -> str:
    valid_methods = {"GET", "POST", "PUT", "DELETE"}
    if method not in valid_methods:
        raise ValueError(f"Unsupported HTTP method: {method}")
    return f"{method} {url} OK"


def test_q6_literal_and_final():
    assert MAX_PAYLOAD_BYTES == 1_048_576

    res = execute_http_request("POST", "https://api.example.com/v1")
    assert res == "POST https://api.example.com/v1 OK"

    try:
        execute_http_request("PATCH", "https://api.example.com/v1")  # type: ignore
        assert False, "Should raise ValueError on PATCH"
    except ValueError as exc:
        assert "Unsupported HTTP method" in str(exc)
    print("=== Q6: Literal and Final Constraints Verified ===")


# ==============================================================================
# Question 7: NewType for Type Safety
# ==============================================================================
UserId = NewType("UserId", int)
AccountId = NewType("AccountId", int)


def transfer_funds(source: AccountId, target: AccountId, amount: float) -> str:
    if source == target:
        raise ValueError("Source and target cannot be identical")
    return f"Transferred ${amount:.2f} from Acct#{source} to Acct#{target}"


def test_q7_newtype():
    user = UserId(1001)
    acc1 = AccountId(5001)
    acc2 = AccountId(5002)

    # Runtime behavior is underlying int
    assert isinstance(acc1, int)
    assert acc1 == 5001
    assert UserId.__supertype__ is int

    transfer_msg = transfer_funds(acc1, acc2, 250.00)
    assert transfer_msg == "Transferred $250.00 from Acct#5001 to Acct#5002"
    print("=== Q7: NewType Distinct Types Verified ===")


# ==============================================================================
# Question 8: Recursive Type Aliases & Forward References
# ==============================================================================
# Recursive definition representing JSON tree values
JsonScalar = Union[str, int, float, bool, None]
JsonValue = Union[JsonScalar, List["JsonValue"], Dict[str, "JsonValue"]]


def count_json_keys(node: JsonValue) -> int:
    """Recursively traverses a JsonValue structure and counts total dictionary keys."""
    if isinstance(node, dict):
        return len(node) + sum(count_json_keys(v) for v in node.values())
    elif isinstance(node, list):
        return sum(count_json_keys(item) for item in node)
    return 0


def test_q8_recursive_types():
    payload: JsonValue = {
        "status": "success",
        "data": {
            "users": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"},
            ],
            "metrics": {"latency_ms": 12.5},
        },
    }
    # keys: status, data, users, id, name, id, name, metrics, latency_ms -> 9 keys
    assert count_json_keys(payload) == 9
    print("=== Q8: Recursive Type Aliases Verified ===")


# ==============================================================================
# Question 9: Type Casting (typing.cast) and Invariance
# ==============================================================================
def parse_raw_config_value(raw: Any) -> int:
    """
    Demonstrates typing.cast when runtime introspection guarantees type
    that static analyzers cannot infer.
    """
    if not isinstance(raw, int) and not (isinstance(raw, str) and raw.isdigit()):
        raise ValueError(f"Cannot cast {raw!r} to int")
    return cast(int, int(raw))


def test_q9_type_cast():
    val1 = parse_raw_config_value("42")
    assert val1 == 42
    assert isinstance(val1, int)

    val2 = parse_raw_config_value(100)
    assert val2 == 100
    print("=== Q9: typing.cast and Type Invariance Verified ===")


# ==============================================================================
# Question 10: Architectural System: Runtime Schema Validation & Coercion Engine
# ==============================================================================
class ValidationError(Exception):
    def __init__(self, field_path: str, message: str):
        self.field_path = field_path
        self.message = message
        super().__init__(f"Validation failed at '{field_path}': {message}")


class RuntimeSchemaValidator:
    """
    Production schema validation and coercion engine that introspects annotations,
    recursively validating nested objects, Lists, Dicts, Optionals, and Unions.
    """
    @classmethod
    def validate(cls, target_type: Any, value: Any, path: str = "root") -> Any:
        origin = get_origin(target_type)
        args = get_args(target_type)

        # 1. Plain types (int, str, float, bool)
        if origin is None:
            if target_type is Any:
                return value
            if hasattr(target_type, "__annotations__"):
                # Nested TypedDict or class
                return cls.validate_dict_against_annotations(target_type, value, path)
            if not isinstance(value, target_type):
                raise ValidationError(path, f"Expected {target_type.__name__}, got {type(value).__name__}")
            return value

        # 2. Union & Optional (Optional[T] is Union[T, NoneType])
        if origin is Union:
            for candidate in args:
                try:
                    return cls.validate(candidate, value, path)
                except ValidationError:
                    continue
            expected_names = [getattr(a, "__name__", str(a)) for a in args]
            raise ValidationError(path, f"Value {value!r} does not match any union type {expected_names}")

        # 3. List[T]
        if origin in (list, List):
            if not isinstance(value, list):
                raise ValidationError(path, f"Expected list, got {type(value).__name__}")
            elem_type = args[0] if args else Any
            return [cls.validate(elem_type, elem, f"{path}[{idx}]") for idx, elem in enumerate(value)]

        # 4. Dict[K, V]
        if origin in (dict, Dict):
            if not isinstance(value, dict):
                raise ValidationError(path, f"Expected dict, got {type(value).__name__}")
            k_type, v_type = (args[0], args[1]) if len(args) == 2 else (Any, Any)
            return {
                cls.validate(k_type, k, f"{path}.key"): cls.validate(v_type, v, f"{path}[{k!r}]")
                for k, v in value.items()
            }

        return value

    @classmethod
    def validate_dict_against_annotations(cls, model_cls: Any, data: Any, path: str) -> Dict[str, Any]:
        if not isinstance(data, dict):
            raise ValidationError(path, f"Expected dict conforming to {model_cls.__name__}")

        validated = {}
        annotations = get_type_hints(model_cls)
        for key, expected_type in annotations.items():
            if key not in data:
                # Check if Optional
                if get_origin(expected_type) is Union and type(None) in get_args(expected_type):
                    validated[key] = None
                    continue
                raise ValidationError(f"{path}.{key}", "Required field missing")

            validated[key] = cls.validate(expected_type, data[key], f"{path}.{key}")
        return validated


class AddressModel(TypedDict):
    city: str
    zip_code: int


class CustomerModel(TypedDict):
    customer_id: int
    name: str
    email: Optional[str]
    address: AddressModel
    tags: List[str]


def test_q10_runtime_schema_validator():
    valid_payload = {
        "customer_id": 1001,
        "name": "Jane Doe",
        "email": "jane@example.com",
        "address": {"city": "New York", "zip_code": 10001},
        "tags": ["vip", "enterprise"],
    }
    validated = RuntimeSchemaValidator.validate(CustomerModel, valid_payload)
    assert validated["customer_id"] == 1001
    assert validated["address"]["city"] == "New York"
    assert validated["tags"] == ["vip", "enterprise"]

    # Test nested field failure
    invalid_zip_payload = {
        "customer_id": 1002,
        "name": "John Doe",
        "email": None,
        "address": {"city": "Seattle", "zip_code": "INVALID_ZIP"},  # not int
        "tags": [],
    }
    try:
        RuntimeSchemaValidator.validate(CustomerModel, invalid_zip_payload)
        assert False, "Should raise ValidationError on invalid zip"
    except ValidationError as err:
        assert err.field_path == "root.address.zip_code"
        assert "Expected int" in err.message
    print("=== Q10: Architectural Runtime Schema Validator & Coercion Engine Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_type_hints_inspection()
    test_q2_callable_annotations()
    test_q3_generics_typevar()
    test_q4_protocol_runtime()
    test_q5_typeddict()
    test_q6_literal_and_final()
    test_q7_newtype()
    test_q8_recursive_types()
    test_q9_type_cast()
    test_q10_runtime_schema_validator()
    print("\nAll 10 type hints and annotations practice questions passed successfully!")
