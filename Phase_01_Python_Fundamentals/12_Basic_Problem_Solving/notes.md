# Topic 12: Basic Problem Solving

---

## 1. Introduction

**Basic Problem Solving** bridges the gap between knowing Python syntax (variables, operators, conditionals, loops) and translating real-world or interview problem statements into working, optimal algorithms.

Before jumping into complex Data Structures, every developer must master a core toolkit of **foundational mathematical and logical patterns**:
1. **Digit Extraction & Reversal** (Palindromes, Armstrong numbers)
2. **Divisibility & Number Theory** (Euclidean GCD/LCM, Prime checking, Sieve of Eratosthenes)
3. **Iterative State Transitions** (`O(1)`-space Fibonacci, FizzBuzz, running min/max)

---

## 2. Why is it used?

1. **Online Coding Assessments (Round 1 Screening):** Almost every coding test includes at least one number-theory, digit-manipulation, or simulation problem.
2. **Algorithmic Efficiency Intuition:** Learning why checking divisors up to $\sqrt{N}$ (`O(sqrt(N))`) beats checking up to $N$ (`O(N)`), or why Euclid's GCD runs in `O(log(min(a, b)))`, prepares you directly for Complexity Analysis in DSA.
3. **Edge-Case Discipline:** Trains you to handle `0`, negative numbers, single-element inputs, and boundary conditions systematically.

---

## 3. Syntax

### The 5-Step Problem-Solving Framework (UMPIRE)
1. **U — Understand:** Clarify inputs, outputs, data types, and edge cases (`0`, negatives, empty inputs).
2. **M — Match:** Connect the problem to a known pattern (digit extraction, GCD, sieve, two rolling variables).
3. **P — Plan:** Write step-by-step pseudocode and verify on a small dry-run example.
4. **I — Implement:** Translate the plan into clean, PEP 8 Python code.
5. **R & E — Review & Evaluate:** Trace edge cases and analyze Time & Space Complexity.

```python
# Classic Euclidean GCD Template: O(log(min(a, b)))
def gcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a
```

---

## 4. Explanation (Core Mathematical Algorithms)

1. **Integer Reversal Without Strings (`rev = rev * 10 + n % 10`):**
   - For `n = 123`:
     - Iter 1: `digit = 3`, `rev = 0 * 10 + 3 = 3`, `n = 12`
     - Iter 2: `digit = 2`, `rev = 3 * 10 + 2 = 32`, `n = 1`
     - Iter 3: `digit = 1`, `rev = 32 * 10 + 1 = 321`, `n = 0`
2. **Euclidean Algorithm for GCD:**
   - Based on the theorem that $\gcd(a, b) = \gcd(b, a \bmod b)$.
   - For `gcd(48, 18)` -> `gcd(18, 12)` -> `gcd(12, 6)` -> `gcd(6, 0)` -> returns `6` in just 3 steps!
3. **Sieve of Eratosthenes (`O(N log log N)`):**
   - Create a boolean array `is_prime[0..N]` initialized to `True`.
   - For each prime `p` from `2` up to $\sqrt{N}$, mark all multiples `p*p, p*p + p, p*p + 2p, ...` as `False`.
   - Why start marking at `p * p`? Because any smaller multiple `k * p` (where `k < p`) was already marked by a smaller prime factor of `k`!

---

## 5. Examples

All three runnable examples are located in this folder:
- [`example_01_palindrome_and_armstrong_numbers.py`](example_01_palindrome_and_armstrong_numbers.py)
- [`example_02_gcd_lcm_and_prime_sieve.py`](example_02_gcd_lcm_and_prime_sieve.py)
- [`example_03_fibonacci_and_fizzbuzz.py`](example_03_fibonacci_and_fizzbuzz.py)

### Example 1: Integer Reversal, Palindrome Check, and Armstrong Numbers (`example_01_palindrome_and_armstrong_numbers.py`)

