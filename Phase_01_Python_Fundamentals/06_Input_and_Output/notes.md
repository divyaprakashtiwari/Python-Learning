# Topic 06: Input and Output

---

## 1. Introduction

Every useful program interacts with the outside world: it reads **Input** (from a user's keyboard, piped standard input, or command-line feeds) and produces **Output** (formatted text, tables, logs, or answers printed to the console).

In Python:
- **`input(prompt)`** pauses execution, waits for the user to type a line of text and press `Enter`, and returns that line as a **string (`str`)**.
- **`print(*objects, sep=' ', end='\n')`** converts one or more values to strings and writes them to standard output (`sys.stdout`).

---

## 2. Why is it used?

Mastering Input and Output is crucial for two major reasons:
1. **Competitive Programming & Online Coding Assessments (LeetCode, HackerRank, Codeforces):** Many coding platforms feed test cases via `stdin` (such as `5 10 20` on a single line) and judge your solution by matching exact `stdout` formatting.
2. **Production CLI Tools & Reporting:** Backend scripts, financial reports, and terminal dashboards rely on **f-strings** (`f"{value:>10.2f}"`) to align columns, format currency, and log debug expressions cleanly.

---

## 3. Syntax

```python
# 1. Reading Input
name = input("Enter your name: ").strip()
age = int(input("Enter your age: "))

# Reading multiple space-separated integers on one line
n, k = map(int, input().split())
arr = list(map(int, input().split()))

# 2. Printing Output with sep and end
print("A", "B", "C", sep=" -> ", end="\n")

# 3. f-String Formatting (Python 3.6+)
price = 1499.5
print(f"Price: Rs.{price:,.2f} | Right-aligned: {price:>10.2f}")
```

---

## 4. Explanation (Step-by-Step Breakdown)

1. **`input()` Always Returns `str`:** Even if the user types `42`, `input()` returns `"42"` (without the trailing newline `\n`). Always wrap `input()` in `int()` or `float()` when reading numbers.
2. **Parsing Space-Separated Values (`input().split()`):**
   - Suppose the input line is `"10 20 30"`.
   - `input().split()` splits on whitespace into `["10", "20", "30"]`.
   - `map(int, ...)` applies `int()` to each string lazily.
   - You can unpack directly (`a, b, c = map(int, input().split())`) or wrap in `list(...)`.
3. **f-String Format Specifiers (`{value : [fill][align][width][,][.precision][type]}`):**
   - `<20` : Left-align within 20 characters.
   - `>10` : Right-align within 10 characters.
   - `^30` : Center-align within 30 characters.
   - `,.2f` : Use comma thousand separators and 2 decimal places.
   - `{x=}` : Prints both the variable name/expression and its value (`x=10`).

---

## 5. Examples

All three runnable examples are located in this folder:
- [`example_01_print_parameters_and_fstrings.py`](example_01_print_parameters_and_fstrings.py)
- [`example_02_simulated_console_input_parsing.py`](example_02_simulated_console_input_parsing.py)
- [`example_03_tabular_receipt_formatter.py`](example_03_tabular_receipt_formatter.py)

### Example 1: Mastering `print()` Parameters (`sep`, `end`) and f-Strings (`example_01_print_parameters_and_fstrings.py`)

```python
def main() -> None:
    print("=== 1. Custom sep and end in print() ===")
    print("2026", "11", "01", sep="-")
    print(" Phase_01", "06_Input_and_Output", "notes.md", sep="/")
    print("Loading modules", end="... ")
    print("Done!")

    population = 1_428_627_663
    accuracy = 0.987654
    items = 12
    unit_cost = 250

    print("\n=== 2. Modern f-String Formatting ===")
    print(f"Formatted Population : {population:,}")
    print(f"Accuracy (2 decimals): {accuracy:.2f}")
    print(f"Accuracy (percentage): {accuracy:.2%}")
    print(f"Debug Expression     : {items=}, {unit_cost=}, {items * unit_cost=}")


if __name__ == "__main__":
    main()
```

### Example 2: Reading Single and Space-Separated Inputs (`example_02_simulated_console_input_parsing.py`)

```python
import io
import sys


def process_student_inputs() -> None:
    full_name = input().strip()
    age, grad_year = map(int, input().split())
    scores = list(map(float, input().split()))
    avg_score = sum(scores) / len(scores)

    print("=== Parsed Standard Input Summary ===")
    print(f"Student Name    : {full_name}")
    print(f"Age & Grad Year : {age} years old | Class of {grad_year}")
    print(f"Scores          : {scores}")
    print(f"Average Score   : {avg_score:.2f}")


def main() -> None:
    simulated_stdin = "Divya Prakash Tiwari\n21 2027\n88.5 92.0 95.5 89.0\n"
    original_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(simulated_stdin)
        process_student_inputs()
    finally:
        sys.stdin = original_stdin


if __name__ == "__main__":
    main()
```

### Example 3: Real-World Tabular Receipt Formatter (`example_03_tabular_receipt_formatter.py`)

```python
def print_bookstore_receipt() -> None:
    cart = [
        ("Fluent Python (2nd Ed)", 1, 1450.00),
        ("Introduction to Algorithms", 1, 1899.50),
        ("Coding Interview Notebook", 3, 120.00),
    ]

    border = "=" * 54
    divider = "-" * 54

    print(border)
    print(f"{'PYTHON LEARNING BOOKSTORE':^54}")
    print(border)
    print(f"{'Item Description':<28} {'Qty':^5} {'Unit':>9} {'Total':>9}")
    print(divider)

    subtotal = 0.0
    for title, qty, unit_price in cart:
        line_total = qty * unit_price
        subtotal += line_total
        print(f"{title:<28} {qty:^5} {unit_price:>9.2f} {line_total:>9.2f}")

    print(divider)
    gst = subtotal * 0.18
    grand_total = subtotal + gst
    print(f"{'Subtotal':<43} {subtotal:>10.2f}")
    print(f"{'GST (18%)':<43} {gst:>10.2f}")
    print(border)
    print(f"{'GRAND TOTAL (INR)':<43} {grand_total:>10.2f}")
    print(border)


if __name__ == "__main__":
    print_bookstore_receipt()
```

---

## 6. Output

### Output for Example 1:
```text
=== 1. Custom sep and end in print() ===
2026-11-01
 Phase_01/06_Input_and_Output/notes.md
Loading modules... Done!

=== 2. Modern f-String Formatting ===
Formatted Population : 1,428,627,663
Accuracy (2 decimals): 0.99
Accuracy (percentage): 98.77%
Debug Expression     : items=12, unit_cost=250, items * unit_cost=3000
```

### Output for Example 2:
```text
=== Parsed Standard Input Summary ===
Student Name    : Divya Prakash Tiwari
Age & Grad Year : 21 years old | Class of 2027
Scores          : [88.5, 92.0, 95.5, 89.0]
Average Score   : 91.25
```

### Output for Example 3:
```text
======================================================
              PYTHON LEARNING BOOKSTORE               
======================================================
Item Description              Qty       Unit     Total
------------------------------------------------------
Fluent Python (2nd Ed)         1     1450.00   1450.00
Introduction to Algorithms     1     1899.50   1899.50
Coding Interview Notebook      3      120.00    360.00
------------------------------------------------------
Subtotal                                       3709.50
GST (18%)                                       667.71
======================================================
GRAND TOTAL (INR)                              4377.21
======================================================
```

---

## 7. Code Explanation

- **`print("Loading modules", end="... ")`** — By default, `print()` ends with `end="\n"` (a newline). Overriding `end="... "` keeps the cursor on the same line so the next `print("Done!")` appears right beside it.
- **`f"{accuracy:.2%}"`** — The `%` format specifier automatically multiplies a ratio by `100` and appends a `%` sign (`0.987654 -> 98.77%`).
- **`f"{items * unit_cost=}"`** — Introduced in Python 3.8, the `=` specifier inside an f-string prints the literal expression followed by its evaluated result (`items * unit_cost=3000`), which is a huge time-saver when debugging.

---

## 8. Common Mistakes

1. **Forgetting `.split()` When Reading Multiple Numbers on One Line:**
   Writing `a, b = int(input())` when the user enters `"10 20"` raises `ValueError: invalid literal for int() with base 10: '10 20'`. Always use `a, b = map(int, input().split())`.
2. **Using `split(" ")` Instead of `split()`:**
   `input().split(" ")` fails if there are two consecutive spaces between numbers (`"10  20" -> ["10", "", "20"]`). Calling `.split()` with no arguments automatically collapses any amount of whitespace and strips leading/trailing spaces.
3. **Concatenating Numbers inside `print()` with `+`:**
   Writing `print("Score: " + 95)` raises a `TypeError`. Use an f-string (`print(f"Score: {95}")`) or comma-separated arguments (`print("Score:", 95)`).

---

## 9. Practice Questions

1. **Easy:** Write a program that takes three words and prints them separated by `" | "` and ending with `" [END]\n"` using `print()`'s `sep` and `end` parameters.
2. **Medium:** Given a single input string `"10 25 30 45 60"`, parse the integers using `map(int, line.split())` and print their count, sum, minimum, maximum, and mean formatted to 2 decimal places.
3. **Hard:** Write a function `format_leaderboard(players: list[tuple[str, int, float]])` that prints a 3-column table (`Rank`, `Player Name`, `Win Rate %`) with properly aligned headers and zero-padded rank numbers (`#01`, `#02`, `#03`).

---

## 10. Interview Questions

### Q1: In competitive programming with massive inputs (`10^6` lines), why is `sys.stdin.readline` faster than `input()`?
**Answer:** `input()` strips the trailing newline, checks for prompts, and handles additional high-level wrapper checks on every call. `sys.stdin.readline()` reads directly from the underlying C buffer with minimal overhead, often running 3x–5x faster on million-line inputs.

### Q2: Why are f-strings (`f"..."`) preferred over `%` formatting and `str.format()`?
**Answer:** f-strings (PEP 498) are evaluated at runtime by compiling directly into efficient `FORMAT_VALUE` and `BUILD_STRING` bytecode instructions. They are both faster to execute and much easier to read than `%` formatting or `.format()`.

### Q3: What does the `flush=True` parameter in `print(..., flush=True)` do?
**Answer:** Standard output is normally buffered in memory (often until a newline is encountered). Setting `flush=True` forces Python to immediately write the output buffer to the terminal or log stream, which is critical for real-time progress bars (`end="\r"`) and Docker container logs.
