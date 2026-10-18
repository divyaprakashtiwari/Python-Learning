"""
Topic 06: File Handling - Question 07: Binary Files

A comprehensive collection of 10 standalone, runnable exercises exploring
low-level binary I/O, `bytes` and `bytearray` manipulation, the `struct` module,
endianness, memoryview zero-copy slicing, and binary record serialization.

Questions Covered:
 1. Bytes vs Bytearray: Immutability, slicing, byte values (0-255), and hex conversions.
 2. Basic Binary I/O: Opening with 'rb' and 'wb', reading fixed-width chunks, and byte streams.
 3. The struct Module: Packing and unpacking integers, floats, and strings with format codes.
 4. Endianness Control: Little-Endian (<), Big-Endian (>), and Network Byte Order (!).
 5. Magic Numbers & Binary Header Detection: Inspecting PNG, WAV, and custom file signatures.
 6. Precise Binary Seeking: SEEK_SET, SEEK_CUR, and SEEK_END navigation in binary streams.
 7. Bitwise Operations & Flag Masks: Storing and extracting bitmask attributes in a single byte.
 8. High-Performance Zero-Copy with memoryview: Mutating underlying buffer slices in-place.
 9. Byte Order & Numeric Conversions: int.to_bytes and int.from_bytes with signed/unsigned flags.
10. Advanced Project: Fixed-Width Binary Record Indexer with file-based binary search.
"""

import os
import shutil
import struct
import sys
import tempfile
from typing import Any


# ==============================================================================
# Question 1: Bytes vs Bytearray Fundamentals
# ==============================================================================
def exercise_q1_bytes_vs_bytearray() -> None:
    """
    Demonstrate immutable bytes vs mutable bytearray, index inspection, and hex conversion.
    """
    print("=== Q1: Bytes vs Bytearray Fundamentals ===")

    # Immutable bytes
    immutable_b = b"Python \x00\x01\xff"
    assert isinstance(immutable_b, bytes)
    assert immutable_b[0] == 80  # ASCII 'P'
    assert immutable_b[-1] == 255  # 0xff

    try:
        # Immutable bytes cannot be modified in place
        immutable_b[0] = 65  # type: ignore
        assert False, "Should raise TypeError"
    except TypeError:
        pass

    # Mutable bytearray
    mutable_ba = bytearray(b"Hello World")
    mutable_ba[0] = ord("J")  # Change 'H' to 'J'
    mutable_ba.extend(b"!")
    assert mutable_ba.decode("ascii") == "Jello World!"

    # Hex conversions
    hex_str = "deadbeef"
    converted_bytes = bytes.fromhex(hex_str)
    assert converted_bytes == b"\xde\xad\xbe\xef"
    assert converted_bytes.hex() == "deadbeef"

    print(f"  Immutable bytes length: {len(immutable_b)}, last byte: {hex(immutable_b[-1])}")
    print(f"  Modified bytearray: {mutable_ba.decode('ascii')}")
    print(f"  Hex roundtrip: {converted_bytes.hex()}")


# ==============================================================================
# Question 2: Basic Binary I/O ('rb' and 'wb')
# ==============================================================================
def exercise_q2_basic_binary_io() -> None:
    """
    Write and read raw byte sequences to a file, verifying fixed-size chunk reading.
    """
    print("\n=== Q2: Basic Binary I/O ===")

    temp_dir = tempfile.mkdtemp(prefix="bin_io_")
    bin_path = os.path.join(temp_dir, "raw_data.bin")

    try:
        raw_payload = bytes(range(100))  # 0x00 to 0x63
        with open(bin_path, "wb") as f:
            f.write(raw_payload)

        # Read back in 16-byte chunks
        chunks = []
        with open(bin_path, "rb") as f:
            while chunk := f.read(16):
                chunks.append(chunk)

        assert len(chunks) == 7  # 6 full chunks of 16 + 1 remainder of 4
        assert len(chunks[-1]) == 4
        assert b"".join(chunks) == raw_payload

        print(f"  Successfully wrote and chunk-read {len(raw_payload)} raw bytes.")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 3: The struct Module (Packing & Unpacking)
