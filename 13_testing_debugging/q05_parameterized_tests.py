"""
Topic 13: Testing and Debugging
Question 05: Parameterized Tests

A comprehensive, production-grade guide to data-driven and parameterized testing in Python.
Covers self.subTest loops, dynamic test method generation with setattr, custom @parameterized
decorators, metaclass-based test generators, Cartesian product permutations with itertools,
JSON/CSV data-driven suites, Boundary Value Analysis (BVA) tables, exception parameterization,
subtest diagnostic tags, and an architectural Go-style Table-Driven Test Runner.

Every question contains standalone runnable exercises verified with 100% assertions.
"""

import unittest
import io
import json
import itertools
from dataclasses import dataclass
from typing import List, Dict, Any, Callable, Optional, Tuple, Type


# =====================================================================
# Q1: Basic self.subTest Parameterized Loop
# =====================================================================
def is_palindrome(text: str) -> bool:
    cleaned = "".join(ch.lower() for ch in text if ch.isalnum())
    return cleaned == cleaned[::-1]


class SubTestLoopTestCase(unittest.TestCase):
    def test_palindromes(self):
        test_cases = [
            ("radar", True),
            ("RaceCar", True),
            ("A man, a plan, a canal: Panama", True),
            ("hello", False),
            ("python", False),
            ("", True),
        ]
        for candidate, expected in test_cases:
            with self.subTest(candidate=candidate, expected=expected):
                self.assertEqual(is_palindrome(candidate), expected)


