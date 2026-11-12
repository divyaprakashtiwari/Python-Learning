# Fast and Slow Pointers (Midpoint Discovery, $O(1)$-Space Palindrome & List Zipping)

---

## 1. Introduction

The **Fast and Slow Pointers** technique (also called the **Two-Speed Pointer Pattern** or **Runner Technique**) traverses a linked list with two pointers initialized at `head` that advance at a fixed speed ratio (most commonly $1 : 2$, where `slow` advances 1 node per iteration and `fast` advances 2 nodes per iteration):

$$\text{When } \texttt{fast} \text{ reaches the tail ($n$ steps), } \texttt{slow} \text{ is at the exact midpoint ($n/2$ steps)!}$$

Beyond cycle detection, the Fast & Slow pointer pattern is the foundation for solving linked list problems in **a single pass and $O(1)$ auxiliary memory** without counting the length $n$ in advance:
1. **Finding the First Middle (Left-Biased) vs Second Middle (Right-Biased)** of an even-length list (LeetCode 876) and **Deleting the Middle Node** (LeetCode 2095).
2. **Palindrome Linked List in $O(1)$ Space** (with structure restoration — LeetCode 234) and **Maximum Twin Sum** (LeetCode 2130).
3. **Reorder List (Zipping Ends $L_0 \to L_n \to L_1 \to L_{n-1}$)** (LeetCode 143) and **Top-Down Linked List Merge Sort** (LeetCode 148).

---

## 2. Why is it used?

1. **Eliminates the Two-Pass Length Count:** Because singly linked lists do not store their length or support `list[n // 2]` indexing, finding the middle naively requires one full $O(n)$ pass to count $n$ and a second $O(n/2)$ pass to walk to index $n // 2$. Fast & Slow pointers locate the midpoint in a single structural scan with better cache locality.
2. **Unlocks Backward Traversal on the Second Half in $O(1)$ Space:** Once `slow` identifies the midpoint, reversing `slow.next` in-place lets us walk inward from both ends (`head` moving right, reversed `tail` moving left) in $O(1)$ extra memory!
3. **Clean Recursive Halving for Divide-and-Conquer ($O(n \log n)$ Merge Sort):** Finding the exact first middle allows splitting a linked list into two balanced halves of sizes $\lceil n/2 \rceil$ and $\lfloor n/2 \rfloor$.

---

## 3. Syntax

### A. First Middle (Left-Biased Midpoint — Index `(n - 1) // 2`)
Use this whenever you are **splitting** a list into two halves (`slow.next = None`) for Merge Sort, Reorder List, or Palindrome Linked List:
```python
slow = head
fast = head
while fast.next is not None and fast.next.next is not None:
    slow = slow.next
    fast = fast.next.next
# On [10, 20, 30, 40], `slow` stops at 20 (index 1, end of first half)
```

### B. Second Middle (Right-Biased Midpoint — Index `n // 2`, LeetCode 876)
Use this when a problem explicitly asks for the second middle node of an even-length list:
```python
slow = head
fast = head
while fast is not None and fast.next is not None:
    slow = slow.next
    fast = fast.next.next
# On [10, 20, 30, 40], `slow` stops at 30 (index 2, start of second half)
```

---

## 4. Explanation (Step-by-Step)

### 1. Why Splitting Requires the **First Middle** (`fast.next and fast.next.next`)
Consider a **2-node list** `10 -> 20 -> None` that we want to split into two 1-node halves for Merge Sort:
- If we used the **Second Middle** loop (`while fast and fast.next:`), after 1 iteration `slow` moves to `Node(20)` and `fast` moves to `None`. Splitting at `slow` leaves the first half with `[10, 20]` (size 2!) and the second half with `None` (size 0), causing **infinite recursion** in Merge Sort!
- Using the **First Middle** loop (`while fast.next and fast.next.next:`), the loop condition is immediately `False` on a 2-node list, so `slow` stays at `Node(10)`. Setting `mid = slow.next` (`Node(20)`) and `slow.next = None` cleanly splits `[10, 20]` into `[10]` and `[20]`.

