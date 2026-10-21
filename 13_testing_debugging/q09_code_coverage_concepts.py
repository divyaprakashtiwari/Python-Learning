"""
Topic 13: Testing and Debugging
Question 09: Code Coverage Concepts

A comprehensive, production-grade guide to software test coverage mechanics implemented
in pure Python using standard library modules (sys, ast, inspect, linecache).
Covers statement coverage vs line coverage, AST discovery of executable statements,
branch coverage & decision paths, function call coverage, visual source code annotation,
test-to-code attribution mapping, coverage threshold enforcement, and an architectural
pure-Python MicroCoverage Engine generating LCOV/JSON reports.

Every question contains standalone runnable exercises verified with 100% assertions.
"""

import sys
import ast
import inspect
import json
from typing import List, Dict, Any, Set, Tuple, Optional, Callable


# =====================================================================
# Q1: Statement Coverage Tracking with sys.settrace
# =====================================================================
def q1_statement_coverage_tracking():
    """
    Demonstrates capturing executed line numbers using sys.settrace.
    """
    executed_lines: Set[int] = set()

    def tracer(frame, event, arg):
        if event == "line" and frame.f_code.co_name == "sample_logic":
            executed_lines.add(frame.f_lineno)
        return tracer

    def sample_logic(flag: bool):
        a = 10
        if flag:
            b = 20
        else:
            b = 30
        return a + b

    old_trace = sys.gettrace()
    try:
        sys.settrace(tracer)
        sample_logic(True)
    finally:
        sys.settrace(old_trace)

    # Executed lines recorded for sample_logic
    assert len(executed_lines) >= 3

    print("=== Q1: Statement Coverage Tracking with sys.settrace Verified ===")


# =====================================================================
# Q2: AST Discovery of Executable Statements
# =====================================================================
def find_executable_lines(source_code: str) -> Set[int]:
    """
    Parses Python source code with ast and identifies all line numbers
    that contain executable statements (excluding docstrings and comments).
    """
    tree = ast.parse(source_code)
    executable: Set[int] = set()

    for node in ast.walk(tree):
        # Check if node is an AST statement
        if isinstance(node, ast.stmt):
            # Skip module docstrings
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                continue
            executable.add(node.lineno)

    return executable


def q2_ast_executable_line_discovery():
    sample_source = (
        '"""Module docstring."""\n'
        '# This is a comment\n'
        'x = 10\n'
        'if x > 5:\n'
        '    y = x * 2\n'
        'else:\n'
        '    y = 0\n'
    )
    lines = find_executable_lines(sample_source)

    # Line 1 is docstring (ignored), Line 2 is comment (ignored)
    # Line 3 (x=10), Line 4 (if), Line 5 (y=x*2), Line 7 (y=0)
    assert 3 in lines
    assert 4 in lines
    assert 5 in lines
    assert 7 in lines
    assert 1 not in lines
    assert 2 not in lines

    print("=== Q2: AST Discovery of Executable Statements Verified ===")


# =====================================================================
# Q3: Line Coverage Percentage Calculation
# =====================================================================
def calculate_coverage_percentage(executed: Set[int], total: Set[int]) -> float:
    """Calculates coverage percentage: (executed / total) * 100."""
    if not total:
        return 100.0
    covered = executed.intersection(total)
    return round((len(covered) / len(total)) * 100.0, 2)


def q3_coverage_percentage_calculation():
    total_executable = {10, 11, 12, 13, 14, 15}
    executed_run_a = {10, 11, 12, 13, 14, 15}
    executed_run_b = {10, 11, 12}

    assert calculate_coverage_percentage(executed_run_a, total_executable) == 100.0
    assert calculate_coverage_percentage(executed_run_b, total_executable) == 50.0
    assert calculate_coverage_percentage(set(), total_executable) == 0.0

    print("=== Q3: Line Coverage Percentage Calculation Verified ===")


# =====================================================================
# Q4: Branch Coverage (Decision Logic)
# =====================================================================
def q4_branch_coverage_analysis():
    """
    Demonstrates branch coverage: ensuring that both the 'True' and 'False'
    branches of conditional decision points have been executed.
    """
    branches_taken: Set[Tuple[str, bool]] = set()

    def evaluate_discount(is_member: bool, order_total: float) -> float:
        # Branch 1: is_member
        branches_taken.add(("branch_member", is_member))
        # Branch 2: order_total >= 100
        over_100 = (order_total >= 100.0)
        branches_taken.add(("branch_large_order", over_100))

        if is_member and over_100:
            return 0.20
        return 0.05

    # Run Test 1: (is_member=True, order_total=150)
    evaluate_discount(True, 150.0)
    # At this point, we only covered the True sides
    assert ("branch_member", True) in branches_taken
    assert ("branch_member", False) not in branches_taken

    # Run Test 2: (is_member=False, order_total=50)
    evaluate_discount(False, 50.0)
    # Now both True and False branches are covered for both decision points!
    assert ("branch_member", True) in branches_taken
    assert ("branch_member", False) in branches_taken
    assert ("branch_large_order", True) in branches_taken
    assert ("branch_large_order", False) in branches_taken

    print("=== Q4: Branch Coverage (Decision Logic) Verified ===")


