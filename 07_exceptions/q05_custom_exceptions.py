"""
Topic 07: Exceptions - Question 05: Custom Exceptions

A comprehensive collection of 10 standalone, runnable exercises exploring
the design, inheritance hierarchies, custom attributes, payload serialization,
and RFC 7807 Problem Details mapping of custom Python exceptions.

Questions Covered:
 1. Basic Custom Exception: Subclassing Exception (and why NOT BaseException).
 2. Custom Attributes in __init__: Attaching status codes, resource IDs, and timestamps.
 3. Custom __str__ Formatting: Providing rich, human-readable exception representations.
 4. Application Exception Hierarchy: Base AppError and specialized domain sub-classes.
 5. Polymorphic Catching: Catching base AppError to handle all domain failures uniformly.
 6. Dual-Audience Messaging: Separating user_message from internal technical_details.
 7. Exception with Payload Snapshots: Preserving failed request payloads for audit logging.
 8. Inheriting from Built-In Types: Subclassing ValueError, KeyError, and LookupError.
 9. Dynamic Exception Factory: Programmatically generating typed exceptions via type().
10. Advanced Project: REST API RFC 7807 Problem Details Exception Transformer Engine.
"""

import json
import time
from typing import Any


# ==============================================================================
# Question 1: Basic Custom Exception
# ==============================================================================
class SimpleCustomError(Exception):
    """Minimal custom exception inheriting from built-in Exception."""
    pass


def exercise_q1_basic_custom_exception() -> None:
    """
    Demonstrate creating and raising a minimal custom exception.
    """
    print("=== Q1: Basic Custom Exception ===")

    assert issubclass(SimpleCustomError, Exception)
    assert issubclass(SimpleCustomError, BaseException)

    caught_exc = None
    try:
        raise SimpleCustomError("A custom application event occurred")
    except SimpleCustomError as exc:
        caught_exc = exc
        assert str(exc) == "A custom application event occurred"

    assert caught_exc is not None
    print(f"  Successfully caught SimpleCustomError: '{caught_exc}'")


# ==============================================================================
# Question 2: Custom Attributes in __init__
# ==============================================================================
class APIRequestError(Exception):
    """
    Custom exception carrying HTTP status code, endpoint, and error code.
    """

    def __init__(self, message: str, status_code: int, endpoint: str) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.endpoint = endpoint
        self.created_at = time.time()


def exercise_q2_custom_attributes() -> None:
    """
    Demonstrate custom exception with rich metadata attributes.
    """
    print("\n=== Q2: Custom Attributes in __init__ ===")

    try:
        raise APIRequestError("Rate limit exceeded", status_code=429, endpoint="/api/v1/users")
    except APIRequestError as err:
        assert err.message == "Rate limit exceeded"
        assert err.status_code == 429
        assert err.endpoint == "/api/v1/users"
        assert isinstance(err.created_at, float)

        print(f"  APIRequestError caught:")
        print(f"    Message:     {err.message}")
        print(f"    Status Code: {err.status_code}")
        print(f"    Endpoint:    {err.endpoint}")


# ==============================================================================
# Question 3: Custom __str__ Formatting
# ==============================================================================
class DatabaseConnectionError(Exception):
    """
    Custom exception with customized __str__ rendering for logging.
    """

    def __init__(self, host: str, port: int, db_name: str, reason: str) -> None:
        self.host = host
        self.port = port
        self.db_name = db_name
        self.reason = reason
        super().__init__(self._build_message())

    def _build_message(self) -> str:
        return f"[DB_ERROR] Failed to connect to '{self.db_name}' at {self.host}:{self.port} -> {self.reason}"

    def __str__(self) -> str:
        return self._build_message()


