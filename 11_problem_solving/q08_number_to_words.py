"""
Topic: Problem Solving - Number to Words
----------------------------------------
Questions Covered:
1. Sub-Thousand Number Converter: Units (0-19), tens (20-90), and hundreds chunks.
2. Standard Western Scale Translation: Billions, Millions, Thousands for numbers up to 10^12.
3. Financial Check Cents Formatter: Standard banking format ("X Dollars and Y/100 Cents").
4. Indian Numbering Scale (Lakhs & Crores): Grouping 3, then 2-digit intervals (Lakh, Crore).
5. Ordinal Word Formatter: Generating positional ranking words ("First", "Twenty-First", etc.).
6. Roman Numeral Bidirectional Converter: Exact conversion between Roman symbols and integers.
7. Word-to-Number Parser: Reverse translation from natural English phrases back to integers.
8. Decimals and Signed Integers: Handling "Negative" prefixes and arbitrary decimal precision.
9. Verbal Arithmetic Expression Evaluator: Parsing and solving spoken math expressions.
10. Architectural System: Production Bank Check Writing & Anti-Tamper Legal Disbursal Engine.
"""

from typing import List, Tuple, Optional, Any, Dict


# ==============================================================================
# Question 1: Sub-Thousand Number Converter
# ==============================================================================
LESS_THAN_20 = [
    "", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
    "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
    "Seventeen", "Eighteen", "Nineteen"
]
TENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]


