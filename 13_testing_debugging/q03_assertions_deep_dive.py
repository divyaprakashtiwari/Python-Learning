"""
Topic 13: Testing and Debugging
Question 03: Assertions Deep Dive

A comprehensive, production-grade guide to assertion mechanics in Python testing.
Covers inequality comparisons, multiline string diffs & regex assertions, sequence/set/tuple
comparisons, dictionary deep assertions, warning assertions (assertWarns & assertWarnsRegex),
custom domain assertion methods, maxDiff & longMessage formatting, built-in assert statements
vs unittest assertions, and an architectural Fluent Assertion Engine.

Every question contains standalone runnable exercises verified with 100% assertions.
"""

import unittest
import io
import re
import warnings
from typing import List, Dict, Any, Optional


# =====================================================================
# Q1: Numerical Boundary and Inequality Assertions
# =====================================================================
class BoundaryInequalityTestCase(unittest.TestCase):
    def test_inequalities(self):
        score = 85.5
        passing_threshold = 70.0
        max_possible = 100.0

        self.assertGreater(score, passing_threshold)
        self.assertGreaterEqual(score, 85.5)
        self.assertLess(score, max_possible)
        self.assertLessEqual(score, 85.5)

        # Boundary checks
        self.assertGreaterEqual(passing_threshold, 70.0)
        self.assertLessEqual(passing_threshold, 70.0)


def q1_numerical_boundary_assertions():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BoundaryInequalityTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 1

    print("=== Q1: Numerical Boundary & Inequality Assertions Verified ===")


# =====================================================================
# Q2: Multiline String Diffs and Regex Pattern Assertions
# =====================================================================
class StringPatternTestCase(unittest.TestCase):
    def test_multiline_equal(self):
        expected_log = "INFO: System started\nDEBUG: Connected to DB\nINFO: Ready"
        actual_log = "INFO: System started\nDEBUG: Connected to DB\nINFO: Ready"
        # Shows unified diff on mismatch
        self.assertMultiLineEqual(actual_log, expected_log)

    def test_regex_matching(self):
        uuid_sample = "c493b254-66c0-42c3-8a9d-4d159baebce5"
        uuid_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
        self.assertRegex(uuid_sample, uuid_pattern)

        # Negative regex assertion
        self.assertNotRegex(uuid_sample, r"^[0-9]+$")


