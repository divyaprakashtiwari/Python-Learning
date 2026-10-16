"""
Topic 02: Control Flow
Question 05: break and continue Statements

Master control flow disruption: early loop termination (break), iteration skipping (continue),
breaking out of nested loops, primality testing, stream filtering, circuit breakers,
and fault-tolerant data parsers.
"""

import math

# ============================================================
# Q1: Early Loop Termination with break (Linear Search)
# ============================================================
# Question: Scan a stream of sensor telemetry records. Halt scanning immediately
# using `break` when a critical temperature threshold (> 85.0 C) is breached.

print("=== Q1: Early Termination with break ===")

telemetry = [
    {"sensor_id": "S-101", "temp": 42.1},
    {"sensor_id": "S-102", "temp": 55.4},
    {"sensor_id": "S-103", "temp": 68.0},
    {"sensor_id": "S-104", "temp": 89.6},  # Critical!
    {"sensor_id": "S-105", "temp": 44.0},
    {"sensor_id": "S-106", "temp": 51.2},
]

CRITICAL_THRESHOLD = 85.0
critical_sensor = None
scanned_count = 0

for reading in telemetry:
    scanned_count += 1
    if reading["temp"] > CRITICAL_THRESHOLD:
        critical_sensor = reading
        print(f"  ALERT: Sensor {reading['sensor_id']} breached limit with {reading['temp']} deg C!")
        break  # Terminate loop immediately; do not process further sensors

print(f"  Telemetry scan stopped after examining {scanned_count}/{len(telemetry)} records.")

# Explanation: `break` exits the nearest enclosing loop instantly, skipping all remaining
# iterations and any subsequent lines within the current loop block.


# ============================================================
# Q2: Skipping Iterations with continue (Comment/Blank Stripper)
# ============================================================
# Question: Parse raw configuration lines. Use `continue` to skip empty lines,
# whitespace-only lines, and comment lines starting with '#'.

print("\n=== Q2: Skipping Iterations with continue ===")

config_stream = [
    "# Database Configuration File",
    "host=127.0.0.1",
    "",
    "   ",
    "# Port and pool settings",
    "port=5432",
    "pool_size=20",
    "# End of configuration",
    ""
]

parsed_config = {}

for line in config_stream:
    cleaned = line.strip()
    
    # Skip blank or whitespace lines
    if not cleaned:
        continue
        
    # Skip comment lines
    if cleaned.startswith("#"):
        continue
        
    # Process valid key-value configuration line
    if "=" in cleaned:
        key, val = cleaned.split("=", 1)
        parsed_config[key.strip()] = val.strip()

print(f"  Parsed {len(parsed_config)} valid config parameters:")
for k, v in parsed_config.items():
    print(f"    {k} = {v}")

# Explanation: `continue` skips the rest of the current iteration and jumps directly
# to the next iteration step (evaluating the loop condition or advancing the iterator).


# ============================================================
# Q3: Primality Testing with Efficient break
# ============================================================
# Question: Implement an optimized primality test using trial division up to sqrt(N).
# Break immediately on finding the first divisor.

print("\n=== Q3: Primality Testing with break ===")

def is_prime(n: int) -> tuple[bool, int | None]:
    """Tests if n is prime. Returns (is_prime, first_divisor_if_composite)."""
    if n <= 1:
        return False, None
    if n <= 3:
        return True, None
    if n % 2 == 0:
        return False, 2
    if n % 3 == 0:
        return False, 3
        
    # Check factors of the form 6k +/- 1 up to sqrt(n)
    limit = int(math.isqrt(n))
    divisor_found = None
    
    for factor in range(5, limit + 1, 6):
        if n % factor == 0:
            divisor_found = factor
            break
        if n % (factor + 2) == 0:
            divisor_found = factor + 2
            break
            
    if divisor_found:
        return False, divisor_found
    return True, None

test_numbers = [2, 17, 49, 97, 121, 541, 1000]
for num in test_numbers:
    prime_status, div = is_prime(num)
    if prime_status:
        print(f"  Number {num:>4} is PRIME")
    else:
        print(f"  Number {num:>4} is COMPOSITE (divisible by {div})")

