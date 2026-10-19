"""
Topic: Problem Solving - Caesar Cipher and Classical Ciphers
------------------------------------------------------------
Questions Covered:
1. Standard Caesar Cipher: Modulo 26 shift preserving casing and punctuation.
2. ROT13 Involutory Cipher: Symmetric self-inverse substitution.
3. Brute-Force Key Cracking: Exhaustive generation across all 25 key shift permutations.
4. Frequency Analysis & Chi-Squared Decryption: Automatic key discovery via English frequency distribution.
5. Vigenere Polyalphabetic Cipher: Repeating keyword polyalphabetic encryption and decryption.
6. Atbash Mirror Substitution Cipher: Symmetric alphabet reversal (A <-> Z, B <-> Y).
7. Affine Cipher with Modular Inverses: Linear congruent substitution E(x) = (a*x + b) % 26.
8. Rail Fence (Zig-Zag) Transposition Cipher: Rail-depth coordinate transposition.
9. Playfair Digraph Cipher: 5x5 key matrix encryption operating on character pairs.
10. Architectural System: Classical Cryptanalysis Suite with Index of Coincidence (IoC) & Auto-Solver.
"""

import math
import string
import collections
from typing import List, Tuple, Optional, Any, Dict, Set


# ==============================================================================
# Question 1: Standard Caesar Cipher (Encrypt & Decrypt)
# ==============================================================================
def caesar_encrypt(plaintext: str, shift: int) -> str:
    """
    Encrypts plaintext by shifting letters by shift positions (modulo 26).
    Preserves casing and leaves non-alphabetical characters unchanged.
    """
    shift %= 26
    result = []
    for ch in plaintext:
        if ch.isupper():
            result.append(chr((ord(ch) - ord("A") + shift) % 26 + ord("A")))
        elif ch.islower():
            result.append(chr((ord(ch) - ord("a") + shift) % 26 + ord("a")))
        else:
            result.append(ch)
    return "".join(result)


def caesar_decrypt(ciphertext: str, shift: int) -> str:
    """Decrypts ciphertext by inverting shift."""
    return caesar_encrypt(ciphertext, -shift)


def test_q1_standard_caesar():
    msg = "Hello, World! 123"
    cipher = caesar_encrypt(msg, 3)
    assert cipher == "Khoor, Zruog! 123"
    assert caesar_decrypt(cipher, 3) == msg
    # Shift of 26 is identity
    assert caesar_encrypt(msg, 26) == msg
    print("=== Q1: Standard Caesar Cipher Verified ===")


# ==============================================================================
# Question 2: ROT13 Involutory Cipher
# ==============================================================================
def rot13(text: str) -> str:
    """Applies ROT13 shift (13 positions). Running twice recovers original."""
    return caesar_encrypt(text, 13)


def test_q2_rot13():
    orig = "The Quick Brown Fox Jumps Over The Lazy Dog."
    encoded = rot13(orig)
    assert encoded != orig
    assert rot13(encoded) == orig  # Involutory
    assert rot13("hello") == "uryyb"
    print("=== Q2: ROT13 Involutory Cipher Verified ===")


# ==============================================================================
# Question 3: Brute-Force Key Cracking
# ==============================================================================
def crack_caesar_bruteforce(ciphertext: str) -> Dict[int, str]:
    """Generates all 25 possible candidate plaintexts for Caesar ciphertext."""
    return {shift: caesar_decrypt(ciphertext, shift) for shift in range(1, 26)}


def test_q3_bruteforce_cracking():
    cipher = "Khoor, Zruog!"
    candidates = crack_caesar_bruteforce(cipher)
    assert len(candidates) == 25
    assert candidates[3] == "Hello, World!"
    print("=== Q3: Brute-Force Key Cracking Verified ===")


# ==============================================================================
# Question 4: Frequency Analysis & Chi-Squared Automatic Decryption
# ==============================================================================
# Standard English letter frequencies (percentage)
ENGLISH_LETTER_FREQS = {
    "A": 8.167, "B": 1.492, "C": 2.782, "D": 4.253, "E": 12.702, "F": 2.228,
    "G": 2.015, "H": 6.094, "I": 6.966, "J": 0.153, "K": 0.772, "L": 4.025,
    "M": 2.406, "N": 6.749, "O": 7.507, "P": 1.929, "Q": 0.095, "R": 5.987,
    "S": 6.327, "T": 9.056, "U": 2.758, "V": 0.978, "W": 2.360, "X": 0.150,
    "Y": 1.974, "Z": 0.074,
}