def q2_string_diffs_and_regex_assertions():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(StringPatternTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 2

    print("=== Q2: Multiline String Diffs & Regex Assertions Verified ===")


# =====================================================================
# Q3: Sequence, Set, and Tuple Assertions
# =====================================================================
class SequenceSetTupleTestCase(unittest.TestCase):
    def test_tuples_and_sequences(self):
        point1 = (10, 20, 30)
        point2 = (10, 20, 30)
        self.assertTupleEqual(point1, point2)

        # Sequence equal works across list/tuple/ranges if values match
        self.assertSequenceEqual([1, 2, 3], (1, 2, 3))

    def test_sets(self):
        set_a = {"admin", "editor", "viewer"}
        set_b = {"viewer", "editor", "admin"}
        self.assertSetEqual(set_a, set_b)


def q3_sequence_set_tuple_assertions():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(SequenceSetTupleTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 2

    print("=== Q3: Sequence, Set, and Tuple Assertions Verified ===")


# =====================================================================
# Q4: Dictionary Deep Assertions & Sub-Dictionary Checks
# =====================================================================
class DictionaryAssertionsTestCase(unittest.TestCase):
    def assertDictSubset(self, subset: Dict[str, Any], full_dict: Dict[str, Any]):
        """Helper assertion verifying all key-values in subset exist in full_dict."""
        for k, v in subset.items():
            self.assertIn(k, full_dict, f"Expected key '{k}' missing from full dict")
            self.assertEqual(full_dict[k], v, f"Value mismatch for key '{k}'")

    def test_dict_equality(self):
        dict_a = {"user": "Alice", "meta": {"role": "admin", "active": True}}
        dict_b = {"meta": {"active": True, "role": "admin"}, "user": "Alice"}
        self.assertDictEqual(dict_a, dict_b)

    def test_sub_dictionary(self):
        response_payload = {
            "status": "success",
            "code": 200,
            "data": [1, 2, 3],
            "timestamp": 1729500000
        }
        expected_subset = {"status": "success", "code": 200}
        self.assertDictSubset(expected_subset, response_payload)


def q4_dictionary_assertions():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DictionaryAssertionsTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 2

    print("=== Q4: Dictionary Assertions & Sub-Dict Checks Verified ===")


# =====================================================================
# Q5: Warning Assertions: assertWarns and assertWarnsRegex
# =====================================================================
def legacy_feature(flag: bool):
    if flag:
        warnings.warn("legacy_feature is deprecated; use modern_feature()", DeprecationWarning, stacklevel=2)
    return "executed"


class WarningAssertionsTestCase(unittest.TestCase):
    def test_warning_captured(self):
        with self.assertWarns(DeprecationWarning) as cm:
            result = legacy_feature(True)

        self.assertEqual(result, "executed")
        self.assertEqual(len(cm.warnings), 1)
        self.assertTrue(issubclass(cm.warnings[0].category, DeprecationWarning))

    def test_warning_regex(self):
        with self.assertWarnsRegex(DeprecationWarning, r"use modern_feature\(\)"):
            legacy_feature(True)


def q5_warning_assertions():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(WarningAssertionsTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 2

    print("=== Q5: Warning Assertions (assertWarns & assertWarnsRegex) Verified ===")


# =====================================================================
# Q6: Custom Reusable Domain Assertions
# =====================================================================
class DomainAssertionsMixin:
    """Provides specialized domain assertions for API responses and business entities."""
    def assertValidUUID4(self, val: str, msg: Optional[str] = None):
        pattern = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$", re.I)
        if not (isinstance(val, str) and pattern.match(val)):
            err = msg or f"'{val}' is not a valid RFC 4122 UUIDv4"
            raise AssertionError(err)

    def assertHTTPStatus(self, response: Dict[str, Any], expected_code: int):
        actual = response.get("status_code")
        if actual != expected_code:
            raise AssertionError(f"Expected HTTP {expected_code}, got {actual}. Body: {response.get('body')}")


class CustomDomainTestCase(DomainAssertionsMixin, unittest.TestCase):
    def test_custom_assertions(self):
        test_uuid = "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
        self.assertValidUUID4(test_uuid)

        mock_resp = {"status_code": 200, "body": '{"ok": true}'}
        self.assertHTTPStatus(mock_resp, 200)


def q6_custom_domain_assertions():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CustomDomainTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 1

    print("=== Q6: Custom Domain Assertions Verified ===")


# =====================================================================
# Q7: maxDiff and Failure Message Customization
# =====================================================================
class DiffFormattingTestCase(unittest.TestCase):
    # Setting maxDiff = None ensures full data diffs are never truncated with '...'
    maxDiff = None
    longMessage = True

    def test_custom_message(self):
        # Assertions support optional custom failure messages appended to standard output
        expected = [1, 2, 3]
        actual = [1, 2, 3]
        self.assertEqual(actual, expected, "Vectors must match exactly in size and values")


def q7_maxdiff_and_message_customization():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DiffFormattingTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 1

    print("=== Q7: maxDiff & Custom Message Formatting Verified ===")


# =====================================================================
# Q8: Built-in assert Statement vs unittest Assertions
# =====================================================================
def q8_builtin_assert_mechanics():
    """
    Demonstrates mechanics of Python's native `assert expression, message`:
    - Raises AssertionError if expression evaluates to false
    - Difference: assert statements can be disabled at runtime when Python is run
      with optimization flags (-O or -OO), which sets `__debug__ = False`!
      Therefore, NEVER use `assert` for security checks, permissions, or user input validation.
    """
    assert __debug__ is True

    # 1. Successful assert
    x = 100
    assert x > 50, "x should be greater than 50"

    # 2. Failed assert raises AssertionError
    caught_assertion = False
    try:
        assert x < 50, "Expected x < 50"
    except AssertionError as e:
        caught_assertion = True
        assert "Expected x < 50" in str(e)

    assert caught_assertion is True
    print("=== Q8: Built-in assert Statement Mechanics Verified ===")


# =====================================================================
# Q9: Multi-Exception and Type Hierarchy Assertions
# =====================================================================
class HierarchyTestCase(unittest.TestCase):
    def test_multiple_expected_exceptions(self):
        # assertRaises can take a tuple of acceptable exception classes
        with self.assertRaises((KeyError, IndexError)):
            data = {"key_a": 1}
            _ = data["missing_key"]

        with self.assertRaises((KeyError, IndexError)):
            items = [10, 20]
            _ = items[99]


def q9_multi_exception_assertions():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(HierarchyTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 1

    print("=== Q9: Multi-Exception Hierarchy Assertions Verified ===")


# =====================================================================
# Q10: Architectural Fluent Assertion Engine
# =====================================================================
class FluentAssertion:
    """
    Fluent assertion builder providing readable, chainable assertion syntax:
    assertThat(val).is_not_none().is_type(int).is_greater_than(10).is_between(10, 100)
    """
    def __init__(self, target: Any, name: str = "value"):
        self.target = target
        self.name = name

    def is_equal_to(self, expected: Any) -> "FluentAssertion":
        if self.target != expected:
            raise AssertionError(f"Expected {self.name} to equal {expected!r}, but got {self.target!r}")
        return self

    def is_not_none(self) -> "FluentAssertion":
        if self.target is None:
            raise AssertionError(f"Expected {self.name} to not be None")
        return self

    def is_type(self, expected_type: type) -> "FluentAssertion":
        if not isinstance(self.target, expected_type):
            raise AssertionError(f"Expected {self.name} of type {expected_type.__name__}, got {type(self.target).__name__}")
        return self

    def is_greater_than(self, threshold: Any) -> "FluentAssertion":
        if not (self.target > threshold):
            raise AssertionError(f"Expected {self.name} > {threshold}, but got {self.target}")
        return self

    def is_between(self, lower: Any, upper: Any) -> "FluentAssertion":
        if not (lower <= self.target <= upper):
            raise AssertionError(f"Expected {self.name} to be between {lower} and {upper}, got {self.target}")
        return self

    def contains(self, item: Any) -> "FluentAssertion":
        if item not in self.target:
            raise AssertionError(f"Expected {self.name} to contain {item!r}, but was not found")
        return self


def assert_that(val: Any, name: str = "value") -> FluentAssertion:
    return FluentAssertion(val, name)


def q10_architectural_fluent_assertions():
    # Chain multiple assertions fluently
    age = 28
    assert_that(age, "user_age") \
        .is_not_none() \
        .is_type(int) \
        .is_greater_than(18) \
        .is_between(20, 30) \
        .is_equal_to(28)

    roles = ["user", "admin", "tester"]
    assert_that(roles, "user_roles") \
        .is_not_none() \
        .contains("admin")

    # Verify failure diagnostic message
    caught = False
    try:
        assert_that(15, "score").is_greater_than(50)
    except AssertionError as err:
        caught = True
        assert "Expected score > 50, but got 15" in str(err)

    assert caught is True
    print("=== Q10: Architectural Fluent Assertion Engine Verified ===")


# =====================================================================
# Main Test Runner
# =====================================================================
if __name__ == "__main__":
    q1_numerical_boundary_assertions()
    q2_string_diffs_and_regex_assertions()
    q3_sequence_set_tuple_assertions()
    q4_dictionary_assertions()
    q5_warning_assertions()
    q6_custom_domain_assertions()
    q7_maxdiff_and_message_customization()
    q8_builtin_assert_mechanics()
    q9_multi_exception_assertions()
    q10_architectural_fluent_assertions()

    print("\nAll 10 assertions deep dive practice questions passed successfully!")
