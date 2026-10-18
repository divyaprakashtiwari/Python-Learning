"""
Topic 08: Modules and Packages - Question 04: Standard Library Tour

A comprehensive collection of 10 standalone, runnable exercises exploring
core Python standard library modules: `sys`, `os`, `math`, `random` vs `secrets`,
`uuid`, `platform`, `copy`, `zlib`, `urllib.parse`, and system diagnostics.

Questions Covered:
 1. sys Module Essentials: version_info, platform, maxsize, getsizeof(), and recursion limits.
 2. os Module Operations: Environment variables, cpu_count(), process PID, and path separators.
 3. math Module Capabilities: gcd, lcm, isclose(), comb, perm, ceil, floor, and log2.
 4. random vs secrets: Pseudo-random simulation vs cryptographically secure secrets generation.
 5. uuid Module: Generating UUID4 (random), UUID5 (namespaced), and string validation.
 6. platform Module: Querying OS architecture, system release, and Python runtime versions.
 7. copy Module: Object cloning semantics (shallow copy.copy vs deep copy.deepcopy).
 8. zlib Compression: In-memory byte compression, decompression, and CRC32 checksums.
 9. urllib.parse: Parsing URL components, query parameter encoding, and quote/unquote.
10. Advanced Project: System Environment & Runtime Health Diagnostic Inspector.
"""

import copy
import math
import os
import platform
import random
import secrets
import sys
import urllib.parse
import uuid
import zlib
from typing import Any


