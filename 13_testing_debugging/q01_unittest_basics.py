"""
Topic 13: Testing and Debugging
Question 01: unittest Basics

A comprehensive, production-grade guide to Python's built-in `unittest` framework.
Covers TestCase structure, equality & identity checks, truthiness & membership,
floating point delta assertions, exception testing (assertRaises & assertRaisesRegex),
type checking, sequence/dict assertions, skipping & expected failures, manual TestSuite
composition, and an architectural Custom TestResult JSON Reporter.

Every question contains standalone runnable exercises verified with 100% assertions.
"""

import unittest
import io
import json
import time
from typing import List, Dict, Any


# =====================================================================
# Q1: Basic TestCase Anatomy and Execution via TestRunner
# =====================================================================
class SimpleMathTestCase(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(2 + 3, 5)

    def test_multiplication(self):
        self.assertEqual(4 * 6, 24)


def q1_testcase_anatomy():
    """
    Demonstrates running a TestCase programmatically with TextTestRunner
    and capturing the test outcome.
    """
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(SimpleMathTestCase)
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert result.testsRun == 2
    assert len(result.failures) == 0
    assert len(result.errors) == 0

    print("=== Q1: TestCase Anatomy & TextTestRunner Verified ===")


# =====================================================================
# Q2: Equality and Identity Assertions
# =====================================================================
class EqualityIdentityTestCase(unittest.TestCase):
    def test_equality_vs_identity(self):
        list_a = [1, 2, 3]
        list_b = [1, 2, 3]
        list_c = list_a

        # Value equality
        self.assertEqual(list_a, list_b)
        self.assertNotEqual(list_a, [4, 5, 6])

        # Object identity (is vs is not)
        self.assertIs(list_a, list_c)
        self.assertIsNot(list_a, list_b)  # distinct memory objects

        # None checks
        val_none = None
        val_active = 42
        self.assertIsNone(val_none)
        self.assertIsNotNone(val_active)


def q2_equality_and_identity_assertions():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(EqualityIdentityTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)
    assert result.wasSuccessful() is True
    assert result.testsRun == 1

    print("=== Q2: Equality and Identity Assertions Verified ===")


# =====================================================================
# Q3: Truthiness and Membership Assertions
# =====================================================================
class TruthinessMembershipTestCase(unittest.TestCase):
    def test_boolean_and_membership(self):
        # Truthiness
        self.assertTrue(10 > 5)
        self.assertFalse(len([]) > 0)

        # Membership in collections
        collection = {"apple", "banana", "cherry"}
        self.assertIn("banana", collection)
        self.assertNotIn("dragonfruit", collection)

        # Substring membership
        text = "Advanced Python Architecture"
        self.assertIn("Python", text)
        self.assertNotIn("Cobol", text)


def q3_truthiness_and_membership():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TruthinessMembershipTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)
    assert result.wasSuccessful() is True
    assert result.testsRun == 1

    print("=== Q3: Truthiness and Membership Assertions Verified ===")


# =====================================================================
# Q4: Floating Point Precision and Delta Assertions
# =====================================================================
class FloatingPointTestCase(unittest.TestCase):
    def test_almost_equal(self):
        # 0.1 + 0.2 = 0.30000000000000004 in IEEE 754 float
        calc = 0.1 + 0.2
        # Default places=7 checks difference to 7 decimal places
        self.assertAlmostEqual(calc, 0.3, places=7)

        # Delta specification
        approx_pi = 22 / 7  # 3.142857...
        real_pi = 3.141592
        self.assertAlmostEqual(approx_pi, real_pi, delta=0.002)

        # Not almost equal
        self.assertNotAlmostEqual(calc, 0.35, delta=0.01)


def q4_floating_point_comparisons():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(FloatingPointTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)
    assert result.wasSuccessful() is True
    assert result.testsRun == 1

    print("=== Q4: Floating Point AlmostEqual & Delta Assertions Verified ===")


# =====================================================================
# Q5: Exception Testing with assertRaises and assertRaisesRegex
# =====================================================================
def divide_positive(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Denominator cannot be zero")
    if a < 0 or b < 0:
        raise ValueError("Only positive numbers allowed: a or b is negative")
    return a / b


class ExceptionTestingTestCase(unittest.TestCase):
    def test_zero_division(self):
        # Using context manager
        with self.assertRaises(ZeroDivisionError) as cm:
            divide_positive(10, 0)
        self.assertIn("Denominator cannot be zero", str(cm.exception))

    def test_regex_pattern_matching(self):
        # assertRaisesRegex checks both exception type and message regex pattern
        with self.assertRaisesRegex(ValueError, r"Only positive numbers"):
            divide_positive(-5, 2)


def q5_exception_testing():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ExceptionTestingTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)
    assert result.wasSuccessful() is True
    assert result.testsRun == 2

    print("=== Q5: Exception Testing (assertRaises & Regex) Verified ===")


# =====================================================================
# Q6: Type and Subclass Hierarchy Assertions
# =====================================================================
class Vehicle:
    pass


class ElectricCar(Vehicle):
    pass


class TypeAssertionsTestCase(unittest.TestCase):
    def test_types(self):
        car = ElectricCar()
        self.assertIsInstance(car, ElectricCar)
        self.assertIsInstance(car, Vehicle)
        self.assertNotIsInstance(car, str)

        # Exact type verification
        self.assertIs(type(car), ElectricCar)


def q6_type_assertions():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TypeAssertionsTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)
    assert result.wasSuccessful() is True
    assert result.testsRun == 1

    print("=== Q6: Type & Subclass Assertions Verified ===")


