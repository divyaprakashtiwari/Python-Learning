"""
Topic 06: File Handling - Question 08: File Iteration and Large Files

A comprehensive collection of 10 standalone, runnable exercises exploring
memory-efficient iteration over massive files, generator streaming pipelines,
external sorting, backwards seeking, resumable checkpoints, and log monitors.

Questions Covered:
 1. Lazy Line Iteration vs readlines(): Demonstrating O(1) vs O(N) memory allocation.
 2. Custom Chunk Reader Generator: Reading arbitrary byte/char blocks using iter(callable, sentinel).
 3. Memory Profiling with tracemalloc: Verifying bounded memory usage on large file streams.
 4. Composable Generator Pipelines: Chaining streaming filters and transformations.
 5. Safe Reading with Max Line Length: Preventing Out-Of-Memory crashes from unclosed runaway lines.
 6. Memory-Efficient 'tail -n' (Reverse Reader): Seeking backwards from EOF in chunks.
 7. External Merge Sort: Sorting gigabyte-scale datasets that exceed RAM limits using heapq.merge.
 8. Byte-Offset Chunk Partitioning: Splitting large files by byte ranges with line boundary realignment.
 9. Resumable File Processor: State checkpointing with byte offsets to resume interrupted batch jobs.
10. Advanced Project: Real-Time Rolling Window Log Stream Anomaly Detector.
"""

import collections
import heapq
import os
import shutil
import tempfile
import tracemalloc
from typing import Any, Generator, Iterator


# ==============================================================================
# Question 1: Lazy Line Iteration vs readlines()
# ==============================================================================
def exercise_q1_lazy_line_iteration() -> None:
    """
    Contrast lazy generator iteration (`for line in f`) which buffers only one
    line at a time, against `f.readlines()` which forces the entire file into a Python list.
    """
    print("=== Q1: Lazy Line Iteration vs readlines() ===")

    temp_dir = tempfile.mkdtemp(prefix="large_iter_")
    test_path = os.path.join(temp_dir, "lines.txt")

    try:
        # Write 1000 lines
        with open(test_path, "w", encoding="utf-8") as f:
            for i in range(1000):
                f.write(f"Record #{i:04d} - Payload data string\n")

        # 1. readlines() loads all into memory
        with open(test_path, "r", encoding="utf-8") as f:
            all_lines = f.readlines()
            assert len(all_lines) == 1000

        # 2. Lazy iteration maintains O(1) buffer
        line_count = 0
        with open(test_path, "r", encoding="utf-8") as f:
            for line in f:
                line_count += 1
                if line_count == 500:
                    assert "Record #0499" in line

        assert line_count == 1000
        print(f"  readlines() loaded {len(all_lines)} items into memory list.")
        print(f"  Lazy iteration processed {line_count} lines streamingly.")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 2: Chunk Reader Generator (iter with Sentinel)
# ==============================================================================
def chunk_reader(file_obj: Any, chunk_size: int = 1024) -> Iterator[str]:
    """
    Idiomatic Python generator using iter(callable, sentinel) to stream
    chunks until empty string EOF sentinel is returned.
    """
    return iter(lambda: file_obj.read(chunk_size), "")


def exercise_q2_chunk_reader() -> None:
    """
    Demonstrate chunk-based reading for binary or non-newline-delimited payloads.
    """
    print("\n=== Q2: Chunk Reader Generator ===")

    temp_dir = tempfile.mkdtemp(prefix="large_chunk_")
    path = os.path.join(temp_dir, "blob.txt")

    try:
        content = "ABCDEFGHIJ" * 10  # 100 chars
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        chunks_read = []
        with open(path, "r", encoding="utf-8") as f:
            for chunk in chunk_reader(f, chunk_size=15):
                chunks_read.append(chunk)

        # 100 chars / 15 chars per chunk = 6 full chunks of 15 + 1 remainder of 10 = 7 chunks
        assert len(chunks_read) == 7
        assert len(chunks_read[-1]) == 10
        assert "".join(chunks_read) == content

        print(f"  Streamed 100 characters in {len(chunks_read)} discrete chunks.")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 3: Memory Profiling with tracemalloc
