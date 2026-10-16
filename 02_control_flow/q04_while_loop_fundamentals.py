"""
Topic 02: Control Flow
Question 04: while Loop Fundamentals

Master condition-based iteration: termination invariants, retry loops,
mathematical algorithms (Euclid, Newton-Raphson, Collatz), binary search,
exponential backoff, and stateful game loops.
"""

import math
import time

# ============================================================
# Q1: Counter Invariants and Infinite Loop Safety
# ============================================================
# Question: Demonstrate the structure of a robust while loop:
# initialization, condition, state mutation, and safety timeout/guard against infinite loops.

print("=== Q1: while Loop Invariants and Safety ===")

def safe_countdown(start: int, max_iterations: int = 100) -> list[int]:
    """Demonstrates guarded countdown with iteration bounding."""
    current = start
    history = []
    iterations = 0
    
    # Safety invariant: iterations < max_iterations prevents runaway infinite loops
    while current > 0:
        history.append(current)
        current -= 1
        iterations += 1
        if iterations >= max_iterations:
            print(f"  Safety guard tripped after {iterations} iterations!")
            break
            
    return history

print(f"  Countdown from 5: {safe_countdown(5)}")

# Explanation: Every `while` loop requires three parts: initial state before the loop,
# a condition checked before each iteration, and state advancement inside the loop
# that eventually makes the condition False.


# ============================================================
# Q2: Simulated Input Validation and Retry Loop
# ============================================================
# Question: Implement an input validation retry loop that accepts a stream of inputs
# and prompts until valid input is encountered or max attempts are exhausted.

print("\n=== Q2: Validation and Retry Loop ===")

def validate_positive_even_number(simulated_inputs: list[str], max_attempts: int = 3) -> dict:
    """Processes input attempts until a valid positive even integer is provided."""
    attempts = 0
    input_index = 0
    
    while attempts < max_attempts and input_index < len(simulated_inputs):
        raw_val = simulated_inputs[input_index]
        input_index += 1
        attempts += 1
        
        try:
            val = int(raw_val)
            if val > 0 and val % 2 == 0:
                return {
                    "success": True,
                    "value": val,
                    "attempts": attempts,
                    "msg": f"Accepted valid input '{val}' on attempt #{attempts}"
                }
            else:
                reason = "must be positive" if val <= 0 else "must be even"
                print(f"    Attempt #{attempts} rejected ('{raw_val}'): {reason}")
        except ValueError:
            print(f"    Attempt #{attempts} rejected ('{raw_val}'): not an integer")

    return {
        "success": False,
        "value": None,
        "attempts": attempts,
        "msg": "Max attempts exceeded without valid input"
    }

user_stream = ["abc", "-4", "15", "42", "100"]
result = validate_positive_even_number(user_stream)
print(f"  Result: {result['msg']}")

# Explanation: `while` loops excel when the total number of iterations is unpredictable
# in advance, such as waiting for valid user input or network acknowledgment.


# ============================================================
# Q3: Pure Mathematical Integer Reversal
# ============================================================
# Question: Reverse the digits of an integer mathematically using a `while` loop
# (without converting the number to a string). Handle negative numbers and 32-bit overflow.

print("\n=== Q3: Mathematical Integer Reversal ===")

def reverse_integer(n: int) -> int:
    """Reverses an integer using modulo arithmetic and digit shifting."""
    is_negative = n < 0
    num = abs(n)
    reversed_num = 0
    
    while num > 0:
        # Extract least significant digit
        digit = num % 10
        # Append digit to reversed result
        reversed_num = (reversed_num * 10) + digit
        # Integer division truncates the processed digit
        num //= 10
        
    if is_negative:
        reversed_num = -reversed_num
        
    # Check 32-bit signed integer boundaries [-2^31, 2^31 - 1]
    if reversed_num < -2**31 or reversed_num > 2**31 - 1:
        return 0  # Overflow standard
        
    return reversed_num

test_ints = [12345, -9876, 1200, 7, 0, 1534236469]
for t in test_ints:
    rev = reverse_integer(t)
    print(f"  reverse_integer({t:<11}) -> {rev}")

# Explanation: Mathematical digit extraction uses `num % 10` to get the tail digit
# and `num //= 10` to shift right in base 10 until `num` drops to 0.


# ============================================================
# Q4: The Collatz Conjecture (3n + 1 Problem)
# ============================================================
# Question: Implement a while loop to compute the Collatz sequence for a positive integer:
# If n is even -> n = n // 2. If n is odd -> n = 3*n + 1.
# Continue until n reaches 1, tracking sequence length and maximum value reached.

print("\n=== Q4: Collatz Conjecture (3n + 1) ===")

def collatz_analysis(n: int) -> dict:
    """Calculates Collatz sequence path, step count, and peak value."""
    if n <= 0:
        raise ValueError("Collatz sequence only defined for n >= 1")
        
    current = n
    steps = 0
    peak = current
    trajectory = [current]
    
    while current != 1:
        if current % 2 == 0:
            current //= 2
        else:
            current = (3 * current) + 1
            
        steps += 1
        trajectory.append(current)
        if current > peak:
            peak = current
            
    return {
        "start": n,
        "steps": steps,
        "peak": peak,
        "path_sample": trajectory[:6] + (["..."] if len(trajectory) > 8 else []) + trajectory[-2:]
    }

