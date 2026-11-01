"""
Topic 03: Variables and Constants
Example 02: Multiple Assignment, Chained Assignment, and Variable Swapping

Demonstrates Pythonic idioms for assigning multiple variables on a single line,
initializing counters with chained assignment, and swapping values in-place.
"""


def main() -> None:
    # 1. Multiple assignment (positional tuple unpacking)
    latitude, longitude, city = 28.6139, 77.2090, "New Delhi"
    print("=== Multiple Assignment ===")
    print(f"City: {city} | Coordinates: ({latitude}, {longitude})")

    # 2. Chained assignment (only use with immutable values like int, float, str)
    wins = losses = draws = 0
    wins += 3
    draws += 1
    print("\n=== Chained Initialization ===")
    print(f"Match Record -> Wins: {wins}, Draws: {draws}, Losses: {losses}")

    # 3. Pythonic variable swapping without a temporary variable
    primary_server = "srv-mumbai-01"
    backup_server = "srv-bangalore-02"
    print("\n=== Variable Swapping (Failover Simulation) ===")
    print(f"Before Failover -> Primary: {primary_server} | Backup: {backup_server}")

    primary_server, backup_server = backup_server, primary_server
    print(f"After Failover  -> Primary: {primary_server} | Backup: {backup_server}")


if __name__ == "__main__":
    main()
