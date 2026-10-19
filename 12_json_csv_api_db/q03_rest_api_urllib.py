"""
Topic 12: JSON, CSV, API, Database
Question 03: REST API Basics (urllib)

A comprehensive, production-grade guide to HTTP networking and REST client operations
using Python's standard library `urllib` package (urllib.request, urllib.parse, urllib.error).
Exercises run against a lightweight local daemon HTTP server to guarantee 100% offline,
deterministic, and fast execution without external internet dependencies.

Every question contains standalone runnable exercises verified with 100% assertions.
"""

import json
import socket
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from http import cookiejar
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, Any, Optional, Tuple


# =====================================================================
# Local In-Process HTTP Mock Server for Deterministic Testing
# =====================================================================
class MockAPIHandler(BaseHTTPRequestHandler):
    """Handles mock REST endpoints for test verification."""

    def log_message(self, format, *args):
        # Suppress standard logging output during unit tests
        pass

    def handle(self):
        try:
            super().handle()
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, OSError):
            pass

    def do_GET(self):
        try:
            self._do_get_impl()
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, OSError):
            pass

    def _do_get_impl(self):
        parsed = urllib.parse.urlsplit(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy", "service": "mock_api"}).encode("utf-8"))

        elif path == "/api/search":
            q = query.get("q", [""])[0]
            limit = int(query.get("limit", [10])[0])
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"query": q, "limit": limit, "results": ["item1", "item2"]}).encode("utf-8"))

        elif path == "/api/headers":
            user_agent = self.headers.get("User-Agent", "")
            auth_header = self.headers.get("Authorization", "")
            x_request_id = self.headers.get("X-Request-ID", "")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "User-Agent": user_agent,
                "Authorization": auth_header,
                "X-Request-ID": x_request_id
            }).encode("utf-8"))

        elif path == "/api/not-found":
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Resource not found", "code": 404}).encode("utf-8"))

        elif path == "/api/server-error":
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Internal Server Error"}).encode("utf-8"))

        elif path == "/api/slow":
            # Sleep 0.25s to test timeouts
            time.sleep(0.25)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": "finished slowly"}).encode("utf-8"))

        elif path == "/api/redirect-start":
            self.send_response(302)
            self.send_header("Location", "/api/redirect-target")
            self.end_headers()

        elif path == "/api/redirect-target":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"arrived_at": "redirect-target"}).encode("utf-8"))

        elif path == "/api/set-cookie":
            self.send_response(200)
            self.send_header("Set-Cookie", "session_token=secret_xyz_123; Path=/")
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": "cookie set"}).encode("utf-8"))

        elif path == "/api/check-cookie":
            cookie_header = self.headers.get("Cookie", "")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"received_cookie": cookie_header}).encode("utf-8"))

        elif path == "/api/stream-data":
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.end_headers()
            for chunk in [b"CHUNKA__", b"CHUNKB__", b"CHUNKC__", b"CHUNKD__"]:
                self.wfile.write(chunk)
                self.wfile.flush()

        else:
            self.send_response(400)
            self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlsplit(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        if parsed.path == "/api/items":
            payload = json.loads(body.decode("utf-8"))
            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response_data = {"id": 999, "created": payload, "status": "success"}
            self.wfile.write(json.dumps(response_data).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_PUT(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        payload = json.loads(body.decode("utf-8"))
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"updated": payload}).encode("utf-8"))

    def do_DELETE(self):
        self.send_response(204)
        self.end_headers()


class SilentHTTPServer(HTTPServer):
    def handle_error(self, request, client_address):
        # Gracefully suppress client timeout disconnection traces
        pass


class LocalServerFixture:
    """Spawns an ephemeral HTTP test server in a background daemon thread."""
    def __init__(self):
        self.server = SilentHTTPServer(("127.0.0.1", 0), MockAPIHandler)
        self.port = self.server.server_address[1]
        self.base_url = f"http://127.0.0.1:{self.port}"
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    def start(self):
        self.thread.start()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()


