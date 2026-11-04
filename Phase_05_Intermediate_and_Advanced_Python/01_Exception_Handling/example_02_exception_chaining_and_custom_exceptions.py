"""
Phase 5 - Topic 01: Exception Handling
Example 02: Custom Domain Exceptions & Exception Chaining (`raise ... from err`)

Demonstrates:
  - Defining a custom exception class with structured diagnostic attributes
  - Wrapping low-level exceptions (`KeyError`) into domain exceptions (`ConfigurationError`)
    using `raise ... from err` so `__cause__` is preserved for debugging
"""


class ConfigurationError(Exception):
    """Domain-specific exception raised when required app configuration is invalid."""

    def __init__(self, setting_key: str, reason: str) -> None:
        super().__init__(f"Config key {setting_key!r} failed: {reason}")
        self.setting_key = setting_key
        self.reason = reason


def load_database_port(raw_env: dict[str, str]) -> int:
    """Extract and validate `DB_PORT` from `raw_env`, chaining underlying errors."""
    try:
        raw_port = raw_env["DB_PORT"]
        port = int(raw_port)
    except KeyError as err:
        raise ConfigurationError("DB_PORT", "missing required environment variable") from err
    except ValueError as err:
        raise ConfigurationError("DB_PORT", f"must be an integer, got {raw_env['DB_PORT']!r}") from err

    if not (1024 <= port <= 65535):
        raise ConfigurationError("DB_PORT", f"port {port} outside unprivileged range 1024..65535")
    return port


def main() -> None:
    print("=== 1. Valid Configuration ===")
    port = load_database_port({"DB_PORT": "5432"})
    print(f"  Loaded DB_PORT = {port}")

    print("\n=== 2. Catching Chained Domain Exceptions (`__cause__`) ===")
    test_envs = [
        {},
        {"DB_PORT": "not-a-port"},
        {"DB_PORT": "80"},
    ]
    for env in test_envs:
        try:
            load_database_port(env)
        except ConfigurationError as err:
            cause_name = type(err.__cause__).__name__ if err.__cause__ else "None"
            print(f"  Caught ConfigurationError: {err} | __cause__={cause_name}")


if __name__ == "__main__":
    main()
