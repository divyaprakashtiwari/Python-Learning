"""
Phase 3 - Topic 04: Default Arguments
Example 01: Optional Parameters with Default Values & Ordering Rules

Demonstrates:
  - Defining functions with sensible default parameter values
  - Calling a function with 1, 2, or all arguments
  - Why non-default (required) parameters must precede default parameters
"""


def build_connection_url(
    host: str,
    database: str,
    port: int = 5432,
    use_ssl: bool = True,
    timeout_sec: int = 30,
) -> str:
    """Build a PostgreSQL connection string with sensible production defaults."""
    ssl_mode = "require" if use_ssl else "disable"
    return (
        f"postgresql://{host}:{port}/{database}"
        f"?sslmode={ssl_mode}&connect_timeout={timeout_sec}"
    )


def main() -> None:
    print("=== 1. Using All Default Arguments ===")
    url_default = build_connection_url("db.internal.local", "analytics")
    print(f"  Default call          : {url_default}")

    print("\n=== 2. Overriding Defaults Positionally ===")
    url_custom_port = build_connection_url("localhost", "dev_db", 5433, False)
    print(f"  Positional override   : {url_custom_port}")

    print("\n=== 3. Overriding a Specific Default by Keyword ===")
    # Skip `port` and `use_ssl` defaults and override only `timeout_sec`
    url_custom_timeout = build_connection_url(
        "db.internal.local",
        "analytics",
        timeout_sec=5,
    )
    print(f"  Keyword skip override : {url_custom_timeout}")


if __name__ == "__main__":
    main()
