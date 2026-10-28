"""
Question 6: Analytical Comprehensions & Inverted Search Index Pipeline
Topic: Advanced Python

Key Concepts Tested:
- Single-expression nested list comprehensions (matrix transposition, 2D filtering)
- Set comprehensions for deduplication and token extraction
- Dict comprehensions with conditional filtering and key normalization
- Inverted index search architecture
- Rectangular matrix validation and edge cases
"""

from typing import List, Dict, Set, Any


class ComprehensionPipeline:
    """
    Data processing pipeline implemented purely with concise, expressive
    list, dict, and set comprehensions.
    """

    @staticmethod
    def transpose_matrix(grid: List[List[float]]) -> List[List[float]]:
        """
        Transposes an N x M grid into an M x N grid using a single nested list comprehension.
        Validates rectangular geometry.
        """
        if not grid or not grid[0]:
            return []

        expected_width = len(grid[0])
        if any(len(row) != expected_width for row in grid):
            raise ValueError("Matrix must have rectangular dimensions")

        return [[row[col] for row in grid] for col in range(expected_width)]

    @staticmethod
    def flatten_and_filter_divisible(grid: List[List[int]], divisor: int) -> List[int]:
        """
        Flattens a 2D matrix into 1D, keeping only numbers divisible by divisor.
        """
        return [num for row in grid for num in row if num % divisor == 0]

    @staticmethod
    def build_inverted_index(documents: Dict[str, List[str]]) -> Dict[str, Set[str]]:
        """
        Builds an inverted search index mapping unique words to document IDs.
        Constructed using nested set and dict comprehensions.
        """
        # Set comprehension to collect all normalized unique words
        unique_words = {word.lower() for words in documents.values() for word in words}

        # Dict comprehension creating word -> {matching doc_ids} mapping
        return {
            word: {
                doc_id
                for doc_id, doc_words in documents.items()
                if word in {w.lower() for w in doc_words}
            }
            for word in unique_words
        }

    @staticmethod
    def normalize_user_scores(raw_data: Dict[str, Dict[str, Any]], pass_threshold: float = 70.0) -> Dict[str, float]:
        """
        Filters active users meeting the passing threshold, applies a 10% curve,
        and capitalizes usernames.
        """
        return {
            user_id.upper(): round(data["score"] * 1.1, 2)
            for user_id, data in raw_data.items()
            if data.get("is_active") and data.get("score", 0.0) >= pass_threshold
        }

    @staticmethod
    def extract_unique_email_domains(emails: List[str]) -> Set[str]:
        """
        Extracts lowercase domain names from valid email addresses using set comprehension.
        """
        return {
            email.split("@")[1].strip().lower()
            for email in emails
            if "@" in email and "." in email.split("@")[1]
        }


if __name__ == "__main__":
    pipeline = ComprehensionPipeline()

    print("=== 1. Matrix Transposition ===")
    matrix = [
        [1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0],
    ]
    transposed = pipeline.transpose_matrix(matrix)
    print("Transposed 2x3 to 3x2 Matrix:")
    print(transposed)

    print("\n=== 2. 2D Flatten & Divisible Filter ===")
    grid_data = [
        [10, 15, 22],
        [30, 41, 55],
        [60, 73, 80],
    ]
    div_5 = pipeline.flatten_and_filter_divisible(grid_data, 5)
    print(f"Elements divisible by 5: {div_5}")

    print("\n=== 3. Inverted Search Index ===")
    corpus = {
        "doc_1": ["python", "async", "fast"],
        "doc_2": ["python", "threading", "gil"],
        "doc_3": ["rust", "fast", "safe"],
    }
    index = pipeline.build_inverted_index(corpus)
    print("Inverted Index Search:")
    for term in ["python", "fast", "rust"]:
        print(f"- '{term}': {index.get(term, set())}")

    print("\n=== 4. User Score Normalization ===")
    users = {
        "usr_alice": {"score": 85.0, "is_active": True},
        "usr_bob": {"score": 62.0, "is_active": True},  # Below 70 threshold
        "usr_charlie": {"score": 95.0, "is_active": False},  # Inactive
        "usr_diana": {"score": 75.0, "is_active": True},
    }
    normalized = pipeline.normalize_user_scores(users, pass_threshold=70.0)
    print(f"Curved Active Passing Scores: {normalized}")

    print("\n=== 5. Unique Domain Extraction ===")
    raw_emails = ["Alice@Corp.Net", "bob@gmail.com", "charlie@CORP.NET", "bad-email", "david@yahoo.com"]
    domains = pipeline.extract_unique_email_domains(raw_emails)
    print(f"Unique Domains Extracted: {sorted(domains)}")

    print("\n=== 6. Edge Case Validations ===")
    print(f"Empty Matrix Transpose: {pipeline.transpose_matrix([])}")
    try:
        pipeline.transpose_matrix([[1, 2], [3]])
    except ValueError as e:
        print(f"Ragged Matrix Validation Caught: {e}")
