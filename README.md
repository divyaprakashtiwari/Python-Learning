# 🐍 Python Learning — Beginner to Advanced Practice Repository

A comprehensive, hands-on Python practice repository covering **200+ questions** across
15+ topics — from absolute basics to async programming, DSA, and testing.

Every question is a standalone, runnable `.py` file with:
- The problem statement as a comment
- A working, tested solution
- Explanation and sample output
- Edge-case handling where relevant

---

## 📚 Topic Index

| # | Folder | Topics Covered | Questions |
|---|--------|---------------|-----------|
| 01 | `01_python_basics/` | Variables, data types, type casting, input/output, operators | 10 |
| 02 | `02_control_flow/` | if/elif/else, for/while loops, break/continue, nested loops | 10 |
| 03 | `03_data_structures/` | Lists, tuples, sets, dictionaries, nested structures | 10 |
| 04 | `04_functions/` | Def, args, kwargs, lambda, recursion, scope, closures | 10 |
| 05 | `05_oop/` | Classes, inheritance, polymorphism, encapsulation, magic methods | 10 |
| 06 | `06_file_handling/` | Read, write, append, CSV, context managers, binary files | 10 |
| 07 | `07_exceptions/` | Try/except, custom exceptions, finally, exception chaining | 10 |
| 08 | `08_modules_packages/` | Imports, __name__, packages, standard library, pip | 10 |
| 09 | `09_advanced_python/` | Iterators, comprehensions, decorators, generators, regex, type hints | 10 |
| 10 | `10_dsa/` | Sorting, searching, stacks, queues, linked lists, trees, graphs | 10 |
| 11 | `11_problem_solving/` | Logic puzzles, math problems, string challenges, pattern printing | 10 |
| 12 | `12_json_csv_api_db/` | JSON, CSV, REST APIs, SQLite, async basics | 10 |
| 13 | `13_testing_debugging/` | unittest, assertions, mocking, debugging, logging, profiling | 10 |

---

## 📁 Folder Structure

```
Python Learning/
├── README.md                    ← You are here
├── 01_python_basics/
│   ├── q01_variables_and_types.py
│   ├── q02_type_casting.py
│   ├── ...
│   └── q10_*.py
├── 02_control_flow/
│   ├── q01_if_elif_else.py
│   └── ...
├── ...
├── 13_testing_debugging/
│   └── ...
├── Basic.py                     ← Existing files
├── ConditionalStatement.py
├── DictionarySet.py
├── Practice Questions.py
├── String.py
└── list and tuples.py
```

---

## 🚀 How to Run

Each `.py` file is **fully self-contained**. Run any file directly:

```bash
# Run a single question file
python 01_python_basics/q01_variables_and_types.py

# Or from any folder
python "01_python_basics/q01_variables_and_types.py"
```

**Requirements:** Python 3.8+ (standard library only for most questions).

---

## 🗺️ Learning Roadmap

```
Start Here
    │
    ▼
┌─────────────────────┐
│  01. Python Basics   │  Variables, types, operators
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  02. Control Flow    │  Conditionals, loops
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  03. Data Structures │  Lists, dicts, sets, tuples
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  04. Functions       │  Args, lambda, recursion
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  05. OOP             │  Classes, inheritance
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  06. File Handling   │  Read/write files, CSV
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  07. Exceptions      │  Error handling
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  08. Modules/Pkgs    │  Imports, packages
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  09. Advanced Python │  Decorators, generators
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  10. DSA             │  Algorithms, data structures
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  11. Problem Solving │  Logic, math, patterns
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  12. JSON/CSV/API/DB │  Real-world data handling
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  13. Testing/Debug   │  Quality & reliability
└──────────┘
```

---

## ✅ Progress Checklist

