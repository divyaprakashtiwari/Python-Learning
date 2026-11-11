# Section D: Arrays and Strings — Topic 01: Array Operations

## 1. Introduction

An **Array** (represented in Python by `list` for dynamic object references, or `array.array` / `bytearray` for unboxed C primitives) is a **contiguous block of memory** where elements are stored at consecutive indices `0, 1, ..., n - 1`.

Because the memory is contiguous, the CPU can compute the exact memory address of **any** index `i` in **$O(1)$ constant time** using a single multiplication and addition:
$$\text{Address}(i) = \text{Base\_Address} + i \times \text{Element\_Size}$$

However, this same contiguity creates a fundamental trade-off: inserting or deleting an element anywhere except the **very end** (`index n - 1`) requires **shifting** all subsequent elements to prevent gaps or overwrites, costing **$O(N)$ time**.

---

## 2. Why is it used?

1. **Unbeatable $O(1)$ Random Access & Hardware Cache Locality:**
   Contiguous arrays are the most CPU-friendly data structure in existence. When you read `arr[i]`, the CPU hardware prefetcher loads the next 64 bytes (8 consecutive 64-bit pointers/integers) into L1 cache automatically, making array loops 10x–50x faster than pointer-chasing linked lists.
2. **In-Place $O(1)$ Space Transformations:**
   Mastering in-place array operations — such as the **Three-Reversal Rotation Algorithm**, **Boyer-Moore Majority Vote**, and **Prefix/Suffix Product Accumulation** — lets you solve complex data transformations in a single $O(N)$ pass with zero extra memory allocation.

---

## 3. Syntax & Core Blueprints

### Time Complexity of Core Python `list` Operations

| Operation | Python Syntax | Time Complexity | Why? |
| :--- | :--- | :--- | :--- |
| **Random Read / Write** | `arr[i]` / `arr[i] = x` | $O(1)$ | Direct offset math: `base + i * 8` |
| **Append at End** | `arr.append(x)` | $O(1)$ amortized | Geometric over-allocation ($\sim 1.125\times$) |
| **Pop from End** | `arr.pop()` | $O(1)$ | Decrements length counter; 0 shifts |
| **Insert at Index `i`** | `arr.insert(i, x)` | $O(N - i) \to O(N)$ | Shifts `arr[i .. n-1]` right by 1 slot |
| **Pop at Index `i`** | `arr.pop(i)` / `del arr[i]` | $O(N - i) \to O(N)$ | Shifts `arr[i+1 .. n-1]` left by 1 slot |
| **Slice Copy** | `arr[a:b]` | $O(b - a)$ | Allocates new list and copies `b - a` refs |
| **Membership Search** | `x in arr` / `arr.index(x)` | $O(N)$ | Sequential linear scan |

### Blueprint: In-Place Right Rotation by $K$ Steps ($O(N)$ Time, $O(1)$ Space)
```python
def reverse_range(arr: list[int], left: int, right: int) -> None:
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1

def rotate_right(arr: list[int], k: int) -> None:
    n = len(arr)
    k %= n
    reverse_range(arr, 0, n - 1)  # 1. Reverse whole array
    reverse_range(arr, 0, k - 1)  # 2. Reverse first k elements
    reverse_range(arr, k, n - 1)  # 3. Reverse remaining n - k elements
```

---

## 4. Step-by-Step Explanation & Complexity Analysis

### 1. Why the Three-Reversal Rotation Algorithm Works in $O(N)$ Time and $O(1)$ Space
Suppose `arr = [1, 2, 3, 4, 5, 6, 7]` ($N = 7$) and we want to rotate right by $k = 3$ steps so the last $3$ elements `[5, 6, 7]` move to the front (`[5, 6, 7, 1, 2, 3, 4]`):
- Think of the array as two blocks $A = [1, 2, 3, 4]$ and $B = [5, 6, 7]$. We want $A B \to B A$.
- **Step 1 — Reverse all $(A B)^R = B^R A^R$:** `[7, 6, 5, 4, 3, 2, 1]` *(Now block $B^R = [7, 6, 5]$ is at the front and $A^R = [4, 3, 2, 1]$ is at the back!)*.
- **Step 2 — Reverse first $k$ elements $(B^R)^R = B$:** `[5, 6, 7, 4, 3, 2, 1]`.
- **Step 3 — Reverse last $n - k$ elements $(A^R)^R = A$:** `[5, 6, 7, 1, 2, 3, 4]`.
Each element is swapped twice $\rightarrow$ **$O(N)$ time and $O(1)$ space!**

