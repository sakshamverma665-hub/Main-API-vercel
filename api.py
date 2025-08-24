from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
import requests


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed_path.query)

        # Root route
        if parsed_path.path == "/":
            response = {
                "message": "API is running!",
                "usage": "/api?num=987654321",
                "owner": "@Saksham24_11"
            }
            self._send_json(response, 200)
            return

        # /get route
        if parsed_path.path == "/get":
            num = query.get("num", [None])[0]
            if not num:
                response = {"error": "Please provide ?num=xxxxxxxxxx", "owner": "@Saksham24_11"}
                self._send_json(response, 400)
                return

            try:
                url = f"https://xploide.site/Api.php?num={num}"
                res = requests.get(url, timeout=10)
                data = res.json()

                if isinstance(data, list):
                    for item in data:
                        item["owner"] = "@Saksham24_11"
                elif isinstance(data, dict):
                    data["owner"] = "@Saksham24_11"

                self._send_json(data, 200)
            except Exception as e:
                response = {"error": str(e), "owner": "@Saksham24_11"}
                self._send_json(response, 500)

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())