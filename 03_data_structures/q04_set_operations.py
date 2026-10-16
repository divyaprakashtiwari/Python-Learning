"""
Topic 03: Data Structures
Question 04: Set Operations (Deep Dive)

Master Python sets: mathematical set operations (union, intersection, difference,
symmetric difference), operator vs method behavioral differences, discard vs remove,
subsets/supersets, frozenset immutability, Jaccard similarity, RBAC permission
engines, and O(1) vocabulary spell checkers.
"""

from typing import Any

# ============================================================
# Q1: Set Construction, Empty Set Trap, and Hashability
# ============================================================
# Question: Demonstrate creating sets, the empty set trap (`{}` creates a dict!),
# automatic deduplication, and the hashability requirement for set members.

print("=== Q1: Set Construction & Empty Set Trap ===")

# THE EMPTY SET TRAP:
empty_braces = {}
empty_set = set()
print(f"  {{}} type:      {type(empty_braces).__name__} (Creates a dictionary, NOT a set!)")
print(f"  set() type:   {type(empty_set).__name__} (True empty set)")

# Automatic deduplication
numbers = {1, 2, 2, 3, 3, 3, 4, 4, 4, 4}
print(f"  Deduplicated: {numbers} (Length: {len(numbers)})")

# Set elements must be hashable
valid_set = {"text", 42, 3.14, (1, 2)}
print(f"  Valid set with hashable types: {valid_set}")

try:
    invalid_set = {1, 2, [3, 4]}  # type: ignore
except TypeError as e:
    print(f"  Caught expected unhashable error: {e}")

# Explanation: In Python, `{}` is reserved for empty dictionaries. To create an empty set,
# always call `set()`. All elements inside a set must be immutable and hashable.


# ============================================================
# Q2: Mathematical Operations: Operators vs Methods
# ============================================================
# Question: Demonstrate Union (|), Intersection (&), Difference (-),
# and Symmetric Difference (^). Highlight the critical distinction: operators require
# sets, while methods accept ANY iterable (list, tuple, generator).

print("\n=== Q2: Set Operations (Operators vs Methods) ===")

set_a = {1, 2, 3, 4, 5}
set_b = {4, 5, 6, 7, 8}
raw_list = [5, 6, 99]

# 1. Union (All elements in either set)
print(f"  Union (A | B):              {set_a | set_b}")
print(f"  Union method (A.union(list)):{set_a.union(raw_list)} (Method accepts any iterable!)")

# 2. Intersection (Elements common to both)
print(f"  Intersection (A & B):       {set_a & set_b}")
print(f"  Intersection method:        {set_a.intersection(raw_list)}")

# 3. Difference (Elements in A but NOT in B)
print(f"  Difference (A - B):         {set_a - set_b}")
print(f"  Difference (B - A):         {set_b - set_a}")

# 4. Symmetric Difference (Elements in A or B, but NOT in both)
print(f"  Symmetric Diff (A ^ B):     {set_a ^ set_b}")

# Critical difference: Operators require set operands
try:
    _ = set_a | raw_list  # type: ignore
except TypeError as e:
    print(f"  Operator with list failed: {e} (Operators require set types!)")

# Explanation: Methods (`union`, `intersection`, etc.) are more flexible because they
# automatically convert foreign iterables (lists, tuples, dicts) into sets on the fly.


# ============================================================
# Q3: In-Place Mutation Methods
# ============================================================
# Question: Demonstrate modifying sets in-place using `.add()`, `.update()`,
# `.intersection_update()`, and `.difference_update()`.

print("\n=== Q3: In-Place Set Mutation Methods ===")

tags = {"python", "programming"}
orig_id = id(tags)

# add() single element
tags.add("backend")
print(f"  After .add('backend'):               {tags}")

# update() adds multiple elements from any iterable (|=)
tags.update(["api", "rest", "python"])
print(f"  After .update(['api', 'rest']):      {tags}")

# intersection_update() keeps only common elements (&=)
tags.intersection_update({"python", "backend", "docker", "cloud"})
print(f"  After .intersection_update(...):     {tags}")

# difference_update() removes elements present in another set (-=)
tags.difference_update({"backend"})
print(f"  After .difference_update({'backend'}): {tags}")
print(f"  Set identity preserved in-place:     {id(tags) == orig_id}")

# Explanation: In-place set methods update the underlying hash table directly
# without allocating a new set object.


# ============================================================
# Q4: Element Deletion: remove() vs discard() vs pop()
# ============================================================
# Question: Compare deleting items using `.remove()`, `.discard()`, `.pop()`, and `.clear()`.
# Demonstrate why `.discard()` is safer when the item might not exist.

print("\n=== Q4: Set Deletion Strategies ===")

active_sessions = {"sess_101", "sess_102", "sess_103"}

# 1. discard(): removes item if present; DOES NOT raise error if missing
active_sessions.discard("sess_102")
print(f"  After discard('sess_102'): {active_sessions}")
active_sessions.discard("non_existent")  # Safe! No exception raised
print(f"  After discard('non_existent'): {active_sessions} (Silently ignored)")

