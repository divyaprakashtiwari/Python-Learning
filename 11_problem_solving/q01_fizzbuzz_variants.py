"""
Topic: Problem Solving - FizzBuzz and Variants
----------------------------------------------
Questions Covered:
1. Classic FizzBuzz: Standard 3 ("Fizz"), 5 ("Buzz"), 15 ("FizzBuzz") branching logic.
2. Extensible Mapping FizzBuzz: Dictionary-driven divisor rules supporting arbitrary token additions.
3. Functional Comprehension FizzBuzz: Single-expression string evaluation without if-elif ladders.
4. Streaming Generator FizzBuzz: Infinite and bounded lazy generator yielding tokens on demand.
5. Reverse FizzBuzz Engine: Deducing the original integer start and range from a sequence of tokens.
6. Modulo-Free FizzBuzz: Counter and step resets eliminating the '%' remainder operator.
7. Digit-Conditioned Variant: Combining divisibility with digit presence checks (e.g. contains '3' or '5').
8. Multi-Threaded Synchronized FizzBuzz: Four cooperative threads coordinated via Condition locks.
9. 2D Spiral Matrix FizzBuzz: Populating an N x N spiral matrix with classified FizzBuzz tokens.
10. Architectural System: Declarative Rule-Engine Business Classifier with priority overrides and metrics.
"""

import threading
from typing import List, Dict, Any, Optional, Tuple, Generator, Callable


# ==============================================================================
# Question 1: Classic FizzBuzz (1 to N)
# ==============================================================================
def classic_fizzbuzz(n: int) -> List[str]:
    """
    Returns list of strings from 1 to n:
    - Multiples of 3 and 5 are 'FizzBuzz'
    - Multiples of 3 are 'Fizz'
    - Multiples of 5 are 'Buzz'
    - Otherwise string of number
    """
    res = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            res.append("FizzBuzz")
        elif i % 3 == 0:
            res.append("Fizz")
        elif i % 5 == 0:
            res.append("Buzz")
        else:
            res.append(str(i))
    return res


def test_q1_classic_fizzbuzz():
    fb15 = classic_fizzbuzz(15)
    assert fb15[0] == "1"
    assert fb15[2] == "Fizz"      # 3
    assert fb15[4] == "Buzz"      # 5
    assert fb15[5] == "Fizz"      # 6
    assert fb15[8] == "Fizz"      # 9
    assert fb15[9] == "Buzz"      # 10
    assert fb15[14] == "FizzBuzz" # 15
    assert len(fb15) == 15
    print("=== Q1: Classic FizzBuzz Verified ===")


# ==============================================================================
# Question 2: Extensible Mapping-Driven FizzBuzz
# ==============================================================================
def extensible_fizzbuzz(n: int, rules: Dict[int, str]) -> List[str]:
    """
    Evaluates numbers from 1 to n against arbitrary divisor-to-word rules.
    Words are concatenated in order of rule definition.
    e.g. {3: 'Fizz', 5: 'Buzz', 7: 'Bazz'} -> 105 is 'FizzBuzzBazz'
    """
    results = []
    for i in range(1, n + 1):
        matched_words = [word for divisor, word in rules.items() if i % divisor == 0]
        if matched_words:
            results.append("".join(matched_words))
        else:
            results.append(str(i))
    return results


def test_q2_extensible_fizzbuzz():
    rules = {3: "Fizz", 5: "Buzz", 7: "Bazz"}
    res = extensible_fizzbuzz(21, rules)
    # 3: Fizz, 5: Buzz, 7: Bazz, 15: FizzBuzz, 21: FizzBazz
    assert res[2] == "Fizz"
    assert res[4] == "Buzz"
    assert res[6] == "Bazz"
    assert res[14] == "FizzBuzz"
    assert res[20] == "FizzBazz"  # 21 divisible by 3 and 7
    print("=== Q2: Extensible Mapping-Driven FizzBuzz Verified ===")


# ==============================================================================
# Question 3: Functional Comprehension FizzBuzz
# ==============================================================================
def functional_fizzbuzz(n: int) -> List[str]:
    """Single list comprehension expression performing FizzBuzz transformation."""
    return [
        ("Fizz" * (i % 3 == 0) + "Buzz" * (i % 5 == 0)) or str(i)
        for i in range(1, n + 1)
    ]


