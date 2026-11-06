"""
Phase 5 - Topic 14: Virtual Environments and pip
Example 03: Parsing `requirements.txt` Specifiers & Semantic Version Constraints

Demonstrates:
  - Parsing a `requirements.txt` file (ignoring comments `#` and blank lines)
  - Understanding version specifiers: pinned (`==`), compatible release (`~=`), and range (`>=,<`)
"""

import re


REQ_LINE_RE = re.compile(
    r"^(?P<package>[A-Za-z0-9_.-]+)\s*(?P<operator>==|~=|>=|<=|>|<|!=)?\s*(?P<version>[0-9A-Za-z.*+-]+)?$"
)


def parse_requirements(raw_text: str) -> list[dict[str, str | None]]:
    """Parse non-comment lines from a `requirements.txt` content string."""
    parsed: list[dict[str, str | None]] = []
    for raw_line in raw_text.splitlines():
        # Strip inline comments and surrounding whitespace
        clean = raw_line.split("#", maxsplit=1)[0].strip()
        if not clean:
            continue
        match = REQ_LINE_RE.match(clean)
        if not match:
            raise ValueError(f"Invalid requirement line: {clean!r}")
        parsed.append(match.groupdict())
    return parsed


def main() -> None:
    sample_requirements = """
    # Production dependencies
    fastapi == 0.115.0        # Exact pin for reproducible builds
    pydantic ~= 2.9.0         # Compatible release: >= 2.9.0, < 2.10.0
    uvicorn >= 0.30.0
    pytest                    # Unpinned (dev tool)
    """

    print("=== Parsing `requirements.txt` Specifiers ===")
    for item in parse_requirements(sample_requirements):
        print(f"  package={item['package']:<10} | op={str(item['operator']):<4} | version={item['version']}")


if __name__ == "__main__":
    main()