def auto_crack_caesar_frequency(ciphertext: str) -> Tuple[int, str]:
    """
    Automatically discovers the Caesar shift using Chi-Squared goodness-of-fit
    against the standard English language letter frequency distribution.
    Returns (best_shift, decrypted_plaintext).
    """
    best_shift = 0
    min_chi2 = float("inf")
    letters_only = [c.upper() for c in ciphertext if c.isalpha()]
    total_letters = len(letters_only)

    if total_letters == 0:
        return 0, ciphertext

    for shift in range(26):
        decrypted = caesar_decrypt(ciphertext, shift)
        dec_letters = [c.upper() for c in decrypted if c.isalpha()]

        observed = collections.Counter(dec_letters)
        chi2 = 0.0

        for letter, expected_pct in ENGLISH_LETTER_FREQS.items():
            expected_count = total_letters * (expected_pct / 100.0)
            obs_count = observed.get(letter, 0)
            chi2 += ((obs_count - expected_count) ** 2) / expected_count

        if chi2 < min_chi2:
            min_chi2 = chi2
            best_shift = shift

    return best_shift, caesar_decrypt(ciphertext, best_shift)


def test_q4_frequency_analysis():
    secret_text = "To be or not to be, that is the question. Whether 'tis nobler in the mind to suffer."
    encrypted = caesar_encrypt(secret_text, shift=14)

    recovered_shift, recovered_text = auto_crack_caesar_frequency(encrypted)
    assert recovered_shift == 14
    assert recovered_text == secret_text
    print("=== Q4: Frequency Analysis & Chi-Squared Decryption Verified ===")


# ==============================================================================
# Question 5: Vigenere Polyalphabetic Cipher
# ==============================================================================
def vigenere_encrypt(plaintext: str, key: str) -> str:
    """Encrypts plaintext using repeating keyword Vigenere polyalphabetic cipher."""
    clean_key = [c.upper() for c in key if c.isalpha()]
    if not clean_key:
        raise ValueError("Key must contain alphabetical characters")

    result = []
    key_idx = 0
    key_len = len(clean_key)

    for ch in plaintext:
        if ch.isalpha():
            shift = ord(clean_key[key_idx % key_len]) - ord("A")
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base + shift) % 26 + base))
            key_idx += 1
        else:
            result.append(ch)

    return "".join(result)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """Decrypts Vigenere ciphertext."""
    clean_key = [c.upper() for c in key if c.isalpha()]
    if not clean_key:
        raise ValueError("Key must contain alphabetical characters")

    result = []
    key_idx = 0
    key_len = len(clean_key)

    for ch in ciphertext:
        if ch.isalpha():
            shift = ord(clean_key[key_idx % key_len]) - ord("A")
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base - shift + 26) % 26 + base))
            key_idx += 1
        else:
            result.append(ch)

    return "".join(result)


def test_q5_vigenere_cipher():
    msg = "ATTACKATDAWN"
    key = "LEMON"
    cipher = vigenere_encrypt(msg, key)
    # L(11) E(4) M(12) O(14) N(13) -> LXFOPVEFRNHR
    assert cipher == "LXFOPVEFRNHR"
    assert vigenere_decrypt(cipher, key) == msg
    print("=== Q5: Vigenere Polyalphabetic Cipher Verified ===")


# ==============================================================================
# Question 6: Atbash Mirror Substitution Cipher
# ==============================================================================
def atbash_cipher(text: str) -> str:
    """
    Substitutes each letter with its symmetric reverse in the alphabet:
    A <-> Z, B <-> Y, C <-> X, etc.
    """
    result = []
    for ch in text:
        if ch.isupper():
            result.append(chr(ord("Z") - (ord(ch) - ord("A"))))
        elif ch.islower():
            result.append(chr(ord("z") - (ord(ch) - ord("a"))))
        else:
            result.append(ch)
    return "".join(result)


def test_q6_atbash():
    msg = "ABC xyz 123"
    enc = atbash_cipher(msg)
    assert enc == "ZYX cba 123"
    assert atbash_cipher(enc) == msg  # Involutory
    print("=== Q6: Atbash Mirror Substitution Cipher Verified ===")


