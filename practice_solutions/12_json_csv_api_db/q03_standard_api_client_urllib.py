"""
Question 3: Production-Grade REST API Client via urllib
Topic: JSON, CSV, Web APIs, and Databases

Key Concepts Tested:
- urllib.request, urllib.parse, and urllib.error standard library usage
- Query parameter encoding with urllib.parse.urlencode
- JSON payload encoding to UTF-8 bytes for HTTP POST
- Comprehensive error hierarchy (APIResponseError, APIConnectionError)
- Transient server error retries (500, 502, 503, 504) with exponential backoff
- Pluggable mock transport for reliable offline unit testing
"""

import io
import json
import time
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, Any, Optional, Callable


class APIResponseError(Exception):
    """Raised when an API responds with HTTP error codes (4xx, 5xx)."""

    def __init__(self, status_code: int, message: str, body: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(f"HTTP {status_code}: {message}")
        self.status_code = status_code
        self.message = message
        self.body = body or {}


class APIConnectionError(Exception):
    """Raised when network connection, DNS, or socket connection fails."""
    pass


class StandardAPIClient:
    """
    Production-grade REST client built strictly using urllib.
    Supports GET, POST, custom headers, query params, retries, and mock transports.
    """

    def __init__(
        self,
        base_url: str,
        default_timeout: float = 10.0,
        max_retries: int = 3,
        backoff_base: float = 0.05,
        transport_opener: Optional[Callable[[urllib.request.Request, float], Any]] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.default_timeout = default_timeout
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self._opener = transport_opener or self._default_opener

    @staticmethod
    def _default_opener(request: urllib.request.Request, timeout: float) -> Any:
        return urllib.request.urlopen(request, timeout=timeout)

    def _execute_with_retry(self, request: urllib.request.Request, timeout: float) -> Dict[str, Any]:
        """Executes request with exponential backoff for transient HTTP 5xx errors."""
        last_error: Optional[Exception] = None

        for attempt in range(self.max_retries + 1):
            try:
                with self._opener(request, timeout) as response:
                    raw_data = response.read().decode("utf-8")
                    status = getattr(response, "status", 200)
                    parsed_json = json.loads(raw_data) if raw_data else {}
                    return {"status": status, "data": parsed_json}

            except urllib.error.HTTPError as err:
                status_code = err.code
                error_body_raw = err.read().decode("utf-8") if err.fp else ""
                try:
                    error_json = json.loads(error_body_raw)
                    msg = error_json.get("message", error_json.get("error", str(err)))
                except Exception:
                    error_json = {}
                    msg = error_body_raw or str(err)

                # Retry transient 5xx errors
                if status_code in (500, 502, 503, 504) and attempt < self.max_retries:
                    delay = self.backoff_base * (2 ** attempt)
                    time.sleep(delay)
                    continue

                raise APIResponseError(status_code=status_code, message=msg, body=error_json)

            except (urllib.error.URLError, TimeoutError, OSError) as err:
                if attempt < self.max_retries:
                    delay = self.backoff_base * (2 ** attempt)
                    time.sleep(delay)
                    continue
                raise APIConnectionError(f"Connection failure: {err}") from err

        raise last_error or APIConnectionError("Max retries exceeded without connection")

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Performs HTTP GET request with optional query parameters."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        if params:
            query_string = urllib.parse.urlencode(params)
            url = f"{url}?{query_string}"

        req_headers = {
            "Accept": "application/json",
            "User-Agent": "StandardAPIClient/1.0 Python-urllib",
        }
        if headers:
            req_headers.update(headers)

        req = urllib.request.Request(url, headers=req_headers, method="GET")
        return self._execute_with_retry(req, timeout or self.default_timeout)

    def post(
        self,
        endpoint: str,
        payload: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Performs HTTP POST request with JSON encoded body."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        encoded_bytes = json.dumps(payload).encode("utf-8")

        req_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "StandardAPIClient/1.0 Python-urllib",
        }
        if headers:
            req_headers.update(headers)

        req = urllib.request.Request(url, data=encoded_bytes, headers=req_headers, method="POST")
        return self._execute_with_retry(req, timeout or self.default_timeout)


# ==========================================
# Mock Transport for Verification & Testing
# ==========================================
class MockHTTPResponse:
    """Simulates urllib response object."""

    def __init__(self, status: int, data: Dict[str, Any]) -> None:
        self.status = status
        self._body = json.dumps(data).encode("utf-8")

    def read(self) -> bytes:
        return self._body

    def __enter__(self) -> "MockHTTPResponse":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass


def mock_transport(req: urllib.request.Request, timeout: float) -> Any:
    """Mock handler simulating remote API endpoints without internet connection."""
    url = req.full_url
    method = req.get_method()

    if "users/99999" in url:
        # Simulate 404
        fp = io.BytesIO(json.dumps({"error": "Resource user with ID 99999 not found"}).encode("utf-8"))
        raise urllib.error.HTTPError(url, 404, "Not Found", {}, fp)

    if "users" in url and method == "GET":
        data = {
            "users": [
                {"id": f"usr_{i}", "name": f"User {i}", "role": "admin"}
                for i in range(1, 6)
            ],
            "count": 5,
        }
        return MockHTTPResponse(200, data)

    if "users" in url and method == "POST":
        return MockHTTPResponse(201, {"id": "usr_8921", "status": "created"})

    return MockHTTPResponse(200, {"status": "ok"})


if __name__ == "__main__":
    client = StandardAPIClient(
        base_url="https://api.example.com/v1",
        default_timeout=5.0,
        transport_opener=mock_transport,
    )

    print("=== 1. HTTP GET with Query Parameters ===")
    get_res = client.get("users", params={"role": "admin", "page": 1})
    print(f"GET Status Code: {get_res['status']}, Users Retrieved: {get_res['data']['count']}")
    print(f"First User Sample: {get_res['data']['users'][0]}")

    print("\n=== 2. HTTP POST with JSON Body ===")
    new_user_data = {"name": "Jordan Lee", "email": "jordan@example.com"}
    post_res = client.post("users", payload=new_user_data)
    print(f"POST Status Code: {post_res['status']}, Created User ID: '{post_res['data']['id']}'")

    print("\n=== 3. Error Handling on 404 ===")
    try:
        client.get("users/99999")
    except APIResponseError as err:
        print(f"Handled 404 APIResponseError: Status {err.status_code}, Message: '{err.message}'")
