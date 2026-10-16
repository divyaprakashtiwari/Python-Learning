"""
Topic 01: Python Basics
Question 07: String Formatting (Deep Dive)

Advanced string formatting techniques: f-strings, format spec
mini-language, custom format methods, and template strings.
"""

# ============================================================
# Q1: F-string expressions and debugging
# ============================================================
# Question: Show advanced f-string features including expressions,
# the = specifier for debugging, and nested f-strings.

print("=== Q1: F-string Expressions and Debugging ===")

# Expressions inside f-strings
x, y = 10, 3
print(f"  {x} + {y} = {x + y}")
print(f"  {x} * {y} = {x * y}")
print(f"  max({x}, {y}) = {max(x, y)}")

# The = specifier (Python 3.8+) -- auto-shows variable name and value
name = "Divya"
age = 21
print(f"  {name = }")
print(f"  {age = }")
print(f"  {x + y = }")
print(f"  {len(name) = }")

# Nested f-strings
width = 20
value = "centered"
print(f"  {f'{value:^{width}}'!r}")

# Conditional inside f-string
score = 85
print(f"  Grade: {'Pass' if score >= 60 else 'Fail'}")

# Calling methods
items = ["apple", "banana", "cherry"]
print(f"  Joined: {', '.join(items)}")

# Explanation: F-strings can contain any valid Python expression.
# The = specifier is incredibly useful for debugging: f"{var=}" prints
# both the variable name and its value. Nested f-strings allow dynamic
# format specifications.


# ============================================================
# Q2: Format specification mini-language
# ============================================================
# Question: Master the full format spec: fill, align, sign,
# width, grouping, precision, and type.

print("\n=== Q2: Format Spec Mini-Language ===")

# Full syntax: [[fill]align][sign][z][#][0][width][grouping_option][.precision][type]

# Alignment: < (left), > (right), ^ (center), = (pad after sign)
n = 42
print(f"  Left:   '{n:<10}'")
print(f"  Right:  '{n:>10}'")
print(f"  Center: '{n:^10}'")
print(f"  Fill:   '{n:*^10}'")
print(f"  Fill:   '{n:.<10}'")
print(f"  Fill:   '{n:->10}'")

# Sign: + (always), - (negative only), space (space for positive)
for num in [-7, 0, 7]:
    print(f"  {num:+d}  {num:-d}  {num: d}")

# Zero-padding
print(f"\n  Zero-pad: {42:05d}")
print(f"  Negative: {-42:05d}")  # Sign before zeros

# Alternate form (#)
print(f"\n  Hex: {255:#x}  Oct: {255:#o}  Bin: {255:#b}")

# Grouping
print(f"  Comma: {1234567:,}")
print(f"  Underscore: {1234567:_}")

# Precision for floats
pi = 3.141592653589793
for prec in range(1, 7):
    print(f"  pi to {prec} decimals: {pi:.{prec}f}")

# Explanation: The format spec mini-language is powerful and consistent
# across f-strings, str.format(), and the format() built-in.
# Key: fill+align control spacing, width sets minimum field width,
# .precision controls decimal places (or max string length for strings).


# ============================================================
# Q3: str.format() method patterns
# ============================================================
# Question: Demonstrate .format() with positional args, keyword args,
# attribute access, and index access.

print("\n=== Q3: str.format() Patterns ===")

# Positional arguments
print("  {} + {} = {}".format(2, 3, 5))

# Numbered positional (reuse arguments)
print("  {0} loves {1}. {1} loves {0}.".format("Alice", "Bob"))

# Keyword arguments
print("  {name} is {age} years old".format(name="Divya", age=21))

# Accessing attributes and indices
person = {"name": "Divya", "scores": [95, 88, 92]}
print("  Name: {p[name]}".format(p=person))
print("  First score: {p[scores][0]}".format(p=person))

# Object attributes
import math
print("  Pi: {m.pi:.4f}".format(m=math))

