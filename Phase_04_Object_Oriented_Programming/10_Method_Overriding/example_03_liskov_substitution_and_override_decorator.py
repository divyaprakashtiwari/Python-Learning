"""
Phase 4 - Topic 10: Method Overriding
Example 03: The Liskov Substitution Principle (LSP) & `@typing.override` (Python 3.12+)

Demonstrates:
  - Using `@typing.override` (PEP 698, Python 3.12+) to document and type-check overrides
  - Overriding a `@property` in a subclass
  - Respecting the Liskov Substitution Principle (signature and return type compatibility)
"""

from typing import override


class BaseRateLimiter:
    """Base rate limiter allowing 60 requests per minute."""

    @property
    def max_requests_per_min(self) -> int:
        return 60

    def check_quota(self, used_requests: int) -> tuple[bool, int]:
        """Return `(is_allowed, remaining_quota)`."""
        remaining = max(0, self.max_requests_per_min - used_requests)
        return used_requests < self.max_requests_per_min, remaining


class EnterpriseRateLimiter(BaseRateLimiter):
    """Overrides the `max_requests_per_min` property and extends `check_quota`."""

    def __init__(self, burst_bonus: int = 200) -> None:
        self.burst_bonus = burst_bonus

    @property
    @override
    def max_requests_per_min(self) -> int:
        return 1000 + self.burst_bonus

    @override
    def check_quota(self, used_requests: int) -> tuple[bool, int]:
        # Preserves exact input/output contract `(bool, int)` required by LSP
        return super().check_quota(used_requests)


def simulate_traffic(limiter: BaseRateLimiter, current_load: int) -> None:
    """Works seamlessly with `BaseRateLimiter` or any LSP-compliant subclass."""
    allowed, rem = limiter.check_quota(current_load)
    print(
        f"  [{type(limiter).__name__:<21}] load={current_load:<4} | "
        f"limit={limiter.max_requests_per_min:<4} -> allowed={allowed}, remaining={rem}"
    )


def main() -> None:
    print("=== Overriding `@property` & Methods with `@typing.override` (Python 3.12+) ===")
    free_tier = BaseRateLimiter()
    enterprise_tier = EnterpriseRateLimiter(burst_bonus=500)

    simulate_traffic(free_tier, 80)
    simulate_traffic(enterprise_tier, 80)


if __name__ == "__main__":
    main()
