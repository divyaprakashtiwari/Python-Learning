"""
Topic 08: Modules and Packages - Question 07: itertools Module

A comprehensive collection of 10 standalone, runnable exercises exploring
Python's standard library `itertools` module: infinite iterators, combinatorial
generators, grouping, streaming filters, and windowed aggregation pipelines.

Questions Covered:
 1. Infinite Iterators: count(), cycle(), and repeat() for stream generation.
 2. Stream Slicing with islice(): Consuming bounded windows from arbitrary iterators.
 3. Chaining & Flattening: chain() and chain.from_iterable() for zero-copy joins.
 4. Selective Filtering: takewhile(), dropwhile(), and filterfalse() stream predicates.
 5. Grouping Streams with groupby(): Aggregating consecutive items by key function.
 6. Cartesian Products & Permutations: product() and permutations() combinatorics.
 7. Combinations & Multi-Choice: combinations() and combinations_with_replacement().
 8. Running Reductions with accumulate(): Running sums, maximums, and custom reductions.
 9. Iterator Duplication & Pairwise: tee() replication and itertools.pairwise() deltas.
10. Advanced Project: Stream Batcher & Time-Windowed Sliding Event Aggregator.
"""

from collections import defaultdict
import itertools
import operator
from typing import Any, Generator, Iterator


# ==============================================================================
# Question 1: Infinite Iterators (count, cycle, repeat)
# ==============================================================================
def exercise_q1_infinite_iterators() -> None:
    """
    Demonstrate itertools infinite generator primitives:
    - count(start, step): unbounded numeric progression
    - cycle(iterable): perpetual loop over sequence
    - repeat(val, times): constant value generator
    """
    print("=== Q1: Infinite Iterators (count, cycle, repeat) ===")

    # 1. itertools.count: generate sequence [10, 15, 20, 25]
    counter = itertools.count(start=10, step=5)
    nums = [next(counter) for _ in range(4)]
    assert nums == [10, 15, 20, 25]

    # 2. itertools.cycle: perpetual round-robin
    cycler = itertools.cycle(["RED", "GREEN", "BLUE"])
    pattern = [next(cycler) for _ in range(7)]
    assert pattern == ["RED", "GREEN", "BLUE", "RED", "GREEN", "BLUE", "RED"]

    # 3. itertools.repeat: generate N instances
    repeater = itertools.repeat("PONG", 3)
    pongs = list(repeater)
    assert pongs == ["PONG", "PONG", "PONG"]

    print(f"  itertools.count(10, 5) first 4: {nums}")
    print(f"  itertools.cycle() 7 steps:      {pattern}")
    print(f"  itertools.repeat('PONG', 3):    {pongs}")


# ==============================================================================
# Question 2: Stream Slicing with islice()
# ==============================================================================
def exercise_q2_islice_slicing() -> None:
    """
    Demonstrate islice() to slice lazy iterators and generators where standard
    list slice syntax (`gen[start:stop]`) is illegal.
    """
    print("\n=== Q2: Stream Slicing with islice() ===")

    # Generator of infinite squares
    def infinite_squares() -> Generator[int, None, None]:
        n = 0
        while True:
            yield n * n
            n += 1

    # Take items from index 5 up to (but not including) index 10
    sliced_squares = list(itertools.islice(infinite_squares(), 5, 10))
    # 5^2=25, 6^2=36, 7^2=49, 8^2=64, 9^2=81
    assert sliced_squares == [25, 36, 49, 64, 81]

    # islice with step=2
    evens = list(itertools.islice(itertools.count(0), 0, 10, 2))
    assert evens == [0, 2, 4, 6, 8]

    print(f"  islice(squares, 5, 10): {sliced_squares}")
    print(f"  islice(count(0), 0, 10, 2): {evens}")


# ==============================================================================
# Question 3: Chaining & Flattening (chain and chain.from_iterable)
# ==============================================================================
def exercise_q3_chaining_and_flattening() -> None:
    """
    Demonstrate zero-copy sequence chaining:
    - itertools.chain(*iterables): concatenates argument streams
    - itertools.chain.from_iterable(container): flattens a stream of sub-iterables
    """
    print("\n=== Q3: Chaining & Flattening ===")

    list1 = [1, 2, 3]
    tuple2 = (4, 5)
    set3 = [6, 7]

    # 1. itertools.chain(*args)
    combined = list(itertools.chain(list1, tuple2, set3))
    assert combined == [1, 2, 3, 4, 5, 6, 7]

    # 2. itertools.chain.from_iterable (lazy flattening)
    matrix = [[10, 20], [30, 40], [50, 60]]
    flattened = list(itertools.chain.from_iterable(matrix))
    assert flattened == [10, 20, 30, 40, 50, 60]

    print(f"  chain(*iterables):            {combined}")
    print(f"  chain.from_iterable(matrix):  {flattened}")