### 2. The 3-Phase Blueprint (`Midpoint -> Reverse 2nd Half -> Two-Pointer Walk`)
Problems like **Palindrome Linked List** (LeetCode 234), **Reorder List** (LeetCode 143), and **Maximum Twin Sum** (LeetCode 2130) all share the exact same 3-step skeleton:
1. **Step 1 (Midpoint):** Find First Middle `slow` using `while fast.next and fast.next.next:`.
2. **Step 2 (Reverse):** Reverse the second half starting at `slow.next` in-place in $O(1)$ space.
3. **Step 3 (Walk / Zip):** Walk `p1` from `head` and `p2` from `second_half_head` simultaneously (and optionally reverse the second half back to restore the input list).

---

## 5. Minimum 3 Examples

### Example 1: First Middle vs Second Middle & Deleting the Middle Node
File: [`example_01_first_and_second_middle_of_linked_list.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/E_Linked_Lists/06_Fast_and_Slow_Pointers/example_01_first_and_second_middle_of_linked_list.py)

```python
def find_first_middle(head: Optional[ListNode]) -> Optional[ListNode]:
    """Returns the left-biased middle node (index (n - 1) // 2)."""
    if head is None:
        return None
    slow: ListNode = head
    fast: ListNode = head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next          # type: ignore[assignment]
        fast = fast.next.next
    return slow


def find_second_middle(head: Optional[ListNode]) -> Optional[ListNode]:
    """Returns the right-biased middle node (index n // 2, LeetCode 876)."""
    if head is None:
        return None
    slow: Optional[ListNode] = head
    fast: Optional[ListNode] = head
    while fast is not None and fast.next is not None:
        assert slow is not None
        slow = slow.next
        fast = fast.next.next
    return slow


def delete_middle_node(head: Optional[ListNode]) -> Optional[ListNode]:
    """Deletes the middle node (index n // 2) in one pass (LeetCode 2095)."""
    if head is None or head.next is None:
        return None

    slow: ListNode = head
    fast: Optional[ListNode] = head.next.next

    while fast is not None and fast.next is not None:
        slow = slow.next          # type: ignore[assignment]
        fast = fast.next.next

    assert slow.next is not None
    slow.next = slow.next.next
    return head
```

---

### Example 2: Palindrome Linked List in $O(1)$ Space (with Structure Restoration) & Max Twin Sum
File: [`example_02_palindrome_linked_list_o1_space.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/E_Linked_Lists/06_Fast_and_Slow_Pointers/example_02_palindrome_linked_list_o1_space.py)

```python
def is_palindrome_linked_list(head: Optional[ListNode]) -> bool:
    """
    Checks whether `head` is a palindrome in O(n) time and O(1) space,
    restoring the original list structure before returning.
    """
    if head is None or head.next is None:
        return True

    # Step 1: Locate the end of the first half (First Middle)
    slow: ListNode = head
    fast: ListNode = head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next          # type: ignore[assignment]
        fast = fast.next.next

    # Step 2: Reverse the second half in-place
    second_half_head = reverse_list(slow.next)

    # Step 3: Compare both halves
    p1: Optional[ListNode] = head
    p2: Optional[ListNode] = second_half_head
    is_pal = True
    while p2 is not None:
        assert p1 is not None
        if p1.val != p2.val:
            is_pal = False
            break
        p1 = p1.next
        p2 = p2.next

    # Step 4: Restore the original list before returning!
    slow.next = reverse_list(second_half_head)
    return is_pal
```

---

