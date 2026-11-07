# Phase 6 — Section A: Complexity Analysis — Topic 04: Best, Average and Worst Cases

## 1. Introduction

For many algorithms, the number of operations executed depends not only on the **size** of the input $N$, but also on the **arrangement or values** of the input data:
- **Best Case:** The minimum operations required over any valid input of size $N$ (most favorable input).
- **Average Case:** The expected number of operations averaged across a realistic probability distribution of inputs of size $N$.
- **Worst Case:** The maximum operations required over any valid input of size $N$ (most adversarial input—provides a hard performance guarantee).
- **Amortized Case:** The guaranteed average cost per operation over a worst-case sequence of $M$ consecutive operations on a data structure.

---

## 2. Why is it used?

1. **SLA & Real-Time Guarantees (Worst Case):** Safety-critical systems and public APIs care about worst-case bounds so an attacker cannot craft a "pathological input" (like a hash-collision DoS or reverse-sorted QuickSort input) that freezes the server.
2. **Practical Throughput (Average & Amortized Case):** Hash tables (`dict`/`set`) have $O(n)$ worst-case lookup on hash collisions, yet in practice run in $O(1)$ average time; dynamic arrays (`list.append`) have $O(n)$ worst-case resize spikes, yet guarantee $O(1)$ **amortized** time.
3. **Adaptive Optimization (Best Case):** Algorithms like **Insertion Sort** and Python's **Timsort** exploit pre-existing order in the input to achieve $O(n)$ best-case time on already-sorted or nearly-sorted data.

---

## 3. Syntax

```text
Summary Table of Best, Average, and Worst Cases:
+----------------------+-------------+--------------+-------------+------------------+
| Algorithm / Op       | Best Case   | Average Case | Worst Case  | Auxiliary Space  |
+----------------------+-------------+--------------+-------------+------------------+
| Linear Search        | O(1)        | O(n)         | O(n)        | O(1)             |
| Binary Search        | O(1)        | O(log n)     | O(log n)    | O(1)             |
| Insertion Sort       | O(n)        | O(n^2)       | O(n^2)      | O(1)             |
| Merge Sort           | O(n log n)  | O(n log n)   | O(n log n)  | O(n)             |
| Quick Sort (random)  | O(n log n)  | O(n log n)   | O(n^2)      | O(log n)         |
| Python `list.append` | O(1)        | O(1) amort.  | O(n) resize | O(1) amort.      |
| Python `dict` lookup | O(1)        | O(1)         | O(n) collis.| O(1)             |
+----------------------+-------------+--------------+-------------+------------------+
```

---

## 4. Explanation (Step-by-Step)

1. **Best, Average, and Worst Case on Linear Search:**
   - **Best Case ($O(1)$):** `target == arr[0]`; finishes in 1 comparison.
   - **Worst Case ($O(n)$):** `target == arr[n - 1]` or `target` is not in `arr`; requires $n$ comparisons.
   - **Average Case ($O(n)$):** Assuming `target` is equally likely to be at any index $0 \dots n-1$, expected comparisons $= \frac{1 + 2 + \dots + n}{n} = \frac{n + 1}{2} = \Theta(n)$.
2. **Amortized Analysis (`list.append()`):**
   - How does Amortized differ from Average Case?
     - **Average Case** assumes a *probability distribution over random inputs*.
     - **Amortized Analysis** makes **zero probability assumptions**—it proves a deterministic upper bound on the total cost of any sequence of $M$ operations divided by $M$.
   - When a dynamic array doubles its capacity at sizes $1, 2, 4, 8, \dots, 2^k = N$, the total number of elements copied across all resizes is:
     $$1 + 2 + 4 + 8 + \dots + \frac{N}{2} = N - 1 < N$$
     Adding the $N$ normal element writes gives $< 2N$ total operations for $N$ appends $\implies \frac{2N}{N} = O(1)$ amortized cost per append!

---

## 5. Minimum 3 Examples

