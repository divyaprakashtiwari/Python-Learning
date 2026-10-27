"""
Topic 06 - File Handling: Question 7
Problem: Binary Asset Inspector, PNG struct Header Parsing, and Stream XOR Cipher.
"""

import os
import struct
from typing import Any, Dict


class BinaryAssetInspector:
    """Inspects binary magic headers, parses struct dimensions, and performs XOR streaming."""

    SIGNATURES = {
        b"\x89PNG\r\n\x1a\n": "PNG",
        b"\xff\xd8\xff": "JPEG",
        b"GIF87a": "GIF",
        b"GIF89a": "GIF",
        b"%PDF-": "PDF"
    }

    def identify_file_type(self, filepath: str) -> str:
        """Identifies file type via initial magic bytes in binary read mode ('rb')."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        with open(filepath, mode="rb") as f:
            header = f.read(8)

        for sig, file_type in self.SIGNATURES.items():
            if header.startswith(sig):
                return file_type
        return "UNKNOWN"

    def parse_png_dimensions(self, filepath: str) -> Dict[str, Any]:
        """Extracts big-endian 32-bit pixel dimensions from PNG IHDR chunk using struct.unpack."""
        file_type = self.identify_file_type(filepath)
        if file_type != "PNG":
            raise ValueError(f"File is not a PNG (detected '{file_type}')")

        with open(filepath, mode="rb") as f:
            f.seek(16)
            dimension_bytes = f.read(8)
            if len(dimension_bytes) < 8:
                raise ValueError("Incomplete PNG IHDR chunk")

            width, height = struct.unpack(">II", dimension_bytes)

        file_size = os.path.getsize(filepath)
        return {
            "format": "PNG",
            "width": width,
            "height": height,
            "size_bytes": file_size
        }

    def xor_cipher_file(self, source_path: str, output_path: str, key_byte: int) -> int:
        """Streams binary data in chunks, applying XOR cipher idempotently."""
        if not (0 <= key_byte <= 255):
            raise ValueError("Key must be a single byte (0-255)")

        total_bytes = 0
        chunk_size = 4096

        with open(source_path, mode="rb") as src, open(output_path, mode="wb") as dst:
            while True:
                chunk = src.read(chunk_size)
                if not chunk:
                    break
                ciphered_chunk = bytes(b ^ key_byte for b in chunk)
                dst.write(ciphered_chunk)
                total_bytes += len(chunk)

        return total_bytes


# Verification & Execution
sample_png = "sample.png"
encrypted_png = "sample.png.enc"
restored_png = "sample_restored.png"

# Synthetic 24-byte PNG stub
png_stub = (
    b"\x89PNG\r\n\x1a\n"
    b"\x00\x00\x00\x0d"
    b"IHDR"
    b"\x00\x00\x03\x20"  # 800 width (big-endian)
    b"\x00\x00\x02\x58"  # 600 height (big-endian)
)

try:
    with open(sample_png, "wb") as f:
        f.write(png_stub)

    inspector = BinaryAssetInspector()
    file_type = inspector.identify_file_type(sample_png)
    print(f"Detected File Type: {file_type}")

    meta = inspector.parse_png_dimensions(sample_png)
    print("PNG Metadata:")
    print(f"- Width: {meta['width']} px")
    print(f"- Height: {meta['height']} px")
    print(f"- Size: {meta['size_bytes']} bytes")

    key = 0xAA
    bytes_enc = inspector.xor_cipher_file(sample_png, encrypted_png, key_byte=key)
    print(f"Obfuscation: Processed {bytes_enc} bytes with key 0x{key:02X}.")

    bytes_dec = inspector.xor_cipher_file(encrypted_png, restored_png, key_byte=key)
    print(f"Decryption: Processed {bytes_dec} bytes with key 0x{key:02X}.")

    with open(sample_png, "rb") as f1, open(restored_png, "rb") as f2:
        is_identical = f1.read() == f2.read()
    print(f"Binary Identity Verification (Original == Restored): {is_identical}")

finally:
    for path in (sample_png, encrypted_png, restored_png):
        if os.path.exists(path):
            os.remove(path)
