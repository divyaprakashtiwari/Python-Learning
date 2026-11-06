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
