"""
Topic 07 - Exception Handling: Question 6
Problem: Exception Chaining (raise ... from orig), Context Suppression (from None), and __cause__ Introspection.
"""

import base64
import binascii
import json
from typing import Any, Dict, Optional


# 1. Custom Domain Exceptions
class ConfigurationLoadError(Exception):
    """Raised when cluster or service configuration loading fails."""
    pass


class InvalidSecurityTokenError(Exception):
    """Raised when authentication token validation fails, suppressing sensitive internal decode traces."""
    pass


# 2. Service Config & Secret Loader
class ServiceConfigLoader:
    """Demonstrates explicit exception chaining and context suppression."""

    def load_cluster_settings(self, filepath: str) -> Dict[str, Any]:
        """Loads cluster settings with explicit exception chaining from original FileNotFoundError."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError as err:
            # Preserves original root cause explicitly (__cause__)
            raise ConfigurationLoadError(f"Cluster config file '{filepath}' is missing") from err

    def decode_api_bearer_token(self, raw_token: str) -> Dict[str, Any]:
        """Decodes API token suppressing internal decode/binascii traceback details (from None)."""
        try:
            decoded_bytes = base64.b64decode(raw_token.encode("utf-8"), validate=True)
            return json.loads(decoded_bytes.decode("utf-8"))
        except (binascii.Error, UnicodeDecodeError, ValueError):
            # Suppresses internal traceback to avoid leaking implementation details
            raise InvalidSecurityTokenError("Bearer token is malformed or signature corrupted") from None

    def inspect_chaining(self, exc: BaseException) -> Dict[str, Any]:
        """Introspects exception cause, context, and context suppression flags."""
        suppress_flag = exc.__cause__ is None and getattr(exc, "__suppress_context__", False)
        return {
            "exception": type(exc).__name__,
            "message": str(exc),
            "cause": type(exc.__cause__).__name__ if exc.__cause__ else None,
            "context": type(exc.__context__).__name__ if exc.__context__ else None,
            "suppress_context": suppress_flag
        }


# Verification & Execution
loader = ServiceConfigLoader()

# Test Case 1: Explicit Chaining (from err)
print("Chaining Info (Test 1 - Explicit Chaining):")
try:
    loader.load_cluster_settings("missing_cluster.json")
except ConfigurationLoadError as err:
    chain_info1 = loader.inspect_chaining(err)
    print(f"- Exception: {chain_info1['exception']}")
    print(f"- Message: {chain_info1['message']}")
    print(f"- Cause: {chain_info1['cause']}")
    print(f"- Suppress Context: {chain_info1['suppress_context']}")

# Test Case 2: Suppressed Chaining (from None)
print("\nChaining Info (Test 2 - Suppressed Context):")
try:
    loader.decode_api_bearer_token("!!!invalid-base64-secret!!!")
except InvalidSecurityTokenError as err:
    chain_info2 = loader.inspect_chaining(err)
    print(f"- Exception: {chain_info2['exception']}")
    print(f"- Message: {chain_info2['message']}")
    print(f"- Cause: {chain_info2['cause']}")
    print(f"- Suppress Context: {chain_info2['suppress_context']}")
