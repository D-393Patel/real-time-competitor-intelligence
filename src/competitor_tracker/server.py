from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .pipeline import build_insights, get_data_source_label, get_matcher_label, insights_to_dict
from .reporting import render_dashboard_html


class TrackerRequestHandler(BaseHTTPRequestHandler):
    server_version = "CompetitorTrackerHTTP/0.1"

    def do_GET(self) -> None:
        if self.path in {"/", "/dashboard"}:
            self._respond_html(
                render_dashboard_html(
                    build_insights(),
                    data_source_label=get_data_source_label(),
                    matcher_label=get_matcher_label(),
                )
            )
            return

        if self.path == "/api/insights":
            self._respond_json(
                {
                    "data_source": get_data_source_label(),
                    "matcher": get_matcher_label(),
                    "insights": insights_to_dict(build_insights()),
                }
            )
            return

        if self.path == "/health":
            self._respond_json({"status": "ok"})
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Route not found")

    def log_message(self, format: str, *args) -> None:
        return

    def _respond_html(self, content: str) -> None:
        body = content.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _respond_json(self, payload: object) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), TrackerRequestHandler)
    print(f"Serving Real-Time Competitor Strategy Tracker at http://{host}:{port}")
    print("Routes: /dashboard, /api/insights, /health")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    run_server()
