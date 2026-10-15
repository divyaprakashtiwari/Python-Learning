"""
Topic 01: Python Basics
Question 06: Input and Output

Master Python's input/output operations: print formatting,
user input handling, stdin/stdout, and output redirection.
"""

# ============================================================
# Q1: print() function parameters
# ============================================================
# Question: Explore all parameters of print(): sep, end, file, flush.

print("=== Q1: print() Parameters ===")

# Default behavior
print("  Hello", "World")  # space separated, newline at end

# Custom separator
print("  2024", "10", "15", sep="-")           # 2024-10-15
print("  /home", "user", "docs", sep="/")      # /home/user/docs

# Custom end
print("  Loading", end="")
print(".", end="")
print(".", end="")
print(". done!")

# Printing to a string (using file parameter)
import io
buffer = io.StringIO()
print("captured output", file=buffer)
print(f"  Captured: {buffer.getvalue()!r}")

# flush parameter (useful for real-time output)
import sys
print("  Real-time output:", end=" ", flush=True)
print("flushed immediately")

# Explanation: print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)
# sep controls what goes between items, end controls line ending.
# file redirects output to any file-like object.
# flush=True forces immediate output (useful in loops/progress bars).


# ============================================================
# Q2: Input handling and validation
# ============================================================
# Question: Demonstrate safe input handling with type validation.
# Since this is non-interactive, simulate input.

print("\n=== Q2: Input Handling and Validation ===")

# Simulating input for demonstration (replace with actual input() for interactive use)
def get_validated_input(prompt, validator, error_msg="Invalid input", max_attempts=3):
    """Get and validate user input with retry logic.

    In production, replace simulated_inputs with actual input() calls.
    """
    # Simulated inputs for demonstration
    simulated_inputs = iter(["abc", "-5", "25"])

    for attempt in range(1, max_attempts + 1):
        try:
            user_input = next(simulated_inputs)  # Replace with input(prompt)
            print(f"  [Simulated input: {user_input!r}]")
            value = validator(user_input)
            return value
        except (ValueError, StopIteration) as e:
            print(f"  Attempt {attempt}/{max_attempts}: {error_msg} ({e})")

    return None

def validate_age(text):
    """Validate that input is a positive integer between 1-150."""
    age = int(text)
    if not 1 <= age <= 150:
        raise ValueError(f"{age} not in range 1-150")
    return age

result = get_validated_input("Enter age: ", validate_age, "Please enter age 1-150")
print(f"  Validated age: {result}")

# Explanation: Always validate user input! input() returns a string,
# so you must convert and validate. Use a retry loop with a maximum
# number of attempts. Separate validation logic into functions.


# ============================================================
# Q3: String formatting for output tables
# ============================================================
# Question: Create well-formatted tabular output using string formatting.

print("\n=== Q3: Formatted Tables ===")

# Student grade table
students = [
    ("Divya", 95, 88, 92),
    ("Amit", 78, 85, 90),
    ("Priya", 100, 97, 95),
    ("Rahul", 65, 72, 68),
]

# Header
print(f"  {'Name':<10} {'Math':>6} {'Sci':>6} {'Eng':>6} {'Avg':>7} {'Grade':>6}")
print(f"  {'-'*10} {'-'*6} {'-'*6} {'-'*6} {'-'*7} {'-'*6}")

for name, math_s, sci, eng in students:
    avg = (math_s + sci + eng) / 3
    grade = "A" if avg >= 90 else "B" if avg >= 80 else "C" if avg >= 70 else "F"
    print(f"  {name:<10} {math_s:>6} {sci:>6} {eng:>6} {avg:>7.1f} {grade:>6}")

# Footer
totals = [sum(s[i] for s in students) for i in range(1, 4)]
print(f"  {'-'*10} {'-'*6} {'-'*6} {'-'*6} {'-'*7}")
print(f"  {'Average':<10} {totals[0]/len(students):>6.1f} "
      f"{totals[1]/len(students):>6.1f} {totals[2]/len(students):>6.1f}")

# Explanation: f-string format specs: <(left), >(right), ^(center) for alignment.
# Width is specified as a number. .1f means 1 decimal place float.
# This creates clean, aligned columns without external libraries.


# ============================================================
# Q4: repr() vs str() -- developer vs user output
# ============================================================
# Question: Explain the difference between repr() and str()
# and when to use each.

print("\n=== Q4: repr() vs str() ===")

text = "Hello\nWorld"
print(f"  str(text):  {str(text)}")     # Human-readable
print(f"  repr(text): {repr(text)}")    # Developer-friendly