# ==============================================================================
def exercise_q3_struct_packing_unpacking() -> None:
    """
    Demonstrate packing multiple primitive types (int, float, string) into a
    compact binary representation and unpacking them back to Python objects.
    """
    print("\n=== Q3: The struct Module ===")

    # Format string:
    # I = unsigned 32-bit int (4 bytes)
    # f = 32-bit float (4 bytes)
    # 8s = 8-byte char string (padded)
    fmt = "=If8s"
    expected_size = struct.calcsize(fmt)  # 4 + 4 + 8 = 16 bytes
    assert expected_size == 16

    record_id = 42001
    score = 98.5
    tag = b"ALPHA\x00\x00\x00"

    packed_data = struct.pack(fmt, record_id, score, tag)
    assert len(packed_data) == 16

    # Unpack
    unpacked_id, unpacked_score, unpacked_tag = struct.unpack(fmt, packed_data)

    assert unpacked_id == record_id
    assert round(unpacked_score, 1) == 98.5
    assert unpacked_tag.rstrip(b"\x00") == b"ALPHA"

    print(f"  Struct format '{fmt}' packed size: {expected_size} bytes")
    print(f"  Packed bytes (hex): {packed_data.hex()}")
    print(f"  Unpacked values: ID={unpacked_id}, Score={round(unpacked_score, 1)}, Tag={unpacked_tag}")


# ==============================================================================
# Question 4: Endianness (Little-Endian vs Big-Endian)
# ==============================================================================
def exercise_q4_endianness() -> None:
    """
    Demonstrate the difference between Little-Endian (<) and Big-Endian (> / !)
    byte ordering when packing multi-byte integers.
    """
    print("\n=== Q4: Endianness ===")

    # 32-bit number 0x12345678
    val = 0x12345678

    little_endian = struct.pack("<I", val)
    big_endian = struct.pack(">I", val)

    # In Little-Endian, the least significant byte comes first: \x78 \x56 \x34 \x12
    assert little_endian == b"\x78\x56\x34\x12"

    # In Big-Endian, the most significant byte comes first: \x12 \x34 \x56 \x78
    assert big_endian == b"\x12\x34\x56\x78"

    # System host byteorder
    host_order = sys.byteorder
    native_packed = struct.pack("=I", val)
    if host_order == "little":
        assert native_packed == little_endian
    else:
        assert native_packed == big_endian

    print(f"  Host byteorder: {host_order}")
    print(f"  Little-Endian:  {little_endian.hex()}")
    print(f"  Big-Endian:     {big_endian.hex()}")


# ==============================================================================
# Question 5: Magic Numbers & Binary Header Detection
# ==============================================================================
def exercise_q5_magic_numbers() -> None:
    """
    Identify file formats by inspecting their initial signature/magic bytes.
    """
    print("\n=== Q5: Magic Numbers & Binary Header Detection ===")

    signatures = {
        b"\x89PNG\r\n\x1a\n": "image/png",
        b"GIF89a": "image/gif",
        b"GIF87a": "image/gif",
        b"%PDF-": "application/pdf",
        b"\xff\xd8\xff": "image/jpeg",
        b"PK\x03\x04": "application/zip",
    }

    def detect_mime_type(binary_stream: bytes) -> str:
        for magic, mime in signatures.items():
            if binary_stream.startswith(magic):
                return mime
        return "application/octet-stream"

    png_header = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
    zip_header = b"PK\x03\x04\x14\x00\x00\x00"
    unknown = b"\x01\x02\x03\x04"

    assert detect_mime_type(png_header) == "image/png"
    assert detect_mime_type(zip_header) == "application/zip"
    assert detect_mime_type(unknown) == "application/octet-stream"

    print("  Detected PNG mime type:", detect_mime_type(png_header))
    print("  Detected ZIP mime type:", detect_mime_type(zip_header))
    print("  Detected fallback mime type:", detect_mime_type(unknown))


# ==============================================================================
# Question 6: Precise Binary Seeking (SEEK_SET, SEEK_CUR, SEEK_END)
# ==============================================================================
def exercise_q6_binary_seeking() -> None:
    """
    Navigate forwards, backwards, and relative to end of file using os.SEEK_*.
    """
    print("\n=== Q6: Precise Binary Seeking ===")

    temp_dir = tempfile.mkdtemp(prefix="bin_seek_")
    test_file = os.path.join(temp_dir, "seek_test.bin")

    try:
        # Write 26 bytes representing ASCII letters A-Z
        with open(test_file, "wb") as f:
            f.write(bytes(range(ord("A"), ord("Z") + 1)))

        with open(test_file, "rb") as f:
            # 1. SEEK_SET: Absolute offset from beginning
            f.seek(5, os.SEEK_SET)
            assert f.read(1) == b"F"  # 6th letter (index 5)

            # 2. SEEK_CUR: Relative offset from current cursor (which is at index 6)
            f.seek(4, os.SEEK_CUR)  # moves to index 10
            assert f.read(1) == b"K"  # 11th letter (index 10)

            # 3. SEEK_END: Relative offset from end of file (must be negative or zero)
            f.seek(-3, os.SEEK_END)  # 3 bytes from end: 'X', 'Y', 'Z'
            tail = f.read(3)
            assert tail == b"XYZ"

        print("  SEEK_SET, SEEK_CUR, and SEEK_END navigated to exact byte offsets.")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 7: Bitwise Operations & Flag Masks