# Explanation: `break` avoids redundant testing once a factor is established,
# reducing composite detection to $O(1)$ in the best case and $O(\sqrt{N})$ worst case.


# ============================================================
# Q4: Breaking Out of Nested Loops (3 Clean Patterns)
# ============================================================
# Question: `break` only exits the innermost loop. Demonstrate 3 techniques
# to break out of multiple nested loops: Flag variable, Helper function with return,
# and Exception handling.

print("\n=== Q4: Breaking from Nested Loops ===")

grid = [
    [1, 2, 3, 4],
    [5, 6, 99, 8],  # 99 is target
    [9, 10, 11, 12]
]
target = 99

# Technique 1: Boolean Flag
print("  Technique 1: Boolean Flag")
found = False
for r_idx, row in enumerate(grid):
    for c_idx, val in enumerate(row):
        if val == target:
            print(f"    Target {target} located at ({r_idx}, {c_idx}) via flag")
            found = True
            break
    if found:
        break

# Technique 2: Helper Function with early return (Most Pythonic!)
print("  Technique 2: Helper Function with early return")
def find_in_grid(matrix: list[list[int]], needle: int):
    for r, row in enumerate(matrix):
        for c, v in enumerate(row):
            if v == needle:
                return r, c  # Instantly exits BOTH loops!
    return None

coords = find_in_grid(grid, target)
print(f"    Function return exited nested loops directly: coords = {coords}")

# Technique 3: Control flow exception (For deeply nested algorithms)
print("  Technique 3: Control Flow Exception")
class BreakNestedLoop(Exception):
    pass

try:
    for r, row in enumerate(grid):
        for c, v in enumerate(row):
            if v == target:
                raise BreakNestedLoop(r, c)
except BreakNestedLoop as e:
    print(f"    Exception cleanly broke out of all levels: coords = {e.args}")

# Explanation: In Python, encapsulating nested loops in a function with `return`
# is almost always the cleanest and most readable pattern.


# ============================================================
# Q5: Data Sanitization Pipeline with continue
# ============================================================
# Question: Clean and standardize a contact list. Use `continue` to filter out
# records missing names, containing invalid email formats, or incomplete phone numbers.

print("\n=== Q5: Data Sanitization Pipeline ===")

raw_contacts = [
    {"name": "Alice Smith", "email": "alice@site.com", "phone": "123-456-7890"},
    {"name": "", "email": "nobody@site.com", "phone": "555-000-1111"},
    {"name": "Bob Jones", "email": "bob_not_an_email", "phone": "987-654-3210"},
    {"name": "Carol White", "email": "carol@corp.org", "phone": "123-45"},  # Too short
    {"name": "David Brown", "email": "david@tech.io", "phone": "(555) 888-9999"},
]

clean_contacts = []

for contact in raw_contacts:
    name = contact.get("name", "").strip()
    if not name:
        continue  # Skip missing names
        
    email = contact.get("email", "").strip()
    if "@" not in email or "." not in email:
        continue  # Skip invalid emails
        
    # Extract digits from phone
    digits = [ch for ch in contact.get("phone", "") if ch.isdigit()]
    if len(digits) != 10:
        continue  # Skip incomplete phone numbers
        
    clean_contacts.append({
        "name": name,
        "email": email.lower(),
        "phone": f"+1-{''.join(digits[:3])}-{''.join(digits[3:6])}-{''.join(digits[6:])}"
    })

print(f"  Sanitized {len(clean_contacts)}/{len(raw_contacts)} valid records:")
for c in clean_contacts:
    print(f"    {c['name']:<14} | {c['email']:<16} | {c['phone']}")

# Explanation: Using `continue` for multiple validation guards produces linear,
# readable data cleaning pipelines without nested if/else pyramids.


# ============================================================
# Q6: Financial Circuit Breaker with break
# ============================================================
# Question: Process an incoming stream of banking ledger debits. Maintain account balance.
# If a single transaction exceeds max single limit or cumulative balance drops below zero,
# trip the circuit breaker with `break`.

