"""
Topic 03 - Data Structures: Question 5
Problem: HTTP Request Header Canonicalization using Dictionary operations & views.
"""

raw_headers = {
    "Content-Type": "application/json",
    "AUTHORIZATION": "Bearer token_xyz_123",
    "User-Agent": "MobileClient/2.4",
    "X-Correlation-ID": "corr-98765"
}

defaults = {
    "user-agent": "InternalGateway/1.0",
    "accept": "application/json",
    "cache-control": "no-cache"
}

# 1. Header Key Normalization via Dictionary Comprehension
normalized_headers = {k.lower(): v for k, v in raw_headers.items()}
print("Normalized Headers:")
for k, v in normalized_headers.items():
    print(f"  '{k}': '{v}'")

# 2. Dynamic Dictionary Views
header_keys = normalized_headers.keys()
header_values = normalized_headers.values()

print(f"\nKeys view before mutation: {list(header_keys)}")
# Mutating dictionary
normalized_headers["x-forwarded-for"] = "10.0.0.1"
print(f"Keys view after adding 'x-forwarded-for': {list(header_keys)}")
print(f"Dynamic view confirmed: 'x-forwarded-for' in view -> {'x-forwarded-for' in header_keys}")

# 3. Fast Key Membership Verification (O(1))
mandatory_headers = ["authorization", "content-type", "x-signature"]
print("\nSecurity Headers Present Check:")
for header in mandatory_headers:
    print(f"- {header}: {header in normalized_headers}")

# 4. Dictionary Merging with the Union Operator (|) (Python 3.9+)
# Client headers override defaults
production_headers = defaults | normalized_headers

print("\nMerged Production Headers (Client overrides defaults):")
for k, v in production_headers.items():
    print(f"- {k}: '{v}'")
