"""
Question 7: Lossless Run-Length Encoding (RLE) & In-Place Array Compressor
Topic: Problem Solving & Competitive Programming Patterns

Key Concepts Tested:
- Run-Length Encoding (RLE) string compression with shorter-length enforcement
- Multi-digit decompression parser with strict syntax validation
- In-place array compression with O(1) auxiliary space (LeetCode 443 pattern)
- Compression analytics (compression ratio, space saved)
"""

import re
from typing import List, Dict, Any


class StringCompressor:
    """
    Lossless Run-Length Encoding (RLE) engine and array compressor.
    """

    @staticmethod
    def compress(s: str, enforce_shorter: bool = True) -> str:
        """
        Compresses string using RLE format: [char][count].
        If enforce_shorter is True and compressed is not strictly shorter, returns original.
        """
        if not s:
            return ""

        parts = []
        curr_char = s[0]
        count = 1

        for i in range(1, len(s)):
            if s[i] == curr_char:
                count += 1
            else:
                parts.append(f"{curr_char}{count}")
                curr_char = s[i]
                count = 1
        parts.append(f"{curr_char}{count}")

        compressed = "".join(parts)
        if enforce_shorter and len(compressed) >= len(s):
            return s
        return compressed

    @staticmethod
    def decompress(compressed: str) -> str:
        """
        Decompresses RLE strings supporting multi-digit counts (e.g. 'w10b2x1').
        Raises ValueError on malformed inputs.
        """
        if not compressed:
            return ""

        # Validate syntax: must be sequences of (non-digit followed by 1+ digits)
        tokens = re.findall(r"([^0-9])([0-9]+)", compressed)
        reconstructed_len = sum(len(ch) + len(digits) for ch, digits in tokens)

        if reconstructed_len != len(compressed) or not tokens:
            raise ValueError(f"Malformed compressed string: '{compressed}'")

        expanded_parts = []
        for ch, count_str in tokens:
            expanded_parts.append(ch * int(count_str))

        return "".join(expanded_parts)

    @staticmethod
    def compress_char_array_inplace(chars: List[str]) -> int:
        """
        Compresses an array of characters in-place using O(1) auxiliary space.
        Consecutive repeating groups write character followed by count digits (if count > 1).
        Returns the new valid length.
        """
        write_idx = 0
        read_idx = 0
        n = len(chars)

        while read_idx < n:
            curr_char = chars[read_idx]
            count = 0

            while read_idx < n and chars[read_idx] == curr_char:
                read_idx += 1
                count += 1

            chars[write_idx] = curr_char
            write_idx += 1

            if count > 1:
                for digit_char in str(count):
                    chars[write_idx] = digit_char
                    write_idx += 1

        return write_idx

    @staticmethod
    def compression_stats(original: str, compressed: str) -> Dict[str, Any]:
        """Calculates compression metrics and percentage savings."""
        orig_len = len(original)
        comp_len = len(compressed)
        saved = orig_len - comp_len
        ratio = round((saved / orig_len) * 100, 2) if orig_len > 0 else 0.0

        return {
            "original_length": orig_len,
            "compressed_length": comp_len,
            "bytes_saved": saved,
            "compression_ratio": ratio,
        }


if __name__ == "__main__":
    compressor = StringCompressor()

    print("=== 1. Standard Compression ===")
    s1 = "aabcccccaaa"
    comp1 = compressor.compress(s1)
    print(f"Compressed '{s1}': '{comp1}'")

    print("\n=== 2. Shorter Length Enforced ===")
    s2 = "abcdef"
    comp2 = compressor.compress(s2, enforce_shorter=True)
    print(f"Compressed '{s2}' (shorter enforced): '{comp2}'")

    print("\n=== 3. Multi-Digit Decompression ===")
    decomp = compressor.decompress("w10b2x1")
    print(f"Decompressed 'w10b2x1': '{decomp}'")

    print("\n=== 4. In-Place Array Compression ===")
    char_arr = ["a", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"]
    new_len = compressor.compress_char_array_inplace(char_arr)
    print(f"In-Place Array New Length: {new_len} (Array prefix: {char_arr[:new_len]})")

    print("\n=== 5. Compression Analytics ===")
    stats = compressor.compression_stats(s1, comp1)
    print(f"Compression Ratio for '{s1}': {stats['compression_ratio']}% savings ({stats['original_length']} -> {stats['compressed_length']} chars)")

    print("\n=== 6. Edge Cases & Validation ===")
    print(f"Empty string compression: '{compressor.compress('')}'")
    print(f"Empty string decompression: '{compressor.decompress('')}'")
    try:
        compressor.decompress("12abc")
    except ValueError as err:
        print(f"Caught malformed decompression input: {err}")
