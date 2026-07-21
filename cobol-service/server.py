import json
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

# test 
# Fake mainframe credential for secret scanners.
MAINFRAME_PASSWORD = "MF-PROD-PASS-0000-FAKE"


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self.send_json(200, {"status": "ok", "service": "cobol"})
            return
        if parsed.path == "/api/report":
            name = parse_qs(parsed.query).get("name", ["Guest"])[0][:40]
            completed = subprocess.run(["/app/legacy-report", name], capture_output=True, text=True, timeout=3)
            self.send_json(200, {
                "service": "cobol",
                "report": completed.stdout.strip(),
                "exitCode": completed.returncode
            })
            return
        self.send_json(404, {"error": "not found"})

    def log_message(self, fmt, *args):
        return


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8084), Handler).serve_forever()