def test_q3_functional_fizzbuzz():
    assert functional_fizzbuzz(15) == classic_fizzbuzz(15)
    print("=== Q3: Functional Comprehension FizzBuzz Verified ===")


# ==============================================================================
# Question 4: Streaming Generator FizzBuzz
# ==============================================================================
def stream_fizzbuzz(start: int = 1) -> Generator[str, None, None]:
    """Infinite lazy generator yielding FizzBuzz evaluations one by one."""
    curr = start
    while True:
        token = ("Fizz" * (curr % 3 == 0) + "Buzz" * (curr % 5 == 0)) or str(curr)
        yield token
        curr += 1


def test_q4_streaming_fizzbuzz():
    gen = stream_fizzbuzz(start=1)
    first_15 = [next(gen) for _ in range(15)]
    assert first_15 == classic_fizzbuzz(15)
    print("=== Q4: Streaming Generator FizzBuzz Verified ===")


# ==============================================================================
# Question 5: Reverse FizzBuzz Engine
# ==============================================================================
def reverse_fizzbuzz(tokens: List[str]) -> Optional[int]:
    """
    Given an output sequence of tokens, determines the smallest starting integer 'start'
    such that classic_fizzbuzz evaluation from start to start + len(tokens) - 1 produces tokens.
    Returns starting integer, or None if no valid starting sequence exists.
    """
    if not tokens:
        return None

    # Find candidate starting numbers by matching any numeric token
    for idx, token in enumerate(tokens):
        if token.isdigit():
            start_candidate = int(token) - idx
            if start_candidate > 0:
                # Verify entire candidate sequence
                expected = [
                    ("Fizz" * (n % 3 == 0) + "Buzz" * (n % 5 == 0)) or str(n)
                    for n in range(start_candidate, start_candidate + len(tokens))
                ]
                if expected == tokens:
                    return start_candidate

    # If all tokens are non-numeric (e.g. ["Fizz", "Buzz"]), test candidates 1..15
    for candidate in range(1, 16):
        expected = [
            ("Fizz" * (n % 3 == 0) + "Buzz" * (n % 5 == 0)) or str(n)
            for n in range(candidate, candidate + len(tokens))
        ]
        if expected == tokens:
            return candidate

    return None


def test_q5_reverse_fizzbuzz():
    seq1 = ["Fizz", "4", "Buzz"]
    assert reverse_fizzbuzz(seq1) == 3

    seq2 = ["Fizz", "Buzz"]  # 9 (Fizz), 10 (Buzz)
    assert reverse_fizzbuzz(seq2) == 9

    seq3 = ["FizzBuzz", "16", "17"]
    assert reverse_fizzbuzz(seq3) == 15

    invalid = ["Buzz", "Buzz"]  # Consecutive buzz is impossible in standard fizzbuzz
    assert reverse_fizzbuzz(invalid) is None
    print("=== Q5: Reverse FizzBuzz Engine Verified ===")


# ==============================================================================
# Question 6: Modulo-Free FizzBuzz (Counters / Step Resets)
# ==============================================================================
def modulo_free_fizzbuzz(n: int) -> List[str]:
    """
    Computes FizzBuzz from 1 to n without using '%' or '//' division operators.
    Uses independent counters resetting at 3 and 5.
    """
    res = []
    c3 = 0
    c5 = 0

    for i in range(1, n + 1):
        c3 += 1
        c5 += 1
        is_fizz = (c3 == 3)
        is_buzz = (c5 == 5)

        if is_fizz and is_buzz:
            res.append("FizzBuzz")
            c3 = 0
            c5 = 0
        elif is_fizz:
            res.append("Fizz")
            c3 = 0
        elif is_buzz:
            res.append("Buzz")
            c5 = 0
        else:
            res.append(str(i))

    return res


def test_q6_modulo_free_fizzbuzz():
    assert modulo_free_fizzbuzz(30) == classic_fizzbuzz(30)
    print("=== Q6: Modulo-Free FizzBuzz Verified ===")


