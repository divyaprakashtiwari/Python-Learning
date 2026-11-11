"""
Phase 6 - Data Structures and Algorithms
Section D: Arrays and Strings - Topic 01: Array Operations
Example 03: Boyer-Moore Majority Vote Algorithm & Product of Array Except Self

Demonstrates:
1. Boyer-Moore Majority Vote Algorithm: finds the element that appears strictly more than
   `N // 2` times in O(N) time and O(1) space (without a hash map!).
2. Product of Array Except Self (LeetCode 238): computes `output[i] = product of all arr[j] (j != i)`
   in O(N) time and O(1) auxiliary space WITHOUT using division (which would fail on zeros!).
"""


def boyer_moore_majority_element(arr: list[int]) -> int | None:
    """
    Find the majority element (occurring > len(arr) // 2 times) in O(N) time and O(1) space.
    Phase 1: Pairwise cancellation to find the surviving `candidate`.
    Phase 2: Verify that `candidate` actually occurs > N // 2 times.
    """
    candidate: int | None = None
    count = 0

    # Phase 1: Voting / Cancellation
    for num in arr:
        if count == 0:
            candidate = num
            count = 1
        elif num == candidate:
            count += 1
        else:
            count -= 1

    # Phase 2: Verification (mandatory if a majority element is not guaranteed!)
    if candidate is not None and arr.count(candidate) > len(arr) // 2:
        return candidate
    return None


def product_except_self(nums: list[int]) -> list[int]:
    """
    Return an array `answer` where `answer[i]` is the product of all elements of `nums`
    except `nums[i]`, computed in O(N) time and O(1) extra space without division!
    """
    n = len(nums)
    answer = [1] * n

    # Pass 1 (Left to Right): store prefix product of nums[0 .. i - 1] in answer[i]
    prefix_prod = 1
    for i in range(n):
        answer[i] = prefix_prod
        prefix_prod *= nums[i]

    # Pass 2 (Right to Left): multiply by suffix product of nums[i + 1 .. n - 1]
    suffix_prod = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix_prod
        suffix_prod *= nums[i]

    return answer


if __name__ == "__main__":
    print("=" * 72)
    print("1. BOYER-MOORE MAJORITY VOTE ALGORITHM (O(N) TIME, O(1) SPACE)")
    print("=" * 72)
    votes_1 = [2, 2, 1, 1, 1, 2, 2]
    votes_2 = [1, 2, 3, 1, 2, 3, 1]
    print(f"Votes {votes_1} -> Majority (>3): {boyer_moore_majority_element(votes_1)}")
    print(f"Votes {votes_2} -> Majority (>3): {boyer_moore_majority_element(votes_2)}")

    print("\n" + "=" * 72)
    print("2. PRODUCT OF ARRAY EXCEPT SELF (WITHOUT DIVISION, HANDLES ZEROS!)")
    print("=" * 72)
    for sample in [[1, 2, 3, 4], [-1, 1, 0, -3, 3]]:
        print(f"  Input: {str(sample):<20} -> Product Except Self: {product_except_self(sample)}")