# Key differences
values = [42, 3.14, "hello", [1, 2], None, True]
print(f"\n  {'Value':<15} {'str()':<15} {'repr()':<15}")
for val in values:
    print(f"  {str(val):<15} {str(val):<15} {repr(val):<15}")

# In f-strings: !s for str(), !r for repr()
name = "Divya"
print(f"\n  f'{{name}}':   {name}")
print(f"  f'{{name!s}}': {name!s}")
print(f"  f'{{name!r}}': {name!r}")

# Custom class example
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

p = Point(3, 4)
print(f"\n  str(Point):  {p}")       # (3, 4)
print(f"  repr(Point): {p!r}")      # Point(3, 4)

# Explanation: str() is for end-user display (human-readable).
# repr() is for developers (unambiguous, often valid Python code).
# str("hello") returns hello, repr("hello") returns 'hello' (with quotes).
# Rule: repr() output should ideally be valid Python to recreate the object.


# ============================================================
# Q5: Formatted number output
# ============================================================
# Question: Format numbers for display: currency, percentages,
# scientific notation, padding, sign control.

print("\n=== Q5: Number Formatting ===")

# Currency formatting
amount = 1234567.89
print(f"  Currency:      ${amount:,.2f}")
print(f"  Indian style:  {amount:,.2f}")  # Standard comma grouping

# Percentage
ratio = 0.8567
print(f"  Percentage:    {ratio:.1%}")    # 85.7%

# Scientific notation
big = 602214076000000000000000
print(f"  Scientific:    {big:.3e}")      # 6.022e+23

# Padding and sign
for num in [-42, 0, 42]:
    print(f"  {num:+6d}  |  {num:06d}  |  {num: d}")
    #       +sign     zero-pad     space for positive

# Binary, octal, hex
n = 255
print(f"\n  Dec: {n:>5d}  Bin: {n:>10b}  Oct: {n:>5o}  Hex: {n:>4x}")

# Dynamic width
for width in [10, 20, 30]:
    print(f"  {'*' * width:>{width}}")

# Explanation: Format spec: [[fill]align][sign][#][0][width][grouping][.precision][type]
# Types: d(int), f(float), e(scientific), %(percent), b(binary), x(hex)
# Sign options: +(always), -(negative only, default), (space for positive)
# Grouping: ,(comma) or _(underscore) for thousand separators


# ============================================================
# Q6: Multi-line output and text wrapping
# ============================================================
# Question: Create formatted multi-line output: boxes, banners,
# and wrapped text.

print("\n=== Q6: Multi-line Output Formatting ===")

import textwrap

# Box drawing
def print_box(text, width=40):
    """Print text in an ASCII box."""
    lines = text.split('\n')
    print(f"  +{'-' * (width - 2)}+")
    for line in lines:
        print(f"  | {line:<{width - 4}} |")
    print(f"  +{'-' * (width - 2)}+")

print_box("Welcome to Python!\nLearn. Code. Create.")

# Text wrapping
long_text = ("Python is a high-level, general-purpose programming language. "
             "Its design philosophy emphasizes code readability with the use of "
             "significant indentation. Python is dynamically typed and garbage-collected.")

wrapped = textwrap.fill(long_text, width=50, initial_indent="  ", subsequent_indent="  ")
print(f"\n  Wrapped text (50 chars wide):")
print(wrapped)

# Dedent
indented = """\
    This text is indented
    in source code but
    should not be in output
"""
print(f"  Dedented:")
print(textwrap.dedent(indented))

# Explanation: textwrap.fill() wraps text to a given width.
# textwrap.dedent() removes common leading whitespace.
# Box-drawing creates professional-looking CLI output.


# ============================================================
# Q7: Progress bar simulation
# ============================================================
# Question: Create a text-based progress bar using print().

import time

print("=== Q7: Progress Bar ===")

def progress_bar(iteration, total, length=30, prefix="  Progress"):
    """Display a text progress bar."""
    percent = iteration / total
    filled = int(length * percent)
    bar = '#' * filled + '-' * (length - filled)
    print(f"\r{prefix} |{bar}| {percent:.0%} ({iteration}/{total})", end='', flush=True)
    if iteration == total:
        print()  # New line at completion

# Simulate a task
total = 20
for i in range(total + 1):
    progress_bar(i, total)
    time.sleep(0.02)  # Shortened for demo

# Simple spinner
spinners = ['|', '/', '-', '\\']
print("  Spinner demo: ", end="")
for i in range(12):
    print(f"\r  Spinner demo: {spinners[i % 4]}", end="", flush=True)
    time.sleep(0.05)
print("\r  Spinner demo: Done!")