### 2. Boyer-Moore Majority Vote Intuition ($O(N)$ Time, $O(1)$ Space)
If an element appears **strictly more than $\lfloor N / 2 \rfloor$ times**, it appears more often than **all other elements combined**. Pairing each occurrence of the majority element with a distinct non-majority element and cancelling them out (`count -= 1`) guarantees the majority element is the last candidate standing!

---

## 5. Practical Examples (3 Complete Programs)

### Example 1: Random Access & Insert/Delete Shift Counts (`example_01_random_access_and_insert_delete_shifts.py`)
```python
def insert_at_index_with_shift_count(
    arr: list[int], index: int, value: int
) -> tuple[list[int], int]:
    a = arr.copy()
    n = len(a)
    if not (0 <= index <= n):
        raise IndexError("Insertion index out of bounds")

    a.append(0)
    shifts = 0

    for j in range(n - 1, index - 1, -1):
        a[j + 1] = a[j]
        shifts += 1

    a[index] = value
    return a, shifts
```

### Example 2: In-Place Reversal & Three-Reverse $K$-Rotation (`example_02_in_place_reversal_and_k_rotation.py`)
```python
def rotate_right_in_place(arr: list[int], k: int, trace: bool = False) -> list[int]:
    a = arr.copy()
    n = len(a)
    if n <= 1:
        return a

    k = k % n
    if k == 0:
        return a

    reverse_subarray_in_place(a, 0, n - 1)
    reverse_subarray_in_place(a, 0, k - 1)
    reverse_subarray_in_place(a, k, n - 1)
    return a
```

### Example 3: Boyer-Moore Majority Vote & Product of Array Except Self (`example_03_boyer_moore_majority_and_product_except_self.py`)
```python
def product_except_self(nums: list[int]) -> list[int]:
    n = len(nums)
    answer = [1] * n

    prefix_prod = 1
    for i in range(n):
        answer[i] = prefix_prod
        prefix_prod *= nums[i]

    suffix_prod = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix_prod
        suffix_prod *= nums[i]

    return answer
```

---

## 6. Verified Console Output

### Output of `example_01_random_access_and_insert_delete_shifts.py`
```text
========================================================================
1. ARRAY INSERTION SHIFT COST BY POSITION (N = 8)
========================================================================
Original Array (N=8): [10, 20, 30, 40, 50, 60, 70, 80]

  Insert 99 at idx 0 (Front (Worst Case)      ) -> Shifts: 8 | Result: [99, 10, 20, 30, 40, 50, 60, 70, 80]
  Insert 99 at idx 4 (Middle (Index 4)        ) -> Shifts: 4 | Result: [10, 20, 30, 40, 99, 50, 60, 70, 80]
  Insert 99 at idx 8 (End / Append (Best Case)) -> Shifts: 0 | Result: [10, 20, 30, 40, 50, 60, 70, 80, 99]

========================================================================
2. ARRAY DELETION SHIFT COST BY POSITION (N = 8)
========================================================================
  Delete at idx 0 (Front pop(0) (Worst)  ) -> Removed 10, Shifts: 7 | Result: [20, 30, 40, 50, 60, 70, 80]
  Delete at idx 3 (Middle pop(3)         ) -> Removed 40, Shifts: 4 | Result: [10, 20, 30, 50, 60, 70, 80]
  Delete at idx 7 (Tail pop() (Best)     ) -> Removed 80, Shifts: 0 | Result: [10, 20, 30, 40, 50, 60, 70]
```

### Output of `example_02_in_place_reversal_and_k_rotation.py`
```text
========================================================================
1. IN-PLACE RIGHT ROTATION BY K STEPS (THREE-REVERSAL ALGORITHM)
========================================================================
Original Array (N=7): [1, 2, 3, 4, 5, 6, 7], Rotate Right by k = 3:

  Step 1 (Reverse all [0..6])     : [7, 6, 5, 4, 3, 2, 1]
  Step 2 (Reverse prefix [0..2])  : [5, 6, 7, 4, 3, 2, 1]
  Step 3 (Reverse suffix [3..6])  : [5, 6, 7, 1, 2, 3, 4]

Final Rotated Array   : [5, 6, 7, 1, 2, 3, 4]
Rotate by k = 10 (10 % 7 == 3): [5, 6, 7, 1, 2, 3, 4]
```

