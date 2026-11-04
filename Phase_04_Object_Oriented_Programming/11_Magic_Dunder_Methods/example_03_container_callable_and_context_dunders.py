"""
Phase 4 - Topic 11: Magic/Dunder Methods
Example 03: Container (`__len__`, `__getitem__`), Callable (`__call__`), and Context Manager (`__enter__`, `__exit__`)

Demonstrates:
  - Making an object behave like a sequence (`len(playlist)`, `playlist[0]`, `for song in playlist`)
  - Making an object callable like a function (`__call__`)
  - Making an object work with the `with` statement (`__enter__` and `__exit__`)
"""

from typing import Iterator


class BatchJobSession:
    """
    Demonstrates Container (`__len__`, `__getitem__`, `__iter__`),
    Callable (`__call__`), and Context Manager (`__enter__`, `__exit__`) dunders.
    """

    def __init__(self, session_name: str) -> None:
        self.session_name = session_name
        self._tasks: list[str] = []
        self.is_open: bool = False

    # 1. Context Manager Protocol (`with BatchJobSession(...) as session:`)
    def __enter__(self) -> "BatchJobSession":
        self.is_open = True
        print(f"  [__enter__] Opened session '{self.session_name}'")
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> bool:
        self.is_open = False
        print(f"  [__exit__ ] Closed session '{self.session_name}' ({len(self)} tasks queued)")
        return False  # Do not suppress exceptions

    # 2. Callable Protocol (`session("task_name")` adds a task)
    def __call__(self, task_name: str) -> None:
        if not self.is_open:
            raise RuntimeError("Cannot queue tasks when session is closed")
        self._tasks.append(task_name)

    # 3. Container Protocol (`len(session)`, `session[i]`, `for t in session`)
    def __len__(self) -> int:
        return len(self._tasks)

    def __getitem__(self, index: int) -> str:
        return self._tasks[index]

    def __iter__(self) -> Iterator[str]:
        return iter(self._tasks)


def main() -> None:
    print("=== Using `__enter__`, `__call__`, `__len__`, `__getitem__`, and `__exit__` ===")
    with BatchJobSession("Nightly-ETL") as job:
        # Calling the `job` object like a function invokes `job.__call__(...)`!
        job("extract_users")
        job("transform_orders")
        job("load_warehouse")

        print(f"  len(job)   : {len(job)}")
        print(f"  job[0]     : {job[0]!r}")
        print(f"  All tasks  : {list(job)}")


if __name__ == "__main__":
    main()