# 2. remove(): removes item, but RAISES KeyError if missing
active_sessions.remove("sess_101")
print(f"  After remove('sess_101'): {active_sessions}")
try:
    active_sessions.remove("non_existent")
except KeyError as e:
    print(f"  remove('non_existent') raised KeyError: {e}")

# 3. pop(): removes and returns an ARBITRARY element
remaining = {"A", "B", "C"}
popped_val = remaining.pop()
print(f"  pop() removed arbitrary element: '{popped_val}', remaining: {remaining}")

# 4. clear(): empties the set
remaining.clear()
print(f"  clear() result: {remaining}")

# Explanation: Use `.discard()` when missing elements are expected or harmless.
# Use `.remove()` when missing an element indicates an invalid state or invariant violation.


# ============================================================
# Q5: Relational Set Predicates (Subsets and Disjoint Sets)
# ============================================================
# Question: Evaluate subset (`<=`), proper subset (`<`), superset (`>=`),
# and disjointness (`.isdisjoint()`) relationships between sets.

print("\n=== Q5: Set Relational Predicates ===")

core_skills = {"python", "sql", "git"}
full_stack_dev = {"python", "sql", "git", "docker", "react", "fastapi"}
data_analyst = {"sql", "excel", "tableau", "python"}
mobile_dev = {"swift", "kotlin", "flutter"}

# Subset: A <= B (Every element of A is in B)
print(f"  core_skills <= full_stack_dev: {core_skills <= full_stack_dev} (Core is subset)")
print(f"  core_skills < full_stack_dev:  {core_skills < full_stack_dev} (Strict/proper subset)")

# Self subset is True, but strict subset is False
print(f"  core_skills <= core_skills:    {core_skills <= core_skills}")
print(f"  core_skills < core_skills:     {core_skills < core_skills} (Cannot be strict subset of itself)")

# Disjoint: A.isdisjoint(B) -> True if intersection is completely empty
print(f"  core_skills.isdisjoint(mobile_dev): {core_skills.isdisjoint(mobile_dev)} (Zero common skills)")
print(f"  core_skills.isdisjoint(data_analyst): {core_skills.isdisjoint(data_analyst)} (Shares python/sql)")

# Explanation: Set relational predicates evaluate containment and orthogonality
# with average $O(\min(|A|, |B|))$ efficiency via hash lookups.


# ============================================================
# Q6: Frozenset: Immutable Sets and Sets of Sets
# ============================================================
# Question: Demonstrate `frozenset`: its immutability, using it as a dictionary key,
# and creating nested sets (sets of sets).

print("\n=== Q6: Frozenset (Immutable Sets) ===")

frozen_a = frozenset([1, 2, 3, 4])
frozen_b = frozenset([3, 4, 5, 6])

print(f"  frozenset: {frozen_a} (Hash: {hash(frozen_a)})")
print(f"  Union of frozensets: {frozen_a | frozen_b}")

# Immutability
try:
    frozen_a.add(10)  # type: ignore
except AttributeError as e:
    print(f"  Caught immutability error: {e}")

# Frozenset as a dictionary key (e.g., caching graph edge pairs or combinations)
route_costs = {
    frozenset({"New York", "London"}): 650.0,
    frozenset({"Paris", "Tokyo"}): 890.0
}

# Lookup works regardless of city argument order!
query_edge = frozenset({"London", "New York"})
print(f"  Bidirectional flight cost lookup: ${route_costs[query_edge]:.2f}")

# Set of sets: regular set CANNOT contain a set, but CAN contain frozensets!
set_of_clusters = {frozenset([1, 2]), frozenset([3, 4]), frozenset([5, 6])}
print(f"  Set of frozensets (nested sets): {set_of_clusters}")

# Explanation: `frozenset` is an immutable, hashable set. It serves as an unalterable
# grouping that can be safely embedded in sets or used as dictionary keys.


# ============================================================
# Q7: Jaccard Similarity Index Engine
# ============================================================
# Question: Implement the Jaccard similarity coefficient between two text documents
# or user preference sets: J(A, B) = |A ∩ B| / |A ∪ B|.

print("\n=== Q7: Jaccard Similarity Engine ===")

def compute_jaccard_similarity(text1: str, text2: str) -> dict:
    """Computes word-level Jaccard similarity between two texts."""
    # Tokenize words into lowercased sets
    words_a = set(text1.lower().split())
    words_b = set(text2.lower().split())
    
    intersection = words_a & words_b
    union = words_a | words_b
    
    similarity = len(intersection) / len(union) if union else 1.0
    
    return {
        "similarity_score": round(similarity, 4),
        "common_words": sorted(list(intersection)),
        "unique_to_first": sorted(list(words_a - words_b)),
        "unique_to_second": sorted(list(words_b - words_a)),
    }

doc1 = "Python is a powerful elegant and clean programming language"
doc2 = "Python is a clean and flexible language for data science"

jaccard_report = compute_jaccard_similarity(doc1, doc2)
print(f"  Doc 1: \"{doc1}\"")
print(f"  Doc 2: \"{doc2}\"")
print(f"  Similarity Score: {jaccard_report['similarity_score'] * 100:.1f}%")
print(f"  Shared Vocabulary: {jaccard_report['common_words']}")