### Output of `example_03_boyer_moore_majority_and_product_except_self.py`
```text
========================================================================
1. BOYER-MOORE MAJORITY VOTE ALGORITHM (O(N) TIME, O(1) SPACE)
========================================================================
Votes [2, 2, 1, 1, 1, 2, 2] -> Majority (>3): 2
Votes [1, 2, 3, 1, 2, 3, 1] -> Majority (>3): None

========================================================================
2. PRODUCT OF ARRAY EXCEPT SELF (WITHOUT DIVISION, HANDLES ZEROS!)
========================================================================
  Input: [1, 2, 3, 4]         -> Product Except Self: [24, 12, 8, 6]
  Input: [-1, 1, 0, -3, 3]    -> Product Except Self: [0, 0, 9, 0, 0]
```

---

## 7. Code Explanation

1. **Why Insertion Shifts Right-to-Left (`range(n - 1, index - 1, -1)`), While Deletion Shifts Left-to-Right (`range(index, n - 1)`):**
   - If you shifted left-to-right during insertion (`a[j + 1] = a[j]` starting from `j = index`), you would overwrite `a[index + 1]` before copying it, filling the entire suffix with copies of `a[index]`! Shifting backward from `n - 1` down to `index` moves each element into an already-vacated slot.
   - Conversely, during deletion, `a[index]` is the vacated slot, so we shift forward from `j = index` up to `n - 2` (`a[j] = a[j + 1]`).
2. **Why `Product Except Self` Never Uses Division:**
   Dividing total product by `nums[i]` crashes with `ZeroDivisionError` whenever any element is `0` (like `[-1, 1, 0, -3, 3]`). Accumulating `prefix_prod` left-to-right and `suffix_prod` right-to-left handles single or multiple zeros naturally in $O(N)$ time and $O(1)$ extra space!

---

## 8. Common Mistakes

1. **Forgetting `k = k % len(arr)` Before Rotating an Array:**
   If `len(arr) == 7` and `k == 10`, calling `reverse_subarray_in_place(a, 0, k - 1)` without `k %= n` accesses `a[9]` and raises `IndexError`! Always normalize `k %= len(arr)` first.
2. **Deleting Elements While Iterating Forward Over the Same List:**
   Writing `for i in range(len(arr)): if cond(arr[i]): arr.pop(i)` both takes **$O(N^2)$ time** AND **skips elements** (because when index `i` is popped, the next element shifts down into index `i`, while the loop advances `i` to `i + 1`)! Use a list comprehension or Reader/Writer two pointers instead.

---

## 9. Practice Questions

1. **Easy — Left Rotation by $K$ Steps In-Place:** Modify the Three-Reversal Algorithm so that it rotates an array **left** by $k$ steps in $O(N)$ time and $O(1)$ space (either by reversing `[0..k-1]`, `[k..n-1]`, and `[0..n-1]`, or by observing that a left rotation by $k$ equals a right rotation by $n - (k \bmod n)$).
2. **Medium — Next Permutation In-Place (LeetCode 31):** Given an array of integers `nums`, rearrange it in-place into the lexicographically next greater permutation (or reverse to lowest sorted order if already descending) in $O(N)$ time and $O(1)$ space.
3. **Hard — First Missing Positive in $O(N)$ Time and $O(1)$ Space (LeetCode 41):** Given an unsorted integer array `nums`, find the smallest missing positive integer (`>= 1`) in $O(N)$ time and $O(1)$ auxiliary space by using cyclic index placement (`nums[i]` placed at index `nums[i] - 1` when `1 <= nums[i] <= n`).

---

## 10. Interview Questions

### Q1: If deleting from the middle of an array (`arr.pop(i)`) normally takes $O(N)$ time, when can you delete an arbitrary index `i` in $O(1)$ time?
**Answer:**
**When element order does NOT matter!** You can overwrite the deleted slot with the last element and pop the tail in **$O(1)$ time**:
```python
arr[i] = arr[-1]
arr.pop()
```
This "Swap-and-Pop" trick is used in randomized sets (`Insert Delete GetRandom O(1)`, LeetCode 380) and game entity pools.

### Q2: Why does Boyer-Moore Majority Vote require a 2nd verification pass when the problem does not guarantee a majority element exists?
**Answer:**
Phase 1 only guarantees that **if** a majority element exists, it will be the surviving `candidate`. If no majority exists (e.g., `[1, 2, 3]`), the last element `3` survives Phase 1 with `count = 1` even though it appeared only once! A single $O(N)$ `arr.count(candidate) > len(arr) // 2` check confirms whether `candidate` is a true majority.