### Example 01: Best, Average, and Worst Case Comparisons in Linear Search
File: [`example_01_linear_search_best_average_worst.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/A_Complexity_Analysis/04_Best_Average_and_Worst_Cases/example_01_linear_search_best_average_worst.py)

```python
"""
Phase 6 - Section A (Complexity Analysis) - Topic 04: Best, Average and Worst Cases
Example 01: Best, Average, and Worst Case Comparisons in Linear Search & Early-Exit Bubble Check

Demonstrates:
  - Best Case Omega(1): target found at index 0 on the very first comparison
  - Average Case Theta(n): target equally likely at any index (`~(n + 1) / 2` comparisons)
  - Worst Case O(n): target at last index `n - 1` or absent (`n` comparisons)
"""


def linear_search_with_count(arr: list[int], target: int) -> tuple[int, int]:
    """Return `(found_index_or_neg1, comparisons_made)`."""
    comparisons = 0
    for idx, val in enumerate(arr):
        comparisons += 1
        if val == target:
            return idx, comparisons
    return -1, comparisons


def main() -> None:
    data = list(range(10, 110, 10))  # [10, 20, ..., 100] (N = 10)

    print("=== Best, Average, and Worst Case of Linear Search (N = 10) ===")
    _, best_comps = linear_search_search_best = linear_search_with_count(data, 10)
    _, worst_comps = linear_search_with_count(data, 999)
    avg_comps = sum(linear_search_with_count(data, x)[1] for x in data) / len(data)

    print(f"  Best Case  (target=10 at idx 0)  : {best_comps} comparison   -> Omega(1)")
    print(f"  Average    (across all 10 hits)  : {avg_comps:.1f} comparisons -> Theta(n)")
    print(f"  Worst Case (target=999 absent)   : {worst_comps} comparisons  -> O(n)")


if __name__ == "__main__":
    main()
```

### Example 02: Amortized Analysis — Dynamic Array (`list.append`) Resizing Cost
File: [`example_02_amortized_dynamic_array_append.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/A_Complexity_Analysis/04_Best_Average_and_Worst_Cases/example_02_amortized_dynamic_array_append.py)

```python
"""
Phase 6 - Section A (Complexity Analysis) - Topic 04: Best, Average and Worst Cases
Example 02: Amortized Analysis — Dynamic Array (`list.append`) Resizing Cost

Demonstrates:
  - Why an operation with O(n) worst-case spikes (when a dynamic array doubles capacity
    and copies all elements) still has O(1) **amortized** cost per `.append()`
"""


def simulate_dynamic_array_appends(total_inserts: int) -> None:
    """Simulate a geometric 2x capacity-doubling dynamic array and count total element copies."""
    capacity = 1
    size = 0
    total_work = 0
    resize_events: list[tuple[int, int, int]] = []

    for i in range(1, total_inserts + 1):
        if size == capacity:
            # Worst-case spike: allocate 2x array and copy `size` existing elements
            copy_cost = size
            capacity *= 2
            total_work += copy_cost
            resize_events.append((i, capacity, copy_cost))
        # Normal O(1) write into pre-allocated slot
        size += 1
        total_work += 1

    print(f"=== Dynamic Array Simulation ({total_inserts} Appends) ===")
    for step, new_cap, copied in resize_events:
        print(f"  Append #{step:>2}: resized capacity to {new_cap:>2} (copied {copied:>2} existing items)")
    print(f"  Total work across {total_inserts} appends : {total_work} operations")
    print(f"  Amortized cost per append   : {total_work / total_inserts:.2f} ops/append (<= 3 -> O(1) amortized!)")


def main() -> None:
    simulate_dynamic_array_appends(17)


if __name__ == "__main__":
    main()
```

