# Section B: Searching — Topic 02: Binary Search

## 1. Introduction

**Binary Search** is a classic **Divide-and-Conquer** searching algorithm that locates a `target` value inside a **sorted** collection in $O(\log N)$ time.

Instead of checking elements one by one like Linear Search ($O(N)$), Binary Search repeatedly inspects the **middle element** (`arr[mid]`) of the current search interval `[low .. high]`:
- If `arr[mid] == target`, we found the element immediately!
- If `arr[mid] < target`, then every element at or to the left of `mid` is also strictly smaller than `target` (because the array is sorted). We **discard the entire left half** by setting `low = mid + 1`.
- If `arr[mid] > target`, every element at or to the right of `mid` is strictly larger than `target`. We **discard the entire right half** by setting `high = mid - 1`.

Because each comparison cuts the remaining search space in **half**, searching $1,000,000,000$ ($10^9$) sorted records takes **at most $30$ comparisons** ($\lceil \log_2(10^9) \rceil = 30$).

---

## 2. Why is it used?

1. **Logarithmic Scalability ($O(\log N)$):** In databases, file systems, and in-memory indexes, datasets routinely hold millions or billions of sorted keys. Binary search turns a 1-second linear scan of $10^7$ items into a sub-microsecond lookup (~24 comparisons).
2. **Range, Floor, and Ceiling Queries:** Unlike hash tables ($O(1)$ exact match only), a sorted array with Binary Search can answer *"What is the largest server capacity $\le 100$ GB?"* (Floor), *"What is the smallest capacity $\ge 50$ GB?"* (Ceiling), or *"How many timestamps fall between $T_1$ and $T_2$?"* in $O(\log N)$ time.
3. **Zero Memory Overhead ($O(1)$ Auxiliary Space):** Iterative binary search operates directly on the sorted array using just three integer pointers (`low`, `high`, `mid`), requiring no hash buckets or tree node pointers.
4. **Continuous Numerical Root Finding (Bisection Method):** Binary search works on continuous monotonic functions (like computing $\sqrt{x}$ or finding break-even interest rates) to arbitrary floating-point precision $\epsilon$.

---

## 3. Syntax & Core Blueprints

### Blueprint 1: Standard Iterative Binary Search ($O(\log N)$ Time, $O(1)$ Space)
```python
def binary_search(arr: list[int], target: int) -> int:
    low = 0
    high = len(arr) - 1

    while low <= high:
        # Overflow-safe midpoint formula
        mid = low + (high - low) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1   # Discard left half [low .. mid]
        else:
            high = mid - 1  # Discard right half [mid .. high]

    return -1               # Target not found
```

### Blueprint 2: Python's Built-in `bisect` Module (C-Speed Binary Search)
```python
import bisect

# First index where x could be inserted to maintain sort order (first >= x)
idx_left = bisect.bisect_left(sorted_list, x)

# First index strictly greater than x (first > x)
idx_right = bisect.bisect_right(sorted_list, x)
```

---

## 4. Step-by-Step Explanation & Complexity Analysis

### Tracing Binary Search on $N = 16$ Elements
Suppose `arr = [105, 112, 128, 144, 159, 173, 188, 204, 219, 235, 250, 268, 281, 297, 310, 325]` and `target = 281`:
1. **Step 1:** `low = 0`, `high = 15` (16 elements). `mid = 0 + (15 - 0) // 2 = 7`. `arr[7] = 204`. Since `204 < 281`, move right: `low = 8`.
2. **Step 2:** `low = 8`, `high = 15` (8 elements). `mid = 8 + (15 - 8) // 2 = 11`. `arr[11] = 268`. Since `268 < 281`, move right: `low = 12`.
3. **Step 3:** `low = 12`, `high = 15` (4 elements). `mid = 12 + (15 - 12) // 2 = 13`. `arr[13] = 297`. Since `297 > 281`, move left: `high = 12`.
4. **Step 4:** `low = 12`, `high = 12` (1 element). `mid = 12`. `arr[12] = 281 == target` $\rightarrow$ **Found at index `12` in 4 steps!**