# =====================================================================
# Q1: Basic GET Request and HTTP Response Anatomy
# =====================================================================
def q1_http_get_basics(base_url: str):
    """
    Demonstrates low-level HTTP GET request using urllib.request.urlopen,
    inspecting response code, headers, content type, and body decoding.
    """
    url = f"{base_url}/api/status"
    with urllib.request.urlopen(url) as response:
        status_code = response.status
        content_type = response.headers.get_content_type()
        charset = response.headers.get_content_charset() or "utf-8"
        raw_body = response.read()
        text = raw_body.decode(charset)
        data = json.loads(text)

    assert status_code == 200
    assert content_type == "application/json"
    assert data["status"] == "healthy"
    assert data["service"] == "mock_api"

    print("=== Q1: HTTP GET Request Anatomy Verified ===")


# =====================================================================
# Q2: URL Query Parameter Encoding, Escaping, and Decomposition
# =====================================================================
def q2_query_param_encoding_and_parsing(base_url: str):
    """
    Demonstrates urlencode, quote, parse_qs, and urlsplit for safe
    construction and decomposition of REST query strings.
    """
    # 1. Encoding special characters safely
    params = {
        "q": "python & machine learning + AI!",
        "limit": 25,
        "tags": ["web", "backend"]
    }
    encoded_query = urllib.parse.urlencode(params, doseq=True)
    assert "q=python+%26+machine+learning+%2B+AI%21" in encoded_query
    assert "tags=web&tags=backend" in encoded_query

    # 2. Sending GET with query string to test endpoint
    url = f"{base_url}/api/search?{encoded_query}"
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))

    assert res["query"] == "python & machine learning + AI!"
    assert res["limit"] == 25
    assert res["results"] == ["item1", "item2"]

    # 3. Parsing back query strings
    parsed = urllib.parse.urlsplit(url)
    assert parsed.scheme == "http"
    assert parsed.path == "/api/search"
    extracted_query = urllib.parse.parse_qs(parsed.query)
    assert extracted_query["q"] == ["python & machine learning + AI!"]
    assert extracted_query["tags"] == ["web", "backend"]

    print("=== Q2: URL Encoding and Query Parsing Verified ===")


# =====================================================================
# Q3: JSON Payload Serialization and HTTP POST Request
# =====================================================================
def q3_http_post_json_payload(base_url: str):
    """
    Constructs an HTTP POST request with serialized JSON body,
    explicit Content-Type header, and byte conversion.
    """
    url = f"{base_url}/api/items"
    payload = {"name": "Laptop Stand", "price": 49.99, "category": "Office"}

    # Serialize to bytes
    json_bytes = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url=url,
        data=json_bytes,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        method="POST"
    )

    with urllib.request.urlopen(req) as resp:
        status = resp.status
        body = json.loads(resp.read().decode("utf-8"))

    assert status == 201
    assert body["status"] == "success"
    assert body["id"] == 999
    assert body["created"]["name"] == "Laptop Stand"
    assert body["created"]["price"] == 49.99

    print("=== Q3: HTTP POST JSON Payload Verified ===")


# =====================================================================
# Q4: Custom Headers and Authorization Bearer Tokens
# =====================================================================
def q4_custom_headers_and_auth(base_url: str):
    """
    Demonstrates injecting User-Agent, Authorization Bearer tokens,
    and custom diagnostic tracing headers into HTTP requests.
    """
    url = f"{base_url}/api/headers"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.t-ID"
    trace_id = "req-uuid-1234-abcd"

    headers = {
        "User-Agent": "EnterpriseWorker/2.4 (compatible; Python/3.12)",
        "Authorization": f"Bearer {token}",
        "X-Request-ID": trace_id
    }

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        echoed = json.loads(resp.read().decode("utf-8"))

    assert echoed["User-Agent"] == "EnterpriseWorker/2.4 (compatible; Python/3.12)"
    assert echoed["Authorization"] == f"Bearer {token}"
    assert echoed["X-Request-ID"] == trace_id

    print("=== Q4: Custom Headers & Bearer Token Authentication Verified ===")