# Explanation: \r (carriage return) moves the cursor to the start of
# the line without a newline, allowing us to overwrite the previous output.
# flush=True ensures the output appears immediately (not buffered).
# This creates smooth progress bars and spinners in the terminal.


# ============================================================
# Q8: Pretty printing with pprint
# ============================================================
# Question: Use pprint for readable output of complex data structures.

from pprint import pprint, pformat

print("\n=== Q8: Pretty Printing ===")

complex_data = {
    "users": [
        {"name": "Divya", "age": 21, "skills": ["Python", "SQL", "Git"]},
        {"name": "Amit", "age": 25, "skills": ["Java", "Spring", "Docker"]},
    ],
    "metadata": {
        "total": 2,
        "page": 1,
        "filters": {"active": True, "verified": True},
    },
}

print("  Regular print:")
print(f"  {complex_data}")

print("\n  Pretty print:")
# pprint with indent and width control
pprint(complex_data, indent=2, width=60)

# pformat returns a string instead of printing
formatted = pformat(complex_data, indent=2, width=50)
print(f"\n  pformat length: {len(formatted)} chars")

# Explanation: pprint formats nested data structures with proper
# indentation and line wrapping. pformat() returns the formatted
# string instead of printing it. Use width to control line length
# and indent to set nesting indentation.


# ============================================================
# Q9: Logging output (preview of logging module)
# ============================================================
# Question: Create a simple logging system to understand
# the concept before the logging module.

print("\n=== Q9: Simple Logging System ===")

import datetime

class SimpleLogger:
    """A basic logging system demonstrating output formatting."""

    LEVELS = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}

    def __init__(self, name, min_level="INFO"):
        self.name = name
        self.min_level = self.LEVELS.get(min_level, 1)

    def _log(self, level, message):
        if self.LEVELS.get(level, 0) >= self.min_level:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"  [{timestamp}] {level:<7} [{self.name}] {message}")

    def debug(self, msg): self._log("DEBUG", msg)
    def info(self, msg): self._log("INFO", msg)
    def warning(self, msg): self._log("WARNING", msg)
    def error(self, msg): self._log("ERROR", msg)

log = SimpleLogger("App", min_level="INFO")
log.debug("This won't show (below min level)")
log.info("Application started")
log.warning("Disk space low")
log.error("Connection failed")

# Change log level
log.min_level = SimpleLogger.LEVELS["DEBUG"]
log.debug("Now this shows!")

# Explanation: This previews concepts from Python's logging module.
# Key ideas: log levels filter what's displayed, timestamps provide
# context, and a consistent format makes logs parseable.


# ============================================================
# Q10: Building a formatted report generator
# ============================================================
# Question: Create a complete report generator combining all
# output techniques learned.

print("\n=== Q10: Report Generator ===")

def generate_report(title, data, show_summary=True):
    """Generate a formatted report from data."""
    width = 60

    # Title banner
    print(f"\n  {'=' * width}")
    print(f"  {title:^{width}}")
    print(f"  {'=' * width}")

    # Column headers
    headers = ["Product", "Units", "Price", "Total"]
    print(f"  {headers[0]:<20} {headers[1]:>8} {headers[2]:>10} {headers[3]:>12}")
    print(f"  {'-'*20} {'-'*8} {'-'*10} {'-'*12}")

    # Data rows
    grand_total = 0
    for product, units, price in data:
        total = units * price
        grand_total += total
        print(f"  {product:<20} {units:>8,} {price:>10,.2f} {total:>12,.2f}")

    # Summary
    if show_summary:
        print(f"  {'-'*20} {'-'*8} {'-'*10} {'-'*12}")
        print(f"  {'TOTAL':<20} {'':>8} {'':>10} {grand_total:>12,.2f}")
        print(f"  {'Tax (18%)':<20} {'':>8} {'':>10} {grand_total * 0.18:>12,.2f}")
        print(f"  {'Grand Total':<20} {'':>8} {'':>10} {grand_total * 1.18:>12,.2f}")

    print(f"  {'=' * width}")

    return grand_total

sales_data = [
    ("Laptop Pro", 150, 899.99),
    ("Wireless Mouse", 500, 29.99),
    ("USB-C Cable", 1200, 12.50),
    ("Monitor 27in", 75, 449.99),
    ("Keyboard Mech", 300, 79.99),
]

total = generate_report("MONTHLY SALES REPORT - OCTOBER 2024", sales_data)

# Explanation: This combines alignment, number formatting, separators,
# and data processing into a professional report. The function is reusable
# with any data that follows the (name, units, price) format.
# Key techniques: f-string alignment, comma separators, calculated fields.