```python
def reverse_integer(n: int) -> int:
    """Reverse the digits of an integer mathematically (preserving sign)."""
    sign = -1 if n < 0 else 1
    remaining = abs(n)
    reversed_num = 0
    while remaining > 0:
        reversed_num = (reversed_num * 10) + (remaining % 10)
        remaining //= 10
    return sign * reversed_num


def is_palindrome_number(n: int) -> bool:
    """Negative numbers are not palindromes; non-negative numbers match their reverse."""
    if n < 0:
        return False
    return n == reverse_integer(n)


def is_armstrong_number(n: int) -> bool:
    """Check if a positive integer equals the sum of its digits raised to the digit count."""
    if n < 0:
        return False
    temp = n
    num_digits = 1 if n == 0 else 0
    while temp > 0:
        num_digits += 1
        temp //= 10

    temp = n
    powered_sum = 0
    while temp > 0:
        digit = temp % 10
        powered_sum += digit ** num_digits
        temp //= 10
    return powered_sum == n


def main() -> None:
    print("=== 1. Integer Reversal & Palindrome Check ===")
    for num in [12321, 4500, -121, 9009]:
        print(f"  n={num:>6} | reversed={reverse_integer(num):>6} | palindrome={is_palindrome_number(num)}")

    print("\n=== 2. Armstrong Numbers up to 10,000 ===")
    armstrong_list = [x for x in range(1, 10000) if is_armstrong_number(x)]
    print(f"  Found: {armstrong_list}")


if __name__ == "__main__":
    main()
```

### Example 2: Euclidean GCD & LCM and Sieve of Eratosthenes (`example_02_gcd_lcm_and_prime_sieve.py`)

```python
def euclidean_gcd(a: int, b: int) -> int:
    """Compute GCD(a, b) using Euclid's iterative remainder algorithm."""
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def compute_lcm(a: int, b: int) -> int:
    """Compute LCM(a, b) using the identity a * b = GCD(a, b) * LCM(a, b)."""
    if a == 0 or b == 0:
        return 0
    return abs(a // euclidean_gcd(a, b) * b)


def sieve_of_eratosthenes(limit: int) -> list[int]:
    """Return all prime numbers <= limit in O(N log log N) time."""
    if limit < 2:
        return []
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    p = 2
    while p * p <= limit:
        if is_prime[p]:
            for multiple in range(p * p, limit + 1, p):
                is_prime[multiple] = False
        p += 1

    return [num for num, prime_flag in enumerate(is_prime) if prime_flag]


def main() -> None:
    print("=== 1. Euclidean GCD & LCM ===")
    pairs = [(48, 18), (105, 35), (17, 23)]
    for x, y in pairs:
        print(f"  Pair ({x:>3}, {y:>2}) -> GCD: {euclidean_gcd(x, y):>2} | LCM: {compute_lcm(x, y):>3}")

    print("\n=== 2. Sieve of Eratosthenes (Primes <= 50) ===")
    primes_up_to_50 = sieve_of_eratosthenes(50)
    print(f"  Count: {len(primes_up_to_50)} primes")
    print(f"  Primes: {primes_up_to_50}")


if __name__ == "__main__":
    main()
```

### Example 3: `O(1)`-Space Iterative Fibonacci and Extensible FizzBuzz (`example_03_fibonacci_and_fizzbuzz.py`)

```python
def generate_fibonacci(count: int) -> list[int]:
    """Return the first `count` Fibonacci numbers starting with 0, 1."""
    result: list[int] = []
    a, b = 0, 1
    for _ in range(count):
        result.append(a)
        a, b = b, a + b
    return result


def extensible_fizzbuzz(limit: int) -> list[str]:
    """Generate FizzBuzz output up to `limit` using extensible divisor rules."""
    rules = [(3, "Fizz"), (5, "Buzz")]
    output: list[str] = []

    for num in range(1, limit + 1):
        word = "".join(label for divisor, label in rules if num % divisor == 0)
        output.append(word if word else str(num))
    return output


def main() -> None:
    print("=== 1. First 12 Fibonacci Numbers ===")
    fib_12 = generate_fibonacci(12)
    print(f"  {fib_12}")

    print("\n=== 2. Extensible FizzBuzz (1 to 20) ===")
    fb_20 = extensible_fizzbuzz(20)
    print("  " + ", ".join(fb_20))


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output for Example 1:
```text
=== 1. Integer Reversal & Palindrome Check ===
  n= 12321 | reversed= 12321 | palindrome=True
  n=  4500 | reversed=    54 | palindrome=False
  n=  -121 | reversed=  -121 | palindrome=False
  n=  9009 | reversed=  9009 | palindrome=True

=== 2. Armstrong Numbers up to 10,000 ===
  Found: [1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, 407, 1634, 8208, 9474]
