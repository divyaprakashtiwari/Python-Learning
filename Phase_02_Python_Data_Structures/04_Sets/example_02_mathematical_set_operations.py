"""
Topic 04: Sets
Example 02: Mathematical Set Theory Operations (`|`, `&`, `-`, `^`, Subsets)

Demonstrates Union, Intersection, Difference, Symmetric Difference, and subset
checks (`<=`, `.isdisjoint()`) to analyze skills across two engineering teams.
"""


def main() -> None:
    backend_team = {"Python", "SQL", "Docker", "Redis"}
    data_team = {"Python", "SQL", "Pandas", "Spark"}

    print("=== 1. Set Theory Operators ===")
    print(f"Backend Team              : {sorted(backend_team)}")
    print(f"Data Team                 : {sorted(data_team)}")
    print(f"Union (|)                 : {sorted(backend_team | data_team)}")
    print(f"Intersection (&)          : {sorted(backend_team & data_team)}")
    print(f"Difference (Backend - Data): {sorted(backend_team - data_team)}")
    print(f"Symmetric Diff (^)        : {sorted(backend_team ^ data_team)}")

    print("\n=== 2. Subset, Superset, and Disjoint Checks ===")
    core_requirements = {"Python", "SQL"}
    frontend_only = {"React", "TypeScript"}

    print(f"Are core_requirements a subset (<=) of backend_team? : {core_requirements <= backend_team}")
    print(f"Is backend_team a superset (>=) of core_requirements?: {backend_team >= core_requirements}")
    print(f"Are backend_team and frontend_only disjoint?         : {backend_team.isdisjoint(frontend_only)}")


if __name__ == "__main__":
    main()