# ==============================================================================
# Question 7: Affine Cipher with Modular Inverses
# ==============================================================================
def affine_encrypt(plaintext: str, a: int, b: int) -> str:
    """
    Affine cipher formula: E(x) = (a * x + b) % 26.
    Requirement: gcd(a, 26) == 1.
    """
    if math.gcd(a, 26) != 1:
        raise ValueError(f"'a' ({a}) must be coprime to 26")

    result = []
    for ch in plaintext:
        if ch.isupper():
            x = ord(ch) - ord("A")
            result.append(chr((a * x + b) % 26 + ord("A")))
        elif ch.islower():
            x = ord(ch) - ord("a")
            result.append(chr((a * x + b) % 26 + ord("a")))
        else:
            result.append(ch)
    return "".join(result)


def affine_decrypt(ciphertext: str, a: int, b: int) -> str:
    """
    Affine decrypt formula: D(y) = a^-1 * (y - b) % 26.
    """
    if math.gcd(a, 26) != 1:
        raise ValueError(f"'a' ({a}) must be coprime to 26")

    # Modular inverse of a mod 26
    a_inv = pow(a, -1, 26)

    result = []
    for ch in ciphertext:
        if ch.isupper():
            y = ord(ch) - ord("A")
            result.append(chr((a_inv * (y - b)) % 26 + ord("A")))
        elif ch.islower():
            y = ord(ch) - ord("a")
            result.append(chr((a_inv * (y - b)) % 26 + ord("a")))
        else:
            result.append(ch)
    return "".join(result)


def test_q7_affine_cipher():
    msg = "AFFINE CIPHER"
    a, b = 5, 8  # gcd(5, 26) == 1
    cipher = affine_encrypt(msg, a, b)
    assert cipher == "IHHWVC SWFRCP"
    assert affine_decrypt(cipher, a, b) == msg
    print("=== Q7: Affine Cipher with Modular Inverses Verified ===")


# ==============================================================================
# Question 8: Rail Fence (Zig-Zag) Transposition Cipher
# ==============================================================================
def rail_fence_encrypt(text: str, num_rails: int) -> str:
    """Encrypts text by writing along num_rails in a zig-zag and reading row by row."""
    if num_rails <= 1 or num_rails >= len(text):
        return text

    rails: List[List[str]] = [[] for _ in range(num_rails)]
    current_rail = 0
    step = 1

    for ch in text:
        rails[current_rail].append(ch)
        current_rail += step
        if current_rail == 0 or current_rail == num_rails - 1:
            step = -step

    return "".join("".join(r) for r in rails)


def rail_fence_decrypt(ciphertext: str, num_rails: int) -> str:
    """Decrypts rail fence ciphertext."""
    if num_rails <= 1 or num_rails >= len(ciphertext):
        return ciphertext

    # 1. Determine positions along rails
    rail_lengths = [0] * num_rails
    current_rail = 0
    step = 1
    for _ in ciphertext:
        rail_lengths[current_rail] += 1
        current_rail += step
        if current_rail == 0 or current_rail == num_rails - 1:
            step = -step

    # 2. Slice ciphertext into rails
    rails: List[List[str]] = []
    idx = 0
    for length in rail_lengths:
        rails.append(list(ciphertext[idx : idx + length]))
        idx += length

    # 3. Read back in zig-zag order
    result = []
    current_rail = 0
    step = 1
    for _ in ciphertext:
        result.append(rails[current_rail].pop(0))
        current_rail += step
        if current_rail == 0 or current_rail == num_rails - 1:
            step = -step

    return "".join(result)


def test_q8_rail_fence():
    msg = "DEFENDTHEEASTWALL"
    num_rails = 3
    cipher = rail_fence_encrypt(msg, num_rails)
    assert cipher == "DNETLEEDHESWLFTAA"
    assert rail_fence_decrypt(cipher, num_rails) == msg
    print("=== Q8: Rail Fence Transposition Cipher Verified ===")


# ==============================================================================
# Question 9: Playfair Digraph 5x5 Cipher
# ==============================================================================
def build_playfair_matrix(key: str) -> List[List[str]]:
    """Builds 5x5 key matrix omitting 'J' (combining I and J)."""
    clean_key = []
    for c in key.upper():
        if c.isalpha():
            ch = "I" if c == "J" else c
            if ch not in clean_key:
                clean_key.append(ch)

    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in clean_key:
            clean_key.append(ch)

    return [clean_key[i * 5 : (i + 1) * 5] for i in range(5)]


