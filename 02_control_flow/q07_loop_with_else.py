"""
Topic 02: Control Flow
Question 07: Loop with else Clause (for...else and while...else)

Master Python's unique `else` block on loops: understanding when it executes
(only when loop terminates normally without `break`), replacing clunky boolean flags,
search algorithms, retry exhaustion handlers, and distributed lock acquisition.
"""

import time
import random

# ============================================================
# Q1: Fundamentals of for...else and while...else
# ============================================================
# Question: Demonstrate the exact execution semantics of `for...else` and `while...else`:
# Show that the `else` block executes ONLY when the loop completes naturally without `break`.

print("=== Q1: Loop with else Semantics ===")

print("  Case 1: for-loop completes naturally (NO break) -> else EXECUTES")
for i in range(3):
    print(f"    Loop step i = {i}")
else:
    print("    [ELSE BLOCK] Loop finished completely without encountering break!")

print("\n  Case 2: for-loop hits break -> else is BYPASSED")
for i in range(3):
    print(f"    Loop step i = {i}")
    if i == 1:
        print("    [BREAK] Breaking loop early at i = 1")
        break
else:
    print("    [ELSE BLOCK] This will NEVER print because break was triggered.")

print("\n  Case 3: while-loop completes naturally (condition becomes False) -> else EXECUTES")
count = 2
while count > 0:
    print(f"    While count = {count}")
    count -= 1
else:
    print("    [ELSE BLOCK] While loop exited normally because count reached 0!")

# Explanation: In Python, `else` on a loop is best thought of as "no-break".
# It executes if and only if no `break` statement was executed in the loop body.


# ============================================================
# Q2: Eliminating Boolean Flags in Search Operations
# ============================================================
# Question: Search an employee registry for a specific ID.
# Contrast the verbose boolean flag approach with Python's clean `for...else` pattern.

print("\n=== Q2: Search without Boolean Flags ===")

employees = [
    {"id": "EMP-101", "name": "Alice Cooper", "dept": "Security"},
    {"id": "EMP-102", "name": "Bob Dylan",     "dept": "Design"},
    {"id": "EMP-103", "name": "Charlie Watts", "dept": "Audio"},
]

def search_with_flag(query_id: str):
    """Verbose pattern using explicit boolean flag."""
    found = False
    for emp in employees:
        if emp["id"] == query_id:
            print(f"    [Flag Pattern] Found {emp['name']} ({emp['dept']})")
            found = True
            break
    if not found:
        print(f"    [Flag Pattern] Error: Employee {query_id} not found.")

def search_with_for_else(query_id: str):
    """Pythonic pattern using for...else without extra flag variable."""
    for emp in employees:
        if emp["id"] == query_id:
            print(f"    [for...else]   Found {emp['name']} ({emp['dept']})")
            break
    else:
        print(f"    [for...else]   Error: Employee {query_id} not found.")

search_with_for_else("EMP-102")
search_with_for_else("EMP-999")

# Explanation: `for...else` eliminates the need to declare, mutate, and check a `found = False`
# flag variable, keeping scope clean and logic succinct.


# ============================================================
# Q3: Elegant Primality Test via for...else
# ============================================================
# Question: Test whether a given number is prime using `for...else`:
# If any factor is found, break; the `else` block declares the number prime.

print("\n=== Q3: Primality Test via for...else ===")

def check_prime_for_else(n: int) -> bool:
    """Tests primality using for...else."""
    if n <= 1:
        print(f"  {n:>3} is not prime (<= 1)")
        return False
        
    for factor in range(2, int(n ** 0.5) + 1):
        if n % factor == 0:
            print(f"  {n:>3} is COMPOSITE (divisible by {factor})")
            break
    else:
        # Reached ONLY if no factor divided n evenly
        print(f"  {n:>3} is PRIME")
        return True
        
    return False

test_candidates = [2, 13, 25, 29, 49, 97]
for c in test_candidates:
    check_prime_for_else(c)

# Explanation: The `else` clause belongs to the `for` statement, not the inner `if`.
# It triggers only when every divisor in the range has been tested and failed to divide $n$.


# ============================================================
# Q4: Retry Loop with Exhaustion Alert via while...else
# ============================================================
# Question: Implement a database connection retry loop with `while...else`:
# Break upon successful connection; if max attempts expire, the `else` block
# alerts DevOps that all retries were exhausted.

print("\n=== Q4: Retry Exhaustion Alert via while...else ===")