# Format as a variable
template = "Hello {name}, welcome to {place}!"
print(f"  {template.format(name='Divya', place='Python')}")

# Explanation: str.format() is more verbose than f-strings but useful
# when the format string is stored as data (templates, config files).
# It supports attribute access (obj.attr) and item access (dict[key])
# directly in the format string.


# ============================================================
# Q4: format() built-in and __format__ protocol
# ============================================================
# Question: Use the format() built-in and implement __format__
# on a custom class.

print("\n=== Q4: format() Built-in and __format__ ===")

# format() built-in
print(f"  format(42, '08b')    = {format(42, '08b')}")
print(f"  format(3.14, '.1f')  = {format(3.14, '.1f')}")
print(f"  format('hi', '>10')  = {format('hi', '>10')!r}")

# Custom __format__ method
class Currency:
    def __init__(self, amount, symbol="$"):
        self.amount = amount
        self.symbol = symbol

    def __format__(self, spec):
        if spec == "short":
            if abs(self.amount) >= 1_000_000:
                return f"{self.symbol}{self.amount/1_000_000:.1f}M"
            elif abs(self.amount) >= 1_000:
                return f"{self.symbol}{self.amount/1_000:.1f}K"
            return f"{self.symbol}{self.amount:.0f}"
        elif spec == "full":
            return f"{self.symbol}{self.amount:,.2f}"
        else:
            return f"{self.symbol}{self.amount:{spec}}"

price = Currency(1234567.89)
print(f"\n  Currency formatting:")
print(f"  Short:   {price:short}")
print(f"  Full:    {price:full}")
print(f"  Custom:  {price:>15,.2f}")

small = Currency(42.5)
print(f"  Small:   {small:short}")
print(f"  Small:   {small:full}")

# Explanation: format(value, spec) calls value.__format__(spec).
# By implementing __format__ on your classes, you can support custom
# format specifiers. This is how datetime objects support strftime-like
# formatting in f-strings: f"{now:%Y-%m-%d}".


# ============================================================
# Q5: String Template (safe substitution)
# ============================================================
# Question: Use string.Template for safe user-provided templates.

from string import Template

print("\n=== Q5: String Template ===")

# Basic template
t = Template("Hello $name, you are $age years old")
result = t.substitute(name="Divya", age=21)
print(f"  {result}")

# Safe substitute (doesn't raise on missing keys)
t2 = Template("$greeting $name, your balance is $$${balance}")
try:
    # This will raise KeyError for missing 'balance'
    result = t2.substitute(greeting="Hi", name="Divya")
except KeyError as e:
    print(f"  substitute() with missing key: KeyError {e}")

# safe_substitute returns the placeholder for missing keys
result = t2.safe_substitute(greeting="Hi", name="Divya")
print(f"  safe_substitute(): {result}")

# Full substitution
result = t2.substitute(greeting="Hi", name="Divya", balance="1,000")
print(f"  Full: {result}")

# Using with dictionaries
data = {"name": "Amit", "role": "Developer", "company": "TechCorp"}
t3 = Template("$name works as a $role at $company")
print(f"  Dict: {t3.substitute(data)}")

# Explanation: string.Template uses $variable syntax and is SAFER than
# f-strings or .format() for user-provided templates because it can't
# execute arbitrary code. Use safe_substitute() when some variables
# might be missing. $$ produces a literal $ character.


# ============================================================
# Q6: Formatting dates and times
# ============================================================
# Question: Format datetime objects using strftime codes in f-strings.

from datetime import datetime, timedelta

print("\n=== Q6: Date/Time Formatting ===")

now = datetime.now()

# strftime codes in f-strings
print(f"  Full:       {now:%A, %B %d, %Y}")
print(f"  Date:       {now:%Y-%m-%d}")
print(f"  Time:       {now:%H:%M:%S}")
print(f"  12-hour:    {now:%I:%M %p}")
print(f"  ISO format: {now:%Y-%m-%dT%H:%M:%S}")
print(f"  Short:      {now:%d/%m/%y}")