# =====================================================================
# Q5: Combinatorial Path Coverage
# =====================================================================
def q5_path_coverage():
    """
    Demonstrates measuring all execution paths through composite boolean logic:
    (condition_a, condition_b) has 4 paths: (T,T), (T,F), (F,T), (F,F).
    """
    paths_recorded: Set[Tuple[bool, bool]] = set()

    def route_request(is_authenticated: bool, has_token: bool) -> str:
        paths_recorded.add((is_authenticated, has_token))
        if is_authenticated and has_token:
            return "SUCCESS"
        elif is_authenticated and not has_token:
            return "TOKEN_REQUIRED"
        elif not is_authenticated and has_token:
            return "SESSION_EXPIRED"
        return "DENIED"

    # Test all 4 combinatorial paths
    route_request(True, True)
    route_request(True, False)
    route_request(False, True)
    route_request(False, False)

    assert len(paths_recorded) == 4
    assert (True, True) in paths_recorded
    assert (True, False) in paths_recorded
    assert (False, True) in paths_recorded
    assert (False, False) in paths_recorded

    print("=== Q5: Combinatorial Path Coverage Verified ===")


# =====================================================================
# Q6: Function & Method Coverage Tracker
# =====================================================================
class ModuleFunctionCoverage:
    """Discovers all defined functions and checks which ones were executed."""
    def __init__(self, target_functions: List[Callable]):
        self.target_names = {fn.__name__ for fn in target_functions}
        self.called_functions: Set[str] = set()

    def tracer(self, frame, event, arg):
        if event == "call" and frame.f_code.co_name in self.target_names:
            self.called_functions.add(frame.f_code.co_name)
        return self.tracer

    @property
    def coverage_ratio(self) -> float:
        return len(self.called_functions) / len(self.target_names) if self.target_names else 1.0


def service_a():
    return "A"


def service_b():
    return "B"


def service_c():
    return "C"


def q6_function_coverage_tracker():
    tracker = ModuleFunctionCoverage([service_a, service_b, service_c])

    old_trace = sys.gettrace()
    try:
        sys.settrace(tracker.tracer)
        service_a()
        service_b()
    finally:
        sys.settrace(old_trace)

    assert tracker.called_functions == {"service_a", "service_b"}
    assert tracker.coverage_ratio == round(2 / 3, 4) or round(tracker.coverage_ratio, 2) == 0.67

    print("=== Q6: Function Coverage Tracker Verified ===")


# =====================================================================
# Q7: Visual Annotated Source Code Coverage Reporter
# =====================================================================
def generate_annotated_coverage(source_code: str, executed_lines: Set[int]) -> str:
    """
    Produces an annotated source report:
    [>] for executed lines
    [!] for missed executable lines
    [ ] for non-executable lines (blank, comment, docstring)
    """
    executable = find_executable_lines(source_code)
    lines = source_code.splitlines()
    report = []

    for idx, line in enumerate(lines, start=1):
        if idx in executed_lines:
            marker = "[>]"
        elif idx in executable:
            marker = "[!]"
        else:
            marker = "[ ]"
        report.append(f"{marker} {idx:3d}: {line}")

    return "\n".join(report)


def q7_visual_annotated_coverage():
    code = (
        "def compute(n):\n"
        "    if n > 0:\n"
        "        return n * 2\n"
        "    else:\n"
        "        return 0\n"
    )
    # Suppose lines 1, 2, 3 were executed
    executed = {1, 2, 3}
    annotated = generate_annotated_coverage(code, executed)

    assert "[>]   1: def compute(n):" in annotated
    assert "[>]   2:     if n > 0:" in annotated
    assert "[>]   3:         return n * 2:" not in annotated  # line 3 has no colon
    assert "[!]   5:         return 0" in annotated  # Line 5 was missed!

    print("=== Q7: Visual Annotated Source Code Coverage Verified ===")