def q1_subtest_parameterized_loop():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(SubTestLoopTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 1

    print("=== Q1: Basic self.subTest Parameterized Loop Verified ===")


# =====================================================================
# Q2: Dynamic Test Method Generation with setattr
# =====================================================================
class DynamicGeneratedTestCase(unittest.TestCase):
    pass


def generate_arithmetic_tests():
    """Generates distinct test_<name> methods programmatically on DynamicGeneratedTestCase."""
    cases = [
        ("add_positive", 10, 5, 15),
        ("add_zeros", 0, 0, 0),
        ("add_negatives", -4, -6, -10),
        ("add_mixed", 20, -5, 15),
    ]

    for name, a, b, expected in cases:
        def test_method(self, val_a=a, val_b=b, exp=expected):
            self.assertEqual(val_a + val_b, exp)

        test_method.__name__ = f"test_{name}"
        setattr(DynamicGeneratedTestCase, f"test_{name}", test_method)


def q2_dynamic_test_generation():
    generate_arithmetic_tests()

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DynamicGeneratedTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 4

    print("=== Q2: Dynamic Test Method Generation with setattr Verified ===")


# =====================================================================
# Q3: Custom @parameterized Method Decorator
# =====================================================================
def parameterized_dataset(dataset: List[Tuple[Any, ...]]):
    """
    Custom decorator that automatically executes a test function
    over all rows in dataset using self.subTest.
    """
    def decorator(fn: Callable):
        def wrapper(self, *args, **kwargs):
            for row in dataset:
                with self.subTest(row=row):
                    fn(self, *row)
        return wrapper
    return decorator


class CustomDecoratorTestCase(unittest.TestCase):
    @parameterized_dataset([
        (2, 4),
        (3, 9),
        (4, 16),
        (5, 25),
        (-6, 36)
    ])
    def test_square(self, base, expected_sq):
        self.assertEqual(base * base, expected_sq)


def q3_custom_parameterized_decorator():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CustomDecoratorTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 1

    print("=== Q3: Custom @parameterized Decorator Verified ===")


# =====================================================================
# Q4: Metaclass-Based Parameterized Test Generation
# =====================================================================
class ParameterizedMeta(type(unittest.TestCase)):
    """
    Metaclass that inspects attributes with `_parameter_matrix` and
    expands them into separate standalone test methods.
    """
    def __new__(mcs, name, bases, attrs):
        new_attrs = {}
        for attr_name, attr_val in attrs.items():
            if hasattr(attr_val, "_parameter_matrix"):
                matrix = getattr(attr_val, "_parameter_matrix")
                for idx, params in enumerate(matrix):
                    method_name = f"{attr_name}_{idx}_{params[0]}"
                    # Capture parameters using default arguments
                    def make_test(fn, p):
                        return lambda self: fn(self, *p)

                    new_attrs[method_name] = make_test(attr_val, params)
            else:
                new_attrs[attr_name] = attr_val
        return super().__new__(mcs, name, bases, new_attrs)


def matrix(*cases):
    def decorator(fn):
        fn._parameter_matrix = cases
        return fn
    return decorator


class MetaclassTestCase(unittest.TestCase, metaclass=ParameterizedMeta):
    @matrix(
        ("lower", "python", "PYTHON"),
        ("mixed", "PyThOn", "PYTHON"),
        ("upper", "PYTHON", "PYTHON"),
    )
    def test_uppercase(self, label, input_str, expected):
        self.assertEqual(input_str.upper(), expected)


def q4_metaclass_parameterized_tests():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(MetaclassTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    # 3 tests expanded by the metaclass
    assert result.testsRun == 3

    print("=== Q4: Metaclass-Based Test Expansion Verified ===")


# =====================================================================
# Q5: Cartesian Product Combinatorial Parameterization
# =====================================================================
def can_access_endpoint(role: str, action: str, env: str) -> bool:
    """Security rule: only admin can delete in production; others denied."""
    if env == "production" and action == "delete":
        return role == "admin"
    return True


class CombinatorialTestCase(unittest.TestCase):
    def test_all_permission_combinations(self):
        roles = ["guest", "user", "admin"]
        actions = ["read", "write", "delete"]
        environments = ["staging", "production"]

        # 3 * 3 * 2 = 18 combinations tested via Cartesian product
        combinations = list(itertools.product(roles, actions, environments))
        assert len(combinations) == 18

        for role, action, env in combinations:
            with self.subTest(role=role, action=action, env=env):
                allowed = can_access_endpoint(role, action, env)
                if env == "production" and action == "delete":
                    expected = (role == "admin")
                else:
                    expected = True
                self.assertEqual(allowed, expected)


def q5_combinatorial_parameterization():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CombinatorialTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 1

    print("=== Q5: Cartesian Product Permutations Verified ===")


# =====================================================================
# Q6: External Data-Driven Test Suites (JSON Fixture)
# =====================================================================
JSON_FIXTURE_DATA = """
[
    {"email": "valid@example.com", "expected_valid": true},
    {"email": "alice.smith@corp.org", "expected_valid": true},
    {"email": "invalid_email_no_at", "expected_valid": false},
    {"email": "bad@domain", "expected_valid": false}
]
"""


def validate_email_simple(email: str) -> bool:
    return "@" in email and "." in email.split("@")[-1]


class DataDrivenJSONTestCase(unittest.TestCase):
    def test_email_validation_from_json(self):
        records = json.loads(JSON_FIXTURE_DATA)
        for rec in records:
            with self.subTest(email=rec["email"]):
                self.assertEqual(validate_email_simple(rec["email"]), rec["expected_valid"])


def q6_external_data_driven_json():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DataDrivenJSONTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 1

    print("=== Q6: External Data-Driven (JSON) Testing Verified ===")


# =====================================================================
# Q7: Boundary Value Analysis (BVA) Parameterization
# =====================================================================
def calculate_discount_tier(order_total: float) -> float:
    """
    Tiered discount rules:
    - order < 50.0   -> 0.0%
    - 50.0 <= order < 100.0 -> 5.0%
    - 100.0 <= order <= 500.0 -> 10.0%
    """
    if order_total < 50.0:
        return 0.0
    elif order_total < 100.0:
        return 0.05
    elif order_total <= 500.0:
        return 0.10
    return 0.15


class BoundaryValueAnalysisTestCase(unittest.TestCase):
    def test_bva_discount_thresholds(self):
        # Systematic testing of nominal and boundary points
        bva_cases = [
            # Case, OrderTotal, ExpectedDiscount
            ("just_below_first_tier", 49.99, 0.0),
            ("exact_first_tier_boundary", 50.00, 0.05),
            ("inside_first_tier", 75.00, 0.05),
            ("just_below_second_tier", 99.99, 0.05),
            ("exact_second_tier_boundary", 100.00, 0.10),
            ("inside_second_tier", 250.00, 0.10),
            ("exact_top_tier_boundary", 500.00, 0.10),
            ("above_top_tier", 500.01, 0.15),
        ]

        for label, total, expected_discount in bva_cases:
            with self.subTest(boundary=label, order_total=total):
                actual = calculate_discount_tier(total)
                self.assertEqual(actual, expected_discount)


def q7_boundary_value_analysis():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BoundaryValueAnalysisTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 1

    print("=== Q7: Boundary Value Analysis (BVA) Verified ===")


# =====================================================================
# Q8: SubTest with Rich Contextual Diagnostic Labels
# =====================================================================
class ContextualSubTestTestCase(unittest.TestCase):
    def test_matrix_with_diagnostics(self):
        matrix_data = [
            {"row": 1, "col": 1, "matrix_name": "GridA", "val": 10},
            {"row": 1, "col": 2, "matrix_name": "GridA", "val": 20},
            {"row": 2, "col": 1, "matrix_name": "GridB", "val": 30},
        ]
        for item in matrix_data:
            # Injecting multiple contextual kwargs into subTest
            with self.subTest(grid=item["matrix_name"], r=item["row"], c=item["col"]):
                self.assertGreater(item["val"], 0)


def q8_contextual_subtest_labels():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ContextualSubTestTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 1

    print("=== Q8: SubTest with Rich Contextual Labels Verified ===")


# =====================================================================
# Q9: Expected Exception Parameterization
# =====================================================================
def parse_age(age_str: str) -> int:
    val = int(age_str)
    if val < 0 or val > 150:
        raise ValueError(f"Age out of bounds: {val}")
    return val


class ExceptionParameterizedTestCase(unittest.TestCase):
    def test_age_parser_outcomes(self):
        # Tuple: (input_str, expected_result, expected_exception_type)
        cases = [
            ("25", 25, None),
            ("0", 0, None),
            ("150", 150, None),
            ("-1", None, ValueError),
            ("200", None, ValueError),
            ("not-a-number", None, ValueError),
        ]

        for raw_val, expected_out, expected_err in cases:
            with self.subTest(input=raw_val):
                if expected_err is not None:
                    with self.assertRaises(expected_err):
                        parse_age(raw_val)
                else:
                    self.assertEqual(parse_age(raw_val), expected_out)


def q9_exception_parameterization():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ExceptionParameterizedTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 1

    print("=== Q9: Expected Exception Parameterization Verified ===")


# =====================================================================
# Q10: Architectural Go-Style Table-Driven Test Framework
# =====================================================================
@dataclass
class TableTestCase:
    name: str
    input_data: Any
    expected_output: Any = None
    expected_exception: Optional[Type[BaseException]] = None


class TableDrivenRunner:
    """
    Executes Go-style Table-Driven Tests with clean diagnostic failure isolation.
    """
    @classmethod
    def run_tests(
        cls,
        test_case_instance: unittest.TestCase,
        target_fn: Callable,
        cases: List[TableTestCase]
    ):
        for tc in cases:
            with test_case_instance.subTest(test_name=tc.name):
                if tc.expected_exception:
                    with test_case_instance.assertRaises(tc.expected_exception):
                        target_fn(tc.input_data)
                else:
                    result = target_fn(tc.input_data)
                    test_case_instance.assertEqual(result, tc.expected_output)


def normalize_slug(text: str) -> str:
    """Converts string to url-friendly slug."""
    import re
    if not isinstance(text, str):
        raise TypeError("Slug input must be a string")
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    slug = re.sub(r"[\s_-]+", "-", text).strip("-")
    if not slug:
        raise ValueError("Slug cannot be empty")
    return slug


class SlugTableDrivenTestCase(unittest.TestCase):
    def test_slug_generation(self):
        test_table = [
            TableTestCase(name="simple_words", input_data="Hello World", expected_output="hello-world"),
            TableTestCase(name="with_special_chars", input_data="Python 3.12 & AI!", expected_output="python-312-ai"),
            TableTestCase(name="consecutive_hyphens", input_data="foo --- bar", expected_output="foo-bar"),
            TableTestCase(name="leading_trailing_spaces", input_data="  spaced out  ", expected_output="spaced-out"),
            TableTestCase(name="empty_string_error", input_data="   ", expected_exception=ValueError),
            TableTestCase(name="non_string_type_error", input_data=12345, expected_exception=TypeError),
        ]
        TableDrivenRunner.run_tests(self, normalize_slug, test_table)


def q10_architectural_table_driven_framework():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(SlugTableDrivenTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 1

    print("=== Q10: Architectural Go-Style Table-Driven Test Framework Verified ===")


# =====================================================================
# Main Test Runner
# =====================================================================
if __name__ == "__main__":
    q1_subtest_parameterized_loop()
    q2_dynamic_test_generation()
    q3_custom_parameterized_decorator()
    q4_metaclass_parameterized_tests()
    q5_combinatorial_parameterization()
    q6_external_data_driven_json()
    q7_boundary_value_analysis()
    q8_contextual_subtest_labels()
    q9_exception_parameterization()
    q10_architectural_table_driven_framework()

    print("\nAll 10 parameterized tests practice questions passed successfully!")