# Relative time
past = now - timedelta(days=45, hours=3, minutes=30)
delta = now - past

def format_timedelta(td):
    """Format timedelta as human-readable string."""
    total_seconds = int(td.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []
    if days: parts.append(f"{days}d")
    if hours: parts.append(f"{hours}h")
    if minutes: parts.append(f"{minutes}m")
    if seconds: parts.append(f"{seconds}s")
    return " ".join(parts) or "0s"

print(f"\n  Time since {past:%Y-%m-%d}: {format_timedelta(delta)}")

# Explanation: datetime objects support strftime format codes directly
# in f-strings via __format__. Common codes: %Y(year), %m(month),
# %d(day), %H(24h), %I(12h), %M(min), %S(sec), %A(weekday name),
# %B(month name), %p(AM/PM).


# ============================================================
# Q7: Formatting collections and nested data
# ============================================================
# Question: Format lists, dicts, and nested structures elegantly.

print("\n=== Q7: Formatting Collections ===")

# List formatting
scores = [95, 88, 72, 91, 85]
print(f"  Scores: {scores}")
print(f"  Pretty: [{', '.join(f'{s:>3}' for s in scores)}]")
print(f"  Bars:   {''.join('#' * (s // 10) for s in scores)}")

# Dictionary formatting
config = {"host": "localhost", "port": 8080, "debug": True, "workers": 4}
print(f"\n  Config:")
max_key_len = max(len(k) for k in config)
for key, value in config.items():
    print(f"    {key:<{max_key_len}} = {value}")

# Table from list of dicts
users = [
    {"name": "Divya", "role": "Student", "active": True},
    {"name": "Amit", "role": "Developer", "active": True},
    {"name": "Priya", "role": "Designer", "active": False},
]

# Auto-detect column widths
columns = list(users[0].keys())
widths = {col: max(len(col), max(len(str(u[col])) for u in users)) for col in columns}

header = "  ".join(f"{col:<{widths[col]}}" for col in columns)
print(f"\n  {header}")
print(f"  {'-' * len(header)}")
for user in users:
    row = "  ".join(f"{str(user[col]):<{widths[col]}}" for col in columns)
    print(f"  {row}")

# Explanation: Formatting collections often involves comprehensions
# with format specs. Auto-detecting column widths makes tables adapt
# to any data. The pattern: compute max width, then use it in f-strings
# with dynamic width: f"{value:<{width}}".


# ============================================================
# Q8: Locale-aware and internationalization formatting
# ============================================================
# Question: Format numbers and currency for different locales.

print("\n=== Q8: Number Formatting Patterns ===")

# Manual locale-style formatting
def format_indian(number):
    """Format number in Indian numbering system (lakhs, crores)."""
    s = str(int(abs(number)))
    if len(s) <= 3:
        result = s
    else:
        result = s[-3:]
        s = s[:-3]
        while s:
            result = s[-2:] + "," + result
            s = s[:-2]
    if number < 0:
        result = "-" + result
    return result

amounts = [1000, 100000, 1234567, 12345678, 1234567890]
print(f"  {'Amount':>15} {'Western':>15} {'Indian':>15}")
for amt in amounts:
    print(f"  {amt:>15} {amt:>15,} {format_indian(amt):>15}")

# File size formatting
def format_bytes(size):
    """Format byte count as human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f} {unit}" if size != int(size) else f"{int(size)} {unit}"
        size /= 1024
    return f"{size:.1f} PB"

test_sizes = [0, 512, 1024, 1536, 1048576, 1073741824, 1099511627776]
for s in test_sizes:
    print(f"  {s:>15,} bytes = {format_bytes(s):>10}")

# Explanation: Python's standard formatting uses Western grouping (commas
# every 3 digits). Indian numbering uses different grouping after the
# first 3 digits (2-digit groups). Custom formatters handle these cases.
# File size formatting is a common practical need.


# ============================================================
# Q9: Padding, truncation, and string formatting tricks
# ============================================================
# Question: Advanced string formatting: truncation, dynamic
# format specs, and practical patterns.

print("\n=== Q9: Advanced String Formatting Tricks ===")

# Truncation with .precision on strings
long_text = "This is a very long string that needs truncation"
print(f"  Full:      {long_text}")
print(f"  Truncated: {long_text:.30}")
print(f"  With ...:  {long_text:.27}...")

# Dynamic format specifications
def format_value(value, width=10, align="<", precision=None):
    """Format any value with dynamic specs."""
    if precision is not None and isinstance(value, float):
        spec = f"{align}{width}.{precision}f"
    else:
        spec = f"{align}{width}"
    return f"{value:{spec}}"

print(f"\n  Dynamic formatting:")
print(f"  {format_value('hello', 15, '<')!r}")
print(f"  {format_value(3.14159, 10, '>', 2)!r}")
print(f"  {format_value(42, 8, '^')!r}")

# Practical: Formatted list with indices
items = ["Python", "JavaScript", "Rust", "Go", "TypeScript"]
for i, item in enumerate(items, 1):
    bar = "#" * (len(item) * 2)
    print(f"  {i:>2}. {item:<12} {bar}")

# Practical: Variable-width columns
data = [("Short", 1), ("A much longer name", 2), ("Medium text", 3)]
max_w = max(len(d[0]) for d in data)
for text, num in data:
    print(f"  [{text:>{max_w}}] -> {num}")

# Explanation: .precision on strings truncates to that many characters.
# You can build format specs dynamically by using variables inside the
# format spec: f"{value:{variable_spec}}". This enables fully configurable
# formatting functions.


# ============================================================
# Q10: Build a mini-template engine
# ============================================================
# Question: Create a simple template engine that supports variable
# substitution, conditionals, and loops.

print("\n=== Q10: Mini Template Engine ===")

def render_template(template, context):
    """Simple template engine supporting {{var}} substitution.

    Supports:
    - {{variable}} for substitution
    - {{variable|default_value}} for defaults
    - {{variable|upper}} for uppercase
    """
    import re

    def replace_var(match):
        expr = match.group(1).strip()

        # Check for pipe (filter or default)
        if '|' in expr:
            var_name, modifier = expr.split('|', 1)
            var_name = var_name.strip()
            modifier = modifier.strip()

            value = context.get(var_name)

            if modifier == "upper" and value is not None:
                return str(value).upper()
            elif modifier == "lower" and value is not None:
                return str(value).lower()
            elif modifier == "title" and value is not None:
                return str(value).title()
            elif value is None:
                return modifier  # Use as default value
            return str(value)
        else:
            value = context.get(expr, f"{{?{expr}}}")
            return str(value)

    result = re.sub(r'\{\{(.+?)\}\}', replace_var, template)
    return result

# Test the template engine
template = """
  Hello {{name|title}},
  Welcome to {{company|Unknown Corp}}.
  Your role is {{role|upper}}.
  Department: {{dept|Not Assigned}}.
"""

context1 = {"name": "divya prakash", "role": "developer", "company": "TechCo"}
context2 = {"name": "amit kumar", "role": "designer"}

print("  Template with full context:")
print(render_template(template, context1))

print("  Template with partial context (defaults used):")
print(render_template(template, context2))

# Practical: Generating multiple outputs from one template
email_template = "  Dear {{name}}, your order #{{order_id}} is {{status}}."
orders = [
    {"name": "Divya", "order_id": "1001", "status": "shipped"},
    {"name": "Amit", "order_id": "1002", "status": "processing"},
    {"name": "Priya", "order_id": "1003", "status": "delivered"},
]

print("  Generated emails:")
for order in orders:
    print(render_template(email_template, order))

# Explanation: This template engine uses regex to find {{variable}} patterns
# and replaces them from a context dictionary. The pipe (|) supports
# filters (upper, lower, title) and default values. This is a simplified
# version of what Jinja2 and Django templates do. Real template engines
# add loops, conditionals, inheritance, and escaping.