### 01 — Python Basics
- [x] Q01: [Annual Salary Calculator](practice_solutions/01_python_basics/q01_annual_salary.py) — Tax deductions, net pay calculation, and dynamic type deduction
- [x] Q02: [Safe Type Converter](practice_solutions/01_python_basics/q02_safe_type_converter.py) — Robust multi-type parsing with fallback default handling
- [x] Q03: [Compound Interest Breakdown](practice_solutions/01_python_basics/q03_compound_interest_breakdown.py) — Mathematical formulas, precision rounding, and power operations
- [x] Q04: [String Slicing & Masking](practice_solutions/01_python_basics/q04_string_slicing_masking.py) — PII data sanitization, credit card masking, and step slicing
- [x] Q05: [Security Access Evaluator](practice_solutions/01_python_basics/q05_security_evaluator.py) — Multi-role boolean logic, operator precedence, short-circuiting
- [x] Q06: [Aligned Invoice Generator](practice_solutions/01_python_basics/q06_aligned_invoice_generator.py) — Tabular console layout with ANSI padding and separators
- [x] Q07: [Telemetry Stream Formatter](practice_solutions/01_python_basics/q07_telemetry_formatter.py) — f-string precision specifiers, engineering notation, fixed widths
- [x] Q08: [Number Systems & Permissions](practice_solutions/01_python_basics/q08_number_systems_permissions.py) — Binary bitmasks, octal permissions (chmod), hex colors
- [x] Q09: [Packet Unpacking & Rotation](practice_solutions/01_python_basics/q09_packet_unpacking_rotation.py) — Extended tuple unpacking (*rest) and cyclic variable rotation
- [x] Q10: [Frozen Constants Namespace](practice_solutions/01_python_basics/q10_frozen_constants_namespace.py) — Immutable configuration objects and attribute protection
- [x] 📖 Study Notes: [notes/01_python_basics/variables.txt](notes/01_python_basics/variables.txt)
- [x] 📝 Practice Questions (10/10): [practice_questions/01_python_basics/variables.txt](practice_questions/01_python_basics/variables.txt)
- [x] 💡 Solution Suite (10/10): [practice_solutions/01_python_basics/](practice_solutions/01_python_basics/)

### 02 — Control Flow
- [x] Q01: [Progressive Tax Calculator](practice_solutions/02_control_flow/q01_progressive_tax_calculator.py) — Tiered tax bracket logic, marginal rate processing, and deductions
- [x] Q02: [Loan Underwriting Engine](practice_solutions/02_control_flow/q02_loan_underwriting_engine.py) — Nested conditional underwriting with credit scoring and LTV bounds
- [x] Q03: [Time-Series Reductions & SMA](practice_solutions/02_control_flow/q03_timeseries_reductions_sma.py) — Moving window averages, loop aggregations, anomaly detection
- [x] Q04: [Collatz Conjecture Analyzer](practice_solutions/02_control_flow/q04_collatz_conjecture_analyzer.py) — while loop state transitions, orbit length, peak path tracking
- [x] Q05: [Network Packet Filter](practice_solutions/02_control_flow/q05_network_packet_filter.py) — break/continue filtering, corrupted payload rejection, early termination
- [x] Q06: [Matrix Multiplication & Frobenius](practice_solutions/02_control_flow/q06_matrix_multiplication_frobenius.py) — 2D nested loops, dot-product calculations, matrix norms
- [x] Q07: [Loop-Else Search Constructs](practice_solutions/02_control_flow/q07_loop_else_constructs.py) — for...else and while...else idioms for prime searches and target lookup
- [x] Q08: [Geometric Pattern Generator](practice_solutions/02_control_flow/q08_geometric_patterns.py) — Nested index transformations, hollow pyramids, and diamond printing
- [x] Q09: [Ternary Decision Expressions](practice_solutions/02_control_flow/q09_ternary_expressions.py) — Inline conditional expressions, sanitization fallbacks, status badges
- [x] Q10: [Structural Pattern Matching](practice_solutions/02_control_flow/q10_structural_pattern_matching.py) — Python 3.10+ match/case syntax with guards and payload destructuring
- [x] 📖 Study Notes: [notes/02_control_flow/control_flow.txt](notes/02_control_flow/control_flow.txt)
- [x] 📝 Practice Questions (10/10): [practice_questions/02_control_flow/control_flow.txt](practice_questions/02_control_flow/control_flow.txt)
- [x] 💡 Solution Suite (10/10): [practice_solutions/02_control_flow/](practice_solutions/02_control_flow/)

