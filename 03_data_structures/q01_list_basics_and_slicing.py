"""
Topic 03: Data Structures
Question 01: List Basics and Slicing (Deep Dive)

Master Python lists: indexing boundaries, slice syntax [start:stop:step],
slice assignment & in-place mutations, shallow vs deep copying, sliding windows,
cyclic rotation, dynamic resizing memory growth, and time-series resampling.
"""

import copy
import sys
from typing import Any

# ============================================================
# Q1: Indexing Mechanics and Boundary Error Handling
# ============================================================
# Question: Demonstrate positive and negative indexing across heterogeneous lists.
# Handle IndexError gracefully when accessing out-of-bounds positions.

print("=== Q1: List Indexing & Boundaries ===")

heterogeneous_list = ["Python", 3.13, True, [10, 20], {"role": "admin"}, None]

print(f"  List length: {len(heterogeneous_list)}")
print(f"  First element (index 0):   {heterogeneous_list[0]}")
print(f"  Last element (index -1):   {heterogeneous_list[-1]}")
print(f"  Nested element [3][1]:     {heterogeneous_list[3][1]}")

def safe_get(lst: list, index: int, default: Any = None) -> Any:
    """Safely retrieves an element by index without crashing on out-of-bounds."""
    try:
        return lst[index]
    except IndexError:
        return default

print(f"  safe_get(index 2):         {safe_get(heterogeneous_list, 2)}")
print(f"  safe_get(index 100):       {safe_get(heterogeneous_list, 100, default='<OUT OF BOUNDS>')}")
print(f"  safe_get(index -10):       {safe_get(heterogeneous_list, -10, default='<OUT OF BOUNDS>')}")

# Explanation: Negative indices count backward from the end: `-1` is the last item,
# `-len(lst)` is the first item. Accessing indices outside `[-len, len - 1]` raises `IndexError`.


# ============================================================
# Q2: Comprehensive Slice Syntax ([start:stop:step])
# ============================================================
# Question: Demonstrate all variations of the slice syntax: default endpoints,
# positive/negative steps, full reversals, and show that slicing NEVER raises IndexError.

print("\n=== Q2: Slice Syntax Variations ===")

data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(f"  Original:          {data}")
print(f"  data[2:7]:         {data[2:7]}        (indices 2 through 6)")
print(f"  data[:4]:          {data[:4]}         (first 4 elements)")
print(f"  data[6:]:          {data[6:]}         (from index 6 to end)")
print(f"  data[::2]:         {data[::2]}        (every 2nd element / evens)")
print(f"  data[1::2]:        {data[1::2]}        (every 2nd starting at 1 / odds)")
print(f"  data[::-1]:        {data[::-1]}  (reversed full list)")
print(f"  data[7:2:-1]:      {data[7:2:-1]}        (reverse slice from 7 down to 3)")

# Slicing is tolerant to out-of-bounds indices (no exception raised!)
print(f"  data[5:1000]:      {data[5:1000]}        (out-of-bounds stop is safely clamped)")
print(f"  data[-100:3]:      {data[-100:3]}        (out-of-bounds negative start clamped to 0)")
print(f"  data[50:100]:      {data[50:100]}                 (empty slice if completely beyond range)")

# Explanation: In slicing, `[start:stop:step]`, `start` is inclusive and `stop` is exclusive.
# Slices gracefully clip out-of-bounds bounds to `[0, len(lst)]` without raising exceptions.


# ============================================================
# Q3: Slice Assignment and In-Place List Mutation
# ============================================================
# Question: Demonstrate mutating lists in-place using slice assignment:
# Replacing a sub-range with different lengths, inserting items without overwriting,
# deleting slices, and clearing lists while preserving object identity.

print("\n=== Q3: Slice Assignment & In-Place Resizing ===")

numbers = [10, 20, 30, 40, 50, 60]
orig_id = id(numbers)
print(f"  Initial:                        {numbers} (id: {orig_id})")

# 1. Replace slice [1:4] (20, 30, 40) with fewer or more elements
numbers[1:4] = [222, 333, 444, 555]
print(f"  Replaced [1:4] with 4 items:    {numbers}")

# 2. Insert items without replacing any existing elements (empty slice insertion)
numbers[2:2] = ["INSERTED_A", "INSERTED_B"]
print(f"  Inserted at empty slice [2:2]:  {numbers}")

# 3. Delete slice using empty list assignment or del
del numbers[2:4]
print(f"  After 'del numbers[2:4]':       {numbers}")

# 4. In-place clear using [:]
numbers[:] = [1, 2, 3]
print(f"  In-place clear & replace [:]:   {numbers} (id: {id(numbers)})")
print(f"  Object identity preserved:      {id(numbers) == orig_id}")

# Explanation: `lst[start:stop] = iterable` replaces the slice in-place, dynamically
# expanding or contracting the underlying array while keeping the same list instance.