# ==============================================================================
def exercise_q3_memory_profiling() -> None:
    """
    Profile heap memory usage during stream processing of 10,000 synthetic records
    using the standard library `tracemalloc` module.
    """
    print("\n=== Q3: Memory Profiling with tracemalloc ===")

    temp_dir = tempfile.mkdtemp(prefix="large_profile_")
    data_path = os.path.join(temp_dir, "large_dataset.txt")

    try:
        # Create 10,000 lines
        with open(data_path, "w", encoding="utf-8") as f:
            for i in range(10000):
                f.write(f"User:{i:06d},Status:Active,Score:{i % 100}\n")

        tracemalloc.start()
        snapshot_start = tracemalloc.take_snapshot()

        total_score = 0
        processed_count = 0

        # Stream lines one by one
        with open(data_path, "r", encoding="utf-8") as f:
            for line in f:
                score = int(line.strip().split("Score:")[1])
                total_score += score
                processed_count += 1

        snapshot_end = tracemalloc.take_snapshot()
        stats = snapshot_end.compare_to(snapshot_start, "lineno")
        tracemalloc.stop()

        # The peak memory delta during lazy iteration is negligible (a few kilobytes)
        memory_delta_bytes = sum(stat.size_diff for stat in stats)

        assert processed_count == 10000
        assert total_score > 0
        print(f"  Processed {processed_count} lines.")
        print(f"  Memory delta during streaming: {memory_delta_bytes} bytes (O(1) memory footprint).")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 4: Composable Generator Pipelines
# ==============================================================================
def exercise_q4_generator_pipelines() -> None:
    """
    Build a multi-stage data processing pipeline by chaining generator expressions
    together (Input Stream -> Line Stripper -> Filter -> Extractor -> Accumulator).
    """
    print("\n=== Q4: Composable Generator Pipelines ===")

    raw_logs = [
        "2026-10-18 10:00:01 INFO Server starting\n",
        "2026-10-18 10:00:02 ERROR DB connection timeout\n",
        "2026-10-18 10:00:03 INFO Worker 1 connected\n",
        "2026-10-18 10:00:04 ERROR Socket buffer overflow\n",
        "2026-10-18 10:00:05 WARNING Low memory\n",
    ]

    # Generator Pipeline stages:
    # 1. Stripper
    stripped_gen = (line.strip() for line in raw_logs)
    # 2. Filter (Errors only)
    error_gen = (line for line in stripped_gen if " ERROR " in line)
    # 3. Message extractor
    msg_gen = (line.split(" ERROR ")[1] for line in error_gen)

    # Consumer (Evaluation occurs lazily)
    errors_list = list(msg_gen)

    assert len(errors_list) == 2
    assert errors_list[0] == "DB connection timeout"
    assert errors_list[1] == "Socket buffer overflow"

    print(f"  Extracted {len(errors_list)} errors via chained generator pipeline:")
    for err in errors_list:
        print(f"    - {err}")


# ==============================================================================
# Question 5: Safe Reading with Max Line Length Safeguard
# ==============================================================================
def safe_readline(file_obj: Any, max_chars: int = 1000) -> str:
    """
    Read up to max_chars characters. If line exceeds max_chars without a newline,
    raise ValueError to prevent runaway allocation or memory exhaustion.
    """
    chunk = file_obj.readline(max_chars)
    if len(chunk) == max_chars and not chunk.endswith("\n"):
        raise ValueError(f"Line exceeded maximum allowable length ({max_chars} chars)!")
    return chunk


