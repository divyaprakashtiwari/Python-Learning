"""
Topic 01 - Python Basics & Variables
Practice Question 4 Solution: String Slicing, Indexing, and Data Masking

Problem Statement:
1. Extract local part and domain from email string.
2. Mask the local part: keep first and last char visible, replace intermediate chars
   with '*' of identical length. If length <= 2, retain first char followed by '*'.
3. Given transaction ID "TXN-YYYYMMDD-SERIAL", extract year, month, day, and serial.
4. Reverse the serial number using negative stride slicing [::-1].
"""


def mask_email(email: str) -> dict[str, str]:
    """Splits email into local and domain parts, masking the local part."""
    if "@" not in email or email.count("@") != 1:
        raise ValueError("Invalid email: must contain exactly one '@' delimiter.")

    local_part, domain = email.split("@")
    if not local_part or not domain:
        raise ValueError("Invalid email: local part and domain must be non-empty.")

    # Masking rule
    if len(local_part) <= 2:
        masked_local = local_part[0] + "*"
    else:
        # First char + middle asterisks + last char
        num_stars = len(local_part) - 2
        masked_local = local_part[0] + ("*" * num_stars) + local_part[-1]

    masked_email = f"{masked_local}@{domain}"

    return {
        "local_part": local_part,
        "domain": domain,
        "masked_email": masked_email,
    }


def parse_transaction_id(txn_id: str) -> dict[str, str]:
    """Parses TXN-YYYYMMDD-SERIAL using slice notation."""
    parts = txn_id.split("-")
    if len(parts) != 3 or parts[0] != "TXN" or len(parts[1]) != 8:
        raise ValueError("Invalid transaction format; expected 'TXN-YYYYMMDD-SERIAL'")

    date_str = parts[1]
    year = date_str[0:4]
    month = date_str[4:6]
    day = date_str[6:8]
    serial = parts[2]
    reversed_serial = serial[::-1]

    return {
        "txn_id": txn_id,
        "year": year,
        "month": month,
        "day": day,
        "serial": serial,
        "reversed_serial": reversed_serial,
    }


def main() -> None:
    sample_email = "alexander.dev@example.org"
    sample_txn = "TXN-20261022-987654"

    email_res = mask_email(sample_email)
    txn_res = parse_transaction_id(sample_txn)

    print("Parsed Email Components:")
    print(f"- Local Part: '{email_res['local_part']}'")
    print(f"- Domain: '{email_res['domain']}'")
    print(f"- Masked Email: '{email_res['masked_email']}'")

    print(f"Parsed Transaction ID (\"{sample_txn}\"):")
    print(f"- Year: '{txn_res['year']}'")
    print(f"- Month: '{txn_res['month']}'")
    print(f"- Day: '{txn_res['day']}'")
    print(f"- Serial: '{txn_res['serial']}'")
    print(f"- Reversed Serial: '{txn_res['reversed_serial']}'")


if __name__ == "__main__":
    main()
