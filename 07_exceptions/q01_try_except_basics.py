"""
Topic 07: Exceptions - Question 01: Try/Except Basics

A comprehensive collection of 10 standalone, runnable exercises exploring
foundational exception handling in Python using `try` and `except` blocks.

Questions Covered:
 1. ZeroDivisionError: Intercepting arithmetic divide-by-zero errors.
 2. ValueError: Handling invalid string-to-number parsing and formatting errors.
 3. IndexError: Guarding against out-of-range sequence access on lists/tuples.
 4. KeyError: Intercepting missing dictionary key lookups.
 5. TypeError: Handling mismatched data types and invalid operator pairings.
 6. FileNotFoundError: Intercepting missing filesystem resource lookups.
 7. AttributeError: Handling non-existent object attributes and methods.
 8. Exception Inspection: Extracting err.args, type(err).__name__, and str(err).
 9. Bare except vs except Exception: Why catching BaseException is dangerous.
10. Advanced Project: Safe Expression Evaluator & Fault-Tolerant Data Pipeline.
"""

from typing import Any


# ==============================================================================
# Question 1: ZeroDivisionError Handling
# ==============================================================================
def safe_divide(numerator: float, denominator: float) -> tuple[float | None, str | None]:
    """
    Safely divide two numbers, intercepting ZeroDivisionError.
    """
    try:
        result = numerator / denominator
        return result, None
    except ZeroDivisionError as err:
        return None, str(err)


def exercise_q1_zero_division() -> None:
    """
    Demonstrate intercepting ZeroDivisionError.
    """
    print("=== Q1: ZeroDivisionError Handling ===")

    success, err1 = safe_divide(10, 2)
    assert success == 5.0
    assert err1 is None

    failure, err2 = safe_divide(10, 0)
    assert failure is None
    assert err2 is not None
    assert "division by zero" in err2

    print(f"  10 / 2 = {success}")
    print(f"  10 / 0 intercepted error: '{err2}'")


# ==============================================================================
# Question 2: ValueError in String Parsing
# ==============================================================================
def parse_integer(value_str: str, default: int = 0) -> int:
    """
    Parses a string into an integer, falling back to default on ValueError.
    """
    try:
        return int(value_str)
    except ValueError:
        return default


def exercise_q2_value_error() -> None:
    """
    Demonstrate catching ValueError during type casting.
    """
    print("\n=== Q2: ValueError in String Parsing ===")

    assert parse_integer("42") == 42
    assert parse_integer("-17") == -17
    assert parse_integer("abc", default=-1) == -1
    assert parse_integer("3.14", default=0) == 0  # int("3.14") raises ValueError

    print("  '42' parsed to:", parse_integer("42"))
    print("  'abc' fell back to default:", parse_integer("abc", default=-1))


# ==============================================================================
# Question 3: IndexError Guarding
# ==============================================================================
def safe_get_element(items: list[Any], index: int, fallback: Any = None) -> Any:
    """
    Retrieve element by index, intercepting IndexError.
    """
    try:
        return items[index]
    except IndexError:
        return fallback


def exercise_q3_index_error() -> None:
    """
    Demonstrate guarding against IndexError on list access.
    """
    print("\n=== Q3: IndexError Guarding ===")

    data = ["alpha", "beta", "gamma"]
    assert safe_get_element(data, 1) == "beta"
    assert safe_get_element(data, 10, fallback="MISSING") == "MISSING"
    assert safe_get_element(data, -4, fallback="OUT_OF_BOUNDS") == "OUT_OF_BOUNDS"

    print("  Index 1 retrieved:", safe_get_element(data, 1))
    print("  Index 10 fallback:", safe_get_element(data, 10, fallback="MISSING"))


# ==============================================================================
# Question 4: KeyError Guarding
# ==============================================================================
def safe_dict_lookup(mapping: dict[str, Any], key: str) -> tuple[bool, Any]:
    """
    Look up key in dictionary with try/except KeyError.
    """
    try:
        return True, mapping[key]
    except KeyError:
        return False, None


