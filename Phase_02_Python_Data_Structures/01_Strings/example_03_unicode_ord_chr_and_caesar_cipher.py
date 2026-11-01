"""
Topic 01: Strings
Example 03: Unicode Code Points (`ord`, `chr`) and Caesar Cipher

Demonstrates how Python represents characters as Unicode code points and implements
a circular alphabet shift (Caesar Cipher) using `ord()` and `chr()`.
"""


def caesar_cipher(text: str, shift: int) -> str:
    """Shift alphabetic characters by `shift` positions while preserving case."""
    result_chars: list[str] = []

    for ch in text:
        if ch.isupper():
            base = ord("A")
            shifted = (ord(ch) - base + shift) % 26 + base
            result_chars.append(chr(shifted))
        elif ch.islower():
            base = ord("a")
            shifted = (ord(ch) - base + shift) % 26 + base
            result_chars.append(chr(shifted))
        else:
            result_chars.append(ch)

    return "".join(result_chars)


def main() -> None:
    print("=== 1. Unicode Code Points (ord & chr) ===")
    for ch in ["A", "Z", "a", "0"]:
        print(f"  Character {ch!r} -> ord({ch!r}) = {ord(ch):>3} -> chr({ord(ch)}) = {chr(ord(ch))!r}")

    print("\n=== 2. Caesar Cipher Encryption & Decryption ===")
    secret_message = "Meet at Gate 04 at 18:30!"
    shift_key = 5
    encrypted = caesar_cipher(secret_message, shift=shift_key)
    decrypted = caesar_cipher(encrypted, shift=-shift_key)

    print(f"Original Message  : {secret_message}")
    print(f"Encrypted (+{shift_key})    : {encrypted}")
    print(f"Decrypted (-{shift_key})    : {decrypted}")


if __name__ == "__main__":
    main()
