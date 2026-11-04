"""
Phase 5 - Topic 02: File Handling
Example 03: Binary File I/O (`rb`/`wb`), Pointer Seeking (`seek`/`tell`), & `pathlib.Path` Helpers

Demonstrates:
  - Writing and inspecting binary headers with `mode='wb'` and `mode='rb'`
  - Navigating byte offsets with `fh.seek()` and `fh.tell()`
  - Concise one-shot file reads/writes using `Path.write_text()` and `Path.read_text()`
"""

from pathlib import Path
import struct
import tempfile


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        bin_path = Path(tmp_dir) / "sample_image.png"

        print("=== 1. Writing Binary Header + Width/Height (`mode='wb'`) ===")
        # Fake minimal PNG header: 8-byte signature + 4-byte length + b'IHDR' + width(1920) + height(1080)
        ihdr_payload = struct.pack(">II", 1920, 1080)
        with open(bin_path, mode="wb") as fh:
            fh.write(PNG_SIGNATURE)
            fh.write(struct.pack(">I", 8))
            fh.write(b"IHDR")
            fh.write(ihdr_payload)

        print("=== 2. Inspecting Binary Offsets with `seek()` and `tell()` (`mode='rb'`) ===")
        with open(bin_path, mode="rb") as fh:
            sig = fh.read(8)
            print(f"  Is valid PNG signature? {sig == PNG_SIGNATURE} (cursor at byte {fh.tell()})")
            # Jump over 4-byte chunk length + 4-byte 'IHDR' tag (8 bytes relative to current position)
            fh.seek(8, 1)
            print(f"  Cursor after relative seek(8, 1): byte {fh.tell()}")
            width, height = struct.unpack(">II", fh.read(8))
            print(f"  Unpacked Dimensions: {width}x{height} (cursor at byte {fh.tell()})")

        print("\n=== 3. Modern `pathlib.Path` One-Liners (`write_text` / `read_text`) ===")
        note_path = Path(tmp_dir) / "quick_note.txt"
        chars_written = note_path.write_text("Pathlib closes the file automatically!", encoding="utf-8")
        print(f"  Wrote {chars_written} characters -> Read back: {note_path.read_text(encoding='utf-8')!r}")


if __name__ == "__main__":
    main()