# ==============================================================================
def exercise_q7_bitwise_flags() -> None:
    """
    Pack and unpack multiple boolean flags and permission states into a single byte
    using bitwise operators (&, |, ^, ~).
    """
    print("\n=== Q7: Bitwise Operations & Flag Masks ===")

    # 1 byte = 8 bits: [B7, B6, B5, B4, B3, B2, B1, B0]
    FLAG_READ = 1 << 0       # 0b00000001 = 1
    FLAG_WRITE = 1 << 1      # 0b00000010 = 2
    FLAG_EXECUTE = 1 << 2    # 0b00000100 = 4
    FLAG_HIDDEN = 1 << 3     # 0b00001000 = 8
    FLAG_SYSTEM = 1 << 4     # 0b00010000 = 16

    # Combine flags with bitwise OR (|)
    attributes = FLAG_READ | FLAG_WRITE | FLAG_SYSTEM
    assert attributes == 1 + 2 + 16  # 19

    # Query flag presence with bitwise AND (&)
    has_read = bool(attributes & FLAG_READ)
    has_write = bool(attributes & FLAG_WRITE)
    has_exec = bool(attributes & FLAG_EXECUTE)

    assert has_read is True
    assert has_write is True
    assert has_exec is False

    # Toggle flag with bitwise XOR (^)
    toggled = attributes ^ FLAG_HIDDEN
    assert bool(toggled & FLAG_HIDDEN) is True
    toggled = toggled ^ FLAG_HIDDEN
    assert bool(toggled & FLAG_HIDDEN) is False

    # Clear a flag using bitwise AND with inverted mask (& ~FLAG)
    cleared_write = attributes & ~FLAG_WRITE
    assert bool(cleared_write & FLAG_WRITE) is False
    assert bool(cleared_write & FLAG_READ) is True

    print(f"  Combined flag byte: bin={bin(attributes)}, int={attributes}")
    print(f"  Flag checks: Read={has_read}, Write={has_write}, Exec={has_exec}")


# ==============================================================================
# Question 8: High-Performance Zero-Copy with memoryview
# ==============================================================================
def exercise_q8_memoryview_zero_copy() -> None:
    """
    Demonstrate zero-copy slicing and in-place buffer modification using memoryview.
    """
    print("\n=== Q8: High-Performance Zero-Copy with memoryview ===")

    buffer = bytearray(b"HEADER____PAYLOAD____FOOTER")
    mv = memoryview(buffer)

    # Slice does NOT copy bytes into a new object! It references the same underlying memory.
    header_slice = mv[0:6]
    assert header_slice.tobytes() == b"HEADER"

    # Modify the payload in-place directly through a memoryview slice
    payload_slice = mv[10:17]
    assert payload_slice.tobytes() == b"PAYLOAD"
    payload_slice[:] = b"UPDATED"

    # The underlying bytearray reflects the modification immediately!
    assert buffer[10:17] == b"UPDATED"
    assert buffer == bytearray(b"HEADER____UPDATED____FOOTER")

    print(f"  Direct in-place memoryview modification: {buffer.decode('ascii')}")


# ==============================================================================
# Question 9: Byte Order & Numeric Conversions (to_bytes / from_bytes)
# ==============================================================================
def exercise_q9_numeric_byte_conversions() -> None:
    """
    Demonstrate int.to_bytes and int.from_bytes with signed integers and endianness.
    """
    print("\n=== Q9: Byte Order & Numeric Conversions ===")

    # Positive integer to 4 bytes big endian
    positive_num = 1000000
    b_pos = positive_num.to_bytes(4, byteorder="big", signed=False)
    assert len(b_pos) == 4
    assert int.from_bytes(b_pos, byteorder="big", signed=False) == positive_num

    # Negative integer (two's complement)
    negative_num = -4500
    b_neg = negative_num.to_bytes(2, byteorder="little", signed=True)
    assert len(b_neg) == 2
    decoded_neg = int.from_bytes(b_neg, byteorder="little", signed=True)
    assert decoded_neg == negative_num

    # Overflows raise OverflowError
    try:
        (1000).to_bytes(1, byteorder="big", signed=False)
        assert False, "Should raise OverflowError"
    except OverflowError:
        pass

    print(f"  Positive int {positive_num} -> {b_pos.hex()}")
    print(f"  Negative int {negative_num} -> {b_neg.hex()} -> decoded back {decoded_neg}")


