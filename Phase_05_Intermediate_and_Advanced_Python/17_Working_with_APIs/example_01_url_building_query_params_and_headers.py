"""
Phase 5 - Topic 17: Working with APIs
Example 01: URL Construction, Query Parameter Encoding (`urlencode`), & Custom Request Headers

Demonstrates:
  - Safely building URLs and encoding special characters in query parameters using
    `urllib.parse.urlencode()` and `urllib.parse.urlunparse()`
  - Constructing a `urllib.request.Request` object with custom HTTP headers (`Authorization`, `User-Agent`)
"""

from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request


def build_search_request(base_url: str, query: str, page: int, api_token: str) -> Request:
    """Construct an HTTP GET Request with URL-encoded query parameters and Bearer auth."""
    params = urlencode({"q": query, "page": page, "limit": 20})
    full_url = f"{base_url.rstrip('/')}?{params}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_token}",
        "User-Agent": "PythonCompleteNotesClient/1.0",
    }
    return Request(full_url, headers=headers, method="GET")


def main() -> None:
    print("=== 1. Safe Query Parameter Encoding (`urllib.parse.urlencode`) ===")
    req = build_search_request(
        "https://api.example.com/v1/articles",
        query="python 3.13 & dsa",
        page=2,
        api_token="tok_live_987",
    )
    print(f"  Method   : {req.get_method()}")
    print(f"  Full URL : {req.full_url}")
    print(f"  Headers  : {dict(req.header_items())}")

    print("\n=== 2. Parsing URL Components Back (`urlparse` & `parse_qs`) ===")
    parsed = urlparse(req.full_url)
    print(f"  Scheme={parsed.scheme!r}, Netloc={parsed.netloc!r}, Path={parsed.path!r}")
    print(f"  Decoded Query Dict: {parse_qs(parsed.query)}")


if __name__ == "__main__":
    main()
