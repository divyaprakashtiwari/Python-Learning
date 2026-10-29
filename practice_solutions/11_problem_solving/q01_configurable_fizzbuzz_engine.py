"""
Question 1: Configurable Rule-Based FizzBuzz Engine
Topic: Problem Solving & Competitive Programming Patterns

Key Concepts Tested:
- Extensible rule-based dispatch via divisor-to-tag mappings
- Lazy sequence generation using Python generator functions
- Aggregate frequency tracking and telemetry analysis
- Boundary and error validation for non-positive divisors
"""

from typing import Dict, Generator, Optional, Any


class ConfigurableFizzBuzz:
    """
    Extensible FizzBuzz engine supporting arbitrary divisor rules,
    lazy stream evaluation, and statistical summaries.
    """

    def __init__(self, rules: Optional[Dict[int, str]] = None) -> None:
        if rules is None:
            self._rules = {3: "Fizz", 5: "Buzz"}
        else:
            for divisor in rules:
                if divisor <= 0:
                    raise ValueError(f"Divisor must be a positive integer, got: {divisor}")
            self._rules = dict(rules)

    def evaluate(self, n: int) -> str:
        """Evaluates a single integer against registered rules in order."""
        result_parts = []
        for divisor, tag in self._rules.items():
            if n % divisor == 0:
                result_parts.append(tag)

        return "".join(result_parts) if result_parts else str(n)

    def generate_sequence(self, start: int, stop: int) -> Generator[str, None, None]:
        """Lazily yields FizzBuzz tokens for the range [start, stop]."""
        if start > stop:
            return
        for i in range(start, stop + 1):
            yield self.evaluate(i)

    def frequency_summary(self, n: int) -> Dict[str, int]:
        """
        Generates summary statistics for evaluations from 1 to n.
        Counts numbers as 'numbers' and tracks specific tag frequencies.
        """
        summary: Dict[str, int] = {"numbers": 0}

        for token in self.generate_sequence(1, n):
            if token.isdigit():
                summary["numbers"] += 1
            else:
                summary[token] = summary.get(token, 0) + 1

        return summary


if __name__ == "__main__":
    engine = ConfigurableFizzBuzz()

    print("=== 1. Standard FizzBuzz Sequence (1 to 15) ===")
    standard_results = list(engine.generate_sequence(1, 15))
    print(f"Standard 1 to 15:\n{standard_results}")

    print("\n=== 2. Custom Rules Evaluation ===")
    custom_engine = ConfigurableFizzBuzz(rules={2: "Bi", 3: "Tri", 5: "Quint"})
    test_values = [2, 3, 6, 15, 30, 7]
    print("Custom Rule Evaluations:")
    for val in test_values:
        print(f"- {val} -> '{custom_engine.evaluate(val)}'")

    print("\n=== 3. Frequency Summary for N=15 ===")
    stats = engine.frequency_summary(15)
    print(f"Frequency Summary for 15:\n{stats}")

    print("\n=== 4. Edge Cases & Validation ===")
    try:
        ConfigurableFizzBuzz(rules={0: "ZeroDiv"})
    except ValueError as err:
        print(f"Caught non-positive divisor: {err}")

    empty_gen = list(engine.generate_sequence(10, 5))
    print(f"Empty sequence when start > stop: {empty_gen}")
