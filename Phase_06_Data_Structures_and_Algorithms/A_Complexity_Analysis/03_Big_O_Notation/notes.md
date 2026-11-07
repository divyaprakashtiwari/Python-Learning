# Phase 6 — Section A: Complexity Analysis — Topic 03: Big O Notation

## 1. Introduction

**Big O Notation** is the standard mathematical language used in computer science to classify algorithms by their **asymptotic growth rate** as input size $n \to \infty$. Together with its siblings **Big Omega ($\Omega$)** and **Big Theta ($\Theta$)**, it abstracts away hardware-specific constants and lower-order terms to focus on the dominant term that governs scalability.

---

## 2. Why is it used?

1. **Hardware-Independent Comparison:** Whether code runs on a 1995 microcontroller or a 2026 server cluster, an $O(n \log n)$ sort will always overtake an $O(n^2)$ sort once $n$ exceeds a modest threshold $n_0$.
2. **Instant Bottleneck Identification:** When a multi-step pipeline runs $O(n)$ preprocessing + $O(n \log n)$ sorting + $O(n)$ output formatting, Big O rules immediately simplify the overall pipeline complexity to $O(n \log n)$.
3. **Precision with $\mathcal{O}$, $\Omega$, and $\Theta$:** Allows engineers to distinguish between an **upper bound** ("takes *at most* this many steps"), a **lower bound** ("takes *at least* this many steps"), and a **tight bound** ("scales *on the exact order of*").

---

## 3. Syntax

```text
Formal Mathematical Definitions:
1. Big O (Asymptotic Upper Bound — "At Most"):
   T(n) = O(g(n))  iff  there exist constants c > 0 and n0 >= 1 such that:
   0 <= T(n) <= c * g(n)   for all n >= n0

2. Big Omega (Asymptotic Lower Bound — "At Least"):
   T(n) = Omega(g(n))  iff  there exist constants c > 0 and n0 >= 1 such that:
   0 <= c * g(n) <= T(n)   for all n >= n0

3. Big Theta (Asymptotic Tight Bound — "Exact Order"):
   T(n) = Theta(g(n))  iff  T(n) = O(g(n)) AND T(n) = Omega(g(n)):
   0 <= c1 * g(n) <= T(n) <= c2 * g(n)   for all n >= n0
```

---

## 4. Explanation (Step-by-Step)

1. **The Two Simplification Rules of Big O:**
   - **Rule 1 — Drop Constant Multipliers:** $O(5n) \to O(n)$, and $O(\frac{1}{2}n^2) \to O(n^2)$. Also note that all logarithm bases differ only by a constant factor ($\log_a n = \frac{\ln n}{\ln a}$), so we always write $O(\log n)$ without a base!
   - **Rule 2 — Drop Lower-Order Terms:** In $T(n) = 3n^2 + 50n + 1000$, as $n \to \infty$, the $n^2$ term dominates completely (at $n = 10,000$, $3n^2$ is $99.83\%$ of the total), so $T(n) = O(n^2)$.
2. **The Standard Complexity Growth Hierarchy (Fastest to Slowest):**
   $$O(1) < O(\log \log n) < O(\log n) < O(\sqrt{n}) < O(n) < O(n \log n) < O(n^2) < O(n^3) < O(2^n) < O(n!)$$
3. **Multiple Independent Variables ($N$ and $M$):**
   - Never collapse two independent input sizes into a single $n$!
   - Traversing a grid of $R$ rows and $C$ columns is **$O(R \times C)$**.
   - Breadth-First Search on a graph with $V$ vertices and $E$ edges is **$O(V + E)$**.

---

## 5. Minimum 3 Examples

### Example 01: Asymptotic Dominance — Why Constants and Lower-Order Terms Drop Out as $N$ Grows
File: [`example_01_asymptotic_dominance_and_constants.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/A_Complexity_Analysis/03_Big_O_Notation/example_01_asymptotic_dominance_and_constants.py)

```python
"""
Phase 6 - Section A (Complexity Analysis) - Topic 03: Big O Notation
Example 01: Asymptotic Dominance — Why Constants and Lower-Order Terms Drop Out as N Grows

Demonstrates:
  - Comparing `T(n) = 3n^2 + 50n + 1000` against `3n^2` as `n` grows from `10` to `10,000`
  - Showing quantitatively that the `3n^2` dominant term accounts for >99.8% of total operations at large N
"""


def exact_cost(n: int) -> tuple[int, int, float]:
    """Return `(total_ops, quadratic_term_ops, quadratic_share_pct)` for T(n) = 3n^2 + 50n + 1000."""
    quad = 3 * (n**2)
    linear = 50 * n
    constant = 1000
    total = quad + linear + constant
    share_pct = (quad / total) * 100.0
    return total, quad, share_pct


def main() -> None:
    print("=== Asymptotic Dominance of `3n^2` in `T(n) = 3n^2 + 50n + 1000` ===")
    print(f"  {'N':>7} | {'Total T(n)':>15} | {'3n^2 Term':>15} | {'3n^2 Share (%)':>14}")
    print("  " + "-" * 59)
    for n in [10, 100, 1_000, 10_000]:
        total, quad, pct = exact_cost(n)
        print(f"  {n:>7,} | {total:>15,} | {quad:>15,} | {pct:>13.2f}%")


if __name__ == "__main__":
    main()
```

### Example 02: The Big O Growth Hierarchy — $O(1) < O(\log n) < O(n) < O(n \log n) < O(n^2) < O(2^n)$
File: [`example_02_complexity_hierarchy_growth_table.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/A_Complexity_Analysis/03_Big_O_Notation/example_02_complexity_hierarchy_growth_table.py)

