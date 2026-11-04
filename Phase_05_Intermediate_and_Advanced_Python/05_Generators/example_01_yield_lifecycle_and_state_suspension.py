"""
Phase 5 - Topic 05: Generators
Example 01: Generator Functions (`yield`) & Frame Suspension Lifecycle

Demonstrates:
  - How the presence of `yield` turns a function into a generator factory
  - Tracing execution pause and resumption across `next()` calls
  - Inspecting generator states (`GEN_CREATED`, `GEN_SUSPENDED`, `GEN_CLOSED`) via `inspect.getgeneratorstate()`
"""

import inspect
from typing import Iterator


def deployment_pipeline() -> Iterator[str]:
    """Yield deployment stages one by one, pausing local state between yields."""
    print("    [generator] Starting pipeline setup...")
    yield "Stage 1: Build Docker Image"
    print("    [generator] Resumed after Stage 1...")
    yield "Stage 2: Run Integration Tests"
    print("    [generator] Resumed after Stage 2...")
    yield "Stage 3: Rollout to Production"
    print("    [generator] Pipeline complete! Exiting function -> StopIteration.")


def main() -> None:
    print("=== Tracing Generator Suspension & Resumption ===")
    gen = deployment_pipeline()
    print(f"  State before first next(): {inspect.getgeneratorstate(gen)}")

    for step in range(1, 4):
        stage = next(gen)
        print(f"  Step {step} received: {stage!r} | state={inspect.getgeneratorstate(gen)}")

    try:
        next(gen)
    except StopIteration:
        print(f"  State after StopIteration: {inspect.getgeneratorstate(gen)}")


if __name__ == "__main__":
    main()
