"""
Topic: Advanced Python - Walrus Operator and Modern Python Features (Python 3.8 - 3.12+)
----------------------------------------------------------------------------------------
Questions Covered:
1. Walrus Operator (:=) in While Loops: Chunked streaming until sentinel without duplicate reads.
2. Walrus Operator in Filtering & Comprehensions: Capturing computed results to avoid redundant calls.
3. Positional-Only Parameters (/): Constraining parameter delivery to enforce clean API boundaries.
4. Keyword-Only Parameters (*): Enforcing named keyword arguments for unambiguous call sites.
5. Combined Signature Grammar (pos-only, standard, kw-only): Strict parameter contract enforcement.
6. Structural Pattern Matching (match/case): Sequence unpacking, capturing wildcards, and rest patterns.
7. Structural Pattern Matching: Mapping patterns and Class patterns with object attribute extraction.
8. Pattern Matching Guard Clauses: Complex conditional validation within 'case ... if' arms.
9. Modern Python Builtin Features: Strict zip (strict=True), dict union operators (| and |=), and itertools.pairwise.
10. Architectural Modern RPC Command Dispatcher: Production command gateway employing pattern matching,
    walrus parameter evaluation, dict merging, and strict positional/keyword APIs.
"""

import itertools
from typing import List, Dict, Any, Optional, Tuple


# ==============================================================================
# Question 1: Walrus Operator (:=) in While Loops (Chunked Stream Ingestion)
# ==============================================================================
class MockByteStream:
    """Simulates an I/O source that yields chunks until an empty byte string."""
    def __init__(self, data: bytes, chunk_size: int = 4):
        self.data = data
        self.chunk_size = chunk_size
        self.offset = 0

    def read(self) -> bytes:
        chunk = self.data[self.offset : self.offset + self.chunk_size]
        self.offset += self.chunk_size
        return chunk


def ingest_stream_chunks(stream: MockByteStream) -> List[bytes]:
    """Ingests all non-empty byte chunks cleanly using the walrus operator (:=)."""
    chunks = []
    # Assignment expression directly inside loop condition
    while (chunk := stream.read()):
        chunks.append(chunk)
    return chunks


def test_q1_walrus_while_loop():
    raw_data = b"ABCDEFGHIJKL"  # 12 bytes
    stream = MockByteStream(raw_data, chunk_size=4)
    chunks = ingest_stream_chunks(stream)

    assert chunks == [b"ABCD", b"EFGH", b"IJKL"]
    assert stream.read() == b""
    print("=== Q1: Walrus Operator (:=) in While Loop Stream Ingestion Verified ===")


# ==============================================================================
# Question 2: Walrus Operator in Filtering and Mapping
# ==============================================================================
def parse_and_filter_integers(raw_inputs: List[str], min_val: int) -> List[int]:
    """
    Parses strings into integers, using walrus operator to store parsed int
    and filter out numbers < min_val without double conversion.
    """
    return [
        val
        for text in raw_inputs
        if text.strip().isdigit() and (val := int(text.strip())) >= min_val
    ]


def test_q2_walrus_in_comprehensions():
    inputs = [" 12 ", "not_a_number", "45", " 3 ", "99", "-5"]
    filtered = parse_and_filter_integers(inputs, min_val=20)
    assert filtered == [45, 99]
    print("=== Q2: Walrus Operator in Filtering & Comprehensions Verified ===")


# ==============================================================================
# Question 3: Positional-Only Parameters (/)
# ==============================================================================
def calculate_hypervolume(length: float, width: float, height: float, /) -> float:
    """
    Calculates 3D volume. All parameters are positional-only (marked by '/').
    Calling via keyword argument raises TypeError.
    """
    return length * width * height


def test_q3_positional_only():
    vol = calculate_hypervolume(2.0, 3.0, 4.0)
    assert vol == 24.0

    try:
        calculate_hypervolume(length=2.0, width=3.0, height=4.0)  # type: ignore
        assert False, "Should raise TypeError when passing positional-only args by keyword"
    except TypeError as exc:
        assert "positional-only" in str(exc)
    print("=== Q3: Positional-Only Parameters (/) Verified ===")


