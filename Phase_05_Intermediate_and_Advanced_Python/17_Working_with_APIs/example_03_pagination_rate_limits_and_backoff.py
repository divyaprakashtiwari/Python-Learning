"""
Phase 5 - Topic 17: Working with APIs
Example 03: Cursor Pagination, Rate-Limit Handling (`HTTP 429`), & Exponential Backoff

Demonstrates:
  - Consuming a paginated API (`next_cursor`) using a lazy generator function
  - Handling transient `HTTP 429 Too Many Requests` responses with retry/backoff logic
"""

from typing import Iterator


class SimulatedPaginatedAPI:
    """In-memory simulation of a cursor-paginated API that rate-limits once."""

    def __init__(self) -> None:
        self._pages = {
            "cursor_1": {"items": ["user_1", "user_2"], "next_cursor": "cursor_2"},
            "cursor_2": {"items": ["user_3", "user_4"], "next_cursor": "cursor_3"},
            "cursor_3": {"items": ["user_5"], "next_cursor": None},
        }
        self._failed_once = False

    def fetch_page(self, cursor: str) -> dict[str, object]:
        if cursor == "cursor_2" and not self._failed_once:
            self._failed_once = True
            raise RuntimeError("HTTP 429 Too Many Requests (Retry-After: 0.01s)")
        return self._pages[cursor]


def iterate_all_users(api: SimulatedPaginatedAPI, max_retries: int = 3) -> Iterator[str]:
    """Lazily yield all users across all pages, automatically retrying HTTP 429 errors."""
    cursor: str | None = "cursor_1"
    while cursor is not None:
        for attempt in range(1, max_retries + 1):
            try:
                page = api.fetch_page(cursor)
                break
            except RuntimeError as err:
                print(f"  [backoff] {err} -> retrying {cursor!r} (attempt {attempt}/{max_retries})")
                if attempt == max_retries:
                    raise
        for user in page["items"]:  # type: ignore[attr-defined]
            yield str(user)
        cursor = page["next_cursor"]  # type: ignore[assignment]


def main() -> None:
    print("=== Streaming Cursor-Paginated API with Automatic 429 Retry ===")
    api = SimulatedPaginatedAPI()
    all_users = list(iterate_all_users(api))
    print(f"  Collected all users across 3 pages: {all_users}")


if __name__ == "__main__":
    main()
