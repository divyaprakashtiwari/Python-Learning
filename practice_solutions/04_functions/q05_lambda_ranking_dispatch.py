"""
Topic 04 - Functions: Question 5
Problem: Multi-Criteria Ranking, Extremum Selection, and Dispatcher using Lambdas.
"""

# 1. Given list of financial asset dictionaries
assets = [
    {"ticker": "AAPL", "sector": "Technology", "market_cap_b": 3400.0, "pe_ratio": 33.2, "div_yield": 0.55},
    {"ticker": "JNJ",  "sector": "Healthcare", "market_cap_b": 380.0,  "pe_ratio": 24.1, "div_yield": 3.10},
    {"ticker": "MSFT", "sector": "Technology", "market_cap_b": 3100.0, "pe_ratio": 35.8, "div_yield": 0.72},
    {"ticker": "PFE",  "sector": "Healthcare", "market_cap_b": 160.0,  "pe_ratio": 15.4, "div_yield": 5.80}
]

# Multi-criteria sorting: Sector ASC, Market Cap DESC (-market_cap_b)
sorted_assets = sorted(assets, key=lambda x: (x["sector"], -x["market_cap_b"]))

print("Sorted Assets (Sector ASC, Market Cap DESC):")
for idx, a in enumerate(sorted_assets, 1):
    print(f"{idx}. {a['sector']}: {a['ticker']} (${a['market_cap_b']:.1f}B)")

# 2. Extremum Extraction via min() and max() with lambdas
highest_div = max(assets, key=lambda x: x["div_yield"])
lowest_pe = min(assets, key=lambda x: x["pe_ratio"])

print(f"\nHighest Dividend Yield: {highest_div['ticker']} ({highest_div['div_yield']:.2f}%)")
print(f"Lowest P/E Valuation: {lowest_pe['ticker']} ({lowest_pe['pe_ratio']:.1f})")

# 3. Anonymous Fee Calculator Dispatcher
fee_dispatch = {
    "BUY": lambda p: max(1.00, p * 0.001),
    "SELL": lambda p: p * 0.0015 + 0.50,
    "TRANSFER": lambda p: 2.50
}

principal = 10000.0
print(f"\nTransaction Fees for ${principal:,.2f} Trade:")
for tx_type, calc in fee_dispatch.items():
    fee = calc(principal)
    print(f"- {tx_type} Fee: ${fee:.2f}")
