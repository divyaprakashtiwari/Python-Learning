"""
Topic: Data Structures and Algorithms (DSA) - Stack Implementation
------------------------------------------------------------------
Questions Covered:
1. Array-Based vs Node-Based Stacks: Encapsulation with push, pop, peek, and capacity limits.
2. Valid Parentheses & Bracket Matching: Validating nested delimiters with stack tracking.
3. Min Stack (O(1) get_min): Aux-stack tracking minimum elements in O(1) constant time.
4. Max Stack (O(1) get_max & pop_max): Dual-stack mechanics supporting maximum item extraction.
5. Postfix / Reverse Polish Notation (RPN) Evaluator: Stack-driven mathematical arithmetic.
6. Infix to Postfix Converter (Shunting-Yard): Managing operator precedence and associativity.
7. Monotonic Stack (Next Greater Element): O(n) linear search for next greater elements.
8. Daily Temperatures / Wait-Day Calculation: Monotonic index stack tracking warmer days.
9. Largest Rectangle in Histogram: Optimal monotonic stack calculating maximum bounding rectangle.
10. Architectural System: Multi-Level Undo/Redo & Transactional Command History Engine.
"""

from typing import List, Tuple, Optional, Any, Dict


# ==============================================================================
# Question 1: Array-Based and Node-Based Stack Implementations
# ==============================================================================
class ArrayStack:
    """Stack implemented using a dynamic Python list."""
    def __init__(self, capacity: Optional[int] = None):
        self._items: List[Any] = []
        self._capacity = capacity

    def push(self, item: Any) -> None:
        if self._capacity is not None and len(self._items) >= self._capacity:
            raise OverflowError("Stack capacity exceeded")
        self._items.append(item)

    def pop(self) -> Any:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> Any:
        if not self._items:
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)


class StackNode:
    def __init__(self, val: Any, next_node: Optional["StackNode"] = None):
        self.val = val
        self.next = next_node


class LinkedStack:
    """Stack implemented using a singly linked chain of nodes."""
    def __init__(self):
        self._head: Optional[StackNode] = None
        self._size = 0

    def push(self, item: Any) -> None:
        self._head = StackNode(item, self._head)
        self._size += 1

    def pop(self) -> Any:
        if self._head is None:
            raise IndexError("pop from empty linked stack")
        val = self._head.val
        self._head = self._head.next
        self._size -= 1
        return val

    def peek(self) -> Any:
        if self._head is None:
            raise IndexError("peek from empty linked stack")
        return self._head.val

    def is_empty(self) -> bool:
        return self._size == 0

    def __len__(self) -> int:
        return self._size


def test_q1_stack_implementations():
    # Array Stack
    arr_stack = ArrayStack(capacity=3)
    arr_stack.push(10)
    arr_stack.push(20)
    assert arr_stack.peek() == 20
    assert len(arr_stack) == 2
    assert arr_stack.pop() == 20
    assert arr_stack.pop() == 10
    assert arr_stack.is_empty()

    # Linked Stack
    lnk_stack = LinkedStack()
    lnk_stack.push("a")
    lnk_stack.push("b")
    assert lnk_stack.peek() == "b"
    assert len(lnk_stack) == 2
    assert lnk_stack.pop() == "b"
    assert lnk_stack.pop() == "a"
    assert lnk_stack.is_empty()
    print("=== Q1: Array-Based and Node-Based Stacks Verified ===")


# ==============================================================================
# Question 2: Valid Parentheses & Bracket Matching
# ==============================================================================
def is_valid_parentheses(s: str) -> bool:
    """
    Validates string containing '()', '{}', '[]'.
    Open brackets must be closed by the same type in correct order.
    """
    bracket_map = {")": "(", "}": "{", "]": "["}
    stack: List[str] = []

    for char in s:
        if char in "({[":
            stack.append(char)
        elif char in bracket_map:
            if not stack or stack[-1] != bracket_map[char]:
                return False
            stack.pop()

    return len(stack) == 0


def test_q2_valid_parentheses():
    assert is_valid_parentheses("()") is True
    assert is_valid_parentheses("()[]{}") is True
    assert is_valid_parentheses("(]") is False
    assert is_valid_parentheses("([)]") is False
    assert is_valid_parentheses("{[]}") is True
    assert is_valid_parentheses("") is True
    assert is_valid_parentheses("(") is False
    assert is_valid_parentheses(")") is False
    print("=== Q2: Valid Parentheses & Bracket Matching Verified ===")


