# Practice Problems by Difficulty (`PRACTICE_PROBLEMS.md`)

A structured bank of practice problems arranged by difficulty (**Easy**, **Medium**, **Hard**) across Python Fundamentals, OOP, Advanced Python, and Data Structures & Algorithms.

---

## Level 1: Easy (Fundamentals, Basic Data Structures & Logic)

1. **Swap Two Variables Without Temp:** Given two integers `a` and `b`, swap their values using tuple unpacking and arithmetic operations.
2. **Leap Year Validator:** Determine if a given year `Y` is a leap year (`divisible by 400` OR `divisible by 4 and not 100`).
3. **FizzBuzz Generator:** Print numbers `1` to `N`, replacing multiples of `3` with `"Fizz"`, `5` with `"Buzz"`, and `15` with `"FizzBuzz"`.
4. **Palindrome Number & String:** Check if an integer or string reads the same backward without converting integers to strings.
5. **Prime Number Checker (`O(sqrt(n))`):** Verify whether `N` is prime by testing divisors up to `int(N ** 0.5)`.
6. **Character Frequency Counter:** Count occurrences of each character in a string using a dictionary (without `collections.Counter`).
7. **Remove Duplicates Preserving Order:** Given a list of integers, return a new list with duplicates removed while keeping first-seen order.
8. **Second Largest Element:** Find the second largest distinct element in an array in a single pass (`O(n)` time, `O(1)` space).
9. **Matrix Transpose:** Transpose an `M x N` 2D list using nested loops and using a list comprehension.
10. **Anagram Check:** Determine if two strings `s` and `t` are anagrams of each other in `O(n)` time.

---

## Level 2: Medium (Functions, OOP, Advanced Python & Core DSA)

1. **Custom Retry Decorator:** Write a decorator `@retry(max_attempts=3)` that re-executes a failing function before raising its exception.
2. **Memory-Efficient Log Reader:** Build a generator function that streams a large log file line by line and yields only `"ERROR"` entries.
3. **Bank Account Hierarchy (OOP):** Implement `Account`, `SavingsAccount`, and `CurrentAccount` with encapsulation, `@property`, and overdraft rules.
4. **Two Sum (Unsorted Array):** Return indices of two numbers in an array that add up to `target` in `O(n)` time using a hash map.
5. **Maximum Subarray Sum (Kadane's Algorithm):** Find the contiguous subarray within a 1D array of numbers (including negatives) that has the largest sum.
6. **Longest Substring Without Repeating Characters:** Use a sliding window to find the length of the longest substring with unique characters.
7. **Valid Parentheses:** Use a stack to check if a string of `'()[]{}'` brackets is properly balanced and nested.
8. **Detect Cycle in Linked List:** Implement Floyd's Tortoise and Hare algorithm (`O(n)` time, `O(1)` space).
9. **Binary Tree Level Order Traversal:** Traverse a binary tree level by level using `collections.deque`.
10. **Top K Frequent Elements:** Given an integer array, return the `k` most frequent elements using `Counter` and `heapq`.

---

## Level 3: Hard (Placement-Level DSA & System Design in Python)

1. **LRU Cache Implementation:** Design an LRU Cache supporting `get(key)` and `put(key, value)` in `O(1)` time using a Doubly Linked List + Hash Map.
2. **Merge K Sorted Linked Lists:** Merge `k` sorted linked lists into one sorted list in `O(N log k)` time using a Min-Heap.
3. **Sliding Window Maximum:** Given an array `nums` and window size `k`, return the max value in each window in `O(n)` time using a Monotonic Deque.
4. **Course Schedule II (Topological Sort):** Given `numCourses` and `prerequisites`, return a valid course ordering or `[]` if a cycle exists.
5. **Dijkstra's Shortest Path in Network:** Find minimum signal propagation time from a source node to all nodes in a weighted directed graph.
6. **N-Queens Solver:** Place `N` queens on an `N x N` chessboard so that no two queens attack each other using Backtracking.
7. **0/1 Knapsack & Coin Change (Dynamic Programming):** Solve both top-down memoized and bottom-up space-optimized `O(W)` / `O(amount)` DP formulations.
8. **Longest Common Subsequence (LCS) with Reconstruction:** Compute the length of the LCS of two strings and reconstruct the actual subsequence string.
9. **Word Ladder (Shortest Transformation Sequence):** Find the shortest word transformation path from `beginWord` to `endWord` using BFS.
10. **Serialize and Deserialize Binary Tree:** Convert any binary tree into a compact string representation and reconstruct the exact tree structure.
