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
    
    if result.get("status") == "success":
        ds_type = "usuario"
        if csv_content:
            ds_type = "usuario (CSV)"
        _save_run_and_update_plots(
            result.get("algorithm_used"),
            ds_type,
            result.get("n"),
            result.get("k"),
            result.get("execution_time_ms"),
            result.get("memory_peak_kb"),
            result.get("cut_value")
        )
        
    return jsonify(result)


def _save_run_and_update_plots(algorithm, dataset_type, n, k, time_ms, mem_kb, cut):
    import os
    import csv
    import sys
    
    ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
        
    try:
        from backend.analysis.benchmark_visualizer import generate_all_plots
        from backend.analysis.benchmark_report import generate_reports
    except ImportError as e:
        print(f"No se pudieron importar generadores: {e}")
        return

    csv_path1 = os.path.join(ROOT, "results", "tables", "summary_results.csv")
    csv_path2 = os.path.join(ROOT, "results", "plots", "summary_results.csv")
    
    row = {
        "algorithm": algorithm,
        "dataset_type": dataset_type,
        "n": n,
        "k": k,
        "execution_time_ms": time_ms,
        "memory_peak_kb": mem_kb,
        "cut_value": cut
    }
    
    for path in [csv_path1, csv_path2]:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            file_exists = os.path.exists(path)
            with open(path, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=[
                    "algorithm", "dataset_type", "n", "k", "execution_time_ms", "memory_peak_kb", "cut_value"
                ])
                if not file_exists:
                    writer.writeheader()
                writer.writerow(row)
        except Exception as e:
            print(f"Error escribiendo en {path}: {e}")
            
    try:
        generate_all_plots()
        generate_reports()
        print("Gráficas y reportes interactivos actualizados exitosamente.")
    except Exception as e:
        print(f"Error al regenerar gráficas/reportes: {e}")


@api_bp.route("/plots/<path:filename>", methods=["GET"])
def get_plot(filename):
    import os
    from flask import send_from_directory
    ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    plots_dir = os.path.join(ROOT, "results", "plots")
    return send_from_directory(plots_dir, filename)


def _parse_csv(csv_text):
    reader = csv.reader(io.StringIO(csv_text.strip()))
    matrix = [row for row in reader if row]
    if not matrix:
        raise ValueError("CSV vacío o formato no válido.")
    parsed = []
    for row in matrix:
        parsed.append([cell.strip() for cell in row])
    return parsed