# ==============================================================================
# Question 4: Keyword-Only Parameters (*)
# ==============================================================================
def configure_cache_store(*, backend: str = "memory", ttl_seconds: int = 3600, compression: bool = False) -> Dict[str, Any]:
    """
    Configuration function where all parameters must be supplied as keyword arguments (after '*').
    """
    return {"backend": backend, "ttl_seconds": ttl_seconds, "compression": compression}


def test_q4_keyword_only():
    cfg = configure_cache_store(backend="redis", ttl_seconds=600, compression=True)
    assert cfg == {"backend": "redis", "ttl_seconds": 600, "compression": True}

    try:
        configure_cache_store("redis", 600)  # type: ignore
        assert False, "Should raise TypeError when passing positional arguments to keyword-only"
    except TypeError as exc:
        assert "takes 0 positional arguments" in str(exc)
    print("=== Q4: Keyword-Only Parameters (*) Verified ===")


# ==============================================================================
# Question 5: Combined Signature Grammar (Pos-Only, Standard, Keyword-Only)
# ==============================================================================
def robust_api_fetch(
    endpoint: str,
    version: str,
    /,
    timeout: float = 10.0,
    *,
    retries: int = 3,
    verbose: bool = False,
) -> Dict[str, Any]:
    """
    Full Python signature grammar:
    - endpoint, version: positional-only (cannot use keywords)
    - timeout: standard positional or keyword
    - retries, verbose: keyword-only
    """
    return {
        "url": f"https://api.internal/{version}/{endpoint}",
        "timeout": timeout,
        "retries": retries,
        "verbose": verbose,
    }


def test_q5_combined_signature():
    # Valid call styles
    call1 = robust_api_fetch("users", "v1", 15.0, retries=5, verbose=True)
    assert call1["url"] == "https://api.internal/v1/users"
    assert call1["timeout"] == 15.0
    assert call1["retries"] == 5

    call2 = robust_api_fetch("health", "v2", timeout=5.0, retries=1)
    assert call2["url"] == "https://api.internal/v2/health"
    assert call2["timeout"] == 5.0

    # Passing positional-only as keyword fails
    try:
        robust_api_fetch(endpoint="users", version="v1")  # type: ignore
        assert False, "Should raise TypeError"
    except TypeError:
        pass

    # Passing keyword-only as positional fails
    try:
        robust_api_fetch("users", "v1", 10.0, 5)  # type: ignore
        assert False, "Should raise TypeError"
    except TypeError:
        pass
    print("=== Q5: Combined Signature Grammar Contract Verified ===")


# ==============================================================================
# Question 6: Structural Pattern Matching (Sequence and Rest Patterns)
# ==============================================================================
def parse_cli_command(tokens: List[str]) -> str:
    """
    Parses CLI tokens using structural pattern matching:
    - ["quit" | "exit"]
    - ["get", key]
    - ["set", key, *values]
    - wildcard _
    """
    match tokens:
        case ["quit"] | ["exit"]:
            return "ACTION:SHUTDOWN"
        case ["get", str(key)]:
            return f"ACTION:GET:{key}"
        case ["set", str(key), *vals] if len(vals) > 0:
            joined_val = " ".join(vals)
            return f"ACTION:SET:{key}={joined_val}"
        case _:
            return "ACTION:UNKNOWN_COMMAND"


def test_q6_pattern_matching_sequences():
    assert parse_cli_command(["quit"]) == "ACTION:SHUTDOWN"
    assert parse_cli_command(["exit"]) == "ACTION:SHUTDOWN"
    assert parse_cli_command(["get", "theme"]) == "ACTION:GET:theme"
    assert parse_cli_command(["set", "greeting", "hello", "world"]) == "ACTION:SET:greeting=hello world"
    assert parse_cli_command(["unknown", "syntax"]) == "ACTION:UNKNOWN_COMMAND"
    assert parse_cli_command(["set", "empty_vals"]) == "ACTION:UNKNOWN_COMMAND"  # len(vals) == 0 fails guard
    print("=== Q6: Structural Pattern Matching (Sequences & Rest Patterns) Verified ===")


# ==============================================================================
# Question 7: Structural Pattern Matching (Mappings & Class Patterns)
# ==============================================================================
class GeoPoint:
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon


def classify_incoming_payload(payload: Any) -> str:
    """
    Classifies payloads matching dictionaries or Class patterns.
    """
    match payload:
        case {"type": "ping"}:
            return "PONG"
        case {"type": "user_event", "user": {"id": int(uid), "role": str(role)}}:
            return f"USER_EVENT:{uid}:{role}"
        case GeoPoint(lat=lat, lon=lon):
            return f"GEO_COORDINATE:{lat},{lon}"
        case _:
            return "UNRECOGNIZED_PAYLOAD"