def exercise_q5_safe_line_reading() -> None:
    """
    Test safeguard against corrupt or malicious files containing endless lines.
    """
    print("\n=== Q5: Safe Reading with Max Line Length Safeguard ===")

    temp_dir = tempfile.mkdtemp(prefix="large_safe_")
    normal_file = os.path.join(temp_dir, "normal.txt")
    runaway_file = os.path.join(temp_dir, "runaway.txt")

    try:
        # 1. Normal file
        with open(normal_file, "w", encoding="utf-8") as f:
            f.write("Short line 1\nShort line 2\n")

        with open(normal_file, "r", encoding="utf-8") as f:
            line1 = safe_readline(f, max_chars=50)
            assert line1 == "Short line 1\n"

        # 2. Runaway file with 1000 chars and NO newline
        with open(runaway_file, "w", encoding="utf-8") as f:
            f.write("A" * 1000)

        with open(runaway_file, "r", encoding="utf-8") as f:
            try:
                safe_readline(f, max_chars=100)
                assert False, "Should have raised ValueError"
            except ValueError as exc:
                assert "exceeded maximum allowable length" in str(exc)

        print("  Normal line read cleanly within limits.")
        print("  Runaway line properly intercepted and blocked.")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 6: Memory-Efficient 'tail -n' (Reverse Reader)
# ==============================================================================
def read_last_n_lines(filepath: str, n: int, chunk_size: int = 512) -> list[str]:
    """
    Reads the last `n` lines of a file by seeking backwards from EOF in chunks,
    without reading earlier portions of the file.
    """
    lines: list[str] = []
    with open(filepath, "rb") as f:
        f.seek(0, os.SEEK_END)
        file_size = f.tell()
        remaining_bytes = file_size
        buffer = b""

        while remaining_bytes > 0 and len(lines) <= n:
            read_size = min(chunk_size, remaining_bytes)
            remaining_bytes -= read_size
            f.seek(remaining_bytes, os.SEEK_SET)
            chunk = f.read(read_size)
            buffer = chunk + buffer
            lines = buffer.splitlines()

    # Decode and return last n lines
    decoded = [line.decode("utf-8") for line in lines[-n:]]
    return decoded


def exercise_q6_reverse_tail_reader() -> None:
    """
    Demonstrate seeking backwards from EOF to tail the last 3 lines.
    """
    print("\n=== Q6: Memory-Efficient 'tail -n' (Reverse Reader) ===")

    temp_dir = tempfile.mkdtemp(prefix="large_tail_")
    test_path = os.path.join(temp_dir, "activity.log")

    try:
        with open(test_path, "w", encoding="utf-8") as f:
            for i in range(1, 201):
                f.write(f"Log event #{i:03d}\n")

        last_3 = read_last_n_lines(test_path, n=3)
        assert len(last_3) == 3
        assert last_3 == ["Log event #198", "Log event #199", "Log event #200"]

        print(f"  Tailed last 3 lines from end of file: {last_3}")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 7: External Merge Sort for Massive Files
# ==============================================================================
def external_merge_sort(input_path: str, output_path: str, chunk_lines: int = 100) -> None:
    """
    Sorts a large file by breaking it into sorted temporary file chunks,
    then merging them using heapq.merge into the final output.
    """
    temp_dir = tempfile.mkdtemp(prefix="ext_sort_")
    chunk_files: list[str] = []

    try:
        # Phase 1: Split & Sort chunks
        with open(input_path, "r", encoding="utf-8") as f:
            chunk_num = 0
            while True:
                lines = []
                for _ in range(chunk_lines):
                    line = f.readline()
                    if not line:
                        break
                    lines.append(int(line.strip()))

                if not lines:
                    break

                lines.sort()
                chunk_file = os.path.join(temp_dir, f"chunk_{chunk_num}.txt")
                with open(chunk_file, "w", encoding="utf-8") as cf:
                    for num in lines:
                        cf.write(f"{num}\n")
                chunk_files.append(chunk_file)
                chunk_num += 1

        # Phase 2: K-Way Merge using heapq.merge
        open_handles = [open(cf, "r", encoding="utf-8") for cf in chunk_files]
        try:
            # Generator per handle yielding ints
            generators = ((int(line.strip()) for line in handle) for handle in open_handles)
            merged = heapq.merge(*generators)

            with open(output_path, "w", encoding="utf-8") as out:
                for num in merged:
                    out.write(f"{num}\n")
        finally:
            for h in open_handles:
                h.close()

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def exercise_q7_external_merge_sort() -> None:
    """
    Demonstrate external sorting on a shuffled sequence.
    """
    print("\n=== Q7: External Merge Sort ===")

    temp_dir = tempfile.mkdtemp(prefix="large_sort_")
    raw_file = os.path.join(temp_dir, "unsorted.txt")
    sorted_file = os.path.join(temp_dir, "sorted.txt")

    try:
        # Write unsorted numbers: 300 numbers across 3 chunks of 100
        numbers = list(range(300, 0, -1))
        with open(raw_file, "w", encoding="utf-8") as f:
            for n in numbers:
                f.write(f"{n}\n")

        external_merge_sort(raw_file, sorted_file, chunk_lines=100)

        # Verify sorted file
        with open(sorted_file, "r", encoding="utf-8") as f:
            sorted_res = [int(line.strip()) for line in f]

        assert sorted_res == list(range(1, 301))
        print(f"  Successfully sorted {len(sorted_res)} integers using external merge sort.")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 8: Byte-Offset Chunk Partitioning