# ==============================================================================
# Question 4: Selective Filtering (takewhile, dropwhile, filterfalse)
# ==============================================================================
def exercise_q4_selective_filtering() -> None:
    """
    Explore streaming predicate filters:
    - takewhile: emits elements as long as predicate is True, then terminates immediately
    - dropwhile: drops elements while predicate is True, then emits all remaining elements
    - filterfalse: emits only elements where predicate is False
    """
    print("\n=== Q4: Selective Filtering ===")

    dataset = [2, 4, 6, 7, 8, 10, 12]

    # 1. takewhile: stops as soon as odd number (7) is encountered
    taken = list(itertools.takewhile(lambda x: x % 2 == 0, dataset))
    assert taken == [2, 4, 6]

    # 2. dropwhile: drops until odd number (7), then yields everything after
    dropped = list(itertools.dropwhile(lambda x: x % 2 == 0, dataset))
    assert dropped == [7, 8, 10, 12]

    # 3. filterfalse: keeps only items that fail the predicate (odd numbers)
    odds = list(itertools.filterfalse(lambda x: x % 2 == 0, dataset))
    assert odds == [7]

    print(f"  takewhile(is_even): {taken}")
    print(f"  dropwhile(is_even): {dropped}")
    print(f"  filterfalse(is_even): {odds}")


# ==============================================================================
# Question 5: Grouping Streams with groupby()
# ==============================================================================
def exercise_q5_groupby_aggregation() -> None:
    """
    Demonstrate itertools.groupby().
    CRITICAL RULE: groupby() ONLY aggregates consecutive items!
    Input data MUST be sorted by the grouping key first.
    """
    print("\n=== Q5: Grouping Streams with groupby() ===")

    records = [
        {"role": "dev", "name": "Alice"},
        {"role": "qa", "name": "Bob"},
        {"role": "dev", "name": "Charlie"},
        {"role": "qa", "name": "Dave"},
        {"role": "dev", "name": "Eve"},
    ]

    # Sort by grouping key first!
    sorted_records = sorted(records, key=lambda r: r["role"])

    grouped_output: dict[str, list[str]] = {}
    for role, group_iter in itertools.groupby(sorted_records, key=lambda r: r["role"]):
        # Consume group iterator into a list
        grouped_output[role] = [item["name"] for item in group_iter]

    assert grouped_output["dev"] == ["Alice", "Charlie", "Eve"]
    assert grouped_output["qa"] == ["Bob", "Dave"]

    print(f"  groupby() aggregated records: {grouped_output}")


# ==============================================================================
# Question 6: Cartesian Products & Permutations
# ==============================================================================
def exercise_q6_products_and_permutations() -> None:
    """
    Explore combinatorics:
    - product(*iterables, repeat=N): Cartesian product (nested loops equivalent)
    - permutations(iterable, r): Ordered arrangements without replacement
    """
    print("\n=== Q6: Cartesian Products & Permutations ===")

    colors = ["red", "blue"]
    sizes = ["S", "M", "L"]

    # 1. Cartesian product (2 * 3 = 6 combinations)
    prod = list(itertools.product(colors, sizes))
    assert len(prod) == 6
    assert ("red", "S") in prod
    assert ("blue", "L") in prod

    # Product with repeat (e.g. coin tosses: 2^3 = 8 outcomes)
    coin_tosses = list(itertools.product(["H", "T"], repeat=3))
    assert len(coin_tosses) == 8

    # 2. Permutations: Order matters! (nPr)
    # 3 letters, choose 2 -> 3 * 2 = 6 permutations
    perms = list(itertools.permutations(["A", "B", "C"], 2))
    assert len(perms) == 6
    assert ("A", "B") in perms
    assert ("B", "A") in perms  # Distinct from ('A', 'B')

    print(f"  Cartesian product count: {len(prod)} -> {prod[:3]}...")
    print(f"  Coin toss outcomes:      {len(coin_tosses)} outcomes")
    print(f"  Permutations count:      {len(perms)} -> {perms}")


# ==============================================================================
# Question 7: Combinations & Multi-Choice
# ==============================================================================
def exercise_q7_combinations() -> None:
    """
    Explore unordered selection:
    - combinations(iterable, r): Unordered subsets without replacement (nCr)
    - combinations_with_replacement(iterable, r): Subsets allowing duplicate items
    """
    print("\n=== Q7: Combinations & Multi-Choice ===")

    items = ["A", "B", "C", "D"]

    # 1. combinations (4 choose 2 = 6 combinations)
    combs = list(itertools.combinations(items, 2))
    assert len(combs) == 6
    assert ("A", "B") in combs
    # Order does NOT matter: ('B', 'A') is NOT present because ('A', 'B') exists
    assert ("B", "A") not in combs

    # 2. combinations_with_replacement (allows selecting same item multiple times)
    # (4 + 2 - 1) choose 2 = 5 choose 2 = 10
    combs_rep = list(itertools.combinations_with_replacement(items, 2))
    assert len(combs_rep) == 10
    assert ("A", "A") in combs_rep
    assert ("B", "B") in combs_rep

    print(f"  combinations(4, 2):                  {len(combs)} pairs -> {combs}")
    print(f"  combinations_with_replacement(4, 2): {len(combs_rep)} pairs -> {combs_rep}")