# =====================================================================
# Q5: Structured Error Handling: HTTPError vs URLError
# =====================================================================
def q5_http_error_handling(base_url: str):
    """
    Demonstrates trapping and extracting diagnostics from urllib.error.HTTPError
    (4xx, 5xx server responses with body) and urllib.error.URLError (connection failure).
    """
    # 1. 404 Not Found error trapping
    not_found_url = f"{base_url}/api/not-found"
    try:
        with urllib.request.urlopen(not_found_url):
            assert False, "Should have raised HTTPError"
    except urllib.error.HTTPError as err:
        assert err.code == 404
        error_body = json.loads(err.read().decode("utf-8"))
        assert error_body["code"] == 404
        assert "not found" in error_body["error"].lower()

    # 2. 500 Internal Server Error
    error_url = f"{base_url}/api/server-error"
    try:
        with urllib.request.urlopen(error_url):
            assert False, "Should have raised HTTPError"
    except urllib.error.HTTPError as err:
        assert err.code == 500
        error_body = json.loads(err.read().decode("utf-8"))
        assert error_body["error"] == "Internal Server Error"

    # 3. Connection refused / invalid host (URLError)
    invalid_url = "http://127.0.0.1:1"  # Port 1 is closed/privileged
    try:
        with urllib.request.urlopen(invalid_url, timeout=0.5):
            assert False, "Should have raised URLError"
    except urllib.error.URLError as err:
        assert isinstance(err, urllib.error.URLError)
        # Reason is socket error / connection refused
        assert err.reason is not None

    print("=== Q5: Structured HTTPError and URLError Diagnostics Verified ===")


# =====================================================================
# Q6: Request Timeouts and Resilient Exponential Backoff Retry Logic
# =====================================================================
def request_with_retry(
    url: str,
    max_retries: int = 3,
    timeout_sec: float = 0.1,
    backoff_factor: float = 0.05
) -> Tuple[int, Dict[str, Any]]:
    """
    Attempts to fetch a URL, catching socket timeouts and retrying with exponential backoff.
    """
    attempts = 0
    while attempts < max_retries:
        attempts += 1
        try:
            with urllib.request.urlopen(url, timeout=timeout_sec) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return resp.status, data
        except (TimeoutError, urllib.error.URLError, socket.timeout) as exc:
            if attempts >= max_retries:
                raise TimeoutError(f"Request failed after {attempts} attempts: {exc}")
            time.sleep(backoff_factor * (2 ** (attempts - 1)))

    raise RuntimeError("Unreachable")


def q6_timeouts_and_exponential_backoff(base_url: str):
    # Endpoint /api/slow takes 0.25s. With timeout 0.05s, it will repeatedly timeout.
    slow_url = f"{base_url}/api/slow"
    caught_timeout = False
    start_time = time.time()
    try:
        request_with_retry(slow_url, max_retries=2, timeout_sec=0.05, backoff_factor=0.02)
    except TimeoutError:
        caught_timeout = True
    elapsed = time.time() - start_time

    assert caught_timeout is True
    # At least two timeouts were attempted
    assert elapsed >= 0.1

    # With adequate timeout (0.5s), it succeeds immediately
    status, data = request_with_retry(slow_url, max_retries=2, timeout_sec=0.5)
    assert status == 200
    assert data["message"] == "finished slowly"

    print("=== Q6: Request Timeouts & Retry Logic Verified ===")