def test_q7_pattern_matching_mappings_and_classes():
    assert classify_incoming_payload({"type": "ping"}) == "PONG"

    event_payload = {
        "type": "user_event",
        "user": {"id": 42, "role": "admin"},
        "extra_ignored_key": "data",
    }
    assert classify_incoming_payload(event_payload) == "USER_EVENT:42:admin"

    pt = GeoPoint(37.77, -122.42)
    assert classify_incoming_payload(pt) == "GEO_COORDINATE:37.77,-122.42"

    assert classify_incoming_payload("random_string") == "UNRECOGNIZED_PAYLOAD"
    print("=== Q7: Structural Pattern Matching (Mappings & Classes) Verified ===")


# ==============================================================================
# Question 8: Pattern Matching Guard Clauses
# ==============================================================================
def route_numeric_transaction(transaction: Dict[str, Any]) -> str:
    """
    Uses pattern matching with guard clauses 'if ...' to route financial transactions.
    """
    match transaction:
        case {"amount": float(amt), "status": "PENDING"} if amt > 10_000.0:
            return "FLAG_FOR_MANUAL_REVIEW"
        case {"amount": float(amt), "status": "PENDING"} if amt <= 0.0:
            return "REJECT_INVALID_AMOUNT"
        case {"amount": float(amt), "status": "PENDING"}:
            return f"AUTO_APPROVE:{amt}"
        case {"status": "CANCELLED"}:
            return "IGNORE_CANCELLED"
        case _:
            return "MALFORMED_TRANSACTION"


def test_q8_pattern_matching_guards():
    assert route_numeric_transaction({"amount": 25000.0, "status": "PENDING"}) == "FLAG_FOR_MANUAL_REVIEW"
    assert route_numeric_transaction({"amount": -5.0, "status": "PENDING"}) == "REJECT_INVALID_AMOUNT"
    assert route_numeric_transaction({"amount": 150.0, "status": "PENDING"}) == "AUTO_APPROVE:150.0"
    assert route_numeric_transaction({"status": "CANCELLED"}) == "IGNORE_CANCELLED"
    assert route_numeric_transaction({}) == "MALFORMED_TRANSACTION"
    print("=== Q8: Pattern Matching Guard Clauses Verified ===")


# ==============================================================================
# Question 9: Modern Python Builtins (Strict zip, dict union |, itertools.pairwise)
# ==============================================================================
def safe_parallel_aggregation(keys: List[str], values: List[int]) -> Dict[str, int]:
    """
    Uses zip with strict=True to prevent silent data loss from mismatched list lengths.
    """
    return dict(zip(keys, values, strict=True))


def compute_step_deltas(numbers: List[int]) -> List[int]:
    """
    Computes differences between consecutive numbers using itertools.pairwise.
    """
    return [b - a for a, b in itertools.pairwise(numbers)]