# ==============================================================================
# Question 8: Running Reductions with accumulate()
# ==============================================================================
def exercise_q8_accumulate_reductions() -> None:
    """
    Demonstrate itertools.accumulate() for computing prefix sums, running maximums,
    and cumulative products across a sequence.
    """
    print("\n=== Q8: Running Reductions with accumulate() ===")

    numbers = [1, 2, 3, 4, 5]

    # 1. Running sum (default)
    running_sums = list(itertools.accumulate(numbers))
    assert running_sums == [1, 3, 6, 10, 15]

    # 2. Running product (custom binary operator)
    running_products = list(itertools.accumulate(numbers, func=operator.mul))
    assert running_products == [1, 2, 6, 24, 120]

    # 3. Running maximum
    fluctuations = [3, 1, 4, 1, 5, 9, 2, 6, 5]
    running_max = list(itertools.accumulate(fluctuations, func=max))
    assert running_max == [3, 3, 4, 4, 5, 9, 9, 9, 9]

    print(f"  Running sums:     {running_sums}")
    print(f"  Running products: {running_products}")
    print(f"  Running max:      {running_max}")


# ==============================================================================
# Question 9: Iterator Duplication & Pairwise
# ==============================================================================
def exercise_q9_tee_and_pairwise() -> None:
    """
    Demonstrate:
    - itertools.tee(iterable, n): splits an iterator into n independent iterators.
    - itertools.pairwise(iterable): yields successive overlapping pairs (Python 3.10+).
    """
    print("\n=== Q9: Iterator Duplication & Pairwise ===")

    # 1. itertools.tee
    gen = (x * 2 for x in [1, 2, 3])
    t1, t2 = itertools.tee(gen, 2)

    # Both independent copies can be consumed separately
    assert list(t1) == [2, 4, 6]
    assert list(t2) == [2, 4, 6]

    # 2. itertools.pairwise (successive sliding pairs)
    price_timeline = [100, 105, 102, 110, 115]
    pairs = list(itertools.pairwise(price_timeline))
    assert pairs == [(100, 105), (105, 102), (102, 110), (110, 115)]

    # Compute step deltas
    deltas = [b - a for a, b in pairs]
    assert deltas == [5, -3, 8, 5]

    print(f"  itertools.tee replicated streams: {list(itertools.tee([1, 2], 2)[0])}")
    print(f"  itertools.pairwise timeline:      {pairs}")
    print(f"  Calculated price deltas:          {deltas}")


# ==============================================================================
# Question 10: Advanced Project - Sliding Window Stream Batcher & Aggregator
# ==============================================================================
def batch_stream(iterable: Iterator[Any], batch_size: int) -> Generator[list[Any], None, None]:
    """
    Batches an arbitrary continuous stream into fixed-size chunks using islice().
    """
    it = iter(iterable)
    while True:
        batch = list(itertools.islice(it, batch_size))
        if not batch:
            break
        yield batch


def exercise_q10_stream_batcher() -> None:
    """
    Demonstrate stream batching and windowed metrics aggregation.
    """
    print("\n=== Q10: Stream Batcher & Sliding Aggregator ===")

    # Simulated continuous sensor data stream
    raw_data_stream = (i for i in range(1, 21))  # 1 to 20

    # Batch into groups of 6
    batches = list(batch_stream(raw_data_stream, batch_size=6))

    # 20 items / 6 = 3 batches of 6 + 1 remainder of 2 = 4 batches
    assert len(batches) == 4
    assert batches[0] == [1, 2, 3, 4, 5, 6]
    assert batches[-1] == [19, 20]

    # Compute batch aggregations
    batch_sums = [sum(b) for b in batches]
    assert batch_sums == [21, 57, 93, 39]

    print(f"  Stream partitioned into {len(batches)} batches:")
    for idx, b in enumerate(batches, start=1):
        print(f"    Batch #{idx}: {b} (Sum={sum(b)})")


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_infinite_iterators()
    exercise_q2_islice_slicing()
    exercise_q3_chaining_and_flattening()
    exercise_q4_selective_filtering()
    exercise_q5_groupby_aggregation()
    exercise_q6_products_and_permutations()
    exercise_q7_combinations()
    exercise_q8_accumulate_reductions()
    exercise_q9_tee_and_pairwise()
    exercise_q10_stream_batcher()

    print("\nAll 10 itertools module questions executed and asserted successfully!")
