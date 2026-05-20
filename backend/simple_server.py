
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.validator import validate_matrix
from core.partition_engine import PartitionEngine

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
        return

    def do_GET(self):
        if self.path == "/":
            self._set_headers(200, "text/plain")
            self.wfile.write(b"Servidor OK. POST /api/partition\n")
            return
        self._set_headers(404, "text/plain")
        self.wfile.write(b"Not found")

    def do_POST(self):
        if self.path != "/api/partition":
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint no encontrado."}).encode())
            return
        
        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length)
        
        try:
            payload = json.loads(raw.decode('utf-8'))
        except:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "JSON inválido."}).encode())
            return

        matrix = payload.get('matrix')
        k = payload.get('k')
        
        if not matrix:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Se requiere 'matrix'."}).encode())
            return
        
        if not k:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Se requiere 'k'."}).encode())
            return
        
        try:
            matrix = [[float(cell) for cell in row] for row in matrix]
        except:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Valores deben ser numéricos."}).encode())
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
    print(f"🚀 Servidor en http://{HOST}:{PORT}")
    server = HTTPServer((HOST, PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
        server.server_close()
