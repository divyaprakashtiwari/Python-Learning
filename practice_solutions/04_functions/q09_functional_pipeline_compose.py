"""
Topic 04 - Functions: Question 9
Problem: Functional stream transformation, functools (partial, reduce), and compose().
"""

import functools
import re
from typing import Any, Callable, Dict, List, Tuple


# 1. Functional Stream Processing
def convert_currency(txn: Dict[str, Any], rate: float = 0.92) -> Dict[str, Any]:
    """Converts a transaction's USD amount to EUR using the supplied rate."""
    return {
        "id": txn["id"],
        "amount_eur": round(txn["amount_usd"] * rate, 2)
    }


transactions = [
    {"id": 101, "status": "SETTLED", "amount_usd": 250.00, "country": "US"},
    {"id": 102, "status": "PENDING", "amount_usd": 500.00, "country": "CA"},
    {"id": 103, "status": "SETTLED", "amount_usd": 75.00,  "country": "US"},
    {"id": 104, "status": "SETTLED", "amount_usd": 1200.00, "country": "UK"},
    {"id": 105, "status": "FAILED",  "amount_usd": 300.00, "country": "DE"}
]

# Lazy filter: status == SETTLED and amount_usd >= 100.0
settled_txns = filter(lambda t: t["status"] == "SETTLED" and t["amount_usd"] >= 100.0, transactions)

# Lazy map using functools.partial
convert_to_eur = functools.partial(convert_currency, rate=0.92)
eur_txns = list(map(convert_to_eur, settled_txns))

print("Filtered & Converted Transactions (EUR):")
for t in eur_txns:
    print(f"- Txn {t['id']}: {t['amount_eur']:,.2f} EUR")

# functools.reduce to compute total volume and max single txn in one pass
total_eur, max_eur = functools.reduce(
    lambda acc, t: (acc[0] + t["amount_eur"], max(acc[1], t["amount_eur"])),
    eur_txns,
    (0.0, 0.0)
)
print(f"Reduced Summary: Total EUR = {total_eur:,.2f} EUR, Max Single Txn = {max_eur:,.2f} EUR")


# 2. Generic Higher-Order Function Composer: (f o g)(x) = f(g(x))
def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Composes multiple functions from right to left: compose(f, g, h)(x) = f(g(h(x)))."""
    return functools.reduce(
        lambda f, g: lambda x: f(g(x)),
        functions,
        lambda x: x
    )


# Text pipeline functions
def strip_whitespace(text: str) -> str:
    return text.strip()


def lowercase(text: str) -> str:
    return text.lower()


def remove_punctuation(text: str) -> str:
    return re.sub(r"[^\w\s]", " ", text)


def word_tokenize(text: str) -> List[str]:
    return text.split()


# Assemble pipeline: rightmost runs first (strip -> lower -> remove_punct -> tokenize)
clean_text_pipeline = compose(
    word_tokenize,
    remove_punctuation,
    lowercase,
    strip_whitespace
)

raw_text = "  Hello, Functional Python WORLD! -- 2026.  "
tokens = clean_text_pipeline(raw_text)

print("\nComposed Text Pipeline Result:")
print(tokens)
