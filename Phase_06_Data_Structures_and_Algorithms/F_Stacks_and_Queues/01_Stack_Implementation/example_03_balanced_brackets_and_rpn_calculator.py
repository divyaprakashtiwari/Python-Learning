"""
Phase 6 - Data Structures and Algorithms
Section F: Stacks and Queues
Topic 01: Stack Implementation
Example 03: Balanced Brackets Validator, Postfix (RPN) Evaluator & Infix-to-Postfix
            (Dijkstra's Shunting-Yard Algorithm)

Three foundational compiler & parser applications of a LIFO Stack:
  1. Valid Parentheses / Balanced Delimiters (LeetCode 20):
     Verifies that every closing bracket `)`, `]`, `}` matches the most recently
     opened unclosed bracket in O(n) time.
  2. Reverse Polish Notation (RPN / Postfix) Expression Evaluator (LeetCode 150):
     Evaluates parenthesis-free postfix tokens in a single left-to-right pass
     using an operand stack, truncating division toward zero as in C/Java/LeetCode.
  3. Dijkstra's Shunting-Yard Algorithm (Infix -> Postfix):
     Converts human-readable infix math (with operator precedence and parentheses)
     into RPN postfix notation using an operator stack.
"""

from typing import Dict, List


def is_valid_parentheses(s: str) -> bool:
    """Checks whether bracket string `s` is properly nested in O(n) time."""
    matching_open: Dict[str, str] = {")": "(", "]": "[", "}": "{"}
    stack: List[str] = []

    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in matching_open:
            if not stack or stack.pop() != matching_open[ch]:
                return False
    return len(stack) == 0


def eval_rpn(tokens: List[str]) -> int:
    """
    Evaluates an arithmetic expression in Reverse Polish Notation (LeetCode 150).
    Division between two integers truncates toward zero (`int(a / b)`).
    """
    stack: List[int] = []
    for token in tokens:
        if token in {"+", "-", "*", "/"}:
            right = stack.pop()
            left = stack.pop()
            if token == "+":
                stack.append(left + right)
            elif token == "-":
                stack.append(left - right)
            elif token == "*":
                stack.append(left * right)
            else:
                # `int(left / right)` truncates toward zero (unlike `left // right` on negatives)
                stack.append(int(left / right))
        else:
            stack.append(int(token))
    return stack[0]


def infix_to_postfix(infix_tokens: List[str]) -> List[str]:
    """
    Converts a list of infix tokens (numbers, `+`, `-`, `*`, `/`, `(`, `)`) into
    Reverse Polish Notation (Postfix) via Dijkstra's Shunting-Yard algorithm.
    """
    precedence: Dict[str, int] = {"+": 1, "-": 1, "*": 2, "/": 2}
    output: List[str] = []
    op_stack: List[str] = []

    for token in infix_tokens:
        if token.lstrip("-").isdigit():
            output.append(token)
        elif token == "(":
            op_stack.append(token)
        elif token == ")":
            while op_stack and op_stack[-1] != "(":
                output.append(op_stack.pop())
            op_stack.pop()  # Discard "("
        elif token in precedence:
            while (
                op_stack
                and op_stack[-1] in precedence
                and precedence[op_stack[-1]] >= precedence[token]
            ):
                output.append(op_stack.pop())
            op_stack.append(token)

    while op_stack:
        output.append(op_stack.pop())

    return output


if __name__ == "__main__":
    print("=" * 72)
    print("1. Balanced Brackets Validator (LeetCode 20)")
    print("=" * 72)
    for sample in ["{[()()]}", "([)]", "((()", "{[]}()"] :
        print(f"  {sample:<12} -> Valid: {is_valid_parentheses(sample)}")

    print("\n" + "=" * 72)
    print("2. Infix -> Postfix (Shunting-Yard) & RPN Evaluation (LeetCode 150)")
    print("=" * 72)

    infix_exprs = [
        ["3", "+", "4", "*", "(", "2", "-", "5", ")"],
        ["10", "+", "6", "/", "(", "9", "-", "3", ")", "*", "-11", "+", "17", "+", "5"],
    ]
    for expr in infix_exprs:
        rpn = infix_to_postfix(expr)
        result = eval_rpn(rpn)
        print(f"Infix  : {' '.join(expr)}")
        print(f"Postfix: {rpn}")
        print(f"Result : {result}\n")

