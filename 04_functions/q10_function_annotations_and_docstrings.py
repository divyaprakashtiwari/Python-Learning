"""
Topic 04: Functions
Question 10: Function Annotations and Docstrings (Deep Dive)

Master Python typing, annotations, docstrings, and runtime schema generation:
- Parameter and return type hints with __annotations__ dictionary
- Docstring formatting standards (Google, Sphinx, NumPy) and inspect.cleandoc()
- Runtime type-checking decorator powered by __annotations__
- Modern typing constructs: Union, Optional, Literal, and typing.get_origin/get_args
- Generic functions with TypeVar and Sequence
- Postponed evaluation of annotations (PEP 563 / inspect.get_annotations)
- Type-safe decorator signature preservation
- OpenAPI / JSON-schema documentation extraction from docstrings and hints
- Function overloading with @typing.overload
- Production-grade JSON-RPC Dispatcher with automatic schema documentation
"""

import inspect
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    get_args,
    get_origin,
    overload,
)


# ============================================================
# Q1: Type Annotations & __annotations__ Dictionary
# ============================================================
# Question: Define a function with comprehensive parameter and return type annotations.
# Inspect its `__annotations__` attribute at runtime to demonstrate that Python annotations
# do not enforce types at runtime by default (they are purely descriptive metadata).

print("=== Q1: Type Annotations & __annotations__ Metadata ===")

