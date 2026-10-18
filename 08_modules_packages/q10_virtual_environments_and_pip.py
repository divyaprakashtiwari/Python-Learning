"""
Topic 08: Modules and Packages - Question 10: Virtual Environments and pip

A comprehensive collection of 10 standalone, runnable exercises exploring
Python virtual environments (venv), isolation mechanics (sys.prefix vs sys.base_prefix),
the site module, importlib.metadata, requirements.txt parsing, and dependency solvers.

Questions Covered:
 1. Virtual Environment Anatomy: sys.prefix vs sys.base_prefix isolation checks.
 2. The site Module: Inspecting site-packages search paths and user site flags.
 3. Programmatic Venv Creation: Using standard library venv.EnvBuilder.
 4. Parsing requirements.txt: Handling version specifiers (==, >=, <=, ~=) and comments.
 5. Semantic Version Comparison: Parsing and ordering SemVer (major, minor, patch) tuples.
 6. Programmatic pip freeze Simulation: Inspecting packages with importlib.metadata.
 7. Package Metadata & Dependencies: Reading Requires-Dist, Summary, and License headers.
 8. Entry Points Discovery: Inspecting CLI entry points using importlib.metadata.entry_points.
 9. Dependency Conflict Detection: Finding incompatible version pin collisions.
10. Advanced Project: Package Dependency Graph & Constraint Solver Engine.
"""

from importlib import metadata
import os
import re
import shutil
import site
import sys
import tempfile
from typing import Any, NamedTuple


# ==============================================================================
# Question 1: Virtual Environment Anatomy (sys.prefix vs sys.base_prefix)
# ==============================================================================
def is_in_virtual_environment() -> bool:
    """
    Returns True if the current interpreter is running inside a virtual environment.
    Python sets sys.base_prefix to the underlying system Python path,
    while sys.prefix points to the virtualenv directory.
    """
    return getattr(sys, "base_prefix", sys.prefix) != sys.prefix


def exercise_q1_venv_anatomy() -> None:
    """
    Demonstrate detecting active virtual environments via sys.prefix inspection.
    """
    print("=== Q1: Virtual Environment Anatomy ===")

    in_venv = is_in_virtual_environment()
    prefix = sys.prefix
    base_prefix = getattr(sys, "base_prefix", sys.prefix)

    assert isinstance(prefix, str)
    assert isinstance(base_prefix, str)

    print(f"  sys.prefix:      {prefix}")
    print(f"  sys.base_prefix: {base_prefix}")
    print(f"  Is Virtual Env:  {in_venv}")


# ==============================================================================
# Question 2: The site Module & Site-Packages
# ==============================================================================
def exercise_q2_site_module() -> None:
    """
    Demonstrate querying package installation directories with the `site` module.
    """
    print("\n=== Q2: The site Module & Site-Packages ===")

    # Retrieve all site-packages directories searched for third-party libraries
    site_packages = site.getsitepackages()
    assert isinstance(site_packages, list)
    assert len(site_packages) > 0

    # User-specific site directory (e.g. pip install --user)
    user_site = site.getusersitepackages()
    assert isinstance(user_site, str)

    print(f"  Primary site-packages directory: {site_packages[0]}")
    print(f"  User site directory:             {user_site}")


# ==============================================================================
# Question 3: Programmatic Venv Creation (venv.EnvBuilder)
# ==============================================================================
def exercise_q3_programmatic_venv_creation() -> None:
    """
    Demonstrate creating a virtual environment programmatically using
    the standard library `venv.EnvBuilder` (with pip installation skipped for speed).
    """
    print("\n=== Q3: Programmatic Venv Creation ===")

    import venv

    temp_dir = tempfile.mkdtemp(prefix="venv_create_")
    env_dir = os.path.join(temp_dir, "test_env")

    try:
        # Create lightweight venv without downloading pip
        builder = venv.EnvBuilder(with_pip=False, clear=True)
        builder.create(env_dir)

        # Verify key artifacts of a standard Python virtual environment:
        # 1. pyvenv.cfg configuration file
        cfg_path = os.path.join(env_dir, "pyvenv.cfg")
        assert os.path.exists(cfg_path)

        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg_content = f.read()

        assert "home = " in cfg_content

        # 2. Executable scripts directory (Scripts on Windows, bin on POSIX)
        scripts_dir = os.path.join(env_dir, "Scripts" if sys.platform == "win32" else "bin")
        assert os.path.isdir(scripts_dir)

        print(f"  Virtual environment created at: {env_dir}")
        print(f"  Found pyvenv.cfg and executable scripts directory.")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 4: Parsing requirements.txt
# ==============================================================================
class Requirement(NamedTuple):
    name: str
    operator: str | None
    version: str | None