def exercise_q3_custom_str_formatting() -> None:
    """
    Demonstrate overriding __str__ for consistent error representation.
    """
    print("\n=== Q3: Custom __str__ Formatting ===")

    err = DatabaseConnectionError("db.internal.net", 5432, "analytics_prod", "Connection timed out")
    err_str = str(err)

    assert "[DB_ERROR]" in err_str
    assert "db.internal.net:5432" in err_str
    assert "analytics_prod" in err_str
    assert "Connection timed out" in err_str

    print(f"  Formatted Exception String:\n    {err_str}")


# ==============================================================================
# Question 4: Application Exception Hierarchy
# ==============================================================================
class CoreAppError(Exception):
    """Root exception for all application-domain errors."""
    pass


class ConfigurationError(CoreAppError):
    """Raised when environment or configuration files are corrupt/missing."""
    pass


class SecurityError(CoreAppError):
    """Raised for authentication or permission violations."""
    pass


class TokenExpiredError(SecurityError):
    """Raised specifically when a JWT/session token has expired."""
    pass


def exercise_q4_exception_hierarchy() -> None:
    """
    Verify inheritance hierarchy across multi-tier custom exceptions.
    """
    print("\n=== Q4: Application Exception Hierarchy ===")

    assert issubclass(ConfigurationError, CoreAppError)
    assert issubclass(SecurityError, CoreAppError)
    assert issubclass(TokenExpiredError, SecurityError)
    assert issubclass(TokenExpiredError, CoreAppError)

    # TokenExpiredError can be caught as TokenExpiredError, SecurityError, or CoreAppError
    caught_as_security = False
    try:
        raise TokenExpiredError("Token expired at 10:00:00 UTC")
    except SecurityError:
        caught_as_security = True

    assert caught_as_security is True
    print("  TokenExpiredError cleanly polymorphic with SecurityError and CoreAppError.")


# ==============================================================================
# Question 5: Polymorphic Catching with Base Domain Exceptions
# ==============================================================================
def exercise_q5_polymorphic_catching() -> None:
    """
    Demonstrate catching the base CoreAppError at system boundaries to handle
    any application-specific error gracefully without catching system errors.
    """
    print("\n=== Q5: Polymorphic Catching ===")

    def execute_service_action(action_type: str) -> str:
        if action_type == "config":
            raise ConfigurationError("Missing REDIS_URL")
        elif action_type == "token":
            raise TokenExpiredError("JWT signature expired")
        elif action_type == "unhandled":
            # Native Python error
            raise ZeroDivisionError("Unexpected math bug")
        return "SUCCESS"

    def safe_gateway(action_type: str) -> dict[str, Any]:
        try:
            return {"status": "OK", "data": execute_service_action(action_type)}
        except CoreAppError as app_exc:
            # Catches ConfigurationError, SecurityError, TokenExpiredError!
            return {
                "status": "APP_ERROR",
                "error_class": type(app_exc).__name__,
                "detail": str(app_exc),
            }

    res_cfg = safe_gateway("config")
    res_tok = safe_gateway("token")

    assert res_cfg["status"] == "APP_ERROR"
    assert res_cfg["error_class"] == "ConfigurationError"

    assert res_tok["status"] == "APP_ERROR"
    assert res_tok["error_class"] == "TokenExpiredError"

    # Native ZeroDivisionError is NOT caught by CoreAppError and propagates
    caught_native = False
    try:
        safe_gateway("unhandled")
    except ZeroDivisionError:
        caught_native = True

    assert caught_native is True
    print(f"  Configuration error caught as CoreAppError: {res_cfg['error_class']}")
    print(f"  TokenExpired error caught as CoreAppError:   {res_tok['error_class']}")
    print("  Native system error correctly bypassed domain exception handler.")


# ==============================================================================
# Question 6: Dual-Audience Messaging (User vs Technical)
# ==============================================================================
class UserFacingError(Exception):
    """
    Exception providing separate messages for external end-users and internal engineering logs.
    """

    def __init__(self, user_message: str, technical_details: str) -> None:
        super().__init__(technical_details)
        self.user_message = user_message
        self.technical_details = technical_details