print("\n=== Q6: Financial Circuit Breaker ===")

initial_balance = 1000.0
MAX_SINGLE_DEBIT = 600.0

pending_transactions = [
    {"id": "TX-01", "amount": 150.0},
    {"id": "TX-02", "amount": 250.0},
    {"id": "TX-03", "amount": 800.0},  # Exceeds max single debit
    {"id": "TX-04", "amount": 100.0},
]

current_balance = initial_balance
processed = []
breaker_tripped = False

for tx in pending_transactions:
    amt = tx["amount"]
    
    # Safety Check 1: Exceeds single transaction risk limit
    if amt > MAX_SINGLE_DEBIT:
        print(f"  CIRCUIT BREAKER: {tx['id']} of ${amt:.2f} exceeds limit ${MAX_SINGLE_DEBIT:.2f}. Halting ledger.")
        breaker_tripped = True
        break
        
    # Safety Check 2: Insufficient balance
    if amt > current_balance:
        print(f"  CIRCUIT BREAKER: Insufficient funds for {tx['id']}. Halting ledger.")
        breaker_tripped = True
        break
        
    current_balance -= amt
    processed.append(tx)

print(f"  Processed {len(processed)} transactions. Final Balance: ${current_balance:.2f} (Breaker Tripped: {breaker_tripped})")

# Explanation: Circuit breakers in financial software halt downstream mutations
# immediately upon encountering suspicious or boundary-violating states.


# ============================================================
# Q7: In-Place Consecutive Duplicate Filter with continue
# ============================================================
# Question: Given a sorted stream of items, filter out consecutive duplicates
# using `continue` without allocating sets or extra lookup tables.

print("\n=== Q7: Consecutive Duplicate Deduplication ===")

sorted_items = [1, 1, 2, 3, 3, 3, 4, 5, 5, 6, 7, 7, 7, 7, 8]
unique_items = []
previous_item = object()  # Sentinel object distinct from any valid item

for item in sorted_items:
    if item == previous_item:
        continue  # Skip consecutive duplicate
        
    unique_items.append(item)
    previous_item = item

print(f"  Original with duplicates: {sorted_items}")
print(f"  Deduplicated stream:      {unique_items}")

# Explanation: Tracking the immediate predecessor with a sentinel and using `continue`
# achieves $O(1)$ auxiliary space deduplication on sorted sequences.


# ============================================================
# Q8: Rate-Limiting Request Simulation with break and continue
# ============================================================
# Question: Simulate processing a web server request queue:
# - Blacklisted IPs trigger a security lock and halt queue processing (`break`).
# - Requests exceeding the per-minute quota are dropped with a warning (`continue`).
# - Legitimate requests are served.

print("\n=== Q8: Rate-Limiting Request Simulator ===")

request_queue = [
    {"ip": "192.168.1.10", "path": "/api/profile", "status": "OK"},
    {"ip": "192.168.1.10", "path": "/api/feed",    "status": "RATE_LIMITED"},
    {"ip": "10.0.0.5",     "path": "/api/status",  "status": "OK"},
    {"ip": "185.220.101.5","path": "/admin/hack",   "status": "BLACKLISTED"},  # Malicious
    {"ip": "10.0.0.8",     "path": "/api/users",   "status": "OK"},
]

served_count = 0
dropped_count = 0

for req in request_queue:
    ip = req["ip"]
    
    # Security Rule: Immediately stop on blacklisted threat
    if req["status"] == "BLACKLISTED":
        print(f"  SECURITY ALERT: Malicious IP {ip} detected! Halting incoming queue.")
        break
        
    # Rate Limit Rule: Drop burst requests
    if req["status"] == "RATE_LIMITED":
        dropped_count += 1
        print(f"  RATE LIMIT: Dropping excess request from {ip} to {req['path']}")
        continue
        
    served_count += 1
    print(f"  SERVED: {ip} -> {req['path']}")

print(f"  Queue summary: {served_count} served, {dropped_count} dropped.")

# Explanation: Combining `continue` (to shed unprocessable items) and `break` (to abort
# on existential hazards) models real-world traffic management systems.


