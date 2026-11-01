"""
Topic 08: Conditional Statements (if, elif, else)
Example 03: Ternary Conditional Expression and Structural Pattern Matching (`match-case`)

Demonstrates:
1. One-line ternary expressions (`x if condition else y`)
2. Python 3.10+ `match ... case` statement for HTTP status & command routing
"""


def describe_http_response(status_code: int) -> str:
    """Classify an HTTP status code using Python 3.10+ match-case."""
    match status_code:
        case 200 | 201:
            return "Success: Request completed"
        case 301 | 302:
            return "Redirection: Resource moved"
        case 400:
            return "Client Error: Bad request syntax"
        case 401 | 403:
            return "Security Error: Unauthorized or Forbidden"
        case 404:
            return "Client Error: Resource not found"
        case code if 500 <= code < 600:
            return f"Server Error ({code}): Internal service failure"
        case _:
            return f"Unknown HTTP status code: {status_code}"


def main() -> None:
    # 1. Ternary Conditional Expression
    print("=== 1. Ternary Conditional Expression ===")
    for cart_total in [350, 750]:
        shipping_fee = 0 if cart_total >= 500 else 49
        print(f"Cart: Rs.{cart_total} -> Shipping Fee: Rs.{shipping_fee}")

    # 2. Structural Pattern Matching (match-case)
    print("\n=== 2. Structural Pattern Matching (match-case) ===")
    for code in [200, 301, 403, 404, 503, 999]:
        print(f"HTTP {code} -> {describe_http_response(code)}")


if __name__ == "__main__":
    main()