# =====================================================================
# Q7: Structured Sequence, Mapping, and Multiset Assertions
# =====================================================================
class CollectionsTestCase(unittest.TestCase):
    def test_list_and_dict_equality(self):
        self.assertListEqual([1, 2, 3], [1, 2, 3])
        self.assertDictEqual({"a": 1, "b": 2}, {"b": 2, "a": 1})
        self.assertSetEqual({1, 2, 3}, {3, 2, 1})

    def test_count_equal_multiset(self):
        # assertCountEqual tests that both sequences have the same elements and frequencies,
        # irrespective of ordering.
        seq1 = [1, 2, 2, 3, 4]
        seq2 = [4, 2, 1, 3, 2]
        self.assertCountEqual(seq1, seq2)


def q7_collections_assertions():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CollectionsTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)
    assert result.wasSuccessful() is True
    assert result.testsRun == 2

    print("=== Q7: Collection (List, Dict, CountEqual) Assertions Verified ===")


# =====================================================================
# Q8: Skipping Tests and Expected Failures
# =====================================================================
FEATURE_FLAG_ENABLED = False


class SkipAndExpectedFailTestCase(unittest.TestCase):
    @unittest.skip("Demonstrating unconditional skip")
    def test_unconditional_skip(self):
        self.fail("Should not execute")

    @unittest.skipIf(not FEATURE_FLAG_ENABLED, "Feature flag is disabled")
    def test_conditional_skip(self):
        self.fail("Should not execute when flag is false")

    @unittest.expectedFailure
    def test_known_bug(self):
        # Test known to fail currently; expectedFailure prevents build failure
        self.assertEqual(1 + 1, 3)


def q8_skipping_and_expected_failures():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(SkipAndExpectedFailTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)

    assert result.wasSuccessful() is True
    assert len(result.skipped) == 2
    assert len(result.expectedFailures) == 1

    print("=== Q8: Skipping Tests and Expected Failures Verified ===")


# =====================================================================
# Q9: Programmatic TestSuite Construction and Filtering
# =====================================================================
class SuiteMathA(unittest.TestCase):
    def test_add(self):
        self.assertEqual(1 + 1, 2)

    def test_sub(self):
        self.assertEqual(5 - 2, 3)


class SuiteMathB(unittest.TestCase):
    def test_mul(self):
        self.assertEqual(3 * 3, 9)


def q9_programmatic_test_suites():
    # Construct an arbitrary composite test suite manually
    custom_suite = unittest.TestSuite()
    custom_suite.addTest(SuiteMathA("test_add"))
    custom_suite.addTest(SuiteMathB("test_mul"))

    assert custom_suite.countTestCases() == 2

    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(custom_suite)
    assert result.wasSuccessful() is True
    assert result.testsRun == 2

    print("=== Q9: Programmatic TestSuite Composition Verified ===")


# =====================================================================
# Q10: Architectural Custom TestResult JSON Reporter
# =====================================================================
class JSONTestResult(unittest.TestResult):
    """
    Custom TestResult collector producing structured JSON reports
    recording start times, execution durations, failures, and skips.
    """
    def __init__(self):
        super().__init__()
        self.records: List[Dict[str, Any]] = []
        self._test_start_time: float = 0.0

    def startTest(self, test):
        super().startTest(test)
        self._test_start_time = time.time()

    def addSuccess(self, test):
        super().addSuccess(test)
        duration = round(time.time() - self._test_start_time, 4)
        self.records.append({
            "test_id": test.id(),
            "status": "PASS",
            "duration": duration
        })

    def addFailure(self, test, err):
        super().addFailure(test, err)
        duration = round(time.time() - self._test_start_time, 4)
        self.records.append({
            "test_id": test.id(),
            "status": "FAIL",
            "error": str(err[1]),
            "duration": duration
        })

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.records.append({
            "test_id": test.id(),
            "status": "SKIP",
            "reason": reason,
            "duration": 0.0
        })

    def generate_report_json(self) -> str:
        summary = {
            "total_run": self.testsRun,
            "passed": len([r for r in self.records if r["status"] == "PASS"]),
            "failed": len(self.failures),
            "skipped": len(self.skipped),
            "tests": self.records
        }
        return json.dumps(summary, indent=2)


class ReportTargetTestCase(unittest.TestCase):
    def test_pass_1(self):
        self.assertEqual(10, 10)

    def test_pass_2(self):
        self.assertTrue(True)

    @unittest.skip("Demo skip for report")
    def test_skip_item(self):
        pass


def q10_architectural_json_test_reporter():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ReportTargetTestCase)
    custom_result = JSONTestResult()
    suite.run(custom_result)

    assert custom_result.wasSuccessful() is True
    assert custom_result.testsRun == 3

    report_str = custom_result.generate_report_json()
    report = json.loads(report_str)

    assert report["total_run"] == 3
    assert report["passed"] == 2
    assert report["skipped"] == 1
    assert report["failed"] == 0
    assert len(report["tests"]) == 3

    print("=== Q10: Architectural Custom JSON Test Reporter Verified ===")


# =====================================================================
# Main Test Runner
# =====================================================================
if __name__ == "__main__":
    q1_testcase_anatomy()
    q2_equality_and_identity_assertions()
    q3_truthiness_and_membership()
    q4_floating_point_comparisons()
    q5_exception_testing()
    q6_type_assertions()
    q7_collections_assertions()
    q8_skipping_and_expected_failures()
    q9_programmatic_test_suites()
    q10_architectural_json_test_reporter()

    print("\nAll 10 unittest basics practice questions passed successfully!")
