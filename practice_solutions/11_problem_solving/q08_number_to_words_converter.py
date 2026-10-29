"""
Question 8: Number-to-Words Converter (International, Indian & Currency)
Topic: Problem Solving & Competitive Programming Patterns

Key Concepts Tested:
- Western / International 3-digit triplet chunking (thousands, millions, billions)
- Indian place-value grouping (hundreds, thousands, lakhs, crores)
- Hyphenated compound tens and irregular teen number mapping
- Dual-unit currency formatting with singular/plural inflection
- Arbitrary scale handling up to 10^15 and negative zero edge cases
"""

from typing import List


class NumberToWordsConverter:
    """
    Number-to-words converter supporting Western, Indian, and Currency formatting.
    """

    ONES: List[str] = [
        "", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
        "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
        "seventeen", "eighteen", "nineteen",
    ]

    TENS: List[str] = [
        "", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety",
    ]

    WESTERN_SCALES: List[str] = [
        "", "thousand", "million", "billion", "trillion", "quadrillion",
    ]

    def _convert_chunk_under_thousand(self, n: int) -> str:
        """Converts an integer 0 <= n < 1000 to English words."""
        parts: List[str] = []
        hundreds = n // 100
        remainder = n % 100

        if hundreds > 0:
            parts.append(f"{self.ONES[hundreds]} hundred")

        if remainder > 0:
            if remainder < 20:
                parts.append(self.ONES[remainder])
            else:
                tens_digit = remainder // 10
                ones_digit = remainder % 10
                if ones_digit > 0:
                    parts.append(f"{self.TENS[tens_digit]}-{self.ONES[ones_digit]}")
                else:
                    parts.append(self.TENS[tens_digit])

        return " ".join(parts)

    def to_words_international(self, num: int) -> str:
        """
        Converts an integer into International / Western English representation.
        Chunks in groups of 3 digits (10^3, 10^6, 10^9, etc.).
        """
        if num == 0:
            return "zero"

        is_negative = num < 0
        n = abs(num)
        chunks: List[str] = []
        scale_idx = 0

        while n > 0:
            chunk = n % 1000
            if chunk > 0:
                words = self._convert_chunk_under_thousand(chunk)
                scale_name = self.WESTERN_SCALES[scale_idx]
                chunks.append(f"{words} {scale_name}".strip())
            n //= 1000
            scale_idx += 1

        result = " ".join(reversed(chunks))
        return f"negative {result}" if is_negative else result

    def to_words_indian(self, num: int) -> str:
        """
        Converts an integer according to the Indian place value system:
        First 3 digits (hundreds), followed by 2-digit groups (thousands, lakhs, crores).
        """
        if num == 0:
            return "zero"

        is_negative = num < 0
        n = abs(num)

        # 1. Hundreds group (up to 3 digits)
        hundreds_part = n % 1000
        n //= 1000

        # 2. Thousands group (up to 2 digits)
        thousands_part = n % 100
        n //= 100

        # 3. Lakhs group (up to 2 digits)
        lakhs_part = n % 100
        n //= 100

        # 4. Crores group (remaining digits)
        crores_part = n

        parts: List[str] = []

        if crores_part > 0:
            # Crores can recursively have its own scale
            crores_words = self.to_words_indian(crores_part)
            parts.append(f"{crores_words} crore")

        if lakhs_part > 0:
            parts.append(f"{self._convert_chunk_under_thousand(lakhs_part)} lakh")

        if thousands_part > 0:
            parts.append(f"{self._convert_chunk_under_thousand(thousands_part)} thousand")

        if hundreds_part > 0:
            parts.append(self._convert_chunk_under_thousand(hundreds_part))

        result = " ".join(parts)
        return f"negative {result}" if is_negative else result

    def to_currency(self, amount: float, currency_unit: str = "dollar", subunit: str = "cent") -> str:
        """
        Converts decimal amounts into currency words with singular/plural handling.
        """
        is_negative = amount < 0
        total_cents = round(abs(amount) * 100)
        units = total_cents // 100
        cents = total_cents % 100

        unit_str = currency_unit if units == 1 else f"{currency_unit}s"
        units_words = self.to_words_international(units)

        if cents > 0:
            subunit_str = subunit if cents == 1 else f"{subunit}s"
            cents_words = self.to_words_international(cents)
            res = f"{units_words} {unit_str} and {cents_words} {subunit_str}"
        else:
            res = f"{units_words} {unit_str}"

        return f"negative {res}" if is_negative else res


if __name__ == "__main__":
    converter = NumberToWordsConverter()

    print("=== 1. Western / International Numbering ===")
    w1 = converter.to_words_international(1234567)
    w2 = converter.to_words_international(1000005)
    w3 = converter.to_words_international(-42)
    print(f"International (1234567): '{w1}'")
    print(f"International (1000005): '{w2}'")
    print(f"International (-42): '{w3}'")

    print("\n=== 2. Indian Numbering System ===")
    ind1 = converter.to_words_indian(12345678)
    print(f"Indian (12345678): '{ind1}'")

    print("\n=== 3. Currency Formatting ===")
    curr1 = converter.to_currency(1050.25, currency_unit="dollar", subunit="cent")
    curr2 = converter.to_currency(1.01, currency_unit="dollar", subunit="cent")
    print(f"Currency (1050.25): '{curr1}'")
    print(f"Currency (1.01): '{curr2}'")

    print("\n=== 4. Edge Cases ===")
    print(f"Zero: '{converter.to_words_international(0)}'")
    print(f"Zero currency: '{converter.to_currency(0.0)}'")
    print(f"Trillion scale: '{converter.to_words_international(1000000000000)}'")
