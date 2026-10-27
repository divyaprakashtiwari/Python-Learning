"""
Question 2: Streaming Telemetry Pipeline & Interactive Coroutine Accumulator
Topic: Advanced Python

Key Concepts Tested:
- Generator functions and lazy stream evaluation
- Subgenerator delegation via 'yield from'
- Bidirectional coroutine communication via .send() and .close()
- Coroutine lifecycle (priming, GeneratorExit handling, closed coroutine behavior)
"""

from typing import Generator, Iterable, List, Dict, Any, Optional


class StreamAnalyticsSuite:
    """
    Streaming telemetry analysis suite demonstrating lazy generators,
    subgenerator delegation with yield from, and interactive coroutines.
    """

    @staticmethod
    def flatten_sensor_batches(nested_data_blocks: List[List[float]]) -> Generator[float, None, None]:
        """
        Lazily flattens nested batches using subgenerator delegation (yield from).
        Emits items one-by-one without pre-allocating an intermediate list.
        """
        for block in nested_data_blocks:
            yield from block

    @staticmethod
    def stream_transformed_telemetry(
        raw_stream: Iterable[float], calibration_offset: float = 1.5
    ) -> Generator[float, None, None]:
        """
        Chains a lazy generator transformation over raw_stream.
        Applies (val + calibration_offset) and filters out any values < 0.0.
        """
        for val in raw_stream:
            calibrated = round(val + calibration_offset, 2)
            if calibrated >= 0.0:
                yield calibrated

    @staticmethod
    def running_stats_coroutine() -> Generator[Optional[Dict[str, Any]], float, None]:
        """
        Interactive coroutine that tracks count, sum, min, max, and mean.
        Requires priming (next() or send(None)) before sending numeric values.
        """
        count = 0
        total = 0.0
        min_v = float("inf")
        max_v = float("-inf")
        response: Optional[Dict[str, Any]] = None

        try:
            while True:
                incoming_val = yield response
                if incoming_val is None:
                    continue
                count += 1
                total += incoming_val
                min_v = min(min_v, incoming_val)
                max_v = max(max_v, incoming_val)
                response = {
                    "count": count,
                    "mean": round(total / count, 2),
                    "min": round(min_v, 2),
                    "max": round(max_v, 2),
                }
        except GeneratorExit:
            pass


if __name__ == "__main__":
    suite = StreamAnalyticsSuite()

    print("=== 1. Subgenerator Delegation (yield from) ===")
    batches = [[10.5, 12.0], [15.2, 18.9, 21.0], [8.4]]
    flat_data = list(suite.flatten_sensor_batches(batches))
    print(f"Flattened Batch Data:\n{flat_data}")

    print("\n=== 2. Lazy Transformation Pipeline ===")
    raw_measurements = [-5.0, -1.0, 0.0, 10.2, 25.4]
    transformed = list(suite.stream_transformed_telemetry(raw_measurements, calibration_offset=1.5))
    print(f"Calibrated and Filtered Stream (offset=+1.5, >=0.0):\n{transformed}")

    print("\n=== 3. Interactive Coroutine Accumulator (.send) ===")
    coro = suite.running_stats_coroutine()
    next(coro)  # Prime the coroutine to advance to the first yield

    stat1 = coro.send(10.0)
    print(f"- Send 10.0 -> {stat1}")

    stat2 = coro.send(20.0)
    print(f"- Send 20.0 -> {stat2}")

    stat3 = coro.send(30.0)
    print(f"- Send 30.0 -> {stat3}")

    coro.close()
    print("Coroutine closed cleanly.")

    print("\n=== 4. Post-Close Behavior & Unprimed Error Check ===")
    # 4a. Sending to closed coroutine
    try:
        coro.send(40.0)
    except StopIteration:
        print("Sending to closed coroutine: Raises StopIteration as expected.")

    # 4b. Sending non-None to unprimed coroutine
    unprimed = suite.running_stats_coroutine()
    try:
        unprimed.send(100.0)
    except TypeError as e:
        print(f"Sending non-None to unprimed generator raised TypeError: {e}")
