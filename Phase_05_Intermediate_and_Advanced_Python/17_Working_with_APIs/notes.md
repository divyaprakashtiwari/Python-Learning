# Phase 5 — Topic 17: Working with APIs

## 1. Introduction

**Working with APIs (Application Programming Interfaces)**—specifically HTTP/REST JSON APIs—is how Python applications communicate with payment gateways, cloud providers, LLM endpoints, and microservices.

Python's standard library provides `urllib.request`, `urllib.parse`, and `urllib.error` for zero-dependency HTTP client communication, while the ecosystem builds on the exact same concepts (`requests`, `httpx`, `aiohttp`). Mastering URL query encoding, request headers, timeouts, status-code error handling, cursor pagination, and rate-limit retries (`HTTP 429`) prepares you for real-world backend integration.

---

## 2. Why is it used?

1. **Service-to-Service Integration:** Fetch weather/stock data, trigger webhooks, authenticate via OAuth2 Bearer tokens, or call AI inference endpoints.
2. **Safe URL & Query Encoding (`urllib.parse.urlencode`):** Escapes spaces, `&`, `?`, and Unicode characters in query strings so user input never corrupts URL structure or causes parameter injection.
3. **Resilience Against Network Failures:** Explicit `timeout=` settings, `HTTPError` status handling, and exponential backoff on `429 Too Many Requests` / `503 Service Unavailable` keep services from hanging or dropping data.

---

## 3. Syntax

```python
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

# 1. Encode Query Parameters Safely
query_str = urlencode({"q": "python & dsa", "limit": 10})
url = f"https://api.example.com/search?{query_str}"

# 2. Build Request with Headers & Optional JSON Body
req = Request(
    url,
    headers={"Accept": "application/json", "Authorization": "Bearer <TOKEN>"},
    method="GET",
)

# 3. Execute with Explicit Timeout & Error Handling
try:
    with urlopen(req, timeout=5.0) as resp:
        data = json.loads(resp.read().decode("utf-8"))
except HTTPError as err:
    print(f"HTTP status error: {err.code}")
except URLError as err:
    print(f"Network/DNS error: {err.reason}")
```

---

## 4. Explanation (Step-by-Step)

1. **Core HTTP Methods (REST Semantics):**
   - `GET`: Retrieve a resource (idempotent, read-only, parameters in URL query string).
   - `POST`: Create a new resource or trigger an action (non-idempotent, payload in request body).
   - `PUT` / `PATCH`: Replace (`PUT`, idempotent) or partially update (`PATCH`) an existing resource.
   - `DELETE`: Remove a resource (idempotent).
2. **Key HTTP Status Code Ranges:**
   - `2xx` (`200 OK`, `201 Created`, `204 No Content`): Success.
   - `4xx` (`400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `429 Too Many Requests`): Client error. Do **not** blindly retry `400`/`401`/`404`—only retry `429` after respecting `Retry-After`!
   - `5xx` (`500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable`, `504 Gateway Timeout`): Server error (safe to retry idempotent requests with exponential backoff + jitter).
3. **Why Always Specify `timeout=`:**
   - Without `timeout=...`, `urlopen()` (and `requests.get()`) waits **forever** if a remote server accepts the TCP connection and never sends a response byte—gradually freezing all worker threads in your application!
4. **Cursor Pagination vs Offset Pagination:**
   - **Offset (`?page=5&limit=20`):** Can skip or duplicate items if new rows are inserted while paging.
   - **Cursor (`?cursor=eyJpZCI6MTAwfQ==`):** Uses an opaque bookmark pointing to the last seen item (`next_cursor`), guaranteeing stable $O(1)$ indexed pagination.

---

## 5. Minimum 3 Examples

### Example 01: URL Construction, Query Parameter Encoding (`urlencode`), & Custom Request Headers
File: [`example_01_url_building_query_params_and_headers.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/17_Working_with_APIs/example_01_url_building_query_params_and_headers.py)

```python
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
```