def parse_requirements(text: str) -> list[Requirement]:
    """
    Parses a requirements.txt file, ignoring comments (#) and extracting
    package names and operator constraints (==, >=, <=, ~=, !=).
    """
    reqs: list[Requirement] = []
    pattern = re.compile(r"^([a-zA-Z0-9_\-\.]+)\s*([><!=~]=?)\s*([0-9a-zA-Z_\.\-]+)?")

    for raw_line in text.splitlines():
        line = raw_line.strip()
        # Skip empty lines and comments
        if not line or line.startswith("#"):
            continue

        match = pattern.match(line)
        if match:
            pkg_name, op, ver = match.groups()
            reqs.append(Requirement(pkg_name, op, ver))
        else:
            # Bare package without version pin
            bare_name = line.split()[0]
            reqs.append(Requirement(bare_name, None, None))

    return reqs


def exercise_q4_parse_requirements() -> None:
    """
    Test parsing diverse requirements.txt declarations.
    """
    print("\n=== Q4: Parsing requirements.txt ===")

    req_file_content = """
# Core Production Dependencies
fastapi >= 0.100.0
pydantic == 2.5.0
requests ~= 2.31.0

# Database Client
psycopg2-binary <= 2.9.9
redis
"""
    parsed = parse_requirements(req_file_content)

    assert len(parsed) == 5
    assert parsed[0] == Requirement("fastapi", ">=", "0.100.0")
    assert parsed[1] == Requirement("pydantic", "==", "2.5.0")
    assert parsed[2] == Requirement("requests", "~=", "2.31.0")
    assert parsed[3] == Requirement("psycopg2-binary", "<=", "2.9.9")
    assert parsed[4] == Requirement("redis", None, None)

    print(f"  Parsed {len(parsed)} requirements:")
    for r in parsed:
        print(f"    - {r.name} {r.operator or ''} {r.version or '(latest)'}")


# ==============================================================================
# Question 5: Semantic Version Comparison
# ==============================================================================
def parse_version_tuple(ver_str: str) -> tuple[int, ...]:
    """Converts '1.10.4' into integer tuple (1, 10, 4) for natural numeric sorting."""
    # Strip any pre-release tags like -alpha or -beta
    clean = re.sub(r"[^0-9\.]", "", ver_str.split("-")[0])
    return tuple(int(part) for part in clean.split(".") if part.isdigit())


def exercise_q5_semver_comparison() -> None:
    """
    Demonstrate version string comparison without lexicographical pitfalls
    ('1.10.0' should be greater than '1.2.0', but string sorting says otherwise).
    """
    print("\n=== Q5: Semantic Version Comparison ===")

    # In raw strings: "1.2.0" > "1.10.0" because '2' > '1'!
    assert "1.2.0" > "1.10.0"  # Flawed string comparison!

    # Correct integer tuple comparison:
    v1_2 = parse_version_tuple("1.2.0")
    v1_10 = parse_version_tuple("1.10.0")
    assert v1_10 > v1_2  # Correct: (1, 10, 0) > (1, 2, 0)

    version_list = ["2.1.0", "1.9.5", "1.10.0", "1.2.0", "3.0.0-rc1"]
    sorted_versions = sorted(version_list, key=parse_version_tuple)

    assert sorted_versions == ["1.2.0", "1.9.5", "1.10.0", "2.1.0", "3.0.0-rc1"]
    print(f"  Correctly sorted SemVer list: {sorted_versions}")


# ==============================================================================
# Question 6: Programmatic pip freeze Simulation
# ==============================================================================
def exercise_q6_pip_freeze_simulation() -> None:
    """
    Demonstrate querying installed packages in the current environment using
    `importlib.metadata.distributions()`, mimicking `pip list` or `pip freeze`.
    """
    print("\n=== Q6: Programmatic pip freeze Simulation ===")

    installed = []
    for dist in metadata.distributions():
        name = dist.metadata["Name"]
        version = dist.version
        installed.append(f"{name}=={version}")

    # The interpreter environment has installed standard packages
    assert len(installed) > 0
    sample = installed[0]
    assert "==" in sample

    print(f"  Total installed distributions found: {len(installed)}")
    print(f"  Sample installed package: '{sample}'")


# ==============================================================================
# Question 7: Package Metadata & Dependencies (Requires-Dist)
# ==============================================================================
def exercise_q7_package_metadata_inspection() -> None:
    """
    Demonstrate inspecting package headers, licenses, and declared dependencies
    using `importlib.metadata.metadata(package_name)`.
    """
    print("\n=== Q7: Package Metadata & Dependencies ===")

    # Standard distribution that is always present in standard environments
    # We inspect the first available distribution
    first_dist = next(iter(metadata.distributions()), None)
    if first_dist:
        pkg_name = first_dist.metadata["Name"]
        meta = metadata.metadata(pkg_name)

        name = meta.get("Name")
        version = meta.get("Version")
        summary = meta.get("Summary", "No summary")

        assert name == pkg_name
        assert version is not None

        print(f"  Distribution: {name} v{version}")
        print(f"  Summary:      {summary[:60]}...")
    else:
        print("  No distribution metadata available in test sandbox.")