def exercise_q6_dual_audience_messaging() -> None:
    """
    Demonstrate clean separation between safe user-facing text and sensitive technical logs.
    """
    print("\n=== Q6: Dual-Audience Messaging ===")

    err = UserFacingError(
        user_message="Unable to process payment. Please check your billing details.",
        technical_details="Stripe gateway declined charge: card_declined_insufficient_funds (code 402, tx_id: tx_99812)",
    )

    # User message contains no sensitive internal details
    assert "Unable to process payment" in err.user_message
    assert "Stripe gateway" not in err.user_message

    # Technical details contain diagnostic keys
    assert "tx_99812" in err.technical_details

    print(f"  Safe End-User Message:     '{err.user_message}'")
    print(f"  Internal Diagnostic Log:  '{err.technical_details}'")


# ==============================================================================
# Question 7: Exception with Payload Snapshots
# ==============================================================================
class InvalidOrderPayloadError(Exception):
    """
    Exception carrying the corrupted or invalid order request payload for audit logging.
    """

    def __init__(self, message: str, raw_payload: dict[str, Any], validation_failures: list[str]) -> None:
        super().__init__(message)
        self.raw_payload = raw_payload
        self.validation_failures = validation_failures


def exercise_q7_exception_payload_snapshots() -> None:
    """
    Demonstrate preserving failed entity state inside the exception object.
    """
    print("\n=== Q7: Exception with Payload Snapshots ===")

    bad_order = {"order_id": 1001, "items": [], "total": -5.0}

    try:
        raise InvalidOrderPayloadError(
            "Order validation rejected payload",
            raw_payload=bad_order,
            validation_failures=["Items list cannot be empty", "Total must be positive"],
        )
    except InvalidOrderPayloadError as exc:
        assert exc.raw_payload == bad_order
        assert len(exc.validation_failures) == 2
        assert exc.raw_payload["total"] == -5.0

        print(f"  Preserved payload order ID: {exc.raw_payload['order_id']}")
        print(f"  Validation failures: {exc.validation_failures}")


# ==============================================================================
# Question 8: Subclassing Built-In Semantic Exceptions
# ==============================================================================
class InvalidCoordinateError(ValueError):
    """A domain-specific error that is ALSO a ValueError."""
    pass


class MissingConfigKeyError(KeyError):
    """A domain-specific error that is ALSO a KeyError."""
    pass


def exercise_q8_subclassing_builtin_exceptions() -> None:
    """
    Demonstrate inheriting from standard built-in semantic exceptions so existing
    libraries catching ValueError or KeyError can handle custom exceptions naturally.
    """
    print("\n=== Q8: Subclassing Built-In Semantic Exceptions ===")

    assert issubclass(InvalidCoordinateError, ValueError)
    assert issubclass(MissingConfigKeyError, KeyError)

    # Library that catches standard ValueError
    def legacy_validator(val: Any) -> bool:
        try:
            if val < 0 or val > 360:
                raise InvalidCoordinateError(f"Coordinate {val} out of 0-360 range")
            return True
        except ValueError as exc:
            # Trapped naturally because InvalidCoordinateError IS-A ValueError!
            assert isinstance(exc, InvalidCoordinateError)
            return False

    assert legacy_validator(180) is True
    assert legacy_validator(450) is False

    print("  InvalidCoordinateError was transparently intercepted by 'except ValueError:'.")


# ==============================================================================
# Question 9: Dynamic Exception Factory
# ==============================================================================
def create_service_exception(service_name: str, base_class: type[Exception] = Exception) -> type[Exception]:
    """
    Factory function that dynamically creates a named exception class.
    """
    class_name = f"{service_name.capitalize()}ServiceError"
    return type(class_name, (base_class,), {"service": service_name})