# ============================================================
# Q4: Shallow Copy vs Deep Copy Mechanics
# ============================================================
# Question: Prove the critical difference between shallow copying (`lst[:]`, `lst.copy()`)
# and deep copying (`copy.deepcopy()`) when dealing with nested mutable structures.

print("\n=== Q4: Shallow Copy vs Deep Copy ===")

original = ["Project A", [100, 200], {"status": "ACTIVE"}]

# Shallow copies
shallow_slice = original[:]
shallow_method = original.copy()

# Deep copy
deep_cloned = copy.deepcopy(original)

# Mutate top-level element: only affects original
original[0] = "Project MODIFIED"

# Mutate nested mutable list and dictionary:
original[1].append(300)
original[2]["status"] = "CLOSED"

print("  After mutating original's nested structures:")
print(f"    Original:       {original}")
print(f"    Shallow slice:  {shallow_slice}  <- NESTED OBJECTS MUTATED!")
print(f"    Deep copied:    {deep_cloned}  <- UNTOUCHED & ISOLATED")

# Verify memory IDs
print(f"    Original nested list id:    {id(original[1])}")
print(f"    Shallow nested list id:     {id(shallow_slice[1])} (IDENTICAL - Shared reference)")
print(f"    Deep copied nested list id: {id(deep_cloned[1])} (DISTINCT - Completely independent)")

# Explanation: Shallow copies duplicate only the outermost container; nested mutable
# objects remain shared references. `copy.deepcopy()` recursively duplicates all nested objects.


# ============================================================
# Q5: Sliding Window Extraction via Slicing
# ============================================================
# Question: Implement a sliding window generator that slides a window of size `K`
# across a sequence with step size `S`, calculating moving averages.

print("\n=== Q5: Sliding Window Generator ===")

def sliding_window(sequence: list, window_size: int, step: int = 1) -> list[list]:
    """Generates consecutive overlapping windows across sequence."""
    if window_size <= 0 or step <= 0:
        raise ValueError("window_size and step must be positive")
    
    windows = []
    for i in range(0, len(sequence) - window_size + 1, step):
        windows.append(sequence[i : i + window_size])
    return windows

daily_temperatures = [20, 22, 21, 24, 27, 26, 25, 23, 22]
window_len = 3
windows = sliding_window(daily_temperatures, window_len, step=1)

print(f"  Dataset: {daily_temperatures}")
print(f"  Moving {window_len}-day windows:")
for idx, win in enumerate(windows, start=1):
    avg = sum(win) / len(win)
    print(f"    Window #{idx}: {win} -> Moving Average = {avg:.2f}")

# Explanation: `sequence[i : i + window_size]` cleanly extracts each slice without
# manual element-by-element buffer copying.


# ============================================================
# Q6: Cyclic Array Rotation with Slicing
# ============================================================
# Question: Rotate a list by K positions to the left or right in O(N) time
# using slice concatenation, handling K values greater than the list length.

print("\n=== Q6: Cyclic Array Rotation ===")

def rotate_list(arr: list, k: int, direction: str = "right") -> list:
    """Rotates list by k positions to 'left' or 'right' using slicing."""
    if not arr:
        return []
        
    n = len(arr)
    k = k % n  # Normalize k if greater than array length
    
    if k == 0:
        return arr[:]
        
    if direction.lower() == "right":
        # Right rotation: tail of k elements moves to front
        return arr[-k:] + arr[:-k]
    elif direction.lower() == "left":
        # Left rotation: head of k elements moves to back
        return arr[k:] + arr[:k]
    else:
        raise ValueError("Direction must be 'left' or 'right'")

sample = [1, 2, 3, 4, 5, 6, 7]
print(f"  Initial List:            {sample}")
print(f"  Rotate Right by 3:       {rotate_list(sample, 3, 'right')}")
print(f"  Rotate Left by 2:        {rotate_list(sample, 2, 'left')}")
print(f"  Rotate Right by 10 (10%7=3): {rotate_list(sample, 10, 'right')}")

# Explanation: Slicing `arr[-k:] + arr[:-k]` splits the array at the pivot point
# and concatenates the two halves in swapped order in $O(N)$ time.


# ============================================================
# Q7: Strided Subsequences and Interleaving
# ============================================================
# Question: Use strided slices (`step = 2`) to extract even-indexed and odd-indexed
# elements, and demonstrate how to zip and recombine them.

print("\n=== Q7: Strided Subsequences and Interleaving ===")

alphabet_sample = ["A", "B", "C", "D", "E", "F", "G", "H"]

even_indexed = alphabet_sample[0::2]  # Step of 2 starting at 0
odd_indexed = alphabet_sample[1::2]   # Step of 2 starting at 1

print(f"  Original:      {alphabet_sample}")
print(f"  Even-indexed:  {even_indexed}")
print(f"  Odd-indexed:   {odd_indexed}")

# Interleave the two strided slices back together
reconstructed = []
for a, b in zip(even_indexed, odd_indexed):
    reconstructed.extend([a, b])
