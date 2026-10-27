"""
Topic 01 - Python Basics & Variables
Practice Question 6 Solution: Aligned Tabular Invoice Generator

Problem Statement:
Parses multi-column inventory records from a raw multiline string and produces an
aligned tabular invoice using string justification methods (ljust, rjust):
1. Input format: "ItemName Quantity UnitPrice".
2. Parse lines, stripping whitespace.
3. Compute line subtotals (Quantity * UnitPrice).
4. Calculate 7.5% sales tax on grand subtotal.
5. Print formatted invoice with headers "ITEM", "QTY", "UNIT PRICE", "TOTAL",
   separators, items, and summary rows (Subtotal, Tax, Final Amount).
"""


def generate_invoice(raw_text: str, tax_rate_pct: float = 7.5) -> str:
    """Parses whitespace-separated inventory lines and builds an aligned invoice."""
    lines = raw_text.strip().splitlines()
    parsed_items = []
    subtotal = 0.0

    for line in lines:
        cleaned = line.strip()
        if not cleaned:
            continue
        parts = cleaned.split()
        if len(parts) != 3:
            continue

        item_name = parts[0]
        qty = int(parts[1])
        unit_price = float(parts[2])
        line_total = qty * unit_price
        subtotal += line_total

        parsed_items.append((item_name, qty, unit_price, line_total))

    tax_amount = round(subtotal * (tax_rate_pct / 100.0), 2)
    grand_total = subtotal + tax_amount

    # Formatting columns:
    # ITEM: 20 chars left-aligned
    # QTY: 5 chars right-aligned
    # UNIT PRICE: 15 chars right-aligned
    # TOTAL: 14 chars right-aligned
    output_lines = []
    header = f"{'ITEM'.ljust(20)}{'QTY'.rjust(5)}{'UNIT PRICE'.rjust(15)}{'TOTAL'.rjust(14)}"
    divider = "-" * len(header)

    output_lines.append(header)
    output_lines.append(divider)

    for name, qty, price, total in parsed_items:
        row = (
            f"{name.ljust(20)}"
            f"{str(qty).rjust(5)}"
            f"{f'${price:,.2f}'.rjust(15)}"
            f"{f'${total:,.2f}'.rjust(14)}"
        )
        output_lines.append(row)

    output_lines.append(divider)
    output_lines.append(f"{'Subtotal:'.ljust(40)}{f'${subtotal:,.2f}'.rjust(14)}")
    output_lines.append(f"{f'Tax ({tax_rate_pct}%):'.ljust(40)}{f'${tax_amount:,.2f}'.rjust(14)}")
    output_lines.append(f"{'Grand Total:'.ljust(40)}{f'${grand_total:,.2f}'.rjust(14)}")

    return "\n".join(output_lines)


def main() -> None:
    raw_stream = """
      Wireless_Mouse    3    25.50  
      USB-C_Cable       5     8.99  
      Mechanical_Keyboard  1  119.00  
    """

    invoice_text = generate_invoice(raw_stream, tax_rate_pct=7.5)
    print(invoice_text)


if __name__ == "__main__":
    main()
