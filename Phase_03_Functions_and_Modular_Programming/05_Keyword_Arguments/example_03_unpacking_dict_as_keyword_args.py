"""
Phase 3 - Topic 05: Keyword Arguments
Example 03: Unpacking Dictionaries into Keyword Arguments (`**config`)

Demonstrates:
  - Using the `**` dictionary unpacking operator at the call site
  - Merging base configuration dictionaries with per-call keyword overrides
  - How Python validates unpacked dictionary keys against formal parameter names
"""


def connect_redis(
    host: str = "127.0.0.1",
    port: int = 6379,
    db: int = 0,
    decode_responses: bool = True,
) -> str:
    """Simulate opening a Redis client connection."""
    return (
        f"Redis(host={host!r}, port={port}, db={db}, "
        f"decode_responses={decode_responses})"
    )


def main() -> None:
    print("=== 1. Unpacking a Config Dictionary (`**prod_config`) ===")
    prod_config = {
        "host": "redis.cache.internal",
        "port": 6380,
        "db": 2,
        "decode_responses": True,
    }
    # `**prod_config` expands key-value pairs into keyword arguments
    conn_1 = connect_redis(**prod_config)  # type: ignore[arg-type]
    print(f"  Unpacked call : {conn_1}")

    print("\n=== 2. Combining Base Config with Overrides (`{**base, **override}`) ===")
    staging_override = {**prod_config, "host": "staging-redis.local", "db": 5}
    conn_2 = connect_redis(**staging_override)  # type: ignore[arg-type]
    print(f"  Overridden    : {conn_2}")

    print("\n=== 3. Unknown Key in Unpacked Dictionary Raises `TypeError` ===")
    invalid_config = {"host": "localhost", "max_connections": 50}
    try:
        connect_redis(**invalid_config)  # type: ignore[arg-type]
    except TypeError as err:
        print(f"  Caught expected TypeError: {err}")


if __name__ == "__main__":
    main()