# =====================================================================
# Q7: HTTP Redirect Interception with Custom Opener
# =====================================================================
class DisallowRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Custom redirect handler that intercepts redirects instead of following them."""
    def http_error_302(self, req, fp, code, msg, headers):
        # Prevent auto-following and return original response or raise
        infourl = urllib.response.addinfourl(fp, headers, req.full_url, code)
        infourl.msg = msg
        return infourl

    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302


def q7_redirect_handling_and_custom_openers(base_url: str):
    url = f"{base_url}/api/redirect-start"

    # Default urllib opener automatically follows redirects (302 -> 200)
    with urllib.request.urlopen(url) as resp:
        assert resp.status == 200
        assert resp.url == f"{base_url}/api/redirect-target"
        body = json.loads(resp.read().decode("utf-8"))
        assert body["arrived_at"] == "redirect-target"

    # Custom opener installed to prevent auto-following
    opener = urllib.request.build_opener(DisallowRedirectHandler)
    response_no_follow = opener.open(url)
    assert response_no_follow.code == 302
    assert response_no_follow.headers.get("Location") == "/api/redirect-target"

    print("=== Q7: Redirect Handling and Custom Openers Verified ===")


# =====================================================================
# Q8: Stateful CookieJar Session Management
# =====================================================================
def q8_cookie_session_management(base_url: str):
    """
    Demonstrates maintaining stateful HTTP sessions using http.cookiejar.CookieJar
    and urllib.request.HTTPCookieProcessor.
    """
    cj = cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    # Request 1: Server sets cookie
    set_url = f"{base_url}/api/set-cookie"
    resp1 = opener.open(set_url)
    assert resp1.status == 200

    # Verify cookie is stored in CookieJar
    stored_cookies = list(cj)
    assert len(stored_cookies) == 1
    cookie = stored_cookies[0]
    assert cookie.name == "session_token"
    assert cookie.value == "secret_xyz_123"

    # Request 2: Send second request with opener; CookieJar sends Cookie header automatically
    check_url = f"{base_url}/api/check-cookie"
    resp2 = opener.open(check_url)
    data = json.loads(resp2.read().decode("utf-8"))

    assert "session_token=secret_xyz_123" in data["received_cookie"]

    print("=== Q8: CookieJar Session Management Verified ===")


# =====================================================================
# Q9: Chunked Binary Streaming for Large Downloads
# =====================================================================
def stream_download(url: str, chunk_size: int = 8) -> Tuple[bytes, int]:
    """Downloads response body in fixed-size binary chunks without buffering whole file in RAM."""
    total_bytes = 0
    buffer = bytearray()

    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        while True:
            chunk = resp.read(chunk_size)
            if not chunk:
                break
            total_bytes += len(chunk)
            buffer.extend(chunk)

    return bytes(buffer), total_bytes


def q9_streaming_chunked_downloads(base_url: str):
    stream_url = f"{base_url}/api/stream-data"
    data, byte_count = stream_download(stream_url, chunk_size=8)

    assert byte_count == 32
    assert data == b"CHUNKA__CHUNKB__CHUNKC__CHUNKD__"

    print("=== Q9: Chunked Binary Streaming Verified ===")


# =====================================================================
# Q10: Architectural Standard-Library RestClient Engine
# =====================================================================
class RestResponse:
    def __init__(self, status_code: int, headers: Dict[str, str], body_bytes: bytes):
        self.status_code = status_code
        self.headers = headers
        self.body_bytes = body_bytes

    def json(self) -> Any:
        return json.loads(self.body_bytes.decode("utf-8"))

    @property
    def text(self) -> str:
        return self.body_bytes.decode("utf-8")


class RestClient:
    """
    Production-grade REST API client built solely on Python's standard library.
    Features:
      - Automatic JSON serialization / deserialization
      - Base URL prefixing & query parameter construction
      - Bearer auth and default headers
      - Configurable timeouts
      - Clean method wrappers: GET, POST, PUT, DELETE
    """
    def __init__(
        self,
        base_url: str,
        auth_token: Optional[str] = None,
        default_timeout: float = 5.0,
        default_headers: Optional[Dict[str, str]] = None
    ):
        self.base_url = base_url.rstrip("/")
        self.default_timeout = default_timeout
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "AgyPythonClient/1.0",
        }
        if auth_token:
            self.headers["Authorization"] = f"Bearer {auth_token}"
        if default_headers:
            self.headers.update(default_headers)

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> RestResponse:
        url = f"{self.base_url}/{path.lstrip('/')}"
        if params:
            query_string = urllib.parse.urlencode(params, doseq=True)
            url = f"{url}?{query_string}"

        req_headers = dict(self.headers)
        if headers:
            req_headers.update(headers)

        payload_bytes = None
        if json_data is not None:
            req_headers["Content-Type"] = "application/json"
            payload_bytes = json.dumps(json_data).encode("utf-8")

        req = urllib.request.Request(
            url=url,
            data=payload_bytes,
            headers=req_headers,
            method=method.upper()
        )

        try:
            with urllib.request.urlopen(req, timeout=self.default_timeout) as resp:
                status = resp.status
                resp_headers = dict(resp.headers)
                body = resp.read()
                return RestResponse(status, resp_headers, body)
        except urllib.error.HTTPError as http_err:
            return RestResponse(http_err.code, dict(http_err.headers), http_err.read())

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> RestResponse:
        return self._request("GET", path, params=params)

    def post(self, path: str, json_data: Optional[Dict[str, Any]] = None) -> RestResponse:
        return self._request("POST", path, json_data=json_data)

    def put(self, path: str, json_data: Optional[Dict[str, Any]] = None) -> RestResponse:
        return self._request("PUT", path, json_data=json_data)

    def delete(self, path: str) -> RestResponse:
        return self._request("DELETE", path)


def q10_architectural_rest_client(base_url: str):
    client = RestClient(
        base_url=base_url,
        auth_token="token_sec_999",
        default_headers={"X-Client-App": "AntigravitySuite"}
    )

    # 1. GET with params
    resp_get = client.get("/api/search", params={"q": "distributed systems", "limit": 5})
    assert resp_get.status_code == 200
    assert resp_get.json()["limit"] == 5
    assert resp_get.json()["query"] == "distributed systems"

    # 2. POST with JSON
    resp_post = client.post("/api/items", json_data={"name": "Ergonomic Chair", "price": 350.00})
    assert resp_post.status_code == 201
    assert resp_post.json()["created"]["name"] == "Ergonomic Chair"

    # 3. PUT with JSON
    resp_put = client.put("/api/items", json_data={"name": "Updated Chair"})
    assert resp_put.status_code == 200
    assert resp_put.json()["updated"]["name"] == "Updated Chair"

    # 4. DELETE
    resp_del = client.delete("/api/items/999")
    assert resp_del.status_code == 204

    # 5. Handled 404
    resp_404 = client.get("/api/not-found")
    assert resp_404.status_code == 404
    assert "not found" in resp_404.json()["error"].lower()

    print("=== Q10: Architectural Standard-Library RestClient Verified ===")


# =====================================================================
# Main Test Runner with Ephemeral Local Server Fixture
# =====================================================================
if __name__ == "__main__":
    fixture = LocalServerFixture()
    fixture.start()
    try:
        base = fixture.base_url
        q1_http_get_basics(base)
        q2_query_param_encoding_and_parsing(base)
        q3_http_post_json_payload(base)
        q4_custom_headers_and_auth(base)
        q5_http_error_handling(base)
        q6_timeouts_and_exponential_backoff(base)
        q7_redirect_handling_and_custom_openers(base)
        q8_cookie_session_management(base)
        q9_streaming_chunked_downloads(base)
        q10_architectural_rest_client(base)

        print("\nAll 10 REST API (urllib) practice questions passed successfully!")
    finally:
        fixture.stop()
