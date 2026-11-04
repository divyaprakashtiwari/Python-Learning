"""
Phase 4 - Topic 08: Encapsulation
Example 03: Preventing Internal Collection Mutation (Defensive Copying & Read-Only Views)

Demonstrates:
  - A subtle encapsulation leak: returning a direct reference to an internal `list` or `dict`
    allows callers to mutate private state without going through validation methods!
  - Fixing the leak by returning a `tuple` or shallow copy from the `@property`
"""


class InvestmentPortfolio:
    """Protects its internal holdings list from unauthorized external mutation."""

    def __init__(self, owner: str) -> None:
        self.owner = owner
        self._tickers: list[str] = []

    def add_ticker(self, symbol: str) -> None:
        cleaned = symbol.strip().upper()
        if not cleaned.isalpha() or len(cleaned) > 10:
            raise ValueError(f"Invalid ticker symbol: {symbol!r}")
        if cleaned not in self._tickers:
            self._tickers.append(cleaned)

    @property
    def tickers_leaky(self) -> list[str]:
        """DANGEROUS: Returns direct reference to internal `_tickers` list!"""
        return self._tickers

    @property
    def tickers(self) -> tuple[str, ...]:
        """SAFE: Returns an immutable `tuple` snapshot so callers cannot mutate `_tickers`."""
        return tuple(self._tickers)


def main() -> None:
    portfolio = InvestmentPortfolio("Divya")
    portfolio.add_ticker("TCS")
    portfolio.add_ticker("INFY")

    print("=== 1. Safe Encapsulated Property (`portfolio.tickers` -> `tuple`) ===")
    safe_view = portfolio.tickers
    print(f"  portfolio.tickers : {safe_view} (type: {type(safe_view).__name__})")

    print("\n=== 2. Demonstrating Why Returning Raw Internal Lists Breaks Encapsulation ===")
    portfolio.tickers_leaky.append("999_INVALID_TICKER!!!")
    print(f"  After external `.append()` on leaky property : {portfolio.tickers}")


if __name__ == "__main__":
    main()