def playfair_encrypt(plaintext: str, key: str) -> str:
    """Encrypts plaintext pairs using Playfair rules (same row -> shift right, same col -> shift down, rect -> swap cols)."""
    matrix = build_playfair_matrix(key)
    # Find pos lookup
    pos = {}
    for r in range(5):
        for c in range(5):
            pos[matrix[r][c]] = (r, c)

    # Form digraphs
    raw_letters = [("I" if c == "J" else c) for c in plaintext.upper() if c.isalpha()]
    pairs = []
    i = 0
    while i < len(raw_letters):
        c1 = raw_letters[i]
        if i + 1 < len(raw_letters):
            c2 = raw_letters[i + 1]
            if c1 == c2:
                pairs.append((c1, "X"))
                i += 1
            else:
                pairs.append((c1, c2))
                i += 2
        else:
            pairs.append((c1, "X"))
            i += 1

    cipher = []
    for c1, c2 in pairs:
        r1, col1 = pos[c1]
        r2, col2 = pos[c2]

        if r1 == r2:  # Same row
            cipher.append(matrix[r1][(col1 + 1) % 5])
            cipher.append(matrix[r2][(col2 + 1) % 5])
        elif col1 == col2:  # Same column
            cipher.append(matrix[(r1 + 1) % 5][col1])
            cipher.append(matrix[(r2 + 1) % 5][col2])
        else:  # Rectangle
            cipher.append(matrix[r1][col2])
            cipher.append(matrix[r2][col1])

    return "".join(cipher)


def test_q9_playfair():
    key = "MONARCHY"
    encrypted = playfair_encrypt("INSTRUMENTS", key)
    # Instruments formed into: IN ST RU ME NT SX
    assert len(encrypted) == 12
    assert playfair_encrypt("HELLO", key) != "HELLO"
    print("=== Q9: Playfair Digraph Cipher Verified ===")


# ==============================================================================
# Question 10: Architectural Classical Cryptanalysis Suite & Solver Gateway
# ==============================================================================
class ClassicalCryptanalysisSuite:
    """
    Automated cryptanalysis engine:
    1. Computes Index of Coincidence (IoC) to detect monoalphabetic vs polyalphabetic
       (English monoalphabetic IoC ~= 0.066, random text ~= 0.038)
    2. Identifies and breaks Caesar and Atbash ciphers automatically
    """
    @classmethod
    def index_of_coincidence(cls, text: str) -> float:
        letters = [c.upper() for c in text if c.isalpha()]
        n = len(letters)
        if n <= 1:
            return 0.0
        counts = collections.Counter(letters)
        numerator = sum(count * (count - 1) for count in counts.values())
        return numerator / (n * (n - 1))

    @classmethod
    def analyze_and_decrypt(cls, ciphertext: str) -> Dict[str, Any]:
        ioc = cls.index_of_coincidence(ciphertext)
        is_monoalphabetic = ioc > 0.055

        # Attempt Caesar crack
        caesar_shift, caesar_candidate = auto_crack_caesar_frequency(ciphertext)

        # Check Atbash
        atbash_candidate = atbash_cipher(ciphertext)

        return {
            "index_of_coincidence": round(ioc, 4),
            "is_likely_monoalphabetic": is_monoalphabetic,
            "best_caesar_shift": caesar_shift,
            "caesar_decrypted": caesar_candidate,
            "atbash_decrypted": atbash_candidate,
        }


def test_q10_cryptanalysis_suite():
    secret = "The secret meeting will take place at dawn behind the old lighthouse."
    encrypted = caesar_encrypt(secret, 7)

    result = ClassicalCryptanalysisSuite.analyze_and_decrypt(encrypted)
    # IoC for Caesar cipher of English text matches English IoC (~0.06)
    assert result["is_likely_monoalphabetic"] is True
    assert result["best_caesar_shift"] == 7
    assert result["caesar_decrypted"] == secret
    print("=== Q10: Architectural Classical Cryptanalysis Suite Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_standard_caesar()
    test_q2_rot13()
    test_q3_bruteforce_cracking()
    test_q4_frequency_analysis()
    test_q5_vigenere_cipher()
    test_q6_atbash()
    test_q7_affine_cipher()
    test_q8_rail_fence()
    test_q9_playfair()
    test_q10_cryptanalysis_suite()
    print("\nAll 10 Caesar and classical cipher problem-solving questions passed successfully!")
