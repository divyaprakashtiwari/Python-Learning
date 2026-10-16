"""
Topic 03: Data Structures
Question 03: Tuple Operations (Deep Dive)

Master Python tuples: immutability semantics, the single-element tuple comma trap,
the "augmented assignment in tuple" paradox, memory efficiency vs lists,
named tuples (collections & typing), hashability as dictionary keys,
lexicographical comparisons, and tuple vector geometry.
"""

import sys
from collections import namedtuple
from typing import NamedTuple, Any
import math

# ============================================================
# Q1: Tuple Creation, Immutability, and the Trailing Comma Trap
# ============================================================
# Question: Demonstrate creating tuples, the trailing comma trap for 1-element tuples,
# and verify that tuples are immutable by catching the TypeError on mutation.

print("=== Q1: Tuple Creation & Trailing Comma Trap ===")

# Empty tuple
empty_tup = ()
print(f"  Empty tuple: {empty_tup} (type: {type(empty_tup).__name__})")

# THE SINGLE-ELEMENT COMMA TRAP:
not_a_tuple = (42)    # Just the integer 42 in parentheses!
is_a_tuple = (42,)     # The trailing comma makes it a tuple!
print(f"  (42)  type is: {type(not_a_tuple).__name__} (NOT a tuple!)")
print(f"  (42,) type is: {type(is_a_tuple).__name__} (True 1-element tuple)")

# Immutability verification
coords = (10, 20, 30)
print(f"  Coordinates: {coords}")
try:
    coords[0] = 99  # type: ignore
except TypeError as e:
    print(f"  Caught expected immutability error: {e}")

# Explanation: In Python, parentheses group expressions; the COMMA `,` actually
# creates the tuple. A single item requires a trailing comma: `(item,)`.


# ============================================================
# Q2: The "Mutable Element in Tuple" Paradox
# ============================================================
# Question: Demonstrate what happens when a tuple contains a mutable object (like a list).
# Explain the famous puzzle: `t[1] += [4]` modifies the list AND raises a TypeError!

print("\n=== Q2: The Mutable Tuple Paradox ===")

# Tuple containing a mutable list
hybrid = ("Alpha", [10, 20])
print(f"  Initial tuple: {hybrid}")

# Mutating the inner list via standard list methods succeeds completely:
hybrid[1].append(30)
print(f"  After hybrid[1].append(30): {hybrid}")

# The Famous Python Puzzle: Augmented Assignment `+=` on an inner list:
try:
    # Under the hood in bytecode:
    # 1. hybrid[1].extend([40]) succeeds in-place
    # 2. Assignment `hybrid[1] = ...` is attempted and raises TypeError!
    hybrid[1] += [40]
except TypeError as e:
    print(f"  hybrid[1] += [40] raised TypeError: {e}")

# The list WAS modified despite the exception!
print(f"  Tuple state after exception: {hybrid} (Element was added!)")

# Explanation: Augmented assignment `+=` performs in-place mutation and then assigns
# the result back to the target (`t[1] = result`). The tuple rejects the assignment,
# raising `TypeError`, but the in-place list modification had already succeeded!


# ============================================================
# Q3: Advanced Unpacking and Extended Starred Binding
# ============================================================
# Question: Demonstrate unpacking fixed, nested, and variable-length tuples
# using `*rest` and throwaway variables `_`.

print("\n=== Q3: Advanced Tuple Unpacking ===")

# 1. Starred unpacking: head, middle, tail
flight_data = ("BA-249", "London", "New York", 450, 7.5, "BOEING-777", "ON_TIME")
flight_num, origin, dest, *telemetry, status = flight_data

print(f"  Flight: {flight_num} from {origin} to {dest}")
print(f"  Telemetry (*middle): {telemetry}")
print(f"  Status: {status}")

# 2. Nested unpacking
student_record = ("Alice", (92, 88, 95), {"grade": "A"})
name, (m1, m2, m3), metadata = student_record
print(f"  Unpacked nested grades: {name} scored {m1}, {m2}, {m3} (Avg: {sum([m1, m2, m3])/3:.1f})")

# 3. Throwaway fields with underscore (_)
server_info = ("192.168.1.100", 8080, "tcp", "worker_pool_3", "active")
host, port, _, _, state = server_info
print(f"  Selected fields: Host={host}, Port={port}, State={state}")

# Explanation: `*` captures zero or more elements into a list. Nested parentheses
# in the assignment target destructure corresponding nested sequences.


# ============================================================
# Q4: Memory and Performance: Tuple vs List
# ============================================================
# Question: Compare memory usage (`sys.getsizeof`) and allocation speed between
# tuples and lists containing identical data. Explain CPython's tuple freelist.

print("\n=== Q4: Tuple vs List Memory Comparison ===")