if len(even_indexed) > len(odd_indexed):
    reconstructed.append(even_indexed[-1])

print(f"  Interleaved:   {reconstructed}")
print(f"  Perfect match: {reconstructed == alphabet_sample}")

# Explanation: A step of 2 strides through alternate memory locations, enabling
# parallel channel separation (e.g. separating stereo audio left/right channels).


# ============================================================
# Q8: Reversing an Internal Sub-Segment
# ============================================================
# Question: Reverse a specific sub-array between indices `[left, right]` inclusive
# while leaving all other elements in their original positions.

print("\n=== Q8: Internal Sub-Segment Reversal ===")

def reverse_subsegment(arr: list, left: int, right: int) -> list:
    """Reverses elements between index left and right inclusive."""
    n = len(arr)
    # Clamp boundaries
    left = max(0, left)
    right = min(n - 1, right)
    
    if left >= right:
        return arr[:]
        
    # Head + Reversed Middle + Tail
    return arr[:left] + arr[left : right + 1][::-1] + arr[right + 1 :]

base_arr = [10, 20, 30, 40, 50, 60, 70, 80]
print(f"  Before:                           {base_arr}")
# Reverse middle range from index 2 to 5 ([30, 40, 50, 60] -> [60, 50, 40, 30])
reversed_mid = reverse_subsegment(base_arr, 2, 5)
print(f"  After reversing indices [2:5]:    {reversed_mid}")

# Explanation: Decomposing a sequence into three slices `prefix + middle[::-1] + suffix`
# allows arbitrary regional transformations without mutating unselected boundaries.


# ============================================================
# Q9: Dynamic Over-Allocation & Memory Resizing Semantics
# ============================================================
# Question: Inspect how Python lists dynamically over-allocate memory during `.append()`
# using `sys.getsizeof()`.

print("\n=== Q9: Dynamic Memory Over-Allocation ===")

growing_list = []
prev_size = sys.getsizeof(growing_list)

print(f"  Empty list size: {prev_size} bytes")
print("  Tracking memory reallocation jumps:")

for i in range(25):
    growing_list.append(i)
    current_size = sys.getsizeof(growing_list)
    if current_size != prev_size:
        allocated_slots = (current_size - 56) // 8  # 64-bit pointer size estimation
        print(f"    Length: {len(growing_list):>2} | Size: {current_size:>4} bytes | Capacity jumps to ~{allocated_slots} slots")
        prev_size = current_size

# Pre-allocated list vs dynamically grown list
preallocated = [0] * 100
appended = []
for x in range(100):
    appended.append(x)

print(f"\n  Size of pre-allocated [0]*100:  {sys.getsizeof(preallocated)} bytes")
print(f"  Size of appended 100 elements:  {sys.getsizeof(appended)} bytes")

# Explanation: CPython lists are dynamic arrays. To achieve amortized $O(1)$ appends,
# the underlying memory buffer grows non-linearly (growth pattern ~0, 4, 8, 16, 25, 35...).


# ============================================================
# Q10: Time-Series Tick Resampler (OHLC Candle Generator)
# ============================================================
# Question: Process an intraday stream of tick trades.
# Use slicing to chunk transactions into candle periods and extract OHLC
# (Open, High, Low, Close) plus Volume.

print("\n=== Q10: Time-Series OHLC Candle Generator ===")

trade_ticks = [
    # (price, volume)
    (150.25, 100), (150.80, 250), (150.10, 50),  (151.00, 300),  # Period 1
    (151.10, 150), (151.75, 400), (150.90, 80),  (151.50, 120),  # Period 2
    (151.40, 200), (152.00, 500), (151.20, 110), (152.30, 350),  # Period 3
]

TICKS_PER_BAR = 4
candle_bars = []

for bar_num, start_idx in enumerate(range(0, len(trade_ticks), TICKS_PER_BAR), start=1):
    chunk = trade_ticks[start_idx : start_idx + TICKS_PER_BAR]
    if not chunk:
        continue
        
    prices = [t[0] for t in chunk]
    volumes = [t[1] for t in chunk]
    
    candle = {
        "bar": bar_num,
        "open": chunk[0][0],        # First tick price
        "high": max(prices),        # Peak tick price
        "low": min(prices),         # Trough tick price
        "close": chunk[-1][0],      # Last tick price
        "total_volume": sum(volumes),
        "tick_count": len(chunk)
    }
    candle_bars.append(candle)

print(f"  {'Bar':<5} {'Open':<8} {'High':<8} {'Low':<8} {'Close':<8} {'Volume':<8}")
print("  " + "-" * 45)
for c in candle_bars:
    print(f"  #{c['bar']:<4} ${c['open']:<7.2f} ${c['high']:<7.2f} ${c['low']:<7.2f} ${c['close']:<7.2f} {c['total_volume']:<8}")

# Summary Output
print("\n" + "=" * 55)
print("  All 10 Questions for Topic 03 - Q01 executed successfully!")
print("=" * 55)