### Mathematical Derivation of $O(\log_2 N)$
After $k$ iterations, the active search window size $\frac{N}{2^k}$ shrinks to $1$ element when:
$$\frac{N}{2^k} = 1 \iff 2^k = N \iff k = \log_2 N$$

| Variant | Best Case ($\Omega$) | Average Case ($\Theta$) | Worst Case ($O$) | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Iterative Binary Search** | $\Omega(1)$ (hit at initial `mid`) | $\Theta(\log N)$ | $O(\log N)$ | $O(1)$ |
| **Recursive Binary Search** | $\Omega(1)$ | $\Theta(\log N)$ | $O(\log N)$ | $O(\log N)$ call stack |

---

## 5. Practical Examples (3 Complete Programs)

### Example 1: Iterative vs Recursive Binary Search & Halving Trace (`example_01_iterative_and_recursive_binary_search.py`)
```python
def binary_search_iterative(
    arr: list[int], target: int, trace: bool = False
) -> tuple[int, int]:
    low = 0
    high = len(arr) - 1
    step = 0

    while low <= high:
        step += 1
        mid = low + (high - low) // 2
        mid_val = arr[mid]

        if trace:
            window_size = high - low + 1
            print(
                f"  Step {step}: low={low:>2}, high={high:>2} (window={window_size:>2}) "
                f"-> mid={mid:>2} (arr[mid]={mid_val})"
            )

        if mid_val == target:
            return mid, step
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1, step
```

### Example 2: Order-Agnostic Binary Search & `bisect` Module (`example_02_order_agnostic_and_bisect_module.py`)
```python
def order_agnostic_binary_search(arr: list[int], target: int) -> int:
    if not arr:
        return -1

    low = 0
    high = len(arr) - 1
    is_ascending = arr[low] <= arr[high]

    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            return mid

        if is_ascending:
            if arr[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        else:
            if arr[mid] < target:
                high = mid - 1
            else:
                low = mid + 1

    return -1
```

### Example 3: Floor, Ceiling, and Continuous Binary Search (`example_03_floor_ceiling_and_continuous_binary_search.py`)
```python
def find_floor_and_ceiling(
    arr: list[int], target: int
) -> tuple[int | None, int | None]:
    low = 0
    high = len(arr) - 1
    floor_val: int | None = None
    ceiling_val: int | None = None

    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            return arr[mid], arr[mid]
        elif arr[mid] < target:
            floor_val = arr[mid]
            low = mid + 1
        else:
            ceiling_val = arr[mid]
            high = mid - 1

    return floor_val, ceiling_val
```

---

## 6. Verified Console Output

### Output of `example_01_iterative_and_recursive_binary_search.py`
```text
========================================================================
1. STEP-BY-STEP BINARY SEARCH HALVING TRACE (N = 16)
========================================================================
Sorted Array: [105, 112, 128, 144, 159, 173, 188, 204, 219, 235, 250, 268, 281, 297, 310, 325]

Tracing search for target = 281 (Present at index 12):
  Step 1: low= 0, high=15 (window=16) -> mid= 7 (arr[mid]=204)
  Step 2: low= 8, high=15 (window= 8) -> mid=11 (arr[mid]=268)
  Step 3: low=12, high=15 (window= 4) -> mid=13 (arr[mid]=297)
  Step 4: low=12, high=12 (window= 1) -> mid=12 (arr[mid]=281)
-> Result: Found at index 12 in 4 steps (log2(16) = 4)

Tracing search for target = 190 (Missing element):
  Step 1: low= 0, high=15 (window=16) -> mid= 7 (arr[mid]=204)
  Step 2: low= 0, high= 6 (window= 7) -> mid= 3 (arr[mid]=144)
  Step 3: low= 4, high= 6 (window= 3) -> mid= 5 (arr[mid]=173)
  Step 4: low= 6, high= 6 (window= 1) -> mid= 6 (arr[mid]=188)
-> Result: Not found (-1) after 4 steps

========================================================================
2. ITERATIVE O(1) SPACE vs RECURSIVE O(log N) STACK SPACE
========================================================================
Query 105 -> Index:  0 | Iterative Steps: 4 | Recursive Stack Depth: 4
Query 204 -> Index:  7 | Iterative Steps: 1 | Recursive Stack Depth: 1
Query 325 -> Index: 15 | Iterative Steps: 5 | Recursive Stack Depth: 5
Query 999 -> Index: -1 | Iterative Steps: 5 | Recursive Stack Depth: 5
```