sample_elements = (10, 20, 30, 40, 50, "hello", True)
as_list = list(sample_elements)
as_tuple = tuple(sample_elements)

list_bytes = sys.getsizeof(as_list)
tuple_bytes = sys.getsizeof(as_tuple)

print(f"  List size:  {list_bytes} bytes")
print(f"  Tuple size: {tuple_bytes} bytes")
print(f"  Memory savings: {((list_bytes - tuple_bytes) / list_bytes) * 100:.1f}% less memory for tuple")

# In CPython, small tuples (length 1 to 20) are cached in a freelist upon deletion,
# making subsequent tuple allocations practically instantaneous with zero malloc overhead.

# Explanation: Tuples are immutable, so they do not allocate extra memory for buffer
# growth. Lists must maintain excess capacity to support $O(1)$ amortized appends.


# ============================================================
# Q5: Named Tuples: collections.namedtuple vs typing.NamedTuple
# ============================================================
# Question: Demonstrate creating self-documenting data records using both
# `collections.namedtuple` and modern class-syntax `typing.NamedTuple`.

print("\n=== Q5: Named Tuples ===")

# Approach 1: collections.namedtuple (Factory function)
Point2D = namedtuple("Point2D", ["x", "y"])
p1 = Point2D(x=15, y=25)
print(f"  collections.namedtuple: {p1} | Dot access: ({p1.x}, {p1.y}) | Index access: p1[0]={p1[0]}")

# Approach 2: typing.NamedTuple (Clean class syntax with type annotations & default values)
class DatabaseConnection(NamedTuple):
    host: str
    port: int = 5432
    username: str = "postgres"
    ssl_enabled: bool = True

    def connection_url(self) -> str:
        protocol = "postgresql+ssl" if self.ssl_enabled else "postgresql"
        return f"{protocol}://{self.username}@{self.host}:{self.port}"

db = DatabaseConnection(host="db.internal.corp")
print(f"  typing.NamedTuple:     {db}")
print(f"  Method call:           {db.connection_url()}")
print(f"  Converted to dict:     {db._asdict()}")

# Explanation: NamedTuples retain all tuple performance benefits (immutability, memory
# footprint, tuple unpacking) while adding readable attribute access (`obj.attr`).


# ============================================================
# Q6: Hashability and Tuples as Dictionary Keys
# ============================================================
# Question: Prove that tuples can serve as dictionary keys and set elements,
# but ONLY if all their constituent elements are also hashable.

print("\n=== Q6: Hashability as Dictionary Keys ===")

# Tuples of immutables are hashable:
matrix_sparse = {
    (0, 0): "Origin",
    (1, 2): "Point A",
    (5, 8): "Point B"
}

print(f"  Sparse matrix lookup (1, 2): '{matrix_sparse[(1, 2)]}'")
print(f"  Hash of (1, 2): {hash((1, 2))}")

# Unhashable tuple: containing a list
unhashable_tuple = (1, 2, [3, 4])
try:
    bad_dict = {unhashable_tuple: "Invalid Key"}
except TypeError as e:
    print(f"  Tuple with mutable list rejected as dict key: {e}")

# Explanation: An object is hashable if its hash value never changes during its lifetime.
# A tuple is hashable if and only if every element inside it is hashable.


# ============================================================
# Q7: Returning Multiple Values from Functions
# ============================================================
# Question: Implement a statistical summary function that returns multiple values
# as a tuple, demonstrating structured error handling and destructuring.

print("\n=== Q7: Multiple Return Values ===")