### Example 02: End-to-End REST JSON Client (`GET` & `POST`) Against a Local HTTP Server
File: [`example_02_rest_api_client_with_local_http_server.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/17_Working_with_APIs/example_02_rest_api_client_with_local_http_server.py)

```python
"""
Phase 5 - Topic 17: Working with APIs
Example 02: End-to-End REST JSON Client (`GET` & `POST`) Against a Local HTTP Server

Demonstrates:
  - Spinning up a real local `HTTPServer` in a background daemon thread (100% offline-safe!)
  - Sending `GET` and `POST` JSON requests using `urllib.request.urlopen()` with timeouts
  - Catching `urllib.error.HTTPError` on `404 Not Found` status codes
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading
from urllib.error import HTTPError
from urllib.request import Request, urlopen


class MiniTodoAPIHandler(BaseHTTPRequestHandler):
    todos: list[dict[str, object]] = [{"id": 1, "task": "Master Phase 5"}]

    def log_message(self, format: str, *args: object) -> None:
        pass  # Silence default stderr access logs for clean console output

    def _send_json(self, status: int, payload: object) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/api/todos":
            self._send_json(200, {"items": self.todos})
        else:
            self._send_json(404, {"error": "Endpoint not found"})

    def do_POST(self) -> None:
        if self.path == "/api/todos":
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length).decode("utf-8"))
            new_item = {"id": len(self.todos) + 1, "task": data["task"]}
            self.todos.append(new_item)
            self._send_json(201, new_item)


def main() -> None:
    server = HTTPServer(("127.0.0.1", 0), MiniTodoAPIHandler)
    port = server.server_port
    base_url = f"http://127.0.0.1:{port}"
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        print("=== 1. POST `/api/todos` (Create Resource -> HTTP 201) ===")
        post_body = json.dumps({"task": "Start Phase 6 DSA"}).encode("utf-8")
        post_req = Request(
            f"{base_url}/api/todos",
            data=post_body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(post_req, timeout=5.0) as resp:
            created = json.loads(resp.read().decode("utf-8"))
            print(f"  Status: {resp.status} | Created: {created}")

        print("\n=== 2. GET `/api/todos` (List Resources -> HTTP 200) ===")
        with urlopen(f"{base_url}/api/todos", timeout=5.0) as resp:
            listing = json.loads(resp.read().decode("utf-8"))
            print(f"  Status: {resp.status} | Todos: {listing['items']}")

        print("\n=== 3. Handling `HTTPError` on Unknown Route (`/api/unknown` -> HTTP 404) ===")
        try:
            urlopen(f"{base_url}/api/unknown", timeout=5.0)
        except HTTPError as err:
            err_payload = json.loads(err.read().decode("utf-8"))
            print(f"  Caught HTTPError {err.code}: {err_payload}")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
```

### Example 03: Cursor Pagination, Rate-Limit Handling (`HTTP 429`), & Exponential Backoff
File: [`example_03_pagination_rate_limits_and_backoff.py`](file:///c:/Users/ACER/OneDrive/Desktop/Python%20Learning/Phase_05_Intermediate_and_Advanced_Python/17_Working_with_APIs/example_03_pagination_rate_limits_and_backoff.py)

```python
"""
Phase 5 - Topic 17: Working with APIs
Example 03: Cursor Pagination, Rate-Limit Handling (`HTTP 429`), & Exponential Backoff

Demonstrates:
  - Consuming a paginated API (`next_cursor`) using a lazy generator function
  - Handling transient `HTTP 429 Too Many Requests` responses with retry/backoff logic
"""

from typing import Iterator


class SimulatedPaginatedAPI:
    """In-memory simulation of a cursor-paginated API that rate-limits once."""

    def __init__(self) -> None:
        self._pages = {
            "cursor_1": {"items": ["user_1", "user_2"], "next_cursor": "cursor_2"},
            "cursor_2": {"items": ["user_3", "user_4"], "next_cursor": "cursor_3"},
            "cursor_3": {"items": ["user_5"], "next_cursor": None},
        }
        self._failed_once = False

    def fetch_page(self, cursor: str) -> dict[str, object]:
        if cursor == "cursor_2" and not self._failed_once:
            self._failed_once = True
            raise RuntimeError("HTTP 429 Too Many Requests (Retry-After: 0.01s)")
        return self._pages[cursor]


def iterate_all_users(api: SimulatedPaginatedAPI, max_retries: int = 3) -> Iterator[str]:
    """Lazily yield all users across all pages, automatically retrying HTTP 429 errors."""
    cursor: str | None = "cursor_1"
    while cursor is not None:
        for attempt in range(1, max_retries + 1):
            try:
                page = api.fetch_page(cursor)
                break
            except RuntimeError as err:
                print(f"  [backoff] {err} -> retrying {cursor!r} (attempt {attempt}/{max_retries})")
                if attempt == max_retries:
                    raise
        for user in page["items"]:  # type: ignore[attr-defined]
            yield str(user)
        cursor = page["next_cursor"]  # type: ignore[assignment]


def main() -> None:
    print("=== Streaming Cursor-Paginated API with Automatic 429 Retry ===")
    api = SimulatedPaginatedAPI()
    all_users = list(iterate_all_users(api))
    print(f"  Collected all users across 3 pages: {all_users}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 01
```text
=== 1. Safe Query Parameter Encoding (`urllib.parse.urlencode`) ===
  Method   : GET
  Full URL : https://api.example.com/v1/articles?q=python+3.13+%26+dsa&page=2&limit=20
  Headers  : {'Accept': 'application/json', 'Authorization': 'Bearer tok_live_987', 'User-agent': 'PythonCompleteNotesClient/1.0'}

=== 2. Parsing URL Components Back (`urlparse` & `parse_qs`) ===
  Scheme='https', Netloc='api.example.com', Path='/v1/articles'
  Decoded Query Dict: {'q': ['python 3.13 & dsa'], 'page': ['2'], 'limit': ['20']}
```

### Output — Example 02
```text
=== 1. POST `/api/todos` (Create Resource -> HTTP 201) ===
  Status: 201 | Created: {'id': 2, 'task': 'Start Phase 6 DSA'}

=== 2. GET `/api/todos` (List Resources -> HTTP 200) ===
  Status: 200 | Todos: [{'id': 1, 'task': 'Master Phase 5'}, {'id': 2, 'task': 'Start Phase 6 DSA'}]

=== 3. Handling `HTTPError` on Unknown Route (`/api/unknown` -> HTTP 404) ===
  Caught HTTPError 404: {'error': 'Endpoint not found'}
```

### Output — Example 03
```text
=== Streaming Cursor-Paginated API with Automatic 429 Retry ===
  [backoff] HTTP 429 Too Many Requests (Retry-After: 0.01s) -> retrying 'cursor_2' (attempt 1/3)
  Collected all users across 3 pages: ['user_1', 'user_2', 'user_3', 'user_4', 'user_5']
```

---

## 7. Code Explanation

1. **`urlencode({"q": "python 3.13 & dsa", ...})` (Example 01):** Converts spaces to `+` and `&` to `%26` so the `&` inside the search query is not misinterpreted as a delimiter for a new query parameter!
2. **`HTTPServer(("127.0.0.1", 0), ...)` (Example 02):** Binding to port `0` asks the OS kernel to assign an available ephemeral localhost port (`server.server_port`), allowing deterministic end-to-end HTTP testing without port conflicts or external internet dependencies.
3. **`HTTPError` Is Also a File-Like Response (Example 02):** In `urllib`, `HTTPError` is a subclass of both `URLError` and `addinfourl`, meaning you can call `err.read()` on a `400` or `404` exception to parse the JSON error payload returned by the server!

---

## 8. Common Mistakes

1. **Omitting `timeout=` on HTTP Requests:**
   - Causes production workers to hang indefinitely on half-open TCP connections.
2. **String-Interpolating Query Parameters Manually (`f"...?q={user_input}"`):**
   - Breaks whenever `user_input` contains spaces, `&`, `=`, or `#`. Always use `urllib.parse.urlencode` (or `params=` in `requests`/`httpx`).
3. **Catching `URLError` Before `HTTPError`:**
   - Because `HTTPError` is a subclass of `URLError`, `except URLError:` will catch `HTTPError` first unless `except HTTPError:` is placed above it.
4. **Hardcoding API Keys in Source Code:**
   - Never commit API tokens into `.py` files; load them from environment variables (`os.environ["API_KEY"]`).

---

## 9. Practice Questions

1. **Easy:** Write a function `build_paginated_url(base: str, cursor: str | None, limit: int = 50) -> str` using `urllib.parse.urlencode` that omits the `cursor` parameter when `cursor is None`.
2. **Medium:** Write a function `compute_backoff_delay(attempt: int, base_delay: float = 0.5, max_delay: float = 30.0) -> float` implementing capped exponential backoff $\min(\text{max\_delay}, \text{base\_delay} \times 2^{\text{attempt} - 1})$.
3. **Hard:** Extend `MiniTodoAPIHandler` in Example 02 to support `DELETE /api/todos/<id>` (returning `204 No Content` on success or `404 Not Found` if missing) and test it with `Request(..., method="DELETE")`.

---

## 10. Interview Questions

### Q1: What does HTTP Idempotency mean, and which HTTP methods are idempotent?
**Answer:** An HTTP operation is **idempotent** if making the exact same request multiple times produces the same server state as making it once.
- **Idempotent:** `GET`, `HEAD`, `OPTIONS`, `PUT` (replaces target resource with exact payload), and `DELETE` (deleting an already-deleted resource leaves it deleted).
- **NOT Idempotent:** `POST` (repeating a `POST /orders` request without an `Idempotency-Key` header creates duplicate orders!).

### Q2: Why do production retry policies add random "jitter" to exponential backoff?
**Answer:** When a server briefly goes down or rate-limits a batch of 1,000 clients at the exact same millisecond, pure deterministic exponential backoff ($1\text{s}, 2\text{s}, 4\text{s}$) causes all 1,000 clients to retry in synchronized waves (**Thundering Herd problem**). Adding random jitter (`random.uniform(0, delay)`) spreads the retries smoothly over time.

### Q3: When using `requests` or `httpx` in production, why should you reuse a `Session` / `Client` instead of calling top-level `requests.get()` in a loop?
**Answer:** Top-level `requests.get()` opens a brand-new TCP connection and performs a full TLS handshake on every single call. Reusing a `requests.Session()` or `httpx.Client()` context manager pools and reuses underlying TCP/TLS connections (HTTP Keep-Alive), reducing latency by 50–80%.
