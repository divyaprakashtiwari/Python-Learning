# Phase 3 — Topic 11: Built-in Modules

## 1. Introduction

Python is famous for its **"Batteries Included"** philosophy: out of the box, the Python Standard Library ships with over 200 battle-tested **built-in and standard library modules** written in C and Python.

Before installing any third-party package via `pip`, you should know what Python's standard library already provides for:
- **Mathematics, Statistics & Cryptography:** `math`, `statistics`, `random`, `secrets`, `decimal`, `fractions`
- **Dates, Timezones & Timers:** `datetime`, `time`, `zoneinfo`
- **File Paths, OS & Runtime:** `pathlib`, `os`, `sys`, `shutil`, `subprocess`
- **Combinatorics, Functional & Data Structures:** `itertools`, `functools`, `collections`, `heapq`, `bisect`

---

## 2. Why is it used?

- **Zero External Dependencies:** Standard library modules work on every Python installation without `pip install`, supply-chain security risks, or version conflicts.
- **C-Level Speed & Numerical Accuracy:** Functions like `math.gcd()`, `math.isqrt()`, `math.isclose()`, and `itertools.combinations()` are implemented in optimized C code, running orders of magnitude faster than hand-written Python loops.
- **Cross-Platform Portability:** `pathlib.Path` automatically handles Windows backslashes (`\`) vs Linux/macOS forward slashes (`/`).

---

## 3. Syntax

```python
import itertools
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path
import random
import secrets

# 1. Exact integer square root & GCD
g = math.gcd(48, 180)
root = math.isqrt(1000)

# 2. Timezone-aware UTC datetime + timedelta
now_utc = datetime.now(timezone.utc)
tomorrow = now_utc + timedelta(days=1)

# 3. Object-oriented paths with `/` operator
config_file = Path(__file__).resolve().parent / "config.json"

# 4. Combinatorics
pairs = list(itertools.combinations(["A", "B", "C"], 2))
```

---

## 4. Explanation (Step-by-Step)

### Step 1: Numeric, Statistical & Randomness Modules (`math`, `statistics`, `random`, `secrets`)
- **`math`:** Provides `math.gcd(a, b)`, `math.lcm(a, b)`, `math.isqrt(n)` (exact integer floor square root without floating-point precision loss for huge integers!), `math.ceil()`, `math.floor()`, `math.comb(n, k)`, `math.perm(n, k)`, and `math.isclose(a, b)` for safe float comparisons.
- **`statistics`:** Computes `mean()`, `median()`, `mode()`, `stdev()`, and `quantiles()` directly on sequences.
- **`random` vs `secrets`:**
  - `random` uses the **Mersenne Twister** pseudo-random number generator (PRNG). It is fast and reproducible via `random.Random(seed)`, ideal for simulations, games, and ML data shuffling—**never** for security!
  - `secrets` uses the operating system's cryptographic entropy source (`os.urandom`) to generate unpredictable password reset tokens, session IDs, and API keys (`secrets.token_hex()`, `secrets. token_urlsafe()`).

### Step 2: Timezone-Aware Dates (`datetime`)
- Always prefer **timezone-aware** `datetime` objects (`datetime.now(timezone.utc)`) over "naive" datetimes (`datetime.now()` or deprecated `datetime.utcnow()`).
- Subtracting two `datetime` objects produces a `timedelta` object (`duration.total_seconds()`).
- Adding or subtracting a `timedelta(days=7, hours=4)` to a `datetime` handles month lengths and leap years automatically.

### Step 3: Modern File System Paths (`pathlib`) and Iterators (`itertools`)
- **`pathlib.Path`** replaces clunky `os.path.join(os.path.dirname(__file__), ...)` chains with clean object attributes (`.parent`, `.name`, `.stem`, `.suffix`) and the `/` path-joining operator.
- **`itertools`** provides memory-efficient $O(1)$-space lazy iterators: `combinations`, `permutations`, `product` (nested loop replacement), `accumulate` (running prefix sums), `chain`, and `islice`.

---

## 5. Minimum 3 Examples

### Example 1: Numeric & Randomness Utilities (`math`, `random`, `statistics`, `secrets`)
File: `example_01_math_random_and_statistics.py`

```python
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
```

---

### Example 2: Dates, Times, Timezones & Performance Timers (`datetime`, `time`)
File: `example_02_datetime_and_time_utilities.py`

```python
from datetime import datetime, timedelta, timezone


def main() -> None:
    print("=== 1. Timezone-Aware Datetimes & `timedelta` Arithmetic ===")
    # Fixed deterministic timestamp for reproducible learning output
    ist_tz = timezone(timedelta(hours=5, minutes=30), name="IST")
    deploy_time_utc = datetime(2026, 11, 4, 10, 30, 0, tzinfo=timezone.utc)
    deploy_time_ist = deploy_time_utc.astimezone(ist_tz)

    print(f"  Deploy Time (UTC) : {deploy_time_utc.isoformat()}")
    print(f"  Deploy Time (IST) : {deploy_time_ist.isoformat()}")

    sla_deadline = deploy_time_ist + timedelta(days=7, hours=4)
    print(f"  SLA Deadline (+7d 4h) : {sla_deadline.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    print("\n=== 2. Parsing Dates & Computing Duration Between Events ===")
    incident_start = datetime.fromisoformat("2026-11-04T14:15:00+05:30")
    incident_resolved = datetime.fromisoformat("2026-11-04T16:02:30+05:30")
    downtime: timedelta = incident_resolved - incident_start
    total_minutes = downtime.total_seconds() / 60.0
    print(f"  Downtime Duration : {downtime} ({total_minutes:.1f} minutes)")


if __name__ == "__main__":
    main()
```

---

### Example 3: System, Path, and Combinatorics Utilities (`pathlib`, `sys`, `itertools`)
File: `example_03_sys_pathlib_and_itertools.py`

```python
import itertools
from pathlib import Path
import sys


def main() -> None:
    print("=== 1. Cross-Platform Path Manipulation (`pathlib.Path`) ===")
    current_file = Path(__file__).resolve()
    topic_folder = current_file.parent
    phase_folder = topic_folder.parent

    print(f"  File name   : {current_file.name}")
    print(f"  File stem   : {current_file.stem} | suffix: {current_file.suffix}")
    print(f"  Topic dir   : {topic_folder.name}")
    print(f"  Phase dir   : {phase_folder.name}")

    # Virtual path construction with `/` operator
    config_path = topic_folder / "configs" / "settings.json"
    print(f"  Joined path : {config_path.relative_to(phase_folder).as_posix()}")

    print("\n=== 2. Combinatorics & Grouping (`itertools`) ===")
    servers = ["srv-A", "srv-B", "srv-C"]
    pairs = list(itertools.combinations(servers, 2))
    print(f"  2-Server Failover Pairs (combinations) : {pairs}")

    # `itertools.accumulate` for running prefix sums
    daily_signups = [120, 150, 90, 210, 180]
    cumulative = list(itertools.accumulate(daily_signups))
    print(f"  Daily signups     : {daily_signups}")
    print(f"  Cumulative prefix : {cumulative}")

    print("\n=== 3. Runtime Environment Metadata (`sys`) ===")
    v = sys.version_info
    print(f"  Python Version    : {v.major}.{v.minor}.{v.micro} | Platform: {sys.platform}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 1 (`example_01_math_random_and_statistics.py`)
```text
=== 1. `math` Module Essentials for Competitive Programming & Engineering ===
  math.gcd(48, 180)              = 12
  math.lcm(12, 18)               = 36
  math.isqrt(1000) (exact int)   = 31
  math.ceil(4.1), math.floor(4.9)= (5, 4)
  math.isclose(0.1+0.2, 0.3)     = True

=== 2. `statistics` Module for Data Summaries ===
  Samples : [110.0, 125.0, 98.0, 142.0, 115.0, 130.0]
  Mean    : 120.00 ms
  Median  : 120.00 ms
  Stdev   : 15.61 ms

=== 3. Reproducible `random` vs Cryptographic `secrets` ===
  Seeded rng.sample(candidates, 3) : ['Aarav', 'Vikram', 'Rohan']
  Seeded rng.randint(1000, 9999)   : 5506
  secrets.token_hex(8) length      : 16 hex chars
```

### Output — Example 2 (`example_02_datetime_and_time_utilities.py`)
```text
=== 1. Timezone-Aware Datetimes & `timedelta` Arithmetic ===
  Deploy Time (UTC) : 2026-11-04T10:30:00+00:00
  Deploy Time (IST) : 2026-11-04T16:00:00+05:30
  SLA Deadline (+7d 4h) : 2026-11-11 20:00:00 IST

=== 2. Parsing Dates & Computing Duration Between Events ===
  Downtime Duration : 1:47:30 (107.5 minutes)
```

### Output — Example 3 (`example_03_sys_pathlib_and_itertools.py`)
```text
=== 1. Cross-Platform Path Manipulation (`pathlib.Path`) ===
  File name   : example_03_sys_pathlib_and_itertools.py
  File stem   : example_03_sys_pathlib_and_itertools | suffix: .py
  Topic dir   : 11_Built_in_Modules
  Phase dir   : Phase_03_Functions_and_Modular_Programming
  Joined path : 11_Built_in_Modules/configs/settings.json

=== 2. Combinatorics & Grouping (`itertools`) ===
  2-Server Failover Pairs (combinations) : [('srv-A', 'srv-B'), ('srv-A', 'srv-C'), ('srv-B', 'srv-C')]
  Daily signups     : [120, 150, 90, 210, 180]
  Cumulative prefix : [120, 270, 360, 570, 750]

=== 3. Runtime Environment Metadata (`sys`) ===
  Python Version    : 3.13.7 | Platform: win32
```

---

## 7. Code Explanation

1. **`math.isclose(0.1 + 0.2, 0.3)` (`example_01`):** Because IEEE-754 binary floats represent `0.1 + 0.2` as `0.30000000000000004`, `0.1 + 0.2 == 0.3` is `False`. `math.isclose()` checks relative/absolute tolerance safely (`True`).
2. **Local `random.Random(42)` Instance (`example_01`):** Instead of calling global `random.seed(42)` (which mutates global RNG state for all libraries in the process), instantiating `rng = random.Random(42)` gives isolated, deterministic randomness.
3. **`timedelta.total_seconds()` (`example_02`):** Always use `downtime.total_seconds()` (which includes days, hours, minutes, and microseconds) rather than `downtime.seconds` (which wraps around every 24 hours and ignores `downtime.days`!).

---

## 8. Common Mistakes

1. **Confusing `timedelta.seconds` with `timedelta.total_seconds()`:**
   - For a `timedelta(days=2, hours=1)`, `.seconds` returns `3600` (ignoring the 2 days!), whereas `.total_seconds()` returns `176400.0` (the true total duration).
2. **Using `int(math.sqrt(n))` on very large integers ($n > 2^{53}$):**
   - `math.sqrt(n)` converts `n` to a 64-bit `float` first, losing precision for integers above $9 \times 10^{15}$. Always use `math.isqrt(n)` for exact integer square roots of arbitrarily large Python integers.
3. **Using `random.choice()` or `random.randint()` to generate OTPs, session IDs, or passwords:**
   - After observing 624 outputs of `random`, an attacker can reconstruct the entire internal state of the Mersenne Twister and predict all future random numbers. Always use the `secrets` module for security tokens.

---

## 9. Practice Questions

1. **Easy — Circle & Hypotenuse Calculator (`math`):**
   Write a function `triangle_metrics(a: float, b: float) -> tuple[float, float]` that uses `math.hypot(a, b)` to compute the hypotenuse of a right triangle and `math.degrees(math.atan2(a, b))` to compute its angle in degrees.

2. **Medium — Subscription Expiry Checker (`datetime`):**
   Write `days_until_expiry(start_iso: str, plan_days: int, current_iso: str) -> int` using `datetime.fromisoformat()` and `timedelta(days=plan_days)` to return the integer number of full days remaining (or negative if expired).

3. **Hard — Directory File Extension Summary (`pathlib` & `collections.Counter`):**
   Write `summarize_extensions(root_dir: str | Path) -> dict[str, int]` that recursively walks `Path(root_dir).rglob("*")` (filtering `p.is_file()`) and returns a count of files per extension (`.py`, `.md`, etc.).

---

## 10. Interview Questions

### Q1: What is the difference between `time.time()`, `time.monotonic()`, and `time.perf_counter()`?
**Answer:**
- **`time.time()`:** Returns wall-clock epoch time. It can jump backward or forward if the system clock is adjusted by NTP or daylight savings—never use it to measure elapsed execution time!
- **`time.monotonic()`:** Guaranteed never to go backward; ideal for long-running timeouts and schedulers.
- **`time.perf_counter()`:** Highest-resolution monotonic timer available on the CPU; ideal for benchmarking and profiling short functions.

### Q2: Why is `datetime.utcnow()` deprecated in Python 3.12+?
**Answer:**
`datetime.utcnow()` returns a **naive** `datetime` object (`tzinfo=None`) whose numbers happen to represent UTC. Many standard library methods (like `.timestamp()` or `.astimezone()`) assume naive datetimes are in the **local system timezone**, leading to silent timezone offset bugs. `datetime.now(timezone.utc)` returns a proper **timezone-aware** UTC datetime.

### Q3: How does `itertools.accumulate` help in solving Prefix Sum array problems?
**Answer:**
Given an array `nums`, `list(itertools.accumulate(nums, initial=0))` constructs the $O(n)$ prefix sum array in C in a single line. It also accepts custom binary functions (e.g., `itertools.accumulate(nums, max)` for running prefix maximums).