# ==============================================================================
# Question 7: Digit-Conditioned FizzBuzz (Divisibility + Digit Presence)
# ==============================================================================
def digit_conditioned_fizzbuzz(n: int) -> List[str]:
    """
    Variant rule:
    - If divisible by 3 OR contains the digit '3': adds 'Fizz'
    - If divisible by 5 OR contains the digit '5': adds 'Buzz'
    - Concatenates combinations, else returns str(num)
    """
    res = []
    for i in range(1, n + 1):
        s_num = str(i)
        is_fizz = (i % 3 == 0) or ("3" in s_num)
        is_buzz = (i % 5 == 0) or ("5" in s_num)

        if is_fizz and is_buzz:
            res.append("FizzBuzz")
        elif is_fizz:
            res.append("Fizz")
        elif is_buzz:
            res.append("Buzz")
        else:
            res.append(s_num)
    return res


def test_q7_digit_conditioned_fizzbuzz():
    res = digit_conditioned_fizzbuzz(35)
    # 13 contains '3' (not divisible by 3) -> Fizz
    assert res[12] == "Fizz"
    # 51 divisible by 3 and contains 5 -> FizzBuzz
    # 35 contains 3 and 5 -> FizzBuzz
    assert res[34] == "FizzBuzz"
    print("=== Q7: Digit-Conditioned FizzBuzz Verified ===")


# ==============================================================================
# Question 8: Multi-Threaded Synchronized FizzBuzz
# ==============================================================================
class SynchronizedFizzBuzz:
    """
    Four concurrent threads cooperate to output FizzBuzz from 1 to n in exact sequence:
    - Thread A calls fizz()
    - Thread B calls buzz()
    - Thread C calls fizzbuzz()
    - Thread D calls number()
    """
    def __init__(self, n: int):
        self.n = n
        self.curr = 1
        self.output: List[str] = []
        self.lock = threading.Lock()
        self.cond = threading.Condition(self.lock)

    def fizz(self):
        while True:
            with self.cond:
                while self.curr <= self.n and not (self.curr % 3 == 0 and self.curr % 5 != 0):
                    self.cond.wait()
                if self.curr > self.n:
                    return
                self.output.append("Fizz")
                self.curr += 1
                self.cond.notify_all()

    def buzz(self):
        while True:
            with self.cond:
                while self.curr <= self.n and not (self.curr % 5 == 0 and self.curr % 3 != 0):
                    self.cond.wait()
                if self.curr > self.n:
                    return
                self.output.append("Buzz")
                self.curr += 1
                self.cond.notify_all()

    def fizzbuzz(self):
        while True:
            with self.cond:
                while self.curr <= self.n and not (self.curr % 15 == 0):
                    self.cond.wait()
                if self.curr > self.n:
                    return
                self.output.append("FizzBuzz")
                self.curr += 1
                self.cond.notify_all()

    def number(self):
        while True:
            with self.cond:
                while self.curr <= self.n and (self.curr % 3 == 0 or self.curr % 5 == 0):
                    self.cond.wait()
                if self.curr > self.n:
                    return
                self.output.append(str(self.curr))
                self.curr += 1
                self.cond.notify_all()

    def run(self) -> List[str]:
        t1 = threading.Thread(target=self.fizz)
        t2 = threading.Thread(target=self.buzz)
        t3 = threading.Thread(target=self.fizzbuzz)
        t4 = threading.Thread(target=self.number)

        threads = [t1, t2, t3, t4]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        return self.output


def test_q8_multithreaded_fizzbuzz():
    fb = SynchronizedFizzBuzz(n=15)
    res = fb.run()
    assert res == classic_fizzbuzz(15)
    print("=== Q8: Multi-Threaded Synchronized FizzBuzz Verified ===")


# ==============================================================================
# Question 9: 2D Spiral Matrix FizzBuzz
# ==============================================================================
def spiral_fizzbuzz_matrix(n: int) -> List[List[str]]:
    """
    Fills an N x N 2D matrix with numbers from 1 to N^2 following a clockwise spiral,
    applying FizzBuzz conversion to each cell.
    """
    matrix: List[List[str]] = [[""] * n for _ in range(n)]
    top, bottom = 0, n - 1
    left, right = 0, n - 1
    num = 1

    def to_token(val: int) -> str:
        return ("Fizz" * (val % 3 == 0) + "Buzz" * (val % 5 == 0)) or str(val)

    while top <= bottom and left <= right:
        # Traverse right across top row
        for c in range(left, right + 1):
            matrix[top][c] = to_token(num)
            num += 1
        top += 1

        # Traverse down right column
        for r in range(top, bottom + 1):
            matrix[r][right] = to_token(num)
            num += 1
        right -= 1

        # Traverse left across bottom row
        if top <= bottom:
            for c in range(right, left - 1, -1):
                matrix[bottom][c] = to_token(num)
                num += 1
            bottom -= 1

        # Traverse up left column
        if left <= right:
            for r in range(bottom, top - 1, -1):
                matrix[r][left] = to_token(num)
                num += 1
            left += 1

    return matrix


