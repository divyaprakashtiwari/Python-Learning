"""
Phase 3 - Topic 05: Keyword Arguments
Example 02: Enforcing Keyword-Only Arguments (`*`) to Prevent Boolean Trap

Demonstrates:
  - The "Boolean Trap" anti-pattern: `export_report(data, True, False, True)`
  - Using bare `*` in a function signature to require self-documenting keyword calls
  - Inspecting `func.__kwdefaults__` for keyword-only parameter defaults
"""


def export_report_bad(
    title: str,
    include_charts: bool = False,
    compress_pdf: bool = False,
    send_email: bool = False,
) -> str:
    """Ambiguous at call site when booleans are passed positionally."""
    return (
        f"Report({title!r}): charts={include_charts}, "
        f"compress={compress_pdf}, email={send_email}"
    )


def export_report_clean(
    title: str,
    *,  # Forces all subsequent parameters to be passed by KEYWORD
    include_charts: bool = False,
    compress_pdf: bool = False,
    send_email: bool = False,
) -> str:
    """Self-documenting API: boolean flags MUST be named at the call site."""
    return (
        f"Report({title!r}): charts={include_charts}, "
        f"compress={compress_pdf}, email={send_email}"
    )


def main() -> None:
    print("=== 1. The 'Boolean Trap' in Positional Calls ===")
    # Looking at this call alone, nobody knows what `True, False, True` mean:
    mystery_call = export_report_bad("Q3 Revenue", True, False, True)
    print(f"  Positional booleans : {mystery_call}")

    print("\n=== 2. Keyword-Only (`*`) Enforces Self-Documenting Calls ===")
    clean_call = export_report_clean(
        "Q3 Revenue",
        include_charts=True,
        compress_pdf=False,
        send_email=True,
    )
    print(f"  Keyword-only flags  : {clean_call}")
    print(f"  __kwdefaults__ dict : {export_report_clean.__kwdefaults__}")

    print("\n=== 3. Positional Call to Keyword-Only Function Raises `TypeError` ===")
    try:
        export_report_clean("Q3 Revenue", True)  # type: ignore[misc]
    except TypeError as err:
        print(f"  Caught expected TypeError: {err}")


if __name__ == "__main__":
    main()