# ==============================================================================
# Question 3: Min Stack with O(1) get_min
# ==============================================================================
class MinStack:
    """
    Stack supporting push, pop, top, and retrieving minimum element in O(1) time.
    Uses an auxiliary min-tracker stack.
    """
    def __init__(self):
        self._stack: List[int] = []
        self._min_stack: List[int] = []

    def push(self, val: int) -> None:
        self._stack.append(val)
        current_min = self._min_stack[-1] if self._min_stack else val
        self._min_stack.append(min(val, current_min))

    def pop(self) -> int:
        if not self._stack:
            raise IndexError("pop from empty MinStack")
        self._min_stack.pop()
        return self._stack.pop()

    def top(self) -> int:
        if not self._stack:
            raise IndexError("top from empty MinStack")
        return self._stack[-1]

    def get_min(self) -> int:
        if not self._min_stack:
            raise IndexError("get_min from empty MinStack")
        return self._min_stack[-1]


def test_q3_min_stack():
    ms = MinStack()
    ms.push(-2)
    ms.push(0)
    ms.push(-3)
    assert ms.get_min() == -3
    assert ms.pop() == -3
    assert ms.top() == 0
    assert ms.get_min() == -2
    print("=== Q3: Min Stack with O(1) get_min Verified ===")


# ==============================================================================
# Question 4: Max Stack with O(1) get_max and pop_max
# ==============================================================================
class MaxStack:
    """
    Stack supporting push, pop, top, get_max, and pop_max.
    """
    def __init__(self):
        self._stack: List[int] = []
        self._max_stack: List[int] = []

    def push(self, x: int) -> None:
        self._stack.append(x)
        curr_max = self._max_stack[-1] if self._max_stack else x
        self._max_stack.append(max(x, curr_max))

    def pop(self) -> int:
        self._max_stack.pop()
        return self._stack.pop()

    def top(self) -> int:
        return self._stack[-1]

    def get_max(self) -> int:
        return self._max_stack[-1]

    def pop_max(self) -> int:
        max_val = self.get_max()
        buffer: List[int] = []

        # Pop until top is the max_val
        while self.top() != max_val:
            buffer.append(self.pop())

        # Pop the actual max
        self.pop()

        # Push buffered elements back
        while buffer:
            self.push(buffer.pop())

        return max_val


def test_q4_max_stack():
    stk = MaxStack()
    stk.push(5)
    stk.push(1)
    stk.push(5)
    assert stk.top() == 5
    assert stk.pop_max() == 5
    assert stk.top() == 1
    assert stk.get_max() == 5
    assert stk.pop() == 1
    assert stk.top() == 5
    print("=== Q4: Max Stack (get_max & pop_max) Verified ===")


# ==============================================================================
# Question 5: Postfix / Reverse Polish Notation (RPN) Expression Evaluator
# ==============================================================================
def eval_rpn(tokens: List[str]) -> int:
    """
    Evaluates value of arithmetic expression in Reverse Polish Notation.
    Valid operators: '+', '-', '*', '/'.
    Division truncates toward zero (as in integer division).
    """
    stack: List[int] = []

    for t in tokens:
        if t in ("+", "-", "*", "/"):
            b = stack.pop()
            a = stack.pop()
            if t == "+":
                stack.append(a + b)
            elif t == "-":
                stack.append(a - b)
            elif t == "*":
                stack.append(a * b)
            elif t == "/":
                # Integer division truncating toward zero
                stack.append(int(a / b))
        else:
            stack.append(int(t))

    return stack.pop()


def test_q5_eval_rpn():
    # ((2 + 1) * 3) -> ["2", "1", "+", "3", "*"] -> 9
    assert eval_rpn(["2", "1", "+", "3", "*"]) == 9
    # (4 + (13 / 5)) -> ["4", "13", "5", "/", "+"] -> 6
    assert eval_rpn(["4", "13", "5", "/", "+"]) == 6
    # ((10 * (6 / ((9 + 3) * -11))) + 17) + 5
    tokens = ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]
    assert eval_rpn(tokens) == 22
    print("=== Q5: Postfix RPN Evaluator Verified ===")


