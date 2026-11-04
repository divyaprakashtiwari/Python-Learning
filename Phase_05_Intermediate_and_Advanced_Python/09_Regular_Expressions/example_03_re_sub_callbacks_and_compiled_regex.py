"""
Phase 5 - Topic 09: Regular Expressions
Example 03: Dynamic Redaction & Replacement with `re.sub()` Callbacks & Greedy vs Non-Greedy

Demonstrates:
  - Passing a callable function to `re.sub(pattern, repl_func, text)` for dynamic PII masking
  - Backreferences in replacement strings (`r"\\g<1>"`)
  - Greedy (`.*`) vs Non-Greedy/Lazy (`.*?`) quantifiers on HTML/tag extraction
"""

import re


def mask_email(match: re.Match[str]) -> str:
    """Mask email local-part keeping only first and last character: `a***v@domain.com`."""
    user = match.group("user")
    domain = match.group("domain")
    masked_user = user[0] + ("*" * max(1, len(user) - 2)) + user[-1] if len(user) > 2 else "***"
    return f"{masked_user}@{domain}"


def main() -> None:
    print("=== 1. Dynamic PII Masking with `re.sub(pattern, callable, text)` ===")
    support_ticket = "Contact aarav.sharma@example.com or diya@company.org for escalation."
    email_re = re.compile(r"(?P<user>[a-zA-Z0-9._%+-]+)@(?P<domain>[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})")
    redacted = email_re.sub(mask_email, support_ticket)
    print(f"  Original : {support_ticket}")
    print(f"  Redacted : {redacted}")

    print("\n=== 2. Greedy (`.*`) vs Non-Greedy (`.*?`) Quantifiers ===")
    snippet = "<b>First</b> and <b>Second</b>"
    print(f"  Greedy     `r'<b>.*</b>'`  -> {re.findall(r'<b>.*</b>', snippet)}")
    print(f"  Non-Greedy `r'<b>.*?</b>'` -> {re.findall(r'<b>.*?</b>', snippet)}")


if __name__ == "__main__":
    main()