### Example 03: Input-Distribution Sensitivity — Insertion Sort Best Case $O(n)$ vs Worst Case $O(n^2)$
File: [`example_03_insertion_sort_input_sensitivity.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/A_Complexity_Analysis/04_Best_Average_and_Worst_Cases/example_03_insertion_sort_input_sensitivity.py)

```python
"""
Phase 6 - Section A (Complexity Analysis) - Topic 04: Best, Average and Worst Cases
Example 03: Input-Distribution Sensitivity — Insertion Sort Best Case O(n) vs Worst Case O(n^2)

Demonstrates:
  - How the exact same algorithm runs in O(n) on already-sorted input (Best Case)
    and O(n^2) on reverse-sorted input (Worst Case)
"""


def insertion_sort_shift_count(arr: list[int]) -> int:
    """Sort `arr` copy via Insertion Sort and return total inner-loop element shifts."""
    a = list(arr)
    shifts = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            shifts += 1
            j -= 1
        a[j + 1] = key
    return shifts


def main() -> None:
    n = 20
    already_sorted = list(range(n))
    reverse_sorted = list(range(n - 1, -1, -1))

    best_shifts = insertion_sort_shift_count(already_sorted)
    worst_shifts = insertion_sort_shift_count(reverse_sorted)
    theoretical_worst = (n * (n - 1)) // 2

    print(f"=== Insertion Sort Shift Counts (N = {n}) ===")
    print(f"  Best Case  (already sorted) : {best_shifts:>3} shifts (O(n) total comparisons, 0 shifts)")
    print(f"  Worst Case (reverse sorted) : {worst_shifts:>3} shifts (matches n*(n-1)/2 = {theoretical_worst} -> O(n^2))")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 01
```text
=== Best, Average, and Worst Case of Linear Search (N = 10) ===
  Best Case  (target=10 at idx 0)  : 1 comparison   -> Omega(1)
  Average    (across all 10 hits)  : 5.5 comparisons -> Theta(n)
  Worst Case (target=999 absent)   : 10 comparisons  -> O(n)
```

### Output — Example 02
```text
=== Dynamic Array Simulation (17 Appends) ===
  Append # 2: resized capacity to  2 (copied  1 existing items)
  Append # 3: resized capacity to  4 (copied  2 existing items)
  Append # 5: resized capacity to  8 (copied  4 existing items)
  Append # 9: resized capacity to 16 (copied  8 existing items)
  Append #17: resized capacity to 32 (copied 16 existing items)
  Total work across 17 appends : 48 operations
  Amortized cost per append   : 2.82 ops/append (<= 3 -> O(1) amortized!)
```

### Output — Example 03
```text
=== Insertion Sort Shift Counts (N = 20) ===
  Best Case  (already sorted) :   0 shifts (O(n) total comparisons, 0 shifts)
  Worst Case (reverse sorted) : 190 shifts (matches n*(n-1)/2 = 190 -> O(n^2))
```

---

## 7. Code Explanation

1. **Average Case $\frac{n + 1}{2}$ (Example 01):** For $N = 10$, averaging the comparison counts across all 10 element positions gives $\frac{10 + 1}{2} = 5.5$ comparisons.
2. **Geometric Doubling $1 + 2 + 4 + 8 + 16 = 31$ (Example 02):** Even on the 17th append—immediately after the most expensive resize spike (`16` copies)—total work across all 17 appends is only $17 + 31 = 48 \implies 2.82 \le 3$ operations per append.
3. **Insertion Sort Shift Count (Example 03):** On `already_sorted`, the `while j >= 0 and a[j] > key:` check fails immediately on every iteration (`0` shifts), whereas on `reverse_sorted` every element shifts all the way to index `0` ($\sum_{i=1}^{19} i = 190$ shifts).

---

## 8. Common Mistakes

1. **Adding a Constant Number of Slots (`capacity += 100`) Instead of Geometric Multiplication (`capacity *= 2`) When Resizing:**
   - If a dynamic array grows by a fixed constant $+K$ each time it fills up, resizing happens at $K, 2K, 3K, \dots, N$, costing $K(1 + 2 + \dots + N/K) = \Theta(N^2 / K)$ total copies—which degrades `.append()` to **$O(n)$ amortized time**! Geometric growth ($\times 2$ or CPython's $\approx \times 1.125$) is mandatory for $O(1)$ amortized time.
2. **Assuming QuickSort Is Always $O(n \log n)$ With Naive First/Last Pivot Selection:**
   - Choosing `arr[0]` or `arr[-1]` as the pivot causes QuickSort to degrade to **$O(n^2)$ worst case** when given an already-sorted array! Using a random pivot or median-of-three (`arr[low]`, `arr[mid]`, `arr[high]`) avoids this trap.

---

## 9. Practice Questions

1. **Easy:** Modify Example 02 so the array grows by an additive constant `capacity += 4` instead of `capacity *= 2`, and show how the amortized cost per append grows linearly as `total_inserts` increases from `16` to `256`.
2. **Medium:** Implement a Queue using **two Python lists** (`in_stack` and `out_stack`) where `.enqueue(x)` appends to `in_stack` and `.dequeue()` pops from `out_stack` (refilling `out_stack` by popping all of `in_stack` only when `out_stack` is empty). Prove why `.dequeue()` is $O(n)$ worst-case but **$O(1)$ amortized**!
3. **Hard:** Count how many comparisons QuickSort makes on `list(range(20))` when choosing `arr[-1]` as the pivot vs choosing the middle element `arr[(low + high) // 2]`.

---

## 10. Interview Questions

### Q1: What is the difference between Average-Case Complexity and Amortized Complexity?
**Answer:**
- **Average-Case Complexity** relies on a probabilistic assumption about the input distribution (e.g., assuming keys are uniformly hashed or array permutations are equally likely). An adversary can still trigger the worst case on every single call.
- **Amortized Complexity** makes **no probabilistic assumptions**—even if an adversary chooses the worst possible sequence of $M$ operations, the total cost of the entire sequence is guaranteed to be at most $M \times (\text{amortized cost})$ because expensive operations (like array doubling or stack transfer) can only happen after enough cheap operations have "paid into the bank."

### Q2: Why does CPython's `dict` randomize hash seeds (`PYTHONHASHSEED`) on startup?
**Answer:** While `dict` lookup is $O(1)$ average case, it is $O(n)$ in the worst case if all keys collide into the same hash bucket. Prior to hash randomization (PEP 456), attackers could send an HTTP JSON payload with thousands of precomputed colliding keys, triggering $O(n^2)$ hash table insertion and causing a Denial-of-Service (HashDoS). Randomizing the SipHash seed per process makes collision crafting infeasible.

### Q3: Which sorting algorithm has $O(n \log n)$ time in the Best, Average, AND Worst cases while using $O(1)$ auxiliary space?
**Answer:** **Heap Sort** runs in $\Theta(n \log n)$ in best, average, and worst cases and operates in-place in $O(1)$ auxiliary space (though in practice Timsort and QuickSort have better CPU cache locality).
