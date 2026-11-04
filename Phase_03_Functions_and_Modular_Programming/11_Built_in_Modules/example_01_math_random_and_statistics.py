"""
Phase 3 - Topic 11: Built-in Modules
Example 01: Numeric & Randomness Utilities (`math`, `random`, `statistics`, `secrets`)

Demonstrates:
  - Precision math functions (`math.gcd`, `math.isqrt`, `math.ceil`, `math.isclose`)
  - Descriptive statistics (`statistics.mean`, `median`, `stdev`)
  - Reproducible pseudo-random sampling (`random.seed`, `choice`, `sample`)
    vs cryptographically secure tokens (`secrets.token_hex`)
"""

import math
import random
import secrets
import statistics


def main() -> None:
    print("=== 1. `math` Module Essentials for Competitive Programming & Engineering ===")
    print(f"  math.gcd(48, 180)              = {math.gcd(48, 180)}")
    print(f"  math.lcm(12, 18)               = {math.lcm(12, 18)}")
    print(f"  math.isqrt(1000) (exact int)   = {math.isqrt(1000)}")
    print(f"  math.ceil(4.1), math.floor(4.9)= ({math.ceil(4.1)}, {math.floor(4.9)})")
    print(f"  math.isclose(0.1+0.2, 0.3)     = {math.isclose(0.1 + 0.2, 0.3)}")

    print("\n=== 2. `statistics` Module for Data Summaries ===")
    response_times = [110.0, 125.0, 98.0, 142.0, 115.0, 130.0]
    print(f"  Samples : {response_times}")
    print(f"  Mean    : {statistics.mean(response_times):.2f} ms")
    print(f"  Median  : {statistics.median(response_times):.2f} ms")
    print(f"  Stdev   : {statistics.stdev(response_times):.2f} ms")

    print("\n=== 3. Reproducible `random` vs Cryptographic `secrets` ===")
    rng = random.Random(42)  # Deterministic local RNG instance (seed=42)
    candidates = ["Aarav", "Priya", "Rohan", "Ananya", "Vikram"]
    print(f"  Seeded rng.sample(candidates, 3) : {rng.sample(candidates, 3)}")
    print(f"  Seeded rng.randint(1000, 9999)   : {rng.randint(1000, 9999)}")
    # `secrets` is used for security-sensitive API keys/reset tokens (not predictable)
    api_token = secrets.token_hex(8)
    print(f"  secrets.token_hex(8) length      : {len(api_token)} hex chars")


if __name__ == "__main__":
    main()
