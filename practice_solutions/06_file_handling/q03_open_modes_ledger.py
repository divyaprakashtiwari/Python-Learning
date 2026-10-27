"""
Topic 06 - File Handling: Question 3
Problem: Append-Only Transaction Ledger demonstrating File Open Modes ('x', 'a', 'r+', 'w+').
"""

import os


class LedgerManager:
    """Manages transactional ledger operations across diverse file open modes."""

    HEADER_TEMPLATE = "LEDGER_HEADER | TX_COUNT: {tx_count:05d} | STATUS: {status:<12}\n"

    def init_ledger(self, filepath: str) -> bool:
        """Initializes ledger using exclusive creation mode 'x'."""
        try:
            with open(filepath, mode="x", encoding="utf-8") as f:
                header = self.HEADER_TEMPLATE.format(tx_count=0, status="ACTIVE")
                f.write(header)
            print("Ledger initialized successfully with mode 'x'.")
            return True
        except FileExistsError:
            return False

    def append_transaction(self, filepath: str, tx_id: str, sender: str, recipient: str, amount: float) -> None:
        """Appends a new transaction line to the end of the file in append mode 'a'."""
        with open(filepath, mode="a", encoding="utf-8") as f:
            line = f"TX | ID: {tx_id:<8} | FROM: {sender:<12} | TO: {recipient:<12} | AMT: ${amount:>10.2f}\n"
            f.write(line)
        print(f"Appended {tx_id}.")

    def update_ledger_header(self, filepath: str, new_tx_count: int, new_status: str) -> None:
        """Overwrites the exact fixed-width header block in place without truncation using 'r+'."""
        with open(filepath, mode="r+", encoding="utf-8") as f:
            f.seek(0)
            updated_header = self.HEADER_TEMPLATE.format(tx_count=new_tx_count, status=new_status)
            f.write(updated_header)
        print("Header updated in-place via mode 'r+' (offset 0).")


# Verification & Execution
ledger_file = "vault_ledger.txt"
hazard_file = "hazard_test.txt"

try:
    ledger = LedgerManager()

    # 1. Exclusive init ('x')
    ledger.init_ledger(ledger_file)

    # 2. Append transactions ('a')
    ledger.append_transaction(ledger_file, "TX-001", "Alice", "Bob", 250.00)
    ledger.append_transaction(ledger_file, "TX-002", "Charlie", "Diana", 750.50)

    # 3. In-place header update ('r+')
    ledger.update_ledger_header(ledger_file, new_tx_count=2, new_status="VERIFIED")

    # 4. Attempt re-initialization on existing file
    created_again = ledger.init_ledger(ledger_file)
    print(f"Attempting re-initialization on existing file: {created_again} (Safely blocked)")

    print(f'\n# Resulting File Content ("{ledger_file}"):')
    with open(ledger_file, "r", encoding="utf-8") as f:
        print(f.read().strip())

    # 5. Truncation Hazard Demonstration ('w+' mode)
    with open(hazard_file, "w", encoding="utf-8") as f:
        f.write("Important historical data: do not delete!")
    size_before = os.path.getsize(hazard_file)

    # Opening with 'w+' immediately truncates to 0 bytes
    with open(hazard_file, "w+", encoding="utf-8") as f:
        size_after_open = os.path.getsize(hazard_file)

    print(f"\nTruncation Hazard ('w+' mode): Before={size_before} bytes -> Immediately upon open={size_after_open} bytes")

finally:
    for path in (ledger_file, hazard_file):
        if os.path.exists(path):
            os.remove(path)