### Example 3: Reorder List In-Place (Zipper Merge) & Linked List Merge Sort
File: [`example_03_reorder_list_and_linked_list_merge_sort.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_06_Data_Structures_and_Algorithms/E_Linked_Lists/06_Fast_and_Slow_Pointers/example_03_reorder_list_and_linked_list_merge_sort.py)

```python
def reorder_list_in_place(head: Optional[ListNode]) -> None:
    """
    Reorders `L_0 -> L_1 -> ... -> L_n` into `L_0 -> L_n -> L_1 -> L_{n-1} -> ...`
    in O(n) time and O(1) space.
    """
    if head is None or head.next is None:
        return

    # 1. Find First Middle
    slow: ListNode = head
    fast: ListNode = head
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next          # type: ignore[assignment]
        fast = fast.next.next

    # 2. Split and reverse the second half
    second: Optional[ListNode] = slow.next
    slow.next = None
    prev: Optional[ListNode] = None
    curr = second
    while curr is not None:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    second = prev

    # 3. Zipper-merge `first` and `second`
    first: Optional[ListNode] = head
    while second is not None:
        assert first is not None
        tmp1 = first.next
        tmp2 = second.next

        first.next = second
        second.next = tmp1

        first = tmp1
        second = tmp2
```

---

## 6. Output

### Output — Example 1 (`example_01_first_and_second_middle_of_linked_list.py`)
```text
========================================================================
First Middle (Left-Biased) vs Second Middle (Right-Biased) & Delete Mid
========================================================================

List (5 nodes): [10, 20, 30, 40, 50]
  First Middle  (idx 2): 30
  Second Middle (idx 2): 30
  After delete_middle_node() : [10, 20, 40, 50]

List (6 nodes): [10, 20, 30, 40, 50, 60]
  First Middle  (idx 2): 30
  Second Middle (idx 3): 40
  After delete_middle_node() : [10, 20, 30, 50, 60]

List (2 nodes): [100, 200]
  First Middle  (idx 0): 100
  Second Middle (idx 1): 200
  After delete_middle_node() : [100]

List (1 nodes): [42]
  First Middle  (idx 0): 42
  Second Middle (idx 0): 42
  After delete_middle_node() : []
```

### Output — Example 2 (`example_02_palindrome_linked_list_o1_space.py`)
```text
========================================================================
1. O(1) Space Palindrome Linked List (with Structure Restoration)
========================================================================
Input: [1, 2, 3, 2, 1]    -> Palindrome: True  | Restored: [1, 2, 3, 2, 1]
Input: [10, 20, 20, 10]   -> Palindrome: True  | Restored: [10, 20, 20, 10]
Input: [1, 2, 3, 4]       -> Palindrome: False | Restored: [1, 2, 3, 4]
Input: [7]                -> Palindrome: True  | Restored: [7]

========================================================================
2. Maximum Twin Sum of an Even-Length Linked List (LeetCode 2130)
========================================================================
List: [5, 4, 2, 1, 10, 3] -> Max Twin Sum (4 + 10 = 14): 14
```

### Output — Example 3 (`example_03_reorder_list_and_linked_list_merge_sort.py`)
```text
========================================================================
1. Reorder List In-Place (Zip Ends: L_0 -> L_n -> L_1 -> L_{n-1})
========================================================================
Original: [1, 2, 3, 4]               -> Reordered: [1, 4, 2, 3]
Original: [1, 2, 3, 4, 5]            -> Reordered: [1, 5, 2, 4, 3]
Original: [10, 20, 30, 40, 50, 60]   -> Reordered: [10, 60, 20, 50, 30, 40]

========================================================================
2. Linked List Merge Sort via Fast & Slow Midpoint Split
========================================================================
Unsorted: [40, 20, 10, 30, 70, 50, 60, 15]
Sorted  : [10, 15, 20, 30, 40, 50, 60, 70]
```

---

## 7. Code Explanation

1. **Starting `fast = head.next.next` in `delete_middle_node`:**
   To delete the second middle node at index `n // 2`, we need `slow` to stop at its **predecessor** (index `n // 2 - 1`), which is exactly 1 step earlier. Giving `fast` a 1-iteration head start (`fast = head.next.next` while `slow = head`) makes `slow` stop on the exact predecessor without needing an extra `prev` variable!
2. **Why `while p2 is not None:` Works for Both Odd and Even Lists in `is_palindrome_linked_list`:**
   On an odd-length list like `[1, 2, 3, 2, 1]`, `slow` stops at `3` (the center pivot), so `slow.next` (`[2, 1]`) has length $\lfloor n/2 \rfloor = 2$. Comparing `p1` (`[1, 2, 3]`) against `p2` (`[1, 2]`) while `p2 is not None` checks the first two elements against the reversed last two elements and naturally ignores the shared center element `3`!

---

## 8. Common Mistakes

1. **Forgetting `slow.next = None` When Splitting the List in `reorder_list_in_place` or `sort_linked_list`:**
   If you reverse `slow.next` without severing `slow.next = None`, the tail of the first half still points to the tail of the reversed second half, creating a cycle at the end of the merged list!
2. **Using Second Middle (`while fast and fast.next:`) in Linked List Merge Sort:**
   On a 2-node list, `slow` advances to the second node, so `head` keeps 2 nodes and `mid` gets 0 nodes, causing `RecursionError: maximum recursion depth exceeded`.
3. **Mutating the Input List Permanently in Read-Only Queries (`is_palindrome`):**
   In production codebases, a boolean predicate like `is_palindrome(head)` should never leave the caller's linked list half-reversed. Always reverse the second half back before returning.

---

## 9. Practice Questions

1. **Easy — Find the One-Third and Two-Thirds Nodes in One Pass:**
   Using pointers advancing at speeds $1, 2,$ and $3$, find the node at index $\lfloor n / 3 \rfloor$ and the node at index $\lfloor 2n / 3 \rfloor$ of a singly linked list in a single pass.
2. **Medium — Convert Sorted Singly Linked List to Height-Balanced BST (LeetCode 109):**
   Given the head of a singly linked list where elements are sorted in ascending order, use Fast & Slow pointers to recursively pick the middle node as the BST root and build a height-balanced Binary Search Tree in $O(n \log n)$ time.
3. **Hard — Bottom-Up Iterative Merge Sort on a Linked List in Strict $O(1)$ Space:**
   Top-down recursive Merge Sort uses $O(\log n)$ call-stack space. Implement bottom-up iterative Merge Sort on a linked list that merges sublists of size $1, 2, 4, 8, \dots$ in $O(n \log n)$ time and strict $O(1)$ auxiliary memory.

---

## 10. Interview Questions

### Q1: In `is_palindrome_linked_list`, is the $O(1)$-space in-place reversal approach thread-safe?
**Answer:** **No!** Because it temporarily mutates `.next` pointers on the second half of the linked list before restoring them, any concurrent reader thread traversing the same linked list simultaneously would see corrupted links or a broken list. If concurrent reads are required without locks, an $O(n)$-space read-only approach is necessary.

### Q2: Why is Merge Sort the preferred $O(n \log n)$ sorting algorithm for Linked Lists instead of Quick Sort or Heap Sort?
**Answer:**
1. Heap Sort requires $O(1)$ random index access (`2*i + 1`), which takes $O(n)$ per access in a linked list.
2. Merge Sort on arrays requires an $O(n)$ auxiliary buffer to merge two halves, whereas merging two sorted linked lists splices existing `.next` pointers in **$O(1)$ auxiliary space**! Furthermore, Merge Sort is guaranteed $O(n \log n)$ worst-case and stable.

### Q3: How can you tell whether to use `while fast and fast.next:` vs `while fast.next and fast.next.next:`?
**Answer:** Test your loop mentally on a **2-node list `[A, B]`**:
- If you want `slow` to land on **`B`** (index 1, the right middle), use `while fast and fast.next:`.
- If you want `slow` to stay on **`A`** (index 0, the left middle so you can split `[A]` and `[B]` via `slow.next = None`), use `while fast.next and fast.next.next:`.