### Output of `example_02_order_agnostic_and_bisect_module.py`
```text
========================================================================
1. ORDER-AGNOSTIC BINARY SEARCH (ASCENDING & DESCENDING)
========================================================================
Ascending Array  : [10, 25, 40, 55, 70, 85, 100]
  Search 70      -> Index: 4
Descending Array : [980, 850, 720, 610, 500, 390, 210]
  Search 720     -> Index: 2
  Search 390     -> Index: 5

========================================================================
2. PYTHON'S BUILT-IN `bisect` MODULE (`bisect_left` vs `bisect_right`)
========================================================================
Sorted Scores          : [60, 70, 70, 70, 80, 90]
bisect_left(scores, 70): 1 (First index >= 70)
bisect_right(scores,70): 4 (First index >  70)
Count of 70s in O(logN): right_pos - left_pos = 3

========================================================================
3. TABLE LOOKUP WITH `bisect_right` (CREDIT SCORE TIERS)
========================================================================
  Credit Score 520 -> Tier: Poor
  Credit Score 580 -> Tier: Fair
  Credit Score 669 -> Tier: Fair
  Credit Score 705 -> Tier: Good
  Credit Score 740 -> Tier: Very Good
  Credit Score 815 -> Tier: Exceptional
```

### Output of `example_03_floor_ceiling_and_continuous_binary_search.py`
```text
========================================================================
1. FINDING FLOOR AND CEILING IN A SORTED ARRAY O(log N)
========================================================================
Available Server RAM Capacities (GB): [16, 32, 64, 128, 256, 512]

  Requested  10 GB -> Floor (<= req): None GB | Ceiling (>= req):   16 GB
  Requested  32 GB -> Floor (<= req):   32 GB | Ceiling (>= req):   32 GB
  Requested  50 GB -> Floor (<= req):   32 GB | Ceiling (>= req):   64 GB
  Requested 100 GB -> Floor (<= req):   64 GB | Ceiling (>= req):  128 GB
  Requested 256 GB -> Floor (<= req):  256 GB | Ceiling (>= req):  256 GB
  Requested 600 GB -> Floor (<= req):  512 GB | Ceiling (>= req): None GB

========================================================================
2. CONTINUOUS BINARY SEARCH ( FLOATING-POINT SQUARE ROOT )
========================================================================
  sqrt(  2.00) -> Approx: 1.414213562 | Actual: 1.414213562 | Bisection Steps: 31
  sqrt( 49.00) -> Approx: 7.000000000 | Actual: 7.000000000 | Bisection Steps: 36
  sqrt(  0.25) -> Approx: 0.500000000 | Actual: 0.500000000 | Bisection Steps: 30
  sqrt(1000.00) -> Approx: 31.622776602 | Actual: 31.622776602 | Bisection Steps: 40
```

---

## 7. Code Explanation

1. **Why `mid = low + (high - low) // 2` Instead of `(low + high) // 2`?**
   In languages with fixed 32-bit signed integers (C, C++, Java, Go `int32`), if `low` and `high` are both near $2 \times 10^9$, their sum `low + high` exceeds $2^{31} - 1$ ($2,147,483,647$) and overflows to a **negative number**! Even though Python `int` has arbitrary precision, writing `low + (high - low) // 2` is a universal engineering best practice expected in coding interviews.
2. **Why `while low <= high:` (with `<=`)?**
   When `low == high`, the window still contains **1 uninspected element** (`arr[low]`). Using `while low < high:` in standard binary search skips checking that final single-element window (see Example 1 where `target = 281` was found on Step 4 when `low = 12, high = 12`).
