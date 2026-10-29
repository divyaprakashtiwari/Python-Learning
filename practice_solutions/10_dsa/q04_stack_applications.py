"""
Question 4: Robust Stack Implementations & Algorithmic Applications
Topic: Data Structures & Algorithms (DSA)

Key Concepts Tested:
- Generic LIFO ArrayStack with custom StackUnderflowError
- Balanced delimiter validation with informative syntax error messages
- Constant-time O(1) MinStack using parallel auxiliary tracking
- Reverse Polish Notation (RPN / Postfix) evaluation with truncate-toward-zero division
"""

from typing import TypeVar, Generic, List, Tuple, Optional

T = TypeVar("T")


class StackUnderflowError(Exception):
    """Raised when an operation is performed on an empty stack."""
    pass


class ArrayStack(Generic[T]):
    """
    Standard LIFO stack backed by a dynamic list.
    """

    def __init__(self) -> None:
        self._data: List[T] = []

    def push(self, item: T) -> None:
        self._data.append(item)

    def pop(self) -> T:
        if self.is_empty():
            raise StackUnderflowError("Cannot pop from an empty stack")
        return self._data.pop()

    def peek(self) -> T:
        if self.is_empty():
            raise StackUnderflowError("Cannot peek into an empty stack")
        return self._data[-1]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        top_str = repr(self._data[-1]) if self._data else "None"
        return f"ArrayStack(size={len(self._data)}, top={top_str})"


def is_balanced(expression: str) -> Tuple[bool, str]:
    """
    Validates balanced nested delimiters (), {}, [] in an expression.
    Returns (True, 'Balanced') or (False, '<error message>').
    """
    stack: List[str] = []
    pairs = {")": "(", "}": "{", "]": "["}
    reverse_pairs = {"(": ")", "{": "}", "[": "]"}

    for char in expression:
        if char in "({[":
            stack.append(char)
        elif char in ")}]":
            if not stack:
                return (False, f"Unexpected closing bracket '{char}'")
            top = stack.pop()
            if top != pairs[char]:
                expected = reverse_pairs[top]
                return (False, f"Mismatched closing bracket '{char}' expecting '{expected}'")

    if stack:
        return (False, f"Unclosed opening bracket '{stack[-1]}'")

    return (True, "Balanced")


class MinStack:
    """
    Constant-time min stack maintaining O(1) time complexity
    for push, pop, top, and get_min operations using an auxiliary min-tracker.
    """

    def __init__(self) -> None:
        self._stack: List[int] = []
        self._min_stack: List[int] = []

    def push(self, val: int) -> None:
        self._stack.append(val)
        current_min = self._min_stack[-1] if self._min_stack else val
        self._min_stack.append(min(val, current_min))

    def pop(self) -> int:
        if not self._stack:
            raise StackUnderflowError("Cannot pop from an empty MinStack")
        self._min_stack.pop()
        return self._stack.pop()

    def top(self) -> int:
        if not self._stack:
            raise StackUnderflowError("Cannot read top of an empty MinStack")
        return self._stack[-1]

    def get_min(self) -> int:
        if not self._min_stack:
            raise StackUnderflowError("Cannot get min from an empty MinStack")
        return self._min_stack[-1]


def evaluate_postfix(tokens: List[str]) -> int:
    """
    Evaluates Reverse Polish Notation (postfix) arithmetic expressions.
    Division truncates towards zero using int(a / b).
    """
    stack: List[int] = []

    for token in tokens:
        if token in {"+", "-", "*", "/"}:
            if len(stack) < 2:
                raise ValueError(f"Insufficient operands for operator '{token}'")
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            elif token == "/":
                if b == 0:
                    raise ZeroDivisionError("Division by zero in postfix expression")
                stack.append(int(a / b))  # Truncates toward zero
        else:
            stack.append(int(token))

    if len(stack) != 1:
        raise ValueError(f"Malformed expression: {len(stack)} operands remaining on stack")

    return stack[0]


if __name__ == "__main__":
    print("=== 1. Generic ArrayStack Operations ===")
    stack = ArrayStack[int]()
    for v in [10, 20, 30]:
        stack.push(v)

    popped_val = stack.pop()
    top_val = stack.peek()
    print(f"ArrayStack Popped: {popped_val}")
    print(f"ArrayStack Top: {top_val}, Current Size: {len(stack)}")
    print(f"ArrayStack Repr: {stack}")

    print("\n=== 2. Balanced Delimiters Validation ===")
    expr1 = "{[a + b] * (c - d)}"
    expr2 = "([)]"
    expr3 = "(()"
    print(f"Expression 1 Balanced: {is_balanced(expr1)}")
    print(f"Expression 2 Balanced: {is_balanced(expr2)}")
    print(f"Expression 3 Balanced: {is_balanced(expr3)}")

    print("\n=== 3. Constant-Time MinStack ===")
    min_s = MinStack()
    min_s.push(5)
    min_s.push(3)
    min_s.push(7)
    min_s.push(2)
    m1 = min_s.get_min()
    print(f"MinStack Initial Min: {m1}")

    popped_item = min_s.pop()  # pops 2
    m2 = min_s.get_min()
    print(f"MinStack Popped {popped_item}, New Min: {m2}")

    print("\n=== 4. Reverse Polish Notation (RPN) Evaluator ===")
    rpn_tokens = ["4", "13", "5", "/", "+"]  # 4 + (13 // 5) = 4 + 2 = 6
    rpn_res = evaluate_postfix(rpn_tokens)
    print(f"Postfix Evaluation Result ({rpn_tokens}): {rpn_res}")

    # Negative truncation toward zero test: 10 / -3 = -3 (not -4)
    neg_rpn = ["10", "-3", "/"]
    print(f"Negative Truncation Result ({neg_rpn}): {evaluate_postfix(neg_rpn)}")

    print("\n=== 5. Underflow Exceptions ===")
    empty_stack = ArrayStack[str]()
    try:
        empty_stack.pop()
    except StackUnderflowError as err:
        print(f"Caught expected underflow: {err}")