def convert_below_thousand(n: int) -> str:
    """Converts a number 0 <= n < 1000 into standard English words."""
    if n == 0:
        return "Zero"

    parts = []
    if n >= 100:
        parts.append(LESS_THAN_20[n // 100] + " Hundred")
        n %= 100

    if n >= 20:
        parts.append(TENS[n // 10])
        if n % 10:
            parts.append(LESS_THAN_20[n % 10])
    elif n > 0:
        parts.append(LESS_THAN_20[n])

    return " ".join(parts)


def test_q1_below_thousand():
    assert convert_below_thousand(0) == "Zero"
    assert convert_below_thousand(5) == "Five"
    assert convert_below_thousand(19) == "Nineteen"
    assert convert_below_thousand(42) == "Forty Two"
    assert convert_below_thousand(105) == "One Hundred Five"
    assert convert_below_thousand(999) == "Nine Hundred Ninety Nine"
    print("=== Q1: Sub-Thousand Number Converter Verified ===")


# ==============================================================================
# Question 2: Standard Western Scale Translation (Up to Trillions)
# ==============================================================================
SCALES = ["", "Thousand", "Million", "Billion", "Trillion"]


def number_to_words_english(num: int) -> str:
    """
    Translates non-negative integer up to 10^15 into English words.
    e.g. 1234567 -> 'One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven'
    """
    if num == 0:
        return "Zero"

    scale_idx = 0
    words = []

    while num > 0:
        chunk = num % 1000
        if chunk != 0:
            chunk_word = convert_below_thousand(chunk)
            scale_name = SCALES[scale_idx]
            if scale_name:
                words.append(chunk_word + " " + scale_name)
            else:
                words.append(chunk_word)
        num //= 1000
        scale_idx += 1

    return " ".join(reversed(words))


def test_q2_western_scale():
    assert number_to_words_english(123) == "One Hundred Twenty Three"
    assert number_to_words_english(12345) == "Twelve Thousand Three Hundred Forty Five"
    assert number_to_words_english(1234567) == "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"
    assert number_to_words_english(1000000) == "One Million"
    assert number_to_words_english(1000000000000) == "One Trillion"
    print("=== Q2: Standard Western Scale Translation Verified ===")


# ==============================================================================
# Question 3: Financial Check & Cents Formatter
# ==============================================================================
def format_currency_words(amount: float, currency_unit: str = "Dollars", subunit: str = "Cents") -> str:
    """
    Formats monetary amount into words:
    e.g. 1250.75 -> 'One Thousand Two Hundred Fifty Dollars and Seventy Five Cents'
    """
    dollars = int(amount)
    cents = int(round((amount - dollars) * 100))

    dollar_words = number_to_words_english(dollars)
    if cents > 0:
        cent_words = convert_below_thousand(cents)
        return f"{dollar_words} {currency_unit} and {cent_words} {subunit}"
    return f"{dollar_words} {currency_unit}"


def test_q3_financial_currency_words():
    res1 = format_currency_words(1250.75)
    assert res1 == "One Thousand Two Hundred Fifty Dollars and Seventy Five Cents"

    res2 = format_currency_words(50.00)
    assert res2 == "Fifty Dollars"
    print("=== Q3: Financial Currency Words Formatter Verified ===")


# ==============================================================================
# Question 4: Indian Numbering Scale (Lakhs & Crores)
# ==============================================================================
def number_to_words_indian(num: int) -> str:
    """
    Translates integer into words using Indian Numbering System:
    Groupings: Hundreds, Thousands, Lakhs (10^5), Crores (10^7).
    e.g. 1,23,45,678 -> 'One Crore Twenty Three Lakh Forty Five Thousand Six Hundred Seventy Eight'
    """
    if num == 0:
        return "Zero"

    crores = num // 10_000_000
    num %= 10_000_000

    lakhs = num // 100_000
    num %= 100_000

    thousands = num // 1000
    num %= 1000

    hundreds_chunk = num

    parts = []
    if crores > 0:
        parts.append(number_to_words_indian(crores) + " Crore")
    if lakhs > 0:
        parts.append(convert_below_thousand(lakhs) + " Lakh")
    if thousands > 0:
        parts.append(convert_below_thousand(thousands) + " Thousand")
    if hundreds_chunk > 0:
        parts.append(convert_below_thousand(hundreds_chunk))

    return " ".join(parts)


def test_q4_indian_scale():
    # 100000 -> 1 Lakh
    assert number_to_words_indian(100_000) == "One Lakh"
    # 12345678 -> 1 Crore 23 Lakh 45 Thousand 6 Hundred 78
    res = number_to_words_indian(12_345_678)
    expected = "One Crore Twenty Three Lakh Forty Five Thousand Six Hundred Seventy Eight"
    assert res == expected
    print("=== Q4: Indian Numbering Scale (Lakhs & Crores) Verified ===")


# ==============================================================================
# Question 5: Ordinal Number Words
# ==============================================================================
ORDINAL_IRREGULAR = {
    "One": "First",
    "Two": "Second",
    "Three": "Third",
    "Five": "Fifth",
    "Eight": "Eighth",
    "Nine": "Ninth",
    "Twelve": "Twelfth",
}


def number_to_ordinal_words(n: int) -> str:
    """
    Converts positive integer into its ordinal word representation:
    1 -> 'First', 21 -> 'Twenty First', 100 -> 'One Hundredth'
    """
    cardinal = number_to_words_english(n)
    words = cardinal.split()
    last_word = words[-1]

    if last_word in ORDINAL_IRREGULAR:
        words[-1] = ORDINAL_IRREGULAR[last_word]
    elif last_word.endswith("y"):
        words[-1] = last_word[:-1] + "ieth"
    else:
        words[-1] = last_word + "th"

    return " ".join(words)


def test_q5_ordinal_words():
    assert number_to_ordinal_words(1) == "First"
    assert number_to_ordinal_words(2) == "Second"
    assert number_to_ordinal_words(3) == "Third"
    assert number_to_ordinal_words(20) == "Twentieth"
    assert number_to_ordinal_words(21) == "Twenty First"
    assert number_to_ordinal_words(100) == "One Hundredth"
    print("=== Q5: Ordinal Number Words Verified ===")


# ==============================================================================
# Question 6: Roman Numerals Bidirectional Conversion
# ==============================================================================
ROMAN_INT_PAIRS = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]


def int_to_roman(num: int) -> str:
    """Converts integer (1 to 3999) to Roman numeral string."""
    if not 0 < num < 4000:
        raise ValueError("num must be between 1 and 3999")
    result = []
    for val, sym in ROMAN_INT_PAIRS:
        while num >= val:
            result.append(sym)
            num -= val
    return "".join(result)


def roman_to_int(roman: str) -> int:
    """Converts Roman numeral string to integer."""
    sym_map = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    prev_val = 0
    for ch in reversed(roman.upper()):
        curr_val = sym_map[ch]
        if curr_val < prev_val:
            total -= curr_val
        else:
            total += curr_val
        prev_val = curr_val
    return total


def test_q6_roman_conversion():
    assert int_to_roman(3) == "III"
    assert int_to_roman(4) == "IV"
    assert int_to_roman(9) == "IX"
    assert int_to_roman(58) == "LVIII"
    assert int_to_roman(1994) == "MCMXCIV"

    assert roman_to_int("III") == 3
    assert roman_to_int("IV") == 4
    assert roman_to_int("IX") == 9
    assert roman_to_int("LVIII") == 58
    assert roman_to_int("MCMXCIV") == 1994
    print("=== Q6: Roman Numerals Bidirectional Conversion Verified ===")


# ==============================================================================
# Question 7: Reverse Word-to-Number Parser
# ==============================================================================
WORD_NUM_MAP = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
    "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40,
    "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
}
WORD_MULTIPLIERS = {
    "hundred": 100, "thousand": 1_000, "million": 1_000_000, "billion": 1_000_000_000,
}


def words_to_number(phrase: str) -> int:
    """Parses verbal English phrase into integer: 'two thousand twenty-six' -> 2026."""
    clean_words = phrase.lower().replace("-", " ").replace(" and ", " ").split()
    total = 0
    current_chunk = 0

    for w in clean_words:
        if w in WORD_NUM_MAP:
            current_chunk += WORD_NUM_MAP[w]
        elif w == "hundred":
            current_chunk *= 100
        elif w in WORD_MULTIPLIERS:
            current_chunk *= WORD_MULTIPLIERS[w]
            total += current_chunk
            current_chunk = 0
        else:
            raise ValueError(f"Unrecognized number word: '{w}'")

    return total + current_chunk


def test_q7_words_to_number():
    assert words_to_number("two thousand twenty six") == 2026
    assert words_to_number("One Million Two Hundred Thirty Four") == 1000234
    assert words_to_number("Forty-Two") == 42
    assert words_to_number("Zero") == 0
    print("=== Q7: Word-to-Number Parser Verified ===")


# ==============================================================================
# Question 8: Decimals and Signed Integers
# ==============================================================================
def number_to_words_complete(num_str: str) -> str:
    """
    Translates arbitrary signed decimal strings into words:
    '-45.08' -> 'Negative Forty Five Point Zero Eight'
    """
    parts = []
    s = num_str.strip()
    if s.startswith("-"):
        parts.append("Negative")
        s = s[1:]

    if "." in s:
        integer_part_str, decimal_part_str = s.split(".", 1)
        int_val = int(integer_part_str) if integer_part_str else 0
        parts.append(number_to_words_english(int_val))
        parts.append("Point")
        # Spell out each digit after decimal
        digit_names = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
        for digit in decimal_part_str:
            parts.append(digit_names[int(digit)])
    else:
        parts.append(number_to_words_english(int(s)))

    return " ".join(parts)


def test_q8_decimals_and_signed():
    assert number_to_words_complete("-45.08") == "Negative Forty Five Point Zero Eight"
    assert number_to_words_complete("100.5") == "One Hundred Point Five"
    print("=== Q8: Decimals and Signed Numbers Verified ===")


# ==============================================================================
# Question 9: Verbal Arithmetic Expression Evaluator
# ==============================================================================
def evaluate_verbal_arithmetic(expr: str) -> int:
    """
    Evaluates spoken arithmetic expressions:
    e.g. 'three plus five times two' -> 3 + (5 * 2) = 13 (honors precedence)
    """
    op_map = {
        "plus": "+",
        "minus": "-",
        "times": "*",
        "divided_by": "/",
    }
    # Normalize 'divided by'
    cleaned = expr.lower().replace("divided by", "divided_by")
    tokens = cleaned.split()

    parsed_tokens: List[str] = []
    current_word_num = []

    for t in tokens:
        if t in op_map:
            if current_word_num:
                parsed_tokens.append(str(words_to_number(" ".join(current_word_num))))
                current_word_num = []
            parsed_tokens.append(op_map[t])
        else:
            current_word_num.append(t)

    if current_word_num:
        parsed_tokens.append(str(words_to_number(" ".join(current_word_num))))

    # Evaluate multiplication and division first
    stack: List[Any] = []
    i = 0
    while i < len(parsed_tokens):
        token = parsed_tokens[i]
        if token in ("*", "/"):
            prev_num = int(stack.pop())
            next_num = int(parsed_tokens[i + 1])
            res = (prev_num * next_num) if token == "*" else (prev_num // next_num)
            stack.append(res)
            i += 2
        else:
            stack.append(token)
            i += 1

    # Evaluate addition and subtraction
    ans = int(stack[0])
    i = 1
    while i < len(stack):
        op = stack[i]
        nxt = int(stack[i + 1])
        ans = (ans + nxt) if op == "+" else (ans - nxt)
        i += 2

    return ans


def test_q9_verbal_arithmetic():
    assert evaluate_verbal_arithmetic("three plus five times two") == 13
    assert evaluate_verbal_arithmetic("twenty divided by four minus two") == 3
    print("=== Q9: Verbal Arithmetic Expression Evaluator Verified ===")


# ==============================================================================
# Question 10: Architectural Bank Check Printing & Legal Disbursal Engine
# ==============================================================================
class BankCheckWriter:
    """
    Production banking check writing engine generating tamper-evident legal currency text:
    - Asterisk padding to prevent unauthorized prefix/suffix handwriting additions
    - Fractional cents formatted as 00/100
    - 'ONLY' terminal suffix
    """
    @classmethod
    def generate_legal_line(cls, amount: float, currency_code: str = "USD", line_length: int = 70) -> str:
        dollars = int(amount)
        cents = int(round((amount - dollars) * 100))

        dollar_words = number_to_words_english(dollars)
        unit = "DOLLARS" if currency_code == "USD" else currency_code

        raw_line = f"**{dollar_words.upper()} {unit} AND {cents:02d}/100 ONLY**"
        # Pad with asterisks to exactly line_length if shorter
        if len(raw_line) < line_length:
            padding = line_length - len(raw_line)
            raw_line = raw_line + ("*" * padding)

        return raw_line


def test_q10_bank_check_writer():
    line = BankCheckWriter.generate_legal_line(1540.25, currency_code="USD", line_length=70)
    assert "**ONE THOUSAND FIVE HUNDRED FORTY DOLLARS AND 25/100 ONLY**" in line
    assert len(line) == 70
    assert line.endswith("*")
    print("=== Q10: Architectural Bank Check Writing Engine Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_below_thousand()
    test_q2_western_scale()
    test_q3_financial_currency_words()
    test_q4_indian_scale()
    test_q5_ordinal_words()
    test_q6_roman_conversion()
    test_q7_words_to_number()
    test_q8_decimals_and_signed()
    test_q9_verbal_arithmetic()
    test_q10_bank_check_writer()
    print("\nAll 10 number to words problem-solving questions passed successfully!")
