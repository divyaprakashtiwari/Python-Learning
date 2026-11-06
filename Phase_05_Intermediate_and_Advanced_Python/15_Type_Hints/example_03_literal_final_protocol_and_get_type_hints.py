"""
Phase 5 - Topic 15: Type Hints
Example 03: `Literal`, `Final`, `Protocol` (Structural Subtyping), & `typing.get_type_hints()`

Demonstrates:
  - Restricting allowed values to specific constants with `Literal["r", "w"]`
  - Marking constants against reassignment with `Final`
  - Structural duck-typing with `typing.Protocol` (`@runtime_checkable`)
  - Resolving type annotations at runtime with `typing.get_type_hints()`
"""

from typing import Final, Literal, Protocol, get_type_hints, runtime_checkable


MAX_RETRIES: Final[int] = 3
LogLevel = Literal["DEBUG", "INFO", "ERROR"]


@runtime_checkable
class Renderable(Protocol):
    """Any object with a `.render() -> str` method satisfies `Renderable` (no inheritance needed!)."""

    def render(self) -> str: ...


class MarkdownBadge:
    """Does NOT inherit from `Renderable`, but implements `.render() -> str`."""

    def __init__(self, label: str) -> None:
        self.label = label

    def render(self) -> str:
        return f"**[{self.label}]**"


def emit_log(level: LogLevel, widget: Renderable) -> str:
    return f"[{level}] {widget.render()} (max_retries={MAX_RETRIES})"


def main() -> None:
    print("=== 1. Structural Subtyping with `Protocol` (`@runtime_checkable`) ===")
    badge = MarkdownBadge("BUILD PASSING")
    print(f"  isinstance(badge, Renderable): {isinstance(badge, Renderable)}")
    print(f"  emit_log output              : {emit_log('INFO', badge)}")

    print("\n=== 2. Runtime Introspection via `typing.get_type_hints()` ===")
    hints = get_type_hints(emit_log)
    for name, tp in hints.items():
        print(f"  {name:<8} -> {tp}")


if __name__ == "__main__":
    main()
