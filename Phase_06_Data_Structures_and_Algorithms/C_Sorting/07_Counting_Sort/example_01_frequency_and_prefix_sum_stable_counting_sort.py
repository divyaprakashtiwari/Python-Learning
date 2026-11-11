"""
Phase 6 - Data Structures and Algorithms
Section C: Sorting - Topic 07: Counting Sort
Example 01: Basic Frequency Counting Sort vs Prefix-Sum Stable Counting Sort

Demonstrates:
1. Why Counting Sort breaks the O(N log N) comparison-based sorting lower bound:
   It NEVER compares two input elements (`a[i] < a[j]`); instead, it uses integer keys
   directly as array indices into a frequency bucket table in O(N + K) linear time!
2. Basic Frequency Counting Sort (for primitive integers) vs Prefix-Sum Stable Counting Sort
   (which traverses the input BACKWARD from `N - 1` down to `0` so duplicate records preserve
   their exact FIFO relative order!).
"""

from dataclasses import dataclass


@dataclass
class ExamSubmission:
    student: str
    score: int  # 0 .. 100
    submission_id: int


def basic_counting_sort_integers(arr: list[int], max_val: int) -> list[int]:
    """
    Simple Counting Sort for non-negative integers in `[0 .. max_val]`.
    Time Complexity : O(N + K) where K = max_val + 1
    Space Complexity: O(K) frequency array + O(N) output
    """
    counts = [0] * (max_val + 1)
    for num in arr:
        counts[num] += 1

    result: list[int] = []
    for val, freq in enumerate(counts):
        if freq > 0:
            result.extend([val] * freq)
    return result


def stable_counting_sort_records(
    records: list[ExamSubmission], max_score: int
) -> list[ExamSubmission]:
    """
    Stable Prefix-Sum Counting Sort on structured objects in O(N + K) time:
    1. Count frequencies of each key in `[0 .. max_score]`.
    2. Convert `counts` into a cumulative prefix-sum array where `counts[k]` holds the
       number of elements `<= k` (i.e., 1 past the last output index for key `k`).
    3. Iterate through `records` BACKWARD (`n - 1` down to `0`), decrementing `counts[key]`
       and placing each record into its exact final slot!
    """
    n = len(records)
    if n <= 1:
        return records.copy()

    counts = [0] * (max_score + 1)
    for rec in records:
        counts[rec.score] += 1

    # Step 2: Cumulative prefix sums
    for k in range(1, max_score + 1):
        counts[k] += counts[k - 1]

    # Step 3: Backward traversal guarantees FIFO stability!
    output: list[ExamSubmission] = [None] * n  # type: ignore[list-item]
    for i in range(n - 1, -1, -1):
        rec = records[i]
        counts[rec.score] -= 1
        target_idx = counts[rec.score]
        output[target_idx] = rec

    return output


if __name__ == "__main__":
    print("=" * 72)
    print("1. BASIC FREQUENCY COUNTING SORT O(N + K)")
    print("=" * 72)
    dice_rolls = [4, 2, 6, 1, 4, 3, 2, 6, 5, 1, 2, 4]
    print(f"Dice Rolls (N={len(dice_rolls)}, K=6) : {dice_rolls}")
    print(f"Sorted Rolls               : {basic_counting_sort_integers(dice_rolls, max_val=6)}")

    print("\n" + "=" * 72)
    print("2. STABLE PREFIX-SUM COUNTING SORT ON OBJECT RECORDS")
    print("=" * 72)
    submissions = [
        ExamSubmission("Aarav", 85, submission_id=1),
        ExamSubmission("Priya", 92, submission_id=2),
        ExamSubmission("Rohan", 85, submission_id=3),
        ExamSubmission("Meera", 78, submission_id=4),
        ExamSubmission("Kabir", 92, submission_id=5),
        ExamSubmission("Ananya", 85, submission_id=6),
    ]
    sorted_subs = stable_counting_sort_records(submissions, max_score=100)
    for s in sorted_subs:
        print(f"  Score: {s.score} | Student: {s.student:<6} | Submission #{s.submission_id}")