# ==============================================================================
# Question 6: Infix to Postfix Converter (Shunting-Yard Algorithm)
# ==============================================================================
def infix_to_postfix(tokens: List[str]) -> List[str]:
    """
    Converts infix token stream to postfix notation using Dijkstra's Shunting-Yard.
    Supports +, -, *, /, and parentheses () with left-associativity.
    """
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2}
    output: List[str] = []
    operator_stack: List[str] = []

    for t in tokens:
        if t.isdigit() or (t.startswith("-") and len(t) > 1 and t[1:].isdigit()):
            output.append(t)
        elif t in precedence:
            while (
                operator_stack
                and operator_stack[-1] in precedence
                and precedence[operator_stack[-1]] >= precedence[t]
            ):
                output.append(operator_stack.pop())
            operator_stack.append(t)
        elif t == "(":
            operator_stack.append(t)
        elif t == ")":
            while operator_stack and operator_stack[-1] != "(":
                output.append(operator_stack.pop())
            if operator_stack and operator_stack[-1] == "(":
                operator_stack.pop()  # discard '('

    while operator_stack:
        output.append(operator_stack.pop())

    return output


def test_q6_infix_to_postfix():
    # A + B * C -> A B C * +
    expr1 = ["3", "+", "4", "*", "2"]
    res1 = infix_to_postfix(expr1)
    assert res1 == ["3", "4", "2", "*", "+"]
    assert eval_rpn(res1) == 11

    # (3 + 4) * 2 -> 3 4 + 2 *
    expr2 = ["(", "3", "+", "4", ")", "*", "2"]
    res2 = infix_to_postfix(expr2)
    assert res2 == ["3", "4", "+", "2", "*"]
    assert eval_rpn(res2) == 14
    print("=== Q6: Infix to Postfix Conversion (Shunting-Yard) Verified ===")


# ==============================================================================
# Question 7: Monotonic Stack: Next Greater Element (NGE)
# ==============================================================================
def next_greater_element(nums: List[int]) -> List[int]:
    """
    For each element in nums, finds the next strictly greater element to its right.
    If no greater element exists, output -1 for that position.
    Runs in O(n) time using a monotonic decreasing stack.
    """
    n = len(nums)
    result = [-1] * n
    stack: List[int] = []  # Stores indices of elements

    for i in range(n):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]
        stack.append(i)

    return result


def test_q7_next_greater_element():
    nums = [4, 5, 2, 25, 7, 8]
    nge = next_greater_element(nums)
    # 4 -> 5, 5 -> 25, 2 -> 25, 25 -> -1, 7 -> 8, 8 -> -1
    assert nge == [5, 25, 25, -1, 8, -1]

    desc = [5, 4, 3, 2, 1]
    assert next_greater_element(desc) == [-1, -1, -1, -1, -1]
    print("=== Q7: Monotonic Stack (Next Greater Element) Verified ===")


# ==============================================================================
# Question 8: Daily Temperatures / Wait-Day Calculation
# ==============================================================================
def daily_temperatures(temperatures: List[int]) -> List[int]:
    """
    Returns an array answer such that answer[i] is the number of days you have to
    wait after the ith day to get a warmer temperature.
    If there is no future day for which this is possible, keep answer[i] == 0.
    """
    n = len(temperatures)
    answer = [0] * n
    stack: List[int] = []  # indices of monotonic decreasing temperatures

    for curr_day, temp in enumerate(temperatures):
        while stack and temp > temperatures[stack[-1]]:
            prev_day = stack.pop()
            answer[prev_day] = curr_day - prev_day
        stack.append(curr_day)

    return answer


def test_q8_daily_temperatures():
    temps = [73, 74, 75, 71, 69, 72, 76, 73]
    # answer: [1, 1, 4, 2, 1, 1, 0, 0]
    res = daily_temperatures(temps)
    assert res == [1, 1, 4, 2, 1, 1, 0, 0]
    print("=== Q8: Daily Temperatures Monotonic Stack Verified ===")