### 03 — Data Structures
- [x] Q01: [List Slicing & Strided Mutations](practice_solutions/03_data_structures/q01_list_slicing_mutations.py) — Slice assignment, strided reversals, and in-place chunk updates
- [x] Q02: [List Mutation Methods](practice_solutions/03_data_structures/q02_list_mutation_methods.py) — insert, extend, remove, pop, index lookup with exception safeguards
- [x] Q03: [NamedTuple Geospatial Modeling](practice_solutions/03_data_structures/q03_namedtuple_geospatial.py) — typing.NamedTuple immutability, coordinate modeling, and distance metrics
- [x] Q04: [RBAC Set Operations](practice_solutions/03_data_structures/q04_rbac_set_operations.py) — Role-based access control, set union, intersection, symmetric difference
- [x] Q05: [Dictionary Header Normalizer](practice_solutions/03_data_structures/q05_dict_header_normalizer.py) — Schema key normalization, collision merging, case insensitivity
- [x] Q06: [Dictionary Methods & Hierarchy](practice_solutions/03_data_structures/q06_dict_methods_hierarchy.py) — setdefault, update, fromkeys, and safe deep dictionary access
- [x] Q07: [Nested JSON Flattener](practice_solutions/03_data_structures/q07_nested_json_flattener.py) — Recursive dictionary flattening and unflattening with dot-notation
- [x] Q08: [Advanced Comprehensions Engine](practice_solutions/03_data_structures/q08_advanced_comprehensions.py) — Nested list, dict, and set comprehensions with conditional projections
- [x] Q09: [Bounded Stack & Queue](practice_solutions/03_data_structures/q09_bounded_stack_queue.py) — LIFO and FIFO implementations with circular boundary overflow guards
- [x] Q10: [Order Book Timsort & Bisect](practice_solutions/03_data_structures/q10_order_book_timsort_bisect.py) — Custom sorting keys, stability, bisect.insort binary searching
- [x] 📖 Study Notes: [notes/03_data_structures/data_structures.txt](notes/03_data_structures/data_structures.txt)
- [x] 📝 Practice Questions (10/10): [practice_questions/03_data_structures/data_structures.txt](practice_questions/03_data_structures/data_structures.txt)
- [x] 💡 Solution Suite (10/10): [practice_solutions/03_data_structures/](practice_solutions/03_data_structures/)

### 04 — Functions
- [x] Q01: [Cone Properties Calculator](practice_solutions/04_functions/q01_cone_properties.py) — Geometric decomposition, math constants, and parameter validation
- [x] Q02: [Mutable Default Arguments](practice_solutions/04_functions/q02_mutable_default_args.py) — Safe sentinel default pattern (None) preventing cross-call state leaks
- [x] Q03: [Dynamic SQL Query Builder](practice_solutions/04_functions/q03_dynamic_sql_builder.py) — Variadic *args and **kwargs processing with parameter sanitization
- [x] Q04: [Multi-Return Factory](practice_solutions/04_functions/q04_multi_return_factory.py) — Tuple unpacking, structured dictionary returns, and multiple exit points
- [x] Q05: [Lambda Ranking & Dispatch](practice_solutions/04_functions/q05_lambda_ranking_dispatch.py) — Anonymous functions, multi-criteria sorting keys, and dispatch tables
- [x] Q06: [Recursive Tree & Nested Sum](practice_solutions/04_functions/q06_recursion_tree_sum.py) — Recursive base cases, nested tree traversals, and recursion depth limits
- [x] Q07: [LEGB Scope & Nonlocal](practice_solutions/04_functions/q07_legb_scope_nonlocal.py) — Local, Enclosing, Global, Builtin name resolution and nonlocal bindings
- [x] Q08: [Closure Rate Limiter](practice_solutions/04_functions/q08_closure_rate_limiter.py) — State encapsulation via lexical closures and sliding window limits
- [x] Q09: [Functional Pipeline Compose](practice_solutions/04_functions/q09_functional_pipeline_compose.py) — Higher-order functions, map, filter, functools.reduce, and currying
- [x] Q10: [Type Contract & Docstring Decorator](practice_solutions/04_functions/q10_type_contract_decorator.py) — Runtime signature inspection, type annotations, and docstring auditing
- [x] 📖 Study Notes: [notes/04_functions/functions.txt](notes/04_functions/functions.txt)
- [x] 📝 Practice Questions (10/10): [practice_questions/04_functions/functions.txt](practice_questions/04_functions/functions.txt)
- [x] 💡 Solution Suite (10/10): [practice_solutions/04_functions/](practice_solutions/04_functions/)

