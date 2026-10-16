"""
Topic 02: Control Flow
Question 09: Ternary Operator (Conditional Expressions)

Master Python's conditional expressions: `X if condition else Y`,
short-circuit evaluation semantics, comprehension integration, lambda functions,
fallbacks, alternative idioms & their pitfalls, and dynamic object selection.
"""

# ============================================================
# Q1: Basic Ternary Syntax and Short-Circuit Evaluation
# ============================================================
# Question: Demonstrate the syntax `val_true if condition else val_false`.
# Prove that Python short-circuits the evaluation so that the unchosen branch is never executed.

print("=== Q1: Ternary Syntax and Short-Circuiting ===")

age = 20
status = "Adult" if age >= 18 else "Minor"
print(f"  Age: {age} -> Status: {status}")

# Short-circuit demonstration:
def expensive_call_a():
    print("    [Called Branch A]")
    return "Branch A Result"

def expensive_call_b():
    print("    [Called Branch B]")
    return "Branch B Result"

condition = True
print(f"\n  Evaluating condition = True:")
# Only expensive_call_a() will execute; expensive_call_b() is never evaluated!
chosen = expensive_call_a() if condition else expensive_call_b()
print(f"  Chosen: {chosen}")

# Proof: ZeroDivisionError is avoided because false branch is never evaluated
divisor = 0
safe_ratio = 100 / divisor if divisor != 0 else float('inf')
print(f"  Guarded division (divisor=0): {safe_ratio}")

# Explanation: `X if C else Y` evaluates condition `C` first. If `C` is truthy,
# `X` is evaluated and returned; `Y` is completely ignored (lazy evaluation).


# ============================================================
# Q2: Chained / Nested Ternary Expressions
# ============================================================
# Question: Classify a number as 'Positive', 'Negative', or 'Zero'
# using a chained ternary expression, and show how parentheses improve readability.

print("\n=== Q2: Chained / Nested Ternary ===")

def classify_sign_chained(num: float) -> str:
    """Classifies number using chained ternary expression."""
    return "Positive" if num > 0 else ("Negative" if num < 0 else "Zero")

test_nums = [42, -15, 0]
for n in test_nums:
    print(f"  Number {n:>3} -> {classify_sign_chained(n)}")

# Readability rule:
# While Python allows `a if c1 else b if c2 else c`, chaining more than 2 conditions
# is discouraged by PEP 8. Standard if/elif/else should be preferred for 3+ branches.


# ============================================================
# Q3: Ternary in Comprehensions (Transform vs Filter)
# ============================================================
# Question: Contrast using the ternary operator for item TRANSFORMATION
# `[A if C else B for x in list]` versus using `if` for item FILTERING `[x for x in list if C]`.

print("\n=== Q3: Ternary in Comprehensions ===")

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 1. TRANSFORMATION (Ternary before 'for'): preserves list length, alters values
parity_labels = ["Even" if n % 2 == 0 else "Odd" for n in numbers]
print(f"  Transformation (Parity labels): {parity_labels[:6]}...")

# Clamp values between [3, 8]
clamped = [3 if n < 3 else (8 if n > 8 else n) for n in numbers]
print(f"  Clamped values between 3 and 8: {clamped}")

# 2. FILTERING ('if' after 'for'): changes list length, keeps matching items
only_evens = [n for n in numbers if n % 2 == 0]
print(f"  Filtering (Only evens):         {only_evens}")