```python
"""
Phase 6 - Section A (Complexity Analysis) - Topic 03: Big O Notation
Example 02: The Big O Growth Hierarchy — O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(2^n)

Demonstrates:
  - Tabulating the 6 major complexity classes side by side to see why O(2^n) and O(n^2)
    hit Time Limit Exceeded (TLE) at ~10^8 operations per second
"""

import math


def main() -> None:
    print("=== Complexity Class Growth Comparison Table ===")
    header = f"  {'N':>4} | {'O(1)':>4} | {'O(log2 n)':>9} | {'O(n)':>6} | {'O(n log2 n)':>11} | {'O(n^2)':>10} | {'O(2^n)':>12}"
    print(header)
    print("  " + "-" * (len(header) - 2))
    for n in [2, 8, 16, 32]:
        o_1 = 1
        o_log = int(math.log2(n))
        o_n = n
        o_nlogn = n * o_log
        o_n2 = n * n
        o_2n = 1 << n
        print(f"  {n:>4} | {o_1:>4} | {o_log:>9} | {o_n:>6} | {o_nlogn:>11} | {o_n2:>10,} | {o_2n:>12,}")


if __name__ == "__main__":
    main()
```

### Example 03: Big O (Upper Bound), Big Omega (Lower Bound), & Big Theta (Tight Bound)
File: [`example_03_big_o_big_omega_big_theta_bounds.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/A_Complexity_Analysis/03_Big_O_Notation/example_03_big_o_big_omega_big_theta_bounds.py)

```python
"""
Phase 6 - Section A (Complexity Analysis) - Topic 03: Big O Notation
Example 03: Big O (Upper Bound), Big Omega (Lower Bound), & Big Theta (Tight Bound)

Demonstrates:
  - Verifying formal inequality definitions `c1 * g(n) <= T(n) <= c2 * g(n)` for all `n >= n0`
  - Why `T(n) = 2n + 5` is Theta(n), O(n), O(n^2), and Omega(n), but NOT Theta(n^2)
"""


def t_linear(n: int) -> int:
    return 2 * n + 5


def verify_theta_linear(c1: int, c2: int, n0: int, max_n: int = 100) -> bool:
    """Verify `c1 * n <= 2n + 5 <= c2 * n` for all `n` in `n0..max_n`."""
    return all(c1 * n <= t_linear(n) <= c2 * n for n in range(n0, max_n + 1))


def main() -> None:
    print("=== Formal Verification of Theta(n) Bounds for `T(n) = 2n + 5` ===")
    # For n >= 5: 2n <= 2n + 5 <= 3n
    c1, c2, n0 = 2, 3, 5
    holds = verify_theta_linear(c1=c1, c2=c2, n0=n0)
    print(f"  Does {c1}*n <= 2n + 5 <= {c2}*n hold for all n >= {n0}? {holds}")
    for sample_n in [5, 10, 50]:
        print(f"    n={sample_n:>2}: lower={c1 * sample_n:>3} <= T(n)={t_linear(sample_n):>3} <= upper={c2 * sample_n:>3}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 01
```text
=== Asymptotic Dominance of `3n^2` in `T(n) = 3n^2 + 50n + 1000` ===
        N |      Total T(n) |       3n^2 Term | 3n^2 Share (%)
  -----------------------------------------------------------
       10 |           1,800 |             300 |         16.67%
      100 |          36,000 |          30,000 |         83.33%
    1,000 |       3,051,000 |       3,000,000 |         98.33%
   10,000 |     300,501,000 |     300,000,000 |         99.83%
```

### Output — Example 02
```text
=== Complexity Class Growth Comparison Table ===
     N | O(1) | O(log2 n) |   O(n) | O(n log2 n) |     O(n^2) |       O(2^n)
  --------------------------------------------------------------------------
     2 |    1 |         1 |      2 |           2 |          4 |            4
     8 |    1 |         3 |      8 |          24 |         64 |          256
    16 |    1 |         4 |     16 |          64 |        256 |       65,536
    32 |    1 |         5 |     32 |         160 |      1,024 | 4,294,967,296
```

### Output — Example 03
```text
=== Formal Verification of Theta(n) Bounds for `T(n) = 2n + 5` ===
  Does 2*n <= 2n + 5 <= 3*n hold for all n >= 5? True
    n= 5: lower= 10 <= T(n)= 15 <= upper= 15
    n=10: lower= 20 <= T(n)= 25 <= upper= 30
    n=50: lower=100 <= T(n)=105 <= upper=150
```

---

## 7. Code Explanation

1. **Dominant Term Share (Example 01):** At $N = 10$, the constant `1000` and linear `50n` terms represent over $83\%$ of the cost, but by $N = 10,000$, the quadratic $3n^2$ term accounts for **$99.83\%$** of the total work.
2. **Exponential Explosion at $N = 32$ (Example 02):** At $N = 32$, $O(n \log_2 n)$ takes just `160` steps, whereas $O(2^n)$ takes `4,294,967,296` ($\approx 4.3 \times 10^9$) steps!
3. **Witness Constants $(c_1, c_2, n_0)$ (Example 03):** Demonstrates the exact mathematical proof that $2n + 5 = \Theta(n)$ by choosing $c_1 = 2$, $c_2 = 3$, and threshold $n_0 = 5$.

---

## 8. Common Mistakes

1. **Dropping the Base in Exponential Expressions ($O(2^n)$ vs $O(3^n)$):**
   - While $\log_2 n$ and $\log_3 n$ differ only by a constant multiplier, **$2^n$ and $3^n$ do NOT differ by a constant** ($\frac{3^n}{2^n} = (1.5)^n \to \infty$)! Never simplify $O(3^n)$ or $O(4^n)$ to $O(2^n)$.
2. **Confusing Big O / Big Omega / Big Theta with Worst / Best / Average Case:**
   - **Misconception:** *"Big O means Worst Case, Big Omega means Best Case, and Big Theta means Average Case."*
   - **Truth:** $O$, $\Omega$, and $\Theta$ are **mathematical bounds on a function** (upper, lower, tight), whereas Best, Average, and Worst case describe **input distributions**! You can describe the **Best Case** of Merge Sort as $\Theta(n \log n)$ and the **Worst Case** of Insertion Sort as $\Theta(n^2)$.

---

## 9. Practice Questions

1. **Easy:** Simplify each expression to its tightest Big O class:
   - $f_1(n) = 500n + 10n \log_2 n + 9999$
   - $f_2(n) = 4n^3 + 100n^2 \log n$
   - $f_3(n) = 2^{n+3} + n^{10}$ (Hint: $2^{n+3} = 8 \cdot 2^n$).
2. **Medium:** Prove mathematically that $\log(n!) = \Theta(n \log n)$ and write a script comparing $\sum_{k=1}^{n} \log_2(k)$ against $n \log_2(n)$ for $n \in \{16, 64, 256, 1024\}$.
3. **Hard:** What is the time complexity of sorting an array of $N$ strings where each string has length at most $L$? Explain why it is $O(N \cdot L \log N)$ rather than $O(N \log N)$.

---

## 10. Interview Questions

### Q1: Why is $O(\log_2 n)$ identical to $O(\log_{10} n)$ in Big O notation, whereas $O(2^n)$ is NOT identical to $O(10^n)$?
**Answer:** By the change-of-base formula, $\log_{10}(n) = \frac{1}{\log_2(10)} \cdot \log_2(n)$. Because $\frac{1}{\log_2(10)} \approx 0.301$ is a fixed constant independent of $n$, Big O drops it. By contrast, $\frac{10^n}{2^n} = 5^n$, which grows exponentially with $n$ and is **not** a constant factor.

### Q2: What is the time complexity of sorting $N$ strings of length $L$?
**Answer:** **$O(N \cdot L \log N)$**. Comparison-based sorting performs $O(N \log N)$ string comparisons, and each comparison between two strings of length $L$ takes up to $O(L)$ character comparisons in the worst case.

### Q3: Is $T(n) = 5n + 3$ also technically $O(n^2)$?
**Answer:** Formally, **yes**—because $O(g(n))$ is an asymptotic *upper bound* ($\le$), $5n + 3 \le 1 \cdot n^2$ for all $n \ge 6$. However, in interviews and engineering, we always state the **tightest** upper bound ($\Theta(n)$ / tight $O(n)$).