### 05 — OOP
- [x] Q01: Classes and Objects
- [x] Q02: Instance and Class Variables
- [x] Q03: Methods (instance, class, static)
- [x] Q04: Inheritance
- [x] Q05: Polymorphism
- [x] Q06: Encapsulation
- [x] Q07: Magic/Dunder Methods
- [x] Q08: Abstract Classes
- [x] Q09: Property Decorators
- [x] Q10: Composition vs Inheritance
- [x] 📖 Study Notes: [notes/05_oop/oop.txt](notes/05_oop/oop.txt)
- [x] 📝 Practice Questions (10/10): [practice_questions/05_oop/oop.txt](practice_questions/05_oop/oop.txt)

### 06 — File Handling
- [x] Q01: Reading Files
- [x] Q02: Writing Files
- [x] Q03: File Modes and Appending
- [x] Q04: Working with File Paths
- [x] Q05: CSV File Handling
- [x] Q06: Context Managers (with statement)
- [x] Q07: Binary Files
- [x] Q08: File Iteration and Large Files
- [x] Q09: Temporary Files
- [x] Q10: File Metadata and OS Operations
- [x] 📖 Study Notes: [notes/06_file_handling/file_handling.txt](notes/06_file_handling/file_handling.txt)
- [x] 📝 Practice Questions (10/10): [practice_questions/06_file_handling/file_handling.txt](practice_questions/06_file_handling/file_handling.txt)

### 07 — Exceptions
- [x] Q01: Try/Except Basics
- [x] Q02: Multiple Exception Types
- [x] Q03: else and finally
- [x] Q04: Raising Exceptions
- [x] Q05: Custom Exceptions
- [x] Q06: Exception Chaining
- [x] Q07: Context Manager Exception Handling
- [x] Q08: Assertions
- [x] Q09: Logging Exceptions
- [x] Q10: Graceful Degradation Patterns
- [x] 📖 Study Notes: [notes/07_exceptions/exceptions.txt](notes/07_exceptions/exceptions.txt)
- [x] 📝 Practice Questions (10/10): [practice_questions/07_exceptions/exceptions.txt](practice_questions/07_exceptions/exceptions.txt)

### 08 — Modules and Packages
- [x] Q01: Importing Modules
- [x] Q02: Creating Your Own Module
- [x] Q03: __name__ == "__main__"
- [x] Q04: Standard Library Tour (os, sys, math)
- [x] Q05: datetime Module
- [x] Q06: collections Module
- [x] Q07: itertools Module
- [x] Q08: functools Module
- [x] Q09: Package Structure
- [x] Q10: Virtual Environments and pip
- [x] 📖 Study Notes: [notes/08_modules_packages/modules_packages.txt](notes/08_modules_packages/modules_packages.txt)
- [x] 📝 Practice Questions (10/10): [practice_questions/08_modules_packages/modules_packages.txt](practice_questions/08_modules_packages/modules_packages.txt)

### 09 — Advanced Python
- [x] Q01: Iterators and __iter__/__next__
- [x] Q02: Generators and yield
- [x] Q03: Decorators (Function)
- [x] Q04: Decorators (Class-based and Parameterized)
- [x] Q05: Context Managers (Custom)
- [x] Q06: List/Dict/Set Comprehensions (Advanced)
- [x] Q07: Regular Expressions
- [x] Q08: Type Hints and Annotations
- [x] Q09: Dataclasses
- [x] Q10: Walrus Operator and Modern Python
- [x] 📖 Study Notes: [notes/09_advanced_python/advanced_python.txt](notes/09_advanced_python/advanced_python.txt)
- [x] 📝 Practice Questions (10/10): [practice_questions/09_advanced_python/advanced_python.txt](practice_questions/09_advanced_python/advanced_python.txt)