def test_q9_spiral_matrix_fizzbuzz():
    # 3x3 spiral:
    # 1(1)    2(2)    3(Fizz)
    # 8(8)    9(Fizz) 4(4)
    # 7(7)    6(Fizz) 5(Buzz)
    matrix = spiral_fizzbuzz_matrix(3)
    assert matrix[0] == ["1", "2", "Fizz"]
    assert matrix[1] == ["8", "Fizz", "4"]
    assert matrix[2] == ["7", "Fizz", "Buzz"]
    print("=== Q9: 2D Spiral Matrix FizzBuzz Verified ===")


# ==============================================================================
# Question 10: Architectural System: Business Event Categorization Rule Engine
# ==============================================================================
class CategorizationRule:
    def __init__(self, name: str, predicate: Callable[[Dict[str, Any]], bool], label: str, priority: int):
        self.name = name
        self.predicate = predicate
        self.label = label
        self.priority = priority


class EventCategorizerEngine:
    """
    Enterprise-grade general rule classifier generalizing FizzBuzz mechanics:
    - Multi-predicate rule evaluation
    - Priority-based conflict resolution and combined tagging
    - Fallback default categorization
    """
    def __init__(self):
        self._rules: List[CategorizationRule] = []
        self.stats = {"categorized": 0, "fallbacks": 0}

    def register_rule(self, name: str, predicate: Callable[[Dict[str, Any]], bool], label: str, priority: int = 0):
        self._rules.append(CategorizationRule(name, predicate, label, priority))
        # Sort by priority descending
        self._rules.sort(key=lambda r: r.priority, reverse=True)

    def categorize_event(self, event: Dict[str, Any], combine_matches: bool = True) -> str:
        self.stats["categorized"] += 1
        matched_labels = [r.label for r in self._rules if r.predicate(event)]

        if matched_labels:
            if combine_matches:
                return "_".join(matched_labels)
            return matched_labels[0]

        self.stats["fallbacks"] += 1
        return "STANDARD"


def test_q10_event_categorizer_engine():
    engine = EventCategorizerEngine()

    # Rule 1: High value transaction
    engine.register_rule("VIP_AMOUNT", lambda e: e.get("amount", 0) >= 1000, "VIP", priority=10)
    # Rule 2: International transfer
    engine.register_rule("CROSS_BORDER", lambda e: e.get("currency") != "USD", "INTERNATIONAL", priority=5)

    # Both rules match -> VIP_INTERNATIONAL
    e1 = {"amount": 2500, "currency": "EUR"}
    assert engine.categorize_event(e1) == "VIP_INTERNATIONAL"

    # Only VIP matches
    e2 = {"amount": 1500, "currency": "USD"}
    assert engine.categorize_event(e2) == "VIP"

    # Fallback
    e3 = {"amount": 50, "currency": "USD"}
    assert engine.categorize_event(e3) == "STANDARD"

    assert engine.stats["categorized"] == 3
    assert engine.stats["fallbacks"] == 1
    print("=== Q10: Architectural Event Categorization Rule Engine Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_classic_fizzbuzz()
    test_q2_extensible_fizzbuzz()
    test_q3_functional_fizzbuzz()
    test_q4_streaming_fizzbuzz()
    test_q5_reverse_fizzbuzz()
    test_q6_modulo_free_fizzbuzz()
    test_q7_digit_conditioned_fizzbuzz()
    test_q8_multithreaded_fizzbuzz()
    test_q9_spiral_matrix_fizzbuzz()
    test_q10_event_categorizer_engine()
    print("\nAll 10 FizzBuzz variant problem-solving questions passed successfully!")