def connect_to_database(simulated_failures: int, max_attempts: int = 3) -> bool:
    """Attempts database connection with while...else exhaustion handling."""
    attempts = 0
    connected = False
    
    print(f"  Connecting with max {max_attempts} attempts (failures expected: {simulated_failures}):")
    while attempts < max_attempts:
        attempts += 1
        print(f"    Attempt #{attempts} connecting...")
        if attempts > simulated_failures:
            print(f"    Connected successfully on attempt #{attempts}!")
            connected = True
            break
        print(f"    Attempt #{attempts} connection timed out.")
    else:
        # Executed if attempts reached max_attempts without break
        print("    [ALERT] CRITICAL: All database connection retries exhausted! Triggering PagerDuty.")
        connected = False
        
    return connected

# Scenario A: Succeeds on attempt 2
connect_to_database(simulated_failures=1, max_attempts=3)
# Scenario B: Fails all 3 attempts
print()
connect_to_database(simulated_failures=5, max_attempts=3)

# Explanation: When a retry loop breaks upon success, the `else` block naturally
# serves as the "exhausted all retries without success" fallback handler.


# ============================================================
# Q5: All-Match Batch Validator via for...else
# ============================================================
# Question: Validate a financial transaction batch.
# If any single transaction is invalid, print error and break.
# If all transactions pass, the `else` block commits the batch atomically.

print("\n=== Q5: Batch Transaction Committer ===")

def commit_transaction_batch(batch: list[dict]):
    """Validates every transaction in batch before committing."""
    print(f"  Processing batch of {len(batch)} transactions:")
    for tx in batch:
        # Validation checks
        if tx.get("amount", 0) <= 0:
            print(f"    REJECTED: Transaction {tx['id']} has invalid amount ${tx['amount']:.2f}")
            break
        if not tx.get("signature_verified", False):
            print(f"    REJECTED: Transaction {tx['id']} failed cryptographic signature!")
            break
    else:
        # All transactions passed inspection!
        total_volume = sum(t["amount"] for t in batch)
        print(f"    SUCCESS: All transactions valid. Committed ${total_volume:,.2f} to ledger.")

valid_batch = [
    {"id": "TX-01", "amount": 100.0, "signature_verified": True},
    {"id": "TX-02", "amount": 250.0, "signature_verified": True},
    {"id": "TX-03", "amount": 50.0,  "signature_verified": True},
]

invalid_batch = [
    {"id": "TX-10", "amount": 120.0, "signature_verified": True},
    {"id": "TX-11", "amount": -40.0, "signature_verified": True},  # Invalid amount!
    {"id": "TX-12", "amount": 300.0, "signature_verified": True},
]

commit_transaction_batch(valid_batch)
commit_transaction_batch(invalid_batch)

# Explanation: The `else` block represents the "atomic commit" step that runs only
# after every element in the sequence has been verified without any early abort.


# ============================================================
# Q6: Isogram / Unique Character Checker via for...else
# ============================================================
# Question: Determine whether a word is an isogram (contains no repeating characters)
# using `for...else` with a tracking set.

print("\n=== Q6: Isogram Verifier via for...else ===")

def is_isogram(word: str) -> bool:
    """Checks if a word has no duplicate letters."""
    seen = set()
    cleaned = word.lower()
    
    for ch in cleaned:
        if ch.isalpha():
            if ch in seen:
                print(f"  '{word}' is NOT an isogram (duplicate letter '{ch}')")
                break
            seen.add(ch)
    else:
        print(f"  '{word}' is a VALID ISOGRAM (all letters unique)")
        return True
        
    return False

words_to_test = ["Dermatoglyphics", "Subdermatoglyphic", "Programming", "Python", "Alphabet"]
for w in words_to_test:
    is_isogram(w)

# Explanation: Early break on duplicate detection pairs cleanly with `else` confirming
# that the full word was scanned with zero collisions.


# ============================================================
# Q7: Detecting Sequence Continuity and First Gap
# ============================================================
# Question: Scan a sorted list of sequence IDs (e.g. invoice numbers).
# If a gap is found, break and report the missing number;
# `else` confirm that the sequence is strictly contiguous.

print("\n=== Q7: Sequence Continuity Checker ===")

