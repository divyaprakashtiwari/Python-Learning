"""
Topic 01 - Python Basics & Variables
Practice Question 8 Solution: Number Systems & POSIX Permission Decoder

Problem Statement:
1. Accept integer representing POSIX permission code (e.g. 493 -> octal 0o755).
2. Display representations across Decimal, Binary (9-bit), Octal, Hexadecimal.
3. Using bitwise operations (&, >>), decode the 9 permission bits into symbolic
   format "rwxrwxrwx" (User, Group, Others).
4. Calculate bit_length() and bit_count().
"""


def decode_posix_permission(code: int) -> dict[str, object]:
    """Decodes an integer permission code using bitwise operations across number systems."""
    if not (0 <= code <= 511):
        raise ValueError("POSIX mode integer must be between 0 (0o000) and 511 (0o777).")

    # Number systems
    bin_str = f"{code:09b}"
    oct_str = f"{code:03o}"
    hex_str = f"{code:#x}"

    # Symbolic decoding using bitwise shifts and masks
    # Bit positions from MSB to LSB (8 down to 0):
    # User: 8 (r), 7 (w), 6 (x)
    # Group: 5 (r), 4 (w), 3 (x)
    # Other: 2 (r), 1 (w), 0 (x)
    symbolic_chars = []
    triplet_patterns = [
        (8, "r"), (7, "w"), (6, "x"),
        (5, "r"), (4, "w"), (3, "x"),
        (2, "r"), (1, "w"), (0, "x"),
    ]

    for bit_pos, char in triplet_patterns:
        # Check if bit at bit_pos is 1
        if (code >> bit_pos) & 1:
            symbolic_chars.append(char)
        else:
            symbolic_chars.append("-")

    symbolic_perm = "".join(symbolic_chars)

    return {
        "decimal": code,
        "binary_raw": bin(code),
        "binary_9bit": bin_str,
        "octal": f"0o{oct_str}",
        "hexadecimal": hex_str,
        "symbolic": symbolic_perm,
        "bit_length": code.bit_length(),
        "active_bits": code.bit_count(),
    }


def main() -> None:
    permission_code = 493  # Octal 0o755

    res = decode_posix_permission(permission_code)

    print(f"{'Decimal Representation':<24}: {res['decimal']}")
    print(f"{'Binary Representation':<24}: {res['binary_raw']} (9 bits: {res['binary_9bit']})")
    print(f"{'Octal Representation':<24}: {res['octal']}")
    print(f"{'Hexadecimal':<24}: {res['hexadecimal']}")
    print(f"{'Symbolic Permissions':<24}: {res['symbolic']}")
    print(f"{'Bit Length':<24}: {res['bit_length']} bits")
    print(f"{'Active Permission Bits':<24}: {res['active_bits']}")


if __name__ == "__main__":
    main()
