import http.server
import urllib.request
import urllib.error
import os
import sys

PORT = 3000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
AI_BACKEND = "http://127.0.0.1:8000"

class CutloopProxyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    def do_GET(self):
        if self.path.startswith("/api/ai"):
            self.proxy_request("GET")
        else:
            super().do_GET()

    def do_POST(self):
        if self.path.startswith("/api/ai"):
            self.proxy_request("POST")
        else:
            self.send_error(404, "Not Found")

    def proxy_request(self, method):
        target_url = f"{AI_BACKEND}{self.path}"
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else None

        req = urllib.request.Request(target_url, data=body, method=method)
        for key, val in self.headers.items():
            if key.lower() not in ["host", "content-length"]:
                req.add_header(key, val)

        try:
            with urllib.request.urlopen(req) as resp:
                self.send_response(resp.status)
                for k, v in resp.getheaders():
                    # Skip transfer-encoding chunked to avoid stream mismatch
                    if k.lower() != "transfer-encoding":
                        self.send_header(k, v)
                self.end_headers()
                self.wfile.write(resp.read())
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            for k, v in e.headers.items():
                if k.lower() != "transfer-encoding":
                    self.send_header(k, v)
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            self.send_error(502, f"AI Gateway Error: {str(e)}")

if __name__ == "__main__":
    server_address = ("0.0.0.0", PORT)
    httpd = http.server.HTTPServer(server_address, CutloopProxyHandler)
    print(f"CUTLOOP Unified Server running on http://0.0.0.0:{PORT} (serving frontend + proxying AI)")
    sys.stdout.flush()
    httpd.serve_forever()