### 10 — DSA
- [x] Q01: Arrays and Two-Pointer Technique
- [x] Q02: Bubble Sort and Selection Sort
- [x] Q03: Binary Search
- [x] Q04: Stack Implementation
- [x] Q05: Queue Implementation
- [x] Q06: Linked List
- [x] Q07: Hash Table
- [x] Q08: Binary Tree and Traversals
- [x] Q09: Graph Representation and BFS/DFS
- [x] Q10: Dynamic Programming Basics
- [x] 📖 Study Notes: [notes/10_dsa/dsa.txt](notes/10_dsa/dsa.txt)
- [x] 📝 Practice Questions (10/10): [practice_questions/10_dsa/dsa.txt](practice_questions/10_dsa/dsa.txt)

### 11 — Problem Solving
- [x] Q01: FizzBuzz and Variants
- [x] Q02: Palindrome Checker
- [x] Q03: Prime Numbers
- [x] Q04: Fibonacci Sequence
- [x] Q05: Anagram Detector
- [x] Q06: Matrix Operations
- [x] Q07: String Compression
- [x] Q08: Number to Words
- [x] Q09: Caesar Cipher
- [x] Q10: Sudoku Validator
- [x] 📖 Study Notes: [notes/11_problem_solving/problem_solving.txt](notes/11_problem_solving/problem_solving.txt)
- [x] 📝 Practice Questions (10/10): [practice_questions/11_problem_solving/problem_solving.txt](practice_questions/11_problem_solving/problem_solving.txt)

### 12 — JSON, CSV, API, Database
- [x] Q01: JSON Read/Write
- [x] Q02: CSV Processing
- [x] Q03: REST API Basics (urllib)
- [x] Q04: SQLite Database CRUD
- [x] Q05: Data Transformation Pipeline
- [x] Q06: Config File Parsing
- [x] Q07: Web Scraping Basics (urllib)
- [x] Q08: Email Validation and Processing
- [x] Q09: Async Basics (asyncio)
- [x] Q10: Command-Line Arguments (argparse)
- [x] 📖 Study Notes: [notes/12_json_csv_api_db/json_csv_api_db.txt](notes/12_json_csv_api_db/json_csv_api_db.txt)
- [x] 📝 Practice Questions (10/10): [practice_questions/12_json_csv_api_db/json_csv_api_db.txt](practice_questions/12_json_csv_api_db/json_csv_api_db.txt)

### 13 — Testing and Debugging
- [x] Q01: unittest Basics
- [x] Q02: Test Fixtures (setUp/tearDown)
- [x] Q03: Assertions Deep Dive
- [x] Q04: Mocking
- [x] Q05: Parameterized Tests
- [x] Q06: Debugging with pdb
- [x] Q07: Logging
- [x] Q08: Profiling and Timing
- [x] Q09: Code Coverage Concepts
- [x] Q10: Defensive Programming
- [x] 📖 Study Notes: [notes/13_testing_debugging/testing_debugging.txt](notes/13_testing_debugging/testing_debugging.txt)
- [x] 📝 Practice Questions (10/10): [practice_questions/13_testing_debugging/testing_debugging.txt](practice_questions/13_testing_debugging/testing_debugging.txt)

---

## 🔧 Git Commit & Push Instructions

Each question in this repository was committed individually. To continue the pattern:

```bash
# 1. Check current status
git status

# 2. Stage only the new/modified file
git add path/to/your_file.py

# 3. Commit with a descriptive message
git commit -m "Add [topic] [question description] solution"

# 4. Push to remote
git push origin master
```

### ⚠️ GitHub Contribution Graph Requirements

For commits to appear on your GitHub contribution graph:
1. **Email must match**: The `user.email` in your git config must match a verified email on your GitHub account.
2. **Default branch**: Commits must be on the default branch (or merged into it).
3. **Not a fork**: The repo must not be a fork (or commits must be to the fork's own default branch).
4. **Delay**: GitHub may take a few hours to update the contribution graph.

```bash
# Verify your git email matches GitHub
git config user.email
# Compare with: GitHub → Settings → Emails
```

---

## 📋 Repository Info

- **Author**: Divya Prakash Tiwari
- **Python Version**: 3.8+
- **Dependencies**: Standard library only (exceptions noted in specific files)
- **License**: MIT

---

*Happy Learning! 🎉 Work through the topics in order, or jump to any topic that interests you.*