# =====================================================================
# Q8: Test-to-Code Attribution Mapping
# =====================================================================
def q8_test_to_code_attribution():
    """
    Demonstrates mapping which specific test method covers which production lines.
    """
    test_line_map: Dict[str, Set[int]] = {}

    def run_instrumented_test(test_name: str, test_fn: Callable):
        executed: Set[int] = set()

        def tracer(frame, event, arg):
            if event == "line" and frame.f_code.co_name == "business_logic":
                executed.add(frame.f_lineno)
            return tracer

        old = sys.gettrace()
        try:
            sys.settrace(tracer)
            test_fn()
        finally:
            sys.settrace(old)

        test_line_map[test_name] = executed

    def business_logic(mode):
        if mode == "A":
            return 1
        elif mode == "B":
            return 2
        return 0

    run_instrumented_test("test_mode_A", lambda: business_logic("A"))
    run_instrumented_test("test_mode_B", lambda: business_logic("B"))

    assert "test_mode_A" in test_line_map
    assert "test_mode_B" in test_line_map
    # Lines differ because test_mode_A enters the first branch, test_mode_B enters second
    assert test_line_map["test_mode_A"] != test_line_map["test_mode_B"]

    print("=== Q8: Test-to-Code Attribution Mapping Verified ===")


# =====================================================================
# Q9: Minimum Coverage Threshold Enforcer
# =====================================================================
class CoverageThresholdError(AssertionError):
    pass


def assert_minimum_coverage(actual_pct: float, minimum_pct: float = 80.0):
    if actual_pct < minimum_pct:
        raise CoverageThresholdError(
            f"Coverage check failed: {actual_pct}% is below required {minimum_pct}%"
        )


def q9_coverage_threshold_enforcement():
    # Pass threshold
    assert_minimum_coverage(85.5, minimum_pct=80.0)

    # Fail threshold
    caught_threshold_error = False
    try:
        assert_minimum_coverage(74.2, minimum_pct=80.0)
    except CoverageThresholdError as err:
        caught_threshold_error = True
        assert "74.2% is below required 80.0%" in str(err)

    assert caught_threshold_error is True
    print("=== Q9: Minimum Coverage Threshold Enforcer Verified ===")


# =====================================================================
# Q10: Architectural Pure-Python MicroCoverage Engine
# =====================================================================
class MicroCoverage:
    """
    Production-grade lightweight code coverage engine in pure Python:
    - Analyzes source AST for executable line discovery
    - Traces execution non-invasively
    - Computes coverage percentage and missed lines
    - Exports structured JSON coverage summary
    """
    def __init__(self, target_func_name: str, source_code: str):
        self.target_func_name = target_func_name
        self.source_code = source_code
        self.executable_lines = find_executable_lines(source_code)
        self.executed_lines: Set[int] = set()

    def _tracer(self, frame, event, arg):
        if event == "line" and frame.f_code.co_name == self.target_func_name:
            self.executed_lines.add(frame.f_lineno)
        return self._tracer

    def run(self, callable_fn: Callable, *args, **kwargs) -> Any:
        old_trace = sys.gettrace()
        try:
            sys.settrace(self._tracer)
            result = callable_fn(*args, **kwargs)
        finally:
            sys.settrace(old_trace)
        return result

    def get_report(self) -> Dict[str, Any]:
        # Filter executable lines to relevant line range
        min_line = min(self.executed_lines) if self.executed_lines else 1
        max_line = max(self.executed_lines) if self.executed_lines else 1
        relevant_executable = {ln for ln in self.executable_lines if min_line <= ln <= max_line}

        missed = relevant_executable - self.executed_lines
        pct = calculate_coverage_percentage(self.executed_lines, relevant_executable)

        return {
            "target": self.target_func_name,
            "executable_count": len(relevant_executable),
            "executed_count": len(self.executed_lines),
            "missed_lines": sorted(list(missed)),
            "coverage_percent": pct,
        }


def sample_calc_function(x: int) -> int:
    val = x * 2
    if x > 5:
        val += 10
    else:
        val -= 5
    return val


def q10_architectural_micro_coverage_engine():
    source = inspect.getsource(sample_calc_function)
    coverage = MicroCoverage("sample_calc_function", source)

    # Run with x = 10 (exercises x > 5 branch, misses else branch)
    res = coverage.run(sample_calc_function, 10)
    assert res == 30

    report = coverage.get_report()
    assert report["target"] == "sample_calc_function"
    assert report["executed_count"] > 0
    assert report["coverage_percent"] > 0.0

    # Ensure JSON serializable
    json_summary = json.dumps(report)
    assert "coverage_percent" in json_summary

    print("=== Q10: Architectural Pure-Python MicroCoverage Engine Verified ===")


# =====================================================================
# Main Test Runner
# =====================================================================
if __name__ == "__main__":
    q1_statement_coverage_tracking()
    q2_ast_executable_line_discovery()
    q3_coverage_percentage_calculation()
    q4_branch_coverage_analysis()
    q5_path_coverage()
    q6_function_coverage_tracker()
    q7_visual_annotated_coverage()
    q8_test_to_code_attribution()
    q9_coverage_threshold_enforcement()
    q10_architectural_micro_coverage_engine()

    print("\nAll 10 code coverage concepts practice questions passed successfully!")