seeds = [6, 19, 27]
for s in seeds:
    stats = collatz_analysis(s)
    path_str = " -> ".join(str(x) for x in stats["path_sample"])
    print(f"  Start: {s:<3} | Steps: {stats['steps']:<4} | Peak: {stats['peak']:<6} | Path: {path_str}")

# Explanation: The Collatz conjecture is an open mathematical problem. A `while current != 1:`
# loop is ideal because the stopping time cannot be computed a priori without running it.


# ============================================================
# Q5: Euclidean Algorithm for Greatest Common Divisor (GCD)
# ============================================================
# Question: Compute the GCD and LCM of two integers using Euclid's algorithm
# with a while loop, demonstrating its logarithmic efficiency over naive subtraction.

print("\n=== Q5: Euclidean Algorithm for GCD and LCM ===")

def compute_gcd(a: int, b: int) -> int:
    """Calculates GCD of a and b using Euclid's remainder division."""
    a, b = abs(a), abs(b)
    while b != 0:
        # a becomes b, and b becomes remainder of a divided by b
        a, b = b, a % b
    return a

def compute_lcm(a: int, b: int) -> int:
    """Calculates Least Common Multiple using relationship LCM(a, b) = |a * b| / GCD(a, b)."""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // compute_gcd(a, b)

gcd_pairs = [(48, 18), (101, 103), (270, 192), (1071, 462)]
for x, y in gcd_pairs:
    g = compute_gcd(x, y)
    l = compute_lcm(x, y)
    print(f"  GCD({x:>4}, {y:>4}) = {g:>4}  |  LCM({x:>4}, {y:>4}) = {l:>7,d}")

# Explanation: Euclid's remainder algorithm runs in $O(\log(\min(a, b)))$ steps,
# making it vastly superior to naive factor testing loops.


# ============================================================
# Q6: Binary Search with a While Loop
# ============================================================
# Question: Implement classic iterative binary search on a sorted list using `while low <= high:`.
# Return the exact index if found, or the index where it should be inserted to maintain sort order.

print("\n=== Q6: Iterative Binary Search ===")

def binary_search(sorted_arr: list[int], target: int) -> tuple[int, int]:
    """Iterative binary search. Returns (index_found_or_insertion_point, comparison_count)."""
    low = 0
    high = len(sorted_arr) - 1
    comparisons = 0
    
    while low <= high:
        comparisons += 1
        # Integer division avoids float inaccuracies
        mid = (low + high) // 2
        mid_val = sorted_arr[mid]
        
        if mid_val == target:
            return mid, comparisons  # Target found
        elif mid_val < target:
            low = mid + 1           # Target is in right half
        else:
            high = mid - 1          # Target is in left half
            
    # If not found, 'low' is the exact insertion point (bisect_left)
    return -low - 1, comparisons    # Negative return indicates not found (bitwise notation)

dataset = [3, 8, 12, 17, 24, 31, 45, 59, 72, 88, 95]
queries = [31, 3, 95, 50, 1]

print(f"  Sorted Array: {dataset}")
for q in queries:
    idx, comps = binary_search(dataset, q)
    if idx >= 0:
        print(f"    Target {q:>2}: Found at index {idx} ({comps} comparisons)")
    else:
        insertion_pt = -(idx + 1)
        print(f"    Target {q:>2}: NOT FOUND. Insertion index = {insertion_pt} ({comps} comparisons)")

# Explanation: Binary search divides the remaining candidate search space in half each step,
# achieving $O(\log N)$ performance compared to $O(N)$ linear scans.


# ============================================================
# Q7: Newton-Raphson Method for Square Roots
# ============================================================
# Question: Implement Newton's method to approximate square roots using a while loop:
# guess = (guess + n / guess) / 2.0. Continue until |guess^2 - n| < epsilon.

print("\n=== Q7: Newton-Raphson Square Root ===")

def sqrt_newton(n: float, epsilon: float = 1e-12, max_iter: int = 1000) -> dict:
    """Computes square root iteratively via Newton-Raphson approximation."""
    if n < 0:
        raise ValueError("Cannot compute real square root of negative number")
    if n == 0:
        return {"sqrt": 0.0, "iterations": 0}
        
    guess = n / 2.0
    iteration = 0
    
    while abs(guess * guess - n) > epsilon and iteration < max_iter:
        guess = (guess + n / guess) / 2.0
        iteration += 1
        
    return {
        "n": n,
        "sqrt": guess,
        "iterations": iteration,
        "error": abs(guess - math.sqrt(n))
    }

numbers_to_sqrt = [2.0, 10.0, 144.0, 123456.78]
for num in numbers_to_sqrt:
    res = sqrt_newton(num)
    print(f"  sqrt({num:>9.2f}) = {res['sqrt']:>14.10f} | Iterations: {res['iterations']} (Error: {res['error']:.2e})")