# ==============================================================================
# Question 1: sys Module Essentials
# ==============================================================================
def exercise_q1_sys_essentials() -> None:
    """
    Explore sys module parameters: runtime version tuple, platform identifier,
    memory byte size via getsizeof(), pointer width (maxsize), and recursion limit.
    """
    print("=== Q1: sys Module Essentials ===")

    # Version inspection
    assert sys.version_info.major >= 3
    assert isinstance(sys.version_info.minor, int)

    # Platform identifier: 'win32', 'linux', or 'darwin'
    assert isinstance(sys.platform, str)

    # sys.maxsize indicates 32-bit vs 64-bit interpreter
    is_64_bit = sys.maxsize > 2 ** 32
    assert is_64_bit is True  # Modern Python installations

    # Memory inspection: getsizeof() returns raw bytes allocated for an object
    empty_list_bytes = sys.getsizeof([])
    populated_list_bytes = sys.getsizeof([1, 2, 3, 4, 5])
    assert populated_list_bytes > empty_list_bytes

    # Recursion limit inspection
    limit = sys.getrecursionlimit()
    assert limit >= 1000

    print(f"  Python Version:   {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print(f"  Platform:         {sys.platform} (64-bit={is_64_bit})")
    print(f"  Empty list size:  {empty_list_bytes} bytes; populated: {populated_list_bytes} bytes")
    print(f"  Recursion limit:  {limit}")


# ==============================================================================
# Question 2: os Module Operations
# ==============================================================================
def exercise_q2_os_operations() -> None:
    """
    Demonstrate os module utilities: querying and setting environment variables,
    retrieving available CPU core count, process ID, and filesystem separators.
    """
    print("\n=== Q2: os Module Operations ===")

    # Environment variable manipulation
    os.environ["ANTIGRAVITY_ENV_TEST"] = "TRUE_2026"
    assert os.getenv("ANTIGRAVITY_ENV_TEST") == "TRUE_2026"
    assert os.getenv("NON_EXISTENT_VAR_XYZ", default="FALLBACK") == "FALLBACK"
    del os.environ["ANTIGRAVITY_ENV_TEST"]
    assert os.getenv("ANTIGRAVITY_ENV_TEST") is None

    # CPU count
    cores = os.cpu_count()
    assert cores is not None and cores >= 1

    # Current process ID
    pid = os.getpid()
    assert isinstance(pid, int) and pid > 0

    # Path separator
    sep = os.sep  # '\\' on Windows, '/' on POSIX
    assert sep in ("\\", "/")

    print(f"  CPU Cores:         {cores}")
    print(f"  Process ID (PID):  {pid}")
    print(f"  Path Separator:    '{sep}'")


# ==============================================================================
# Question 3: math Module Capabilities
# ==============================================================================
def exercise_q3_math_capabilities() -> None:
    """
    Demonstrate advanced mathematical operations: greatest common divisor (gcd),
    least common multiple (lcm), isclose() tolerance comparisons, combinatorics
    (comb, perm), and logarithms.
    """
    print("\n=== Q3: math Module Capabilities ===")

    # GCD and LCM
    assert math.gcd(48, 18) == 6
    assert math.lcm(12, 15) == 60

    # Floating point comparison with tolerance: math.isclose()
    # 0.1 + 0.2 in binary floating point is 0.30000000000000004 != 0.3
    assert 0.1 + 0.2 != 0.3
    assert math.isclose(0.1 + 0.2, 0.3, rel_tol=1e-9)

    # Combinatorics: nCr and nPr
    # 5 choose 2 = 10
    assert math.comb(5, 2) == 10
    # 5 permute 2 = 20
    assert math.perm(5, 2) == 20

    # Rounding and logarithms
    assert math.ceil(4.1) == 5
    assert math.floor(4.9) == 4
    assert math.log2(256) == 8.0

    print("  math.gcd(48, 18) = 6, math.lcm(12, 15) = 60")
    print(f"  math.isclose(0.1 + 0.2, 0.3) verified: {math.isclose(0.1 + 0.2, 0.3)}")
    print(f"  math.comb(5, 2) = {math.comb(5, 2)}, math.perm(5, 2) = {math.perm(5, 2)}")


# ==============================================================================
# Question 4: random vs secrets (Security & Cryptography)
# ==============================================================================
def exercise_q4_random_vs_secrets() -> None:
    """
    Contrast PRNG (random module - reproducible, not cryptographically secure)
    against CSPRNG (secrets module - OS entropy source, timing-attack safe).
    """
    print("\n=== Q4: random vs secrets ===")

    # 1. random module: seeded reproducibility for simulations
    random.seed(42)
    val1 = random.randint(1, 100)
    random.seed(42)
    val2 = random.randint(1, 100)
    assert val1 == val2  # Seeded reproducibility!

    # 2. secrets module: cryptographically secure tokens
    token_hex = secrets.token_hex(16)  # 32 characters
    token_url = secrets.token_urlsafe(16)
    assert len(token_hex) == 32
    assert isinstance(token_url, str)

    # Constant-time comparison to prevent side-channel timing attacks
    secret_key = "a8f4c2b9"
    user_input = "a8f4c2b9"
    assert secrets.compare_digest(secret_key, user_input) is True
    assert secrets.compare_digest(secret_key, "wrong_key") is False

    print(f"  Reproducible random randint: {val1}")
    print(f"  Secure secrets token_hex:    {token_hex}")
    print(f"  Timing-safe compare_digest:  {secrets.compare_digest(secret_key, user_input)}")


# ==============================================================================
# Question 5: uuid Module (UUIDv4 vs UUIDv5)
# ==============================================================================
def exercise_q5_uuid_module() -> None:
    """
    Demonstrate generating UUID4 (random) and deterministic UUID5 (SHA-1 namespaced),
    and validating UUID string representations.
    """
    print("\n=== Q5: uuid Module ===")

    # 1. UUID4: Random unique identifier
    u4_a = uuid.uuid4()
    u4_b = uuid.uuid4()
    assert u4_a != u4_b
    assert u4_a.version == 4

    # 2. UUID5: Deterministic identifier generated from a namespace and a string
    namespace = uuid.NAMESPACE_DNS
    u5_a = uuid.uuid5(namespace, "example.com")
    u5_b = uuid.uuid5(namespace, "example.com")
    assert u5_a == u5_b  # Exact same inputs produce exact same UUID5!
    assert u5_a.version == 5

    # 3. Parsing and validating UUID strings
    parsed = uuid.UUID(str(u4_a))
    assert parsed == u4_a

    print(f"  UUID4 (Random):        {u4_a} (version={u4_a.version})")
    print(f"  UUID5 (Deterministic): {u5_a} (version={u5_a.version})")


# ==============================================================================
# Question 6: platform Module
# ==============================================================================
def exercise_q6_platform_module() -> None:
    """
    Query operating system, kernel release, architecture, and Python implementation
    using the platform module.
    """
    print("\n=== Q6: platform Module ===")

    sys_os = platform.system()  # 'Windows', 'Linux', 'Darwin'
    release = platform.release()
    machine = platform.machine()  # 'AMD64', 'x86_64', 'arm64'
    python_impl = platform.python_implementation()  # 'CPython'

    assert sys_os in ("Windows", "Linux", "Darwin", "Java")
    assert python_impl == "CPython"

    print(f"  Operating System:      {sys_os} ({release})")
    print(f"  Machine Architecture:  {machine}")
    print(f"  Python Implementation: {python_impl} {platform.python_version()}")


# ==============================================================================
# Question 7: copy Module (Shallow vs Deep Copy)
# ==============================================================================
def exercise_q7_copy_module() -> None:
    """
    Demonstrate the critical difference between copy.copy() (shallow copy)
    and copy.deepcopy() (recursive deep copy) on nested data structures.
    """
    print("\n=== Q7: copy Module ===")

    original = {
        "user": "Alice",
        "scores": [90, 85, 95],
        "meta": {"role": "admin"},
    }

    # 1. Shallow copy
    shallow = copy.copy(original)
    # Outer dict is distinct
    assert shallow is not original
    # BUT nested objects are SHARED references!
    assert shallow["scores"] is original["scores"]

    shallow["scores"].append(100)
    assert 100 in original["scores"]  # Mutation affects original!

    # 2. Deep copy
    deep = copy.deepcopy(original)
    assert deep is not original
    assert deep["scores"] is not original["scores"]  # Fully cloned nested list!

    deep["scores"].append(999)
    assert 999 not in original["scores"]  # Mutation does NOT affect original!

    print(f"  Original scores after shallow mutation: {original['scores']}")
    print(f"  Deep copy scores after deep mutation:    {deep['scores']}")


# ==============================================================================
# Question 8: zlib Compression & Checksums
# ==============================================================================
def exercise_q8_zlib_compression() -> None:
    """
    Demonstrate lossless in-memory byte compression/decompression using zlib,
    and computing CRC32 integrity checksums.
    """
    print("\n=== Q8: zlib Compression & Checksums ===")

    payload = (
        b"Repeated data payload for compression testing. "
        b"Antigravity Python Systems Programming 2026. " * 20
    )
    raw_size = len(payload)

    # Compress
    compressed = zlib.compress(payload, level=9)
    compressed_size = len(compressed)
    assert compressed_size < raw_size

    # Decompress
    decompressed = zlib.decompress(compressed)
    assert decompressed == payload

    # CRC32 Checksum
    crc = zlib.crc32(payload)
    assert isinstance(crc, int)
    assert crc == zlib.crc32(decompressed)

    compression_ratio = (1.0 - (compressed_size / raw_size)) * 100
    print(f"  Raw Size:        {raw_size} bytes")
    print(f"  Compressed Size: {compressed_size} bytes ({compression_ratio:.1f}% space savings)")
    print(f"  CRC32 Checksum:  {hex(crc)}")


# ==============================================================================
# Question 9: urllib.parse URL Decomposition & Encoding
# ==============================================================================
def exercise_q9_urllib_parse() -> None:
    """
    Demonstrate urlparse, parse_qs, urlencode, and quote/unquote operations.
    """
    print("\n=== Q9: urllib.parse ===")

    raw_url = "https://api.example.com:8443/v1/search?query=python+programming&sort=desc&tag=dev"

    # 1. Deconstruct URL components
    parsed = urllib.parse.urlparse(raw_url)
    assert parsed.scheme == "https"
    assert parsed.netloc == "api.example.com:8443"
    assert parsed.port == 8443
    assert parsed.path == "/v1/search"

    # 2. Parse query parameters into dictionary
    query_params = urllib.parse.parse_qs(parsed.query)
    assert query_params["sort"] == ["desc"]
    assert query_params["tag"] == ["dev"]

    # 3. Encode dictionary back into query string
    new_params = {"client": "web_app", "filter": "status=active&type=prod"}
    encoded_query = urllib.parse.urlencode(new_params)
    assert "filter=status%3Dactive%26type%3Dprod" in encoded_query

    # 4. Percent-encoding (quote & unquote)
    quoted = urllib.parse.quote("Path with spaces & special chars: 100%")
    assert "%20" in quoted or "+" in quoted
    assert urllib.parse.unquote(quoted) == "Path with spaces & special chars: 100%"

    print(f"  Parsed host & port: {parsed.netloc}")
    print(f"  Parsed query dict:  {query_params}")
    print(f"  Encoded query URL:  {encoded_query}")


# ==============================================================================
# Question 10: Advanced Project - System Environment Diagnostic Inspector
# ==============================================================================
class SystemDiagnosticsInspector:
    """
    System diagnostic engine that aggregates host metrics, interpreter details,
    process states, memory limits, and security entropy into a telemetry report.
    """

    @classmethod
    def run_health_check(cls) -> dict[str, Any]:
        return {
            "timestamp": math.floor(sys.float_info.max),  # dummy bound check
            "os": {
                "system": platform.system(),
                "release": platform.release(),
                "machine": platform.machine(),
            },
            "python": {
                "version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "implementation": platform.python_implementation(),
                "executable": sys.executable,
                "is_64_bit": sys.maxsize > 2 ** 32,
            },
            "process": {
                "pid": os.getpid(),
                "cpu_cores": os.cpu_count() or 1,
                "recursion_limit": sys.getrecursionlimit(),
            },
            "security": {
                "csprng_verified": len(secrets.token_hex(8)) == 16,
                "session_uuid": str(uuid.uuid4()),
            },
        }


def exercise_q10_system_diagnostics_inspector() -> None:
    """
    Verify SystemDiagnosticsInspector compiles a complete telemetry report.
    """
    print("\n=== Q10: System Environment Diagnostic Inspector ===")

    report = SystemDiagnosticsInspector.run_health_check()

    assert report["os"]["system"] in ("Windows", "Linux", "Darwin", "Java")
    assert report["python"]["is_64_bit"] is True
    assert report["process"]["pid"] > 0
    assert report["security"]["csprng_verified"] is True
    assert len(report["security"]["session_uuid"]) == 36

    print("  System Health Manifest:")
    print(f"    OS:       {report['os']['system']} {report['os']['machine']}")
    print(f"    Python:   {report['python']['implementation']} {report['python']['version']}")
    print(f"    PID:      {report['process']['pid']} (Cores: {report['process']['cpu_cores']})")
    print(f"    UUID:     {report['security']['session_uuid']}")


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_sys_essentials()
    exercise_q2_os_operations()
    exercise_q3_math_capabilities()
    exercise_q4_random_vs_secrets()
    exercise_q5_uuid_module()
    exercise_q6_platform_module()
    exercise_q7_copy_module()
    exercise_q8_zlib_compression()
    exercise_q9_urllib_parse()
    exercise_q10_system_diagnostics_inspector()

    print("\nAll 10 standard library tour questions executed and asserted successfully!")
