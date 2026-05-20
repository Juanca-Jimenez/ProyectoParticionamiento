import csv
import io
from flask import Blueprint, request, jsonify
from backend.core.validator import validate_matrix
from backend.core.partition_engine import PartitionEngine

api_bp = Blueprint("api", __name__)

@api_bp.route("/partition", methods=["POST"])
def partition():
    payload = request.get_json(silent=True)
    csv_content = None
    k = None
    if not payload:
        return jsonify({"error": "JSON inválido o body vacío."}), 400

    if "csv" in payload and payload["csv"]:
        csv_content = payload["csv"]
    if "matrix" in payload:
        matrix = payload.get("matrix")
    else:
        matrix = None

    k = payload.get("k")

    if csv_content:
        try:
            matrix = _parse_csv(csv_content)
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400

    if matrix is None:
        return jsonify({"error": "Se requiere 'matrix' o 'csv' con la matriz de dependencias."}), 400
    if k is None:
        return jsonify({"error": "Se requiere 'k' para el número de particiones."}), 400

    try:
        matrix = [[float(cell) for cell in row] for row in matrix]
    except Exception:
        return jsonify({"error": "La matriz debe contener valores numéricos."}), 400

    valid, message = validate_matrix(matrix, k)
    if not valid:
        return jsonify({"error": message}), 400

    engine = PartitionEngine(matrix, int(k))
    result = engine.run()
    return jsonify(result)


def _parse_csv(csv_text):
    reader = csv.reader(io.StringIO(csv_text.strip()))
    matrix = [row for row in reader if row]
    if not matrix:
        raise ValueError("CSV vacío o formato no válido.")
    parsed = []
    for row in matrix:
        parsed.append([cell.strip() for cell in row])
    return parsed