def merge_and_update_configurations(base: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
    """
    Uses Python 3.9+ dictionary union operator (|).
    """
    return base | overrides


def test_q9_modern_builtins():
    # 1. zip(..., strict=True)
    d = safe_parallel_aggregation(["a", "b"], [1, 2])
    assert d == {"a": 1, "b": 2}

    try:
        safe_parallel_aggregation(["a", "b", "c"], [1, 2])
        assert False, "Should raise ValueError on unequal lengths with strict=True"
    except ValueError as exc:
        assert "zip() argument" in str(exc) or "lengths" in str(exc)

    # 2. itertools.pairwise
    deltas = compute_step_deltas([10, 15, 25, 40])
    assert deltas == [5, 10, 15]

    # 3. Dict union operator |
    base_cfg = {"host": "localhost", "port": 8000, "debug": False}
    override_cfg = {"port": 9000, "debug": True}
    merged = merge_and_update_configurations(base_cfg, override_cfg)
    assert merged == {"host": "localhost", "port": 9000, "debug": True}
    assert base_cfg["port"] == 8000  # original unmodified
    print("=== Q9: Modern Python Builtins (strict zip, dict |, pairwise) Verified ===")


# ==============================================================================
# Question 10: Architectural Modern RPC Gateway & Dispatch Engine
# ==============================================================================
class RPCResponse:
    def __init__(self, success: bool, result: Any, error: Optional[str] = None):
        self.success = success
        self.result = result
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        return {"success": self.success, "result": self.result, "error": self.error}


class ModernRPCGateway:
    """
    Production RPC Command Gateway featuring:
    - Structural pattern matching on command messages
    - Walrus operator inline header parsing
    - Positional-only and keyword-only API constraints
    - Dict merging for response enrichment
    """
    def __init__(self):
        self._accounts: Dict[str, float] = {"acc_1": 1000.0, "acc_2": 500.0}

    def dispatch(
        self,
        request: Dict[str, Any],
        /,
        *,
        auth_header: Optional[str] = None,
    ) -> Dict[str, Any]:
        # Validate authentication using walrus operator
        if not auth_header or not (token := auth_header.removeprefix("Bearer ")).isalnum():
            return RPCResponse(False, None, error="Invalid or missing bearer token").to_dict()

        # Structural pattern matching on RPC request
        match request:
            case {"command": "get_balance", "account_id": str(acc)}:
                if acc in self._accounts:
                    resp = RPCResponse(True, {"account_id": acc, "balance": self._accounts[acc]})
                else:
                    resp = RPCResponse(False, None, error=f"Account '{acc}' not found")

            case {"command": "transfer", "source": str(src), "target": str(dst), "amount": (int() | float()) as amt} if amt > 0:
                if src not in self._accounts or dst not in self._accounts:
                    resp = RPCResponse(False, None, error="Unknown source or destination account")
                elif self._accounts[src] < amt:
                    resp = RPCResponse(False, None, error="Insufficient funds")
                else:
                    self._accounts[src] -= float(amt)
                    self._accounts[dst] += float(amt)
                    resp = RPCResponse(
                        True,
                        {"transferred": amt, "source_balance": self._accounts[src], "target_balance": self._accounts[dst]},
                    )

            case {"command": "ping"}:
                resp = RPCResponse(True, "pong")

            case _:
                resp = RPCResponse(False, None, error="Malformed RPC request")

        # Enrich response dictionary using modern dict union operator
        metadata = {"caller_token": token[:4] + "***"}
        return resp.to_dict() | metadata


def test_q10_modern_rpc_gateway():
    gateway = ModernRPCGateway()

    # 1. Unauthenticated request
    unauth = gateway.dispatch({"command": "ping"}, auth_header=None)
    assert unauth["success"] is False
    assert "Invalid or missing" in unauth["error"]

    # 2. Ping command
    ping_res = gateway.dispatch({"command": "ping"}, auth_header="Bearer secret123")
    assert ping_res["success"] is True
    assert ping_res["result"] == "pong"
    assert ping_res["caller_token"] == "secr***"

    # 3. Get balance command
    bal_res = gateway.dispatch(
        {"command": "get_balance", "account_id": "acc_1"},
        auth_header="Bearer secret123",
    )
    assert bal_res["success"] is True
    assert bal_res["result"]["balance"] == 1000.0

    # 4. Transfer command
    xfer_res = gateway.dispatch(
        {"command": "transfer", "source": "acc_1", "target": "acc_2", "amount": 200.0},
        auth_header="Bearer secret123",
    )
    assert xfer_res["success"] is True
    assert xfer_res["result"]["source_balance"] == 800.0
    assert xfer_res["result"]["target_balance"] == 700.0

    # 5. Invalid negative amount rejected by pattern guard
    invalid_xfer = gateway.dispatch(
        {"command": "transfer", "source": "acc_1", "target": "acc_2", "amount": -50.0},
        auth_header="Bearer secret123",
    )
    assert invalid_xfer["success"] is False
    assert invalid_xfer["error"] == "Malformed RPC request"
    print("=== Q10: Architectural Modern RPC Gateway Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_walrus_while_loop()
    test_q2_walrus_in_comprehensions()
    test_q3_positional_only()
    test_q4_keyword_only()
    test_q5_combined_signature()
    test_q6_pattern_matching_sequences()
    test_q7_pattern_matching_mappings_and_classes()
    test_q8_pattern_matching_guards()
    test_q9_modern_builtins()
    test_q10_modern_rpc_gateway()
    print("\nAll 10 modern Python and walrus operator practice questions passed successfully!")