```

### Output for Example 2:
```text
=== 1. Euclidean GCD & LCM ===
  Pair ( 48, 18) -> GCD:  6 | LCM: 144
  Pair (105, 35) -> GCD: 35 | LCM: 105
  Pair ( 17, 23) -> GCD:  1 | LCM: 391

=== 2. Sieve of Eratosthenes (Primes <= 50) ===
  Count: 15 primes
  Primes: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
```

### Output for Example 3:
```text
=== 1. First 12 Fibonacci Numbers ===
  [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

=== 2. Extensible FizzBuzz (1 to 20) ===
  1, 2, Fizz, 4, Buzz, Fizz, 7, 8, Fizz, Buzz, 11, Fizz, 13, 14, FizzBuzz, 16, 17, Fizz, 19, Buzz
```

---

## 7. Code Explanation

- **`abs(a // euclidean_gcd(a, b) * b)`** —Dividing `a // gcd(a, b)` **before** multiplying by `b` is a classic best practice from C++/Java that prevents intermediate integer overflow.
- **`for multiple in range(p * p, limit + 1, p):`** — Steps directly through multiples of `p` (`p^2, p^2 + p, p^2 + 2p, ...`) using `range`'s `step` parameter.
- **`a, b = b, a + b`** — Advances the Fibonacci state in `O(1)` auxiliary space without recursion overhead.

---

## 8. Common Mistakes

1. **Checking Divisors All the Way to `N - 1` Instead of `int(N ** 0.5)`:**
   Testing primality of $N = 10^{12}$ by looping up to $N$ takes $10^{12}$ operations (minutes/hours). Looping up to $\sqrt{N} = 10^6$ takes less than `0.05` seconds!
2. **Checking `num % 3 == 0` Before `num % 15 == 0` in Naive FizzBuzz:**
   If you write `if num % 3 == 0:` as the first branch and `elif num % 15 == 0:` second, `15` will print `"Fizz"` and never reach `"FizzBuzz"`.
3. **Forgetting Trailing Zeros When Reversing an Integer:**
   `reverse_integer(4500)` becomes `54` because leading zeros are dropped in integers. That is completely expected, and `4500 == 54` still accurately evaluates to `False` for palindrome checks.

---

## 9. Practice Questions

1. **Easy:** Write a function `is_perfect_number(n: int) -> bool` that checks if a positive integer equals the sum of its proper positive divisors (e.g., `6 = 1 + 2 + 3`, `28 = 1 + 2 + 4 + 7 + 14`) in `O(sqrt(n))` time.
2. **Medium:** Write a function `prime_factorization(n: int) -> list[int]` that returns all prime factors of `n` in ascending order with multiplicity (e.g., `60 -> [2, 2, 3, 5]`) in `O(sqrt(n))` time.
3. **Hard:** Write a function `count_trailing_zeros_in_factorial(n: int) -> int` that computes how many trailing zeros `n!` has in `O(log5(n))` time (without computing `n!`) by counting factors of `5` (`n // 5 + n // 25 + n // 125 + ...`).

---

## 10. Interview Questions

### Q1: Why is it sufficient to check divisors only up to $\sqrt{N}$ when testing if $N$ is prime?
**Answer:** Divisors of $N$ always come in pairs $(d, N/d)$. If $N$ has any non-trivial factor $d > \sqrt{N}$, then its paired cofactor $N / d$ must be strictly less than $\sqrt{N}$. Therefore, if no divisor is found in $[2, \lfloor\sqrt{N}\rfloor]$, no divisor can exist above $\sqrt{N}$ either.

### Q2: How do you find the number of trailing zeros in $1000!$ without computing $1000!$?
**Answer:** Every trailing zero is produced by a factor of $10 = 2 \times 5$. In any factorial $n!$, factors of $2$ are always more plentiful than factors of $5$. Thus, the number of trailing zeros equals the multiplicity of prime factor $5$ in $n!$, computed via Legendre's formula: $\sum_{k=1}^{\infty} \lfloor \frac{n}{5^k} \rfloor$ in `O(log_5(n))` time.

### Q3: What is the time complexity of the Sieve of Eratosthenes up to $N$, and why?
**Answer:** For each prime $p \le \sqrt{N}$, the inner loop runs $N / p$ times. The total work is $N \sum_{p \text{ prime} \le N} \frac{1}{p}$. By Mertens' second theorem, the sum of reciprocals of primes up to $N$ grows as $\ln(\ln N)$, giving a total time complexity of **`O(N log log N)`** and space complexity of **`O(N)`**.