def verify_invoice_sequence(invoice_ids: list[int]):
    """Verifies invoice numbers are contiguous without skipped numbers."""
    if not invoice_ids:
        print("  Empty invoice sequence.")
        return
        
    start_id = invoice_ids[0]
    for idx, expected in enumerate(range(start_id, start_id + len(invoice_ids))):
        actual = invoice_ids[idx]
        if actual != expected:
            print(f"  GAP DETECTED: Expected #{expected}, but found #{actual}! (Missing #{expected})")
            break
    else:
        print(f"  AUDIT PASSED: Invoices #{start_id} through #{invoice_ids[-1]} are fully contiguous.")

verify_invoice_sequence([1001, 1002, 1003, 1004, 1005])
verify_invoice_sequence([501, 502, 504, 505])  # 503 is missing!

# Explanation: `for expected in range(...)` generates expected sequential numbers;
# `else` confirms every single ledger item followed strict chronological continuity.


# ============================================================
# Q8: Conceptual Distinction: loop...else vs try...else vs if...else
# ============================================================
# Question: Clarify the three distinct uses of `else` in Python:
# `if...else`, `try...else`, and `for/while...else`.

print("\n=== Q8: The 3 Faces of else in Python ===")

# 1. if...else: Condition was False
x = 10
if x > 20:
    branch = "IF"
else:
    branch = "ELSE (Condition was False)"
print(f"  1. if...else:     {branch}")

# 2. try...else: NO exception was raised in try block
try:
    calc = 100 / 5
except ZeroDivisionError:
    calc = 0
else:
    print(f"  2. try...else:    ELSE (Executed because no exception occurred, result={calc})")

# 3. for...else: NO break occurred during loop
for item in [1, 2, 3]:
    pass
else:
    print("  3. for...else:    ELSE (Executed because loop did NOT break)")

# Explanation:
# - `if ... else`: Runs when condition is False.
# - `try ... else`: Runs when NO exception was raised.
# - `for/while ... else`: Runs when NO break was encountered.


# ============================================================
# Q9: Target Substring Search with Fallback Parser
# ============================================================
# Question: Scan an array of user-agent strings for a recognized mobile browser signature.
# If recognized, break; `else` fall back to desktop default renderer.

print("\n=== Q9: Substring Search with Fallback ===")

def detect_device_category(user_agent: str) -> str:
    """Matches known mobile tokens in user-agent string."""
    mobile_signatures = ["Mobile", "Android", "iPhone", "iPad", "Silk/"]
    
    for sig in mobile_signatures:
        if sig.lower() in user_agent.lower():
            device = f"Mobile Device (Matched: '{sig}')"
            break
    else:
        # None of the mobile signatures matched
        device = "Standard Desktop Browser (Fallback Default)"
        
    return device

test_agents = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36",
]

for ua in test_agents:
    print(f"  User-Agent: {ua[:40]}...")
    print(f"    -> Category: {detect_device_category(ua)}")

# Explanation: Using `for...else` to detect tokens provides a self-contained lookup
# with built-in default fallback behavior.


# ============================================================
# Q10: Distributed Lock Acquisition with Jitter and while...else
# ============================================================
# Question: Simulate distributed lock acquisition using `while...else`:
# Attempt to acquire lock up to N times with simulated contention.
# If acquired, break; `else` raise an alert that lock could not be secured.

print("\n=== Q10: Distributed Lock Acquisition ===")

def acquire_distributed_lock(lock_name: str, max_attempts: int = 4) -> dict:
    """Simulates distributed lock acquisition using while...else."""
    attempts = 0
    acquired = False
    
    # Deterministic simulation: succeeds on attempt 3
    success_attempt = 3
    
    while attempts < max_attempts:
        attempts += 1
        print(f"    Lock [{lock_name}]: Attempt #{attempts} requesting lease...")
        
        # Simulate contention check
        if attempts == success_attempt:
            acquired = True
            print(f"    Lock [{lock_name}]: LEASE GRANTED on attempt #{attempts}!")
            break
            
        print(f"    Lock [{lock_name}]: Busy/Contention. Retrying...")
    else:
        print(f"    Lock [{lock_name}]: FAILED to acquire lease after {max_attempts} attempts!")
        acquired = False
        
    return {"lock": lock_name, "acquired": acquired, "attempts": attempts}

lock_result = acquire_distributed_lock("RESOURCE_ORDERS_DB")
print(f"  Lock Result: Status={'ACQUIRED' if lock_result['acquired'] else 'TIMEOUT'}")

# Summary Output
print("\n" + "=" * 55)
print("  All 10 Questions for Topic 02 - Q07 executed successfully!")
print("=" * 55)