def exercise_q4_key_error() -> None:
    """
    Demonstrate catching KeyError on dictionary lookups.
    """
    print("\n=== Q4: KeyError Guarding ===")

    config = {"host": "localhost", "port": 8080}
    found, val = safe_dict_lookup(config, "port")
    assert found is True
    assert val == 8080

    missing_found, missing_val = safe_dict_lookup(config, "ssl_cert")
    assert missing_found is False
    assert missing_val is None

    print(f"  'port' lookup: found={found}, val={val}")
    print(f"  'ssl_cert' lookup: found={missing_found}, val={missing_val}")


# ==============================================================================
# Question 5: TypeError Handling
# ==============================================================================
def safe_string_concat(item1: Any, item2: Any) -> str:
    """
    Concatenate two items as strings, handling TypeError if operation fails.
    """
    try:
        return item1 + item2
    except TypeError:
        return str(item1) + str(item2)


def exercise_q5_type_error() -> None:
    """
    Demonstrate catching TypeError when incompatible types are combined.
    """
    print("\n=== Q5: TypeError Handling ===")

    assert safe_string_concat("Hello ", "World") == "Hello World"
    # "Score: " + 100 raises TypeError; fallback coerces to str
    assert safe_string_concat("Score: ", 100) == "Score: 100"
    assert safe_string_concat([1, 2], [3]) == [1, 2, 3]

    print("  Safe concatenation fallback:", safe_string_concat("Score: ", 100))