def compute_statistics(values: list[float]) -> tuple[float, float, float, float]:
    """Returns (mean, median, minimum, maximum) as an implicit tuple."""
    if not values:
        raise ValueError("Cannot compute statistics on empty list")
        
    sorted_v = sorted(values)
    n = len(sorted_v)
    
    mean = sum(sorted_v) / n
    median = sorted_v[n // 2] if n % 2 != 0 else (sorted_v[n // 2 - 1] + sorted_v[n // 2]) / 2.0
    minimum = sorted_v[0]
    maximum = sorted_v[-1]
    
    return mean, median, minimum, maximum  # Implicit tuple creation!

dataset = [12.0, 45.0, 67.0, 23.0, 89.0, 34.0, 56.0]
avg, med, mn, mx = compute_statistics(dataset)
print(f"  Dataset: {dataset}")
print(f"  Unpacked stats: Mean={avg:.1f}, Median={med:.1f}, Min={mn:.1f}, Max={mx:.1f}")

# Explanation: When a Python function returns `a, b, c` separated by commas,
# Python automatically packages them into a single tuple `(a, b, c)`.


# ============================================================
# Q8: Lexicographical Tuple Comparison
# ============================================================
# Question: Demonstrate how Python compares tuples element by element from left to right.
# Use this property to sort complex employee records by multiple criteria.

print("\n=== Q8: Lexicographical Tuple Comparison ===")

# Comparison rules: compares first elements. If equal, moves to second, etc.
print(f"  (1, 2, 3) < (1, 2, 4):  {(1, 2, 3) < (1, 2, 4)}")
print(f"  (1, 9, 0) < (2, 0, 0):  {(1, 9, 0) < (2, 0, 0)} (Decided at index 0)")
print(f"  ('apple', 10) < ('apple', 20): {('apple', 10) < ('apple', 20)}")

# Multi-criteria sorting using tuple keys:
# Priority: 1. Dept ascending, 2. Salary descending, 3. Name ascending
staff = [
    {"name": "Alice",   "dept": "Eng",   "salary": 120_000},
    {"name": "Bob",     "dept": "Eng",   "salary": 140_000},
    {"name": "Charlie", "dept": "HR",    "salary": 80_000},
    {"name": "David",   "dept": "Eng",   "salary": 120_000},
]

staff_sorted = sorted(
    staff,
    key=lambda s: (s["dept"], -s["salary"], s["name"])
)

print("\n  Sorted staff (Dept asc, Salary desc, Name asc):")
for s in staff_sorted:
    print(f"    {s['dept']:<5} | ${s['salary']:>7,d} | {s['name']}")

# Explanation: Lexicographical comparison evaluates elements sequentially. Negating
# numeric values (`-s['salary']`) cleanly inverts the sort direction for that specific field.


# ============================================================
# Q9: Immutability Defenses and Sequence Conversion
# ============================================================
# Question: Enforce defensive immutability by converting incoming mutable collections
# into tuples to prevent downstream callers from tampering with shared state.

print("\n=== Q9: Defensive Immutability Enforcement ===")

class SecurityContext:
    def __init__(self, allowed_roles: list[str]):
        # DEFENSIVE COPY: Convert mutable list to immutable tuple
        self._roles = tuple(allowed_roles)

    @property
    def roles(self) -> tuple[str, ...]:
        return self._roles

user_roles = ["admin", "auditor"]
ctx = SecurityContext(user_roles)

print(f"  Security context roles: {ctx.roles}")

# Attacker tries to modify original list outside:
user_roles.append("super_root_access")
print(f"  External list mutated:  {user_roles}")
print(f"  SecurityContext roles:  {ctx.roles} (Protected & Untampered!)")

# Attacker tries to modify through property:
try:
    ctx.roles[0] = "hacked"  # type: ignore
except TypeError as e:
    print(f"  Direct mutation caught: {e}")

# Explanation: Converting mutable inputs (`list`, `set`) to `tuple` inside constructor
# prevents shared-reference side-effects and guarantees write-protection.


# ============================================================
# Q10: 2D & 3D Vector Geometry on Tuples
# ============================================================
# Question: Implement vector arithmetic functions on 3D coordinate tuples:
# Vector addition, scalar multiplication, dot product, cross product, and Euclidean norm.

print("\n=== Q10: 3D Vector Geometry on Tuples ===")

Vector3D = tuple[float, float, float]

def vec_add(u: Vector3D, v: Vector3D) -> Vector3D:
    return (u[0] + v[0], u[1] + v[1], u[2] + v[2])

def vec_scale(u: Vector3D, s: float) -> Vector3D:
    return (u[0] * s, u[1] * s, u[2] * s)

def vec_dot(u: Vector3D, v: Vector3D) -> float:
    return (u[0] * v[0]) + (u[1] * v[1]) + (u[2] * v[2])

def vec_cross(u: Vector3D, v: Vector3D) -> Vector3D:
    # Cross product formula: (u2*v3 - u3*v2, u3*v1 - u1*v3, u1*v2 - u2*v1)
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0]
    )

def vec_magnitude(u: Vector3D) -> float:
    return math.sqrt(vec_dot(u, u))

v1 = (1.0, 2.0, 3.0)
v2 = (4.0, 5.0, 6.0)

print(f"  Vector 1:            {v1}")
print(f"  Vector 2:            {v2}")
print(f"  v1 + v2:             {vec_add(v1, v2)}")
print(f"  v1 * 2.5:            {vec_scale(v1, 2.5)}")
print(f"  Dot Product (v1 . v2): {vec_dot(v1, v2)}")
print(f"  Cross Product(v1 x v2):{vec_cross(v1, v2)}")
print(f"  Magnitude |v1|:      {vec_magnitude(v1):.3f}")

# Summary Output
print("\n" + "=" * 55)
print("  All 10 Questions for Topic 03 - Q03 executed successfully!")
print("=" * 55)