# 3. BOTH combined: transform elements that match a filter
evens_squared_or_halved = [n ** 2 if n > 4 else n // 2 for n in numbers if n % 2 == 0]
print(f"  Transform + Filter combined:    {evens_squared_or_halved}")

# Explanation:
# - `[<ternary> for x in it]`: shapes the output elements (always 1-to-1 length).
# - `[x for x in it if <filter>]`: selects which items from the iterable to include.


# ============================================================
# Q4: Ternary in Lambda Functions and Function Arguments
# ============================================================
# Question: Use ternary expressions inside lambda functions for custom sorting keys,
# and pass conditional values inline into function calls.

print("\n=== Q4: Ternary in Lambdas and Arguments ===")

# Sort priority: VIP users first, then standard users sorted by score
users = [
    {"name": "Alice",   "score": 90, "is_vip": False},
    {"name": "Bob",     "score": 85, "is_vip": True},
    {"name": "Charlie", "score": 98, "is_vip": False},
    {"name": "Diana",   "score": 70, "is_vip": True},
]

# Ternary inside lambda creates a composite tuple key: (0, -score) if VIP else (1, -score)
sorted_users = sorted(
    users,
    key=lambda u: (0 if u["is_vip"] else 1, -u["score"])
)

print("  Sorted users (VIPs first, then highest score):")
for u in sorted_users:
    tag = "[VIP]     " if u["is_vip"] else "[STANDARD]"
    print(f"    {tag} {u['name']:<8} (Score: {u['score']})")

# Inline function argument ternary
def log_event(level: str, message: str):
    print(f"    [{level}] {message}")

server_status_code = 500
log_event(
    "ERROR" if server_status_code >= 400 else "INFO",
    f"Server responded with code {server_status_code}"
)

# Explanation: Because Python ternary expressions are expressions (producing values)
# rather than statements, they can be embedded directly inside lambdas, tuples, and function args.


# ============================================================
# Q5: Alternative Ternary Idioms and Their Critical Pitfalls
# ============================================================
# Question: Compare Python's official ternary `X if C else Y` against two historic idioms:
# 1. Tuple indexing: `(Y, X)[C]`
# 2. Boolean short-circuit: `C and X or Y`
# Demonstrate why both alternatives have subtle, dangerous bugs.

print("\n=== Q5: Alternative Ternary Idioms & Pitfalls ===")

# PITFALL 1: Tuple Indexing: `(False_Val, True_Val)[condition]`
# Danger: Does NOT short circuit! Both sides are ALWAYS evaluated!
def explode():
    raise RuntimeError("Exploded! This branch should not run!")

try:
    # Attempting to use tuple indexing with conditional guard:
    result = ("Safe", explode())[False]
except RuntimeError as e:
    print(f"  Tuple indexing BUG caught: {e} (Evaluated both branches!)")

# PITFALL 2: `condition and True_Val or False_Val`
# Danger: If True_Val evaluates to falsy (0, "", False, None, []), it silently falls through to False_Val!
user_credit = 0  # Valid balance of 0 credits
# We want to display user_credit if authenticated, else "Login Required"
buggy_val = True and user_credit or "Login Required"
print(f"  'and/or' BUG: Got '{buggy_val}' instead of 0!")

# Correct Pythonic Ternary:
correct_val = user_credit if True else "Login Required"
print(f"  Official Ternary: Correctly got {correct_val}")

# Explanation: Never use `(Y, X)[C]` or `C and X or Y` as substitutes for `X if C else Y`.
# The official conditional expression guarantees short-circuiting and handles falsy values correctly.


# ============================================================
# Q6: Safe Null / None Fallbacks (Elvis Equivalent)
# ============================================================
# Question: Compare `val if val is not None else default` against `val or default`.
# Show where `val or default` fails on valid falsy inputs (0, False, empty string).

print("\n=== Q6: Safe Null / None Fallbacks ===")

def get_timeout_bad(config_val):
    # Bug: If config_val is 0 (immediate / non-blocking), '0 or 30' evaluates to 30!
    return config_val or 30

def get_timeout_good(config_val):
    # Correct: Only falls back if explicitly None
    return config_val if config_val is not None else 30

configs = [None, 15, 0]  # 0 is a valid zero-second timeout!
for cfg in configs:
    bad = get_timeout_bad(cfg)
    good = get_timeout_good(cfg)
    print(f"  Config input: {str(cfg):<5} -> 'or' fallback: {bad:<2} | 'ternary is not None': {good:<2}")

# Explanation: In Python, `or` checks truthiness, conflating `None` with `0`, `False`, and `""`.
# Using `val if val is not None else default` explicitly handles `None` without falsy collisions.


# ============================================================
# Q7: Dynamic Class / Strategy Selection via Ternary
# ============================================================
# Question: Select between two operational strategy classes using a ternary expression
# based on runtime environment configuration.

print("\n=== Q7: Dynamic Strategy Selection ===")

class CloudStorage:
    def upload(self, filename: str) -> str:
        return f"Uploading '{filename}' to AWS S3 bucket..."

class LocalStorage:
    def upload(self, filename: str) -> str:
        return f"Saving '{filename}' to local disk /var/uploads..."

is_production = True
# Instantiate the appropriate strategy via ternary expression
storage_service = CloudStorage() if is_production else LocalStorage()
print(f"  Storage Strategy ({'PROD' if is_production else 'DEV'}): {storage_service.upload('report.pdf')}")

is_production = False
storage_service = CloudStorage() if is_production else LocalStorage()
print(f"  Storage Strategy ({'PROD' if is_production else 'DEV'}): {storage_service.upload('test.png')}")

# Explanation: Ternary expressions can return class constructors or factory functions,
# providing concise Dependency Injection and strategy selection.


# ============================================================
# Q8: UI Pluralization and String Formatting
# ============================================================
# Question: Build an inline pluralization formatter that handles English grammar rules:
# "1 file" vs "5 files", "1 match" vs "3 matches", "1 person" vs "2 people".

print("\n=== Q8: Pluralization and Formatting ===")

def format_count_simple(count: int, singular: str, plural_suffix: str = "s") -> str:
    """Standard English suffix pluralization."""
    return f"{count} {singular}{'' if count == 1 else plural_suffix}"

def format_count_irregular(count: int, singular: str, plural: str) -> str:
    """Irregular noun pluralization."""
    return f"{count} {singular if count == 1 else plural}"

for n in [0, 1, 2, 5]:
    print(f"  Files:   {format_count_simple(n, 'file')}")
for n in [1, 3]:
    print(f"  Boxes:   {format_count_simple(n, 'box', 'es')}")
for n in [1, 4]:
    print(f"  People:  {format_count_irregular(n, 'person', 'people')}")

# Explanation: Ternary string interpolation `f"{'singular' if n == 1 else 'plural'}"`
# keeps presentation formatting inline without bulky multi-line if/else blocks.


# ============================================================
# Q9: Data Dictionary Normalization and Cleaning
# ============================================================
# Question: Clean a raw dictionary representing an external API payload.
# Use ternary expressions to normalize booleans, timestamps, and empty collections.

print("\n=== Q9: Data Cleaning and Normalization ===")

raw_user_records = [
    {"user_id": 1, "active_flag": "Y", "tags": ["admin", "dev"], "last_login": 1690000000},
    {"user_id": 2, "active_flag": "N", "tags": None,            "last_login": 0},
    {"user_id": 3, "active_flag": "y", "tags": [],              "last_login": None},
]

clean_records = []
for r in raw_user_records:
    clean_records.append({
        "id": r["user_id"],
        # Normalize active flag to boolean
        "is_active": True if str(r.get("active_flag")).upper() == "Y" else False,
        # Normalize null/empty tags to empty list
        "tags": r["tags"] if r["tags"] else [],
        # Normalize timestamp: "Never" if 0 or None, else string timestamp
        "last_login": "Never" if not r.get("last_login") else f"Timestamp({r['last_login']})"
    })

print("  Normalized Records:")
for c in clean_records:
    print(f"    User #{c['id']}: Active={c['is_active']} | Tags={c['tags']} | Login={c['last_login']}")

# Explanation: Ternary expressions allow dictionary literals to be constructed with
# normalized, validated values in a single declarative block.


# ============================================================
# Q10: Payment Gateway Surcharge and Discount Rule Engine
# ============================================================
# Question: Compute total transaction cost with inline conditional fees:
# Gateway fee (Credit Card: 2.9% + $0.30; Debit: 0.8% + $0.15; Crypto: 1.0%),
# International cross-border surcharge (+1.5% if international),
# and Volume discount (-0.5% if order > $1,000).

print("\n=== Q10: Payment Gateway Fee Engine ===")

def compute_payment_settlement(
    amount: float,
    payment_method: str,
    is_international: bool
) -> dict:
    """Calculates gateway fees using ternary conditional expressions."""
    method = payment_method.upper()
    
    # 1. Base rate percent based on payment method
    pct_rate = 0.029 if method == "CREDIT" else (0.008 if method == "DEBIT" else 0.010)
    
    # 2. Fixed transaction fee based on payment method
    fixed_fee = 0.30 if method == "CREDIT" else (0.15 if method == "DEBIT" else 0.00)
    
    # 3. Cross-border fee: add 1.5% if international
    intl_surcharge = 0.015 if is_international else 0.000
    
    # 4. Volume discount: 0.5% discount if amount > $1,000
    volume_discount = 0.005 if amount > 1000.0 else 0.000
    
    effective_rate = pct_rate + intl_surcharge - volume_discount
    total_fee = (amount * effective_rate) + fixed_fee
    net_payout = amount - total_fee
    
    return {
        "amount": amount,
        "method": method,
        "is_intl": is_international,
        "fee_rate_pct": round(effective_rate * 100, 2),
        "total_fee": round(total_fee, 2),
        "net_payout": round(net_payout, 2)
    }

transactions = [
    {"amount": 100.0,  "method": "Credit", "intl": False},
    {"amount": 100.0,  "method": "Debit",  "intl": False},
    {"amount": 500.0,  "method": "Credit", "intl": True},
    {"amount": 2500.0, "method": "Credit", "intl": False},
]

for tx in transactions:
    res = compute_payment_settlement(tx["amount"], tx["method"], tx["intl"])
    intl_label = "INTL" if res["is_intl"] else "DOMESTIC"
    print(f"  ${res['amount']:>7.2f} | {res['method']:<6} ({intl_label:<8}) -> Fee: ${res['total_fee']:>5.2f} ({res['fee_rate_pct']}%) | Net: ${res['net_payout']:>7.2f}")

# Summary Output
print("\n" + "=" * 55)
print("  All 10 Questions for Topic 02 - Q09 executed successfully!")
print("=" * 55)