# Explanation: The Jaccard similarity index measures overlap over total diversity.
# It is widely used in recommendation engines, plagiarism detection, and search indexing.


# ============================================================
# Q8: Role-Based Access Control (RBAC) Permission Verifier
# ============================================================
# Question: Implement an authorization engine using set operations:
# Check if a user's accumulated permissions satisfy the required permissions for an action.

print("\n=== Q8: RBAC Permission Engine ===")

# Define permissions mapped to roles
ROLE_PERMISSIONS = {
    "VIEWER": {"doc:read", "comment:read"},
    "EDITOR": {"doc:read", "comment:read", "doc:write", "comment:write"},
    "ADMIN":  {"doc:read", "comment:read", "doc:write", "comment:write", "doc:delete", "user:manage"},
}

def authorize_action(user_roles: list[str], required_permissions: set[str]) -> tuple[bool, set[str]]:
    """Verifies user has all required permissions using set union and superset."""
    # Accumulate all permissions across all roles assigned to user
    effective_permissions = set()
    for role in user_roles:
        effective_permissions.update(ROLE_PERMISSIONS.get(role, set()))
        
    # Check if effective_permissions is a superset of required_permissions
    is_authorized = required_permissions <= effective_permissions
    missing_permissions = required_permissions - effective_permissions
    
    return is_authorized, missing_permissions

# Test action requiring edit and delete permissions
critical_action_perms = {"doc:write", "doc:delete"}

user_a_roles = ["EDITOR"]
user_b_roles = ["VIEWER", "ADMIN"]

ok_a, missing_a = authorize_action(user_a_roles, critical_action_perms)
print(f"  User A (Editor) -> Authorized: {ok_a} | Missing: {missing_a}")

ok_b, missing_b = authorize_action(user_b_roles, critical_action_perms)
print(f"  User B (Admin)  -> Authorized: {ok_b} | Missing: {missing_b}")

# Explanation: Sets model authorization elegantly: user capabilities are combined via
# set union (`update`), and privilege gates are verified via subset comparison (`<=`).


# ============================================================
# Q9: Finding Missing and Duplicate Records in O(N)
# ============================================================
# Question: Given a list of transaction IDs that should contain all integers from 1 to N,
# use set operations to identify missing IDs and duplicate IDs in O(N) time.

print("\n=== Q9: Missing and Duplicate Number Detector ===")

def find_missing_and_duplicates(stream: list[int], expected_n: int) -> dict:
    """Detects missing and duplicate IDs using set arithmetic."""
    expected_set = set(range(1, expected_n + 1))
    seen = set()
    duplicates = set()
    
    for item in stream:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
            
    missing = expected_set - seen
    
    return {
        "expected_count": expected_n,
        "processed_count": len(stream),
        "duplicates": sorted(list(duplicates)),
        "missing": sorted(list(missing)),
    }

incoming_ids = [1, 2, 3, 3, 5, 6, 6, 8, 9, 10]  # Missing 4 and 7; duplicates 3 and 6
analysis = find_missing_and_duplicates(incoming_ids, expected_n=10)

print(f"  Input IDs:   {incoming_ids}")
print(f"  Duplicates:  {analysis['duplicates']}")
print(f"  Missing IDs: {analysis['missing']}")

# Explanation: `expected_set - seen` determines missing elements in $O(N)$ time
# using set difference without sorting.


# ============================================================
# Q10: O(1) Vocabulary Spell Checker & Edit Distance Candidate Generator
# ============================================================
# Question: Build a fast spell-checking engine with an O(1) vocabulary set.
# If a word is misspelled, generate candidate words by single-character deletion
# and check which candidates exist in the dictionary.

print("\n=== Q10: O(1) Vocabulary Spell Checker ===")

# Standard dictionary vocabulary stored in a set for O(1) average lookup time
VOCABULARY = {
    "python", "coding", "language", "clean", "program", "developer",
    "computer", "system", "network", "database", "algorithm", "design"
}

def spell_check(word: str) -> dict:
    """Checks spelling and suggests single-deletion candidates."""
    target = word.lower()
    
    if target in VOCABULARY:
        return {"word": word, "status": "CORRECT", "suggestions": []}
        
    # Generate 1-edit distance candidates (single deletions)
    candidates = set()
    for i in range(len(target)):
        # Delete character at index i
        candidate = target[:i] + target[i + 1 :]
        if candidate in VOCABULARY:
            candidates.add(candidate)
            
    return {
        "word": word,
        "status": "MISSPELLED",
        "suggestions": sorted(list(candidates)) if candidates else ["<No simple suggestion>"]
    }

test_words = ["python", "pythons", "cleann", "algoriithm", "xyz123"]
for w in test_words:
    res = spell_check(w)
    sug_str = f"-> Did you mean: {res['suggestions']}" if res['status'] == "MISSPELLED" else ""
    print(f"  Word: {w:<12} [{res['status']:<10}] {sug_str}")

# Summary Output
print("\n" + "=" * 55)
print("  All 10 Questions for Topic 03 - Q04 executed successfully!")
print("=" * 55)
