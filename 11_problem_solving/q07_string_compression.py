"""
Topic: Problem Solving - String Compression
-------------------------------------------
Questions Covered:
1. Run-Length Encoding (RLE): Compression and exact lossless decompression.
2. In-Place Character Array Compression: Two-pointer in-place compaction with digit splitting.
3. Word-Level Run-Length Compression: Tokenized sentence compaction with repeated count markers.
4. Huffman Coding from Scratch: Min-heap tree construction, prefix codes, bitstring encoding & decoding.
5. LZW (Lempel-Ziv-Welch) Compression: Dynamic dictionary token replacement and reconstruction.
6. Byte Pair Encoding (BPE): Iterative frequent bigram pair replacement.
7. Binary Run-Length Bitmap Compression: Bitmask run sequences for spatial masks.
8. Delta Encoding for Sorted Sequences: Storing first element and subsequent differences.
9. Varint / Variable-Byte Integer Encoding: Protocol Buffer-style 7-bit continuation encoding.
10. Architectural System: Multi-Algorithm Telemetry Compressor with Entropy-Adaptive Selection.
"""

import heapq
import collections
from typing import List, Tuple, Optional, Any, Dict


# ==============================================================================
# Question 1: Run-Length Encoding (RLE) and Decompression
# ==============================================================================
def rle_compress(s: str) -> str:
    """Compresses string into run-length encoding: 'aaabbc' -> 'a3b2c1'."""
    if not s:
        return ""

    encoded = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            encoded.append(f"{s[i - 1]}{count}")
            count = 1
    encoded.append(f"{s[-1]}{count}")
    return "".join(encoded)


def rle_decompress(encoded: str) -> str:
    """Decompresses 'a3b2c1' back into 'aaabbc'."""
    decoded = []
    i = 0
    n = len(encoded)

    while i < n:
        ch = encoded[i]
        i += 1
        num_str = []
        while i < n and encoded[i].isdigit():
            num_str.append(encoded[i])
            i += 1
        count = int("".join(num_str)) if num_str else 1
        decoded.append(ch * count)

    return "".join(decoded)


def test_q1_rle():
    orig = "aaabbccccdddddd"
    comp = rle_compress(orig)
    assert comp == "a3b2c4d6"
    assert rle_decompress(comp) == orig
    assert rle_compress("") == ""
    assert rle_decompress("") == ""
    print("=== Q1: Run-Length Encoding and Decompression Verified ===")


