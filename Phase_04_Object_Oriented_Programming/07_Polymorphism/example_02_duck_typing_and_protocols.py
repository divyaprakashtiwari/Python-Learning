"""
Phase 4 - Topic 07: Polymorphism
Example 02: Duck Typing & Structural Polymorphism (`typing.Protocol`)

Demonstrates:
  - "If it walks like a duck and quacks like a duck, it's a duck"
  - Polymorphism WITHOUT a shared base class: unrelated classes sharing a `.read()` method
  - Using `typing.Protocol` (PEP 544) for static type-checked Duck Typing
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class ReadableStream(Protocol):
    """Structural Protocol: ANY object with `read() -> str` satisfies this interface!"""

    def read(self) -> str:
        ...


class InMemoryBuffer:
    """Does NOT inherit from `ReadableStream`, yet implements `.read() -> str`."""

    def __init__(self, text: str) -> None:
        self.text = text

    def read(self) -> str:
        return self.text


class MockNetworkSocket:
    """Completely unrelated class that also implements `.read() -> str`."""

    def __init__(self, packet_payload: str) -> None:
        self.packet_payload = packet_payload

    def read(self) -> str:
        return f"SOCKET_DATA:{self.packet_payload}"


def count_words_from_stream(stream: ReadableStream) -> int:
    """Accepts ANY object that quacks like a `ReadableStream` (has `.read()`)."""
    content = stream.read()
    return len(content.split())


def main() -> None:
    print("=== Duck Typing & `typing.Protocol` Without Shared Inheritance ===")
    mem_buf = InMemoryBuffer("Python duck typing enables flexible polymorphism")
    net_sock = MockNetworkSocket("SYN ACK payload received from peer")

    for source in (mem_buf, net_sock):
        is_stream = isinstance(source, ReadableStream)
        words = count_words_from_stream(source)
        print(
            f"  {type(source).__name__:<18} | "
            f"satisfies Protocol={is_stream} | word_count={words}"
        )


if __name__ == "__main__":
    main()