# ==============================================================================
def partition_file_by_bytes(filepath: str, num_chunks: int) -> list[tuple[int, int]]:
    """
    Divides a file into approximately equal byte segments, realigning segment
    boundaries to the next newline character to avoid splitting lines across workers.
    """
    file_size = os.path.getsize(filepath)
    if file_size == 0:
        return []

    target_chunk_size = file_size // num_chunks
    ranges: list[tuple[int, int]] = []
    start = 0

    with open(filepath, "rb") as f:
        for _ in range(num_chunks - 1):
            target_end = start + target_chunk_size
            if target_end >= file_size:
                break
            f.seek(target_end, os.SEEK_SET)
            # Advance to the end of the current line
            f.readline()
            end = f.tell()
            ranges.append((start, end))
            start = end

        # Final chunk takes remainder to EOF
        if start < file_size:
            ranges.append((start, file_size))

    return ranges


def exercise_q8_byte_offset_partitioning() -> None:
    """
    Demonstrate computing clean line-aligned byte boundaries for parallel workers.
    """
    print("\n=== Q8: Byte-Offset Chunk Partitioning ===")

    temp_dir = tempfile.mkdtemp(prefix="large_part_")
    test_path = os.path.join(temp_dir, "partition_test.txt")

    try:
        with open(test_path, "w", encoding="utf-8") as f:
            for i in range(50):
                f.write(f"Line {i:02d}: payload payload payload\n")

        ranges = partition_file_by_bytes(test_path, num_chunks=3)
        assert len(ranges) == 3

        # Verify each segment begins and ends cleanly at line boundaries
        with open(test_path, "rb") as f:
            for start, end in ranges:
                f.seek(start)
                data = f.read(end - start)
                assert data.endswith(b"\n")

        print(f"  Computed {len(ranges)} line-aligned byte ranges: {ranges}")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 9: Resumable File Processor with State Checkpoints
# ==============================================================================
class ResumableFileProcessor:
    """
    Processes a file and persists the byte offset after every batch.
    If terminated and restarted, resumes seamlessly from the saved checkpoint.
    """

    def __init__(self, data_file: str, checkpoint_file: str) -> None:
        self.data_file = data_file
        self.checkpoint_file = checkpoint_file

    def get_offset(self) -> int:
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    return int(content)
        return 0

    def save_offset(self, offset: int) -> None:
        with open(self.checkpoint_file, "w", encoding="utf-8") as f:
            f.write(str(offset))

    def process_records(self, max_records: int | None = None) -> list[str]:
        offset = self.get_offset()
        processed: list[str] = []

        with open(self.data_file, "r", encoding="utf-8") as f:
            f.seek(offset)
            while True:
                if max_records is not None and len(processed) >= max_records:
                    break
                line = f.readline()
                if not line:
                    break
                processed.append(line.strip())
                self.save_offset(f.tell())

        return processed