# Explanation: Newton's method exhibits quadratic convergence near the root:
# each iteration approximately doubles the number of accurate decimal places.


# ============================================================
# Q8: Exponential Backoff Polling Mechanism
# ============================================================
# Question: Implement a client retry loop with exponential backoff:
# While service call fails, increase delay exponentially (1s, 2s, 4s...) up to max attempts.

print("\n=== Q8: Exponential Backoff Retry Loop ===")

def simulate_flaky_service(attempt: int, fail_until_attempt: int = 3) -> bool:
    """Simulates a remote API that fails until a given attempt number."""
    return attempt >= fail_until_attempt

def call_service_with_backoff(max_retries: int = 4, base_delay: float = 0.05) -> dict:
    """Retries a failing operation with increasing delays using a while loop."""
    attempt = 1
    current_delay = base_delay
    success = False
    
    while attempt <= max_retries:
        print(f"    Attempt #{attempt}: contacting remote service...")
        # Check call result
        if simulate_flaky_service(attempt, fail_until_attempt=3):
            success = True
            print(f"    Attempt #{attempt}: SUCCESS! Connected to service.")
            break
        else:
            print(f"    Attempt #{attempt}: FAILED. Backing off for {current_delay:.2f}s...")
            time.sleep(current_delay)  # Short simulated delay
            current_delay *= 2.0       # Double the wait time
            attempt += 1

    return {"success": success, "total_attempts": attempt}

retry_report = call_service_with_backoff()
print(f"  Backoff summary: Final Status={'OK' if retry_report['success'] else 'FAILED'}")

# Explanation: Exponential backoff prevents "thundering herd" problems by spacing
# retries progressively further apart when external systems experience outages.


# ============================================================
# Q9: Arbitrary Base Number Converter
# ============================================================
# Question: Convert a positive decimal integer into any target base (from 2 up to 36)
# using repeated division and remainder extraction inside a while loop.

print("\n=== Q9: Arbitrary Base Number Converter ===")

def convert_to_base(n: int, base: int) -> str:
    """Converts a decimal number to an arbitrary base string (2 <= base <= 36)."""
    if not (2 <= base <= 36):
        raise ValueError("Base must be between 2 and 36")
    if n == 0:
        return "0"
        
    digits_map = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    is_negative = n < 0
    num = abs(n)
    remainders = []
    
    while num > 0:
        remainder = num % base
        remainders.append(digits_map[remainder])
        num //= base
        
    # Remainders are extracted least-significant first, so reverse
    result = "".join(reversed(remainders))
    return f"-{result}" if is_negative else result

test_decimal = 255
for b in [2, 8, 16, 26, 36]:
    base_str = convert_to_base(test_decimal, b)
    print(f"  Decimal {test_decimal} in Base {b:>2}: {base_str}")

# Explanation: Any integer in base $b$ is represented by repeated division:
# quotients form next states, while remainders represent digits from right to left.


# ============================================================
# Q10: Turn-Based Combat Simulation Game Loop
# ============================================================
# Question: Implement a complete turn-based RPG battle loop using a while loop:
# Player vs Boss. Loop runs while both have HP > 0.
# Process turns, critical hits, damage mitigation, and victory/defeat states.

print("\n=== Q10: Turn-Based Combat Game Loop ===")

def simulate_battle(player: dict, boss: dict) -> dict:
    """Executes turn-based combat until one combatant falls."""
    turn = 1
    combat_log = []
    
    while player["hp"] > 0 and boss["hp"] > 0:
        combat_log.append(f"--- Turn {turn} ---")
        
        # 1. Player Attack
        p_damage = max(1, player["attack"] - (boss["defense"] // 2))
        boss["hp"] = max(0, boss["hp"] - p_damage)
        combat_log.append(f"  Player strikes {boss['name']} for {p_damage} damage! ({boss['name']} HP: {boss['hp']})")
        
        if boss["hp"] <= 0:
            combat_log.append(f"  VICTORY! {boss['name']} has been defeated!")
            winner = "PLAYER"
            break
            
        # 2. Boss Counter-Attack
        b_damage = max(1, boss["attack"] - player["defense"])
        player["hp"] = max(0, player["hp"] - b_damage)
        combat_log.append(f"  {boss['name']} counters for {b_damage} damage! (Player HP: {player['hp']})")
        
        if player["hp"] <= 0:
            combat_log.append(f"  DEFEAT! Player was slain in battle.")
            winner = "BOSS"
            break
            
        turn += 1

    return {"winner": winner, "total_turns": turn, "log": combat_log}

hero = {"name": "Hero", "hp": 120, "attack": 25, "defense": 5}
dragon = {"name": "Dragon", "hp": 150, "attack": 22, "defense": 10}

battle_result = simulate_battle(hero, dragon)
for entry in battle_result["log"][:8]:  # Print first 8 lines
    print(f"  {entry}")
print(f"  ... [Battle concluded in {battle_result['total_turns']} turns with {battle_result['winner']} victory]")

# Summary Output
print("\n" + "=" * 55)
print("  All 10 Questions for Topic 02 - Q04 executed successfully!")
print("=" * 55)
