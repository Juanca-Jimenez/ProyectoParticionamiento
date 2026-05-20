import os
import sys
from flask import Flask

# Ensure parent project directory is on sys.path so imports work whether
# this file is executed from the package root or the backend/ folder.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    # Prefer package-style import when running as module
    from backend.api.routes import api_bp
except Exception:
    # Fallback for legacy executions from inside backend/
    from api.routes import api_bp

try:
    from flask_cors import CORS
    _have_cors = True
except Exception:
    # If flask_cors is not installed, we'll add permissive CORS headers manually
    _have_cors = False

app = Flask(__name__)

# Configurar CORS para permitir conexiones del frontend
if _have_cors:
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

@app.after_request
def _add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

app.register_blueprint(api_bp, url_prefix='/api')

@app.route("/", methods=["GET"])
def index():
    return {
        "status": "ok",
        "message": "Sistema de particionamiento de dependencias. Use /api/partition"
    }

if __name__ == "__main__":
    app.run(debug=True, port=5000)