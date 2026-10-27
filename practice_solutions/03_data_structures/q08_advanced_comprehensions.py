"""
Topic 03 - Data Structures: Question 8
Problem: Advanced Comprehensions (Nested List, Set, and Dict Comprehensions).
"""

# 1. Matrix Operations via List Comprehensions
matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12]
]

# Transpose (n x m) using single nested list comprehension
transposed = [[row[c] for row in matrix] for c in range(len(matrix[0]))]
print(f"Transposed Matrix ({len(transposed)}x{len(transposed[0])}):")
print(transposed)

# Flatten retaining multiples of 4
flat_multiples_of_4 = [elem for row in matrix for elem in row if elem % 4 == 0]
print(f"Filtered Flattened List (Multiples of 4): {flat_multiples_of_4}")

# 2. Inverted Text Index via Set and Dict Comprehensions
corpus = {
    "doc1": "python list dict set",
    "doc2": "python tuple list",
    "doc3": "dict hash table"
}

# Vocabulary set comprehension
vocabulary = {word for doc in corpus.values() for word in doc.split()}
print(f"\nUnique Vocabulary ({len(vocabulary)} words): {sorted(vocabulary)}")

# Inverted index dict comprehension mapping word -> set of doc_ids
inverted_index = {
    word: {doc_id for doc_id, doc in corpus.items() if word in doc.split()}
    for word in vocabulary
}

print("Inverted Search Index:")
for word, doc_ids in sorted(inverted_index.items()):
    print(f"- '{word}': {doc_ids}")

# 3. Dictionary Key Inversion & Filtering
user_accounts = {
    101: {"username": "alice_dev", "is_active": True},
    102: {"username": "bob_ops", "is_active": False},
    103: {"username": "charlie_lead", "is_active": True},
    104: {"username": "diana_sec", "is_active": False},
}

active_lookup = {
    info["username"]: uid
    for uid, info in user_accounts.items()
    if info.get("is_active") is True
}

print("\nActive Usernames to ID Lookup:")
print(active_lookup)
