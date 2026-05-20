import os
import sys
from flask import Flask

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from backend.api.routes import api_bp

app = Flask(__name__)
app.register_blueprint(api_bp, url_prefix="/api")

@app.route("/", methods=["GET"])
def index():
    return {
        "status": "ok",
        "message": "Sistema de particionamiento de dependencias. Use /api/partition"
    }

if __name__ == "__main__":
    app.run(debug=True, port=5000)