# ==============================================================================
# Question 6: FileNotFoundError Handling
# ==============================================================================
def safe_read_file(filepath: str) -> str | None:
    """
    Attempts to read text file, catching FileNotFoundError.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None


def exercise_q6_file_not_found() -> None:
    """
    Demonstrate intercepting missing file system requests.
    """
    print("\n=== Q6: FileNotFoundError Handling ===")

    res = safe_read_file("non_existent_system_file_12345.xyz")
    assert res is None
    print("  Missing file safely handled, returned None.")


# ==============================================================================
# Question 7: AttributeError Handling
# ==============================================================================
def safe_invoke_method(obj: Any, method_name: str, *args: Any) -> Any:
    """
    Invokes named method on object if it exists, catching AttributeError.
    """
    try:
        method = getattr(obj, method_name)
        return method(*args)
    except AttributeError:
        return None


def exercise_q7_attribute_error() -> None:
    """
    Demonstrate catching AttributeError for missing object methods.
    """
    print("\n=== Q7: AttributeError Handling ===")

    text = "hello python"
    res1 = safe_invoke_method(text, "upper")
    assert res1 == "HELLO PYTHON"

    # Numbers do not have an .upper() method
    res2 = safe_invoke_method(12345, "upper")
    assert res2 is None

    print(f"  text.upper() succeeded: '{res1}'")
    print(f"  (12345).upper() caught AttributeError: {res2}")


# ==============================================================================
# Question 8: Exception Inspection (args, name, message)
# ==============================================================================
def exercise_q8_exception_inspection() -> None:
    """
    Inspect an exception object's type name, args tuple, and formatted string.
    """
    print("\n=== Q8: Exception Inspection ===")

    try:
        # Intentionally trigger an exception with details
        raise ValueError("Invalid configuration parameter", 400, "MISSING_API_KEY")
    except ValueError as err:
        type_name = type(err).__name__
        err_args = err.args
        err_str = str(err)

        assert type_name == "ValueError"
        assert len(err_args) == 3
        assert err_args[1] == 400
        assert "MISSING_API_KEY" in err_str

        print(f"  Exception Class: {type_name}")
        print(f"  Exception Args:  {err_args}")
        print(f"  Exception Str:   {err_str}")


# ==============================================================================
# Question 9: Bare except vs except Exception
# ==============================================================================
def exercise_q9_bare_except_dangers() -> None:
    """
    Contrast catching `Exception` (catches standard application errors)
    versus bare `except:` or `BaseException` (which catches system-exiting signals
    like KeyboardInterrupt and SystemExit).
    """
    print("\n=== Q9: Bare except vs except Exception ===")

    # Standard application errors inherit from Exception
    assert issubclass(ValueError, Exception)
    assert issubclass(KeyError, Exception)
    assert issubclass(ZeroDivisionError, Exception)

    # System signals inherit directly from BaseException, NOT Exception
    assert issubclass(KeyboardInterrupt, BaseException)
    assert not issubclass(KeyboardInterrupt, Exception)
    assert issubclass(SystemExit, BaseException)
    assert not issubclass(SystemExit, Exception)

    # An `except Exception:` block properly lets KeyboardInterrupt pass through!
    caught_by_standard_exception = False
    try:
        try:
            raise KeyboardInterrupt("Simulated Ctrl+C")
        except Exception:
            caught_by_standard_exception = True
    except KeyboardInterrupt:
        pass  # Caught here at top level

    assert caught_by_standard_exception is False
    print("  KeyboardInterrupt successfully bypassed 'except Exception:' (preventing swallowed Ctrl+C).")


# ==============================================================================
# Question 10: Advanced Project - Fault-Tolerant Expression Pipeline
# ==============================================================================
class FaultTolerantPipeline:
    """
    Executes a sequence of data transformation steps, intercepting errors
    at individual steps and producing a comprehensive execution ledger.
    """

    def __init__(self) -> None:
        self.successes: list[tuple[str, Any]] = []
        self.failures: list[dict[str, Any]] = []

    def execute_step(self, step_name: str, func: Any, *args: Any, **kwargs: Any) -> Any:
        try:
            result = func(*args, **kwargs)
            self.successes.append((step_name, result))
            return result
        except Exception as exc:
            self.failures.append({
                "step": step_name,
                "error_type": type(exc).__name__,
                "message": str(exc),
            })
            return None


def exercise_q10_fault_tolerant_pipeline() -> None:
    """
    Demonstrate FaultTolerantPipeline executing mixed valid and invalid operations.
    """
    print("\n=== Q10: Fault-Tolerant Expression Pipeline ===")

    pipeline = FaultTolerantPipeline()

    pipeline.execute_step("parse_int", int, "42")
    pipeline.execute_step("bad_parse", int, "invalid_num")
    pipeline.execute_step("valid_div", lambda a, b: a / b, 100, 4)
    pipeline.execute_step("div_zero", lambda a, b: a / b, 100, 0)
    pipeline.execute_step("list_pop", lambda lst: lst.pop(), [1, 2])

    assert len(pipeline.successes) == 3
    assert len(pipeline.failures) == 2

    assert pipeline.successes[0] == ("parse_int", 42)
    assert pipeline.successes[1] == ("valid_div", 25.0)

    assert pipeline.failures[0]["step"] == "bad_parse"
    assert pipeline.failures[0]["error_type"] == "ValueError"

    assert pipeline.failures[1]["step"] == "div_zero"
    assert pipeline.failures[1]["error_type"] == "ZeroDivisionError"

    print(f"  Successful steps ({len(pipeline.successes)}): {[s[0] for s in pipeline.successes]}")
    print(f"  Captured failures ({len(pipeline.failures)}): {pipeline.failures}")


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_zero_division()
    exercise_q2_value_error()
    exercise_q3_index_error()
    exercise_q4_key_error()
    exercise_q5_type_error()
    exercise_q6_file_not_found()
    exercise_q7_attribute_error()
    exercise_q8_exception_inspection()
    exercise_q9_bare_except_dangers()
    exercise_q10_fault_tolerant_pipeline()

    print("\nAll 10 try/except basics questions executed and asserted successfully!")
