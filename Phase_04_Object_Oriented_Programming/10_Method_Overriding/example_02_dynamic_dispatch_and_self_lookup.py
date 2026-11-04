"""
Phase 4 - Topic 10: Method Overriding
Example 02: Dynamic Dispatch Trap (Parent Method Calling an Overridden Child Method)

Demonstrates:
  - A classic OOP interview question: When `Parent.method_a(self)` calls `self.method_b()`,
    and `Child` overrides `method_b()`, which `method_b()` runs?
  - Answer: `Child.method_b()` runs because `self` is a `Child` instance!
  - How Private Name Mangling (`__internal_hook`) prevents accidental child overrides
"""


class BaseReportGenerator:
    """Base class whose `generate()` calls `self.format_header()` and `self.__security_stamp()`."""

    def format_header(self) -> str:
        return "=== BASE REPORT ==="

    def __security_stamp(self) -> str:
        """Private name-mangled method (`_BaseReportGenerator__security_stamp`)."""
        return "STAMP:VERIFIED-BASE"

    def generate(self) -> str:
        # `self.format_header()` is dispatched dynamically on `type(self)`!
        # `self.__security_stamp()` is mangled to `_BaseReportGenerator__security_stamp`!
        return f"{self.format_header()} | {self.__security_stamp()}"


class CustomPDFReportGenerator(BaseReportGenerator):
    """Overrides `format_header()` and defines its own `__security_stamp()`."""

    def format_header(self) -> str:
        return "=== CUSTOM PDF REPORT ==="

    def __security_stamp(self) -> str:
        """Mangled to `_CustomPDFReportGenerator__security_stamp` (does NOT override base!)."""
        return "STAMP:UNVERIFIED-CHILD"


def main() -> None:
    print("=== Dynamic Dispatch on `self.format_header()` vs Name-Mangled `__security_stamp()` ===")
    base_gen = BaseReportGenerator()
    pdf_gen = CustomPDFReportGenerator()

    print(f"  base_gen.generate() : {base_gen.generate()}")
    print(f"  pdf_gen.generate()  : {pdf_gen.generate()}")
    print("  Notice `pdf_gen.generate()` used Child's `format_header()`,")
    print("  but kept Base's `__security_stamp()` due to name mangling!")


if __name__ == "__main__":
    main()
