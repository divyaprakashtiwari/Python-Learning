"""
Topic 02 - Control Flow
Practice Question 3 Solution: Time-Series Reductions, Moving Average & Spike Detection

Problem Statement:
Processes a discrete time-series of sensor temperature readings using for loops and range():
1. Manual Reductions: sum, min, max without built-in sum(), min(), max().
2. Moving Window Average (SMA): window size k = 3.
3. Downsampling: step size 2.
4. Backward Spike Detection: iterate backwards using range(len - 1, -1, -1) to locate
   most recent reading exceeding 30.0 C.
"""


def analyze_temperatures(readings: list[float], window_size: int = 3, threshold: float = 30.0) -> dict[str, object]:
    """Analyzes temperature series using manual reductions and range indexing."""
    if not readings:
        raise ValueError("Readings list cannot be empty.")
    if window_size <= 0 or window_size > len(readings):
        raise ValueError("Invalid window size.")

    # 1. Manual Reductions (sum, min, max, avg)
    total_sum = 0.0
    min_val = readings[0]
    max_val = readings[0]

    for val in readings:
        total_sum += val
        if val < min_val:
            min_val = val
        if val > max_val:
            max_val = val

    avg_val = total_sum / len(readings)

    # 2. Moving Window Average (SMA)
    moving_averages = []
    num_windows = len(readings) - window_size + 1

    for i in range(num_windows):
        window_sum = 0.0
        for j in range(i, i + window_size):
            window_sum += readings[j]
        window_mean = round(window_sum / window_size, 2)
        moving_averages.append(window_mean)

    # 3. Downsampling with step size 2
    downsampled = []
    for i in range(0, len(readings), 2):
        downsampled.append(readings[i])

    # 4. Backward Spike Detection
    spike_idx = -1
    spike_val = None

    for i in range(len(readings) - 1, -1, -1):
        if readings[i] > threshold:
            spike_idx = i
            spike_val = readings[i]
            break

    return {
        "sum": total_sum,
        "min": min_val,
        "max": max_val,
        "avg": avg_val,
        "moving_averages": moving_averages,
        "downsampled": downsampled,
        "spike_idx": spike_idx,
        "spike_val": spike_val,
    }


def main() -> None:
    temperatures = [21.5, 23.0, 28.5, 31.2, 29.8, 33.4, 27.1, 24.0]
    k = 3
    thresh = 30.0

    res = analyze_temperatures(temperatures, window_size=k, threshold=thresh)

    print(
        f"Manual Reductions: Sum = {res['sum']:.2f}, Min = {res['min']:.2f}, "
        f"Max = {res['max']:.2f}, Average = {res['avg']:.2f}"
    )
    print(f"3-Point Moving Averages: {res['moving_averages']}")
    print(f"Downsampled (Step 2): {res['downsampled']}")
    if res["spike_idx"] != -1:
        print(f"Most Recent Spike Moving Backwards: Index {res['spike_idx']} with value {res['spike_val']:.2f} C")


if __name__ == "__main__":
    main()