3. **Continuous Binary Search Bound for $0 < x < 1$:**
   When computing $\sqrt{x}$ for $x = 0.25$, notice that $\sqrt{0.25} = 0.5 > 0.25$. Setting `high = max(1.0, number)` ensures the true square root always lies inside `[0.0, high]`.

---

## 8. Common Mistakes

1. **Infinite Loop from Setting `low = mid` or `high = mid` in a `while low <= high:` Loop:**
   If `low == high == 5` and `arr[5] < target`, setting `low = mid` keeps `low = 5` forever! Always exclude `mid` (`low = mid + 1` and `high = mid - 1`) once `arr[mid] != target` has been verified.
2. **Slicing the Array in Recursive Binary Search (`binary_search(arr[:mid], target)`):**
   In Python, slicing `arr[:mid]` allocates and copies $\frac{N}{2}$ elements, turning a fast $O(\log N)$ algorithm into an **$O(N)$ time and $O(N)$ space** algorithm! Always pass `low` and `high` index bounds instead of slicing.
3. **Running Binary Search on an Unsorted List:**
   Binary search assumes global monotonicity. If the input list is unsorted, `arr[mid] < target` tells you nothing about which half contains `target`.

---

## 9. Practice Questions

1. **Easy — Search Insert Position (LeetCode 35):** Given a sorted array of distinct integers `nums` and a `target` value, return the index if `target` is found. If not, return the index where it would be inserted in order. Verify that at termination of standard binary search (`while low <= high:`), the pointer `low` **always** equals the exact insertion index (`bisect_left`)!
2. **Medium — Search a 2D Sorted Matrix (LeetCode 74):** You are given an $R \times C$ matrix where each row is sorted left-to-right and the first integer of each row is greater than the last integer of the previous row. Write a single binary search over virtual indices `[0 .. R * C - 1]` using `row = mid // C` and `col = mid % C` in $O(\log(R \cdot C))$ time and $O(1)$ space.
3. **Hard — Valid Perfect Square & Integer Cube Root Without `math`:** Write two functions `is_perfect_square(n: int) -> bool` and `integer_cbrt(n: int) -> int` (returning $\lfloor \sqrt[3]{n} \rfloor$) using pure integer binary search in $O(\log n)$ time.

---

## 10. Interview Questions

### Q1: Why did Joshua Bloch (author of Java's `Arrays.binarySearch`) famously write that his binary search implementation in the JDK had a bug for 9 years?
**Answer:**
He wrote `int mid = (low + high) / 2;`. When arrays grew past $2^{30}$ elements ($\approx 1.07$ billion), `low + high` overflowed a 32-bit signed integer into a negative value, throwing `ArrayIndexOutOfBoundsException`. The fix is `low + (high - low) // 2` (or `(low + high) >>> 1` in Java).

### Q2: Can we use Binary Search on a Sorted Singly Linked List to get $O(\log N)$ search time?
**Answer:**
**No!** Even though a sorted linked list needs only $O(\log N)$ *comparisons*, jumping to the middle node `mid` requires traversing $\frac{N}{2} + \frac{N}{4} + \frac{N}{8} + \dots = O(N)$ `.next` pointers because linked lists lack $O(1)$ random index access. To get $O(\log N)$ search on linked structures, you need a **Skip List** or a **Balanced Binary Search Tree (AVL / Red-Black Tree)**.

### Q3: Is Ternary Search ($\log_3 N$ divisions) faster than Binary Search ($\log_2 N$ divisions) for searching a sorted array?
**Answer:**
**No — Ternary Search actually does MORE comparisons in the worst case!**
- Binary Search performs **1** comparison per step to shrink $N$ by $\frac{1}{2}$: $\approx 1 \cdot \log_2 N$ comparisons.
- Ternary Search checks two midpoints (`mid1`, `mid2`), requiring **2** comparisons per step to shrink $N$ by $\frac{1}{3}$: $\approx 2 \cdot \log_3 N = \frac{2}{\log_2 3} \log_2 N \approx 1.26 \log_2 N$ comparisons (26% more work!). Ternary search is only used for finding the maximum/minimum of unimodal functions.