# ============================================================
# Q9: 2D Grid / Maze Obstacle Navigation
# ============================================================
# Question: Traverse a grid coordinate route:
# Skip wall obstacles ('#') using `continue`, and stop at the destination ('E') using `break`.

print("\n=== Q9: 2D Grid Obstacle Navigation ===")

# Grid: '.' is passable path, '#' is obstacle/wall, 'E' is Exit
world_grid = [
    [".", ".", "#", "."],
    [".", "#", ".", "."],
    [".", ".", ".", "E"],
    [".", ".", "#", "."]
]

# Coordinate path to evaluate
path_to_walk = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (3, 3)]

steps_taken = 0
reached_goal = False

for r, c in path_to_walk:
    tile = world_grid[r][c]
    
    if tile == "#":
        print(f"  Step ({r}, {c}): Hit wall '#' -> Skipping step with continue")
        continue
        
    steps_taken += 1
    print(f"  Step ({r}, {c}): Moved onto '{tile}'")
    
    if tile == "E":
        print(f"  GOAL: Reached exit 'E' at ({r}, {c})!")
        reached_goal = True
        break

print(f"  Path result: Steps={steps_taken}, Goal Reached={reached_goal}")

# Explanation: Navigation algorithms utilize `continue` to discard invalid steps
# and `break` upon meeting the terminal objective.


# ============================================================
# Q10: Resilient CSV/Log Parser with Error Tolerance Budget
# ============================================================
# Question: Build a data pipeline parser with an error tolerance budget:
# Malformed rows are logged and skipped with `continue`.
# However, if malformed row count exceeds the error threshold (e.g., 3 errors),
# abort file ingestion immediately with `break` to avoid processing corrupted datasets.

print("\n=== Q10: Fault-Tolerant Parser with Error Budget ===")

raw_csv_rows = [
    "user_id,username,credits",      # Header
    "101,alice,500",                  # Valid
    "102,bob,invalid_credits",        # Error 1
    "103,carol,750",                  # Valid
    "corrupted_line_without_commas",  # Error 2
    "104,,300",                       # Error 3: Empty username
    "105,david,not_a_number",         # Error 4: Exceeds threshold of 3!
    "106,eve,900"                     # Should never be reached
]

MAX_ALLOWED_ERRORS = 3
error_count = 0
valid_records = []
aborted = False

for line_num, line in enumerate(raw_csv_rows[1:], start=2):
    parts = line.split(",")
    
    # Validation 1: Column count
    if len(parts) != 3:
        error_count += 1
        print(f"  [Line {line_num}] Format Error (Expected 3 columns, got {len(parts)})")
        if error_count > MAX_ALLOWED_ERRORS:
            print(f"  ABORT: Exceeded error budget of {MAX_ALLOWED_ERRORS}. Aborting ingestion!")
            aborted = True
            break
        continue
        
    uid, uname, credits_raw = parts
    
    # Validation 2: Field integrity
    if not uname.strip():
        error_count += 1
        print(f"  [Line {line_num}] Validation Error (Empty username)")
        if error_count > MAX_ALLOWED_ERRORS:
            print(f"  ABORT: Exceeded error budget of {MAX_ALLOWED_ERRORS}. Aborting ingestion!")
            aborted = True
            break
        continue
        
    # Validation 3: Type parsing
    try:
        credits_val = int(credits_raw)
    except ValueError:
        error_count += 1
        print(f"  [Line {line_num}] Type Error (Credits '{credits_raw}' is not integer)")
        if error_count > MAX_ALLOWED_ERRORS:
            print(f"  ABORT: Exceeded error budget of {MAX_ALLOWED_ERRORS}. Aborting ingestion!")
            aborted = True
            break
        continue
        
    valid_records.append({"id": uid, "username": uname, "credits": credits_val})

print(f"\n  Parser Final: Ingested {len(valid_records)} records, encountered {error_count} errors (Aborted: {aborted})")

# Summary Output
print("\n" + "=" * 55)
print("  All 10 Questions for Topic 02 - Q05 executed successfully!")
print("=" * 55)