def exercise_q9_dynamic_exception_factory() -> None:
    """
    Demonstrate programmatically creating unique exception classes via type().
    """
    print("\n=== Q9: Dynamic Exception Factory ===")

    BillingError = create_service_exception("billing")
    EmailError = create_service_exception("email")

    assert BillingError.__name__ == "BillingServiceError"
    assert EmailError.__name__ == "EmailServiceError"
    assert issubclass(BillingError, Exception)
    assert issubclass(EmailError, Exception)
    assert BillingError is not EmailError

    caught_billing = False
    try:
        raise BillingError("Credit card processing timeout")
    except BillingError as exc:
        caught_billing = True
        assert exc.service == "billing"  # type: ignore

    assert caught_billing is True
    print(f"  Created and caught dynamic class: {BillingError.__name__} (service='{BillingError.service}')")  # type: ignore


# ==============================================================================
# Question 10: Advanced Project - REST API RFC 7807 Problem Details Transformer
# ==============================================================================
class RestAPIError(Exception):
    """
    Base REST API exception conforming to RFC 7807 Problem Details specification.
    """

    status_code = 500
    title = "Internal Server Error"
    type_uri = "about:blank"

    def __init__(self, detail: str, instance_uri: str = "", extra_meta: dict[str, Any] | None = None) -> None:
        super().__init__(detail)
        self.detail = detail
        self.instance_uri = instance_uri
        self.extra_meta = extra_meta or {}

    def to_problem_details(self) -> dict[str, Any]:
        """Serializes the exception to an RFC 7807 JSON-compatible dictionary."""
        problem = {
            "type": self.type_uri,
            "title": self.title,
            "status": self.status_code,
            "detail": self.detail,
        }
        if self.instance_uri:
            problem["instance"] = self.instance_uri
        if self.extra_meta:
            problem.update(self.extra_meta)
        return problem


class ResourceNotFoundError(RestAPIError):
    status_code = 404
    title = "Resource Not Found"
    type_uri = "https://api.example.com/errors/not-found"


class ValidationFailedError(RestAPIError):
    status_code = 422
    title = "Unprocessable Entity"
    type_uri = "https://api.example.com/errors/validation-failed"


def exercise_q10_problem_details_transformer() -> None:
    """
    Test RestAPIError hierarchy serialization to RFC 7807 responses.
    """
    print("\n=== Q10: REST API RFC 7807 Problem Details Transformer ===")

    # 1. Resource Not Found
    err_404 = ResourceNotFoundError(
        detail="User account 'usr_881' does not exist",
        instance_uri="/api/v1/users/usr_881",
    )
    problem_404 = err_404.to_problem_details()

    assert problem_404["status"] == 404
    assert problem_404["title"] == "Resource Not Found"
    assert problem_404["detail"] == "User account 'usr_881' does not exist"
    assert problem_404["instance"] == "/api/v1/users/usr_881"

    # 2. Validation Failed with Extra Metadata
    err_422 = ValidationFailedError(
        detail="The request body has validation errors",
        instance_uri="/api/v1/orders",
        extra_meta={"invalid_params": [{"name": "quantity", "reason": "Must be > 0"}]},
    )
    problem_422 = err_422.to_problem_details()

    assert problem_422["status"] == 422
    assert problem_422["invalid_params"][0]["name"] == "quantity"

    # Test JSON serializability
    json_str = json.dumps(problem_422)
    assert '"status": 422' in json_str

    print("  RFC 7807 404 Problem Details:\n   ", json.dumps(problem_404))
    print("  RFC 7807 422 Problem Details:\n   ", json.dumps(problem_422))


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_basic_custom_exception()
    exercise_q2_custom_attributes()
    exercise_q3_custom_str_formatting()
    exercise_q4_exception_hierarchy()
    exercise_q5_polymorphic_catching()
    exercise_q6_dual_audience_messaging()
    exercise_q7_exception_payload_snapshots()
    exercise_q8_subclassing_builtin_exceptions()
    exercise_q9_dynamic_exception_factory()
    exercise_q10_problem_details_transformer()

    print("\nAll 10 custom exceptions questions executed and asserted successfully!")