def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculates Body Mass Index (BMI)."""
    return round(weight_kg / (height_m ** 2), 2)

bmi_val = calculate_bmi(70.0, 1.75)
print(f"  Calculated BMI: {bmi_val}")
assert bmi_val == 22.86

# Inspect __annotations__ dictionary
ann = calculate_bmi.__annotations__
print(f"  Runtime __annotations__: {ann}")

assert ann["weight_kg"] is float
assert ann["height_m"] is float
assert ann["return"] is float

# Demonstrate non-enforcement: passing ints or strings runs unless manually checked
assert calculate_bmi(70, 2) == 17.5

# Explanation: Type hints are stored in `__annotations__` at compile time.
# CPython does NOT validate types at runtime; type checking is performed statically
# by tools like mypy, Pyright, or IDEs, or dynamically via custom decorators.


# ============================================================
# Q2: Docstring Conventions & inspect.cleandoc()
# ============================================================
# Question: Compare Google-style and Sphinx/reST docstring conventions.
# Use `inspect.cleandoc()` to clean up leading indentation and format for display.

print("\n=== Q2: Docstring Standards & inspect.cleandoc() ===")

def query_user_records(user_id: int, include_deleted: bool = False) -> List[Dict[str, Any]]:
    """
    Retrieves user account records from the database.

    Args:
        user_id (int): Unique identifier of the user account.
        include_deleted (bool, optional): Whether soft-deleted records should be returned.
            Defaults to False.

    Returns:
        List[Dict[str, Any]]: List of record dictionaries containing user metadata.

    Raises:
        ValueError: If user_id is negative or zero.
    """
    if user_id <= 0:
        raise ValueError("user_id must be positive")
    return [{"id": user_id, "active": not include_deleted}]

raw_doc = query_user_records.__doc__
clean_doc = inspect.cleandoc(raw_doc or "")

print(f"  Cleaned Docstring (first 3 lines):")
for line in clean_doc.splitlines()[:3]:
    print(f"    {line}")

assert "Args:" in clean_doc
assert "Returns:" in clean_doc
assert "Raises:" in clean_doc

# Explanation: `inspect.cleandoc()` strips uniform indentation from multi-line docstrings,
# conforming to PEP 257 standards for documentation generators.


# ============================================================
# Q3: Runtime Type Validation Decorator
# ============================================================
# Question: Implement a `@enforce_types` decorator that intercepts calls, checks incoming
# arguments against the function's `__annotations__`, and raises `TypeError` on mismatch.

print("\n=== Q3: Runtime Type Validation Decorator ===")

def enforce_types(func: Callable[..., Any]) -> Callable[..., Any]:
    sig = inspect.signature(func)
    annotations = func.__annotations__

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        for param_name, value in bound.arguments.items():
            expected_type = annotations.get(param_name)
            if expected_type and isinstance(expected_type, type):
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"Argument '{param_name}' must be {expected_type.__name__}, got {type(value).__name__} ({value!r})"
                    )

        result = func(*args, **kwargs)

        return_type = annotations.get("return")
        if return_type and isinstance(return_type, type):
            if not isinstance(result, return_type):
                raise TypeError(f"Return value must be {return_type.__name__}, got {type(result).__name__}")

        return result

    return wrapper

@enforce_types
def create_order(item_id: int, quantity: int, unit_price: float) -> str:
    total = quantity * unit_price
    return f"Order #{item_id}: Total ${total:.2f}"

# Valid invocation
valid_order = create_order(101, 3, 29.99)
print(f"  Valid order: {valid_order}")
assert "Order #101" in valid_order

# Invalid invocation: passing string for item_id
caught_type_err = False
try:
    create_order("BAD_ID", 3, 29.99)  # type: ignore
except TypeError as err:
    caught_type_err = True
    print(f"  Caught expected runtime TypeError: {err}")

assert caught_type_err

# Explanation: Decorators can inspect `__annotations__` or `inspect.signature`
# to enforce dynamic validation at API boundaries (e.g. Pydantic / FastAPI).


# ============================================================
# Q4: Modern Typing Constructs (Union, Optional, Literal, get_origin/args)
# ============================================================
# Question: Demonstrate `Union`, `Optional`, and `Literal` types.
# Use `typing.get_origin()` and `typing.get_args()` to introspect composite types at runtime.

print("\n=== Q4: Introspecting Composite Type Constructs ===")

def configure_network(
    protocol: Literal["http", "https", "grpc"],
    timeout: Optional[float] = None,
    payload: Union[str, bytes] = "ready"
) -> str:
    return f"{protocol.upper()} configured"

res_net = configure_network("https", 5.0)
print(f"  configure_network result: '{res_net}'")
assert res_net == "HTTPS configured"

# Introspect protocol annotation (Literal)
proto_ann = configure_network.__annotations__["protocol"]
print(f"  protocol origin: {get_origin(proto_ann)}, args: {get_args(proto_ann)}")
assert get_origin(proto_ann) is Literal
assert get_args(proto_ann) == ("http", "https", "grpc")

# Introspect payload annotation (Union)
payload_ann = configure_network.__annotations__["payload"]
print(f"  payload origin:  {get_origin(payload_ann)}, args: {get_args(payload_ann)}")
assert get_origin(payload_ann) is Union
assert set(get_args(payload_ann)) == {str, bytes}

# Explanation: `typing.get_origin(T)` returns the unsubscripted generic class (e.g. Union, list),
# and `typing.get_args(T)` returns the type parameters tuple (e.g. (int, str)).


# ============================================================
# Q5: Generic Functions with TypeVar
# ============================================================
# Question: Implement a generic `first_or_default()` function using `TypeVar`
# that preserves element types without losing type hints.

print("\n=== Q5: Generic Functions with TypeVar ===")

T = TypeVar("T")

def first_or_default(sequence: Sequence[T], default: T) -> T:
    """Returns first item of sequence or default value if sequence is empty."""
    return sequence[0] if sequence else default

int_res = first_or_default([10, 20, 30], 0)
str_res = first_or_default([], "fallback")

print(f"  first_or_default([10, 20, 30], 0) = {int_res} (type: {type(int_res).__name__})")
print(f"  first_or_default([], 'fallback')  = '{str_res}'")

assert int_res == 10
assert str_res == "fallback"

# Constrained TypeVar
NumberType = TypeVar("NumberType", int, float)

def clamp(val: NumberType, min_val: NumberType, max_val: NumberType) -> NumberType:
    return max(min_val, min(val, max_val))

assert clamp(15, 0, 10) == 10
assert clamp(-5.5, 0.0, 10.0) == 0.0

# Explanation: `TypeVar` creates parameterized generic types that allow static type checkers
# to guarantee that input and return types match precisely across call sites.


# ============================================================
# Q6: inspect.get_annotations() (PEP 563 & Stringified Types)
# ============================================================
# Question: Use Python 3.10+ `inspect.get_annotations()` to safely resolve
# annotations even when stringified or forward-referenced.

print("\n=== Q6: inspect.get_annotations() ===")

class Node:
    # Forward-referencing 'Node' within its own class body
    def __init__(self, val: int, next_node: Optional["Node"] = None):
        self.val = val
        self.next_node = next_node

def find_tail(root: "Node") -> "Node":
    curr = root
    while curr.next_node is not None:
        curr = curr.next_node
    return curr

node_b = Node(2)
node_a = Node(1, node_b)
tail = find_tail(node_a)

print(f"  Linked list tail val: {tail.val}")
assert tail.val == 2

# Inspect annotations with inspect.get_annotations (safe across forward refs)
resolved_ann = inspect.get_annotations(find_tail)
print(f"  Resolved annotations for find_tail: {resolved_ann}")
assert "root" in resolved_ann and "return" in resolved_ann

# Explanation: `inspect.get_annotations(obj)` is the official, safe standard API
# introduced in Python 3.10 to read annotations without directly querying `__dict__['__annotations__']`.


# ============================================================
# Q7: Function Overloading with @typing.overload
# ============================================================
# Question: Demonstrate `@overload` to declare multiple valid parameter/return types
# for a single function (e.g. process(int) -> int, process(str) -> str).

print("\n=== Q7: Function Overloading with @overload ===")

@overload
def double_value(val: int) -> int: ...

@overload
def double_value(val: str) -> str: ...

@overload
def double_value(val: List[T]) -> List[T]: ...

# Concrete implementation handles all overloaded variants
def double_value(val: Any) -> Any:
    if isinstance(val, (int, float)):
        return val * 2
    elif isinstance(val, str):
        return f"{val}{val}"
    elif isinstance(val, list):
        return val + val
    raise TypeError(f"Unsupported type: {type(val)}")

r_int = double_value(21)
r_str = double_value("Echo")
r_lst = double_value([1, 2])

print(f"  double_value(21):     {r_int}")
print(f"  double_value('Echo'): '{r_str}'")
print(f"  double_value([1, 2]): {r_lst}")

assert r_int == 42
assert r_str == "EchoEcho"
assert r_lst == [1, 2, 1, 2]

# Explanation: `@typing.overload` stubs provide static type checkers with precise
# conditional return types for diverse argument signatures while keeping a single runtime implementation.


# ============================================================
# Q8: Automated OpenAPI Endpoint Schema Extraction
# ============================================================
# Question: Write a schema extraction function that reflects over a function's docstring
# and `__annotations__` to generate a Swagger/OpenAPI-compatible path operation JSON schema.

print("\n=== Q8: OpenAPI Endpoint Schema Extraction ===")

def api_get_user(user_id: int, format: Literal["json", "xml"] = "json") -> Dict[str, Any]:
    """
    Retrieve user profile by ID.
    Fetches full account attributes and settings.
    """
    return {"user_id": user_id, "format": format}

def generate_openapi_spec(fn: Callable[..., Any], http_method: str = "GET") -> Dict[str, Any]:
    """Reflects docstrings and type hints into an OpenAPI operation object."""
    sig = inspect.signature(fn)
    doc = inspect.cleandoc(fn.__doc__ or "")
    summary = doc.splitlines()[0] if doc else fn.__name__

    parameters = []
    for param_name, param in sig.parameters.items():
        param_type = "string"
        if param.annotation is int:
            param_type = "integer"
        elif param.annotation is float:
            param_type = "number"
        elif param.annotation is bool:
            param_type = "boolean"

        param_spec: Dict[str, Any] = {
            "name": param_name,
            "in": "query",
            "required": param.default is inspect.Parameter.empty,
            "schema": {"type": param_type}
        }
        if param.default is not inspect.Parameter.empty:
            param_spec["schema"]["default"] = param.default

        parameters.append(param_spec)

    return {
        "operationId": fn.__name__,
        "summary": summary,
        "method": http_method.upper(),
        "parameters": parameters
    }

spec = generate_openapi_spec(api_get_user, "GET")
print(f"  Generated OpenAPI Spec:")
print(f"    Summary:    {spec['summary']}")
print(f"    Parameters: {len(spec['parameters'])}")
for p in spec["parameters"]:
    print(f"      - {p['name']} ({p['schema']['type']}, required={p['required']})")

assert spec["operationId"] == "api_get_user"
assert spec["summary"] == "Retrieve user profile by ID."
assert spec["parameters"][0]["name"] == "user_id"
assert spec["parameters"][0]["required"] is True
assert spec["parameters"][1]["name"] == "format"
assert spec["parameters"][1]["required"] is False

# Explanation: Type hints and docstrings form the basis of automated API frameworks
# like FastAPI, automatically generating interactive Swagger and ReDoc documentation.


# ============================================================
# Q9: Validating Literal Enum-Style Arguments
# ============================================================
# Question: Implement a runtime validator for `Literal[...]` annotations to ensure
# only allowed string constants are accepted.

print("\n=== Q9: Literal Enum Argument Validation ===")

LogLevel = Literal["DEBUG", "INFO", "WARN", "ERROR"]

def set_log_level(level: LogLevel) -> str:
    allowed_levels = get_args(LogLevel)
    if level not in allowed_levels:
        raise ValueError(f"Invalid log level '{level}'. Allowed: {allowed_levels}")
    return f"Log level set to {level}"

# Valid
res_info = set_log_level("INFO")
print(f"  Valid level:   {res_info}")
assert res_info == "Log level set to INFO"

# Invalid
caught_invalid_level = False
try:
    set_log_level("TRACE")  # type: ignore
except ValueError as err:
    caught_invalid_level = True
    print(f"  Caught invalid level: {err}")

assert caught_invalid_level

# Explanation: `Literal` combined with `get_args()` provides compile-time type-checking
# for IDEs and easy runtime whitelist validation without full `enum.Enum` classes.


# ============================================================
# Q10: Production-Grade JSON-RPC Method Dispatcher with Validation
# ============================================================
# Question: Implement a production-grade JSON-RPC 2.0 dispatcher.
# Register methods with type hints, validate incoming JSON parameters against signatures,
# and return standardized JSON-RPC responses or error objects.

print("\n=== Q10: Validated JSON-RPC Dispatcher ===")

class JsonRpcDispatcher:
    def __init__(self):
        self._registry: Dict[str, Callable[..., Any]] = {}

    def register(self, method_name: Optional[str] = None):
        """Decorator to register an RPC method."""
        def decorator(fn: Callable[..., Any]):
            name = method_name or fn.__name__
            self._registry[name] = fn
            return fn
        return decorator

    def dispatch(self, request: Dict[str, Any]) -> Dict[str, Any]:
        req_id = request.get("id")
        method_name = request.get("method")
        params = request.get("params", {})

        if not method_name or method_name not in self._registry:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method '{method_name}' not found"}
            }

        fn = self._registry[method_name]
        sig = inspect.signature(fn)

        try:
            # Bind arguments to test signature compatibility
            if isinstance(params, dict):
                bound = sig.bind(**params)
            elif isinstance(params, list):
                bound = sig.bind(*params)
            else:
                bound = sig.bind()
            bound.apply_defaults()
            
            # Execute handler
            result = fn(*bound.args, **bound.kwargs)
            return {"jsonrpc": "2.0", "id": req_id, "result": result}
        except TypeError as err:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32602, "message": f"Invalid params: {err}"}
            }
        except Exception as err:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32603, "message": f"Internal error: {err}"}
            }

rpc = JsonRpcDispatcher()

@rpc.register("add")
def rpc_add(a: float, b: float) -> float:
    return a + b

@rpc.register("greet")
def rpc_greet(user: str, formal: bool = False) -> str:
    return f"Dear {user}" if formal else f"Hi {user}"

# 1. Successful call with dict params
r1 = rpc.dispatch({"jsonrpc": "2.0", "id": 1, "method": "add", "params": {"a": 10.5, "b": 2.5}})
print(f"  RPC add result:   {r1['result']}")
assert r1["result"] == 13.0

# 2. Successful call with list positional params
r2 = rpc.dispatch({"jsonrpc": "2.0", "id": 2, "method": "greet", "params": ["Alice", True]})
print(f"  RPC greet result: '{r2['result']}'")
assert r2["result"] == "Dear Alice"

# 3. Missing required parameters
r3 = rpc.dispatch({"jsonrpc": "2.0", "id": 3, "method": "add", "params": {"a": 10.5}})
print(f"  RPC error caught: {r3['error']['message']}")
assert r3["error"]["code"] == -32602

# 4. Unknown method
r4 = rpc.dispatch({"jsonrpc": "2.0", "id": 4, "method": "non_existent"})
assert r4["error"]["code"] == -32601

print("\nAll 10 function annotations and docstrings questions executed and asserted successfully!")
