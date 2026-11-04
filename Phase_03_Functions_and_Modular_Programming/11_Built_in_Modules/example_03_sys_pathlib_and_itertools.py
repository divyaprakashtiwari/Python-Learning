"""
Phase 3 - Topic 11: Built-in Modules
Example 03: System, Path, and Combinatorics Utilities (`pathlib`, `sys`, `itertools`)

Demonstrates:
  - Object-oriented cross-platform path manipulation with `pathlib.Path`
  - Combinatorial iterators with `itertools` (`permutations`, `combinations`, `groupby`)
  - Runtime environment inspection with `sys` (`sys.version_info`, `sys.platform`)
"""

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
