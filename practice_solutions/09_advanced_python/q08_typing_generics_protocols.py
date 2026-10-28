"""
Question 8: Statically-Typed Event Message Bus & Schema Validator
Topic: Advanced Python

Key Concepts Tested:
- Structural subtyping via @runtime_checkable Protocol
- Generic containers using typing.TypeVar and typing.Generic
- Runtime parameter type validation via typing.get_type_hints
- Handling typing.Union and Optional types dynamically
- Type-safe subscriber dispatcher pattern
"""

from typing import (
    TypeVar,
    Generic,
    Protocol,
    runtime_checkable,
    get_type_hints,
    get_origin,
    get_args,
    Union,
    Callable,
    Dict,
    List,
    Optional,
    Any,
)


@runtime_checkable
class Serializable(Protocol):
    """
    Protocol enforcing structural subtyping for serializable payloads.
    Objects must provide a callable to_payload() method returning a dict.
    """

    def to_payload(self) -> Dict[str, Any]:
        ...


T = TypeVar("T")


class EventEnvelope(Generic[T]):
    """
    Generic event wrapper preserving type annotations of inner payload.
    """

    def __init__(self, event_id: str, payload: T, metadata: Optional[Dict[str, str]] = None) -> None:
        self.event_id = event_id
        self.payload: T = payload
        self.metadata = metadata or {}

    def extract_payload(self) -> T:
        return self.payload


def validate_annotated_arguments(func: Callable, kwargs: Dict[str, Any]) -> bool:
    """
    Validates keyword arguments against type annotations declared on func.
    Raises TypeError if an argument does not match its expected type.
    """
    type_hints = get_type_hints(func)

    for param_name, param_val in kwargs.items():
        if param_name not in type_hints:
            continue

        expected_type = type_hints[param_name]
        origin = get_origin(expected_type)

        if origin is Union:
            allowed_types = get_args(expected_type)
            if not isinstance(param_val, allowed_types):
                raise TypeError(
                    f"Argument '{param_name}' expected {expected_type}, received {type(param_val)}"
                )
        elif not isinstance(param_val, expected_type):
            raise TypeError(
                f"Argument '{param_name}' expected {expected_type}, received {type(param_val)}"
            )

    return True


class TypedEventDispatcher(Generic[T]):
    """
    Dispatcher enforcing payload serialization protocols and subscriber delivery.
    """

    def __init__(self) -> None:
        self._subscribers: List[Callable[[EventEnvelope[T]], None]] = []

    def subscribe(self, handler: Callable[[EventEnvelope[T]], None]) -> None:
        self._subscribers.append(handler)

    def dispatch(self, envelope: EventEnvelope[T]) -> None:
        payload = envelope.extract_payload()
        if not (isinstance(payload, Serializable) and callable(getattr(payload, "to_payload", None))):
            raise TypeError(
                f"Payload of type '{type(payload).__name__}' does not satisfy the Serializable Protocol."
            )

        for subscriber in self._subscribers:
            subscriber(envelope)


# Example domain classes
class UserLoginEvent:
    def __init__(self, username: str, user_id: int):
        self.username = username
        self.user_id = user_id

    def to_payload(self) -> Dict[str, Any]:
        return {"user": self.username, "id": self.user_id}


class NonSerializableEvent:
    def __init__(self, msg: str):
        self.msg = msg


if __name__ == "__main__":
    event = UserLoginEvent("dtiwari", 1001)
    non_serializable = NonSerializableEvent("test message")
    envelope = EventEnvelope(event_id="EVT-9001", payload=event)

    print("=== 1. Runtime Protocol Verification ===")
    is_event_serializable = isinstance(event, Serializable)
    is_bad_serializable = isinstance(non_serializable, Serializable)
    print(f"UserLoginEvent implements Serializable Protocol: {is_event_serializable}")
    print(f"NonSerializableEvent implements Serializable Protocol: {is_bad_serializable}")
    print(f"Generic Envelope Payload Type: {type(envelope.extract_payload()).__name__}")

    print("\n=== 2. Runtime Type Annotation Validation ===")
    def send_notification(recipient: str, retry_count: int, is_urgent: bool = False) -> bool:
        return True

    val_success = validate_annotated_arguments(
        send_notification, {"recipient": "admin@corp.io", "retry_count": 3}
    )
    print(f"Argument Validation: {'Valid (All parameters matched annotations)' if val_success else 'Invalid'}")

    print("\n=== 3. Signature Mismatch Handling ===")
    try:
        validate_annotated_arguments(
            send_notification, {"recipient": 12345, "retry_count": "three"}
        )
    except TypeError as err:
        print(f"Caught Expected: {err}")

    print("\n=== 4. Event Dispatcher Pipeline ===")
    dispatcher = TypedEventDispatcher[UserLoginEvent]()

    received_events = []
    dispatcher.subscribe(lambda env: received_events.append(env.extract_payload().to_payload()))
    dispatcher.dispatch(envelope)
    print(f"Dispatched Event Received: {received_events}")

    try:
        bad_envelope = EventEnvelope(event_id="EVT-BAD", payload=non_serializable)
        dispatcher.dispatch(bad_envelope)  # type: ignore[arg-type]
    except TypeError as err:
        print(f"Non-serializable payload dispatch caught: {err}")
