import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path == "/restaurants/open":
            query_params = parse_qs(parsed_url.query)
            date_time_str = query_params.get("datetime", [None])[0]
            if date_time_str:
                try:
                    date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
                    open_restaurants = []
                    response = open_restaurants
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())
                except ValueError:
                    self.send_error(
                        400, "Invalid datetime format. Use YYYY-MM-DD HH:MM:SS"
                    )
            else:
                self.send_error(400, "Missing datetime parameter")
        else:
            self.send_error(404, "Endpoint not found")


def run_server(port=8000):
    server_address = ("", port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"Server running on port {port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
