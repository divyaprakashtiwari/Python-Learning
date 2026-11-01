"""
Topic 06: Input and Output
Example 03: Real-World Tabular Receipt Formatter

Demonstrates left (`<`), center (`^`), and right (`>`) text alignment in f-strings
to render a professional bookstore invoice in the terminal.
"""


def print_bookstore_receipt() -> None:
    cart = [
        ("Fluent Python (2nd Ed)", 1, 1450.00),
        ("Introduction to Algorithms", 1, 1899.50),
        ("Coding Interview Notebook", 3, 120.00),
    ]

    border = "=" * 54
    divider = "-" * 54

    print(border)
    print(f"{'PYTHON LEARNING BOOKSTORE':^54}")
    print(border)
    print(f"{'Item Description':<28} {'Qty':^5} {'Unit':>9} {'Total':>9}")
    print(divider)

    subtotal = 0.0
    for title, qty, unit_price in cart:
        line_total = qty * unit_price
        subtotal += line_total
        print(f"{title:<28} {qty:^5} {unit_price:>9.2f} {line_total:>9.2f}")

    print(divider)
    gst = subtotal * 0.18
    grand_total = subtotal + gst
    print(f"{'Subtotal':<43} {subtotal:>10.2f}")
    print(f"{'GST (18%)':<43} {gst:>10.2f}")
    print(border)
    print(f"{'GRAND TOTAL (INR)':<43} {grand_total:>10.2f}")
    print(border)


if __name__ == "__main__":
    print_bookstore_receipt()