# ==============================================================================
# Question 2: In-Place Character Array Compression
# ==============================================================================
def compress_chars_inplace(chars: List[str]) -> int:
    """
    Compresses character array in-place:
    If a character run has length 1, write character.
    If run > 1, write character followed by digits of length.
    Returns new length k of chars[:k].
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
            for digit in str(count):
                chars[write_idx] = digit
                write_idx += 1

    return write_idx


def test_q2_compress_chars_inplace():
    # ["a","a","b","b","c","c","c"] -> ["a","2","b","2","c","3"], return 6
    arr1 = ["a", "a", "b", "b", "c", "c", "c"]
    k1 = compress_chars_inplace(arr1)
    assert k1 == 6
    assert arr1[:k1] == ["a", "2", "b", "2", "c", "3"]

    # ["a"] -> ["a"], return 1
    arr2 = ["a"]
    k2 = compress_chars_inplace(arr2)
    assert k2 == 1
    assert arr2[:k2] == ["a"]

    # 12 'b's -> 'b', '1', '2'
    arr3 = ["a"] + ["b"] * 12
    k3 = compress_chars_inplace(arr3)
    assert k3 == 4
    assert arr3[:k3] == ["a", "b", "1", "2"]
    print("=== Q2: In-Place Character Array Compression Verified ===")


# ==============================================================================
# Question 3: Word-Level Run-Length Encoding
# ==============================================================================
def word_rle_compress(sentence: str) -> str:
    """Compresses repeated words: 'echo echo echo test' -> 'echo(3) test(1)'."""
    words = sentence.split()
    if not words:
        return ""

    compressed = []
    curr_word = words[0]
    count = 1

    for w in words[1:]:
        if w == curr_word:
            count += 1
        else:
            compressed.append(f"{curr_word}({count})")
            curr_word = w
            count = 1
    compressed.append(f"{curr_word}({count})")

    return " ".join(compressed)


def test_q3_word_rle():
    text = "hello hello hello world world again"
    assert word_rle_compress(text) == "hello(3) world(2) again(1)"
    print("=== Q3: Word-Level Run-Length Encoding Verified ===")


# ==============================================================================
# Question 4: Huffman Coding (Prefix Code Tree) from Scratch
# ==============================================================================
class HuffmanNode:
    def __init__(self, char: Optional[str], freq: int, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other: "HuffmanNode") -> bool:
        return self.freq < other.freq


class HuffmanCoding:
    @classmethod
    def build_tree(cls, text: str) -> Optional[HuffmanNode]:
        if not text:
            return None
        freq = collections.Counter(text)
        heap: List[HuffmanNode] = [HuffmanNode(ch, count) for ch, count in freq.items()]
        heapq.heapify(heap)

        if len(heap) == 1:
            node = heapq.heappop(heap)
            return HuffmanNode(None, node.freq, left=node)

        while len(heap) > 1:
            n1 = heapq.heappop(heap)
            n2 = heapq.heappop(heap)
            merged = HuffmanNode(None, n1.freq + n2.freq, left=n1, right=n2)
            heapq.heappush(heap, merged)

        return heap[0]

    @classmethod
    def generate_codes(cls, root: Optional[HuffmanNode]) -> Dict[str, str]:
        codes = {}

        def traverse(node, prefix):
            if not node:
                return
            if node.char is not None:
                codes[node.char] = prefix or "0"
                return
            traverse(node.left, prefix + "0")
            traverse(node.right, prefix + "1")

        traverse(root, "")
        return codes

    @classmethod
    def encode(cls, text: str) -> Tuple[str, Optional[HuffmanNode]]:
        root = cls.build_tree(text)
        codes = cls.generate_codes(root)
        bitstring = "".join(codes[ch] for ch in text)
        return bitstring, root

    @classmethod
    def decode(cls, bitstring: str, root: Optional[HuffmanNode]) -> str:
        if not bitstring or not root:
            return ""

        decoded = []
        curr = root
        for bit in bitstring:
            curr = curr.left if bit == "0" else curr.right
            if curr and curr.char is not None:
                decoded.append(curr.char)
                curr = root

        return "".join(decoded)


def test_q4_huffman_coding():
    text = "BEEP BOOP BEER"
    bitstring, tree = HuffmanCoding.encode(text)
    decoded = HuffmanCoding.decode(bitstring, tree)
    assert decoded == text
    assert len(bitstring) < len(text) * 8  # Substantial compression compared to 8-bit ASCII
    print("=== Q4: Huffman Coding Prefix Tree from Scratch Verified ===")


# ==============================================================================
# Question 5: LZW (Lempel-Ziv-Welch) Dictionary Compression
# ==============================================================================
def lzw_compress(uncompressed: str) -> List[int]:
    """Compresses string to list of integer dictionary code tokens."""
    dict_size = 256
    dictionary: Dict[str, int] = {chr(i): i for i in range(dict_size)}

    w = ""
    result: List[int] = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    if w:
        result.append(dictionary[w])

    return result


def lzw_decompress(compressed: List[int]) -> str:
    """Decompresses list of integer codes back to original string."""
    dict_size = 256
    dictionary: Dict[int, str] = {i: chr(i) for i in range(dict_size)}

    if not compressed:
        return ""

    w = chr(compressed[0])
    result = [w]

    for k in compressed[1:]:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError(f"Bad compressed code: {k}")

        result.append(entry)
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        w = entry

    return "".join(result)


def test_q5_lzw_compression():
    text = "TOBEORNOTTOBEORTOBEORNOT"
    comp = lzw_compress(text)
    # Compressed has fewer codes than raw characters
    assert len(comp) < len(text)
    decomp = lzw_decompress(comp)
    assert decomp == text
    print("=== Q5: LZW Dictionary Compression Verified ===")


# ==============================================================================
# Question 6: Byte Pair Encoding (BPE)
# ==============================================================================
def byte_pair_encode(text: str, iterations: int = 3) -> Tuple[str, List[Tuple[str, str]]]:
    """
    Subword tokenization via Byte Pair Encoding:
    Finds most frequent adjacent pair in string, replaces with novel token.
    """
    tokens = list(text)
    merges: List[Tuple[str, str]] = []

    for step in range(iterations):
        pairs = collections.Counter(zip(tokens[:-1], tokens[1:]))
        if not pairs:
            break
        best_pair, freq = pairs.most_common(1)[0]
        if freq < 2:
            break  # No benefit merging pairs with frequency < 2

        new_token = chr(256 + step)
        merges.append(best_pair)

        # Replace pair in tokens list
        new_tokens = []
        i = 0
        while i < len(tokens):
            if i < len(tokens) - 1 and (tokens[i], tokens[i + 1]) == best_pair:
                new_tokens.append(new_token)
                i += 2
            else:
                new_tokens.append(tokens[i])
                i += 1
        tokens = new_tokens

    return "".join(tokens), merges


def test_q6_byte_pair_encoding():
    text = "aaabdaaabac"
    encoded_str, merges = byte_pair_encode(text, iterations=2)
    # Most frequent pair initially is ('a', 'a')
    assert ('a', 'a') in merges
    assert len(encoded_str) < len(text)
    print("=== Q6: Byte Pair Encoding (BPE) Verified ===")


# ==============================================================================
# Question 7: Binary Run-Length Bitmap Mask Compression
# ==============================================================================
def compress_bitmap_mask(bits: List[int]) -> List[int]:
    """
    Compresses binary bitmap list [0, 0, 0, 1, 1, 0] into run counts.
    Format: [initial_bit_value, count1, count2, count3, ...]
    """
    if not bits:
        return []

    compressed = [bits[0]]
    curr_bit = bits[0]
    count = 0

    for b in bits:
        if b == curr_bit:
            count += 1
        else:
            compressed.append(count)
            curr_bit = b
            count = 1
    compressed.append(count)

    return compressed


def decompress_bitmap_mask(compressed: List[int]) -> List[int]:
    """Decompresses [initial_bit, count1, count2...] back to binary bitmap."""
    if not compressed:
        return []

    curr_bit = compressed[0]
    result = []
    for count in compressed[1:]:
        result.extend([curr_bit] * count)
        curr_bit = 1 - curr_bit  # Flip bit

    return result


def test_q7_bitmap_compression():
    mask = [0, 0, 0, 0, 1, 1, 1, 0, 0, 1]
    comp = compress_bitmap_mask(mask)
    # Starts with 0, then 4 zeros, 3 ones, 2 zeros, 1 one -> [0, 4, 3, 2, 1]
    assert comp == [0, 4, 3, 2, 1]
    assert decompress_bitmap_mask(comp) == mask
    print("=== Q7: Binary Run-Length Bitmap Compression Verified ===")


# ==============================================================================
# Question 8: Delta Encoding for Sorted Sequences
# ==============================================================================
def delta_encode(nums: List[int]) -> List[int]:
    """
    Compresses sorted integer sequence:
    Stores first number as baseline, subsequent numbers as differences:
    [100, 102, 105, 109] -> [100, 2, 3, 4].
    """
    if not nums:
        return []
    encoded = [nums[0]]
    for i in range(1, len(nums)):
        encoded.append(nums[i] - nums[i - 1])
    return encoded


def delta_decode(encoded: List[int]) -> List[int]:
    if not encoded:
        return []
    decoded = [encoded[0]]
    for diff in encoded[1:]:
        decoded.append(decoded[-1] + diff)
    return decoded


def test_q8_delta_encoding():
    timestamps = [1700000000, 1700000005, 1700000012, 1700000020]
    encoded = delta_encode(timestamps)
    assert encoded == [1700000000, 5, 7, 8]
    assert delta_decode(encoded) == timestamps
    print("=== Q8: Delta Encoding for Sorted Sequences Verified ===")


# ==============================================================================
# Question 9: Varint / Variable-Byte Integer Encoding
# ==============================================================================
def encode_varint(val: int) -> bytes:
    """
    Encodes non-negative integer into variable-byte sequence (Protocol Buffers varint).
    Lowest 7 bits stored in each byte. MSB is set to 1 if more bytes follow.
    """
    if val < 0:
        raise ValueError("Varint values must be non-negative")

    result = bytearray()
    while True:
        byte = val & 0x7F
        val >>= 7
        if val > 0:
            result.append(byte | 0x80)  # Set MSB continuation bit
        else:
            result.append(byte)
            break
    return bytes(result)


def decode_varint(data: bytes) -> Tuple[int, int]:
    """
    Decodes variable-byte sequence into (integer_value, bytes_consumed).
    """
    result = 0
    shift = 0
    for idx, byte in enumerate(data):
        result |= (byte & 0x7F) << shift
        if not (byte & 0x80):  # MSB is 0, end of varint
            return result, idx + 1
        shift += 7
    raise ValueError("Truncated varint byte stream")


def test_q9_varint_encoding():
    # 1: 0x01 (1 byte)
    v1 = encode_varint(1)
    assert v1 == bytes([1])
    assert decode_varint(v1)[0] == 1

    # 300: 300 = (0x2C | 0x80), 0x02 -> [172, 2]
    v300 = encode_varint(300)
    assert len(v300) == 2
    decoded, consumed = decode_varint(v300)
    assert decoded == 300
    assert consumed == 2
    print("=== Q9: Varint / Variable-Byte Encoding Verified ===")


# ==============================================================================
# Question 10: Architectural Multi-Algorithm Telemetry Compressor
# ==============================================================================
class TelemetryCompressorEngine:
    """
    Production telemetry compression engine selecting optimal compression strategy:
    - Delta Encoding for monotonically increasing timestamps
    - RLE for repetitive categorical states (e.g. OK, OK, OK, WARN)
    - LZW for complex structured log messages
    """
    @classmethod
    def compress_numeric_stream(cls, nums: List[int]) -> Dict[str, Any]:
        """Encodes numeric metric stream using delta encoding."""
        encoded = delta_encode(nums)
        return {
            "strategy": "DELTA",
            "encoded_data": encoded,
            "original_count": len(nums),
        }

    @classmethod
    def decompress_numeric_stream(cls, package: Dict[str, Any]) -> List[int]:
        if package["strategy"] != "DELTA":
            raise ValueError("Unsupported strategy")
        return delta_decode(package["encoded_data"])

    @classmethod
    def compress_string_payload(cls, text: str) -> Dict[str, Any]:
        """Chooses between RLE and LZW based on which yields smaller footprint."""
        rle_cand = rle_compress(text)
        lzw_cand = lzw_compress(text)

        # LZW outputs 2-byte integers; estimate byte sizes
        rle_size = len(rle_cand)
        lzw_size = len(lzw_cand) * 2

        if rle_size <= lzw_size:
            return {"strategy": "RLE", "payload": rle_cand}
        else:
            return {"strategy": "LZW", "payload": lzw_cand}

    @classmethod
    def decompress_string_payload(cls, package: Dict[str, Any]) -> str:
        strategy = package["strategy"]
        if strategy == "RLE":
            return rle_decompress(package["payload"])
        elif strategy == "LZW":
            return lzw_decompress(package["payload"])
        else:
            raise ValueError(f"Unknown strategy {strategy}")


def test_q10_telemetry_compressor_engine():
    # 1. Numeric telemetry stream
    metrics = [1000, 1004, 1009, 1015, 1022]
    num_pkg = TelemetryCompressorEngine.compress_numeric_stream(metrics)
    assert num_pkg["strategy"] == "DELTA"
    assert TelemetryCompressorEngine.decompress_numeric_stream(num_pkg) == metrics

    # 2. String text compression (RLE preferred on highly repeated characters)
    repeat_text = "AAAAABBBBBCCCCCDDDDD"
    str_pkg_rle = TelemetryCompressorEngine.compress_string_payload(repeat_text)
    assert str_pkg_rle["strategy"] == "RLE"
    assert TelemetryCompressorEngine.decompress_string_payload(str_pkg_rle) == repeat_text

    # 3. String text compression (LZW preferred on phrases with repeated substrings)
    lzw_text = "ERROR_TIMEOUT_ON_PORT_80_ERROR_TIMEOUT_ON_PORT_80_ERROR_TIMEOUT"
    str_pkg_lzw = TelemetryCompressorEngine.compress_string_payload(lzw_text)
    assert str_pkg_lzw["strategy"] in ("LZW", "RLE")
    assert TelemetryCompressorEngine.decompress_string_payload(str_pkg_lzw) == lzw_text
    print("=== Q10: Architectural Telemetry Compressor Engine Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_rle()
    test_q2_compress_chars_inplace()
    test_q3_word_rle()
    test_q4_huffman_coding()
    test_q5_lzw_compression()
    test_q6_byte_pair_encoding()
    test_q7_bitmap_compression()
    test_q8_delta_encoding()
    test_q9_varint_encoding()
    test_q10_telemetry_compressor_engine()
    print("\nAll 10 string compression problem-solving questions passed successfully!")
