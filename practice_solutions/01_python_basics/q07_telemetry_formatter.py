"""
Topic 01 - Python Basics & Variables
Practice Question 7 Solution: Standardized Telemetry Report & Format Specifications

Problem Statement:
Format financial, scientific, and networking metrics into a standardized telemetry
report using Python f-string format specifications:
1. Stock Performance: price with '$' and 2 decimals; change as signed percentage (+4.38%).
2. Scientific Constant: Planck constant in scientific notation (e) with 4 decimals.
3. Network Throughput: megabytes/sec with thousands separator and 2 decimals.
4. Padded Identifier: server ID zero-padded to 6 digits width ("000042").
"""


def format_telemetry(
    server_id: int,
    ticker: str,
    current_price: float,
    price_change_pct: float,
    planck_constant: float,
    transferred_bytes: int,
    elapsed_sec: float,
) -> str:
    """Formats metrics using Python f-string mini-language specifications."""
    # Compute MB/s (1 MB = 1024 * 1024 bytes)
    megabytes_transferred = transferred_bytes / (1024.0**2)
    throughput_mb_s = megabytes_transferred / elapsed_sec

    report_lines = [
        "[TELEMETRY REPORT]",
        f"{'Server ID':<19}: {server_id:06d}",
        f"{'Asset Ticker':<19}: {ticker}",
        f"{'Current Price':<19}: ${current_price:.2f}",
        f"{'Change (24h)':<19}: {price_change_pct:+.2%}",
        f"{'Planck Constant':<19}: {planck_constant:.4e}",
        f"{'Throughput':<19}: {throughput_mb_s:,.2f} MB/s",
    ]

    return "\n".join(report_lines)


def main() -> None:
    s_id = 42
    sym = "NVDA"
    price = 142.876
    change = 0.04382
    planck = 6.62607015e-34
    data_bytes = 14258790400
    sec = 12.45

    output = format_telemetry(s_id, sym, price, change, planck, data_bytes, sec)
    print(output)


if __name__ == "__main__":
    main()
