"""
Question 9: Classical Cipher Suite & Automated Frequency-Analysis Cryptanalysis
Topic: Problem Solving & Competitive Programming Patterns

Key Concepts Tested:
- Case-preserving Caesar cipher substitution with arbitrary shift normalization
- Automated cryptanalysis via Chi-Squared (χ²) goodness-of-fit statistic against English letter frequencies
- Polyalphabetic Vigenère cipher encryption and decryption
- Keyword alignment management ignoring non-alphabetic characters
"""

from collections import Counter
from typing import Tuple, Dict


class ClassicalCipherToolkit:
    """
    Classical cryptography suite featuring Caesar cipher, automated
    statistical frequency cracker, and polyalphabetic Vigenère cipher.
    """

    # Standard English monographic letter frequency distribution
    ENGLISH_FREQ: Dict[str, float] = {
        "a": 0.08167, "b": 0.01492, "c": 0.02782, "d": 0.04253, "e": 0.12702,
        "f": 0.02228, "g": 0.02015, "h": 0.06094, "i": 0.06966, "j": 0.00153,
        "k": 0.00772, "l": 0.04025, "m": 0.02406, "n": 0.06749, "o": 0.07507,
        "p": 0.01929, "q": 0.00095, "r": 0.05987, "s": 0.06327, "t": 0.09056,
        "u": 0.02758, "v": 0.00978, "w": 0.02360, "x": 0.00150, "y": 0.01974,
        "z": 0.00074,
    }

    def encrypt_caesar(self, plaintext: str, shift: int) -> str:
        """
        Shifts letters forward by shift positions modulo 26, preserving casing.
        """
        normalized_shift = shift % 26
        result = []

        for ch in plaintext:
            if "a" <= ch <= "z":
                shifted = chr((ord(ch) - ord("a") + normalized_shift) % 26 + ord("a"))
                result.append(shifted)
            elif "A" <= ch <= "Z":
                shifted = chr((ord(ch) - ord("A") + normalized_shift) % 26 + ord("A"))
                result.append(shifted)
            else:
                result.append(ch)

        return "".join(result)

    def decrypt_caesar(self, ciphertext: str, shift: int) -> str:
        """Decrypts Caesar ciphertext by inverting the shift."""
        return self.encrypt_caesar(ciphertext, -shift)

    def crack_caesar(self, ciphertext: str) -> Tuple[int, str, float]:
        """
        Automated frequency-analysis cracker.
        Evaluates all 26 possible shifts and finds the one minimizing Chi-Squared distance.
        Returns (best_shift, decrypted_plaintext, chi_squared_score).
        """
        best_shift = 0
        best_score = float("inf")
        best_plaintext = ciphertext

        for shift in range(26):
            candidate = self.decrypt_caesar(ciphertext, shift)
            letters = [ch.lower() for ch in candidate if ch.isalpha()]
            n_letters = len(letters)

            if n_letters == 0:
                continue

            observed = Counter(letters)
            chi_sq = 0.0
            for char, expected_freq in self.ENGLISH_FREQ.items():
                expected_count = n_letters * expected_freq
                obs_count = observed.get(char, 0)
                chi_sq += ((obs_count - expected_count) ** 2) / expected_count

            if chi_sq < best_score:
                best_score = chi_sq
                best_shift = shift
                best_plaintext = candidate

        return (best_shift, best_plaintext, round(best_score, 2))

    def encrypt_vigenere(self, plaintext: str, keyword: str) -> str:
        """
        Polyalphabetic Vigenère encryption using cyclic keyword characters.
        Non-alphabetic characters do not advance the keyword index.
        """
        if not keyword or not keyword.isalpha():
            raise ValueError(f"Keyword must contain only alphabetic characters, got: '{keyword}'")

        shifts = [ord(k.upper()) - ord("A") for k in keyword]
        result = []
        key_idx = 0
        key_len = len(shifts)

        for ch in plaintext:
            if ch.isalpha():
                shift = shifts[key_idx % key_len]
                key_idx += 1
                base = ord("a") if ch.islower() else ord("A")
                shifted = chr((ord(ch) - base + shift) % 26 + base)
                result.append(shifted)
            else:
                result.append(ch)

        return "".join(result)

    def decrypt_vigenere(self, ciphertext: str, keyword: str) -> str:
        """Polyalphabetic Vigenère decryption by reversing keyword shifts."""
        if not keyword or not keyword.isalpha():
            raise ValueError(f"Keyword must contain only alphabetic characters, got: '{keyword}'")

        # Invert shifts
        inverted_keyword = "".join(
            chr((26 - (ord(k.upper()) - ord("A"))) % 26 + ord("A"))
            for k in keyword
        )
        return self.encrypt_vigenere(ciphertext, inverted_keyword)


if __name__ == "__main__":
    toolkit = ClassicalCipherToolkit()

    print("=== 1. Caesar Cipher Encryption & Decryption ===")
    caesar_plain = "Hello, World! Python Cryptography 101."
    caesar_cipher = toolkit.encrypt_caesar(caesar_plain, shift=7)
    caesar_decrypted = toolkit.decrypt_caesar(caesar_cipher, shift=7)

    print(f"Caesar Encrypted (shift 7): '{caesar_cipher}'")
    print(f"Caesar Decrypted (shift 7): '{caesar_decrypted}'")

    print("\n=== 2. Automated Frequency-Analysis Cracker ===")
    intercepted_text = "Esp bftnv mczhy qzi ufxad zgpc esp wlkj ozr."
    best_shift, cracked_plain, score = toolkit.crack_caesar(intercepted_text)
    print(f"Automated Cracked Shift: {best_shift}")
    print(f"Cracked Plaintext: '{cracked_plain}'")
    print(f"Goodness of Fit Chi-Square Score: {score}")

    print("\n=== 3. Polyalphabetic Vigenère Cipher ===")
    vigenere_plain = "ATTACK AT DAWN"
    vigenere_cipher = toolkit.encrypt_vigenere(vigenere_plain, keyword="LEMON")
    vigenere_decrypted = toolkit.decrypt_vigenere(vigenere_cipher, keyword="LEMON")

    print(f"Vigenère Encrypted ('LEMON'): '{vigenere_cipher}'")
    print(f"Vigenère Decrypted ('LEMON'): '{vigenere_decrypted}'")

    print("\n=== 4. Edge Cases & Validation ===")
    print(f"Large shift 1000: '{toolkit.encrypt_caesar('abc', 1000)}'")
    print(f"Empty string: '{toolkit.encrypt_caesar('', 5)}'")
    try:
        toolkit.encrypt_vigenere("Secret", "KEY123")
    except ValueError as err:
        print(f"Caught invalid keyword: {err}")
