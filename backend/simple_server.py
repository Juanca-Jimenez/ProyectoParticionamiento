import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import os
from urllib.parse import urlparse

ROOT_PARENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_PARENT not in sys.path:
    sys.path.insert(0, ROOT_PARENT)

from backend.core.validator import validate_matrix
from backend.core.partition_engine import PartitionEngine

HOST = "127.0.0.1"
PORT = 5000

class Handler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()
        # empty body for preflight
        return

    def do_GET(self):
        if self.path == "/":
            self._set_headers(200, "text/plain")
            self.wfile.write(b"Simple partitioning server. POST /api/partition\n")
            return
        self._set_headers(404, "text/plain")
        self.wfile.write(b"Not found")

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/api/partition":
            self._set_headers(404, "application/json")
            self.wfile.write(json.dumps({"error": "Endpoint no encontrado."}).encode())
            return
        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode('utf-8'))
        except Exception:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "JSON inválido."}).encode())
            return

        matrix = payload.get('matrix') or None
        csv_text = payload.get('csv') or None
        k = payload.get('k')
        if csv_text:
            # simple CSV parser
            rows = [line for line in csv_text.strip().splitlines() if line.strip()]
            matrix = [ [cell.strip() for cell in row.split(',')] for row in rows ]
        if matrix is None:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Se requiere 'matrix' o 'csv'."}).encode())
            return
        try:
            matrix = [[float(cell) for cell in row] for row in matrix]
        except Exception:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Valores de matriz deben ser numéricos."}).encode())
            return
        valid, message = validate_matrix(matrix, k)
        if not valid:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": message}).encode())
            return

        engine = PartitionEngine(matrix, int(k))
        result = engine.run()
        self._set_headers(200)
        self.wfile.write(json.dumps(result).encode())

if __name__ == '__main__':
    print(f"Starting simple server at http://{HOST}:{PORT}")
    server = HTTPServer((HOST, PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down")
        server.server_close()