# ==============================================================================
# Question 10: Advanced Project - Fixed-Width Binary Record Indexer
# ==============================================================================
class FixedBinaryStorage:
    """
    High-performance on-disk binary database table. Stores fixed-size records
    sorted by integer key, enabling O(log N) binary search directly against
    the disk file without loading all records into memory.

    Record Format (24 bytes):
      - ID (4 bytes, unsigned int, big-endian)
      - Value (8 bytes, double float, big-endian)
      - Label (12 bytes, ASCII string, null-padded)
    """

    MAGIC = b"BINDB01\x00"  # 8 bytes header magic
    RECORD_FORMAT = ">Id12s"
    RECORD_SIZE = struct.calcsize(RECORD_FORMAT)  # 4 + 8 + 12 = 24 bytes

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self._init_file()

    def _init_file(self) -> None:
        if not os.path.exists(self.filepath):
            with open(self.filepath, "wb") as f:
                # Header: 8 bytes MAGIC + 4 bytes record count
                f.write(self.MAGIC + struct.pack(">I", 0))

    def count(self) -> int:
        with open(self.filepath, "rb") as f:
            f.seek(8, os.SEEK_SET)
            (cnt,) = struct.unpack(">I", f.read(4))
            return cnt

    def write_records(self, records: list[tuple[int, float, str]]) -> None:
        # Sort by ID
        sorted_records = sorted(records, key=lambda r: r[0])
        with open(self.filepath, "wb") as f:
            f.write(self.MAGIC + struct.pack(">I", len(sorted_records)))
            for rec_id, val, label in sorted_records:
                padded_label = label.encode("ascii")[:12].ljust(12, b"\x00")
                f.write(struct.pack(self.RECORD_FORMAT, rec_id, val, padded_label))

    def find_by_id(self, target_id: int) -> dict[str, Any] | None:
        """Binary search directly over disk blocks."""
        with open(self.filepath, "rb") as f:
            # Verify magic
            magic = f.read(8)
            if magic != self.MAGIC:
                raise ValueError("Corrupt database file header!")

            (total,) = struct.unpack(">I", f.read(4))
            low = 0
            high = total - 1

            while low <= high:
                mid = (low + high) // 2
                offset = 12 + (mid * self.RECORD_SIZE)
                f.seek(offset, os.SEEK_SET)
                chunk = f.read(self.RECORD_SIZE)
                rec_id, val, raw_label = struct.unpack(self.RECORD_FORMAT, chunk)

                if rec_id == target_id:
                    clean_label = raw_label.rstrip(b"\x00").decode("ascii")
                    return {"id": rec_id, "value": val, "label": clean_label}
                elif rec_id < target_id:
                    low = mid + 1
                else:
                    high = mid - 1

        return None


def exercise_q10_fixed_binary_indexer() -> None:
    """
    Demonstrate disk-based binary search over fixed-size binary records.
    """
    print("\n=== Q10: Fixed-Width Binary Record Indexer ===")

    temp_dir = tempfile.mkdtemp(prefix="bin_db_")
    db_file = os.path.join(temp_dir, "records.bdb")

    try:
        storage = FixedBinaryStorage(db_file)
        sample_records = [
            (105, 54.2, "SENSOR_A"),
            (101, 12.0, "SENSOR_B"),
            (250, 99.8, "SENSOR_C"),
            (177, 42.1, "SENSOR_D"),
            (310, 88.0, "SENSOR_E"),
        ]
        storage.write_records(sample_records)

        assert storage.count() == 5

        # Binary search lookup
        found = storage.find_by_id(177)
        assert found is not None
        assert found["id"] == 177
        assert round(found["value"], 1) == 42.1
        assert found["label"] == "SENSOR_D"

        missing = storage.find_by_id(999)
        assert missing is None

        print(f"  Stored {storage.count()} binary records.")
        print(f"  Disk-based binary search found record 177: {found}")
        print(f"  Missing record query cleanly returned: {missing}")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_bytes_vs_bytearray()
    exercise_q2_basic_binary_io()
    exercise_q3_struct_packing_unpacking()
    exercise_q4_endianness()
    exercise_q5_magic_numbers()
    exercise_q6_binary_seeking()
    exercise_q7_bitwise_flags()
    exercise_q8_memoryview_zero_copy()
    exercise_q9_numeric_byte_conversions()
    exercise_q10_fixed_binary_indexer()

    print("\nAll 10 binary files questions executed and asserted successfully!")