def exercise_q9_resumable_processor() -> None:
    """
    Simulate processing half a dataset, stopping, and resuming from checkpoint.
    """
    print("\n=== Q9: Resumable File Processor with State Checkpoints ===")

    temp_dir = tempfile.mkdtemp(prefix="large_resume_")
    data_file = os.path.join(temp_dir, "jobs.txt")
    ckpt_file = os.path.join(temp_dir, "checkpoint.state")

    try:
        # Create 10 jobs
        with open(data_file, "w", encoding="utf-8") as f:
            for i in range(1, 11):
                f.write(f"JOB_{i}\n")

        processor = ResumableFileProcessor(data_file, ckpt_file)

        # Batch 1: Process 4 jobs then stop
        batch1 = processor.process_records(max_records=4)
        assert batch1 == ["JOB_1", "JOB_2", "JOB_3", "JOB_4"]
        checkpoint1 = processor.get_offset()
        assert checkpoint1 > 0

        # Batch 2: Resume! Should automatically continue with JOB_5
        batch2 = processor.process_records()
        assert batch2 == ["JOB_5", "JOB_6", "JOB_7", "JOB_8", "JOB_9", "JOB_10"]

        # Batch 3: Nothing left to process at EOF
        batch3 = processor.process_records()
        assert batch3 == []

        print(f"  Batch 1 processed: {batch1}")
        print(f"  Resumed Batch 2 processed: {batch2}")
        print(f"  Final state cleanly verified at EOF.")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# ==============================================================================
# Question 10: Advanced Project - Rolling Window Log Anomaly Detector
# ==============================================================================
class LogAnomalyDetector:
    """
    Monitors a streaming log file using a fixed-capacity deque rolling window,
    detecting frequency anomalies (e.g. spike of 500 errors within 10 lines).
    """

    def __init__(self, window_size: int = 10, error_threshold: int = 3) -> None:
        self.window_size = window_size
        self.error_threshold = error_threshold
        self.window: collections.deque[bool] = collections.deque(maxlen=window_size)
        self.anomalies_detected: list[int] = []

    def ingest_line(self, line_num: int, line_content: str) -> bool:
        is_error = "500 Internal Server Error" in line_content
        self.window.append(is_error)

        error_count = sum(self.window)
        if error_count >= self.error_threshold:
            self.anomalies_detected.append(line_num)
            return True
        return False


def exercise_q10_rolling_window_anomaly_detector() -> None:
    """
    Demonstrate real-time stream monitoring for error spikes.
    """
    print("\n=== Q10: Rolling Window Log Anomaly Detector ===")

    detector = LogAnomalyDetector(window_size=5, error_threshold=3)

    log_stream = [
        "200 OK",
        "200 OK",
        "500 Internal Server Error",
        "200 OK",
        "500 Internal Server Error",
        "500 Internal Server Error",  # Anomaly triggered here! (3 errors in last 4 lines)
        "200 OK",
        "200 OK",
        "200 OK",
        "200 OK",                     # Error cleared from sliding window
    ]

    for idx, log in enumerate(log_stream, start=1):
        alert = detector.ingest_line(idx, log)
        if idx == 6:
            assert alert is True
        elif idx >= 10:
            assert alert is False

    # Line 6 triggers anomaly (errors at lines 3, 5, 6).
    # Line 7 also has 3 errors in window (lines 3, 5, 6 still in last 5 lines).
    # Line 8 pushes line 3 out, dropping error count to 2, clearing anomaly.
    assert detector.anomalies_detected == [6, 7]
    print(f"  Anomalies detected at line indices: {detector.anomalies_detected}")
    print("  Sliding window naturally cleared anomaly after error subsided.")


# ==============================================================================
# Main Runner
# ==============================================================================
if __name__ == "__main__":
    exercise_q1_lazy_line_iteration()
    exercise_q2_chunk_reader()
    exercise_q3_memory_profiling()
    exercise_q4_generator_pipelines()
    exercise_q5_safe_line_reading()
    exercise_q6_reverse_tail_reader()
    exercise_q7_external_merge_sort()
    exercise_q8_byte_offset_partitioning()
    exercise_q9_resumable_processor()
    exercise_q10_rolling_window_anomaly_detector()

    print("\nAll 10 large file iteration questions executed and asserted successfully!")