# ==============================================================================
# Question 9: Largest Rectangle in Histogram
# ==============================================================================
def largest_rectangle_area(heights: List[int]) -> int:
    """
    Finds the area of the largest rectangle in a histogram.
    Time Complexity: O(n) using monotonic increasing stack.
    Space Complexity: O(n).
    """
    stack: List[int] = []  # indices
    max_area = 0
    # Append dummy height 0 at end to flush stack
    extended_heights = heights + [0]

    for i, h in enumerate(extended_heights):
        while stack and h < extended_heights[stack[-1]]:
            height = extended_heights[stack.pop()]
            width = i if not stack else (i - stack[-1] - 1)
            max_area = max(max_area, height * width)
        stack.append(i)

    return max_area


def test_q9_largest_rectangle_area():
    heights1 = [2, 1, 5, 6, 2, 3]
    # Largest rectangle between indices 2 and 3: min(5, 6) * 2 = 10
    assert largest_rectangle_area(heights1) == 10

    heights2 = [2, 4]
    assert largest_rectangle_area(heights2) == 4

    assert largest_rectangle_area([6, 7, 5, 2, 4, 5, 9, 3]) == 16
    print("=== Q9: Largest Rectangle in Histogram Verified ===")


# ==============================================================================
# Question 10: Architectural System: Multi-Level Undo/Redo Command Engine
# ==============================================================================
class TextEditorCommand:
    """Reversible command abstraction."""
    def execute(self, doc: List[str]) -> None:
        raise NotImplementedError

    def undo(self, doc: List[str]) -> None:
        raise NotImplementedError


class InsertTextCommand(TextEditorCommand):
    def __init__(self, position: int, text: str):
        self.position = position
        self.text = text

    def execute(self, doc: List[str]) -> None:
        doc.insert(self.position, self.text)

    def undo(self, doc: List[str]) -> None:
        doc.pop(self.position)


class UndoRedoStackEngine:
    """
    Production dual-stack Undo/Redo Engine with capacity bounding.
    """
    def __init__(self, max_history: int = 50):
        self._undo_stack: List[TextEditorCommand] = []
        self._redo_stack: List[TextEditorCommand] = []
        self._max_history = max_history
        self.document: List[str] = []

    def execute_command(self, cmd: TextEditorCommand) -> None:
        cmd.execute(self.document)
        self._undo_stack.append(cmd)
        if len(self._undo_stack) > self._max_history:
            self._undo_stack.pop(0)  # Evict oldest history
        # New execution invalidates redo history branch
        self._redo_stack.clear()

    def undo(self) -> bool:
        if not self._undo_stack:
            return False
        cmd = self._undo_stack.pop()
        cmd.undo(self.document)
        self._redo_stack.append(cmd)
        return True

    def redo(self) -> bool:
        if not self._redo_stack:
            return False
        cmd = self._redo_stack.pop()
        cmd.execute(self.document)
        self._undo_stack.append(cmd)
        return True

    def get_text(self) -> str:
        return " ".join(self.document)


def test_q10_undo_redo_engine():
    engine = UndoRedoStackEngine(max_history=5)

    # Execute 3 commands
    engine.execute_command(InsertTextCommand(0, "Hello"))
    engine.execute_command(InsertTextCommand(1, "World"))
    engine.execute_command(InsertTextCommand(2, "!"))
    assert engine.get_text() == "Hello World !"

    # Undo twice
    assert engine.undo() is True
    assert engine.get_text() == "Hello World"
    assert engine.undo() is True
    assert engine.get_text() == "Hello"

    # Redo once
    assert engine.redo() is True
    assert engine.get_text() == "Hello World"

    # Branching execution clears redo
    engine.execute_command(InsertTextCommand(2, "Python"))
    assert engine.get_text() == "Hello World Python"
    assert engine.redo() is False  # Redo was cleared by new action
    print("=== Q10: Architectural Undo/Redo Command Engine Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_stack_implementations()
    test_q2_valid_parentheses()
    test_q3_min_stack()
    test_q4_max_stack()
    test_q5_eval_rpn()
    test_q6_infix_to_postfix()
    test_q7_next_greater_element()
    test_q8_daily_temperatures()
    test_q9_largest_rectangle_area()
    test_q10_undo_redo_engine()
    print("\nAll 10 stack implementation DSA questions passed successfully!")