# ==============================================================================
# Question 8: Entry Points Discovery
# ==============================================================================
def exercise_q8_entry_points_discovery() -> None:
    """
    Demonstrate discovering console_scripts entry points exposed by installed packages.
    """
    print("\n=== Q8: Entry Points Discovery ===")

    eps = metadata.entry_points()
    # Query console_scripts group
    console_scripts = [ep for ep in eps if ep.group == "console_scripts"]

    assert isinstance(console_scripts, list)
    print(f"  Discovered {len(console_scripts)} console_scripts entry points in environment.")
    if console_scripts:
        print(f"  Sample entry point: {console_scripts[0].name} -> {console_scripts[0].value}")


# ==============================================================================
# Question 9: Dependency Conflict Detection
# ==============================================================================
def detect_conflicts(pinned_dependencies: dict[str, str], requested_specs: dict[str, str]) -> list[str]:
    """
    Detects version conflicts when a package requested version does not match
    the existing pinned version.
    """
    conflicts = []
    for pkg, requested_ver in requested_specs.items():
        if pkg in pinned_dependencies:
            pinned_ver = pinned_dependencies[pkg]
            if parse_version_tuple(requested_ver) != parse_version_tuple(pinned_ver):
                conflicts.append(
                    f"Conflict for '{pkg}': requested {requested_ver}, but pinned to {pinned_ver}"
                )
    return conflicts


def exercise_q9_dependency_conflict_detection() -> None:
    """
    Demonstrate detecting dependency pin conflicts across requirements.
    """
    print("\n=== Q9: Dependency Conflict Detection ===")

    pinned = {"urllib3": "1.26.15", "requests": "2.28.1"}
    requested_valid = {"urllib3": "1.26.15"}
    requested_conflict = {"urllib3": "2.0.0"}

    assert len(detect_conflicts(pinned, requested_valid)) == 0
    conflicts = detect_conflicts(pinned, requested_conflict)
    assert len(conflicts) == 1
    assert "Conflict for 'urllib3'" in conflicts[0]

    print(f"  Clean validation: 0 conflicts.")
    print(f"  Detected conflict: {conflicts[0]}")


# ==============================================================================
# Question 10: Advanced Project - Dependency Graph & Constraint Solver
# ==============================================================================
class DependencyResolver:
    """
    Mini package dependency resolver. Traverses a dependency manifest,
    builds a directed acyclic graph (DAG), checks for cyclical dependencies,
    and resolves an installation order.
    """

    def __init__(self, registry: dict[str, list[str]]) -> None:
        # package_name -> list of dependency package_names
        self.registry = registry

    def resolve_install_order(self, target_package: str) -> list[str]:
        install_order: list[str] = []
        visited: set[str] = set()
        visiting: set[str] = set()

        def _dfs(pkg: str) -> None:
            if pkg in visiting:
                raise ValueError(f"Cyclic dependency detected involving '{pkg}'!")
            if pkg in visited:
                return

            visiting.add(pkg)
            # Resolve dependencies first (depth-first)
            for dep in self.registry.get(pkg, []):
                _dfs(dep)

            visiting.remove(pkg)
            visited.add(pkg)
            install_order.append(pkg)

        _dfs(target_package)
        return install_order


def exercise_q10_dependency_resolver() -> None:
    """
    Verify DependencyResolver calculates clean topological install order and catches cycles.
    """
    print("\n=== Q10: Dependency Graph & Constraint Solver ===")

    # Registry dependency graph:
    # webapp -> [fastapi, sqlalchemy]
    # fastapi -> [pydantic]
    # sqlalchemy -> []
    # pydantic -> []
    registry = {
        "webapp": ["fastapi", "sqlalchemy"],
        "fastapi": ["pydantic"],
        "sqlalchemy": [],
        "pydantic": [],
    }

    resolver = DependencyResolver(registry)
    install_order = resolver.resolve_install_order("webapp")

    # Dependencies must appear BEFORE the dependent package
    assert install_order.index("pydantic") < install_order.index("fastapi")
    assert install_order.index("fastapi") < install_order.index("webapp")
    assert install_order.index("sqlalchemy") < install_order.index("webapp")
    assert install_order[-1] == "webapp"

    # Test cyclic dependency detection: A -> B -> A
    cyclic_registry = {
        "pkg_a": ["pkg_b"],
        "pkg_b": ["pkg_a"],
    }
    cyclic_resolver = DependencyResolver(cyclic_registry)
    caught_cycle = False
    try:
        cyclic_resolver.resolve_install_order("pkg_a")
    except ValueError as exc:
        caught_cycle = True
        assert "Cyclic dependency detected" in str(exc)

    assert caught_cycle is True

    print(f"  Calculated topological installation order: {install_order}")
    print("  Cyclic dependency successfully trapped and reported.")


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_venv_anatomy()
    exercise_q2_site_module()
    exercise_q3_programmatic_venv_creation()
    exercise_q4_parse_requirements()
    exercise_q5_semver_comparison()
    exercise_q6_pip_freeze_simulation()
    exercise_q7_package_metadata_inspection()
    exercise_q8_entry_points_discovery()
    exercise_q9_dependency_conflict_detection()
    exercise_q10_dependency_resolver()

    print("\nAll 10 virtual environments and pip questions executed and asserted successfully!")
